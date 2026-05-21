---
name: academic-army-architect
description: >-
  This skill creates, refines, or revises a standardized academic paper blueprint from a user's research idea, partial plan, draft notes, or existing blueprint. It produces paper_blueprint.md, paper_blueprint_analysis.md, and, for product state, source_ledger.json. It uses DeepResearch for literature, venue, contribution, claim-strength, evaluation, code, dataset, benchmark, artifact, and uncertainty judgments; the orchestration layer handles intake, focused briefs, integration, templates, validation, rendering, diffs, and file generation.
---

# Academic Army Architect

## Purpose

This skill turns a user's existing research idea into a standardized paper blueprint grounded by DeepResearch.

Primary outputs:

1. `paper_blueprint.md`
2. `paper_blueprint_analysis.md`
3. `source_ledger.json` when maintaining product state or revision history

The skill organizes and grounds the user's idea. It does not invent a new research project.

## Operating Model

The workflow has two layers:

- **Orchestration layer**: intake, task classification, clarification questions, DeepResearch briefs, file generation, template rendering, schema validation, diffs, source ledger updates, and local edits.
- **DeepResearch**: literature synthesis, closest-work comparison, venue fit, contribution boundaries, claim strength, method/evaluation design, artifact discovery, and uncertainty resolution.

Default routing:

- DeepResearch handles scholarly judgment.
- The orchestration layer handles mechanical edits directly.

Mechanical edits include typo fixes, Markdown formatting, file renaming, title numbering, JSON conversion, field deletion explicitly requested by the user, and wording edits that do not change research meaning.

## Request Modes

Each request is classified as:

1. `new_blueprint_from_incomplete_idea`
2. `new_blueprint_from_complete_plan`
3. `revise_existing_blueprint`
4. `rebase_to_new_venue_or_journal`
5. `fine_edit_existing_blueprint`

Modes 1-4 use DeepResearch. Mode 5 uses DeepResearch only when the edit changes scholarly meaning.

## Intake

If the user's input is too thin to create a useful DeepResearch brief, the workflow asks up to 3 targeted questions. Priority order:

1. field or subfield
2. core research problem
3. proposed method
4. existing evidence
5. target venue or journal
6. available data, code, or artifacts

If a brief can be created, unknown fields are marked as `TBD`.

## DeepResearch Use

Substantive blueprint content follows this process:

1. Identify the blueprint sections that require research judgment.
2. Read `references/deepresearch_protocol.md`.
3. Read `references/deepresearch_question_plans.md`.
4. Create one or more focused `DeepResearch Brief` objects.
5. Call DeepResearch with `scripts/call_deepresearch.py` or the product's equivalent API layer.
6. Integrate the returned `DeepResearch Report` into the blueprint, analysis file, and source ledger.

## DeepResearch Gate

DeepResearch is a hard gate for every step that requires scholarly judgment. There is no fallback path where the orchestration layer substitutes its own scholarly judgment after DeepResearch fails.

`scripts/call_deepresearch.py` retries a failed DeepResearch call up to 3 attempts by default. If all attempts fail, the workflow stops immediately:

- do not generate `paper_blueprint.md`;
- do not generate `paper_blueprint_analysis.md`;
- do not update `source_ledger.json` as though research succeeded;
- report the DeepResearch failure to the user or product layer;
- wait for the API, credential, model, schema, or network issue to be fixed before continuing.

Only mechanical edits that did not require DeepResearch may proceed without a DeepResearch report.

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

Separate focused questions are used when one broad request would mix unrelated judgments.

## Provenance

Each substantive blueprint decision is tracked internally as:

- `user_provided`
- `deepresearch_supported`
- `workflow_inferred_from_user_input`
- `TBD`

`workflow_inferred_from_user_input` is reserved for lightweight inferences from the user's own facts. Unsupported claims, evaluation designs, contribution wording, and related-work statements are marked as `TBD` or `needs_user_confirmation`.

Every source used in the blueprint or analysis is recorded. Unrecorded papers, codebases, datasets, benchmarks, artifacts, and venue rules are excluded.

## Outputs

`paper_blueprint.md` is rendered from `assets/blueprint_template.md`; its 15 top-level sections are preserved unless the user requests a custom export.

`paper_blueprint_analysis.md` is rendered from `assets/analysis_template.md`; its 14 top-level sections are preserved. The analysis uses the user's conversation language unless they request another language. Keep `Referenced Papers` as the final section so long paper metadata does not pull later rationale sections away from the conversation language.

The blueprint stays concise and executable. Rationale, source influence, assumptions, and change history belong in the analysis file.

`source_ledger.json` maintains product state, revision history, and future edit context. It is validated with `schemas/source_ledger.schema.json`.

## Revision Workflow

Existing blueprint revisions follow this sequence:

1. Parse the existing blueprint.
2. Parse the analysis file and source ledger when available.
3. Classify the requested change.
4. Use DeepResearch for venue, claim, contribution, method, evaluation, related-work, code, dataset, benchmark, artifact, or other intellectual changes.
5. Apply the narrowest useful edit.
6. Update the analysis file, change log, and source ledger.

Unaffected sections are preserved unless new evidence changes their meaning.

## Product/API Workflow

Product implementations use this chain:

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

Intermediate artifacts use structured JSON:

- `schemas/deepresearch_brief.schema.json`
- `schemas/deepresearch_report.schema.json`
- `schemas/paper_blueprint.schema.json`
- `schemas/paper_blueprint_analysis.schema.json`
- `schemas/source_ledger.schema.json`

GPT-5.5-pro is the default high-compute research model when the product requires Responses API tools such as web search, structured outputs, code interpreter, and MCP. Specialized deep-research models can fill the same DeepResearch role if they preserve the brief/report contracts.

## Final Checks

Finalization checks:

- Match the blueprint and analysis templates.
- Ensure every referenced paper, codebase, dataset, benchmark, artifact, and venue rule is recorded.
- Keep DeepResearch recommendations traceable to user input, cited evidence, or explicit assumptions.
- Mark missing information as `TBD`.
- Validate generated JSON with `scripts/validate_blueprint_json.py`.
- Treat a nonzero exit from `scripts/call_deepresearch.py` as a blocking failure. Do not proceed to rendering, ledger update, or blueprint generation after that failure.

## Resource Guide

- `references/deepresearch_protocol.md`: DeepResearch role, brief format, source expectations, and integration boundary.
- `references/deepresearch_question_plans.md`: question-type selection and section mapping.
- `assets/blueprint_template.md`: required blueprint structure.
- `assets/analysis_template.md`: required analysis structure.
- `assets/deepresearch_brief_template.json`: focused brief starter.
- `assets/source_ledger_template.json`: ledger starter.
- `scripts/call_deepresearch.py`: DeepResearch API wrapper.
- `scripts/validate_blueprint_json.py`: structural checks for blueprint, analysis, ledger, brief, and report JSON.
