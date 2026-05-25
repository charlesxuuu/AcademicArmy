"""Validate a strategic paper-blueprint summary JSON file."""

from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_CLAIM_ROLE = {"acceptance_critical", "mechanism", "scope", "supporting", "deferred"}
VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_STORY_RECENCY = {"last_2_3_years", "latest_3_cycles", "expanded_last_5_years", "needs_verification"}
VALID_DEFAULT_AREAS = {"venue", "contribution", "evidence", "narrative", "method", "scope"}
VALID_DELEGATED_AREAS = {"content_planning", "experiment_planning", "figure_planning", "method_planning", "review_planning"}
DELEGATION_BOUNDARIES = ["content_planning", "experiment_planning", "figure_planning", "method_planning", "review_planning"]

TACTICAL_BLUEPRINT_PATTERNS = {
    "Main-result experiment:",
    "Ablation experiment:",
    "Figure 1:",
    "Figure 2:",
    "Experiment ID",
    "Figure ID",
    "dataset split",
    "statistical protocol",
    "plotting script",
    "run order",
    "implementation task",
    "section-by-section outline",
    "manuscript structure specification",
    "figure and table specification",
    "evaluation specification",
    "execution task graph",
    "MPC or",
    "Lyapunov or",
    "Pensieve",
    "BOLA",
}
TACTICAL_EXPLANATION_PATTERNS = {
    "which trace",
    "which dataset",
    "which baseline",
    "which figure layout",
    "which algorithm",
    "MPC or",
    "Lyapunov or",
    "run order",
    "next step",
    "TODO",
    "deepresearch",
    "MCP",
    "web search",
    "rate limit",
    "downstream agent",
    "output format",
}
SYNTHETIC_ID_RE = re.compile(r"\b(?:C|E|R|A|B|K|D)[1-9]\d?\b|\b(?:F|T)[1-9]\d?\b(?!\s*[- ]?score)|\bAR[1-9]\d?\b")
SECTION_REF_RE = re.compile(r"\bSection\s+(?:[1-9]|1[0-2])(?:\.\d+)?\b|第\s*(?:[1-9]|1[0-2])(?:\.\d+)?\s*节")


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
    return None


def validate_exemplar_analysis(exemplar_analysis: dict) -> str | None:
    if not isinstance(exemplar_analysis, dict):
        return "exemplar_analysis must be an object"
    error = require_keys(exemplar_analysis, ["storytelling_exemplars", "technical_exemplars", "evidence_exemplars"], "exemplar_analysis")
    if error:
        return error
    current_year = datetime.now().year
    storytelling = exemplar_analysis["storytelling_exemplars"]
    if not isinstance(storytelling, list) or not storytelling:
        return "exemplar_analysis.storytelling_exemplars must be a non-empty array"
    for index, item in enumerate(storytelling, start=1):
        error = require_keys(item, ["title", "venue", "year", "source", "recency_basis", "strategic_story_lesson", "verification_status"], f"storytelling_exemplars[{index}]")
        if error:
            return error
        if item["recency_basis"] not in VALID_STORY_RECENCY:
            return f"storytelling_exemplars[{index}].recency_basis must be one of {sorted(VALID_STORY_RECENCY)}"
        if item["verification_status"] not in VALID_RELATED_STATUS:
            return f"storytelling_exemplars[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
        year = item["year"]
        if isinstance(year, int) and year < current_year - 5:
            return f"storytelling_exemplars[{index}] is too old for current storytelling style"
    for group, keys in {
        "technical_exemplars": ["title", "venue", "year", "source", "strategic_technical_lesson", "verification_status"],
        "evidence_exemplars": ["title", "venue", "year", "source", "strategic_evidence_lesson", "verification_status"],
    }.items():
        items = exemplar_analysis[group]
        if not isinstance(items, list):
            return f"exemplar_analysis.{group} must be an array"
        for index, item in enumerate(items, start=1):
            error = require_keys(item, keys, f"{group}[{index}]")
            if error:
                return error
            if item["verification_status"] not in VALID_RELATED_STATUS:
                return f"{group}[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
    return None


def validate_confirmed_user_context(context: dict) -> str | None:
    if not isinstance(context, dict):
        return "confirmed_user_context must be an object"
    required = [
        "research_inputs",
        "existing_materials",
        "target_field_or_venue_preferences",
        "blueprint_purpose",
        "downstream_planning_pipeline",
        "output_requirements",
        "abstraction_level_preferences",
        "explanation_preferences",
        "content_delegated_to_later_planning",
        "working_assumptions",
    ]
    error = require_keys(context, required, "confirmed_user_context")
    if error:
        return error
    for key in required:
        if not isinstance(context[key], list):
            return f"confirmed_user_context.{key} must be an array"
    return None


def validate_claim_strategy(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "claim_strategy must be a non-empty array"
    roles = set()
    for index, claim in enumerate(items, start=1):
        error = require_keys(
            claim,
            ["title", "claim_statement", "strategic_role", "evidence_posture", "scope_boundary", "downgrade_condition"],
            f"claim_strategy[{index}]",
        )
        if error:
            return error
        if claim["strategic_role"] not in VALID_CLAIM_ROLE:
            return f"claim_strategy[{index}].strategic_role must be one of {sorted(VALID_CLAIM_ROLE)}"
        roles.add(claim["strategic_role"])
    if "acceptance_critical" not in roles:
        return "claim_strategy must include an acceptance_critical claim"
    return None


def validate_evidence_posture(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "evidence_posture must be a non-empty array"
    for index, item in enumerate(items, start=1):
        error = require_keys(
            item,
            [
                "title",
                "strategic_claim_supported",
                "high_level_evidence_type",
                "comparison_posture",
                "outcome_family",
                "minimum_standard_for_strategic_viability",
                "delegated_tactical_choices",
                "downgrade_implication",
            ],
            f"evidence_posture[{index}]",
        )
        if error:
            return error
        error = require_nonempty_list(item, "delegated_tactical_choices", f"evidence_posture[{index}]")
        if error:
            return error
    return None


def validate_delegation_boundaries(boundaries: dict) -> str | None:
    if not isinstance(boundaries, dict):
        return "delegation_boundaries must be an object"
    error = require_keys(boundaries, DELEGATION_BOUNDARIES, "delegation_boundaries")
    if error:
        return error
    for name in DELEGATION_BOUNDARIES:
        boundary = boundaries[name]
        if not isinstance(boundary, dict):
            return f"delegation_boundaries.{name} must be an object"
        error = require_keys(boundary, ["strategic_boundary", "constraints_to_preserve", "tactical_choices_delegated"], f"delegation_boundaries.{name}")
        if error:
            return error
        for key in ("constraints_to_preserve", "tactical_choices_delegated"):
            error = require_nonempty_list(boundary, key, f"delegation_boundaries.{name}")
            if error:
                return error
    return None


def validate_strategic_defaults(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "strategic_defaults must be a non-empty array"
    for index, item in enumerate(items, start=1):
        error = require_keys(
            item,
            ["posture_area", "recommended_default", "why_matches_premises", "evidence_that_would_change_it", "downstream_skill_to_explore_tactical_alternatives"],
            f"strategic_defaults[{index}]",
        )
        if error:
            return error
        if item["posture_area"] not in VALID_DEFAULT_AREAS:
            return f"strategic_defaults[{index}].posture_area must be one of {sorted(VALID_DEFAULT_AREAS)}"
    return None


def validate_design_rationale(rationale: dict) -> str | None:
    if not isinstance(rationale, dict):
        return "design_rationale must be an object"
    error = require_keys(
        rationale,
        [
            "strategic_overview",
            "validation_overview",
            "item_rationales",
            "delegated_detail_rationale",
            "fragile_strategic_chains",
            "strategic_disagreement_diagnosis",
        ],
        "design_rationale",
    )
    if error:
        return error
    overview = rationale["strategic_overview"]
    error = require_keys(
        overview,
        [
            "paper_positioning",
            "central_research_bet",
            "primary_contribution",
            "acceptance_critical_claim",
            "evidence_posture_summary",
            "delegation_summary",
            "highest_strategic_risk",
        ],
        "design_rationale.strategic_overview",
    )
    if error:
        return error
    for group, keys in {
        "validation_overview": ["key_strategic_content", "why_it_matters", "main_user_validation_question"],
        "item_rationales": ["semantic_item_name", "strategic_content_digest", "premise_source", "derivation", "downstream_constraint", "user_validation_point"],
        "delegated_detail_rationale": ["detail_area", "what_is_delegated", "strategic_constraint", "reason_for_delegation"],
        "fragile_strategic_chains": ["starting_premise", "derived_strategy", "evidence_needed", "likely_failure_point", "strategy_revision_if_chain_fails"],
        "strategic_disagreement_diagnosis": ["disagreement_type", "upstream_premise_to_inspect", "affected_strategy_objects", "likely_revision_direction"],
    }.items():
        items = rationale[group]
        if not isinstance(items, list) or not items:
            return f"design_rationale.{group} must be a non-empty array"
        for index, item in enumerate(items, start=1):
            error = require_keys(item, keys, f"{group}[{index}]")
            if error:
                return error
            if group == "delegated_detail_rationale" and item["detail_area"] not in VALID_DELEGATED_AREAS:
                return f"delegated_detail_rationale[{index}].detail_area must be one of {sorted(VALID_DELEGATED_AREAS)}"
    return None


def validate_style_checks(style_checks: dict) -> str | None:
    required = [
        "strategic_validation_companion",
        "includes_strategic_content_digest",
        "uses_semantic_anchors",
        "explains_delegation_boundaries",
        "avoids_tactical_questionnaire",
        "avoids_synthetic_ids",
    ]
    if not isinstance(style_checks, dict):
        return "explanation_style_checks must be an object"
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
            "confirmed_user_context",
            "title",
            "paper_identity",
            "exemplar_analysis",
            "core_strategy_premises",
            "central_research_bet",
            "contribution_contract",
            "claim_strategy",
            "novelty_and_comparison_strategy",
            "method_abstraction_strategy",
            "evidence_posture",
            "narrative_and_visual_strategy",
            "strategic_risks_and_uncertainties",
            "delegation_boundaries",
            "strategic_defaults",
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
        lambda d: validate_confirmed_user_context(d["confirmed_user_context"]),
        lambda d: validate_exemplar_analysis(d["exemplar_analysis"]),
        lambda d: validate_claim_strategy(d["claim_strategy"]),
        lambda d: validate_evidence_posture(d["evidence_posture"]),
        lambda d: validate_delegation_boundaries(d["delegation_boundaries"]),
        lambda d: validate_strategic_defaults(d["strategic_defaults"]),
        lambda d: validate_design_rationale(d["design_rationale"]),
        lambda d: validate_style_checks(d["explanation_style_checks"]),
    )
    for validator in validators:
        error = validator(data)
        if error:
            return error
    for path, keys in (
        ("paper_identity", ["research_object", "target_venue_posture", "paper_type", "current_input_state", "user_confirmed_constraints", "intended_downstream_planning_pipeline", "strategic_abstraction_level"]),
        ("core_strategy_premises", ["venue_premise", "problem_premise", "contribution_premise", "novelty_premise", "evidence_premise", "scope_premise"]),
        ("central_research_bet", ["one_sentence_thesis", "acceptance_critical_bet", "downgrade_condition"]),
        ("contribution_contract", ["primary_contribution", "secondary_contribution_roles", "non_contributions_and_boundaries"]),
        ("novelty_and_comparison_strategy", ["closest_work_clusters", "differentiation_posture", "comparison_posture", "overclaim_boundary"]),
        ("method_abstraction_strategy", ["core_abstraction", "mechanism_class", "strategic_decision_space", "constraints_and_invariants", "delegated_tactical_method_details"]),
        ("narrative_and_visual_strategy", ["opening_tension", "central_abstraction_to_foreground", "story_arc", "visual_argument_requirements", "delegated_content_and_figure_choices"]),
        ("strategic_risks_and_uncertainties", ["highest_risk_premise", "highest_risk_claim", "highest_risk_novelty_boundary", "highest_risk_evidence_gap", "strategy_change_if_risks_materialize"]),
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
        for pattern in TACTICAL_BLUEPRINT_PATTERNS:
            if pattern.lower() in text.lower():
                return f"paper_blueprint.md contains tactical detail instead of strategic posture: {pattern}"
        if contains_synthetic_id(text):
            return "paper_blueprint.md contains synthetic object IDs; use semantic headings"
        required_headings = [
            "## 1. Paper Identity and Confirmed Inputs",
            "## 2. Core Strategy Premises",
            "## 3. Central Research Bet",
            "## 4. Contribution Contract",
            "## 5. Claim Strategy",
            "## 6. Novelty and Comparison Strategy",
            "## 7. Method Abstraction Strategy",
            "## 8. Evidence Posture",
            "## 9. Narrative and Visual Strategy",
            "## 10. Strategic Risks and Decision-Critical Uncertainties",
            "## 11. Delegation Boundaries for Downstream Skills",
            "## 12. Strategic Defaults",
        ]
        for heading in required_headings:
            if heading not in text:
                return f"paper_blueprint.md must contain '{heading}'"
    if explanation_path.exists():
        text = explanation_path.read_text(encoding="utf-8-sig")
        required_heading_groups = [
            ["## 0. Confirmed User Context", "## 0. 用户已明确的信息"],
            ["## Strategic Blueprint Overview", "## 战略蓝图速览"],
            ["## Key Strategic Content and Validation Entry Points", "## 战略重点内容与审核入口"],
            ["## Core Premises", "## 核心出发点"],
            ["## Item-by-Item Strategic Validation", "## 战略蓝图逐项解释"],
            ["## What Is Delegated to Later Specialized Planning", "## 哪些内容留给后续专项规划"],
            ["## Priority Questions for User Review", "## 用户应优先确认的战略问题"],
        ]
        for headings in required_heading_groups:
            if not any(heading in text for heading in headings):
                return f"explanation file must contain one of: {', '.join(headings)}"
        if contains_synthetic_id(text):
            return "explanation file contains synthetic object IDs; use semantic names"
        for pattern in TACTICAL_EXPLANATION_PATTERNS:
            if pattern.lower() in text.lower():
                return f"explanation file asks about tactical detail instead of strategy: {pattern}"
        if len(SECTION_REF_RE.findall(text)) > 8:
            return "explanation file relies too heavily on numbered section references"
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
    print("[OK] strategic paper blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
