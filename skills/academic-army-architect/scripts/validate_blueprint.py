"""Validate a minimal paper-blueprint summary JSON file."""

from datetime import datetime
import json
import sys
from pathlib import Path


VALID_CLAIM_STATUS = {"supported", "unsupported", "needs_experiment", "needs_verification"}
VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_RELATED_ROLE = {"required_baseline", "required_citation", "contextual"}
VALID_STORY_RECENCY = {"last_2_3_years", "latest_3_cycles", "expanded_last_5_years", "needs_verification"}


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


def validate_core_focus_items(items: list) -> tuple[str | None, set[str]]:
    if not isinstance(items, list) or not items:
        return "core_focus_items must be a non-empty array", set()
    ids = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"core_focus_items[{index}] must be an object", set()
        error = require_keys(item, ["id", "focus", "purpose", "primary_blueprint_sections"], f"core_focus_items[{index}]")
        if error:
            return error, set()
        if not item["id"].startswith("K"):
            return f"core_focus_items[{index}].id must start with K", set()
        if item["id"] in ids:
            return f"duplicate core focus id: {item['id']}", set()
        ids.add(item["id"])
        if not isinstance(item["primary_blueprint_sections"], list) or not item["primary_blueprint_sections"]:
            return f"core_focus_items[{index}].primary_blueprint_sections must be a non-empty array", set()
    return None, ids


def validate_section_traceability(items: list, core_focus_ids: set[str]) -> str | None:
    if not isinstance(items, list) or not items:
        return "section_traceability must be a non-empty array"
    required_sections = {
        "Metadata",
        "Target Venue and Contribution Type",
        "Acceptance Hypothesis",
        "Core Claims",
        "Related-Work Positioning",
        "Method Blueprint",
        "Evaluation Blueprint",
        "Figure and Table Storyboard",
        "Section-by-Section Outline",
        "Reviewer Risk Register",
        "Reproducibility and Artifact Plan",
        "Missing Evidence",
        "Next Actions",
    }
    covered = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"section_traceability[{index}] must be an object"
        error = require_keys(item, ["blueprint_section", "core_focus_ids", "related_blueprint_ids", "why_this_section_exists", "downstream_impact"], f"section_traceability[{index}]")
        if error:
            return error
        covered.add(item["blueprint_section"])
        if not item["core_focus_ids"]:
            return f"section_traceability[{index}] needs core_focus_ids"
        unknown = [focus_id for focus_id in item["core_focus_ids"] if focus_id not in core_focus_ids]
        if unknown:
            return f"section_traceability[{index}] references unknown core focus id(s): {', '.join(unknown)}"
    missing = sorted(required_sections - covered)
    if missing:
        return f"section_traceability missing major section(s): {', '.join(missing)}"
    return None


def validate_claim_traceability(items: list, core_focus_ids: set[str], claim_ids: set[str]) -> str | None:
    if not isinstance(items, list) or not items:
        return "claim_traceability must be a non-empty array"
    covered = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            return f"claim_traceability[{index}] must be an object"
        error = require_keys(item, ["claim_id", "core_focus_ids", "supporting_experiments", "supporting_figures_or_tables", "main_reviewer_risks", "explanation"], f"claim_traceability[{index}]")
        if error:
            return error
        if item["claim_id"] not in claim_ids:
            return f"claim_traceability[{index}] references unknown claim: {item['claim_id']}"
        covered.add(item["claim_id"])
        unknown = [focus_id for focus_id in item["core_focus_ids"] if focus_id not in core_focus_ids]
        if unknown:
            return f"claim_traceability[{index}] references unknown core focus id(s): {', '.join(unknown)}"
        if not item["supporting_experiments"]:
            return f"claim_traceability[{index}] needs supporting_experiments"
        if not item["supporting_figures_or_tables"]:
            return f"claim_traceability[{index}] needs supporting_figures_or_tables"
        if not item["main_reviewer_risks"]:
            return f"claim_traceability[{index}] needs main_reviewer_risks"
    missing = sorted(claim_ids - covered)
    if missing:
        return f"claim_traceability missing claim(s): {', '.join(missing)}"
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
            "core_focus_items",
            "acceptance_hypothesis",
            "claims",
            "related_work",
            "figures_and_tables",
            "section_traceability",
            "claim_traceability",
            "explanation_decision_log",
            "risks",
            "next_actions",
        ],
        "paper_blueprint_summary",
    )
    if top_error:
        return top_error

    for validator in (validate_output_files, lambda d: validate_exemplar_analysis(d["exemplar_analysis"])):
        error = validator(data)
        if error:
            return error

    focus_error, core_focus_ids = validate_core_focus_items(data["core_focus_items"])
    if focus_error:
        return focus_error

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

    claims = data["claims"]
    if not isinstance(claims, list) or not claims:
        return "claims must be a non-empty array"
    claim_ids = set()
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            return f"claims[{index}] must be an object"
        error = require_keys(claim, ["id", "claim", "evidence_required", "baselines", "baseline_gap_rationale", "metrics", "figure_or_table", "related_experiments", "related_risks", "failure_condition", "status"], f"claims[{index}]")
        if error:
            return error
        claim_ids.add(claim["id"])
        if claim["status"] not in VALID_CLAIM_STATUS:
            return f"claims[{index}].status must be one of {sorted(VALID_CLAIM_STATUS)}"
        if not claim["evidence_required"]:
            return f"claims[{index}] must include evidence_required"
        if not claim["baselines"] and not claim["baseline_gap_rationale"]:
            return f"claims[{index}] needs baselines or baseline_gap_rationale"
        if not claim["failure_condition"]:
            return f"claims[{index}] needs a failure_condition"

    related_work = data["related_work"]
    if not isinstance(related_work, list):
        return "related_work must be an array"
    for index, work in enumerate(related_work, start=1):
        if not isinstance(work, dict):
            return f"related_work[{index}] must be an object"
        error = require_keys(work, ["title", "source", "delta", "role", "verification_status"], f"related_work[{index}]")
        if error:
            return error
        if work["role"] not in VALID_RELATED_ROLE:
            return f"related_work[{index}].role must be one of {sorted(VALID_RELATED_ROLE)}"
        if work["verification_status"] not in VALID_RELATED_STATUS:
            return f"related_work[{index}].verification_status must be one of {sorted(VALID_RELATED_STATUS)}"

    figures = data["figures_and_tables"]
    if not isinstance(figures, list):
        return "figures_and_tables must be an array"
    for index, item in enumerate(figures, start=1):
        if not isinstance(item, dict):
            return f"figures_and_tables[{index}] must be an object"
        error = require_keys(item, ["id", "message", "supports_claims"], f"figures_and_tables[{index}]")
        if error:
            return error
        unknown = [claim_id for claim_id in item["supports_claims"] if claim_id not in claim_ids]
        if unknown:
            return f"figures_and_tables[{index}] references unknown claim(s): {', '.join(unknown)}"

    section_error = validate_section_traceability(data["section_traceability"], core_focus_ids)
    if section_error:
        return section_error
    claim_trace_error = validate_claim_traceability(data["claim_traceability"], core_focus_ids, claim_ids)
    if claim_trace_error:
        return claim_trace_error

    decision_log = data["explanation_decision_log"]
    if not isinstance(decision_log, list):
        return "explanation_decision_log must be an array"
    for index, entry in enumerate(decision_log, start=1):
        if not isinstance(entry, dict):
            return f"explanation_decision_log[{index}] must be an object"
        error = require_keys(entry, ["decision", "blueprint_id", "reason", "evidence_or_pattern", "uncertainty"], f"explanation_decision_log[{index}]")
        if error:
            return error

    if any(claim["status"] == "unsupported" for claim in claims):
        unsupported_ids = [claim["id"] for claim in claims if claim["status"] == "unsupported"]
        print(f"[WARN] unsupported claims present: {', '.join(unsupported_ids)}")
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
    if error:
        return fail(error)

    print("[OK] blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
