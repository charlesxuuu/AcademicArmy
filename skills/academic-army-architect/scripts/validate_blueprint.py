"""Validate a strategic paper-blueprint summary JSON file and optional Markdown outputs."""

from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_STORY_RECENCY = {
    "last_1_3_years",
    "latest_3_cycles",
    "expanded_last_5_years",
    "needs_verification",
}
SOURCE_SIGNAL_GROUPS = [
    "closest_technical_substrate",
    "venue_posture",
    "closest_competing_systems",
    "storytelling_exemplars",
    "method_precedents",
    "evaluation_precedents",
]
CONTRACTS = [
    "content_planning_contract",
    "method_planning_contract",
    "experiment_planning_contract",
    "figure_planning_contract",
]
OPTIONAL_CONTRACTS = ["review_planning_contract", "writing_planning_contract"]

REQUIRED_BLUEPRINT_HEADINGS = [
    "Paper Identity",
    "Strategic Thesis",
    "Canonical Resource Model and Terminology",
    "Core Strategic Goals",
    "Claim and Scope Architecture",
    "Evidence Objectives",
    "Downstream Skill Contract",
]
FORBIDDEN_LEGACY_BLUEPRINT_HEADINGS = [
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
REQUIRED_EXPLANATION_HEADING_PATTERNS = [
    ("What You Should Check First", "优先确认", "最需要确认", "先检查"),
    ("User-Confirmed Inputs", "用户已明确", "已确认输入"),
    ("User-Mentioned Preferences", "用户提到的偏好", "用户提及的偏好"),
    ("Working Assumptions", "工作假设"),
    ("Research Signals Used", "研究信号", "使用的研究依据"),
    ("Core Starting Points", "核心出发点"),
    ("Blueprint Items and Rationale", "蓝图条目", "逐项解释"),
    ("Remaining Strategic Choices", "剩余战略", "仍需确认"),
    ("Change Impact", "输入变化"),
    ("Evidence-Dependent Claim Calibration", "证据依赖", "claim calibration", "声明校准"),
]
FORBIDDEN_LEGACY_EXPLANATION_HEADINGS = [
    "Fragile Goal Chains",
    "Goal Cards",
    "Goal-Oriented Overview",
    "Strategic Defaults and Change Conditions",
]
FORBIDDEN_EXPLANATION_META_PATTERNS = {
    "from the skill",
    "skill's terminology",
    "skill file contract",
    "this skill decided",
    "来自 skill",
    "来自skill",
    "技能的文件契约",
    "术语稳定化要求",
}
EXECUTION_PATH_RE = re.compile(r"[A-Za-z]:\\")

TACTICAL_BLUEPRINT_PATTERNS = {
    "robust mpc",
    "lyapunov",
    "primal-dual",
    "structured bandit",
    "reinforcement learning",
    "pensieve",
    "bola",
    "5g trace",
    "lte trace",
    "wi-fi trace",
    "wifi trace",
    "6dof viewport trace",
    "statistical test",
    "dataset split",
    "device setup",
    "figure 1",
    "figure 2",
    "figure count",
    "one figure",
    "two figures",
    "three figures",
    "four figures",
    "tile priority",
    "tile-based",
    "main-result experiment",
    "ablation experiment",
    "oracle baseline",
    "plotting script",
    "run order",
    "section-by-section outline",
}
TACTICAL_EXPLANATION_QUESTION_PATTERNS = {
    "which algorithm",
    "which dataset",
    "which trace",
    "which baseline",
    "which figure",
    "how many figures",
    "which statistical test",
    "which device",
    "要不要用",
    "用哪种算法",
    "用哪个数据集",
    "用哪条trace",
    "画几张图",
}
FORBIDDEN_BLUEPRINT_META_PATTERNS = {
    "confirmed user context",
    "user-confirmed inputs",
    "the user has provided",
    "the user should confirm",
    "confirm whether",
    "confirmation prompt",
    "current input state",
    "why this goal matters",
    "why this matters",
    "failure or revision implication",
    "failure implication",
    "reviewers may otherwise",
    "reviewers can reject",
    "this skill",
    "this blueprint uses",
    "sources used",
    "research signals used",
}
DEFENSIVE_BLUEPRINT_PATTERNS = {
    "must not",
    "avoid ",
    "does not require",
    "downgrade",
    "can reject",
    "will reject",
}
OVERCOMMITMENT_BLUEPRINT_PATTERNS = {
    "formal control model",
    "formal model",
    "end-to-end prototype",
    "dynamic video",
    "mobile/edge",
    "theorem",
    "regret bound",
    "multi-user",
}
SYNTHETIC_ID_RE = re.compile(
    r"\b(?:C|E|R|A|B|K|D)[1-9]\d?\b|\b(?:F|T)[1-9]\d?\b(?!\s*[- ]?score)|\bAR[1-9]\d?\b"
)
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


def heading_containing_present(text: str, options: tuple[str, ...]) -> bool:
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
    error = require_keys(
        files,
        ["blueprint_markdown", "explanation_markdown", "output_language", "explanation_language_suffix"],
        "output_files",
    )
    if error:
        return error
    if Path(files["blueprint_markdown"]).name != "paper_blueprint.md":
        return "output_files.blueprint_markdown must end with paper_blueprint.md"
    expected_suffix = f"paper_blueprint_explanation.{files['explanation_language_suffix']}.md"
    if Path(files["explanation_markdown"]).name != expected_suffix:
        return f"output_files.explanation_markdown must end with {expected_suffix}"
    if str(files["output_language"]).lower() != "english":
        return "output_files.output_language must be english"
    return None


def validate_confirmed_user_context(context: dict) -> str | None:
    if not isinstance(context, dict):
        return "confirmed_user_context must be an object"
    required = [
        "research_inputs",
        "existing_materials",
        "target_field_or_venue_preferences",
        "paper_type_preferences",
        "existing_method_or_substrate",
        "existing_experiment_or_prototype_foundation",
        "strategic_preferences_or_boundaries",
        "blueprint_purpose",
        "downstream_planning_pipeline",
        "abstraction_level_preferences",
        "explanation_preferences",
        "content_delegated_to_later_planning",
    ]
    error = require_keys(context, required, "confirmed_user_context")
    if error:
        return error
    for key in required:
        if not isinstance(context[key], list):
            return f"confirmed_user_context.{key} must be an array"
    return None


def validate_user_mentioned_preferences(preferences: dict) -> str | None:
    if not isinstance(preferences, dict):
        return "user_mentioned_preferences must be an object"
    required = [
        "method_preferences",
        "evidence_preferences",
        "baseline_or_comparison_preferences",
        "implementation_or_deployment_preferences",
        "language_or_readability_preferences",
    ]
    error = require_keys(preferences, required, "user_mentioned_preferences")
    if error:
        return error
    for key in required:
        if not isinstance(preferences[key], list):
            return f"user_mentioned_preferences.{key} must be an array"
    return None


def validate_working_assumptions(assumptions: list) -> str | None:
    if not isinstance(assumptions, list):
        return "working_assumptions must be an array"
    for index, item in enumerate(assumptions, start=1):
        if not isinstance(item, dict):
            return f"working_assumptions[{index}] must be an object"
        error = require_keys(item, ["assumption", "why_needed", "replaced_by_confirmed_input_when"], f"working_assumptions[{index}]")
        if error:
            return error
    return None


def validate_research_signals(signals: dict) -> str | None:
    if not isinstance(signals, dict):
        return "research_signals_used must be an object"
    error = require_keys(signals, SOURCE_SIGNAL_GROUPS, "research_signals_used")
    if error:
        return error
    current_year = datetime.now().year
    for group in SOURCE_SIGNAL_GROUPS:
        items = signals[group]
        if not isinstance(items, list):
            return f"research_signals_used.{group} must be an array"
        if group in {"closest_technical_substrate", "venue_posture", "closest_competing_systems", "storytelling_exemplars"} and not items:
            return f"research_signals_used.{group} must be a non-empty array"
        for index, item in enumerate(items, start=1):
            required = ["title", "venue_or_source", "year", "link", "lesson_for_blueprint", "verification_status"]
            if group == "storytelling_exemplars":
                required.append("recency_basis")
            error = require_keys(item, required, f"research_signals_used.{group}[{index}]")
            if error:
                return error
            if item["verification_status"] not in VALID_RELATED_STATUS:
                return f"research_signals_used.{group}[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
            if group == "storytelling_exemplars":
                if item["recency_basis"] not in VALID_STORY_RECENCY:
                    return f"research_signals_used.storytelling_exemplars[{index}].recency_basis must be one of {sorted(VALID_STORY_RECENCY)}"
                year = item["year"]
                if isinstance(year, int) and year < current_year - 5:
                    return f"research_signals_used.storytelling_exemplars[{index}] is too old for current storytelling style"
    return None


def validate_core_goals(goals: list) -> str | None:
    if not isinstance(goals, list) or not 4 <= len(goals) <= 8:
        return "core_strategic_goals must contain 4 to 8 strategic goals"
    seen_names: set[str] = set()
    for index, item in enumerate(goals, start=1):
        if not isinstance(item, dict):
            return f"core_strategic_goals[{index}] must be an object"
        error = require_keys(
            item,
            ["goal_name", "objective", "strategic_function", "downstream_constraints", "success_signal"],
            f"core_strategic_goals[{index}]",
        )
        if error:
            return error
        name = item["goal_name"].strip().lower()
        if name in seen_names:
            return f"core_strategic_goals[{index}] duplicates goal_name '{item['goal_name']}'"
        seen_names.add(name)
        error = require_nonempty_list(item, "downstream_constraints", f"core_strategic_goals[{index}]")
        if error:
            return error
    return None


def validate_downstream_contract(contracts: dict) -> str | None:
    if not isinstance(contracts, dict):
        return "downstream_skill_contract must be an object"
    error = require_keys(contracts, CONTRACTS, "downstream_skill_contract")
    if error:
        return error
    optional_contracts = contracts.get("optional_contracts", {})
    if optional_contracts and not isinstance(optional_contracts, dict):
        return "downstream_skill_contract.optional_contracts must be an object"
    contract_names = CONTRACTS + [key for key in OPTIONAL_CONTRACTS if key in contracts]
    for key in OPTIONAL_CONTRACTS:
        if key in optional_contracts:
            contract_names.append(("optional_contracts", key))
    for name in contract_names:
        if isinstance(name, tuple):
            group, child = name
            contract = contracts[group][child]
            path = f"downstream_skill_contract.{group}.{child}"
        else:
            contract = contracts[name]
            path = f"downstream_skill_contract.{name}"
        if not isinstance(contract, dict):
            return f"{path} must be an object"
        error = require_keys(contract, ["purpose", "preserve", "open_tactical_choices"], path)
        if error:
            return error
        for key in ("preserve", "open_tactical_choices"):
            error = require_nonempty_list(contract, key, path)
            if error:
                return error
    return None


def validate_open_strategic_variables(items: list) -> str | None:
    if not isinstance(items, list):
        return "open_strategic_variables must be an array"
    for index, item in enumerate(items, start=1):
        error = require_keys(
            item,
            ["variable", "status", "affects", "current_conservative_stance", "allowed_resolutions", "default_propagation_rule"],
            f"open_strategic_variables[{index}]",
        )
        if error:
            return error
        if str(item["status"]).lower() != "unresolved":
            return f"open_strategic_variables[{index}].status must be unresolved"
        for key in ("affects", "allowed_resolutions"):
            error = require_nonempty_list(item, key, f"open_strategic_variables[{index}]")
            if error:
                return error
        prompt = " ".join(str(value).lower() for value in item.values())
        for pattern in ("confirm whether", "the user should confirm", "confirmation prompt", "please confirm"):
            if pattern in prompt:
                return f"open_strategic_variables[{index}] contains a user-facing confirmation prompt: {pattern}"
        for pattern in TACTICAL_EXPLANATION_QUESTION_PATTERNS:
            if pattern in prompt:
                return f"open_strategic_variables[{index}] asks about tactical detail: {pattern}"
    return None


def validate_explanation_design(design: dict) -> str | None:
    if not isinstance(design, dict):
        return "explanation_design must be an object"
    error = require_keys(
        design,
        [
            "what_to_check_first",
            "source_budget",
            "core_starting_points",
            "blueprint_item_rationales",
            "confirmed_context_coverage",
            "remaining_strategic_choices",
            "change_impact_if_confirmed_inputs_change",
            "evidence_dependent_claim_calibration",
        ],
        "explanation_design",
    )
    if error:
        return error
    source_budget = design["source_budget"]
    if not isinstance(source_budget, dict):
        return "explanation_design.source_budget must be an object"
    error = require_keys(source_budget, ["load_bearing_signal_count", "additional_background_summary"], "explanation_design.source_budget")
    if error:
        return error
    if not isinstance(source_budget["load_bearing_signal_count"], int):
        return "explanation_design.source_budget.load_bearing_signal_count must be an integer"
    if source_budget["load_bearing_signal_count"] > 8:
        return "explanation_design.source_budget.load_bearing_signal_count must be at most 8"
    if not isinstance(source_budget["additional_background_summary"], list):
        return "explanation_design.source_budget.additional_background_summary must be an array"
    groups = {
        "what_to_check_first": ["strategic_judgment", "why_user_should_check_it"],
        "core_starting_points": ["starting_point", "derived_from_confirmed_inputs_or_research_signal"],
        "blueprint_item_rationales": [
            "blueprint_item",
            "item_type",
            "restated_content_digest",
            "derived_from_starting_point",
            "relationship_to_other_blueprint_items",
            "downstream_constraints_explained",
            "user_check_point",
        ],
        "confirmed_context_coverage": [
            "confirmed_context_item",
            "strategic_variable_covered_or_narrowed",
            "effect_on_remaining_questions",
        ],
        "remaining_strategic_choices": [
            "strategic_choice",
            "confirmed_part",
            "unresolved_part",
            "current_default_stance",
            "what_changes_under_different_choices",
        ],
        "change_impact_if_confirmed_inputs_change": [
            "confirmed_input",
            "affected_blueprint_items",
            "likely_revision_direction",
        ],
        "evidence_dependent_claim_calibration": [
            "evidence_outcome",
            "calibrated_claim_level",
            "affected_blueprint_items",
        ],
    }
    for group, keys in groups.items():
        items = design[group]
        if not isinstance(items, list):
            return f"explanation_design.{group} must be an array"
        if group in {"what_to_check_first", "core_starting_points", "blueprint_item_rationales"} and not items:
            return f"explanation_design.{group} must be a non-empty array"
        if group == "what_to_check_first" and len(items) > 6:
            return "explanation_design.what_to_check_first must contain at most 6 items"
        for index, item in enumerate(items, start=1):
            error = require_keys(item, keys, f"explanation_design.{group}[{index}]")
            if error:
                return error
            if group == "remaining_strategic_choices":
                text = " ".join(str(item[key]).lower() for key in keys)
                for pattern in TACTICAL_EXPLANATION_QUESTION_PATTERNS:
                    if pattern in text:
                        return f"explanation_design.remaining_strategic_choices[{index}] asks about tactical detail: {pattern}"
            if group == "blueprint_item_rationales":
                valid_types = {"top_level_section", "core_goal", "open_variable", "downstream_contract"}
                if item["item_type"] not in valid_types:
                    return f"explanation_design.blueprint_item_rationales[{index}].item_type must be one of {sorted(valid_types)}"
    return None


def validate_validation_checks(checks: dict) -> str | None:
    required = [
        "file_separation_check",
        "confirmed_input_hygiene_check",
        "redundancy_check",
        "tactical_leakage_check",
        "defensive_tone_check",
        "question_deduplication_check",
        "source_role_check",
        "source_budget_check",
        "source_role_freshness_check",
        "skill_meta_language_check",
        "item_level_explanation_check",
        "evidence_vs_input_separation_check",
        "terminology_alignment_check",
        "contradiction_check",
        "terminology_check",
        "overcommitment_check",
        "resource_model_completeness_check",
        "baseline_fairness_check",
        "explanation_alignment_check",
        "uses_positive_scope_language",
        "uses_semantic_anchors",
        "outputs_only_remaining_strategic_questions",
        "avoids_tactical_questionnaire",
        "avoids_synthetic_ids",
    ]
    if not isinstance(checks, dict):
        return "validation_checks must be an object"
    error = require_keys(checks, required, "validation_checks")
    if error:
        return error
    for key in required:
        if checks[key] is not True:
            return f"validation_checks.{key} must be true"
    return None


def validate(data: dict) -> str | None:
    top_error = require_keys(
        data,
        [
            "output_files",
            "confirmed_user_context",
            "user_mentioned_preferences",
            "working_assumptions",
            "title",
            "paper_identity",
            "research_signals_used",
            "strategic_thesis",
            "canonical_resource_model_and_terminology",
            "core_strategic_goals",
            "claim_and_scope_architecture",
            "evidence_objectives",
            "downstream_skill_contract",
            "open_strategic_variables",
            "explanation_design",
            "validation_checks",
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
        lambda d: validate_user_mentioned_preferences(d["user_mentioned_preferences"]),
        lambda d: validate_working_assumptions(d["working_assumptions"]),
        lambda d: validate_research_signals(d["research_signals_used"]),
        lambda d: validate_core_goals(d["core_strategic_goals"]),
        lambda d: validate_downstream_contract(d["downstream_skill_contract"]),
        lambda d: validate_open_strategic_variables(d["open_strategic_variables"]),
        lambda d: validate_explanation_design(d["explanation_design"]),
        lambda d: validate_validation_checks(d["validation_checks"]),
    )
    for validator in validators:
        error = validator(data)
        if error:
            return error
    object_requirements = (
        ("paper_identity", ["research_idea", "target_venue_posture", "paper_type", "research_object", "context_anchors"]),
        ("strategic_thesis", ["main_thesis", "central_bet", "acceptance_target"]),
        (
            "canonical_resource_model_and_terminology",
            [
                "canonical_resource_terms",
                "control_object",
                "delivery_unit",
                "reference_state",
                "reference_usefulness",
                "deadline_feasibility_model",
                "metric_families",
            ],
        ),
        (
            "claim_and_scope_architecture",
            ["main_claim", "supporting_claims", "novelty_scope", "positive_scope_boundary", "evidence_dependent_claim_calibration"],
        ),
        (
            "evidence_objectives",
            [
                "metric_families",
                "phenomena_to_establish",
                "system_level_outcomes",
                "baseline_families",
                "evidence_dimensions_to_cover",
                "tactical_choices_delegated_to_experiment_planning",
            ],
        ),
    )
    for path, keys in object_requirements:
        obj = data[path]
        if not isinstance(obj, dict):
            return f"{path} must be an object"
        error = require_keys(obj, keys, path)
        if error:
            return error
    list_fields = {
        "paper_identity": ["context_anchors"],
        "canonical_resource_model_and_terminology": ["canonical_resource_terms", "metric_families"],
        "claim_and_scope_architecture": ["supporting_claims"],
        "evidence_objectives": [
            "metric_families",
            "phenomena_to_establish",
            "system_level_outcomes",
            "baseline_families",
            "evidence_dimensions_to_cover",
            "tactical_choices_delegated_to_experiment_planning",
        ],
    }
    for path, keys in list_fields.items():
        obj = data[path]
        for key in keys:
            if not isinstance(obj[key], list):
                return f"{path}.{key} must be an array"
    terms = data["canonical_resource_model_and_terminology"]["canonical_resource_terms"]
    for index, term in enumerate(terms, start=1):
        if not isinstance(term, dict):
            return f"canonical_resource_model_and_terminology.canonical_resource_terms[{index}] must be an object"
        error = require_keys(
            term,
            ["term", "definition"],
            f"canonical_resource_model_and_terminology.canonical_resource_terms[{index}]",
        )
        if error:
            return error
    term_names = " ".join(str(term.get("term", "")).lower() for term in terms if isinstance(term, dict))
    summary_text = json.dumps(data, ensure_ascii=False).lower()
    if any(marker in summary_text for marker in ("refabr", "3dgs", "gaussian")):
        if "gaussian resource" not in term_names:
            return "canonical_resource_model_and_terminology.canonical_resource_terms must define Gaussian resource for RefABR/3DGS-like blueprints"
    if "reference resource" in summary_text and "reference resource" not in term_names:
        return "canonical_resource_model_and_terminology.canonical_resource_terms must define reference resource when the blueprint uses that term"
    return None


def resolve_output_path(raw_path: str, base_dir: Path) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return base_dir / path


def validate_blueprint_markdown(text: str) -> str | None:
    lower = text.lower()
    for pattern in FORBIDDEN_BLUEPRINT_META_PATTERNS:
        if pattern in lower:
            return f"paper_blueprint.md contains explanation/meta marker: {pattern}"
    for pattern in DEFENSIVE_BLUEPRINT_PATTERNS:
        if pattern in lower:
            return f"paper_blueprint.md contains defensive wording; rewrite as positive scope or claim calibration: {pattern}"
    for pattern in OVERCOMMITMENT_BLUEPRINT_PATTERNS:
        if pattern == "dynamic video" and "dynamic-scene breadth" in lower and "current conservative object" in lower:
            continue
        if pattern == "mobile/edge" and "claim strength" in lower:
            continue
        if pattern in lower:
            return f"paper_blueprint.md contains overcommitted unresolved scope/proof/deployment wording: {pattern}"
    for pattern in TACTICAL_BLUEPRINT_PATTERNS:
        if pattern in lower:
            return f"paper_blueprint.md contains tactical detail instead of strategic specification: {pattern}"
    if contains_synthetic_id(text):
        return "paper_blueprint.md contains synthetic object IDs; use semantic headings"
    for heading in REQUIRED_BLUEPRINT_HEADINGS:
        if not heading_present(text, heading):
            return f"paper_blueprint.md must contain strategic heading '{heading}'"
    for heading in FORBIDDEN_LEGACY_BLUEPRINT_HEADINGS:
        if heading_present(text, heading):
            return f"paper_blueprint.md still contains legacy heading '{heading}'"
    core_goals = extract_section(text, "Core Strategic Goals")
    if not core_goals.strip():
        return "paper_blueprint.md must contain Core Strategic Goals section content"
    objective_count = len(re.findall(r"^Objective:\s+", core_goals, flags=re.MULTILINE))
    if objective_count and not 4 <= objective_count <= 8:
        return f"Core Strategic Goals should define 4 to 8 goals; found {objective_count}"
    if "Research Signals Used" in text or "Source-role" in text:
        return "source-role analysis belongs in the explanation file, not paper_blueprint.md"
    if "svq" in lower:
        return "paper_blueprint.md contains SVQ; use VQ-based wording unless SVQ is user-confirmed or source-confirmed"
    if "reference bits" in lower and "reference resource" not in lower:
        return "paper_blueprint.md uses reference bits without the broader reference resource term"
    open_variables = extract_section(text, "Open Strategic Variables")
    if open_variables.strip():
        for field in ("Status:", "Affects:", "Current conservative stance:", "Allowed resolutions:", "Default propagation rule:"):
            if field not in open_variables:
                return f"Open Strategic Variables missing machine-consumable field '{field}'"
        for pattern in ("Confirm whether", "the user should confirm", "Confirmation prompt", "Please confirm"):
            if pattern.lower() in open_variables.lower():
                return f"Open Strategic Variables contains user-facing prompt language: {pattern}"
    return None


def validate_explanation_markdown(text: str) -> str | None:
    for headings in REQUIRED_EXPLANATION_HEADING_PATTERNS:
        if not heading_containing_present(text, headings):
            return f"explanation file must contain a heading matching one of: {', '.join(headings)}"
    for heading in FORBIDDEN_LEGACY_EXPLANATION_HEADINGS:
        if heading_present(text, heading):
            return f"explanation file still contains legacy heading '{heading}'"
    if contains_synthetic_id(text):
        return "explanation file contains synthetic object IDs; use semantic names"
    lower = text.lower()
    for pattern in FORBIDDEN_EXPLANATION_META_PATTERNS:
        if pattern in lower:
            return f"explanation file contains skill-meta language instead of paper rationale: {pattern}"
    if EXECUTION_PATH_RE.search(text):
        return "explanation file contains local execution path; keep output paths out of paper_blueprint_explanation"
    if "svq" in lower:
        return "explanation file contains SVQ; use VQ-based wording unless SVQ is user-confirmed or source-confirmed"
    if "reference bits" in lower and "bitrate" not in lower and "bandwidth" not in lower:
        return "explanation file uses reference bits outside bitrate/bandwidth context; prefer reference resource"
    if "gaussian bits" in lower and "bitrate" not in lower and "bandwidth" not in lower:
        return "explanation file uses Gaussian bits outside bitrate/bandwidth context; prefer Gaussian resource"
    for pattern in TACTICAL_EXPLANATION_QUESTION_PATTERNS:
        if pattern in lower:
            return f"explanation file asks about tactical detail instead of strategic confirmation: {pattern}"
    if len(SECTION_REF_RE.findall(text)) > 8:
        return "explanation file relies too heavily on numbered section references"
    source_heading = any(heading_containing_present(text, (name,)) for name in ("Research Signals Used", "研究信号", "使用的研究依据"))
    if source_heading:
        role_terms = [
            "Closest technical substrate",
            "Venue posture",
            "Closest competing system",
            "Storytelling exemplar",
            "Method precedent",
            "Evaluation precedent",
            "技术底座",
            "venue",
            "写作",
            "方法先例",
            "评估先例",
        ]
        if not any(term.lower() in lower for term in role_terms):
            return "explanation file has research signals but no source-role labels"
    if "downstream planning implications" in lower or "后续规划影响" in lower:
        section = extract_section(text, "Downstream Planning Implications")
        if section.count("\n") > 8:
            return "Downstream Planning Implications should be omitted or compressed; explain downstream effects item-by-item"
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
    print("[OK] strategic paper blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
