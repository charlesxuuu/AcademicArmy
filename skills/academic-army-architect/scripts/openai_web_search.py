#!/usr/bin/env python3
"""Run an OpenAI Responses API web-search pass for Academic Army Architect.

This script turns a research query into structured source records that can be
copied into paper_blueprint_analysis.md and source_ledger.json.

Requires:
  pip install openai
  set OPENAI_API_KEY in the environment
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_TYPES = [
    "paper",
    "code",
    "dataset",
    "benchmark",
    "venue_guideline",
    "documentation",
    "other_artifact",
]

SEARCH_RESULT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "search_summary",
        "sources_consulted",
        "positioning_notes",
        "missing_information",
        "suggested_followup_queries",
    ],
    "properties": {
        "search_summary": {"type": "string"},
        "sources_consulted": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "source_id",
                    "type",
                    "title_or_name",
                    "authors_or_owner",
                    "year_or_date",
                    "venue_or_platform",
                    "url_or_doi",
                    "citation_signal",
                    "reason_for_inclusion",
                    "blueprint_sections_influenced",
                    "confidence_level",
                    "limitations_or_caveats",
                ],
                "properties": {
                    "source_id": {"type": "string"},
                    "type": {"type": "string", "enum": SOURCE_TYPES},
                    "title_or_name": {"type": "string"},
                    "authors_or_owner": {"type": "string"},
                    "year_or_date": {"type": "string"},
                    "venue_or_platform": {"type": "string"},
                    "url_or_doi": {"type": "string"},
                    "citation_signal": {"type": "string"},
                    "reason_for_inclusion": {"type": "string"},
                    "blueprint_sections_influenced": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "confidence_level": {"type": "string", "enum": ["low", "medium", "high"]},
                    "limitations_or_caveats": {"type": "string"},
                },
            },
        },
        "positioning_notes": {"type": "array", "items": {"type": "string"}},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "suggested_followup_queries": {"type": "array", "items": {"type": "string"}},
    },
}


SYSTEM_PROMPT = """You are the search layer for Academic Army Architect.
Search for sources that can ground a standardized academic paper blueprint.
Do not invent citations, repositories, datasets, benchmarks, or venue rules.
Separate user-provided ideas from web-supported positioning.
Return concise structured JSON that records source metadata, relevance,
blueprint sections influenced, confidence, and limitations.
If citation counts or repository health are not verified, write "Not verified".
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Search query or research question")
    parser.add_argument("--purpose", default="related_paper_search", help="Search purpose, such as related_paper_search or venue_search")
    parser.add_argument("--search-id", default="S1", help="Search ID to store in the ledger")
    parser.add_argument("--context", help="Inline research context to include")
    parser.add_argument("--context-file", help="Path to a text/Markdown file with research context")
    parser.add_argument("--model", default="gpt-5.5-pro", help="OpenAI model ID")
    parser.add_argument("--reasoning-effort", default="high", choices=["low", "medium", "high", "xhigh"], help="Reasoning effort")
    parser.add_argument("--search-context-size", default="high", choices=["low", "medium", "high"], help="Web search context size")
    parser.add_argument("--allowed-domain", action="append", default=[], help="Allowed search domain; repeatable")
    parser.add_argument("--blocked-domain", action="append", default=[], help="Blocked search domain; repeatable")
    parser.add_argument("--tool-choice", default="required", choices=["required", "auto"], help="Use required for mandatory search passes")
    parser.add_argument("--no-structured-output", action="store_true", help="Disable JSON schema response formatting")
    parser.add_argument("--output", help="Write normalized result JSON to this path")
    parser.add_argument("--raw-output", help="Optionally write raw API response JSON to this path")
    return parser.parse_args()


def read_context(args: argparse.Namespace) -> str:
    parts: list[str] = []
    if args.context:
        parts.append(args.context)
    if args.context_file:
        parts.append(Path(args.context_file).read_text(encoding="utf-8-sig"))
    return "\n\n".join(part for part in parts if part.strip())


def build_web_search_tool(args: argparse.Namespace) -> dict[str, Any]:
    tool: dict[str, Any] = {
        "type": "web_search",
        "search_context_size": args.search_context_size,
    }
    filters: dict[str, list[str]] = {}
    if args.allowed_domain:
        filters["allowed_domains"] = args.allowed_domain
    if args.blocked_domain:
        filters["blocked_domains"] = args.blocked_domain
    if filters:
        tool["filters"] = filters
    return tool


def extract_possible_api_sources(raw: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            sources = value.get("sources")
            if isinstance(sources, list):
                for item in sources:
                    if isinstance(item, dict):
                        found.append(item)
            annotations = value.get("annotations")
            if isinstance(annotations, list):
                for item in annotations:
                    if isinstance(item, dict) and ("url" in item or "title" in item):
                        found.append(item)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(raw)
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in found:
        key = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def response_to_dict(response: Any) -> dict[str, Any]:
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if hasattr(response, "dict"):
        return response.dict()
    return json.loads(json.dumps(response, default=str))


def parse_output_text(output_text: str) -> Any:
    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return {"unparsed_output_text": output_text}


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

    context = read_context(args)
    user_payload = {
        "search_id": args.search_id,
        "purpose": args.purpose,
        "query": args.query,
        "research_context": context or "TBD",
        "required_source_types": SOURCE_TYPES,
        "output_use": "paper_blueprint_analysis.md and source_ledger.json",
    }

    request: dict[str, Any] = {
        "model": args.model,
        "reasoning": {"effort": args.reasoning_effort},
        "tools": [build_web_search_tool(args)],
        "tool_choice": args.tool_choice,
        "include": ["web_search_call.action.sources"],
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False, indent=2)},
        ],
    }
    if not args.no_structured_output:
        request["text"] = {
            "format": {
                "type": "json_schema",
                "name": "academic_army_search_result",
                "strict": True,
                "schema": SEARCH_RESULT_SCHEMA,
            }
        }

    client = OpenAI()
    response = client.responses.create(**request)
    raw = response_to_dict(response)
    output_text = getattr(response, "output_text", "") or raw.get("output_text", "")
    parsed = parse_output_text(output_text)

    normalized = {
        "search_id": args.search_id,
        "purpose": args.purpose,
        "query": args.query,
        "date": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "tool_choice": args.tool_choice,
        "search_context_size": args.search_context_size,
        "allowed_domains": args.allowed_domain,
        "blocked_domains": args.blocked_domain,
        "result": parsed,
        "api_sources": extract_possible_api_sources(raw),
    }

    rendered = json.dumps(normalized, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    if args.raw_output:
        Path(args.raw_output).write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())