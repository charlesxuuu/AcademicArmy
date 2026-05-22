# DeepResearch Protocol

## Role

DeepResearch supplies scholarly judgment for paper blueprints. It reads sources, compares related work, synthesizes evidence, and recommends blueprint decisions.

The surrounding workflow handles intake, formatting, validation, rendering, diffs, change logs, and file assembly.

## Scope

Use DeepResearch for:

- literature interpretation
- closest-work comparison
- venue or journal adaptation
- contribution framing
- claim-strength judgment
- method and evaluation planning
- baseline and metric selection
- code, dataset, benchmark, and artifact discovery
- substantive revisions

Handle mechanical edits without DeepResearch.

## Brief Contents

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

## Question Types

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

## Source Priority

Prioritize traceable sources:

1. peer-reviewed papers
2. official proceedings pages
3. official venue or journal pages
4. arXiv or preprint pages when appropriate
5. official repositories
6. dataset or benchmark homepages
7. publisher or lab pages

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

Each recommendation used in the blueprint links back to user input, cited evidence, or an explicit assumption.

## Integration Boundary

DeepResearch answers research questions. The surrounding workflow assembles files, preserves template structure, marks `TBD`, writes change logs, updates `source_ledger.json`, and keeps unaffected sections stable.
