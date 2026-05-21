# DeepResearch Protocol

## Role

DeepResearch is the senior research analyst for this skill.

It is not a search tool. It is responsible for reading, comparing, synthesizing, and recommending blueprint decisions.

Codex is the orchestrator, formatter, validator, renderer, and patcher. DeepResearch is the research lead and judgment layer.

Codex must not send every task as one all-purpose DeepResearch request. Codex should identify which blueprint sections are hard, ask focused research questions, and integrate the answers.

## When to Call DeepResearch

Call DeepResearch whenever the task requires any of the following:

- literature interpretation;
- related work positioning;
- venue or journal adaptation;
- contribution framing;
- claim-strength judgment;
- evaluation planning;
- baseline selection;
- metric selection;
- artifact discovery;
- uncertainty resolution;
- revision of substantive paper content.

Do not call DeepResearch for purely mechanical edits.

## DeepResearch Brief Format

A DeepResearch Brief must include:

- task mode;
- conversation language;
- user goal;
- DeepResearch question type;
- user idea summary;
- known field;
- known subfield;
- target venue or journal;
- known paper type;
- known method;
- known evidence;
- known data, code, or artifacts;
- known constraints;
- existing blueprint if any;
- user revision request if any;
- missing information;
- blueprint sections under review;
- questions for DeepResearch;
- required source types;
- Codex integration instructions;
- requested output schema.

Supported question types:

- `general_blueprint_judgment`
- `venue_style_analysis`
- `related_direction_synthesis`
- `closest_work_comparison`
- `contribution_boundary`
- `claim_strength`
- `method_evaluation_design`
- `artifact_landscape`
- `paper_structure_strategy`
- `revision_impact_analysis`

## Required Questions for DeepResearch

DeepResearch must answer:

1. What existing work is most relevant?
2. Which papers are closest to the user's idea?
3. What gap does the user's idea appear to target?
4. What contribution framing is justified?
5. What claim strength is appropriate?
6. What evaluation plan is standard or defensible?
7. What code, datasets, benchmarks, or artifacts are relevant?
8. What venue or journal constraints matter?
9. What should Codex put into the blueprint?
10. What should remain `TBD` or user-confirmed?

## Source Requirements

DeepResearch must prioritize:

1. peer-reviewed papers;
2. official proceedings pages;
3. official venue or journal pages;
4. arXiv or preprint pages when appropriate;
5. official GitHub repositories;
6. dataset or benchmark homepages;
7. publisher or lab pages.

DeepResearch must not fabricate citations, citation counts, papers, repositories, datasets, benchmarks, or venue rules.

## Output Requirements

Return a structured report with:

- cited sources;
- source metadata;
- relevance explanation;
- closest-work analysis;
- contribution framing advice;
- claim strength recommendation;
- evaluation recommendations;
- blueprint decision recommendations;
- uncertainties;
- fields that should remain `TBD`.

Every recommendation that Codex uses in the blueprint must be traceable to user input, DeepResearch evidence, or a clearly marked assumption.

## Integration Boundary

DeepResearch answers research questions. Codex still decides how to assemble files, preserve fixed section order, mark `TBD`, write change logs, update `source_ledger.json`, and avoid changing unaffected sections.
