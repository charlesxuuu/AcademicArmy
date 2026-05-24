"""Validate a core paper-blueprint summary JSON file."""

from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_SUPPORT_STATUS = {"supported", "unsupported", "needs_evidence", "needs_verification"}
VALID_CLAIM_ROLE = {"acceptance_critical", "supporting", "optional", "deferred"}
VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_STORY_RECENCY = {"last_2_3_years", "latest_3_cycles", "expanded_last_5_years", "needs_verification"}
VALID_DELEGATED_AREAS = {"content_planning", "experiment_planning", "figure_planning", "method_planning", "writing", "review_risk"}
DOWNSTREAM_INTERFACES = ["content_planning", "experiment_planning", "figure_planning", "writing", "review_risk"]

OFF_SCOPE_BLUEPRINT_PATTERNS = {
    "Main-result experiment:",
    "Ablation experiment:",
    "Figure 1:",
    "Figure 2:",
    "Experiment ID",
    "Figure ID",
    "Section-by-Section Outline",
    "Manuscript Structure Specification",
    "Figure and Table Specification",
    "Evaluation Specification",
    "Execution Task Graph",
    "Artifact cautions",
    "Assumptions to validate",
    "Do not assume",
    "You should",
    "Caution",
    "Warning",
    "Reasoning Summary",
}
OFF_SCOPE_EXPLANATION_PATTERNS = {
    "deepresearch",
    "MCP",
    "web search",
    "rate limit",
    "PDF parsing",
    "output directory",
    "downstream agent",
    "implementation agent",
    "experiment agent",
    "writing agent",
    "output format",
    "specification format",
    "implementation-plan format",
    "how to use the files",
    "TODO",
}
SYNTHETIC_ID_RE = re.compile(r"\b(?:C|E|R|A|B|K|D)[1-9]\d?\b|\b(?:F|T)[1-9]\d?\b(?!\s*[- ]?score)|\bAR[1-9]\d?\b")
SECTION_REF_RE = re.compile(r"\bSection\s+(?:[1-9]|1[0-5])(?:\.\d+)?\b|第\s*(?:[1-9]|1[0-5])(?:\.\d+)?\s*节")


def fail(message: str) -> int:
    print(f"[ERROR] {message}")
    return 1


def require_keys(obj: dict, keys: list[str], path: str) -> str | None:
    missing = [key for key in keys if key not in obj]
    if missing:
        return f"{path} missing required key(s): {', '.join(missing)}"
    return None


def require_nonempty_list(obj: dict, key: str, path: str) -> str | None:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        return f"{path}.{key} must be a non-empty array"
    return None


def load_summary(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data.get("paper_blueprint_summary", data.get("paper_blueprint", data))


def normalize_metric_text(text: str) -> str:
    return re.sub(r"\bF1\s*[- ]?\s*score\b", "f1_metric", text, flags=re.IGNORECASE)


def contains_synthetic_id(text: str) -> bool:
    return bool(SYNTHETIC_ID_RE.search(normalize_metric_text(text)))


def find_synthetic_id_path(obj: Any, path: str = "paper_blueprint_summary") -> str | None:
    if isinstance(obj, str):
        if contains_synthetic_id(obj):
            return path
    elif isinstance(obj, list):
        for index, item in enumerate(obj, start=1):
            found = find_synthetic_id_path(item, f"{path}[{index}]")
            if found:
                return found
    elif isinstance(obj, dict):
        for key, value in obj.items():
            found = find_synthetic_id_path(value, f"{path}.{key}")
            if found:
                return found
    return None


def validate_output_files(data: dict) -> str | None:
    files = data["output_files"]
    if not isinstance(files, dict):
        return "output_files must be an object"
    error = require_keys(files, ["blueprint_markdown", "explanation_markdown", "output_language", "explanation_language_suffix"], "output_files")
    if error:
        return error
    if Path(files["blueprint_markdown"]).name != "paper_blueprint.md":
        return "output_files.blueprint_markdown must end with paper_blueprint.md"
    expected_suffix = f"paper_blueprint_explanation.{files['explanation_language_suffix']}.md"
    if Path(files["explanation_markdown"]).name != expected_suffix:
        return f"output_files.explanation_markdown must end with {expected_suffix}"
    if not files["output_language"]:
        return "output_files.output_language is required"
    return None


def validate_exemplar_analysis(exemplar_analysis: dict) -> str | None:
    if not isinstance(exemplar_analysis, dict):
        return "exemplar_analysis must be an object"
    error = require_keys(exemplar_analysis, ["storytelling_exemplars", "technical_exemplars", "evaluation_exemplars"], "exemplar_analysis")
    if error:
        return error

    current_year = datetime.now().year
    storytelling = exemplar_analysis["storytelling_exemplars"]
    if not isinstance(storytelling, list) or not storytelling:
        return "exemplar_analysis.storytelling_exemplars must be a non-empty array"
    for index, exemplar in enumerate(storytelling, start=1):
        if not isinstance(exemplar, dict):
            return f"storytelling_exemplars[{index}] must be an object"
        error = require_keys(
            exemplar,
            ["title", "venue", "year", "source", "recency_basis", "why_current_storytelling_exemplar", "transferable_storytelling_lesson", "non_transferable_warning", "verification_status"],
            f"storytelling_exemplars[{index}]",
        )
        if error:
            return error
        if exemplar["recency_basis"] not in VALID_STORY_RECENCY:
            return f"storytelling_exemplars[{index}].recency_basis must be one of {sorted(VALID_STORY_RECENCY)}"
        if exemplar["verification_status"] not in VALID_RELATED_STATUS:
            return f"storytelling_exemplars[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
        year = exemplar["year"]
        if year is None and exemplar["verification_status"] != "needs_verification":
            return f"storytelling_exemplars[{index}].year can be null only when verification_status is needs_verification"
        if isinstance(year, int) and year < current_year - 5:
            return f"storytelling_exemplars[{index}] is too old for current storytelling style"

    for group, keys in {
        "technical_exemplars": ["title", "venue", "year", "source", "influence_signal", "core_technical_idea", "technical_lesson_for_current_work", "verification_status"],
        "evaluation_exemplars": ["title", "venue", "year", "source", "evidence_class_lesson", "metric_family_lesson", "comparison_class_lesson", "verification_status"],
    }.items():
        items = exemplar_analysis[group]
        if not isinstance(items, list):
            return f"exemplar_analysis.{group} must be an array"
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                return f"{group}[{index}] must be an object"
            error = require_keys(item, keys, f"{group}[{index}]")
            if error:
                return error
            if item["verification_status"] not in VALID_RELATED_STATUS:
                return f"{group}[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
    return None


def validate_target_venue(data: dict) -> str | None:
    venue = data["target_venue"]
    if not isinstance(venue, dict):
        return "target_venue must be an object"
    error = require_keys(
        venue,
        ["primary", "alternatives", "reviewer_audience", "contribution_posture", "evidence_standard", "fit_score", "fit_rationale"],
        "target_venue",
    )
    if error:
        return error
    if venue["fit_score"] is not None and not isinstance(venue["fit_score"], int):
        return "target_venue.fit_score must be an integer or null"
    if isinstance(venue["fit_score"], int) and not 1 <= venue["fit_score"] <= 5:
        return "target_venue.fit_score must be between 1 and 5"
    return None


def validate_premises(premises: dict) -> str | None:
    if not isinstance(premises, dict):
        return "core_strategy_premises must be an object"
    return require_keys(
        premises,
        [
            "target_venue_premise",
            "problem_premise",
            "contribution_premise",
            "novelty_premise",
            "evidence_premise",
            "storytelling_premise",
            "scope_premise",
        ],
        "core_strategy_premises",
    )


def validate_claim_hierarchy(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "claim_hierarchy must be a non-empty array"
    roles = set()
    for index, claim in enumerate(items, start=1):
        if not isinstance(claim, dict):
            return f"claim_hierarchy[{index}] must be an object"
        error = require_keys(
            claim,
            [
                "title",
                "statement",
                "role",
                "evidence_obligation",
                "acceptable_proof_modes",
                "required_comparison_class",
                "metric_family",
                "scope_boundary",
                "current_support_status",
                "failure_implication",
            ],
            f"claim_hierarchy[{index}]",
        )
        if error:
            return error
        if claim["role"] not in VALID_CLAIM_ROLE:
            return f"claim_hierarchy[{index}].role must be one of {sorted(VALID_CLAIM_ROLE)}"
        if claim["current_support_status"] not in VALID_SUPPORT_STATUS:
            return f"claim_hierarchy[{index}].current_support_status must be one of {sorted(VALID_SUPPORT_STATUS)}"
        for key in ("evidence_obligation", "failure_implication"):
            if not claim[key]:
                return f"claim_hierarchy[{index}].{key} is required"
        roles.add(claim["role"])
    if "acceptance_critical" not in roles:
        return "claim_hierarchy must include at least one acceptance_critical claim"
    return None


def validate_related_work_boundary(boundary: dict) -> str | None:
    if not isinstance(boundary, dict):
        return "related_work_boundary must be an object"
    error = require_keys(boundary, ["work_clusters", "required_differentiation_points", "highest_related_work_risks"], "related_work_boundary")
    if error:
        return error
    clusters = boundary["work_clusters"]
    if not isinstance(clusters, list) or not clusters:
        return "related_work_boundary.work_clusters must be a non-empty array"
    for index, cluster in enumerate(clusters, start=1):
        if not isinstance(cluster, dict):
            return f"work_clusters[{index}] must be an object"
        error = require_keys(
            cluster,
            ["cluster_name", "already_solves", "blueprint_delta", "comparison_obligation", "overclaim_boundary", "verification_status"],
            f"work_clusters[{index}]",
        )
        if error:
            return error
        if cluster["verification_status"] not in VALID_RELATED_STATUS:
            return f"work_clusters[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
    return require_nonempty_list(boundary, "required_differentiation_points", "related_work_boundary")


def validate_method_abstraction(method: dict) -> str | None:
    if not isinstance(method, dict):
        return "method_abstraction must be an object"
    error = require_keys(
        method,
        ["core_idea", "mechanism_class", "inputs", "outputs", "decision_variables", "constraints", "assumptions_and_invariants", "delegated_method_details"],
        "method_abstraction",
    )
    if error:
        return error
    for key in ("inputs", "outputs", "decision_variables", "constraints"):
        error = require_nonempty_list(method, key, "method_abstraction")
        if error:
            return error
    return None


def validate_evidence_obligations(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "evidence_obligations must be a non-empty array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"evidence_obligations[{index}] must be an object"
        error = require_keys(
            item,
            [
                "title",
                "supported_claim",
                "required_evidence_type",
                "metric_family",
                "baseline_or_comparison_class",
                "data_or_workload_class",
                "minimum_acceptable_support",
                "planning_freedom",
                "failure_implication",
            ],
            f"evidence_obligations[{index}]",
        )
        if error:
            return error
        for key in ("metric_family", "baseline_or_comparison_class", "data_or_workload_class"):
            error = require_nonempty_list(item, key, f"evidence_obligations[{index}]")
            if error:
                return error
    return None


def validate_narrative_requirements(narrative: dict) -> str | None:
    if not isinstance(narrative, dict):
        return "narrative_requirements must be an object"
    error = require_keys(
        narrative,
        ["opening_tension", "central_abstraction", "story_arc", "terms_to_foreground", "claims_to_avoid_foregrounding", "delegated_content_planning"],
        "narrative_requirements",
    )
    if error:
        return error
    return require_nonempty_list(narrative, "story_arc", "narrative_requirements")


def validate_visual_requirements(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "visual_argument_requirements must be a non-empty array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"visual_argument_requirements[{index}] must be an object"
        error = require_keys(
            item,
            ["title", "message_that_must_be_visible", "why_it_matters", "related_thesis_or_claim", "planning_freedom"],
            f"visual_argument_requirements[{index}]",
        )
        if error:
            return error
    return None


def validate_scope_boundaries(scope: dict) -> str | None:
    if not isinstance(scope, dict):
        return "scope_boundaries must be an object"
    required = ["in_scope_setting", "out_of_scope_setting", "accepted_assumptions", "allowed_claims", "deferred_claims", "claims_avoided_by_design"]
    error = require_keys(scope, required, "scope_boundaries")
    if error:
        return error
    for key in ("in_scope_setting", "allowed_claims", "claims_avoided_by_design"):
        error = require_nonempty_list(scope, key, "scope_boundaries")
        if error:
            return error
    return None


def validate_open_variables(variables: dict) -> str | None:
    if not isinstance(variables, dict):
        return "open_planning_variables must be an object"
    required = ["content_planning", "experiment_planning", "figure_planning", "method_planning", "related_work_planning", "review_risk_planning"]
    error = require_keys(variables, required, "open_planning_variables")
    if error:
        return error
    for key in required:
        error = require_nonempty_list(variables, key, "open_planning_variables")
        if error:
            return error
    return None


def validate_downstream_interfaces(interfaces: dict) -> str | None:
    if not isinstance(interfaces, dict):
        return "downstream_planning_interfaces must be an object"
    error = require_keys(interfaces, DOWNSTREAM_INTERFACES, "downstream_planning_interfaces")
    if error:
        return error
    for name in DOWNSTREAM_INTERFACES:
        interface = interfaces[name]
        if not isinstance(interface, dict):
            return f"downstream_planning_interfaces.{name} must be an object"
        error = require_keys(interface, ["use", "preserve_constraints", "produce_later", "allowed_to_decide"], f"downstream_planning_interfaces.{name}")
        if error:
            return error
        for key in ("use", "preserve_constraints", "produce_later", "allowed_to_decide"):
            error = require_nonempty_list(interface, key, f"downstream_planning_interfaces.{name}")
            if error:
                return error
    return None


def validate_design_rationale(rationale: dict) -> str | None:
    if not isinstance(rationale, dict):
        return "design_rationale must be an object"
    error = require_keys(
        rationale,
        [
            "blueprint_overview",
            "validation_overview",
            "item_rationales",
            "delegated_detail_rationale",
            "diagnostic_derivation_chains",
            "disagreement_diagnosis",
        ],
        "design_rationale",
    )
    if error:
        return error

    overview = rationale["blueprint_overview"]
    if not isinstance(overview, dict):
        return "design_rationale.blueprint_overview must be an object"
    error = require_keys(
        overview,
        [
            "paper_positioning",
            "central_thesis",
            "main_contribution",
            "primary_claim",
            "evidence_obligation_summary",
            "most_important_boundary",
            "open_planning_variable_summary",
        ],
        "design_rationale.blueprint_overview",
    )
    if error:
        return error

    validation_overview = rationale["validation_overview"]
    if not isinstance(validation_overview, list) or not validation_overview:
        return "design_rationale.validation_overview must be a non-empty array"
    for index, item in enumerate(validation_overview, start=1):
        if not isinstance(item, dict):
            return f"validation_overview[{index}] must be an object"
        error = require_keys(item, ["key_blueprint_content", "why_it_matters", "main_user_validation_question"], f"validation_overview[{index}]")
        if error:
            return error

    for group, keys in {
        "item_rationales": ["semantic_item_name", "blueprint_content_digest", "premise_source", "derivation", "downstream_connections", "user_validation_point"],
        "delegated_detail_rationale": ["detail_area", "what_is_left_open", "why_left_open", "constraint_from_blueprint"],
        "diagnostic_derivation_chains": ["starting_premise", "derived_blueprint_choices", "evidence_needed", "likely_failure_point", "blueprint_revision_if_chain_fails"],
        "disagreement_diagnosis": ["disagreement_type", "upstream_premise_to_inspect", "affected_blueprint_objects", "likely_revision_direction"],
    }.items():
        items = rationale[group]
        if not isinstance(items, list) or not items:
            return f"design_rationale.{group} must be a non-empty array"
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                return f"{group}[{index}] must be an object"
            error = require_keys(item, keys, f"{group}[{index}]")
            if error:
                return error
            if group == "delegated_detail_rationale" and item["detail_area"] not in VALID_DELEGATED_AREAS:
                return f"delegated_detail_rationale[{index}].detail_area must be one of {sorted(VALID_DELEGATED_AREAS)}"
    return None


def validate_style_checks(style_checks: dict) -> str | None:
    if not isinstance(style_checks, dict):
        return "explanation_style_checks must be an object"
    required = [
        "standalone_validation_companion",
        "includes_blueprint_content_digest",
        "uses_semantic_anchors",
        "explains_delegated_details",
        "avoids_synthetic_ids",
    ]
    error = require_keys(style_checks, required, "explanation_style_checks")
    if error:
        return error
    for key in required:
        if style_checks[key] is not True:
            return f"explanation_style_checks.{key} must be true"
    return None


def validate(data: dict) -> str | None:
    top_error = require_keys(
        data,
        [
            "output_files",
            "title",
            "paper_identity",
            "target_venue",
            "exemplar_analysis",
            "distilled_patterns",
            "core_strategy_premises",
            "central_thesis",
            "contribution_contract",
            "claim_hierarchy",
            "related_work_boundary",
            "method_abstraction",
            "evidence_obligations",
            "narrative_requirements",
            "visual_argument_requirements",
            "scope_boundaries",
            "research_risks_and_dependency_signals",
            "open_planning_variables",
            "downstream_planning_interfaces",
            "design_rationale",
            "explanation_style_checks",
        ],
        "paper_blueprint_summary",
    )
    if top_error:
        return top_error

    synthetic_path = find_synthetic_id_path(data)
    if synthetic_path:
        return f"synthetic object ID found in {synthetic_path}; use semantic names instead"

    validators = (
        validate_output_files,
        lambda d: validate_exemplar_analysis(d["exemplar_analysis"]),
        validate_target_venue,
        lambda d: validate_premises(d["core_strategy_premises"]),
        lambda d: validate_claim_hierarchy(d["claim_hierarchy"]),
        lambda d: validate_related_work_boundary(d["related_work_boundary"]),
        lambda d: validate_method_abstraction(d["method_abstraction"]),
        lambda d: validate_evidence_obligations(d["evidence_obligations"]),
        lambda d: validate_narrative_requirements(d["narrative_requirements"]),
        lambda d: validate_visual_requirements(d["visual_argument_requirements"]),
        lambda d: validate_scope_boundaries(d["scope_boundaries"]),
        lambda d: validate_open_variables(d["open_planning_variables"]),
        lambda d: validate_downstream_interfaces(d["downstream_planning_interfaces"]),
        lambda d: validate_design_rationale(d["design_rationale"]),
        lambda d: validate_style_checks(d["explanation_style_checks"]),
    )
    for validator in validators:
        error = validator(data)
        if error:
            return error

    for path, keys in (
        ("paper_identity", ["working_title", "research_area", "target_venue_candidates", "paper_type", "research_artifact", "current_input_state"]),
        ("central_thesis", ["one_sentence_thesis", "acceptance_critical_paper_bet", "downgrade_or_falsification_condition"]),
        ("contribution_contract", ["primary_contribution", "secondary_contributions", "supporting_contributions", "non_contributions_and_boundaries"]),
        ("research_risks_and_dependency_signals", ["highest_risk_premise", "highest_risk_claim", "highest_risk_related_work_boundary", "highest_risk_evidence_gap", "risk_materialization_changes"]),
    ):
        obj = data[path]
        if not isinstance(obj, dict):
            return f"{path} must be an object"
        error = require_keys(obj, keys, path)
        if error:
            return error
    return None


def resolve_output_path(raw_path: str, base_dir: Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return base_dir / path


def validate_markdown_files(data: dict, base_dir: Path) -> str | None:
    files = data["output_files"]
    blueprint_path = resolve_output_path(files["blueprint_markdown"], base_dir)
    explanation_path = resolve_output_path(files["explanation_markdown"], base_dir)

    if blueprint_path.exists():
        text = blueprint_path.read_text(encoding="utf-8-sig")
        for pattern in OFF_SCOPE_BLUEPRINT_PATTERNS:
            if pattern.lower() in text.lower():
                return f"paper_blueprint.md contains overly detailed or advisory blueprint text: {pattern}"
        if contains_synthetic_id(text):
            return "paper_blueprint.md contains synthetic object IDs; use semantic headings instead"
        required_headings = [
            "## 1. Paper Identity",
            "## 2. Target Venue and Contribution Posture",
            "## 3. Core Strategy Premises",
            "## 4. Central Thesis",
            "## 5. Contribution Contract",
            "## 6. Claim Hierarchy",
            "## 7. Related-Work and Novelty Boundary",
            "## 8. Method Abstraction",
            "## 9. Evidence Obligations",
            "## 10. Narrative Requirements",
            "## 11. Visual Argument Requirements",
            "## 12. Scope and Constraint Boundaries",
            "## 13. Research Risks and Dependency Signals",
            "## 14. Open Planning Variables",
            "## 15. Downstream Planning Interfaces",
        ]
        for heading in required_headings:
            if heading not in text:
                return f"paper_blueprint.md must contain '{heading}'"

    if explanation_path.exists():
        text = explanation_path.read_text(encoding="utf-8-sig")
        required_heading_groups = [
            ["## Blueprint Overview", "## 蓝图速览"],
            ["## Key Blueprint Content and Validation Entry Points", "## 蓝图重点内容与审核入口"],
            ["## Core Strategy Premises", "## 核心出发点"],
            ["## Item-by-Item Blueprint Validation", "## 蓝图逐项解释"],
            ["## What Is Delegated to Later Planning Skills", "## 哪些内容留给后续规划技能"],
            ["## Priority Questions for User Review", "## 用户审核时最应该确认的问题"],
        ]
        for headings in required_heading_groups:
            if not any(heading in text for heading in headings):
                return f"explanation file must contain one of: {', '.join(headings)}"
        if "paper_blueprint_summary:" in text:
            return "explanation file appears to duplicate machine-oriented blueprint content"
        if contains_synthetic_id(text):
            return "explanation file contains synthetic object IDs; use semantic names instead"
        for pattern in OFF_SCOPE_EXPLANATION_PATTERNS:
            if pattern.lower() in text.lower():
                return f"explanation file leaves paper-strategy validation scope: {pattern}"
        section_refs = SECTION_REF_RE.findall(text)
        if len(section_refs) > 8:
            return "explanation file relies too heavily on numbered section references; use semantic anchors"
        paragraphs = re.split(r"\n\s*\n", text)
        for paragraph in paragraphs:
            if len(SECTION_REF_RE.findall(paragraph)) > 2:
                return "explanation file has a paragraph driven by numbered section references; use semantic item names"
    return None


def main() -> int:
    if len(sys.argv) != 2:
        return fail("Usage: validate_blueprint.py <blueprint-summary.json>")

    path = Path(sys.argv[1])
    if not path.exists():
        return fail(f"File not found: {path}")

    try:
        data = load_summary(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(str(exc))

    error = validate(data)
    if not error:
        error = validate_markdown_files(data, path.parent)
    if error:
        return fail(error)

    print("[OK] core paper blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
