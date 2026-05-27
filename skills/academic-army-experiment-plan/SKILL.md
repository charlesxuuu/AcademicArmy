---
name: academic-army-experiment-plan
description: >-
  Create a concise strategic academic experiment plan from a research idea,
  paper_blueprint.md, paper claims, storytelling blueprint, target venue,
  existing notes/results, or revision feedback. Produces an English,
  AI-facing experiment_plan.md organized around claim-to-evidence objectives
  and a user-language experiment_plan_explanation.LANG.md that explains the
  causal reasoning behind the plan. Uses academic_army_mcp_tools.deepresearch
  for current venue, baseline, dataset, metric, benchmark, artifact,
  motivation-pattern, and reviewer-expectation research when those facts affect
  the plan.
---

# Academic Army Experiment Plan

## Purpose

Create a strategic experiment plan that lets downstream AI skills decide how to
run, implement, plot, and write experiments without overfitting to premature
execution details.

The main plan is not a runbook. It states what evidence the paper needs, why
that evidence exists, what claims it supports, which current protocols shape the
choice, and how objectives depend on each other.

## Required Outputs

Create exactly two required Markdown files:

1. `experiment_plan.md`
   - English.
   - AI-facing.
   - Contains only the strategic experiment specification.
   - Uses compact, stable fields for downstream skills.

2. `experiment_plan_explanation.<lang>.md`
   - Uses the user's conversation language.
   - Human-facing confirmation companion.
   - Explains how the plan follows from user inputs, the paper blueprint,
     existing evidence, live research, and the paper's core thesis.

Create an optional `experiment_plan_execution_contract.md` only when the user
explicitly asks for execution contracts or when an existing workflow artifact
already requires one. Put metric implementation handles, logging schemas,
output file paths, manifest fields, owners, and concrete artifact paths there,
not in `experiment_plan.md`.

## Research Tool

Use `academic_army_mcp_tools.deepresearch` when venue-, field-, or date-sensitive
facts affect the plan.

- Server: `academic_army_mcp_tools`
- Tool: `deepresearch`
- Canonical Codex MCP name when exposed:
  `mcp__academic_army_mcp_tools__deepresearch`

Use live research for:

- recent target-venue and adjacent-venue experiment patterns
- current baselines, datasets, traces, metrics, benchmarks, and protocols
- reviewer expectations for artifacts, scale, user/perceptual evidence,
  deployment realism, and reproducibility
- motivation or design-insight experiment patterns that make a core intuition
  visible before full-system evaluation

The plan should contain only the resulting planning commitments and stable IDs.
Put source summaries, provenance, and confidence in the explanation file.

## Source Confidence Rule

For every live-research anchor that shapes the plan, record this in the
explanation file:

- `source`: title and link
- `date`: publication date, submission date, or metadata date visible in the
  source
- `venue_status`: one of `verified`, `arxiv_only`, or `source_claim`
- `why_it_affects_this_plan`: the planning decision it changes

Use `verified` only when the venue is confirmed by source metadata from the
venue, publisher, proceedings, author PDF, or institutional publication page.
Use `arxiv_only` when only arXiv metadata is visible. Use `source_claim` when a
venue label appears in a non-primary source or page text but is not confirmed by
the source metadata. Do not promote an arXiv-only paper to a venue-labeled
anchor inside the plan.

## Inputs to Extract

Read `paper_blueprint.md` first when present. Extract:

- top-level paper goal
- central research bet
- main claims and novelty boundary
- strategic evidence posture
- storytelling and communication posture
- motivation points and method insights
- experiment-planning interface, if present

Also extract or infer:

- target venue, track, and submission context
- field and subfield
- target system, method, dataset, benchmark, or theoretical object
- available resources: code, data, models, compute, hardware, traces,
  deployment access, annotation access, or user-study access
- known constraints: compute, time, privacy, inaccessible data, required public
  benchmarks, mandatory baselines, unavailable baselines
- existing notes, drafts, preliminary results, prior plans, prior explanation
  files, or revision feedback
- user conversation language and output directory

## Confirmation-State Model

Before writing, build or update a confirmation ledger in the explanation file.
Classify candidate planning items as:

- `resolved_by_user_instruction`
- `resolved_by_paper_blueprint`
- `resolved_by_existing_evidence`
- `resolved_by_live_research`
- `downstream_execution_detail`
- `remaining_open_planning_item`
- `non_controlling_ambiguity`

A fact resolved by the user, blueprint, existing evidence, or live research
becomes a planning commitment. A downstream execution detail is omitted from the
main plan unless it changes the strategic objective. A remaining open planning
item appears only in the explanation file and only when it affects objective
design, story placement, required resources, or claim coverage.

As revisions add confirmed facts, retire matching open items rather than
restating them.

## Strategic Plan Boundary

`experiment_plan.md` should include:

- experimental thesis, primary comparison, and operating conditions
- claim-to-evidence map
- shared evidence context
- metric registry
- baseline registry
- objective definitions
- objective dependency graph

`experiment_plan.md` should not include:

- source prose or literature-review notes
- confirmed-input ledger
- user-review guidance
- implementation owners
- concrete output file paths
- logging schemas
- manifest fields
- detailed metric implementation contracts
- repeated metric or baseline lists inside every objective

Represent execution-level detail with logical handles. Let downstream skills
choose concrete filenames, logs, schemas, owners, and implementation layouts.

## Positive Evidence Language

Write the plan as a positive evidence specification. The purpose is to make the
paper's intuition, mechanism, and claims visible and credible.

Prefer fields such as:

- `Evidence scope`
- `Evidence role`
- `Handled by later skills`
- `Claim calibration output`
- `Expected evidence outputs`
- `Target evidence pattern`

Avoid defensive or user-facing planning language in `experiment_plan.md`.
Replace negative boundary structures with evidential roles:

```markdown
- Evidence scope:
  - Measures per-state marginal utility under controlled candidate states.
- Evidence role:
  - Establishes when references are useful online state.
- Handled by later skills:
  - Concrete logging schema.
  - Exact figure filenames.
```

Use this evidence-role field pair instead of a negative boundary field in the
main plan.

## Goal-Oriented Objective Design

Start every objective from a paper claim, not from a generic evaluation
checklist.

For each candidate objective, decide:

- Which claim does it support?
- What story role does it serve?
- What evidence output should downstream plotting or writing produce?
- What target evidence pattern should the output make visible?
- What claim-calibration signals should it export?
- Which registry metrics, registry baselines, workloads, controlled factors,
  and comparators are necessary?
- Which details are strategic, and which belong to later execution skills?

Valid story roles include:

- motivation/problem definition
- method design insight
- main end-to-end effectiveness
- mechanism/ablation
- robustness/stress
- generalization
- human/perceptual evidence
- deployment realism
- cost/scalability/reproducibility protocol

Merge objectives that do not support an independent claim, story role, or
primary evidence output. Represent secondary needs as reporting views, metric
slices, or shared protocol entries.

## Motivation and Design-Insight Experiments

A motivation or design-insight objective makes a core intuition, current-system
defect, or method mechanism directly observable before full-system evaluation.

Use two main forms:

- `Existing-system defect demonstration`: show a structural weakness in current
  systems, metrics, schedulers, pipelines, or protocols.
- `Core-mechanism feasibility demonstration`: show that the proposed mechanism
  captures the important structure in a minimal faithful setting.

Place these objectives in the Introduction, Motivation, Method opening, or
Method design justification. Their expected evidence output should be readable
at a glance: figure, compact table, case study, trace timeline, qualitative
grid, heatmap, breakdown, curve separation, before/after panel, or diagnostic
example.

## Registry Rules

Define shared registries once, then reference IDs in objectives.

### Metric Registry

Use compact metric entries:

```markdown
- `metric_id`: <what it measures; unit/range if strategically important;
  aggregation policy if it changes interpretation>
```

Group metrics by role:

- quality/perceptual quality
- latency/deadline/responsiveness
- resource/cost
- waste/inefficiency
- control/action behavior
- statistical reporting
- user/perceptual study signal, when relevant

Objectives reference metrics as:

```markdown
- Metrics: [`qoe_score`, `deadline_miss_ratio`, `bandwidth_cost`]
```

Do not repeat metric definitions inside objectives.

### Baseline Registry

Use compact baseline entries:

```markdown
- `baseline_id`:
  - Role: required | diagnostic | oracle
  - Comparison purpose:
  - Fairness principle:
  - Used by objectives:
```

Keep observation access, action space, resource budget, and implementation owner
out of the main plan unless they change the strategic comparison. Put those
details in the optional execution contract when needed.

Objectives reference comparators as:

```markdown
- Comparators: [`required_networking_baselines`, `reference_diagnostics`,
  `oracle_bounds`]
```

### Workload Context

Define:

- `Required workloads`: workloads committed by user input, blueprint, existing
  evidence, or live-research-selected venue protocol.
- `Scope-extension workload candidates`: workloads that would extend claim
  scope and whose provenance is explained in the explanation file.

Do not use fallback phrases such as `when available` for workloads. If a
workload is not strategically required, place it under scope-extension
candidates or leave it out.

## Objective Redundancy Check

Before finalizing, merge or demote objectives that share more than half of their
controlled factors, workloads, metrics, comparators, or expected evidence
outputs.

Common reductions:

- Reference usefulness and substitution feasibility often become one objective
  with two evidence outputs.
- End-to-end QoE and deadline reliability often become one main objective with
  quality and responsiveness reporting views.
- Resource efficiency, waste, artifact readiness, and reproducibility usually
  become shared protocols or reporting views unless they support a distinct
  paper claim.

Keep objectives separate only when they have distinct claim support, story role,
and primary evidence output.

## Live Research Prompt Shape

Use the smallest set of deepresearch passes needed. A useful prompt shape:

```text
You are supporting a confirmation-state-aware academic experiment planner.

Research brief:
[RESEARCH_BRIEF]

Target venue and field:
[TARGET_VENUE_AND_FIELD]

Confirmed planning facts:
[CONFIRMED_FACTS]

Return:

1. Current venue and field protocols
   Separate must-use protocols, optional confidence-building protocols, older
   canonical baselines still expected by reviewers, stale protocols, and
   implementation availability useful to later execution skills.

2. Recent paper evidence patterns
   For recent strong papers, extract claim-to-evidence patterns, datasets,
   traces, benchmarks, baselines, metrics, ablations, stress tests, scale tests,
   qualitative/user/deployment evidence, artifact signals, and result
   presentation patterns.

3. Motivation and design-insight patterns
   Extract the intuition or failure mode, minimal setting, one-glance artifact,
   story placement, and connection to final evaluation.

4. Planning commitments for this paper
   Explain which objectives, story placements, baseline/dataset/metric choices,
   and evidence outputs should be used.

For each source, include title, link, date, visible venue metadata, provenance
quality, relevance, and the lesson for experiment planning. Distinguish
verified venue metadata, arXiv-only metadata, and source claims.
```

## Workflow

### Step 1: Build the Explanation Ledger

Start `experiment_plan_explanation.<lang>.md` with a concise ledger:

```markdown
## Confirmed User Inputs

## Blueprint-Confirmed Inputs

## Existing Evidence Inputs

## Live-Research Context Used

## Skill-Derived Planning Commitments

## Remaining Open Planning Items
```

Use `Remaining Open Planning Items` only for strategic gaps. If none remain,
state in the user's language that no remaining open item changes the current
plan structure.

Do not include closed-item administration unless the user specifically asks for
revision bookkeeping.

### Step 2: Normalize the Thesis

In `experiment_plan.md`, write:

- `Experimental thesis`: the central mechanism and claim.
- `Primary comparison`: comparator families.
- `Operating conditions`: workload, environment, and variability conditions.

Keep this section concise.

### Step 3: Build the Claim-to-Evidence Map

Map each major claim to:

- evidence objective
- story role
- expected evidence output
- downstream consumers

Use these downstream consumer IDs unless the local toolchain provides a more
specific skill ID:

- `experiment_runner`
- `code_generation`
- `result_analysis`
- `plot_planning`
- `paper_writing`
- `reproducibility`

Use `rebuttal_preparation` only when the user asks for response/rebuttal
planning or when the paper is already in a review-response stage.

### Step 4: Build Shared Evidence Context

Factor out repeated details into:

- workloads
- research context IDs
- metric registry
- baseline registry
- resource and cost reporting principles
- reproducibility/artifact principles

Keep these strategic. Avoid concrete paths, logs, schemas, and owner fields.

### Step 5: Design Objectives

For each objective, use this compact schema:

```markdown
### Objective <n>: <Name>

- Story role:
- Evidence goal:
- Claims supported:
- Evidence scope:
- Evidence role:
- Claim calibration output:
- Workloads:
- Controlled factors:
- Comparators:
- Metrics:
- Expected evidence outputs:
- Target evidence pattern:
- Handled by later skills:
- Dependencies:
- Priority:
```

Use IDs from registries for metrics and comparators. Use logical evidence output
names, not file paths. Keep `Handled by later skills` short and concrete, such
as `figure filenames`, `logging schema`, or `statistical test implementation`.

### Step 6: Write the Explanation Causally

The explanation should make the derivation inspectable without becoming a
workflow-management memo.

Explain:

- which confirmed facts anchor the plan
- how the core thesis decomposes into evidence needs
- why each objective exists
- why its story role fits the paper
- why its evidence output and target evidence pattern fit the claim
- how objectives depend on or calibrate each other
- which source anchors changed the plan, with confidence/provenance

Avoid:

- generic user audit checklists
- closed planning item lists unless requested
- dense cross-reference codes such as `C1/B2/E3`
- long literature-review prose
- advice about how the user should review the file

## `experiment_plan.md` Template

```markdown
# Experiment Plan: <Paper/System Name>

## 1. Experimental Thesis

- Experimental thesis:
- Primary comparison:
- Operating conditions:

## 2. Claim-to-Evidence Map

| Claim | Evidence Objective | Story Role | Expected Evidence Output | Downstream Consumers |
|---|---|---|---|---|

## 3. Shared Evidence Context

### Workloads

- Required workloads:
- Scope-extension workload candidates:

### Research Context IDs

- Baseline IDs:
- Workload IDs:
- Metric IDs:

### Metric Registry

- `<metric_id>`:

### Baseline Registry

- `<baseline_id>`:
  - Role:
  - Comparison purpose:
  - Fairness principle:
  - Used by objectives:

### Resource, Cost, and Reproducibility Principles

- Resource/cost reporting:
- Reproducibility/artifact principle:

## 4. Experiment Objectives

### Objective 1: <Name>

- Story role:
- Evidence goal:
- Claims supported:
- Evidence scope:
- Evidence role:
- Claim calibration output:
- Workloads:
- Controlled factors:
- Comparators:
- Metrics:
- Expected evidence outputs:
- Target evidence pattern:
- Handled by later skills:
- Dependencies:
- Priority:

## 5. Objective Dependency Graph

- <objective/output> -> <objective/output>:
```

Omit empty optional fields. Keep the dependency graph short.

## `experiment_plan_explanation.<lang>.md` Template

Translate headings naturally when appropriate:

```markdown
# Experiment Plan Explanation: <Paper/System Name>

## Confirmed User Inputs

## Blueprint-Confirmed Inputs

## Existing Evidence Inputs

## Live-Research Context Used

## Skill-Derived Planning Commitments

## Remaining Open Planning Items

## Current Field and Target-Venue Experiment Patterns

## Core Experimental Logic

## Derivation of Each Objective

### <Objective name>

## Evidence Chain Across Objectives
```

For each objective, write readable prose rather than numbered cross-reference
logic. Explain the causal chain from thesis to claim, from claim to evidence
need, and from evidence need to objective design.

## Lint Rules

Before finalizing, check:

- `experiment_plan.md` is English-only and contains only the strategic plan.
- The plan does not contain the confirmation ledger, source explanations,
  literature-review prose, user-review checklists, logging schemas, manifest
  fields, implementation owners, or concrete output paths.
- The plan defines metric and baseline registries once and references IDs in
  objectives.
- Objective-level metric and comparator fields do not repeat registry
  definitions.
- Objectives use `Evidence scope`, `Evidence role`, and `Handled by later
  skills`.
- `Expected evidence outputs` uses logical artifact names, not filenames.
- Open planning items appear only in the explanation file.
- A fact resolved by user input, blueprint, existing evidence, or live research
  is not restated as an open question.
- Every live-research anchor in the explanation has source, date,
  `venue_status`, and why it affects the plan.
- Venue labels are not upgraded beyond the source confidence available.
- The explanation is causal and readable, not an administrative checklist.
- The explanation uses the user's language and begins with the confirmation
  ledger.
- Each objective has a distinct claim, story role, or primary evidence output.
- Overlapping objectives are merged or represented as reporting views.
- Downstream consumers use the fixed vocabulary unless a more specific local
  skill ID is known.
