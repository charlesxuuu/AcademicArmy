#!/usr/bin/env python3
"""Validate Academic Army blueprint, analysis, or source-ledger JSON shape."""

import argparse
import json
import sys
from pathlib import Path


BLUEPRINT_TOP_LEVEL = [
    "basic_information",
    "research_idea_summary",
    "target_paper_type",
    "target_venue_or_journal",
    "research_problem",
    "motivation",
    "central_claim",
    "research_questions",
    "proposed_contribution",
    "method_or_approach",
    "data_materials_or_artifacts",
    "evaluation_or_validation_plan",
    "related_work_positioning",
    "paper_structure",
    "missing_information_and_next_actions",
]

ANALYSIS_TOP_LEVEL = [
    "analysis_summary",
    "user_provided_inputs",
    "search_process",
    "referenced_papers",
    "referenced_code_datasets_or_artifacts",
    "venue_or_journal_considerations",
    "problem_framing_rationale",
    "central_claim_rationale",
    "contribution_structure_rationale",
    "evaluation_plan_rationale",
    "assumptions_uncertainties_and_missing_information",
    "change_log",
]

LEDGER_TOP_LEVEL = [
    "blueprint_id",
    "version",
    "created_at",
    "updated_at",
    "conversation_language",
    "mode",
    "user_inputs",
    "searches",
    "assumptions",
    "changes",
]

BLUEPRINT_REQUIRED_NESTED = {
    "basic_information": [
        "field",
        "subfield",
        "paper_type",
        "target_venue_or_journal",
        "target_readers",
        "current_stage",
        "blueprint_version",
    ],
    "research_idea_summary": ["one_sentence_summary", "expanded_summary"],
    "target_paper_type": ["primary_paper_type", "secondary_paper_type", "reason"],
    "target_venue_or_journal": ["name", "venue_expectations", "fit_considerations", "constraints"],
    "research_problem": ["problem", "context", "existing_difficulty", "why_this_problem_matters"],
    "motivation": ["academic_motivation", "practical_motivation", "why_now"],
    "central_claim": ["main_claim", "conservative_version", "strong_version", "claim_scope"],
    "method_or_approach": ["core_method", "key_mechanism", "input", "output", "assumptions", "scope", "non_goals"],
    "data_materials_or_artifacts": [
        "dataset_corpus_or_case",
        "code_system_or_tool",
        "benchmark",
        "external_resources",
        "availability",
        "risks",
    ],
    "evaluation_or_validation_plan": [
        "evaluation_goal",
        "baselines_or_comparisons",
        "metrics",
        "quantitative_evaluation",
        "qualitative_evaluation",
        "ablation_or_sensitivity_analysis",
        "robustness_or_generalization_check",
    ],
    "related_work_positioning": [
        "reference_anchors",
        "closest_existing_work",
        "differentiation",
        "gap",
        "positioning_statement",
    ],
    "missing_information_and_next_actions": [
        "missing_information",
        "user_decisions_needed",
        "next_writing_actions",
    ],
}


def fail(message: str) -> int:
    print(f"[ERROR] {message}")
    return 1


def missing_keys(obj, keys):
    return [key for key in keys if key not in obj]


def require_object(data, key):
    value = data.get(key)
    if not isinstance(value, dict):
        return f"{key} must be an object"
    return None


def validate_blueprint(data) -> str | None:
    missing = missing_keys(data, BLUEPRINT_TOP_LEVEL)
    if missing:
        return f"Blueprint missing required key(s): {', '.join(missing)}"

    for key, required in BLUEPRINT_REQUIRED_NESTED.items():
        error = require_object(data, key)
        if error:
            return error
        nested_missing = missing_keys(data[key], required)
        if nested_missing:
            return f"{key} missing required key(s): {', '.join(nested_missing)}"

    for key in ("research_questions", "proposed_contribution", "paper_structure"):
        if not isinstance(data.get(key), list):
            return f"{key} must be an array"

    if len(data["research_questions"]) != 3:
        return "research_questions must contain exactly 3 items"
    if len(data["proposed_contribution"]) != 3:
        return "proposed_contribution must contain exactly 3 items"
    if len(data["paper_structure"]) < 8:
        return "paper_structure must contain at least 8 sections"
    return None


def validate_analysis(data) -> str | None:
    missing = missing_keys(data, ANALYSIS_TOP_LEVEL)
    if missing:
        return f"Analysis missing required key(s): {', '.join(missing)}"

    list_fields = [
        "user_provided_inputs",
        "search_process",
        "referenced_papers",
        "referenced_code_datasets_or_artifacts",
        "assumptions_uncertainties_and_missing_information",
        "change_log",
    ]
    for key in list_fields:
        if not isinstance(data.get(key), list):
            return f"{key} must be an array"

    if not isinstance(data.get("venue_or_journal_considerations"), dict):
        return "venue_or_journal_considerations must be an object"

    return None


def validate_ledger(data) -> str | None:
    missing = missing_keys(data, LEDGER_TOP_LEVEL)
    if missing:
        return f"Ledger missing required key(s): {', '.join(missing)}"

    for key in ("user_inputs", "searches", "assumptions", "changes"):
        if not isinstance(data.get(key), list):
            return f"{key} must be an array"
    return None


def infer_kind(data) -> str | None:
    if all(key in data for key in BLUEPRINT_TOP_LEVEL[:5]):
        return "blueprint"
    if all(key in data for key in ANALYSIS_TOP_LEVEL[:5]):
        return "analysis"
    if all(key in data for key in LEDGER_TOP_LEVEL[:5]):
        return "ledger"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="JSON file to validate")
    parser.add_argument(
        "--kind",
        choices=["auto", "blueprint", "analysis", "ledger"],
        default="auto",
        help="Artifact kind. Defaults to auto-detection.",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        return fail(f"File not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return fail(f"Invalid JSON: {exc}")

    if not isinstance(data, dict):
        return fail("Artifact must be a JSON object.")

    kind = infer_kind(data) if args.kind == "auto" else args.kind
    if not kind:
        return fail("Could not infer kind. Pass --kind blueprint, --kind analysis, or --kind ledger.")

    validators = {
        "blueprint": validate_blueprint,
        "analysis": validate_analysis,
        "ledger": validate_ledger,
    }
    error = validators[kind](data)
    if error:
        return fail(error)

    print(f"[OK] {kind} JSON has the required structure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
