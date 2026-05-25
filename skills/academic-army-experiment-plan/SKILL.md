---
name: academic-army-experiment-plan
description: >-
  Create two Markdown files for a confirmation-state-aware, positive-evidence academic experiment strategy: an English experiment_plan.md for downstream AI experiment, coding, plotting, writing, and review skills, plus a user-language language-suffixed experiment_plan_explanation Markdown file for human confirmation. Use when a research idea, paper_blueprint.md, paper goals, claims, storytelling blueprint, target venue, existing notes/results, or revision feedback must be converted into confirmed planning facts, experiment objectives, story placement, evidence roles, motivation one-glance artifacts, current baselines/datasets/metrics, and downstream execution interfaces. Uses academic_army_mcp_tools.deepresearch, canonical Codex MCP tool name mcp__academic_army_mcp_tools__deepresearch, for live recent-paper, target-venue, baseline, dataset, metric, benchmark, artifact, motivation-pattern, and reviewer-expectation research.
---

# Academic Army Experiment Plan

## Output Contract

Create exactly two Markdown deliverables.

### File 1: `experiment_plan.md`

Write this file in English. Make it an AI-facing strategic experiment plan for later coding, experiment-running, plotting, paper-writing, and review-feedback skills.

The plan is a positive evidence specification. It organizes experiments around paper claims, confirmed planning facts, evidence roles, story placement, planning state, one-glance evidence artifacts, and downstream execution interfaces.

Include:

- paper-level experimental thesis
- evidence strategy for the paper story
- claim-to-evidence map
- objective groups
- planning state and source for each objective
- motivation/design-insight fields when the objective makes an intuition visible
- venue-current dataset, benchmark, trace, workload, baseline, metric, and protocol choices when live evidence supports them
- controls, variables, and stress conditions
- expected tables, figures, qualitative artifacts, logs, and result files
- downstream execution interface
- priority, dependencies, and downstream feedback slots

### File 2: `experiment_plan_explanation.<lang>.md`

Write this file in the user's conversation language. Make it a human confirmation companion that explains how the plan follows from confirmed facts, the paper blueprint, live venue research, and the paper story.

Start with a confirmation ledger. As the user adds instructions across revisions, confirmed facts should grow and remaining open planning items should shrink. Open items appear only in this explanation ledger, and only when the missing input would change the experiment objective, required resource, story placement, or claim coverage.

## Required Research MCP

Use the `deepresearch` tool from the `academic_army_mcp_tools` MCP server for live research.

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical Codex MCP tool name, when exposed: `mcp__academic_army_mcp_tools__deepresearch`

Use `academic_army_mcp_tools.deepresearch` for venue- and field-sensitive facts:

- recent strong target-venue or adjacent-venue papers
- current baselines, datasets, benchmarks, traces, workloads, metrics, and evaluation protocols
- current reviewer expectations around artifacts, user studies, production traces, scale tests, perceptual studies, deployment evidence, or reproducibility
- motivation and design-insight experiment patterns that make an intuition visible before full method evaluation

Use live research to decide how confirmed paper commitments should be evidenced for the target community.

## Inputs to Extract

Extract or infer:

- target venue, track, and likely submission context
- research field and subfield
- research idea, method, system, dataset, benchmark, or theoretical object under evaluation
- upstream `paper_blueprint.md` or equivalent blueprint content
- paper-level goals, claims, novelty boundary, evidence posture, and storytelling blueprint
- available resources: code, data, models, compute, hardware, testbed, traces, simulator, deployment access, annotation resources, user-study access
- known constraints: time, compute, inaccessible data, required public benchmarks, privacy limits, mandatory baselines, unavailable baselines
- existing experiment notes, drafts, preliminary results, prior explanation files, or revision feedback
- user conversation language and output directory

When an upstream `paper_blueprint.md` exists, read it first and extract:

- top-level paper goal
- central research bet
- contribution and novelty-boundary goals
- strategic claim posture
- strategic evidence posture
- scope-control goal
- storytelling and communication posture
- experiment-planning interface
- confirmed motivation points and method insights

## Confirmation-State Model

Before writing the deliverables, build or update a confirmation ledger from:

- explicit user instructions
- paper blueprint facts
- existing experiment notes, drafts, or prior results
- previous `experiment_plan_explanation.<lang>.md`, if present
- live deepresearch findings for current venue and field facts

Classify every candidate planning item as:

- `resolved_by_user_instruction`
- `resolved_by_paper_blueprint`
- `resolved_by_existing_evidence`
- `resolved_by_live_research`
- `downstream_execution_detail`
- `remaining_open_planning_item`
- `non_controlling_ambiguity`

A user-specified, blueprint-confirmed, existing-evidence, or live-research-selected item becomes a planning commitment. A downstream execution detail becomes part of `Downstream Execution Interface`. A remaining open planning item appears only in the explanation ledger.

### Open Item Retirement

For each candidate planning item:

1. Match against user-specified facts. If matched, resolve it as a user-controlled commitment.
2. Match against blueprint-confirmed facts. If matched, resolve it as a blueprint-controlled commitment.
3. Match against existing drafts, notes, or result facts. If matched, resolve it as an existing-evidence commitment.
4. Match against runtime research facts. If the item is venue, field, or current-protocol sensitive, use deepresearch and resolve it as a live-research-selected commitment.
5. Classify execution-level details. If later coding, experiment-running, plotting, or writing skills can decide the detail without changing the strategic objective, encode it as a downstream execution interface field.
6. Preserve only strategic open items. Keep an item open only when it changes the experiment objective, required resource, story placement, or claim coverage.
7. Omit non-controlling ambiguity.

When a new fact closes an item that was previously open, list it under `Planning items closed in this revision` in the explanation ledger.

## Positive Evidence Contract

The plan's purpose is to make the paper's core intuition, method mechanism, and main claims visible and credible to reviewers.

Use positive planning fields:

```markdown
#### Planning State and Source
- Source state: user-specified / blueprint-confirmed / existing-evidence / live-research-selected / skill-derived / open-input.
- Source detail: <which fact or research synthesis controls this choice>.
- Execution selection handle: <what later execution skills should use when selecting concrete files, implementations, or scripts>.
```

Use `open-input` only when the missing input changes the plan structure. Explain the corresponding item in the explanation ledger's `Remaining open planning items`.

Use `Downstream Feedback Slots` for later result-driven updates from experiment execution, plotting, writing, or review feedback. These slots are update interfaces for future evidence, not predictions that a claim will fail.

## Motivation and Design-Insight Experiments

A motivation experiment makes a core intuition, existing-system defect, or method mechanism directly observable before the full system is complete.

Use two main forms:

- `Existing-system defect demonstration`: show a structural weakness in current systems, methods, metrics, schedulers, pipelines, or evaluation protocols.
- `Core-mechanism feasibility demonstration`: show that the proposed mechanism captures the important structure in a minimal faithful setting.

Motivation and design-insight objectives belong in the Introduction, Motivation, Method opening, or Method design justification. Their result artifact should be immediately readable: a figure, compact table, case study, trace timeline, qualitative grid, heatmap, breakdown, curve separation, before/after panel, or diagnostic example.

When an objective's `Evidence Role` includes `motivation` or `design insight`, include:

```markdown
#### Intuition Made Visible
The engineering intuition, existing-system defect, or core mechanism this objective makes directly observable.

#### Minimal Demonstration Setting
The smallest existing-system, partial-prototype, diagnostic, trace-based, benchmark-based, or controlled setting that can reveal the intuition before the full system is complete.

#### One-Glance Evidence Artifact
The figure, table, case study, timeline, qualitative grid, heatmap, breakdown, or curve that should make the intuition obvious to the reader.

#### Link to the Full Method Evaluation
How this early evidence prepares the reader for the later end-to-end or final-effectiveness objective.
```

## Live Research Strategy

Run the smallest set of deepresearch passes needed for the task:

1. **Recent venue pattern scan.** Find recent strong papers and extract their experimental thesis, evidence roles, datasets, traces, benchmarks, testbeds, user studies, deployments, baselines, metrics, ablations, stress tests, artifact signals, and reviewer expectations.
2. **Baseline / benchmark freshness scan.** Separate current must-use protocols, optional protocols useful for reviewer confidence, older canonical baselines still expected by reviewers, stale protocols, and implementation availability for later execution skills. Return the synthesis as planning commitments.
3. **Motivation pattern scan.** Find recent papers that use motivation or early design-insight experiments to make an intuition visible before full evaluation. Extract the intuition, setting, one-glance artifact, story placement, and connection to final evaluation.
4. **High-impact pattern scan.** Extract reusable evidence-design patterns from high-impact papers from the last 3-5 years. Use them for plan architecture, not stale baseline selection.

Compress live research into:

- `runtime_research_facts_used_in_this_version`
- `planning_commitments_derived_from_those_facts`
- objective-specific planning state and source details

## Deepresearch Prompt Shape

Use this shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a confirmation-state-aware positive evidence planner for an academic paper.

Research brief:
[RESEARCH_BRIEF]

Target venue and field:
[TARGET_VENUE_AND_FIELD]

Confirmed planning facts:
[CONFIRMED_FACTS]

Return four sections:

1. Current venue and field protocols
   Separate facts into current must-use protocols, optional protocols useful for reviewer confidence, older canonical baselines still expected by reviewers, protocols stale for the target year, and implementation availability later execution skills can use. Return these as planning commitments, not user questions.

2. Recent paper evidence patterns
   Find recent strong papers from the last 24 months or latest target-venue cycles. Extract claim-to-evidence patterns, datasets, traces, benchmarks, baselines, metrics, ablations, stress tests, scale tests, qualitative/user/deployment evidence, artifact signals, and result presentation patterns.

3. Motivation and design-insight patterns
   Find recent strong papers that use motivation experiments or early design-insight experiments to make an intuition visible before full method evaluation. For each, extract the intuition or failure mode, the minimal setting, the one-glance artifact, the story placement, and how it prepares the reader for final evaluation.

4. Planning commitments for this paper
   Explain how the confirmed facts should become experiment objectives, story placements, motivation artifacts, final-evaluation objectives, baseline/dataset/metric protocols, and downstream execution interfaces.

For each source, include title, venue/year when available, link, relevance to this paper, and the lesson for experiment planning.
Use concise evidence-facing prose.
```

## Workflow

### Step 1: Update Confirmed Planning Facts

Create the explanation ledger:

```markdown
## Confirmed planning facts

### User-specified facts

### Blueprint-confirmed facts

### Existing draft, note, or result facts

### Runtime research facts used in this version

### Planning commitments derived from those facts

### Planning items closed in this revision

### Remaining open planning items
```

If no strategic open item remains, write:

```markdown
There are no remaining open planning items that affect the current experiment-plan structure.
```

### Step 2: Normalize the Experimental Thesis

Write a concise paper-level thesis:

```text
The experiments are designed to show that {method/system} solves {problem} by {mechanism}, under {venue-relevant settings}, while improving {primary outcomes} relative to {current alternatives}.
```

### Step 3: Build the Claim-to-Evidence Map

For each major claim, identify:

- required evidence
- objective heading
- evidence role
- story placement
- planning state
- comparator or baseline class
- dataset, benchmark, trace, workload, scene, user, deployment, or simulation class
- metric or observable evidence family
- intended reader takeaway

Use confirmed facts first, live research second, and skill-derived planning logic third.

### Step 4: Design Motivation and Design-Insight Objectives

For each confirmed core intuition or problem claim, create a motivation or design-insight objective when the paper story needs early evidence.

Each such objective specifies:

- `Intuition Made Visible`
- `Minimal Demonstration Setting`
- `One-Glance Evidence Artifact`
- `Link to the Full Method Evaluation`

Use existing systems, public benchmarks, traces, partial prototypes, controlled diagnostic settings, or small faithful demonstrations before the full system is complete.

### Step 5: Design Final-Evaluation Objectives

Create objectives for main effectiveness, mechanism/ablation, generalization, robustness, efficiency/scalability, human/perceptual evidence, deployment realism, and artifact readiness as required by the claims and target venue.

### Step 6: Write `experiment_plan.md`

Use this structure:

```markdown
# Experiment Plan: <Working Title>

## 1. Paper-level Experimental Thesis

## 2. Evidence Strategy for the Paper Story

## 3. Claim-to-Evidence Map

| Paper claim | Required evidence | Objective heading | Story placement | Planning state |
|---|---|---|---|---|

## 4. Experiment Objective Groups

### Objective: <heading>

#### Story Placement
#### Evidence Role
#### Supported Paper Claims
#### Planning State and Source
#### Intuition Made Visible
#### Minimal Demonstration Setting
#### One-Glance Evidence Artifact
#### Link to the Full Method Evaluation
#### Evaluation Setting
#### Comparators and Baselines
#### Metrics and Observable Evidence
#### Controls, Variables, and Stress Conditions
#### Expected Tables, Figures, or Qualitative Artifacts
#### Downstream Execution Interface
#### Priority and Dependencies

## 5. Cross-Experiment Coherence

## 6. Downstream Feedback Slots
```

Use the motivation-specific fields for motivation and design-insight objectives. Omit those fields for objectives where they are not relevant.

### Step 7: Write `experiment_plan_explanation.<lang>.md`

Use this structure, translated naturally when appropriate:

```markdown
# Experiment Plan Explanation: <Working Title>

## Confirmed planning facts

### User-specified facts
### Blueprint-confirmed facts
### Existing draft, note, or result facts
### Runtime research facts used in this version
### Planning commitments derived from those facts
### Planning items closed in this revision
### Remaining open planning items

## The experimental story this plan is building

## How the motivation and insight objectives make the core intuition visible

### Objective: <same heading as in experiment_plan.md>

## How the final evaluation objectives support the paper claims

### Objective: <same heading as in experiment_plan.md>

## How the objectives connect into one evidence chain

## Review guide for this plan
```

For each objective, explain in prose:

- which confirmed fact or paper claim it follows from
- why its story placement is appropriate
- for motivation/design-insight objectives, what intuition it makes visible
- what one-glance artifact should convince the reader
- how it prepares for or complements later objectives
- what upstream confirmed fact the user should inspect when reviewing this part

Use objective headings and semantic names. Avoid artificial chains such as `C1/B2/E3`.

## Machine-Readable Summary

When writing a machine-readable summary for validation, use `assets/experiment_plan_schema.yaml` and optionally run:

```bash
python scripts/validate_experiment_plan.py <experiment-plan-summary.json>
```

The summary is optional unless the user or pipeline asks for it. It is a validation aid, not one of the two required deliverables.

## Final Quality Checklist

Before finalizing `experiment_plan.md`, check that:

- the file is English-only and contains only the experiment plan
- the plan is a positive evidence specification
- every major paper claim has at least one evidence objective
- every objective has story placement
- every objective has `Planning State and Source`
- user-specified, blueprint-confirmed, existing-evidence, and live-research-selected facts appear as planning commitments
- `open-input` appears only when the missing input changes plan structure
- motivation and design-insight objectives make a core intuition, existing-system defect, or method mechanism visible before full evaluation
- every motivation or design-insight objective has a one-glance artifact intent
- current baselines, datasets, benchmarks, metrics, and protocols come from live research or confirmed user/blueprint constraints
- downstream execution interfaces are present for later AI skills
- downstream feedback slots are present for future result-driven updates

Before finalizing `experiment_plan_explanation.<lang>.md`, check that:

- the file uses the user's conversation language and contains only the plan explanation
- the file begins with the confirmation ledger
- confirmed facts are separated by source
- newly resolved items appear in `Planning items closed in this revision`
- remaining open planning items materially affect objective design, story placement, required resources, or claim coverage
- no remaining open item duplicates a user-specified, blueprint-confirmed, existing-evidence, or live-research-selected fact
- if no strategic open item remains, the ledger says there are no remaining open planning items that affect the current experiment-plan structure
- the explanation shows how each objective follows from confirmed facts, story placement, venue patterns, one-glance evidence needs, and downstream interfaces
- the explanation uses readable prose and objective headings instead of dense cross-reference codes
