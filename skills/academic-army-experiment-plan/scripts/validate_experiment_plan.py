"""Validate the multi-artifact experiment-plan summary JSON file."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "output_files",
    "explanation_confirmation_ledger",
    "research_context_summary",
    "title",
    "experimental_thesis",
    "claim_to_evidence_architecture",
    "plan_references",
    "shared_protocol_summary",
    "experiment_objectives",
    "derived_analyses",
    "objective_dependency_graph",
    "interface_contracts_summary",
    "metric_contracts_summary",
}

REMOVED_TOP_LEVEL_FIELDS = {
    "confirmation_ledger",
    "paper_level_experimental_thesis",
    "evidence_strategy_for_paper_story",
    "experiment_objective_groups",
    "cross_experiment_coherence",
    "downstream_feedback_slots",
    "shared_experimental_protocol",
}

REQUIRED_OUTPUT_FILES = {
    "experiment_plan_markdown",
    "explanation_markdown",
    "interface_contracts_yaml",
    "metric_contracts_yaml",
    "research_context_markdown",
    "plan_language",
    "explanation_language_suffix",
}

REQUIRED_LEDGER_FIELDS = {
    "user_specified_facts",
    "blueprint_confirmed_facts",
    "existing_draft_note_or_result_facts",
    "live_research_context_used_in_this_version",
    "skill_derived_experiment_arrangements",
    "planning_items_closed_in_this_revision",
    "remaining_open_planning_items",
    "required_explanation_headings",
}

REQUIRED_RESEARCH_CONTEXT_FIELDS = {
    "research_context_ref",
    "last_verified_at",
    "target_venue",
    "field",
    "exported_ids",
    "source_backed_anchors",
}

REQUIRED_EXPORTED_ID_FIELDS = {"baseline_ids", "workload_ids", "metric_ids"}

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

REQUIRED_PLAN_REFERENCE_FIELDS = {
    "research_context_ref",
    "interface_contracts_ref",
    "metric_contracts_ref",
}

REQUIRED_PROTOCOL_SUMMARY_FIELDS = {
    "required_workload_ids",
    "scope_extension_workload_candidate_ids",
    "required_baseline_ids",
    "diagnostic_baseline_ids",
    "upper_bound_ids",
    "primary_metric_ids",
    "secondary_metric_ids",
    "cost_or_waste_metric_ids",
    "logging_schema_ref",
    "artifact_manifest_ref",
    "execution_input_slots_ref",
}

REQUIRED_OBJECTIVE_FIELDS = {
    "objective_heading",
    "story_role",
    "primary_claim",
    "evidence_goal",
    "claims_supported",
    "evidence_outputs",
    "writing_scope_outputs",
    "boundary",
    "core_experiment",
    "controlled_factors",
    "comparator_ids",
    "primary_metric_ids",
    "secondary_metric_ids",
    "target_evidence_artifacts",
    "target_evidence_pattern",
    "output_files",
    "logging_schema_ref",
    "reuse_policy",
    "dependencies",
    "priority",
}

REQUIRED_BOUNDARY_FIELDS = {"includes", "excludes"}
REQUIRED_REUSE_POLICY_FIELDS = {"base_runs_from", "new_runs_only_for"}

REQUIRED_DERIVED_ANALYSIS_FIELDS = {
    "analysis_heading",
    "inputs",
    "evidence_outputs",
    "output_files",
    "consumers",
    "contract_refs",
}

REQUIRED_INTERFACE_FIELDS = {
    "workloads",
    "baselines",
    "logging_schema",
    "execution_input_slots",
    "artifact_manifest",
}

REQUIRED_WORKLOAD_FIELDS = {
    "required_workloads",
    "scope_extension_workload_candidates",
}

REQUIRED_REQUIRED_WORKLOAD_FIELDS = {
    "scenes_or_datasets",
    "viewport_or_user_traces",
    "network_traces",
    "compute_or_hardware_profiles",
    "deadline_profiles",
}

REQUIRED_BASELINE_GROUPS = {
    "required_baselines",
    "diagnostic_baselines",
    "upper_bounds",
}

REQUIRED_BASELINE_FIELDS = {
    "baseline_id",
    "role",
    "available_state",
    "state_used_by_policy",
    "forbidden_state_usage",
    "action_space",
    "resource_budget",
    "implementation_status",
    "implementation_owner",
    "acceptable_implementations",
    "minimum_contract",
    "fairness_constraint",
    "allowed_use",
    "used_by_objectives",
}

REQUIRED_LOGGING_FIELDS = {
    "required_keys",
    "required_timing_fields",
    "required_resource_fields",
    "required_quality_fields",
    "required_action_or_controller_fields",
    "required_run_metadata",
}

REQUIRED_METRIC_FIELDS = {
    "metric_id",
    "type",
    "unit_or_range",
    "sign",
    "definition_status",
    "definition_owner",
    "formula_id",
    "required_inputs",
    "aggregation_policy",
    "used_by_objectives",
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
}

ALLOWED_PRIORITIES = {"critical", "high", "medium", "low"}

ALLOWED_DOWNSTREAM_CONSUMERS = {
    "experiment_runner",
    "code_generation",
    "result_analysis",
    "plot_planning",
    "paper_writing",
    "rebuttal_preparation",
    "reproducibility",
}

ALLOWED_BASELINE_ALLOWED_USE = {
    "main_comparison",
    "diagnostic",
    "oracle_upper_bound",
    "ablation_only",
}

ALLOWED_DEFINITION_STATUS = {"confirmed", "delegated", "unresolved"}

REMOVED_OBJECTIVE_FIELDS = {"decision_supported", "claim_calibration_output"}
REMOVED_PROTOCOL_FIELDS = {"shared_baseline_families", "verified_research_context_ids"}

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
    "when available",
    "if resources permit",
    "otherwise clearly label",
    "should remain",
    "narrower claim",
    "hidden substrate cost",
    "cannot reproduce",
    "claim holds",
    "joint allocation is valuable",
    "hide cost",
    "Fallback path",
    "degradation path",
    "downgrade path",
    "failure implication",
    "if the method fails",
    "negative result",
    "sufficiently stable",
    "rebuttal-ready",
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


def normalize_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


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


def require_list(value: Any, name: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{name} must be a list.")
        return []
    return value


def validate_output_files(summary: dict[str, Any], errors: list[str]) -> None:
    output_files = summary.get("output_files")
    if not isinstance(output_files, dict):
        errors.append("output_files must be an object.")
        return
    missing = missing_fields(output_files, REQUIRED_OUTPUT_FILES)
    if missing:
        errors.append(f"output_files missing fields: {', '.join(missing)}")


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
    for index, item in enumerate(require_list(remaining, "remaining_open_planning_items", errors), start=1):
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


def validate_research_context(summary: dict[str, Any], errors: list[str]) -> None:
    context = summary.get("research_context_summary")
    if not isinstance(context, dict):
        errors.append("research_context_summary must be an object.")
        return
    missing = missing_fields(context, REQUIRED_RESEARCH_CONTEXT_FIELDS)
    if missing:
        errors.append(f"research_context_summary missing fields: {', '.join(missing)}")
    require_object(
        context,
        "exported_ids",
        REQUIRED_EXPORTED_ID_FIELDS,
        errors,
        "research_context_summary",
    )
    require_list(context.get("source_backed_anchors", []), "source_backed_anchors", errors)


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
        consumers = claim.get("downstream_consumers", [])
        invalid = [
            item for item in require_list(consumers, f"claim {index} downstream_consumers", errors)
            if item not in ALLOWED_DOWNSTREAM_CONSUMERS
        ]
        if invalid:
            errors.append(
                f"Claim-to-evidence item {index} has invalid downstream_consumers: "
                + ", ".join(sorted(map(str, invalid)))
            )


def validate_plan_references(summary: dict[str, Any], errors: list[str]) -> None:
    refs = summary.get("plan_references")
    if not isinstance(refs, dict):
        errors.append("plan_references must be an object.")
        return
    missing = missing_fields(refs, REQUIRED_PLAN_REFERENCE_FIELDS)
    if missing:
        errors.append(f"plan_references missing fields: {', '.join(missing)}")


def validate_shared_protocol_summary(summary: dict[str, Any], errors: list[str]) -> None:
    protocol = summary.get("shared_protocol_summary")
    if not isinstance(protocol, dict):
        errors.append("shared_protocol_summary must be an object.")
        return
    missing = missing_fields(protocol, REQUIRED_PROTOCOL_SUMMARY_FIELDS)
    if missing:
        errors.append(f"shared_protocol_summary missing fields: {', '.join(missing)}")
    removed = sorted(REMOVED_PROTOCOL_FIELDS & set(protocol))
    if removed:
        errors.append("shared_protocol_summary uses removed fields: " + ", ".join(removed))


def validate_interface_contracts(summary: dict[str, Any], errors: list[str]) -> None:
    interface = summary.get("interface_contracts_summary")
    if not isinstance(interface, dict):
        errors.append("interface_contracts_summary must be an object.")
        return
    missing = missing_fields(interface, REQUIRED_INTERFACE_FIELDS)
    if missing:
        errors.append(f"interface_contracts_summary missing fields: {', '.join(missing)}")

    workloads = require_object(
        interface,
        "workloads",
        REQUIRED_WORKLOAD_FIELDS,
        errors,
        "interface_contracts_summary",
    )
    if workloads:
        require_object(
            workloads,
            "required_workloads",
            REQUIRED_REQUIRED_WORKLOAD_FIELDS,
            errors,
            "interface_contracts_summary.workloads",
        )
        for index, candidate in enumerate(
            require_list(
                workloads.get("scope_extension_workload_candidates", []),
                "scope_extension_workload_candidates",
                errors,
            ),
            start=1,
        ):
            if not isinstance(candidate, dict):
                errors.append(f"scope_extension_workload_candidates[{index}] must be an object.")
                continue
            for field in ("workload_id", "scope_signal", "explanation_ref", "research_context_ref"):
                if field not in candidate:
                    errors.append(
                        f"scope_extension_workload_candidates[{index}] missing field: {field}"
                    )

    baselines = require_object(
        interface,
        "baselines",
        REQUIRED_BASELINE_GROUPS,
        errors,
        "interface_contracts_summary",
    )
    if baselines:
        for group in REQUIRED_BASELINE_GROUPS:
            entries = baselines.get(group, [])
            for index, baseline in enumerate(require_list(entries, f"baselines.{group}", errors), start=1):
                if not isinstance(baseline, dict):
                    errors.append(f"baselines.{group}[{index}] must be an object.")
                    continue
                missing_baseline = missing_fields(baseline, REQUIRED_BASELINE_FIELDS)
                if missing_baseline:
                    errors.append(
                        f"baselines.{group}[{index}] missing fields: "
                        + ", ".join(missing_baseline)
                    )
                allowed_use = baseline.get("allowed_use")
                if allowed_use and allowed_use not in ALLOWED_BASELINE_ALLOWED_USE:
                    errors.append(
                        f"baselines.{group}[{index}] has invalid allowed_use: {allowed_use}"
                    )
                if group == "upper_bounds" and allowed_use == "main_comparison":
                    errors.append(
                        f"baselines.{group}[{index}] is an upper bound but uses main_comparison."
                    )

    require_object(interface, "logging_schema", REQUIRED_LOGGING_FIELDS, errors, "interface_contracts_summary")
    require_list(interface.get("execution_input_slots", []), "execution_input_slots", errors)
    require_list(interface.get("artifact_manifest", []), "artifact_manifest", errors)


def metric_contracts(summary: dict[str, Any]) -> list[dict[str, Any]]:
    metric_summary = summary.get("metric_contracts_summary", {})
    if not isinstance(metric_summary, dict):
        return []
    metrics = metric_summary.get("metrics", [])
    if not isinstance(metrics, list):
        return []
    return [metric for metric in metrics if isinstance(metric, dict)]


def validate_metric_contracts(summary: dict[str, Any], errors: list[str]) -> None:
    metric_summary = summary.get("metric_contracts_summary")
    if not isinstance(metric_summary, dict):
        errors.append("metric_contracts_summary must be an object.")
        return
    metrics = metric_summary.get("metrics")
    if not isinstance(metrics, list):
        errors.append("metric_contracts_summary.metrics must be a list.")
        return

    seen: set[str] = set()
    for index, metric in enumerate(metrics, start=1):
        if not isinstance(metric, dict):
            errors.append(f"metric_contracts_summary.metrics[{index}] must be an object.")
            continue
        missing_metric = missing_fields(metric, REQUIRED_METRIC_FIELDS)
        if missing_metric:
            errors.append(
                f"metric_contracts_summary.metrics[{index}] missing fields: "
                + ", ".join(missing_metric)
            )

        metric_id = metric.get("metric_id")
        if isinstance(metric_id, str):
            norm = normalize_id(metric_id)
            if norm in seen:
                errors.append(f"Duplicate metric_id: {metric_id}")
            seen.add(norm)

        status = metric.get("definition_status")
        if status and status not in ALLOWED_DEFINITION_STATUS:
            errors.append(f"metric {metric_id or index} has invalid definition_status: {status}")
        if status == "confirmed" and not metric.get("formula_ref"):
            errors.append(f"metric {metric_id or index} is confirmed but lacks formula_ref.")
        if status in {"delegated", "unresolved"} and not metric.get("required_decision"):
            errors.append(
                f"metric {metric_id or index} is {status} but lacks required_decision."
            )

        metric_type = str(metric.get("type", "")).lower()
        if metric_type == "ratio":
            for field in ("numerator", "denominator"):
                if not metric.get(field):
                    errors.append(f"ratio metric {metric_id or index} missing {field}.")
        if metric_type in {"cdf", "distribution"}:
            for field in ("x_unit", "y_unit", "zero_point"):
                if not metric.get(field):
                    errors.append(f"{metric_type} metric {metric_id or index} missing {field}.")


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

        removed = sorted(REMOVED_OBJECTIVE_FIELDS & set(objective))
        if removed:
            errors.append(f"Objective {index} uses removed fields: {', '.join(removed)}")

        heading = objective.get("objective_heading")
        if isinstance(heading, str) and heading.strip():
            headings.append(heading.strip())
        else:
            errors.append(f"Objective {index} must have a non-empty objective_heading.")

        role = objective.get("story_role")
        if isinstance(role, str) and role not in ALLOWED_STORY_ROLES:
            errors.append(f"Objective {index} has invalid story_role: {role}")

        priority = objective.get("priority")
        if isinstance(priority, str) and priority not in ALLOWED_PRIORITIES:
            errors.append(f"Objective {index} has invalid priority: {priority}")

        for field in ("evidence_outputs", "writing_scope_outputs", "target_evidence_artifacts", "output_files"):
            if not isinstance(objective.get(field), list) or not objective.get(field):
                errors.append(f"Objective {index} must include non-empty {field} list.")

        boundary = objective.get("boundary")
        if not isinstance(boundary, dict):
            errors.append(f"Objective {index} must include boundary object.")
        else:
            missing_boundary = missing_fields(boundary, REQUIRED_BOUNDARY_FIELDS)
            if missing_boundary:
                errors.append(
                    f"Objective {index} boundary missing fields: {', '.join(missing_boundary)}"
                )
            for field in REQUIRED_BOUNDARY_FIELDS:
                value = boundary.get(field)
                if not isinstance(value, list) or not value:
                    errors.append(f"Objective {index} boundary.{field} must be a non-empty list.")

        reuse_policy = objective.get("reuse_policy")
        if not isinstance(reuse_policy, dict):
            errors.append(f"Objective {index} must include reuse_policy object.")
        else:
            missing_reuse = missing_fields(reuse_policy, REQUIRED_REUSE_POLICY_FIELDS)
            if missing_reuse:
                errors.append(
                    f"Objective {index} reuse_policy missing fields: {', '.join(missing_reuse)}"
                )

        core = " ".join(flatten_strings(objective.get("core_experiment", ""))).lower()
        if "aggregate logs from objective" in core or "aggregate logs from objectives" in core:
            errors.append(
                f"Objective {index} appears to be a derived analysis; move it to derived_analyses."
            )

    if len(headings) != len(set(headings)):
        errors.append("Objective headings must be unique.")


def validate_derived_analyses(summary: dict[str, Any], errors: list[str]) -> None:
    analyses = summary.get("derived_analyses", [])
    if not isinstance(analyses, list):
        errors.append("derived_analyses must be a list.")
        return
    for index, analysis in enumerate(analyses, start=1):
        if not isinstance(analysis, dict):
            errors.append(f"Derived analysis {index} must be an object.")
            continue
        missing = missing_fields(analysis, REQUIRED_DERIVED_ANALYSIS_FIELDS)
        if missing:
            errors.append(f"Derived analysis {index} missing fields: {', '.join(missing)}")


def validate_dependency_graph(summary: dict[str, Any], errors: list[str]) -> None:
    graph = summary.get("objective_dependency_graph", [])
    if not isinstance(graph, list):
        errors.append("objective_dependency_graph must be a list.")
        return
    for index, edge in enumerate(graph, start=1):
        if not isinstance(edge, dict):
            errors.append(f"Dependency graph edge {index} must be an object.")
            continue
        for field in ("from_objective_or_artifact", "to_objective_or_artifact", "evidence_chain_role"):
            if field not in edge:
                errors.append(f"Dependency graph edge {index} missing field: {field}")


def collect_baseline_ids(summary: dict[str, Any]) -> set[str]:
    baselines = summary.get("interface_contracts_summary", {}).get("baselines", {})
    ids: set[str] = set()
    if isinstance(baselines, dict):
        for group in REQUIRED_BASELINE_GROUPS:
            for baseline in baselines.get(group, []) if isinstance(baselines.get(group, []), list) else []:
                if isinstance(baseline, dict) and isinstance(baseline.get("baseline_id"), str):
                    ids.add(normalize_id(baseline["baseline_id"]))
    return ids


def collect_workload_ids(summary: dict[str, Any]) -> set[str]:
    workloads = summary.get("interface_contracts_summary", {}).get("workloads", {})
    ids: set[str] = set()
    if not isinstance(workloads, dict):
        return ids
    required = workloads.get("required_workloads", {})
    if isinstance(required, dict):
        ids.update(normalize_id(item) for item in flatten_strings(required) if item)
    candidates = workloads.get("scope_extension_workload_candidates", [])
    if isinstance(candidates, list):
        for candidate in candidates:
            if isinstance(candidate, dict) and isinstance(candidate.get("workload_id"), str):
                ids.add(normalize_id(candidate["workload_id"]))
    return ids


def collect_metric_ids(summary: dict[str, Any]) -> set[str]:
    return {
        normalize_id(metric.get("metric_id", ""))
        for metric in metric_contracts(summary)
        if isinstance(metric.get("metric_id"), str)
    }


def validate_id_references(summary: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    baseline_ids = collect_baseline_ids(summary)
    workload_ids = collect_workload_ids(summary)
    metric_ids = collect_metric_ids(summary)

    context = summary.get("research_context_summary", {})
    exported = context.get("exported_ids", {}) if isinstance(context, dict) else {}
    exported_baselines = {normalize_id(x) for x in flatten_strings(exported.get("baseline_ids", []))}
    exported_workloads = {normalize_id(x) for x in flatten_strings(exported.get("workload_ids", []))}
    exported_metrics = {normalize_id(x) for x in flatten_strings(exported.get("metric_ids", []))}

    missing_baseline_sources = sorted(baseline_ids - exported_baselines)
    if missing_baseline_sources:
        warnings.append(
            "Baseline IDs missing from research_context_summary.exported_ids.baseline_ids: "
            + ", ".join(missing_baseline_sources)
        )
    missing_workload_sources = sorted(workload_ids - exported_workloads)
    if missing_workload_sources:
        warnings.append(
            "Workload IDs missing from research_context_summary.exported_ids.workload_ids: "
            + ", ".join(missing_workload_sources)
        )
    missing_metric_sources = sorted(metric_ids - exported_metrics)
    if missing_metric_sources:
        warnings.append(
            "Metric IDs missing from research_context_summary.exported_ids.metric_ids: "
            + ", ".join(missing_metric_sources)
        )

    protocol = summary.get("shared_protocol_summary", {})
    if isinstance(protocol, dict):
        for field in ("required_baseline_ids", "diagnostic_baseline_ids", "upper_bound_ids"):
            for baseline_id in flatten_strings(protocol.get(field, [])):
                if normalize_id(baseline_id) not in baseline_ids:
                    errors.append(f"{field} references unknown baseline ID: {baseline_id}")
        for field in ("primary_metric_ids", "secondary_metric_ids", "cost_or_waste_metric_ids"):
            for metric_id in flatten_strings(protocol.get(field, [])):
                if normalize_id(metric_id) not in metric_ids:
                    errors.append(f"{field} references unknown metric ID: {metric_id}")

    for index, objective in enumerate(summary.get("experiment_objectives", []), start=1):
        if not isinstance(objective, dict):
            continue
        for comparator in flatten_strings(objective.get("comparator_ids", [])):
            if normalize_id(comparator) not in baseline_ids:
                errors.append(f"Objective {index} references unknown comparator ID: {comparator}")
        for metric in flatten_strings(objective.get("primary_metric_ids", [])):
            if normalize_id(metric) not in metric_ids:
                errors.append(f"Objective {index} references unknown primary metric ID: {metric}")
        for metric in flatten_strings(objective.get("secondary_metric_ids", [])):
            if normalize_id(metric) not in metric_ids:
                errors.append(f"Objective {index} references unknown secondary metric ID: {metric}")


def validate_explanation_refs(summary: dict[str, Any], warnings: list[str]) -> None:
    ledger = summary.get("explanation_confirmation_ledger", {})
    headings = set(flatten_strings(ledger.get("required_explanation_headings", []))) if isinstance(ledger, dict) else set()
    if not headings:
        return
    workloads = summary.get("interface_contracts_summary", {}).get("workloads", {})
    candidates = workloads.get("scope_extension_workload_candidates", []) if isinstance(workloads, dict) else []
    if not isinstance(candidates, list):
        return
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        ref = candidate.get("explanation_ref")
        if isinstance(ref, str) and ref and ref not in headings:
            warnings.append(f"explanation_ref does not match required explanation heading: {ref}")


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
            "Summary uses removed top-level fields from the old single-plan schema: "
            + ", ".join(removed_present)
        )

    unknown = sorted(set(summary) - REQUIRED_TOP_LEVEL)
    if unknown:
        warnings.append(f"Unknown top-level fields: {', '.join(unknown)}")

    validate_output_files(summary, errors)
    validate_ledger(summary, errors, warnings)
    validate_research_context(summary, errors)
    validate_thesis(summary, errors)
    validate_claims(summary, errors)
    validate_plan_references(summary, errors)
    validate_shared_protocol_summary(summary, errors)
    validate_interface_contracts(summary, errors)
    validate_metric_contracts(summary, errors)
    validate_objectives(summary, errors, warnings)
    validate_derived_analyses(summary, errors)
    validate_dependency_graph(summary, errors)
    validate_id_references(summary, errors, warnings)
    validate_explanation_refs(summary, warnings)
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
