"""Validate a minimal paper-blueprint summary JSON file."""

import json
import sys
from pathlib import Path


VALID_CLAIM_STATUS = {
    "supported",
    "unsupported",
    "needs_experiment",
    "needs_verification",
}
VALID_RELATED_STATUS = {"verified", "tentative", "needs_verification"}
VALID_RELATED_ROLE = {"required_baseline", "required_citation", "contextual"}
VALID_EXEMPLAR_STATUS = {"verified", "tentative", "needs_verification"}


def fail(message: str) -> int:
    print(f"[ERROR] {message}")
    return 1


def require_keys(obj: dict, keys: list[str], path: str) -> str | None:
    missing = [key for key in keys if key not in obj]
    if missing:
        return f"{path} missing required key(s): {', '.join(missing)}"
    return None


def load_blueprint(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("top-level JSON must be an object")
    return data.get("paper_blueprint", data)


def validate_exemplar_analysis(exemplar_analysis: dict) -> str | None:
    if not isinstance(exemplar_analysis, dict):
        return "exemplar_analysis must be an object"
    error = require_keys(
        exemplar_analysis,
        [
            "enabled",
            "target_venue_exemplars",
            "field_exemplars",
            "nearest_neighbor_exemplars",
        ],
        "exemplar_analysis",
    )
    if error:
        return error
    if not isinstance(exemplar_analysis["enabled"], bool):
        return "exemplar_analysis.enabled must be a boolean"

    group_requirements = {
        "target_venue_exemplars": [
            "title",
            "venue",
            "source",
            "influence_signal",
            "core_pattern",
            "transferable_lesson",
            "non_transferable_warning",
            "verification_status",
        ],
        "field_exemplars": [
            "title",
            "venue",
            "source",
            "influence_signal",
            "core_pattern",
            "transferable_lesson",
            "non_transferable_warning",
            "verification_status",
        ],
        "nearest_neighbor_exemplars": [
            "title",
            "venue",
            "source",
            "relation_to_current_work",
            "reviewer_comparison_risk",
            "transferable_lesson",
            "non_transferable_warning",
            "verification_status",
        ],
    }

    for group, keys in group_requirements.items():
        exemplars = exemplar_analysis[group]
        if not isinstance(exemplars, list):
            return f"exemplar_analysis.{group} must be an array"
        if exemplar_analysis["enabled"] and not exemplars:
            return f"exemplar_analysis.{group} must not be empty when exemplar analysis is enabled"
        for index, exemplar in enumerate(exemplars, start=1):
            if not isinstance(exemplar, dict):
                return f"exemplar_analysis.{group}[{index}] must be an object"
            error = require_keys(exemplar, keys, f"exemplar_analysis.{group}[{index}]")
            if error:
                return error
            if exemplar["verification_status"] not in VALID_EXEMPLAR_STATUS:
                return (
                    f"exemplar_analysis.{group}[{index}].verification_status must be one of "
                    f"{sorted(VALID_EXEMPLAR_STATUS)}"
                )
            if not exemplar["non_transferable_warning"]:
                return f"exemplar_analysis.{group}[{index}] needs a non_transferable_warning"
    return None


def validate(data: dict) -> str | None:
    top_error = require_keys(
        data,
        [
            "output_language",
            "reasoning_summary_mode",
            "title",
            "target_venue",
            "contribution_type",
            "exemplar_analysis",
            "distilled_excellence_patterns",
            "acceptance_hypothesis",
            "claims",
            "related_work",
            "figures_and_tables",
            "reviewer_risks",
            "reasoning_summary",
            "blueprint_decision_log",
            "reproducibility",
            "missing_evidence",
            "next_actions",
        ],
        "paper_blueprint",
    )
    if top_error:
        return top_error
    if not data["output_language"]:
        return "output_language is required"
    if data["reasoning_summary_mode"] != "decision_log":
        return "reasoning_summary_mode must be decision_log"

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
    if venue["fit_score"] is not None and not venue["fit_rationale"]:
        return "target_venue.fit_rationale is required when fit_score is set"

    exemplar_error = validate_exemplar_analysis(data["exemplar_analysis"])
    if exemplar_error:
        return exemplar_error

    patterns = data["distilled_excellence_patterns"]
    if not isinstance(patterns, list):
        return "distilled_excellence_patterns must be an array"
    pattern_names = set()
    for index, pattern in enumerate(patterns, start=1):
        if not isinstance(pattern, dict):
            return f"distilled_excellence_patterns[{index}] must be an object"
        error = require_keys(
            pattern,
            ["pattern", "evidence_from_exemplars", "implication_for_current_blueprint", "used_in_blueprint"],
            f"distilled_excellence_patterns[{index}]",
        )
        if error:
            return error
        pattern_names.add(pattern["pattern"])
        if not pattern["evidence_from_exemplars"]:
            return f"distilled_excellence_patterns[{index}] needs evidence_from_exemplars"

    claims = data["claims"]
    if not isinstance(claims, list) or not claims:
        return "claims must be a non-empty array"

    claim_ids = set()
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            return f"claims[{index}] must be an object"
        error = require_keys(
            claim,
            [
                "id",
                "claim",
                "evidence_required",
                "baselines",
                "baseline_gap_rationale",
                "metrics",
                "figure_or_table",
                "influenced_by_exemplar_patterns",
                "failure_condition",
                "status",
            ],
            f"claims[{index}]",
        )
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
        unknown_patterns = [
            pattern for pattern in claim["influenced_by_exemplar_patterns"] if pattern not in pattern_names
        ]
        if unknown_patterns:
            return f"claims[{index}] references unknown exemplar pattern(s): {', '.join(unknown_patterns)}"

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
        if not item["supports_claims"]:
            return f"figures_and_tables[{index}] must support at least one claim"
        unknown_claims = [claim_id for claim_id in item["supports_claims"] if claim_id not in claim_ids]
        if unknown_claims:
            return f"figures_and_tables[{index}] references unknown claim(s): {', '.join(unknown_claims)}"
        for pattern in item.get("influenced_by_exemplar_patterns", []):
            if pattern not in pattern_names:
                return f"figures_and_tables[{index}] references unknown exemplar pattern: {pattern}"

    if any(claim["status"] == "unsupported" for claim in claims):
        unsupported_ids = [claim["id"] for claim in claims if claim["status"] == "unsupported"]
        print(f"[WARN] unsupported claims present: {', '.join(unsupported_ids)}")

    summary = data["reasoning_summary"]
    if not isinstance(summary, dict):
        return "reasoning_summary must be an object"
    summary_error = require_keys(
        summary,
        [
            "user_request_interpretation",
            "assumptions",
            "deepresearch_usage",
            "evidence_used",
            "exemplar_pattern_summary",
            "key_decisions",
            "downgraded_claims",
            "unresolved_uncertainties",
            "evidence_that_would_change_blueprint",
        ],
        "reasoning_summary",
    )
    if summary_error:
        return summary_error
    for key in (
        "assumptions",
        "evidence_used",
        "exemplar_pattern_summary",
        "key_decisions",
        "downgraded_claims",
        "unresolved_uncertainties",
        "evidence_that_would_change_blueprint",
    ):
        if not isinstance(summary[key], list):
            return f"reasoning_summary.{key} must be an array"

    decision_log = data["blueprint_decision_log"]
    if not isinstance(decision_log, list):
        return "blueprint_decision_log must be an array"
    for index, entry in enumerate(decision_log, start=1):
        if not isinstance(entry, dict):
            return f"blueprint_decision_log[{index}] must be an object"
        error = require_keys(
            entry,
            ["decision", "reason", "supporting_exemplar_pattern", "uncertainty"],
            f"blueprint_decision_log[{index}]",
        )
        if error:
            return error
        pattern = entry["supporting_exemplar_pattern"]
        if pattern and pattern != "none" and pattern not in pattern_names:
            return f"blueprint_decision_log[{index}] references unknown exemplar pattern: {pattern}"

    return None


def main() -> int:
    if len(sys.argv) != 2:
        return fail("Usage: validate_blueprint.py <blueprint-summary.json>")

    path = Path(sys.argv[1])
    if not path.exists():
        return fail(f"File not found: {path}")

    try:
        data = load_blueprint(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return fail(str(exc))

    error = validate(data)
    if error:
        return fail(error)

    print("[OK] blueprint summary passes structural checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
