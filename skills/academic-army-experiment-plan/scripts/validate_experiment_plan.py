"""Validate a claim-driven experiment-plan summary JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "output_files",
    "title",
    "paper_level_experimental_thesis",
    "evidence_strategy_for_paper_story",
    "claim_to_evidence_map",
    "experiment_objective_groups",
    "cross_experiment_coherence",
    "downstream_feedback_slots",
}

REQUIRED_CLAIM_FIELDS = {
    "claim_statement",
    "required_evidence",
    "objective_group",
    "evidence_role",
    "story_placement",
    "comparator_or_baseline_class",
    "dataset_benchmark_trace_workload_scene_user_deployment_or_simulation_class",
    "metric_or_observable_evidence_family",
    "minimum_convincing_result_pattern",
    "failure_or_downgrade_implication",
}

REQUIRED_OBJECTIVE_FIELDS = {
    "objective_heading",
    "purpose_in_the_paper_story",
    "supported_paper_claims",
    "evidence_role",
    "story_placement",
    "evaluation_setting",
    "comparators_and_baselines",
    "metrics_and_observable_evidence",
    "controls_variables_and_stress_conditions",
    "expected_tables_figures_or_qualitative_artifacts",
    "downstream_execution_interface",
    "evidence_maturity_and_required_confirmation",
    "priority_and_dependencies",
    "revision_and_feedback_slots",
}

REQUIRED_DOWNSTREAM_INTERFACE_FIELDS = {
    "data_handles",
    "code_model_benchmark_or_simulator_handles",
    "required_measurements_or_logging_schema",
    "expected_result_files",
    "figure_table_or_writing_consumers",
}

REQUIRED_FEEDBACK_FIELDS = {
    "experiment_execution_feedback",
    "result_analysis_feedback",
    "plotting_feedback",
    "paper_writing_feedback",
    "review_feedback",
    "revision_implication",
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

DENSE_REFERENCE_PATTERNS = {
    "C1",
    "C2",
    "B1",
    "B2",
    "M1",
    "R1",
}


def load_summary(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
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
        out: list[str] = []
        for item in value.values():
            out.extend(flatten_strings(item))
        return out
    return []


def missing_fields(obj: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(required - set(obj))


def validate_required_fields(summary: dict[str, Any], errors: list[str]) -> None:
    missing = missing_fields(summary, REQUIRED_TOP_LEVEL)
    if missing:
        errors.append(f"Missing top-level fields: {', '.join(missing)}")

    claims = summary.get("claim_to_evidence_map", [])
    if not isinstance(claims, list) or not claims:
        errors.append("claim_to_evidence_map must contain at least one claim.")
    else:
        for index, claim in enumerate(claims, start=1):
            if not isinstance(claim, dict):
                errors.append(f"Claim-to-evidence item {index} must be an object.")
                continue
            missing_claim = missing_fields(claim, REQUIRED_CLAIM_FIELDS)
            if missing_claim:
                errors.append(
                    f"Claim-to-evidence item {index} missing fields: {', '.join(missing_claim)}"
                )

    objectives = summary.get("experiment_objective_groups", [])
    if not isinstance(objectives, list) or not objectives:
        errors.append("experiment_objective_groups must contain at least one objective.")
        return

    for index, objective in enumerate(objectives, start=1):
        if not isinstance(objective, dict):
            errors.append(f"Objective group {index} must be an object.")
            continue
        missing_objective = missing_fields(objective, REQUIRED_OBJECTIVE_FIELDS)
        if missing_objective:
            errors.append(f"Objective group {index} missing fields: {', '.join(missing_objective)}")

        interface = objective.get("downstream_execution_interface")
        if not isinstance(interface, dict):
            errors.append(f"Objective group {index} must include downstream_execution_interface object.")
        else:
            missing_interface = missing_fields(interface, REQUIRED_DOWNSTREAM_INTERFACE_FIELDS)
            if missing_interface:
                errors.append(
                    f"Objective group {index} downstream interface missing: {', '.join(missing_interface)}"
                )

        feedback = objective.get("revision_and_feedback_slots")
        if not isinstance(feedback, dict):
            errors.append(f"Objective group {index} must include revision_and_feedback_slots object.")
        else:
            missing_feedback = missing_fields(feedback, REQUIRED_FEEDBACK_FIELDS)
            if missing_feedback:
                errors.append(
                    f"Objective group {index} feedback slots missing: {', '.join(missing_feedback)}"
                )


def validate_objective_headings(summary: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    headings: list[str] = []
    for objective in summary.get("experiment_objective_groups", []):
        if isinstance(objective, dict) and isinstance(objective.get("objective_heading"), str):
            headings.append(objective["objective_heading"].strip())

    if len(headings) != len(set(headings)):
        errors.append("Objective headings must be unique.")

    for heading in headings:
        if not heading:
            errors.append("Objective headings must be non-empty.")
        if heading.upper().startswith("E") and heading[1:].isdigit():
            warnings.append(
                f"Objective heading looks like a dense experiment ID instead of a semantic anchor: {heading}"
            )


def validate_content_quality(summary: dict[str, Any], warnings: list[str]) -> None:
    all_text = "\n".join(flatten_strings(summary))
    lower_text = all_text.lower()

    for pattern in PLAN_META_LEAK_PATTERNS:
        if pattern.lower() in lower_text:
            warnings.append(f"Possible meta/process leakage: {pattern}")

    for pattern in TACTICAL_SCRIPT_PATTERNS:
        if pattern in all_text:
            warnings.append(f"Possible execution-script detail in strategic plan summary: {pattern}")

    dense_hits = [pattern for pattern in DENSE_REFERENCE_PATTERNS if pattern in all_text]
    if len(dense_hits) >= 4:
        warnings.append(
            "Summary may rely on dense cross-reference codes; prefer objective headings and semantic names."
        )

    for index, objective in enumerate(summary.get("experiment_objective_groups", []), start=1):
        if not isinstance(objective, dict):
            continue
        if not objective.get("story_placement"):
            warnings.append(f"Objective group {index} has empty story_placement.")
        if not objective.get("supported_paper_claims"):
            warnings.append(f"Objective group {index} has empty supported_paper_claims.")
        if not objective.get("expected_tables_figures_or_qualitative_artifacts"):
            warnings.append(
                f"Objective group {index} has empty expected_tables_figures_or_qualitative_artifacts."
            )

        interface = objective.get("downstream_execution_interface", {})
        if isinstance(interface, dict):
            if not interface.get("expected_result_files"):
                warnings.append(f"Objective group {index} has empty expected_result_files.")
            if not interface.get("figure_table_or_writing_consumers"):
                warnings.append(f"Objective group {index} has empty figure/table/writing consumers.")


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
    validate_objective_headings(summary, errors, warnings)
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
