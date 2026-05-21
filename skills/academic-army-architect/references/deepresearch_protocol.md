# DeepResearch Protocol

## Role

DeepResearch is the research judgment layer for the paper blueprint workflow. It reads sources, compares related work, synthesizes evidence, and recommends blueprint decisions.

Orchestration handles formatting, validation, rendering, patching, and file assembly.

## Scope

Use DeepResearch for:

- literature interpretation
- related-work positioning
- venue or journal adaptation
- contribution framing
- claim-strength judgment
- evaluation planning
- baseline and metric selection
- code, dataset, benchmark, and artifact discovery
- substantive paper revisions

Mechanical edits stay in orchestration.

## Brief Format

A DeepResearch Brief includes:

- task mode
- conversation language
- user goal
- question type
- user idea summary
- known field and subfield
- target venue or journal
- paper type
- method
- evidence
- data, code, or artifacts
- constraints
- existing blueprint or revision request
- missing information
- blueprint sections under review
- research questions
- source types
- integration instructions
- requested output schema

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

## Core Questions

DeepResearch answers the relevant subset:

1. What existing work is most relevant?
2. Which papers are closest to the user's idea?
3. What gap does the user's idea target?
4. What contribution framing is justified?
5. What claim strength fits the evidence?
6. What evaluation plan fits the field?
7. What code, datasets, benchmarks, or artifacts matter?
8. What venue or journal constraints matter?
9. What blueprint decisions follow?
10. What information remains missing?

## Source Priority

Prioritize:

1. peer-reviewed papers
2. official proceedings pages
3. official venue or journal pages
4. arXiv or preprint pages when appropriate
5. official GitHub repositories
6. dataset or benchmark homepages
7. publisher or lab pages

Use traceable sources for citations, repositories, datasets, benchmarks, artifacts, and venue rules.

## Output

Return a structured report with:

- cited sources and metadata
- relevance notes
- closest-work analysis
- contribution framing advice
- claim strength recommendation
- evaluation recommendations
- blueprint decision recommendations
- material gaps

Every recommendation used in the blueprint is traceable to user input, DeepResearch evidence, or an explicit assumption.

## Integration Boundary

DeepResearch answers research questions. Orchestration assembles files, preserves fixed section order, marks `TBD`, writes change logs, updates `source_ledger.json`, and keeps unaffected sections stable.

## Failure Handling

The API wrapper retries a failed DeepResearch call 3 times. If all attempts fail, research-dependent outputs stay unchanged and the failure is returned for retry. Mechanical edits may proceed when the task does not require DeepResearch.
