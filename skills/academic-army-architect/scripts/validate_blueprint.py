"""Validate a minimal paper-blueprint summary JSON file."""

from datetime import datetime
import json
import re
import sys
from pathlib import Path
from typing import Any


VALID_CLAIM_STATUS = {"supported", "unsupported", "needs_experiment", "needs_verification"}
VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_RELATED_ROLE = {"required_baseline", "required_citation", "contextual"}
VALID_STORY_RECENCY = {"last_2_3_years", "latest_3_cycles", "expanded_last_5_years", "needs_verification"}
OFF_SCOPE_BLUEPRINT_PATTERNS = {
    "Artifact cautions",
    "Assumptions to validate",
    "Metadata and Input State",
    "Review Risk Mitigation Plan",
    "Evidence Gaps and Dependencies",
    "Execution Plan",
    "Do not assume",
    "You should",
    "Be careful",
    "Remember",
    "It is important to note",
    "Caution",
    "Warning",
    "Reasoning Summary",
    "High-impact paper pattern analysis",
    "why I chose",
}
OFF_SCOPE_EXPLANATION_PATTERNS = {
    "deepresearch",
    "MCP",
    "web search",
    "rate limit",
    "probe",
    "PDF parsing",
    "output directory",
    "downstream agent",
    "implementation agent",
    "experiment agent",
    "writing agent",
    "two files",
    "output format",
    "specification format",
    "implementation-plan format",
    "how to use the files",
    "next steps",
    "TODO",
    "Execution Plan",
    "Evidence Gaps and Dependencies",
    "Review Risk Mitigation Plan",
}
SYNTHETIC_ID_RE = re.compile(r"\b(?:C|E|R|A|B|K|D)[1-9]\d?\b|\b(?:F|T)[1-9]\d?\b(?!\s*[- ]?score)|\bAR[1-9]\d?\b")


def fail(message: str) -> int:
    print(f"[ERROR] {message}")
    return 1


def require_keys(obj: dict, keys: list[str], path: str) -> str | None:
    missing = [key for key in keys if key not in obj]
    if missing:
        return f"{path} missing required key(s): {', '.join(missing)}"
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
        if not exemplar["non_transferable_warning"]:
            return f"storytelling_exemplars[{index}] needs a non_transferable_warning"

    for group in ("technical_exemplars", "evaluation_exemplars"):
        exemplars = exemplar_analysis[group]
        if not isinstance(exemplars, list):
            return f"exemplar_analysis.{group} must be an array"
        for index, exemplar in enumerate(exemplars, start=1):
            if not isinstance(exemplar, dict):
                return f"{group}[{index}] must be an object"
            error = require_keys(exemplar, ["title", "venue", "year", "source", "verification_status"], f"{group}[{index}]")
            if error:
                return error
            if exemplar["verification_status"] not in VALID_RELATED_STATUS:
                return f"{group}[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
    return None


def validate_design_rationale(rationale: dict) -> str | None:
    if not isinstance(rationale, dict):
        return "design_rationale must be an object"
    error = require_keys(
        rationale,
        [
            "core_judgment",
            "venue_storytelling_patterns",
            "technical_anchor_rationale",
            "claim_rationale",
            "experiment_rationale",
            "figure_rationale",
            "scope_and_limitation_rationale",
        ],
        "design_rationale",
    )
    if error:
        return error
    if not rationale["core_judgment"]:
        return "design_rationale.core_judgment is required"
    for group, keys in {
        "venue_storytelling_patterns": ["pattern", "influence_on_blueprint"],
        "technical_anchor_rationale": ["anchor", "influence_on_method_or_evaluation"],
        "claim_rationale": ["claim_section", "why_scoped_this_way", "relation_to_thesis"],
        "experiment_rationale": ["experiment_section", "why_needed", "relation_to_claims"],
        "figure_rationale": ["figure_section", "narrative_role"],
    }.items():
        items = rationale[group]
        if not isinstance(items, list):
            return f"design_rationale.{group} must be an array"
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                return f"{group}[{index}] must be an object"
            error = require_keys(item, keys, f"{group}[{index}]")
            if error:
                return error
    return None


def validate_section_ref(value: str, path: str) -> str | None:
    if not isinstance(value, str) or not value:
        return f"{path} must be a non-empty string"
    if not re.search(r"\b(?:[1-9]|1[0-2])(?:\.\d+)?\b", value):
        return f"{path} should use a natural section reference such as 'Section 7.1'"
    return None


def validate_style_checks(style_checks: dict) -> str | None:
    if not isinstance(style_checks, dict):
        return "explanation_style_checks must be an object"
    required = [
        "paper_design_rationale_only",
        "no_tool_process",
        "no_file_format_rationale",
        "no_downstream_agent_usage",
        "no_project_todos",
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
            "target_venue",
            "contribution_type",
            "exemplar_analysis",
            "distilled_patterns",
            "design_rationale",
            "central_thesis",
            "problem_framing",
            "core_idea",
            "method_design",
            "claims",
            "related_work",
            "experiments",
            "figures_and_tables",
            "paper_structure",
            "reproducibility_assets",
            "limitations_and_scope",
            "explanation_style_checks",
        ],
        "paper_blueprint_summary",
    )
    if top_error:
        return top_error

    synthetic_path = find_synthetic_id_path(data)
    if synthetic_path:
        return f"synthetic object ID found in {synthetic_path}; use natural section references instead"

    for validator in (
        validate_output_files,
        lambda d: validate_exemplar_analysis(d["exemplar_analysis"]),
        lambda d: validate_design_rationale(d["design_rationale"]),
        lambda d: validate_style_checks(d["explanation_style_checks"]),
    ):
        error = validator(data)
        if error:
            return error

    venue = data["target_venue"]
    if not isinstance(venue, dict):
        return "target_venue must be an object"
    venue_error = require_keys(venue, ["primary", "fit_score", "fit_rationale"], "target_venue")
    if venue_error:
        return venue_error
    if venue["fit_score"] is not None and not isinstance(venue["fit_score"], int):
        return "target_venue.fit_score must be an integer or null"
    if isinstance(venue["fit_score"], int) and not 1 <= venue["fit_score"] <= 5:
        return "target_venue.fit_score must be between 1 and 5"

    for path, keys in (
        ("central_thesis", ["thesis", "acceptance_critical_statement", "contribution_boundary"]),
        ("problem_framing", ["community_pain_point", "why_now", "existing_approach_gap"]),
        ("core_idea", ["insight", "narrative_center_rationale", "tradeoff_changed"]),
    ):
        obj = data[path]
        if not isinstance(obj, dict):
            return f"{path} must be an object"
        error = require_keys(obj, keys, path)
        if error:
            return error

    method_error = validate_method_design(data["method_design"])
    if method_error:
        return method_error
    claim_error = validate_claims(data["claims"])
    if claim_error:
        return claim_error
    related_error = validate_related_work(data["related_work"])
    if related_error:
        return related_error
    experiment_error = validate_experiments(data["experiments"])
    if experiment_error:
        return experiment_error
    figure_error = validate_figures_and_tables(data["figures_and_tables"])
    if figure_error:
        return figure_error
    structure_error = validate_paper_structure(data["paper_structure"])
    if structure_error:
        return structure_error
    asset_error = validate_reproducibility_assets(data["reproducibility_assets"])
    if asset_error:
        return asset_error
    limitation_error = validate_limitations(data["limitations_and_scope"])
    if limitation_error:
        return limitation_error

    unsupported = [claim["title"] for claim in data["claims"] if claim["status"] == "unsupported"]
    if unsupported:
        print(f"[WARN] unsupported claims present: {', '.join(unsupported)}")
    return None


def validate_method_design(method_design: dict) -> str | None:
    if not isinstance(method_design, dict):
        return "method_design must be an object"
    error = require_keys(method_design, ["components", "assumptions"], "method_design")
    if error:
        return error
    if not isinstance(method_design["components"], list) or not method_design["components"]:
        return "method_design.components must be a non-empty array"
    for index, component in enumerate(method_design["components"], start=1):
        error = require_keys(component, ["title", "function", "relation_to_thesis"], f"method_design.components[{index}]")
        if error:
            return error
    return None


def validate_claims(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "claims must be a non-empty array"
    for index, claim in enumerate(items, start=1):
        if not isinstance(claim, dict):
            return f"claims[{index}] must be an object"
        error = require_keys(
            claim,
            [
                "section_reference",
                "title",
                "claim",
                "why_it_matters_to_thesis",
                "evidence_required",
                "baselines",
                "baseline_gap_rationale",
                "metrics",
                "connected_experiment_sections",
                "connected_figure_sections",
                "connected_scope_sections",
                "failure_condition",
                "status",
            ],
            f"claims[{index}]",
        )
        if error:
            return error
        section_error = validate_section_ref(claim["section_reference"], f"claims[{index}].section_reference")
        if section_error:
            return section_error
        if claim["status"] not in VALID_CLAIM_STATUS:
            return f"claims[{index}].status must be one of {sorted(VALID_CLAIM_STATUS)}"
        if not claim["evidence_required"]:
            return f"claims[{index}] must include evidence_required"
        if not claim["baselines"] and not claim["baseline_gap_rationale"]:
            return f"claims[{index}] needs baselines or baseline_gap_rationale"
        if not claim["failure_condition"]:
            return f"claims[{index}] needs a failure_condition"
    return None


def validate_related_work(items: list) -> str | None:
    if not isinstance(items, list):
        return "related_work must be an array"
    for index, work in enumerate(items, start=1):
        if not isinstance(work, dict):
            return f"related_work[{index}] must be an object"
        error = require_keys(work, ["title", "source", "delta", "role", "verification_status"], f"related_work[{index}]")
        if error:
            return error
        if work["role"] not in VALID_RELATED_ROLE:
            return f"related_work[{index}].role must be one of {sorted(VALID_RELATED_ROLE)}"
        if work["verification_status"] not in VALID_RELATED_STATUS:
            return f"related_work[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"
    return None


def validate_experiments(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "experiments must be a non-empty array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"experiments[{index}] must be an object"
        error = require_keys(item, ["section_reference", "title", "purpose", "datasets_or_workloads", "baselines", "metrics", "evidence_role", "connected_claim_sections"], f"experiments[{index}]")
        if error:
            return error
        section_error = validate_section_ref(item["section_reference"], f"experiments[{index}].section_reference")
        if section_error:
            return section_error
    return None


def validate_figures_and_tables(items: list) -> str | None:
    if not isinstance(items, list):
        return "figures_and_tables must be an array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"figures_and_tables[{index}] must be an object"
        error = require_keys(item, ["section_reference", "title", "message", "narrative_role", "supports_claim_sections", "data_source"], f"figures_and_tables[{index}]")
        if error:
            return error
        section_error = validate_section_ref(item["section_reference"], f"figures_and_tables[{index}].section_reference")
        if section_error:
            return section_error
    return None


def validate_paper_structure(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "paper_structure must be a non-empty array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"paper_structure[{index}] must be an object"
        error = require_keys(item, ["section_name", "rhetorical_role", "required_content"], f"paper_structure[{index}]")
        if error:
            return error
    return None


def validate_reproducibility_assets(items: list) -> str | None:
    if not isinstance(items, list):
        return "reproducibility_assets must be an array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"reproducibility_assets[{index}] must be an object"
        error = require_keys(item, ["title", "asset_type", "contents", "claim_sections_supported", "status"], f"reproducibility_assets[{index}]")
        if error:
            return error
    return None


def validate_limitations(items: list) -> str | None:
    if not isinstance(items, list) or not items:
        return "limitations_and_scope must be a non-empty array"
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"limitations_and_scope[{index}] must be an object"
        error = require_keys(item, ["section_reference", "title", "boundary_or_limitation", "reason_for_boundary", "affected_claim_sections"], f"limitations_and_scope[{index}]")
        if error:
            return error
        section_error = validate_section_ref(item["section_reference"], f"limitations_and_scope[{index}].section_reference")
        if section_error:
            return section_error
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
                return f"paper_blueprint.md contains off-scope workflow/advisory text: {pattern}"
        if contains_synthetic_id(text):
            return "paper_blueprint.md contains synthetic object IDs; use natural section numbering instead"
        required_headings = [
            "## 1. Target Venue and Paper Type",
            "## 2. Central Thesis",
            "## 3. Problem Framing",
            "## 4. Related-Work and Novelty Boundary",
            "## 5. Core Idea",
            "## 6. Method Design",
            "## 7. Claims and Evidence Plan",
            "## 8. Experimental Design",
            "## 9. Figure and Table Plan",
            "## 10. Paper Structure",
            "## 11. Reproducibility-Relevant Assets",
            "## 12. Limitations and Scope Boundaries",
        ]
        for heading in required_headings:
            if heading not in text:
                return f"paper_blueprint.md must contain '{heading}'"

    if explanation_path.exists():
        text = explanation_path.read_text(encoding="utf-8-sig")
        if "paper_blueprint_summary:" in text:
            return "explanation file appears to duplicate machine-oriented blueprint content"
        if contains_synthetic_id(text):
            return "explanation file contains synthetic object IDs; use natural section references instead"
        for pattern in OFF_SCOPE_EXPLANATION_PATTERNS:
            if pattern.lower() in text.lower():
                return f"explanation file leaves the paper-strategy scope: {pattern}"
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

    print("[OK] blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
