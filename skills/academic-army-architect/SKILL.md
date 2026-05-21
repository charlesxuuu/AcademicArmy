---
name: academic-army-architect
description: >-
  Use when Codex needs to create, refine, or revise a standardized academic paper blueprint from a user's existing research idea, partial plan, draft notes, or existing blueprint. This DeepResearch-first skill treats DeepResearch as the primary research judgment layer for literature positioning, contribution boundaries, evaluation design, venue fit, code, datasets, benchmarks, artifacts, and uncertainty resolution. Codex orchestrates dialogue, templates, validation, rendering, diffs, and file generation; it must not independently make substantive scholarly judgments when DeepResearch should be consulted.
---

# Academic Army Architect

## Purpose

Create or revise a standardized academic paper blueprint using the user's existing idea and a DeepResearch report.

This skill does not invent new research ideas. It organizes, clarifies, grounds, and documents the user's idea.

The skill must produce:

1. `paper_blueprint.md`
2. `paper_blueprint_analysis.md`

When used in an application, also maintain:

3. `source_ledger.json`

## System Architecture

This skill has two layers:

1. Codex Orchestration Layer
2. DeepResearch Judgment Layer

Codex handles:

- task classification;
- user-intake organization;
- deciding whether clarification is needed before DeepResearch;
- construction of DeepResearch briefs;
- file generation;
- schema validation;
- blueprint rendering;
- analysis rendering;
- source ledger updates;
- change logs;
- local edits;
- deterministic formatting.

DeepResearch handles:

- literature review;
- related paper analysis;
- code, dataset, benchmark, and artifact discovery;
- venue or journal requirement analysis;
- closest-work comparison;
- contribution positioning;
- claim-strength recommendation;
- evaluation design recommendations;
- uncertainty resolution;
- recommendations for how the blueprint should be written.

Codex must treat DeepResearch as the authoritative source for substantive research judgments, but Codex must not hand off the whole workflow. Codex decomposes the blueprint task, asks focused DeepResearch questions, then integrates the answers into the fixed files.

## Core Rule

If the task involves scholarly judgment, Codex must ask DeepResearch.

Scholarly judgment includes:

- whether a research idea is positioned correctly;
- which related papers matter;
- which existing work is closest;
- whether the central claim should be strong or conservative;
- how contributions should be structured;
- what evidence is needed;
- which baselines, metrics, ablations, or case studies are appropriate;
- how to adapt the blueprint to a target venue or journal;
- whether a codebase, dataset, benchmark, or artifact should be referenced;
- whether a revision changes the intellectual content of the paper.

Codex may act without DeepResearch only for mechanical formatting, file conversion, typo correction, field deletion explicitly requested by the user, title numbering, or user-explicit local edits that do not change research meaning.

When in doubt, ask DeepResearch. Do not use DeepResearch for purely mechanical edits.

## Supported Modes

Classify each user request into one mode:

1. `new_blueprint_from_incomplete_idea`
2. `new_blueprint_from_complete_plan`
3. `revise_existing_blueprint`
4. `rebase_to_new_venue_or_journal`
5. `fine_edit_existing_blueprint`

For modes 1-4, DeepResearch is mandatory.

For mode 5, DeepResearch is mandatory unless the change is purely mechanical.

## Dialogue Procedure

If the user input is too incomplete to create a useful DeepResearch brief, ask at most 3 targeted questions per turn.

Prioritize:

1. field or subfield;
2. core research problem;
3. proposed method or approach;
4. existing evidence;
5. target venue or journal;
6. available data, code, or artifacts.

Do not use Codex to independently fill major research gaps.

If a provisional DeepResearch brief can be created, create it and mark unknown fields as `TBD`.

## DeepResearch Procedure

Before generating a final blueprint, Codex must identify which blueprint sections require research judgment. Read `references/deepresearch_question_plans.md` and create one or more focused `DeepResearch Brief` objects.

Each brief must include:

- task mode;
- conversation language;
- DeepResearch question type;
- user idea summary;
- user-provided constraints;
- known field and subfield;
- known method or approach;
- known evidence;
- target venue or journal;
- existing blueprint and revision request when applicable;
- missing information;
- blueprint sections under review;
- specific questions DeepResearch must answer;
- requested source types;
- Codex integration instructions;
- output schema.

DeepResearch must return a `DeepResearch Report` for the focused question.

The report must include:

1. research summary;
2. user idea interpretation;
3. key related papers;
4. closest existing work;
5. code, dataset, benchmark, or artifact findings;
6. venue or journal implications;
7. gap analysis;
8. contribution framing advice;
9. claim strength recommendation;
10. method and evaluation advice;
11. risks and uncertainties;
12. recommended blueprint decisions;
13. source metadata.

Codex must not use unrecorded sources in the final blueprint or analysis file. Codex must combine multiple DeepResearch reports when several hard blueprint sections require separate analysis.

## Mandatory DeepResearch Triggers

Call DeepResearch whenever any of these apply:

- generating a formal paper blueprint;
- the user idea is incomplete and current literature is needed to help clarify direction;
- related work positioning is needed;
- closest existing work must be identified;
- contribution wording or contribution boundary must be judged;
- central claim strength must be judged;
- experiment, baseline, metric, ablation, user study, or case study design must be judged;
- similar code, datasets, benchmarks, or artifacts may exist;
- target venue or journal requirements matter;
- the user asks to change venue or journal;
- an existing blueprint revision affects claim, method, evaluation, related work, venue, code, dataset, benchmark, or artifact content;
- Codex would otherwise rely on its own general academic knowledge.

Use focused DeepResearch question types rather than one generic request:

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

## Mechanical-Only Exceptions

DeepResearch is not required for:

- typo correction;
- Markdown formatting;
- converting an existing blueprint to JSON;
- renaming files;
- deleting a field the user explicitly asks to delete;
- changing title numbering;
- purely local wording edits that do not change research meaning.

If a formatting request changes intellectual framing, such as "make this contribution sound more like CHI", call DeepResearch.

## DeepResearch Escalation Policy

Escalate to DeepResearch when:

- two or more plausible blueprint framings are possible;
- the correct venue framing is unclear;
- the related-work cluster is unclear;
- it is unclear whether a contribution is novel, too broad, or too weak;
- evaluation choices depend on field norms;
- baseline choices depend on recent literature;
- the user's requested revision may change the intellectual positioning of the paper;
- Codex would otherwise need to rely on its own general knowledge.

## Provenance Rules

Every substantive blueprint decision must be marked internally as one of:

- `user_provided`
- `deepresearch_supported`
- `codex_inferred_from_user_input`
- `TBD`

Do not present `codex_inferred_from_user_input` as established fact.

If a contribution, claim, evaluation design, or related-work statement is not supported by the user input or DeepResearch report, mark it as `TBD` or `needs_user_confirmation`.

## Fixed Blueprint Output

Always output `paper_blueprint.md` with the exact 15-section order in `assets/blueprint_template.md`. Do not add, remove, or rename top-level sections unless the user explicitly requests a custom export format.

The blueprint should be concise and executable. Put detailed reasoning in the analysis file, not in the blueprint.

## Fixed Analysis Output

Always output `paper_blueprint_analysis.md` with the exact 14-section order in `assets/analysis_template.md`.

The analysis file must use the user's conversation language unless the user requests another language.

Required analysis section order:

1. Analysis Summary
2. User-Provided Inputs
3. DeepResearch Brief
4. DeepResearch Process Summary
5. Referenced Papers
6. Referenced Code, Datasets, Benchmarks, or Artifacts
7. Venue / Journal Considerations
8. Why the Research Problem Was Framed This Way
9. Why the Central Claim Was Written This Way
10. Why the Contributions Were Structured This Way
11. Why the Evaluation Plan Was Chosen
12. Assumptions, Uncertainties, and Missing Information
13. How DeepResearch Influenced the Blueprint
14. Change Log

## Source Ledger

Maintain `source_ledger.json` for product state, revision tracking, and future edits. Use `schemas/source_ledger.schema.json` for the expected structure.

This ledger is especially important when the user later says "change the venue", "remove the third contribution", "replace the baseline", or "make the claim more conservative".

## Revision Rules

When revising an existing blueprint:

1. Parse the old blueprint.
2. Parse the old analysis file if available.
3. Parse the old source ledger if available.
4. Classify the requested modification.
5. Decide whether DeepResearch is required.
6. If required, create a revision-specific DeepResearch Brief.
7. Apply only necessary changes.
8. Update the analysis file.
9. Update the change log.
10. Preserve unaffected sections unless the new DeepResearch report requires wider changes.

DeepResearch is mandatory for:

- venue changes;
- journal changes;
- claim changes;
- contribution changes;
- method changes;
- evaluation changes;
- related work updates;
- code, dataset, benchmark, or artifact updates.

## API Workflow Guidance

For a product implementation, prefer this call chain:

1. `classify_request`
2. `intake_or_revision_parser`
3. `identify_hard_blueprint_steps`
4. `deepresearch_brief_generator`
5. `call_deepresearch` with `scripts/call_deepresearch.py` for each focused question
6. `deepresearch_report_synthesizer`
7. `blueprint_json_generator`
8. `analysis_json_generator`
9. `markdown_renderer`
10. `source_ledger_updater`

Use structured outputs for the intermediate JSON so fixed sections do not drift. Use these schemas:

- `schemas/deepresearch_brief.schema.json`
- `schemas/deepresearch_report.schema.json`
- `schemas/paper_blueprint.schema.json`
- `schemas/paper_blueprint_analysis.schema.json`
- `schemas/source_ledger.schema.json`

Use GPT-5.5-pro as the default high-compute research model when the product requires Responses API tools such as web search, structured outputs, code interpreter, and MCP. Do not rely on GPT-5.5-pro natively loading this skill; it does not support Skills as a Responses API tool. Use the skill as the orchestration package and call the OpenAI API from Python.

If using OpenAI's specialized deep-research models instead, treat them as an implementation variant of the same DeepResearch role and preserve the same brief/report contracts.

## Consistency Checks

Before finalizing:

- the blueprint must follow the fixed 15-section structure;
- the analysis must follow the fixed 14-section structure;
- every referenced paper must appear in the analysis file;
- every substantive DeepResearch recommendation used in the blueprint must be traceable;
- every referenced codebase, dataset, benchmark, or artifact must appear in the analysis file or source ledger;
- missing information must be marked as `TBD`;
- Codex must not invent new research ideas;
- the analysis must explain why the blueprint was written this way;
- revision requests must preserve unaffected sections when possible.

## Resource Guide

- Read `references/deepresearch_protocol.md` before constructing or interpreting a DeepResearch Brief.
- Read `references/deepresearch_question_plans.md` to decide which blueprint steps require DeepResearch and which question type to ask.
- Read `assets/blueprint_template.md` before writing `paper_blueprint.md`.
- Read `assets/analysis_template.md` before writing `paper_blueprint_analysis.md`.
- Read `assets/deepresearch_brief_template.json` when creating a focused DeepResearch brief.
- Read `assets/source_ledger_template.json` when creating `source_ledger.json`.
- Use `schemas/deepresearch_brief.schema.json` for DeepResearch brief output.
- Use `schemas/deepresearch_report.schema.json` for DeepResearch report output.
- Use `schemas/paper_blueprint.schema.json` for structured blueprint output.
- Use `schemas/paper_blueprint_analysis.schema.json` for structured analysis output.
- Use `schemas/source_ledger.schema.json` for structured ledger output.
- Use `scripts/call_deepresearch.py` to execute the DeepResearch API layer.
- Run `scripts/validate_blueprint_json.py --kind blueprint <file>`, `--kind analysis <file>`, `--kind ledger <file>`, `--kind deepresearch-brief <file>`, or `--kind deepresearch-report <file>` for quick structural checks.
