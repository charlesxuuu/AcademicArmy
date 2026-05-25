"""Validate a goal-oriented strategic paper-blueprint summary JSON file."""

from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_GOAL_ROLES = {
    "acceptance",
    "positioning",
    "contribution",
    "novelty",
    "evidence",
    "scope",
    "communication",
    "downstream_planning",
}
VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_STORY_RECENCY = {"last_2_3_years", "latest_3_cycles", "expanded_last_5_years", "needs_verification"}
VALID_DELEGATED_AREAS = {"content_planning", "experiment_planning", "figure_planning", "method_planning", "review_planning"}
DELEGATION_INTERFACES = [
    "content_planning_interface",
    "experiment_planning_interface",
    "figure_planning_interface",
    "method_planning_interface",
    "review_planning_interface",
]

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
REQUIRED_BLUEPRINT_HEADINGS = [
    "Paper Identity",
    "Top-Level Paper Goal",
    "Goal Decomposition",
    "Goal Cards",
    "Goal Dependency Map",
    "Strategic Claim Posture",
    "Strategic Evidence Posture",
    "Strategic Communication Posture",
    "Strategic Risks",
    "Delegation Interfaces for Downstream Skills",
]
FORBIDDEN_LEGACY_BLUEPRINT_HEADINGS = [
    "Core Strategy Premises",
    "Central Research Bet",
    "Contribution Contract",
    "Claim Strategy",
    "Evidence Posture",
    "Narrative and Visual Strategy",
    "Strategic Defaults",
]
GOAL_CARD_FIELDS = [
    "Goal statement",
    "Why this goal matters",
    "Strategic role",
    "Success condition",
    "Derived constraints",
    "Delegated details",
    "Failure or revision implication",
]
EXPLANATION_HEADING_PATTERNS = [
    ("Confirmed User Context", "用户已明确的信息"),
    ("Blueprint Overview", "蓝图速览"),
    ("Core Goal Set", "核心目标组"),
    ("Derivation from Core Goals", "从核心目标到论文蓝图的推导"),
    ("Key Blueprint Content", "蓝图重点内容概括与解释"),
    ("How the Goals Support Each Other", "目标之间如何相互支撑"),
    ("Fragile Goal Chains", "当前最脆弱的目标链"),
    ("Remaining Strategic Questions", "用户仍需确认的战略问题"),
]
FORBIDDEN_LEGACY_EXPLANATION_HEADINGS = [
    "Strategic Blueprint Overview",
    "Key Strategic Content and Validation Entry Points",
    "Core Premises",
    "Item-by-Item Strategic Validation",
    "Strategic Defaults and Change Conditions",
]
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


def heading_present(text: str, heading: str) -> bool:
    pattern = rf"^##\s+(?:\d+\.\s+)?{re.escape(heading)}\b"
    return bool(re.search(pattern, text, flags=re.MULTILINE))


def heading_containing_present(text: str, options: tuple[str, str]) -> bool:
    return any(re.search(rf"^##\s+.*{re.escape(option)}.*$", text, flags=re.MULTILINE) for option in options)


def extract_section(text: str, heading: str) -> str:
    pattern = rf"^##\s+(?:\d+\.\s+)?{re.escape(heading)}\b.*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end]


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


def validate_goal_cards(items: list) -> str | None:
    if not isinstance(items, list) or len(items) < 6:
        return "goal_cards must contain at least 6 goal cards"
    required = [
        "goal_name",
        "goal_statement",
        "why_this_goal_matters",
        "strategic_role",
        "success_condition",
        "derived_constraints",
        "delegated_details",
        "failure_or_revision_implication",
    ]
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"goal_cards[{index}] must be an object"
        error = require_keys(item, required, f"goal_cards[{index}]")
        if error:
            return error
        if item["strategic_role"] not in VALID_GOAL_ROLES:
            return f"goal_cards[{index}].strategic_role must be one of {sorted(VALID_GOAL_ROLES)}"
        for key in ("derived_constraints", "delegated_details"):
            error = require_nonempty_list(item, key, f"goal_cards[{index}]")
            if error:
                return error
    return None


def validate_delegation_interfaces(interfaces: dict) -> str | None:
    if not isinstance(interfaces, dict):
        return "delegation_interfaces must be an object"
    error = require_keys(interfaces, DELEGATION_INTERFACES, "delegation_interfaces")
    if error:
        return error
    for name in DELEGATION_INTERFACES:
        interface = interfaces[name]
        if not isinstance(interface, dict):
            return f"delegation_interfaces.{name} must be an object"
        error = require_keys(interface, ["goals_to_operationalize", "constraints_to_preserve", "tactical_choices_delegated"], f"delegation_interfaces.{name}")
        if error:
            return error
        for key in ("goals_to_operationalize", "constraints_to_preserve", "tactical_choices_delegated"):
            error = require_nonempty_list(interface, key, f"delegation_interfaces.{name}")
            if error:
                return error
    return None


def validate_design_rationale(rationale: dict) -> str | None:
    if not isinstance(rationale, dict):
        return "design_rationale must be an object"
    error = require_keys(
        rationale,
        [
            "goal_oriented_overview",
            "validation_overview",
            "confirmed_context_coverage",
            "remaining_strategic_questions",
            "goal_rationales",
            "goal_derived_arrangements",
            "delegated_detail_rationale",
            "fragile_goal_chains",
            "strategic_disagreement_diagnosis",
        ],
        "design_rationale",
    )
    if error:
        return error
    overview = rationale["goal_oriented_overview"]
    error = require_keys(
        overview,
        [
            "top_level_paper_goal",
            "central_research_bet",
            "main_contribution_goal",
            "evidence_goal",
            "communication_goal",
            "largest_strategic_risk",
        ],
        "design_rationale.goal_oriented_overview",
    )
    if error:
        return error
    for group, keys in {
        "validation_overview": ["key_goal_or_arrangement", "why_it_matters", "main_user_validation_question"],
        "confirmed_context_coverage": ["confirmed_context_item", "covered_or_narrowed_question", "effect_on_remaining_questions"],
        "remaining_strategic_questions": ["question", "why_not_covered_by_confirmed_context", "strategy_change_if_answer_changes"],
        "goal_rationales": ["goal_name", "goal_content_digest", "design_idea", "relationship_to_other_goals", "downstream_constraint", "user_validation_point"],
        "goal_derived_arrangements": ["arrangement_name", "content_digest", "generating_goal", "derivation", "user_validation_point"],
        "delegated_detail_rationale": ["detail_area", "what_is_delegated", "goal_constraint", "reason_for_delegation"],
        "fragile_goal_chains": ["starting_goal", "derived_arrangement", "evidence_or_planning_dependency", "likely_failure_point", "blueprint_revision_if_chain_fails"],
        "strategic_disagreement_diagnosis": ["disagreement_type", "upstream_goal_to_inspect", "affected_goal_or_arrangement", "likely_revision_direction"],
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
        "goal_oriented_structure",
        "goal_cards_are_core",
        "includes_goal_content_digest",
        "uses_semantic_anchors",
        "explains_delegation_interfaces",
        "applies_confirmed_context_filter",
        "outputs_only_remaining_strategic_questions",
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
            "top_level_paper_goal",
            "goal_decomposition",
            "goal_cards",
            "goal_dependency_map",
            "strategic_claim_posture",
            "strategic_evidence_posture",
            "strategic_communication_posture",
            "strategic_risks",
            "delegation_interfaces",
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
        lambda d: validate_goal_cards(d["goal_cards"]),
        lambda d: validate_delegation_interfaces(d["delegation_interfaces"]),
        lambda d: validate_design_rationale(d["design_rationale"]),
        lambda d: validate_style_checks(d["explanation_style_checks"]),
    )
    for validator in validators:
        error = validator(data)
        if error:
            return error
    object_requirements = (
        ("paper_identity", ["research_idea", "target_venue_posture", "paper_type", "research_object", "current_input_state"]),
        ("top_level_paper_goal", ["acceptance_goal", "central_research_bet", "strategic_success_condition", "strategic_downgrade_condition"]),
        ("goal_decomposition", ["positioning_goal", "problem_framing_goal", "contribution_goal", "novelty_boundary_goal", "evidence_goal", "communication_goal", "scope_control_goal", "downstream_planning_goal"]),
        ("goal_dependency_map", ["supports_acceptance_goal", "protects_main_contribution", "protects_novelty_boundary", "determines_evidence_posture", "determines_communication_posture", "downstream_operationalization", "fragile_goals"]),
        ("strategic_claim_posture", ["acceptance_goal_claim", "contribution_goal_claim", "evidence_goal_claim", "deferred_claims"]),
        ("strategic_evidence_posture", ["top_level_goal_evidence", "contribution_goal_evidence", "novelty_boundary_evidence", "delegated_experiment_planning"]),
        ("strategic_communication_posture", ["first_reader_belief", "central_abstraction", "story_movement", "delegated_figure_planning", "delegated_content_planning"]),
        ("strategic_risks", ["goal_most_likely_to_fail", "goal_most_likely_to_be_challenged", "goal_most_dependent_on_missing_evidence", "blueprint_changes_if_risks_materialize"]),
    )
    for path, keys in object_requirements:
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


def validate_blueprint_markdown(text: str) -> str | None:
    if "Confirmed User Context" in text or "用户已明确的信息" in text:
        return "paper_blueprint.md must not contain confirmed user context"
    for pattern in TACTICAL_BLUEPRINT_PATTERNS:
        if pattern.lower() in text.lower():
            return f"paper_blueprint.md contains tactical detail instead of goal-oriented strategy: {pattern}"
    if contains_synthetic_id(text):
        return "paper_blueprint.md contains synthetic object IDs; use semantic headings"
    for heading in REQUIRED_BLUEPRINT_HEADINGS:
        if not heading_present(text, heading):
            return f"paper_blueprint.md must contain goal-oriented heading '{heading}'"
    for heading in FORBIDDEN_LEGACY_BLUEPRINT_HEADINGS:
        if heading_present(text, heading):
            return f"paper_blueprint.md still contains legacy strategic-posture heading '{heading}'"
    goal_cards = extract_section(text, "Goal Cards")
    if not goal_cards.strip():
        return "paper_blueprint.md must contain Goal Cards section content"
    card_count = len(re.findall(r"^###\s+", goal_cards, flags=re.MULTILINE))
    if card_count < 6:
        return f"Goal Cards section must contain at least 6 goal cards; found {card_count}"
    for field in GOAL_CARD_FIELDS:
        if f"**{field}.**" not in goal_cards:
            return f"Goal Cards section missing field '{field}'"
    return None


def validate_explanation_markdown(text: str) -> str | None:
    for headings in EXPLANATION_HEADING_PATTERNS:
        if not heading_containing_present(text, headings):
            return f"explanation file must contain a heading matching one of: {', '.join(headings)}"
    for heading in FORBIDDEN_LEGACY_EXPLANATION_HEADINGS:
        if heading_present(text, heading):
            return f"explanation file still contains legacy heading '{heading}'"
    if contains_synthetic_id(text):
        return "explanation file contains synthetic object IDs; use semantic names"
    for pattern in TACTICAL_EXPLANATION_PATTERNS:
        if pattern.lower() in text.lower():
            return f"explanation file asks about tactical detail instead of strategy: {pattern}"
    if len(SECTION_REF_RE.findall(text)) > 8:
        return "explanation file relies too heavily on numbered section references"
    return None


def validate_markdown_files(data: dict, base_dir: Path) -> str | None:
    files = data["output_files"]
    blueprint_path = resolve_output_path(files["blueprint_markdown"], base_dir)
    explanation_path = resolve_output_path(files["explanation_markdown"], base_dir)
    if blueprint_path.exists():
        error = validate_blueprint_markdown(blueprint_path.read_text(encoding="utf-8-sig"))
        if error:
            return error
    if explanation_path.exists():
        error = validate_explanation_markdown(explanation_path.read_text(encoding="utf-8-sig"))
        if error:
            return error
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
    print("[OK] goal-oriented strategic paper blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
