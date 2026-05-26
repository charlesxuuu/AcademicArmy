"""Validate the clean two-artifact experiment-plan summary JSON file."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "output_files",
    "explanation_confirmation_ledger",
    "title",
    "experimental_thesis",
    "claim_to_evidence_architecture",
    "shared_experimental_protocol",
    "experiment_objectives",
}

OPTIONAL_TOP_LEVEL = {"objective_dependency_graph"}

REMOVED_TOP_LEVEL_FIELDS = {
    "confirmation_ledger",
    "paper_level_experimental_thesis",
    "evidence_strategy_for_paper_story",
    "experiment_objective_groups",
    "cross_experiment_coherence",
    "downstream_feedback_slots",
}

REQUIRED_LEDGER_FIELDS = {
    "user_specified_facts",
    "blueprint_confirmed_facts",
    "existing_draft_note_or_result_facts",
    "live_research_context_used_in_this_version",
    "skill_derived_experiment_arrangements",
    "planning_items_closed_in_this_revision",
    "remaining_open_planning_items",
}

REQUIRED_THESIS_FIELDS = {
    "experimental_thesis",
    "primary_comparison",
    "operating_conditions",
}

REQUIRED_CLAIM_FIELDS = {
    "claim",
    "evidence_objective",
    "story_role",
    "main_artifact",
    "downstream_consumers",
}

REQUIRED_PROTOCOL_FIELDS = {
    "workloads",
    "shared_baseline_families",
    "shared_metrics",
    "shared_logging_schema",
    "shared_resource_waste_and_artifact_protocol",
    "execution_input_slots",
}

REQUIRED_WORKLOAD_FIELDS = {
    "scenes_or_datasets",
    "viewport_or_user_traces",
    "network_traces",
    "compute_or_hardware_profiles",
    "deadline_profiles",
    "other_workloads",
}

REQUIRED_METRIC_FIELDS = {
    "quality",
    "deadline_or_responsiveness",
    "resource_or_cost",
    "waste",
    "statistical_reporting",
}

REQUIRED_SHARED_LOGGING_FIELDS = {
    "required_keys",
    "required_timing_fields",
    "required_resource_fields",
    "required_quality_fields",
    "required_action_or_controller_fields",
    "required_run_metadata",
}

REQUIRED_RESOURCE_ARTIFACT_FIELDS = {
    "resource_cost_reporting",
    "waste_taxonomy",
    "artifact_manifest",
}

REQUIRED_OBJECTIVE_FIELDS = {
    "objective_heading",
    "story_role",
    "evidence_goal",
    "claims_supported",
    "decision_supported",
    "core_experiment",
    "controlled_factors",
    "comparators",
    "primary_metrics",
    "secondary_metrics",
    "target_evidence_artifacts",
    "target_evidence_pattern",
    "output_files",
    "logging_schema",
    "dependencies",
    "priority",
}

ALLOWED_STORY_ROLES = {
    "motivation",
    "problem_definition",
    "method_design_insight",
    "main_end_to_end_effectiveness",
    "mechanism_ablation",
    "robustness_stress",
    "generalization",
    "human_perceptual",
    "deployment_realism",
    "cost_scalability_reproducibility_protocol",
}

ALLOWED_PRIORITIES = {"critical", "high", "medium", "low"}

PLAN_EXPLANATION_LEAK_PATTERNS = {
    "Planning State and Source",
    "Source state",
    "Source detail",
    "Execution selection handle",
    "Intuition Made Visible",
    "Link to the Full Method Evaluation",
    "Evidence Strategy for the Paper Story",
    "Relevant live-research anchors",
    "Cross-Experiment Coherence",
    "Downstream Feedback Slots",
    "deepresearch log",
    "tool call log",
    "MCP failure",
    "why this skill",
}

DEFENSIVE_OR_QUESTIONNAIRE_PATTERNS = {
    "Assumptions to validate",
    "Questions to validate",
    "Need to validate",
    "need to verify whether",
    "if resources permit",
    "otherwise clearly label",
    "Fallback path",
    "degradation path",
    "downgrade path",
    "failure implication",
    "if the method fails",
    "negative result",
    "sufficiently stable",
    "rebuttal-ready",
    "prevents hidden cost",
    "boundary language",
}

QUESTIONNAIRE_REGEXES = {
    r"(?im)^\s*(\"[^\"]+\"\s*:\s*\")?(which|whether)\b.*\?\s*\"?,?\s*$",
    r"(?im)^\s*(\"[^\"]+\"\s*:\s*\")?(what|when|where|who|how)\b.*\?\s*\"?,?\s*$",
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

RESOURCE_ARTIFACT_OBJECTIVE_TERMS = {
    "artifact readiness",
    "resource efficiency, waste, and artifact readiness",
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


def require_object(
    parent: dict[str, Any],
    key: str,
    required: set[str],
    errors: list[str],
    context: str,
) -> dict[str, Any] | None:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{context}.{key} must be an object.")
        return None
    missing = missing_fields(value, required)
    if missing:
        errors.append(f"{context}.{key} missing fields: {', '.join(missing)}")
    return value


def validate_ledger(summary: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    ledger = summary.get("explanation_confirmation_ledger")
    if not isinstance(ledger, dict):
        errors.append("explanation_confirmation_ledger must be an object.")
        return

    missing = missing_fields(ledger, REQUIRED_LEDGER_FIELDS)
    if missing:
        errors.append(f"explanation_confirmation_ledger missing fields: {', '.join(missing)}")

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


def validate_thesis(summary: dict[str, Any], errors: list[str]) -> None:
    thesis = summary.get("experimental_thesis")
    if not isinstance(thesis, dict):
        errors.append("experimental_thesis must be an object.")
        return
    missing = missing_fields(thesis, REQUIRED_THESIS_FIELDS)
    if missing:
        errors.append(f"experimental_thesis missing fields: {', '.join(missing)}")


def validate_claims(summary: dict[str, Any], errors: list[str]) -> None:
    claims = summary.get("claim_to_evidence_architecture", [])
    if not isinstance(claims, list) or not claims:
        errors.append("claim_to_evidence_architecture must contain at least one claim.")
        return

    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            errors.append(f"Claim-to-evidence item {index} must be an object.")
            continue
        missing = missing_fields(claim, REQUIRED_CLAIM_FIELDS)
        if missing:
            errors.append(f"Claim-to-evidence item {index} missing fields: {', '.join(missing)}")
        role = claim.get("story_role")
        if isinstance(role, str) and role not in ALLOWED_STORY_ROLES:
            errors.append(f"Claim-to-evidence item {index} has invalid story_role: {role}")


def validate_shared_protocol(summary: dict[str, Any], errors: list[str]) -> None:
    protocol = summary.get("shared_experimental_protocol")
    if not isinstance(protocol, dict):
        errors.append("shared_experimental_protocol must be an object.")
        return

    missing = missing_fields(protocol, REQUIRED_PROTOCOL_FIELDS)
    if missing:
        errors.append(f"shared_experimental_protocol missing fields: {', '.join(missing)}")

    require_object(
        protocol,
        "workloads",
        REQUIRED_WORKLOAD_FIELDS,
        errors,
        "shared_experimental_protocol",
    )
    require_object(
        protocol,
        "shared_metrics",
        REQUIRED_METRIC_FIELDS,
        errors,
        "shared_experimental_protocol",
    )
    require_object(
        protocol,
        "shared_logging_schema",
        REQUIRED_SHARED_LOGGING_FIELDS,
        errors,
        "shared_experimental_protocol",
    )
    require_object(
        protocol,
        "shared_resource_waste_and_artifact_protocol",
        REQUIRED_RESOURCE_ARTIFACT_FIELDS,
        errors,
        "shared_experimental_protocol",
    )

    baseline_families = protocol.get("shared_baseline_families", [])
    if not isinstance(baseline_families, list):
        errors.append("shared_baseline_families must be a list.")
    execution_slots = protocol.get("execution_input_slots", [])
    if not isinstance(execution_slots, list):
        errors.append("execution_input_slots must be a list.")


def validate_objectives(summary: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    objectives = summary.get("experiment_objectives", [])
    if not isinstance(objectives, list) or not objectives:
        errors.append("experiment_objectives must contain at least one objective.")
        return

    headings: list[str] = []
    for index, objective in enumerate(objectives, start=1):
        if not isinstance(objective, dict):
            errors.append(f"Objective {index} must be an object.")
            continue

        missing = missing_fields(objective, REQUIRED_OBJECTIVE_FIELDS)
        if missing:
            errors.append(f"Objective {index} missing fields: {', '.join(missing)}")

        heading = objective.get("objective_heading")
        if isinstance(heading, str) and heading.strip():
            headings.append(heading.strip())
            if heading.strip().lower() in RESOURCE_ARTIFACT_OBJECTIVE_TERMS:
                warnings.append(
                    f"Objective {index} looks like a resource/artifact protocol; "
                    "represent it as a shared protocol unless it supports an independent claim."
                )
        else:
            errors.append(f"Objective {index} must have a non-empty objective_heading.")

        role = objective.get("story_role")
        if isinstance(role, str) and role not in ALLOWED_STORY_ROLES:
            errors.append(f"Objective {index} has invalid story_role: {role}")

        priority = objective.get("priority")
        if isinstance(priority, str) and priority not in ALLOWED_PRIORITIES:
            errors.append(f"Objective {index} has invalid priority: {priority}")

        if not objective.get("target_evidence_pattern"):
            errors.append(f"Objective {index} must include target_evidence_pattern.")

        if not objective.get("target_evidence_artifacts"):
            warnings.append(f"Objective {index} has empty target_evidence_artifacts.")

        if not objective.get("output_files"):
            warnings.append(f"Objective {index} has empty output_files.")

    if len(headings) != len(set(headings)):
        errors.append("Objective headings must be unique.")


def validate_dependency_graph(summary: dict[str, Any], errors: list[str]) -> None:
    graph = summary.get("objective_dependency_graph", [])
    if graph is None:
        return
    if not isinstance(graph, list):
        errors.append("objective_dependency_graph must be a list when present.")
        return
    for index, edge in enumerate(graph, start=1):
        if not isinstance(edge, dict):
            errors.append(f"Dependency graph edge {index} must be an object.")
            continue
        for field in ("from_objective_or_artifact", "to_objective_or_artifact", "evidence_chain_role"):
            if field not in edge:
                errors.append(f"Dependency graph edge {index} missing field: {field}")


def validate_content_quality(summary: dict[str, Any], warnings: list[str]) -> None:
    all_text = "\n".join(flatten_strings(summary))
    lower_text = all_text.lower()

    for pattern in PLAN_EXPLANATION_LEAK_PATTERNS:
        if pattern.lower() in lower_text:
            warnings.append(f"Possible explanation/research prose leaked into plan summary: {pattern}")

    for pattern in DEFENSIVE_OR_QUESTIONNAIRE_PATTERNS:
        if pattern.lower() in lower_text:
            warnings.append(f"Possible defensive or questionnaire language: {pattern}")

    for pattern in QUESTIONNAIRE_REGEXES:
        if re.search(pattern, all_text):
            warnings.append(f"Possible questionnaire-style open item: {pattern}")

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

    removed_present = sorted(REMOVED_TOP_LEVEL_FIELDS & set(summary))
    if removed_present:
        errors.append(
            "Summary uses removed top-level fields from the old mixed plan/explanation schema: "
            + ", ".join(removed_present)
        )

    unknown = sorted(set(summary) - REQUIRED_TOP_LEVEL - OPTIONAL_TOP_LEVEL)
    if unknown:
        warnings.append(f"Unknown top-level fields: {', '.join(unknown)}")

    validate_ledger(summary, errors, warnings)
    validate_thesis(summary, errors)
    validate_claims(summary, errors)
    validate_shared_protocol(summary, errors)
    validate_objectives(summary, errors, warnings)
    validate_dependency_graph(summary, errors)
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
