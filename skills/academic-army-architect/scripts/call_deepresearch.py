#!/usr/bin/env python3
"""Call DeepResearch, the research judgment layer for Academic Army Architect.

DeepResearch is not a search helper. It is a Python-invoked OpenAI API research
component that reads, compares, synthesizes, and returns a structured report for
paper blueprint generation or revision.

Requires:
  pip install openai
  set OPENAI_API_KEY in the environment
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gpt-5.5-pro"
DEFAULT_REPORT_SCHEMA = "schemas/deepresearch_report.schema.json"


BASE_SYSTEM_MESSAGE = """DeepResearch is the research judgment layer for an academic paper blueprint system.

It reads, compares, synthesizes, and answers the focused research question in the brief.

The orchestration layer handles templates, validation, rendering, file generation, and local edits. DeepResearch provides evidence-backed recommendations for paper_blueprint.md, paper_blueprint_analysis.md, and source_ledger.json.

Output:
- Use traceable sources for papers, citations, repositories, datasets, results, and venue rules.
- Separate user-provided facts from research-supported findings and DeepResearch recommendations.
- Return source metadata for every source used.
- Mark material gaps as TBD or user_input_needed.
- Provide blueprint decisions for sections affected by the research question.
"""


QUESTION_TYPE_MESSAGES = {
    "general_blueprint_judgment": """Answer the brief as a general blueprint research judgment task. Identify the most relevant evidence, summarize key implications, and recommend blueprint decisions.""",
    "venue_style_analysis": """Analyze the target venue or journal. Focus on accepted-paper style, contribution expectations, audience, method/evaluation norms, constraints, and blueprint adaptation.""",
    "related_direction_synthesis": """Analyze the research direction around the user idea. Focus on clusters of related work, recurring problem formulations, common methods, open gaps, and where the user's idea plausibly fits.""",
    "closest_work_comparison": """Identify and compare the closest existing work. Focus on overlap, differences, novelty issues, positioning issues, and Related Work Positioning language.""",
    "contribution_boundary": """Judge contribution framing. Focus on evidence-supported contributions, claims needing confirmation, and contribution wording at different strength levels.""",
    "claim_strength": """Judge central claim strength. Focus on what the evidence supports, remaining gaps, claim strength, assumptions, and confirmations.""",
    "method_evaluation_design": """Analyze method and evaluation design. Focus on baselines, metrics, ablations, user studies, case studies, robustness checks, validity considerations, and evidence for the central claim.""",
    "artifact_landscape": """Analyze code, datasets, benchmarks, tools, protocols, and reproducibility artifacts. Focus on relevance, availability, license or activity notes when visible, and how artifacts enter the blueprint.""",
    "paper_structure_strategy": """Analyze paper organization strategy. Focus on how the problem, method, evidence, limitations, and related work are sequenced for the target paper type and venue.""",
    "revision_impact_analysis": """Analyze a requested blueprint revision. Focus on changed sections, stable sections, reusable sources, new evidence, and source ledger/change log updates.""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", required=True, help="Path to DeepResearch brief JSON")
    parser.add_argument("--output", required=True, help="Path to write DeepResearch report JSON")
    parser.add_argument("--raw-output", help="Optional path to write raw OpenAI response JSON")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model ID")
    parser.add_argument(
        "--question-type",
        choices=sorted(QUESTION_TYPE_MESSAGES),
        help="Focused DeepResearch question type. Defaults to brief.deepresearch_question_type or general_blueprint_judgment.",
    )
    parser.add_argument(
        "--system-prompt-file",
        help="Optional additional system prompt file for a custom DeepResearch question. Appended after the built-in role and question-type prompt.",
    )
    parser.add_argument(
        "--reasoning-effort",
        default="high",
        choices=["low", "medium", "high", "xhigh"],
        help="Reasoning effort for the research call",
    )
    parser.add_argument(
        "--reasoning-summary",
        default="auto",
        choices=["auto", "concise", "detailed"],
        help="Reasoning summary setting when supported",
    )
    parser.add_argument(
        "--schema",
        default=None,
        help="Path to DeepResearch report JSON schema. Defaults to schemas/deepresearch_report.schema.json beside the skill root.",
    )
    parser.add_argument(
        "--research-context-size",
        default="high",
        choices=["low", "medium", "high"],
        help="Context size for the OpenAI web research tool used inside DeepResearch",
    )
    parser.add_argument("--allowed-domain", action="append", default=[], help="Optional allowed domain; repeatable")
    parser.add_argument("--blocked-domain", action="append", default=[], help="Optional blocked domain; repeatable")
    parser.add_argument(
        "--no-code-interpreter",
        action="store_true",
        help="Disable code interpreter. Keep enabled for long research tasks that may need tabulation or comparison.",
    )
    parser.add_argument(
        "--no-background",
        action="store_true",
        help="Run synchronously instead of using background mode.",
    )
    parser.add_argument("--poll-interval", type=float, default=5.0, help="Seconds between background polling attempts")
    parser.add_argument("--timeout", type=float, default=900.0, help="Maximum seconds to wait for background completion")
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=3,
        help="Maximum DeepResearch attempts before returning failure. Defaults to 3.",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=8.0,
        help="Seconds to wait between failed DeepResearch attempts.",
    )
    return parser.parse_args()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def response_to_dict(response: Any) -> dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if hasattr(response, "dict"):
        return response.dict()
    return json.loads(json.dumps(response, default=str))


def parse_output_text(output_text: str) -> Any:
    try:
        return json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"DeepResearch returned non-JSON output: {exc}") from exc


def load_report_schema(args: argparse.Namespace) -> dict[str, Any]:
    if args.schema:
        schema_path = Path(args.schema)
    else:
        schema_path = skill_root() / DEFAULT_REPORT_SCHEMA
    return read_json(schema_path)


def resolve_question_type(args: argparse.Namespace, brief: dict[str, Any]) -> str:
    question_type = args.question_type or brief.get("deepresearch_question_type") or "general_blueprint_judgment"
    if question_type not in QUESTION_TYPE_MESSAGES:
        allowed = ", ".join(sorted(QUESTION_TYPE_MESSAGES))
        raise ValueError(f"Unknown DeepResearch question type '{question_type}'. Allowed: {allowed}")
    return question_type


def build_system_message(args: argparse.Namespace, brief: dict[str, Any]) -> str:
    question_type = resolve_question_type(args, brief)
    parts = [
        BASE_SYSTEM_MESSAGE,
        f"DeepResearch question type: {question_type}",
        QUESTION_TYPE_MESSAGES[question_type],
    ]
    if args.system_prompt_file:
        parts.append(Path(args.system_prompt_file).read_text(encoding="utf-8-sig"))
    return "\n\n".join(parts)


def build_tools(args: argparse.Namespace) -> list[dict[str, Any]]:
    web_tool: dict[str, Any] = {
        "type": "web_search",
        "search_context_size": args.research_context_size,
    }

    filters: dict[str, list[str]] = {}
    if args.allowed_domain:
        filters["allowed_domains"] = args.allowed_domain
    if args.blocked_domain:
        filters["blocked_domains"] = args.blocked_domain
    if filters:
        web_tool["filters"] = filters

    tools = [web_tool]
    if not args.no_code_interpreter:
        tools.append({"type": "code_interpreter", "container": {"type": "auto"}})
    return tools


def create_request(args: argparse.Namespace, brief: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    request: dict[str, Any] = {
        "model": args.model,
        "reasoning": {
            "effort": args.reasoning_effort,
            "summary": args.reasoning_summary,
        },
        "tools": build_tools(args),
        "input": [
            {"role": "system", "content": build_system_message(args, brief)},
            {"role": "user", "content": json.dumps(brief, ensure_ascii=False, indent=2)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "deepresearch_report",
                "strict": True,
                "schema": schema,
            }
        },
    }

    if not args.no_background:
        request["background"] = True

    return request


def wait_for_completion(client: Any, response: Any, args: argparse.Namespace) -> Any:
    if args.no_background:
        return response

    started = time.monotonic()
    while getattr(response, "status", None) in {"queued", "in_progress"}:
        if time.monotonic() - started > args.timeout:
            raise TimeoutError(f"DeepResearch did not complete within {args.timeout} seconds")
        time.sleep(args.poll_interval)
        response = client.responses.retrieve(response.id)
    return response


def run_deepresearch_once(client: Any, args: argparse.Namespace, brief: dict[str, Any], schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    response = client.responses.create(**create_request(args, brief, schema))
    response = wait_for_completion(client, response, args)

    status = getattr(response, "status", None)
    if status and status != "completed":
        raise RuntimeError(f"DeepResearch failed with status: {status}")

    raw = response_to_dict(response)
    output_text = getattr(response, "output_text", "") or raw.get("output_text", "")
    report = parse_output_text(output_text)
    return report, raw


def run_deepresearch_with_retries(client: Any, args: argparse.Namespace, brief: dict[str, Any], schema: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if args.max_attempts < 1:
        raise ValueError("--max-attempts must be at least 1")

    last_error: Exception | None = None
    for attempt in range(1, args.max_attempts + 1):
        try:
            print(f"[INFO] DeepResearch attempt {attempt}/{args.max_attempts}", file=sys.stderr)
            return run_deepresearch_once(client, args, brief, schema)
        except Exception as exc:  # noqa: BLE001 - retry boundary with final re-raise.
            last_error = exc
            print(f"[ERROR] DeepResearch attempt {attempt}/{args.max_attempts} failed: {exc}", file=sys.stderr)
            if attempt < args.max_attempts:
                time.sleep(args.retry_delay)

    raise RuntimeError(
        f"DeepResearch failed after {args.max_attempts} attempts. "
        "No report was written; research-dependent outputs stay unchanged."
    ) from last_error


def main() -> int:
    args = parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY is not set.", file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("[ERROR] Missing dependency. Install with: pip install openai", file=sys.stderr)
        return 2

    brief = read_json(Path(args.brief))
    schema = load_report_schema(args)

    client = OpenAI()
    try:
        report, raw = run_deepresearch_with_retries(client, args, brief, schema)
    except Exception as exc:  # noqa: BLE001 - CLI boundary returns a clear error.
        print(f"[FATAL] {exc}", file=sys.stderr)
        return 1

    write_json(Path(args.output), report)
    if args.raw_output:
        write_json(Path(args.raw_output), raw)

    print(f"[OK] DeepResearch report written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
