---
name: academic-army-architect
description: >-
  Use when Codex needs to create or revise a search-grounded, standardized academic paper blueprint from a user's existing research idea, notes, partial plan, draft, old blueprint, or venue-change request. This skill runs as a product workflow and prompt/template package that clarifies the user's idea, requires web search for related papers, code, datasets, artifacts, and venue or journal requirements when producing formal outputs, then generates paper_blueprint.md, paper_blueprint_analysis.md, and source_ledger.json. It must not invent research ideas, fabricate sources, fabricate results, or silently add unconfirmed contributions.
---

# Academic Army Architect

## Purpose

Convert the user's existing academic research idea, partial plan, draft notes, or existing blueprint into a search-grounded standard paper blueprint. Treat this skill as a reusable workflow/template/system-prompt package for a product using GPT-5.5-pro, Responses API, web search, structured outputs, and optional code execution. Do not rely on GPT-5.5-pro natively mounting hosted Skills inside the same request; run this package as the product's orchestration layer.

The formal workflow produces:

1. `paper_blueprint.md`
2. `paper_blueprint_analysis.md`
3. `source_ledger.json`

## Core Boundaries

The skill may:

- clarify the user's existing idea through dialogue;
- search for related papers, code, datasets, benchmarks, artifacts, and venue guidelines;
- organize the user's idea into a fixed blueprint structure;
- identify missing information and user decisions needed;
- propose alternative framings only as options or `TBD`;
- explain why each blueprint decision was made.

The skill must not:

- invent a new research idea;
- fabricate experimental results, citations, repositories, datasets, or venue rules;
- claim that a source exists without search support;
- silently add contributions not grounded in user input or searched evidence;
- guarantee acceptance, impact, novelty, citation count, or venue fit;
- merge user-provided content and search-supported content without provenance.

## Supported Modes

Classify each request into exactly one mode:

1. `new_blueprint_from_incomplete_idea`
2. `new_blueprint_from_complete_plan`
3. `revise_existing_blueprint`
4. `rebase_to_new_venue_or_journal`
5. `fine_edit_existing_blueprint`

If the user provides an existing blueprint, preserve unaffected sections whenever possible. Venue changes, central claim changes, method changes, evaluation changes, and related-work changes can require wider revision.

## Dialogue Procedure

If the user does not provide enough information to create a provisional blueprint, ask no more than 3 questions per turn. Prioritize:

1. field or subfield;
2. core research problem;
3. proposed method or approach;
4. existing evidence;
5. target venue or journal;
6. intended contribution;
7. available data, code, or artifacts.

If a provisional blueprint is possible, proceed and mark missing fields as `TBD`. Do not block on perfect intake.

## Mandatory Search Policy

Before producing any formal new blueprint or substantive revision, perform at least one search pass. Use Responses API web search with required tool choice in product implementations when search must occur. Use domain filtering as a starting point, not a fixed rule; choose domains by discipline.

Search is optional only for:

- `format_only` changes;
- narrow wording changes that do not affect claims, contributions, method, evidence, venue fit, related work, code, datasets, or artifacts.

Search is mandatory when a request affects:

- venue or journal;
- research claim;
- contribution;
- method;
- evaluation;
- related work;
- code, dataset, benchmark, or artifact references.

## Search Tiers

Use only the tiers needed for the current mode, but formal outputs must include at least one executed search pass.

- `S0: Clarification Search`: Use for vague ideas to understand terminology, task definitions, and common problem framing. Use results to ask better questions; do not directly turn them into user-owned claims.
- `S1: Related Paper Search`: Find recent papers, influential papers, surveys, benchmark papers, and closest competing work.
- `S2: Code / Artifact Search`: Find code repositories, tools, systems, benchmark implementations, dataset repositories, and reproducibility artifacts.
- `S3: Venue / Journal Search`: Find official author guides, review criteria, submission checklists, and recent accepted papers. Required when the user gives or changes a target venue or journal.
- `S4: Gap and Positioning Search`: Determine how the idea should be positioned against related work. Use it to write differentiation and caution against overclaiming, not to invent the user's contribution.

## Search Result Handling

Classify every source as one of:

- `paper`
- `code`
- `dataset`
- `benchmark`
- `venue_guideline`
- `documentation`
- `other_artifact`

For each source, record source ID, title or name, authors or owner, year or date if available, venue or platform if available, URL or DOI, citation signal if available, reason for inclusion, blueprint sections influenced, confidence level, and limitations or caveats.

Do not use a source in the blueprint unless it appears in `paper_blueprint_analysis.md` or `source_ledger.json`.

## Provenance Rules

Track the origin of substantive fields with one of:

- `user_provided`
- `web_supported`
- `model_inferred`
- `TBD`

Use this rule:

```text
Blueprint fields may organize and clarify the user's idea.
Search may provide positioning, references, baselines, artifacts, and venue constraints.
New core contributions, experimental results, and research conclusions must come from user confirmation or be explicitly marked as suggestions / TBD.
```

## Fixed Blueprint Output

Always output `paper_blueprint.md` with the exact 15-section order in `assets/blueprint_template.md`. Do not add, remove, or rename top-level sections unless the user explicitly requests a custom export format.

The blueprint should be concise and executable. Put detailed reasoning in the analysis file, not in the blueprint.

## Fixed Analysis Output

Always output `paper_blueprint_analysis.md` with the exact 12-section order in `assets/analysis_template.md`.

The analysis file explains why the blueprint was written that way, what sources were used, what changed, and what remains uncertain. Use the language used in the user conversation unless the user requests another language.

## Source Ledger

Maintain `source_ledger.json` for product state, revision tracking, and future edits. Use `references/source_ledger_schema.json` for the expected structure. This ledger is especially important when the user later says "change the venue", "remove the third contribution", "replace the baseline", or "make the claim more conservative".

## Revision Workflow

For existing-blueprint tasks:

1. Parse existing `paper_blueprint.md`.
2. Parse existing `paper_blueprint_analysis.md` and `source_ledger.json` when available.
3. Classify the modification request.
4. Decide whether new search is required.
5. Create a revision plan.
6. Apply localized or global changes.
7. Update the analysis file.
8. Update the source ledger.

Classify revision requests as:

- `local_text_edit`
- `claim_revision`
- `contribution_revision`
- `method_revision`
- `evaluation_revision`
- `venue_rebase`
- `related_work_update`
- `artifact_update`
- `format_only`

Search rules for revisions:

- `format_only`: no search required.
- `local_text_edit`: usually no search required.
- `claim_revision`: search required unless only making wording more conservative.
- `contribution_revision`: usually search required.
- `method_revision`: search required.
- `evaluation_revision`: search required.
- `venue_rebase`: search required.
- `related_work_update`: search required.
- `artifact_update`: search required.

## API Workflow Guidance

For a product implementation, prefer this call chain:

1. `classify_request`
2. `intake_or_revision_parser`
3. `search_plan_generator`
4. `web_search_research`
5. `blueprint_json_generator`
6. `analysis_json_generator`
7. `markdown_renderer`

Use structured outputs for the intermediate JSON so fixed sections do not drift. Use `references/blueprint_schema.json`, `references/analysis_schema.json`, and `references/source_ledger_schema.json` as schemas or schema design references.

For `web_search_research`, use GPT-5.5-pro with web search and required tool choice when search is mandatory. Include domain filters only after choosing discipline-appropriate sources:

- CS / AI: arxiv.org, openreview.net, aclanthology.org, dl.acm.org, ieeexplore.ieee.org, github.com, paperswithcode.com, semanticscholar.org.
- Medicine / life sciences: pubmed.ncbi.nlm.nih.gov, nature.com, science.org, cell.com, nejm.org, thelancet.com.
- Social science / humanities: publisher pages, SSRN, venue pages, DOI pages, and field-specific archives where appropriate.

## Consistency Checks

Before finalizing, verify:

- every substantive contribution is grounded in user input or searched evidence;
- every referenced paper or artifact appears in the analysis file or source ledger;
- missing information is marked as `TBD`;
- the blueprint uses the fixed 15-section structure;
- the analysis uses the fixed 12-section structure;
- revision requests preserve unaffected sections when possible;
- search-supported claims have clear, clickable source references in user-facing output when web results are shown.

## Resource Guide

- Read `assets/blueprint_template.md` before writing `paper_blueprint.md`.
- Read `assets/analysis_template.md` before writing `paper_blueprint_analysis.md`.
- Read `assets/source_ledger_template.json` when creating `source_ledger.json`.
- Use `references/blueprint_schema.json` for structured blueprint output.
- Use `references/analysis_schema.json` for structured analysis output.
- Use `references/source_ledger_schema.json` for structured ledger output.
- Run `scripts/validate_blueprint_json.py --kind blueprint <file>`, `--kind analysis <file>`, or `--kind ledger <file>` for quick structural checks.
