#!/usr/bin/env python3
"""Validate the basic shape of an Academic Army paper blueprint JSON file."""

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = [
    "basic_information",
    "one_sentence_paper_idea",
    "research_problem",
    "motivation_and_importance",
    "central_claim",
    "proposed_contribution",
    "method_or_approach",
    "expected_evidence",
    "evaluation_or_validation_plan",
    "paper_structure",
    "missing_information",
    "next_writing_actions",
]

REQUIRED_BASIC_INFO = [
    "field",
    "subfield",
    "paper_type",
    "target_venue",
    "target_readers",
    "current_stage",
    "existing_materials",
    "constraints",
]

REQUIRED_EVIDENCE = [
    "evidence_type",
    "existing_evidence",
    "missing_evidence",
    "evidence_to_claim_fit",
]


def fail(message: str) -> int:
    print(f"[ERROR] {message}")
    return 1


def require_keys(obj, keys, label):
    missing = [key for key in keys if key not in obj]
    if missing:
        return f"{label} missing required key(s): {', '.join(missing)}"
    return None


def main() -> int:
    if len(sys.argv) != 2:
        return fail("Usage: validate_blueprint_json.py <blueprint.json>")

    path = Path(sys.argv[1])
    if not path.exists():
        return fail(f"File not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return fail(f"Invalid JSON: {exc}")

    if not isinstance(data, dict):
        return fail("Blueprint must be a JSON object.")

    for error in (
        require_keys(data, REQUIRED_TOP_LEVEL, "Blueprint"),
        require_keys(data.get("basic_information", {}), REQUIRED_BASIC_INFO, "basic_information")
        if isinstance(data.get("basic_information"), dict)
        else "basic_information must be an object",
        require_keys(data.get("expected_evidence", {}), REQUIRED_EVIDENCE, "expected_evidence")
        if isinstance(data.get("expected_evidence"), dict)
        else "expected_evidence must be an object",
    ):
        if error:
            return fail(error)

    if not isinstance(data.get("proposed_contribution"), list):
        return fail("proposed_contribution must be an array.")
    if not isinstance(data.get("paper_structure"), list):
        return fail("paper_structure must be an array.")
    if not isinstance(data.get("missing_information"), list):
        return fail("missing_information must be an array.")
    if not isinstance(data.get("next_writing_actions"), list):
        return fail("next_writing_actions must be an array.")

    print("[OK] Blueprint JSON has the required structure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
