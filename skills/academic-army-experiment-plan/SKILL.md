---
name: academic-army-experiment-plan
description: >-
  Create a clean two-artifact academic experiment plan: an English, AI-facing
  experiment_plan.md that contains only the strategic experiment specification,
  and a user-language experiment_plan_explanation.<lang>.md that explains the
  confirmed-input ledger, live-research context, and reasoning behind each
  objective. Use when a research idea, paper_blueprint.md, paper goals, claims,
  storytelling blueprint, target venue, existing notes/results, or revision
  feedback must be converted into claim-to-evidence objectives, shared
  protocols, target evidence artifacts, target evidence patterns, and downstream
  execution interfaces. Uses academic_army_mcp_tools.deepresearch, canonical
  Codex MCP tool name mcp__academic_army_mcp_tools__deepresearch, for current
  venue, baseline, dataset, metric, benchmark, artifact, motivation-pattern,
  and reviewer-expectation research.
---

# Academic Army Experiment Plan

## Output Contract

Create exactly two Markdown deliverables.

### File 1: `experiment_plan.md`

Write this file in English. It is an AI-facing strategic experiment plan for
later experiment-running, coding, plotting, paper-writing, and review-response
skills.

The plan contains only the experiment specification. It does not contain the
confirmed-input ledger, source explanations, live-research notes, skill
self-explanations, literature-review prose, user-facing caveats, fallback
language, or future feedback questionnaires.

Include only:

- experimental thesis, primary comparison, and operating conditions
- claim-to-evidence architecture
- shared workloads, baselines, metrics, logging schema, resource/cost protocol,
  waste taxonomy, and artifact manifest protocol
- experiment objectives organized by paper claim and story role
- for each objective: story role, evidence goal, supported claims, decision
  supported by the experiment, core experiment, controlled factors,
  comparators, metrics, target evidence artifacts, target evidence pattern,
  output files, logging schema, dependencies, and priority
- a short objective dependency graph or evidence order when useful
- concise execution input slots only when a missing concrete handle is needed
  by downstream execution skills

The plan must be fielded, compact, and machine-readable enough for later AI
skills. Prefer short bullets and stable field names over long explanatory
paragraphs.

### File 2: `experiment_plan_explanation.<lang>.md`

Write this file in the user's conversation language. It is the human
confirmation companion for the plan.

The explanation begins with a confirmed-input ledger and then explains why the
plan is structured as it is. It should make the derivation inspectable: the user
should be able to see which objective follows from which core paper claim,
storytelling choice, venue pattern, live-research update, or skill-derived
planning step.

Include:

- confirmed facts from the user
- confirmed facts from the paper blueprint
- confirmed facts from existing notes, drafts, results, or previous explanation
  files
- live-research context used in this version, including recent-paper anchors
  only when they shaped the plan
- skill-derived experiment arrangements based on the confirmed facts
- planning items closed in this revision
- remaining open planning items only when the missing input changes an
  objective, required resource, story placement, or claim coverage
- prose explaining the core experimental logic and each objective's role in the
  paper story

Open items appear only in the explanation ledger, not in the plan. As the user
adds instructions across revisions, confirmed facts grow and remaining open
planning items shrink.

## Required Research MCP

Use the `deepresearch` tool from the `academic_army_mcp_tools` MCP server for
live research whenever venue-, field-, or date-sensitive facts affect the plan.

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical Codex MCP tool name, when exposed:
  `mcp__academic_army_mcp_tools__deepresearch`

Use `academic_army_mcp_tools.deepresearch` for:

- recent strong target-venue or adjacent-venue papers
- current baselines, datasets, benchmarks, traces, workloads, metrics, and
  evaluation protocols
- current reviewer expectations around artifacts, user studies, production
  traces, scale tests, perceptual studies, deployment evidence, or
  reproducibility
- motivation and design-insight experiment patterns that make an intuition
  visible before full method evaluation

Use live research to make planning commitments. Put the concise synthesis and
source anchors in the explanation file. Put only the resulting experiment
choices in the plan.

## Inputs to Extract

Extract or infer:

- target venue, track, and likely submission context
- research field and subfield
- research idea, method, system, dataset, benchmark, or theoretical object under
  evaluation
- upstream `paper_blueprint.md` or equivalent blueprint content
- paper-level goals, claims, novelty boundary, evidence posture, and
  storytelling blueprint
- available resources: code, data, models, compute, hardware, testbed, traces,
  simulator, deployment access, annotation resources, user-study access
- known constraints: time, compute, inaccessible data, required public
  benchmarks, privacy limits, mandatory baselines, unavailable baselines
- existing experiment notes, drafts, preliminary results, prior explanation
  files, or revision feedback
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

A user-specified, blueprint-confirmed, existing-evidence, or live-research
choice becomes a planning commitment. A downstream execution detail becomes an
execution input slot or handle for later skills. A remaining open planning item
appears only in the explanation ledger.

### Open Item Retirement

For each candidate planning item:

1. Match against user-specified facts. If matched, resolve it as a
   user-controlled commitment.
2. Match against blueprint-confirmed facts. If matched, resolve it as a
   blueprint-controlled commitment.
3. Match against existing drafts, notes, or result facts. If matched, resolve it
   as an existing-evidence commitment.
4. Match against runtime research facts. If the item is venue, field, or
   current-protocol sensitive, use deepresearch and resolve it as a
   live-research-selected commitment.
5. Classify execution-level details. If later coding, experiment-running,
   plotting, or writing skills can decide the detail without changing the
   strategic objective, encode it as an execution input slot or handle.
6. Preserve only strategic open items. Keep an item open only when it changes
   the experiment objective, required resource, story placement, or claim
   coverage.
7. Omit non-controlling ambiguity.

When a new fact closes an item that was previously open, list it under
`Planning items closed in this revision` in the explanation ledger.

## Positive Evidence Contract

The plan's purpose is to make the paper's core intuition, method mechanism, and
main claims visible and credible to reviewers.

Use positive, executable planning language:

- Write `Measure visible quality, deadline feasibility, and action distribution
  as prediction error increases.`
- Write `Report quality metrics with matching bandwidth, rendering,
  restoration, controller-overhead, and resource-cost metrics.`
- Write `The evaluation scope is trace-driven prototype evaluation unless the
  confirmed input ledger specifies deployment-scale evaluation.`
- Write `Dynamic scenes are included when the confirmed claim scope covers
  dynamic volumetric media; otherwise they are secondary workload candidates in
  the explanation file.`
- Write `The plan includes artifact outputs when they directly support
  execution, plotting, writing, or reproducibility.`

Avoid defensive reviewer-facing phrasing, fallback paths, and questionnaire
language in the plan. Express uncertainty as structured execution input slots in
the plan only when downstream skills need a concrete handle; express strategic
open items in the explanation ledger only.

## Goal-Oriented Objective Design

Each objective starts from the paper claim it supports, not from a generic
evaluation checklist.

For every candidate objective, answer:

- Which paper claim does it support?
- What story role does it serve: motivation/problem definition, method design
  insight, main end-to-end effectiveness, mechanism/ablation, robustness/stress,
  generalization, human/perceptual evidence, deployment realism, or
  cost/scalability/reproducibility protocol?
- What reader decision should this experiment enable?
- What target evidence artifact should downstream plotting or writing produce?
- What target evidence pattern should the artifact make visible?
- Which workloads, comparators, metrics, controlled factors, logging fields, and
  output files are necessary for that artifact?

If a candidate objective does not correspond to an independent claim,
independent story role, or independent paper artifact, merge it into another
objective as a metric slice, reporting view, or shared protocol.

### Target Evidence Pattern

Every objective must include `Target evidence pattern`.

This field describes the phenomenon the paper needs the figure, table, timeline,
heatmap, qualitative panel, or diagnostic artifact to expose. It is not a
prediction of exact numeric success and not a fallback condition. It tells
downstream experiment, plotting, and writing skills what should be made
immediately legible.

Examples:

- `The heatmap exposes state regions where references are useful, stale,
  mismatched, redundant, or dominated by Gaussian enhancement.`
- `The deadline view shows visible-region quality together with deadline-hit
  rate and interaction-to-visible-quality latency under bandwidth, viewport,
  rendering, and restoration variability.`
- `The ablation chart shows which controller component accounts for resource
  selection, viewport-risk handling, and deadline-aware scheduling behavior.`

## Motivation and Design-Insight Experiments

A motivation experiment makes a core intuition, existing-system defect, or
method mechanism directly observable before the full system is complete.

Use two main forms:

- `Existing-system defect demonstration`: show a structural weakness in current
  systems, methods, metrics, schedulers, pipelines, or evaluation protocols.
- `Core-mechanism feasibility demonstration`: show that the proposed mechanism
  captures the important structure in a minimal faithful setting.

Motivation and design-insight objectives belong in the Introduction,
Motivation, Method opening, or Method design justification. Their target
evidence artifact should be immediately readable: a figure, compact table, case
study, trace timeline, qualitative grid, heatmap, breakdown, curve separation,
before/after panel, or diagnostic example.

In the plan, encode this through `Story role`, `Evidence goal`, `Target evidence
artifact`, and `Target evidence pattern`. Explain the intuition and derivation
in the explanation file, not in the plan.

## Redundancy Control

Before finalizing objectives, run a redundancy pass.

Merge or demote objectives when two candidates share more than half of their
controlled factors, workloads, metrics, or output artifacts.

Common merges:

- A `Reference Usefulness` objective and a `Gaussian-Reference Substitution`
  objective usually become one parent objective with two evidence artifacts:
  `Reference Usefulness Heatmap` and `Substitution Phase Diagram`.
- `End-to-End Interactive QoE` and `Deadline Reliability/Responsiveness`
  usually become one main objective with two required reporting views:
  `Quality/QoE View` and `Deadline/Responsiveness View`.
- `Resource Efficiency`, `Waste`, and `Artifact Readiness` usually become
  shared measurement, waste-taxonomy, and artifact-manifest protocols rather
  than standalone objectives.

Keep objectives separate only when they support distinct claims, occupy distinct
story roles, or produce distinct paper artifacts that cannot be represented as
views of the same experiment.

## Shared Protocols

Move repeated details into shared protocols instead of duplicating them in every
objective.

Use shared sections for:

- workloads: scenes, datasets, traces, users, simulations, hardware, network
  profiles, compute profiles, deadline profiles, and deployment/testbed scope
- baseline families: fair information, fair actions, fair resources, and oracle
  upper bounds
- metrics: quality, accuracy, latency, responsiveness, resource/cost, waste,
  user/perceptual, statistical reporting, and uncertainty reporting
- logging schema: required keys, timing fields, resource fields, quality fields,
  action/controller fields, trace/workload fields, random seeds, and run
  metadata
- waste taxonomy for reference-related, compute-related, bandwidth-related, or
  prediction-related resources
- artifact manifest protocol for result files, figure/table consumers,
  reproducibility handles, and handoff metadata

## Live Research Strategy

Run the smallest set of deepresearch passes needed for the task:

1. **Recent venue pattern scan.** Find recent strong papers and extract their
   experimental thesis, evidence roles, datasets, traces, benchmarks, testbeds,
   user studies, deployments, baselines, metrics, ablations, stress tests, scale
   tests, qualitative/user/deployment evidence, artifact signals, and reviewer
   expectations.
2. **Baseline / benchmark freshness scan.** Separate current must-use protocols,
   optional protocols useful for reviewer confidence, older canonical baselines
   still expected by reviewers, stale protocols, and implementation availability
   for later execution skills. Return these as planning commitments.
3. **Motivation pattern scan.** Find recent papers that use motivation or early
   design-insight experiments to make an intuition visible before full
   evaluation. Extract the intuition, setting, one-glance artifact, story
   placement, and connection to final evaluation.
4. **High-impact pattern scan.** Extract reusable evidence-design patterns from
   high-impact papers from the last 3-5 years. Use them for plan architecture,
   not stale baseline selection.

Compress live research into the explanation file:

- `Current field and venue experiment patterns`
- `Live-research anchors used in this version`
- `Planning commitments derived from those anchors`

Do not put full literature notes, URLs, tool logs, or research-anchor prose in
`experiment_plan.md`.

## Deepresearch Prompt Shape

Use this shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a confirmation-state-aware positive evidence planner for an
academic paper.

Research brief:
[RESEARCH_BRIEF]

Target venue and field:
[TARGET_VENUE_AND_FIELD]

Confirmed planning facts:
[CONFIRMED_FACTS]

Return four sections:

1. Current venue and field protocols
   Separate facts into current must-use protocols, optional protocols useful for
   reviewer confidence, older canonical baselines still expected by reviewers,
   protocols stale for the target year, and implementation availability later
   execution skills can use. Return these as planning commitments, not user
   questions.

2. Recent paper evidence patterns
   Find recent strong papers from the last 24 months or latest target-venue
   cycles. Extract claim-to-evidence patterns, datasets, traces, benchmarks,
   baselines, metrics, ablations, stress tests, scale tests, qualitative/user/
   deployment evidence, artifact signals, and result presentation patterns.

3. Motivation and design-insight patterns
   Find recent strong papers that use motivation experiments or early
   design-insight experiments to make an intuition visible before full method
   evaluation. For each, extract the intuition or failure mode, the minimal
   setting, the one-glance artifact, the story placement, and how it prepares
   the reader for final evaluation.

4. Planning commitments for this paper
   Explain how the confirmed facts should become experiment objectives, story
   placements, motivation artifacts, final-evaluation objectives,
   baseline/dataset/metric protocols, and downstream execution interfaces.

For each source, include title, venue/year when available, link, relevance to
this paper, and the lesson for experiment planning.
Use concise evidence-facing prose.
```

## Workflow

### Step 1: Update Confirmed Planning Facts

Create the explanation ledger:

```markdown
## 用户已经明确的内容 / Confirmed User Inputs

## 论文蓝图中已经确定的内容 / Blueprint-Confirmed Inputs

## 已有草稿、笔记或结果中已经确定的内容 / Existing Evidence Inputs

## 本次 live research 更新的外部背景 / Live-Research Context Used

## 基于上述内容推导出的实验安排 / Skill-Derived Experiment Arrangements

## 本轮修改已经关闭的规划项 / Planning Items Closed in This Revision

## 剩余开放规划项 / Remaining Open Planning Items
```

Use the user's conversation language for headings and prose. If no strategic
open item remains, write the equivalent of:

```markdown
There are no remaining open planning items that affect the current
experiment-plan structure.
```

### Step 2: Normalize the Experimental Thesis

Split the thesis into stable fields:

- `Experimental thesis`: central mechanism and claim.
- `Primary comparison`: baseline and comparator families.
- `Operating conditions`: venue-relevant workload, environment, and variability
  conditions.

Keep this section to two or three concise sentences.

### Step 3: Build the Claim-to-Evidence Architecture

For each major claim, identify:

- evidence objective
- story role
- main artifact
- downstream consumers

Use confirmed facts first, live research second, and skill-derived planning
logic third. Put source explanations in the explanation file.

### Step 4: Build Shared Experimental Protocols

Before writing objectives, factor out repeated:

- workloads
- baseline families
- shared metrics
- logging schema
- resource/cost reporting
- waste taxonomy
- artifact manifest protocol
- execution input slots

These shared protocols prevent objective-level repetition and give downstream
skills a stable interface.

### Step 5: Design Goal-Oriented Objectives

For each confirmed core claim, create the smallest objective set that covers:

- motivation/problem definition
- method design insight
- main end-to-end effectiveness
- mechanism/ablation
- robustness/stress
- generalization
- human/perceptual evidence
- deployment realism
- cost/scalability/reproducibility protocol

The last category is usually a shared reporting protocol or view, not an
independent objective.

### Step 6: Run Objective Redundancy Check

Merge objectives that share more than half of their controlled factors, metrics,
workloads, and artifacts. Convert repeated cost, waste, latency, and artifact
readiness details into shared protocols or reporting views.

### Step 7: Write `experiment_plan.md`

Use this structure:

```markdown
# Experiment Plan: <Paper/System Name>

## 1. Experimental Thesis

- Experimental thesis:
- Primary comparison:
- Operating conditions:

## 2. Claim-to-Evidence Architecture

| Claim | Evidence Objective | Story Role | Main Artifact | Downstream Consumers |
|---|---|---|---|---|

## 3. Shared Experimental Protocol

### Workloads
- Scenes/datasets:
- Viewport/user traces:
- Network traces:
- Compute/hardware profiles:
- Deadline profiles:

### Shared Baseline Families
- <baseline family>: <fair information/actions/resources>
- <oracle>: <upper-bound role, not a deployable baseline>

### Shared Metrics
- Quality:
- Deadline/responsiveness:
- Resource/cost:
- Waste:
- Statistical reporting:

### Shared Logging Schema
- Required keys:
- Required timing fields:
- Required resource fields:
- Required quality fields:
- Required action/controller fields:

### Shared Resource, Waste, and Artifact Protocol
- Resource/cost reporting:
- Waste taxonomy:
- Artifact manifest:

### Execution Input Slots
- <slot>: <required handle for downstream execution skills>

## 4. Experiment Objectives

### Objective 1: <Name>

- Story role:
- Evidence goal:
- Claims supported:
- Decision supported:
- Core experiment:
- Controlled factors:
- Comparators:
- Primary metrics:
- Secondary metrics:
- Target evidence artifacts:
- Target evidence pattern:
- Output files:
- Logging schema:
- Dependencies:
- Priority:

### Objective 2: <Name>
...

## 5. Objective Dependency Graph

- <objective/evidence artifact> -> <objective/evidence artifact>:
```

Omit `Execution Input Slots` only when no concrete execution handles are needed.
Keep the dependency graph short. Do not add a separate cross-experiment prose
essay.

### Step 8: Write `experiment_plan_explanation.<lang>.md`

Use this structure, translated naturally when appropriate:

```markdown
# Experiment Plan Explanation: <Paper/System Name>

## 用户已经明确的内容

## 论文蓝图中已经确定的内容

## 已有草稿、笔记或结果中已经确定的内容

## 本次 live research 更新的外部背景

## 基于上述内容推导出的实验安排

## 本轮修改已经关闭的规划项

## 剩余开放规划项

## 当前领域和目标 venue 的实验模式

## 核心实验逻辑

## 每个 Objective 的推导

### <Objective name>

## Objective 之间的证据链关系

## 用户审核这份计划时应重点看的地方
```

For each objective, explain in prose:

- which confirmed fact or paper claim it follows from
- why its story placement is appropriate
- which intuition, defect, or mechanism it makes visible
- why the target artifact and target evidence pattern fit the paper story
- how it prepares for or complements later objectives
- which upstream confirmed fact the user should inspect when reviewing this
  objective

Use objective headings and semantic names. Avoid dense cross-reference codes
such as `C1/C2/B1/E1`.

## Machine-Readable Summary

When writing a machine-readable summary for validation, use
`assets/experiment_plan_schema.yaml` and optionally run:

```bash
python scripts/validate_experiment_plan.py <experiment-plan-summary.json>
```

The summary is optional unless the user or pipeline asks for it. It is a
validation aid, not one of the two required deliverables.

## Final Quality Checklist

Before finalizing `experiment_plan.md`, check that:

- the file is English-only and contains only the experiment plan
- the plan does not contain the confirmation ledger, source explanations,
  live-research notes, literature review prose, skill self-description, or
  user-facing rationale
- the plan uses `Experimental thesis`, `Primary comparison`, and `Operating
  conditions`
- every major paper claim has at least one evidence objective
- every objective has story role, evidence goal, supported claims, decision
  supported, target evidence artifacts, and target evidence pattern
- resource/cost metrics, waste taxonomy, logging schema, and artifact manifest
  requirements are shared protocols unless they support an independent claim
- objectives with overlapping workloads, metrics, controls, and artifacts have
  been merged or represented as reporting views
- open planning items do not appear in the plan
- execution input slots are machine-readable handles, not user questions
- the plan avoids fallback language, future feedback questionnaires, and
  defensive reviewer-facing phrasing
- current baselines, datasets, benchmarks, metrics, and protocols come from
  confirmed user/blueprint constraints or live research

Before finalizing `experiment_plan_explanation.<lang>.md`, check that:

- the file uses the user's conversation language and contains only the plan
  explanation
- the file begins with the confirmed-input ledger
- confirmed facts are separated by user, blueprint, existing evidence, live
  research, and skill-derived arrangements
- newly resolved items appear in `Planning items closed in this revision`
- remaining open planning items materially affect objective design, story
  placement, required resources, or claim coverage
- no remaining open item duplicates a user-specified, blueprint-confirmed,
  existing-evidence, or live-research-selected fact
- if no strategic open item remains, the ledger says there are no remaining
  open planning items that affect the current experiment-plan structure
- live-research anchors are summarized here rather than in the plan
- the explanation shows how each objective follows from the core thesis, story
  placement, venue patterns, target evidence needs, and downstream interfaces
- the explanation uses readable prose and objective headings instead of dense
  cross-reference codes
