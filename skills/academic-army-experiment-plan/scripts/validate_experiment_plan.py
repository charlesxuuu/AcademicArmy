"""Validate a venue-calibrated experiment-plan summary JSON file."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "output_files",
    "title",
    "experiment_plan_identity",
    "empirical_evidence_thesis",
    "claim_to_evidence_map",
    "evaluation_posture",
    "experiment_inventory",
    "experiment_cards",
    "execution_dependency_graph",
    "result_interpretation_rules",
    "figure_table_interface",
    "downstream_interfaces",
}

REQUIRED_CARD_FIELDS = {
    "experiment_id",
    "title",
    "evidence_objective",
    "claim_supported",
    "venue_reviewer_pressure_addressed",
    "evaluation_setting",
    "comparators",
    "metrics",
    "protocol",
    "controls_and_fairness_constraints",
    "expected_result_pattern",
    "interpretation_rule",
    "output_artifact",
    "dependencies",
    "revision_implication",
}

REQUIRED_INTERPRETATION_FIELDS = {
    "strong_result",
    "mixed_result",
    "weak_result",
    "negative_result",
}

PLAN_META_LEAK_PATTERNS = {
    "deepresearch log",
    "tool call log",
    "MCP failure",
    "why this skill",
    "why output two files",
    "Do not assume reviewers will run code",
    "Artifact cautions",
    "Assumptions to validate",
}

TACTICAL_SCRIPT_PATTERNS = {
    "python train.py",
    "bash ",
    "sbatch ",
    "CUDA_VISIBLE_DEVICES",
    "--learning-rate",
    "--dataset",
}


def load_summary(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "experiment_plan_summary" in data:
        data = data["experiment_plan_summary"]
    if not isinstance(data, dict):
        raise ValueError("Summary root must be an object.")
    return data


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten_strings(item))
        return out
    if isinstance(value, dict):
        out = []
        for item in value.values():
            out.extend(flatten_strings(item))
        return out
    return []


def validate_required_fields(summary: dict[str, Any], errors: list[str]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(summary))
    if missing:
        errors.append(f"Missing top-level fields: {', '.join(missing)}")

    claims = summary.get("claim_to_evidence_map", [])
    if not isinstance(claims, list) or not claims:
        errors.append("claim_to_evidence_map must contain at least one claim.")

    cards = summary.get("experiment_cards", [])
    if not isinstance(cards, list) or not cards:
        errors.append("experiment_cards must contain at least one Experiment Card.")
        return

    for index, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            errors.append(f"Experiment card {index} must be an object.")
            continue
        missing_card = sorted(REQUIRED_CARD_FIELDS - set(card))
        if missing_card:
            errors.append(f"Experiment card {index} missing fields: {', '.join(missing_card)}")
        interpretation = card.get("interpretation_rule")
        if not isinstance(interpretation, dict):
            errors.append(f"Experiment card {index} must include interpretation_rule object.")
        else:
            missing_interp = sorted(REQUIRED_INTERPRETATION_FIELDS - set(interpretation))
            if missing_interp:
                errors.append(
                    f"Experiment card {index} interpretation_rule missing: {', '.join(missing_interp)}"
                )


def validate_experiment_ids(summary: dict[str, Any], errors: list[str]) -> None:
    ids = []
    for card in summary.get("experiment_cards", []):
        if isinstance(card, dict) and isinstance(card.get("experiment_id"), str):
            ids.append(card["experiment_id"])
    if len(ids) != len(set(ids)):
        errors.append("Experiment IDs must be unique.")
    invalid = [exp_id for exp_id in ids if not re.fullmatch(r"E\d+", exp_id)]
    if invalid:
        errors.append(f"Experiment IDs should use E<n> format: {', '.join(invalid)}")


def validate_content_quality(summary: dict[str, Any], warnings: list[str]) -> None:
    all_text = "\n".join(flatten_strings(summary))
    for pattern in PLAN_META_LEAK_PATTERNS:
        if pattern.lower() in all_text.lower():
            warnings.append(f"Possible meta/process leakage: {pattern}")
    for pattern in TACTICAL_SCRIPT_PATTERNS:
        if pattern in all_text:
            warnings.append(f"Possible execution-script detail in planning summary: {pattern}")

    for index, card in enumerate(summary.get("experiment_cards", []), start=1):
        if not isinstance(card, dict):
            continue
        if not card.get("comparators"):
            warnings.append(f"Experiment card {index} has empty comparators.")
        if not card.get("metrics"):
            warnings.append(f"Experiment card {index} has empty metrics.")
        if not card.get("output_artifact"):
            warnings.append(f"Experiment card {index} has empty output_artifact.")
        if not card.get("controls_and_fairness_constraints"):
            warnings.append(f"Experiment card {index} has empty fairness constraints.")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_experiment_plan.py <experiment-plan-summary.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    errors: list[str] = []
    warnings: list[str] = []

    try:
        summary = load_summary(path)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: failed to load JSON: {exc}", file=sys.stderr)
        return 1

    validate_required_fields(summary, errors)
    validate_experiment_ids(summary, errors)
    validate_content_quality(summary, warnings)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        return 1
    print("Experiment-plan summary validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
