---
name: academic-army-architect
description: >-
  This skill creates, refines, and revises evidence-grounded academic paper blueprints from research ideas, draft notes, plans, or existing blueprint files. It uses DeepResearch for literature synthesis, venue fit, contribution framing, claim strength, evaluation design, artifact discovery, and substantive revisions. It renders paper_blueprint.md, paper_blueprint_analysis.md, and source_ledger.json when a durable project state is needed.
---

# Academic Army Architect

## Purpose

This skill turns a research idea into a concise paper blueprint with traceable scholarly support.

Primary outputs:

1. `paper_blueprint.md`
2. `paper_blueprint_analysis.md`
3. `source_ledger.json`

## Workflow

1. Classify the request:
   - `new_blueprint_from_incomplete_idea`
   - `new_blueprint_from_complete_plan`
   - `revise_existing_blueprint`
   - `rebase_to_new_venue_or_journal`
   - `fine_edit_existing_blueprint`
2. Gather the field, problem, method, evidence, target venue, and available data or artifacts. Use `TBD` for unknown fields. Ask up to 3 targeted questions when the idea is too thin to brief.
3. Use DeepResearch for substantive scholarly judgment: related work, novelty, venue expectations, contribution scope, claim strength, method design, evaluation design, and artifact landscape.
4. Keep mechanical edits local: formatting, wording that preserves meaning, section renaming, JSON conversion, and requested field deletion.
5. Render final files from the templates and update provenance.

## DeepResearch

For substantive work:

1. Identify blueprint sections needing research judgment.
2. Read `references/deepresearch_protocol.md`.
3. Read `references/deepresearch_question_plans.md`.
4. Create focused DeepResearch Brief objects from `assets/deepresearch_brief_template.json`.
5. Call `deepresearch` through `academic_army_mcp_tools` with a self-contained prompt.
6. Integrate the returned report into the blueprint, analysis file, and source ledger.

Use separate briefs when a request mixes unrelated judgments.

Question types:

- `venue_style_analysis`
- `related_direction_synthesis`
- `closest_work_comparison`
- `contribution_boundary`
- `claim_strength`
- `method_evaluation_design`
- `artifact_landscape`
- `paper_structure_strategy`
- `revision_impact_analysis`
- `general_blueprint_judgment`

## Provenance

Label substantive decisions as:

- `user_provided`
- `deepresearch_supported`
- `workflow_inferred_from_user_input`
- `TBD`

Use `workflow_inferred_from_user_input` for lightweight inferences from user-provided facts. Record every paper, codebase, dataset, benchmark, artifact, and venue rule that influences the blueprint or analysis.

## Outputs

- Render `paper_blueprint.md` from `assets/blueprint_template.md`.
- Render `paper_blueprint_analysis.md` from `assets/analysis_template.md`.
- Keep the blueprint concise and executable.
- Put rationale, source influence, assumptions, and change history in the analysis file.
- Maintain `source_ledger.json` for project state and future revisions.
- Validate structured artifacts with `scripts/validate_blueprint_json.py`.

## Revision Rules

For existing blueprints:

1. Parse the blueprint, analysis file, and source ledger when available.
2. Classify the requested change.
3. Use DeepResearch for venue, claim, contribution, method, evaluation, related-work, code, dataset, benchmark, artifact, or other intellectual changes.
4. Apply the narrowest useful edit.
5. Update the analysis file, change log, and source ledger.

Preserve unaffected sections unless new evidence changes their meaning.

## Resource Guide

- `references/deepresearch_protocol.md`: DeepResearch role, brief contents, source expectations, and integration boundary.
- `references/deepresearch_question_plans.md`: question-type selection and section mapping.
- `assets/blueprint_template.md`: blueprint structure.
- `assets/analysis_template.md`: analysis structure.
- `assets/deepresearch_brief_template.json`: focused brief starter.
- `assets/source_ledger_template.json`: ledger starter.
- `schemas/*.schema.json`: structured artifact schemas.
- `scripts/validate_blueprint_json.py`: structural validation for blueprint, analysis, ledger, brief, and report JSON.
