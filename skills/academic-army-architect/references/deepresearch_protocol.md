# DeepResearch Protocol

## Role

DeepResearch is the senior research analyst for this skill. It reads, compares, synthesizes, and recommends blueprint decisions.

The orchestration layer handles formatting, validation, rendering, patching, and file assembly. DeepResearch is the research lead and judgment layer.

The workflow identifies hard blueprint sections first, then addresses them through focused research questions.

## DeepResearch Scope

Use DeepResearch for:

- literature interpretation;
- related work positioning;
- venue or journal adaptation;
- contribution framing;
- claim-strength judgment;
- evaluation planning;
- baseline selection;
- metric selection;
- artifact discovery;
- uncertainty handling;
- revision of substantive paper content.

Mechanical edits stay in the orchestration layer.

## DeepResearch Brief Format

A DeepResearch Brief includes:

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
- integration instructions;
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

## Core Questions

DeepResearch answers:

1. What existing work is most relevant?
2. Which papers are closest to the user's idea?
3. What gap does the user's idea appear to target?
4. What contribution framing is justified?
5. What claim strength is appropriate?
6. What evaluation plan fits the field?
7. What code, datasets, benchmarks, or artifacts are relevant?
8. What venue or journal constraints matter?
9. What blueprint decisions follow from the evidence?
10. Which items remain `TBD` or user-confirmed?

## Source Priority

Prioritize:

1. peer-reviewed papers;
2. official proceedings pages;
3. official venue or journal pages;
4. arXiv or preprint pages when appropriate;
5. official GitHub repositories;
6. dataset or benchmark homepages;
7. publisher or lab pages.

Use traceable sources for citations, papers, repositories, datasets, benchmarks, and venue rules.

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

Every recommendation used in the blueprint is traceable to user input, DeepResearch evidence, or a clearly marked assumption.

## Integration Boundary

DeepResearch answers research questions. The orchestration layer assembles files, preserves fixed section order, marks `TBD`, writes change logs, updates `source_ledger.json`, and keeps unaffected sections stable.
