"""Validate a confirmation-state-aware experiment-plan summary JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "output_files",
    "confirmation_ledger",
    "title",
    "paper_level_experimental_thesis",
    "evidence_strategy_for_paper_story",
    "claim_to_evidence_map",
    "experiment_objective_groups",
    "cross_experiment_coherence",
    "downstream_feedback_slots",
}

REQUIRED_LEDGER_FIELDS = {
    "user_specified_facts",
    "blueprint_confirmed_facts",
    "existing_draft_note_or_result_facts",
    "runtime_research_facts_used_in_this_version",
    "planning_commitments_derived_from_those_facts",
    "planning_items_closed_in_this_revision",
    "remaining_open_planning_items",
}

REQUIRED_CLAIM_FIELDS = {
    "paper_claim",
    "required_evidence",
    "objective_heading",
    "story_placement",
    "planning_state",
    "comparator_or_baseline_class",
    "dataset_benchmark_trace_workload_scene_user_deployment_or_simulation_class",
    "metric_or_observable_evidence_family",
    "intended_reader_takeaway",
}

REQUIRED_OBJECTIVE_FIELDS = {
    "objective_heading",
    "story_placement",
    "evidence_role",
    "supported_paper_claims",
    "planning_state_and_source",
    "evaluation_setting",
    "comparators_and_baselines",
    "metrics_and_observable_evidence",
    "controls_variables_and_stress_conditions",
    "expected_tables_figures_or_qualitative_artifacts",
    "downstream_execution_interface",
    "priority_and_dependencies",
}

REQUIRED_PLANNING_STATE_FIELDS = {
    "source_state",
    "source_detail",
    "execution_selection_handle",
}

REQUIRED_MOTIVATION_FIELDS = {
    "intuition_made_visible",
    "minimal_demonstration_setting",
    "one_glance_evidence_artifact",
    "link_to_the_full_method_evaluation",
}

REQUIRED_DOWNSTREAM_INTERFACE_FIELDS = {
    "data_handles",
    "code_model_benchmark_or_simulator_handles",
    "required_measurements_or_logging_schema",
    "expected_result_files",
    "figure_table_or_writing_consumers",
}

ALLOWED_SOURCE_STATES = {
    "user_specified",
    "blueprint_confirmed",
    "existing_evidence",
    "live_research_selected",
    "skill_derived",
    "open_input",
}

MOTIVATION_ROLES = {"motivation", "design_insight"}

LEGACY_OR_DEFENSIVE_PATTERNS = {
    "Assumptions to validate",
    "Questions to validate",
    "Need to validate",
    "need to verify whether",
    "Fallback path",
    "degradation path",
    "downgrade path",
    "failure implication",
    "if the method fails",
    "negative result",
}

PLAN_META_LEAK_PATTERNS = {
    "deepresearch log",
    "tool call log",
    "MCP failure",
    "why this skill",
    "Do not assume reviewers will run code",
    "Artifact cautions",
}

TACTICAL_SCRIPT_PATTERNS = {
    "python train.py",
    "bash ",
    "sbatch ",
    "CUDA_VISIBLE_DEVICES",
    "--learning-rate",
    "--dataset",
}

DENSE_REFERENCE_PATTERNS = {"C1", "C2", "B1", "B2", "M1", "R1", "E1", "E2"}


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


def validate_ledger(summary: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    ledger = summary.get("confirmation_ledger")
    if not isinstance(ledger, dict):
        errors.append("confirmation_ledger must be an object.")
        return

    missing = missing_fields(ledger, REQUIRED_LEDGER_FIELDS)
    if missing:
        errors.append(f"confirmation_ledger missing fields: {', '.join(missing)}")

    remaining = ledger.get("remaining_open_planning_items", [])
    if remaining is None:
        return
    if not isinstance(remaining, list):
        errors.append("remaining_open_planning_items must be a list.")
        return
    for index, item in enumerate(remaining, start=1):
        if not isinstance(item, dict):
            errors.append(f"Remaining open planning item {index} must be an object.")
            continue
        for field in ("item", "why_it_changes_plan_structure", "affected_objective_or_claim"):
            if field not in item:
                errors.append(f"Remaining open planning item {index} missing field: {field}")
        if not item.get("why_it_changes_plan_structure"):
            warnings.append(
                f"Remaining open planning item {index} lacks a structure-changing reason."
            )


def validate_claims(summary: dict[str, Any], errors: list[str]) -> None:
    claims = summary.get("claim_to_evidence_map", [])
    if not isinstance(claims, list) or not claims:
        errors.append("claim_to_evidence_map must contain at least one claim.")
        return

    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            errors.append(f"Claim-to-evidence item {index} must be an object.")
            continue
        missing = missing_fields(claim, REQUIRED_CLAIM_FIELDS)
        if missing:
            errors.append(f"Claim-to-evidence item {index} missing fields: {', '.join(missing)}")
        state = claim.get("planning_state")
        if isinstance(state, str) and state not in ALLOWED_SOURCE_STATES:
            errors.append(f"Claim-to-evidence item {index} has invalid planning_state: {state}")


def objective_roles(objective: dict[str, Any]) -> set[str]:
    roles = objective.get("evidence_role", [])
    if isinstance(roles, str):
        return {roles}
    if isinstance(roles, list):
        return {role for role in roles if isinstance(role, str)}
    return set()


def validate_objectives(summary: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    objectives = summary.get("experiment_objective_groups", [])
    if not isinstance(objectives, list) or not objectives:
        errors.append("experiment_objective_groups must contain at least one objective.")
        return

    headings: list[str] = []
    for index, objective in enumerate(objectives, start=1):
        if not isinstance(objective, dict):
            errors.append(f"Objective group {index} must be an object.")
            continue

        missing = missing_fields(objective, REQUIRED_OBJECTIVE_FIELDS)
        if missing:
            errors.append(f"Objective group {index} missing fields: {', '.join(missing)}")

        heading = objective.get("objective_heading")
        if isinstance(heading, str) and heading.strip():
            headings.append(heading.strip())
        else:
            errors.append(f"Objective group {index} must have a non-empty objective_heading.")

        planning_state = objective.get("planning_state_and_source")
        if not isinstance(planning_state, dict):
            errors.append(f"Objective group {index} must include planning_state_and_source object.")
        else:
            missing_state = missing_fields(planning_state, REQUIRED_PLANNING_STATE_FIELDS)
            if missing_state:
                errors.append(
                    f"Objective group {index} planning_state_and_source missing: {', '.join(missing_state)}"
                )
            state = planning_state.get("source_state")
            if isinstance(state, str) and state not in ALLOWED_SOURCE_STATES:
                errors.append(f"Objective group {index} has invalid source_state: {state}")

        interface = objective.get("downstream_execution_interface")
        if not isinstance(interface, dict):
            errors.append(f"Objective group {index} must include downstream_execution_interface object.")
        else:
            missing_interface = missing_fields(interface, REQUIRED_DOWNSTREAM_INTERFACE_FIELDS)
            if missing_interface:
                errors.append(
                    f"Objective group {index} downstream interface missing: {', '.join(missing_interface)}"
                )

        roles = objective_roles(objective)
        motivation_fields = objective.get("motivation_design_insight_fields")
        if roles & MOTIVATION_ROLES:
            if not isinstance(motivation_fields, dict):
                errors.append(
                    f"Objective group {index} has motivation/design-insight role but no motivation_design_insight_fields object."
                )
            else:
                missing_motivation = missing_fields(motivation_fields, REQUIRED_MOTIVATION_FIELDS)
                if missing_motivation:
                    errors.append(
                        f"Objective group {index} motivation fields missing: {', '.join(missing_motivation)}"
                    )
                for field in REQUIRED_MOTIVATION_FIELDS:
                    if not motivation_fields.get(field):
                        warnings.append(
                            f"Objective group {index} motivation field is empty: {field}"
                        )

        if not objective.get("expected_tables_figures_or_qualitative_artifacts"):
            warnings.append(
                f"Objective group {index} has empty expected_tables_figures_or_qualitative_artifacts."
            )

    if len(headings) != len(set(headings)):
        errors.append("Objective headings must be unique.")


def validate_content_quality(summary: dict[str, Any], warnings: list[str]) -> None:
    all_text = "\n".join(flatten_strings(summary))
    lower_text = all_text.lower()

    for pattern in LEGACY_OR_DEFENSIVE_PATTERNS:
        if pattern.lower() in lower_text:
            warnings.append(f"Possible legacy defensive planning language: {pattern}")

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

    missing = missing_fields(summary, REQUIRED_TOP_LEVEL)
    if missing:
        errors.append(f"Missing top-level fields: {', '.join(missing)}")

    validate_ledger(summary, errors, warnings)
    validate_claims(summary, errors)
    validate_objectives(summary, errors, warnings)
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
