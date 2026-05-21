---
name: academic-army-architect
description: >-
  This skill creates, refines, and revises standardized academic paper blueprints from research ideas, draft notes, plans, or existing blueprint files. It produces paper_blueprint.md, paper_blueprint_analysis.md, and source_ledger.json when product state or revision history is needed. It uses DeepResearch for literature synthesis, venue fit, contribution boundaries, claim strength, evaluation design, artifact discovery, and other scholarly judgments; local orchestration handles intake, briefs, templates, validation, rendering, diffs, and file assembly.
---

# Academic Army Architect

## Purpose

This skill turns a user's research idea into a concise, evidence-grounded paper blueprint. It organizes the idea, identifies missing information, and keeps scholarly claims traceable to user input or DeepResearch evidence.

Primary outputs:

1. `paper_blueprint.md`
2. `paper_blueprint_analysis.md`
3. `source_ledger.json` for product state or revision history

## Operating Model

Use two layers:

- **Orchestration**: intake, task classification, focused briefs, template rendering, schema validation, source-ledger updates, diffs, and mechanical edits.
- **DeepResearch**: literature synthesis, closest-work comparison, venue fit, contribution framing, claim strength, evaluation design, artifact discovery, and uncertainty resolution.

Mechanical edits stay local: typo fixes, Markdown formatting, file renaming, title numbering, JSON conversion, requested field deletion, and wording edits that preserve research meaning.

## Request Modes

Classify each request as one mode:

1. `new_blueprint_from_incomplete_idea`
2. `new_blueprint_from_complete_plan`
3. `revise_existing_blueprint`
4. `rebase_to_new_venue_or_journal`
5. `fine_edit_existing_blueprint`

Modes 1-4 use DeepResearch. Mode 5 uses DeepResearch only when the requested edit changes scholarly meaning.

## Intake

Create a DeepResearch brief when the user's input gives enough context. Use `TBD` for unknown fields.

When context is too thin, ask up to 3 targeted questions, prioritizing:

1. field or subfield
2. core research problem
3. proposed method
4. existing evidence
5. target venue or journal
6. available data, code, or artifacts

## DeepResearch Workflow

For substantive blueprint work:

1. Identify sections needing scholarly judgment.
2. Read `references/deepresearch_protocol.md`.
3. Read `references/deepresearch_question_plans.md`.
4. Create one or more focused `DeepResearch Brief` objects.
5. Call DeepResearch with `scripts/call_deepresearch.py` or the product API layer.
6. Integrate the returned report into the blueprint, analysis file, and source ledger.

Focused question types:

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

Use separate focused questions when a broad request mixes unrelated judgments.

## Research Gate

DeepResearch supplies scholarly judgment. If the DeepResearch call fails after retry, leave research-dependent outputs unchanged and return the failure for retry. Mechanical edits that do not require research may continue.

## Provenance

Track each substantive decision as:

- `user_provided`
- `deepresearch_supported`
- `workflow_inferred_from_user_input`
- `TBD`

Use `workflow_inferred_from_user_input` only for lightweight inferences from the user's own facts. Record every paper, codebase, dataset, benchmark, artifact, and venue rule used in the blueprint or analysis.

## Outputs

Render `paper_blueprint.md` from `assets/blueprint_template.md` and preserve its 15 top-level sections unless the user requests a custom export.

Render `paper_blueprint_analysis.md` from `assets/analysis_template.md` and preserve its 14 top-level sections. Use the user's conversation language unless another language is requested. Keep `Referenced Papers` as the final section.

Keep the blueprint concise and executable. Put rationale, source influence, assumptions, and change history in the analysis file.

Maintain `source_ledger.json` for product state, revision history, and future edit context. Validate it with `schemas/source_ledger.schema.json`.

## Revision Workflow

For existing blueprints:

1. Parse the blueprint.
2. Parse the analysis file and source ledger when available.
3. Classify the requested change.
4. Use DeepResearch for venue, claim, contribution, method, evaluation, related-work, code, dataset, benchmark, artifact, or other intellectual changes.
5. Apply the narrowest useful edit.
6. Update the analysis file, change log, and source ledger.

Preserve unaffected sections unless new evidence changes their meaning.

## Product/API Chain

Product implementations may use this chain:

1. `classify_request`
2. `intake_or_revision_parser`
3. `identify_hard_blueprint_steps`
4. `deepresearch_brief_generator`
5. `call_deepresearch`
6. `deepresearch_report_synthesizer`
7. `blueprint_json_generator`
8. `analysis_json_generator`
9. `markdown_renderer`
10. `source_ledger_updater`

Intermediate artifacts use:

- `schemas/deepresearch_brief.schema.json`
- `schemas/deepresearch_report.schema.json`
- `schemas/paper_blueprint.schema.json`
- `schemas/paper_blueprint_analysis.schema.json`
- `schemas/source_ledger.schema.json`

GPT-5.5-pro is the default high-compute research model when the product needs web search, structured outputs, code interpreter, or MCP. Specialized deep-research models can fill the same role when they preserve the brief/report contracts.

## Final Checks

- Match the blueprint and analysis templates.
- Record all sources that influence blueprint or analysis content.
- Keep DeepResearch recommendations traceable to user input, cited evidence, or explicit assumptions.
- Mark material gaps as `TBD`.
- Validate generated JSON with `scripts/validate_blueprint_json.py`.

## Resource Guide

- `references/deepresearch_protocol.md`: DeepResearch role, brief format, source expectations, and integration boundary.
- `references/deepresearch_question_plans.md`: question-type selection and section mapping.
- `assets/blueprint_template.md`: blueprint structure.
- `assets/analysis_template.md`: analysis structure.
- `assets/deepresearch_brief_template.json`: focused brief starter.
- `assets/source_ledger_template.json`: ledger starter.
- `scripts/call_deepresearch.py`: DeepResearch API wrapper.
- `scripts/validate_blueprint_json.py`: structural checks for blueprint, analysis, ledger, brief, and report JSON.
