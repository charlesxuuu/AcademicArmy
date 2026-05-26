---
name: academic-army-experiment-plan
description: >-
  Create a clean multi-artifact academic experiment plan: an English,
  AI-facing experiment_plan.md that contains only the strategic experiment
  specification; a user-language experiment_plan_explanation.<lang>.md for
  human confirmation; experiment_interface_contracts.yaml for workloads,
  baselines, logging, artifact manifests, and execution handles;
  experiment_metric_contracts.yaml for metric definitions; and
  research_context.md for live-research anchors and verified IDs. Use when a
  research idea, paper_blueprint.md, paper goals, claims, storytelling
  blueprint, target venue, existing notes/results, or revision feedback must be
  converted into claim-to-evidence objectives, shared protocol references,
  target evidence artifacts, target evidence patterns, and downstream execution
  interfaces. Uses academic_army_mcp_tools.deepresearch, canonical Codex MCP
  tool name mcp__academic_army_mcp_tools__deepresearch, for current venue,
  baseline, dataset, metric, benchmark, artifact, motivation-pattern, and
  reviewer-expectation research.
---

# Academic Army Experiment Plan

## Output Contract

Create exactly five deliverables.

### File 1: `experiment_plan.md`

Write this file in English. It is an AI-facing strategic experiment plan for
later experiment-running, coding, plotting, paper-writing, and review-response
skills.

The plan contains only the experiment specification. It does not contain the
confirmed-input ledger, source explanations, live-research notes, skill
self-explanations, literature-review prose, user-facing caveats, fallback
language, future feedback questionnaires, full baseline contracts, full metric
contracts, or live-research source lists.

Include only:

- experimental thesis, primary comparison, and operating conditions
- claim-to-evidence architecture
- research context and contract references
- shared protocol summary that points to contract files
- experiment objectives organized by paper claim and story role
- for each objective: story role, evidence goal, supported claims, evidence
  outputs, writing scope outputs, boundary, core experiment, controlled factors,
  comparator IDs, metric IDs, target evidence artifacts, target evidence
  pattern, output files, logging schema reference, reuse policy, dependencies,
  and priority
- derived analyses and artifact protocol summaries when they aggregate existing
  objective outputs rather than running new experiments
- a short objective dependency graph or evidence order when useful

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

### File 3: `experiment_interface_contracts.yaml`

Write this file in YAML. It is the machine-facing interface for experiment
runner, code generation, result analysis, plot planning, and reproducibility
skills.

Include:

- workload contracts, split into required workloads and scope-extension
  workload candidates
- baseline contracts, split into required baselines, diagnostic baselines, and
  upper bounds
- baseline state contracts with `available_state`, `state_used_by_policy`, and
  `forbidden_state_usage`
- baseline implementation contracts with acceptable implementations and minimum
  behavioral contract when a named external implementation is not the only
  valid route
- `allowed_use` for each baseline: `main_comparison`, `diagnostic`,
  `oracle_upper_bound`, or `ablation_only`
- shared logging schema
- execution input slots
- artifact manifest and result-file handoff protocol

### File 4: `experiment_metric_contracts.yaml`

Write this file in YAML. It is the machine-facing metric dictionary.

Include every metric ID used in `experiment_plan.md` or
`experiment_interface_contracts.yaml`. Each metric contract includes:

- `metric_id`
- `type`
- `unit_or_range`
- `sign`
- `definition_status`: `confirmed`, `delegated`, or `unresolved`
- `definition_owner`
- `formula_id`
- `formula_ref` when confirmed
- `required_decision` when delegated or unresolved
- `required_inputs`
- `aggregation_policy`
- `used_by_objectives`

For ratio metrics, include `numerator` and `denominator`. For CDF or
distribution metrics, include `x_unit`, `y_unit`, and `zero_point`.

### File 5: `research_context.md`

Write this file in English unless the user explicitly asks otherwise. It is the
source-backed context for current venue patterns, research anchors, and
canonical IDs used by the plan and contracts.

Include:

- `last_verified_at` using the current date
- target venue and field
- source-backed baseline, workload, and metric IDs used by other artifacts
- source title, venue/year from source metadata, link, relevance, and planning
  lesson
- alternatives or implementation notes when a canonical baseline family can be
  satisfied by multiple equivalent implementations

The plan references this file by ID or path. The plan does not repeat the
source discussion.

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

Use live research to make planning commitments. Put source anchors and current
venue/field synthesis in `research_context.md`. Put user-facing reasoning about
how that research shaped the plan in `experiment_plan_explanation.<lang>.md`.
Put only references and IDs in `experiment_plan.md`.

When live research identifies papers, datasets, baselines, metrics, or workload
families, create stable IDs for the plan and put the source explanation in
`research_context.md`. The plan should reference canonical IDs such as
`lapisgs_like_layered_3dgs`, `lts_like_dynamic_multilayer_3dgs`, or
`n3dv_dynamic_multiview_sequences` only after `research_context.md` records the
verification source.

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
- Write `Required workloads: trace-driven prototype workloads confirmed by the
  ledger.`
- Write `Scope-extension workload candidates: dynamic volumetric sequences
  listed in the explanation file.`
- Write `The plan includes artifact outputs when they directly support
  execution, plotting, writing, or reproducibility.`
- Write `Evidence outputs: supported_scene_scope, supported_trace_scope,
  supported_substrate_scope.`
- Write `Writing scope outputs: dynamic_scene_claim_support,
  deployment_claim_support.`

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
- What evidence outputs should this experiment export for experiment runner,
  result analysis, plot planning, and paper writing skills?
- What writing scope outputs should this experiment export for paper writing and
  rebuttal preparation skills?
- What target evidence artifact should downstream plotting or writing produce?
- What target evidence pattern should the artifact make visible?
- Which workloads, comparators, metrics, controlled factors, logging fields, and
  output files are necessary for that artifact?
- What is the objective boundary, including what it measures and what it leaves
  to another objective or shared protocol?

If a candidate objective does not correspond to an independent claim,
independent story role, or independent paper artifact, merge it into another
objective as a metric slice, reporting view, or shared protocol.

Use `Evidence outputs` and `Writing scope outputs` as machine-readable lists of
signals, not as human-facing questions. Examples:

- `supported_scene_scope`
- `supported_trace_scope`
- `supported_substrate_scope`
- `mechanism_attribution_to_state_terms`
- `dynamic_scene_claim_support`
- `deployment_claim_support`

The plan uses `Evidence outputs` and `Writing scope outputs` for these signals.
Human-readable decision reasoning belongs in the explanation file.

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

When two objectives overlap but should remain separate, add a `Boundary` field
to each objective:

```markdown
- Boundary:
  - Includes:
    - <what this objective measures>
  - Excludes:
    - <what another objective or shared protocol measures>
```

Example:

```markdown
- Boundary:
  - Includes:
    - Per-state marginal utility under controlled candidate states.
  - Excludes:
    - Full online queue evolution beyond controlled deadline slack.
```

## Shared Protocols

Move repeated details into shared protocols instead of duplicating them in every
objective.

Use shared sections for:

- workloads: scenes, datasets, traces, users, simulations, hardware, network
  profiles, compute profiles, deadline profiles, deployment/testbed scope,
  required workloads, and scope-extension workload candidates. Put the full
  workload contract in `experiment_interface_contracts.yaml`.
- research context references: paths and anchors for source-backed baseline,
  workload, and metric IDs. Put the source notes in `research_context.md`.
- baseline contract references: baseline IDs grouped by required, diagnostic,
  and upper bound roles. Put full state and fairness contracts in
  `experiment_interface_contracts.yaml`.
- metric references: metric IDs grouped by quality, deadline/responsiveness,
  resource/cost, waste, and statistical reporting. Put full metric definitions
  in `experiment_metric_contracts.yaml`.
- logging schema reference, waste taxonomy reference, execution input slots
  reference, and artifact manifest reference. Put full fields in
  `experiment_interface_contracts.yaml`.

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

Compress live research into `research_context.md`:

- `Current field and venue experiment patterns`
- `Live-research anchors used in this version`
- `Planning commitments derived from those anchors`
- `Canonical IDs exported to the plan and contracts`

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

For each source, include title, venue/year from source metadata, link,
relevance to this paper, and the lesson for experiment planning. If the source
metadata does not provide a venue or year, leave that source attribute empty in
the explanation file instead of adding fallback language to the plan.
Use concise evidence-facing prose.
```

## Workflow

### Step 1: Update Confirmed Planning Facts

Create the explanation ledger:

```markdown
## 用户已经明确的内容 / Confirmed User Inputs

- Target system:
- Target venue / field:
- Core method claim:
- Confirmed story roles:
- Confirmed experiment scope:
- Confirmed workloads:
- Confirmed baselines:
- Confirmed exclusions:

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

Use only these downstream consumer IDs unless the local toolchain provides a
more specific skill ID:

- `experiment_runner`
- `code_generation`
- `result_analysis`
- `plot_planning`
- `paper_writing`
- `rebuttal_preparation`
- `reproducibility`

### Step 4: Build Shared Experimental Protocols

Before writing objectives, factor out repeated:

- workloads
- research context references
- baseline contract references
- metric ID references
- logging schema references
- resource/cost reporting references
- waste taxonomy references
- artifact manifest protocol references
- execution input slot references

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

For workload scope, write deterministic categories:

- `Required workloads`: workloads committed by the user, blueprint, existing
  evidence, or live-research-selected venue protocol.
- `Scope-extension workload candidates`: workload IDs that would extend claim
  scope and are explained in the explanation file.

Do not write `when available`, `if resources permit`, or equivalent fallback
phrases in the plan.

### Step 6: Run Objective Redundancy Check

Merge objectives that share more than half of their controlled factors, metrics,
workloads, and artifacts. Convert repeated cost, waste, latency, and artifact
readiness details into shared protocols or reporting views.

Each objective must satisfy:

- `unique_claim_supported`
- `unique_story_role`
- `unique_primary_artifact`
- `non_overlapping_boundary`

If these cannot all be satisfied, merge the objective into another objective or
make it a reporting view.

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

### Research and Contract References
- research_context_ref: research_context.md
- interface_contracts_ref: experiment_interface_contracts.yaml
- metric_contracts_ref: experiment_metric_contracts.yaml

### Workload Scope Summary
- Required workload IDs:
- Scope-extension workload candidate IDs:

### Baseline Summary
- Required baseline IDs:
- Diagnostic baseline IDs:
- Upper-bound IDs:

### Metric Summary
- Primary metric IDs:
- Secondary metric IDs:
- Cost/waste metric IDs:
- Statistical reporting IDs:

### Artifact and Logging Summary
- logging_schema_ref:
- artifact_manifest_ref:
- execution_input_slots_ref:

## 4. Experiment Objectives

### Objective 1: <Name>

- Story role:
- Evidence goal:
- Claims supported:
- Evidence outputs:
- Writing scope outputs:
- Boundary:
  - Includes:
  - Excludes:
- Core experiment:
- Controlled factors:
- Comparator IDs:
- Primary metric IDs:
- Secondary metric IDs:
- Target evidence artifacts:
- Target evidence pattern:
- Output files:
- Logging schema ref:
- Reuse policy:
- Dependencies:
- Priority:

### Objective 2: <Name>
...

## 5. Derived Analyses and Artifact Protocol

### Derived Analysis A: <Name>
- Inputs:
- Evidence outputs:
- Output files:
- Consumers:
- Contract refs:

## 6. Objective Dependency Graph

- <objective/evidence artifact> -> <objective/evidence artifact>:
```

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

### Step 9: Write `experiment_interface_contracts.yaml`

Use this structure:

```yaml
workloads:
  required_workloads:
    scenes_or_datasets: []
    viewport_or_user_traces: []
    network_traces: []
    compute_or_hardware_profiles: []
    deadline_profiles: []
  scope_extension_workload_candidates:
    - workload_id:
      scope_signal:
      explanation_ref:
      research_context_ref:

baselines:
  required_baselines:
    - baseline_id:
      role: required
      available_state: []
      state_used_by_policy: []
      forbidden_state_usage: []
      action_space:
      resource_budget:
      implementation_status:
      acceptable_implementations: []
      minimum_contract: []
      fairness_constraint:
      allowed_use: main_comparison
      used_by_objectives: []
  diagnostic_baselines: []
  upper_bounds:
    - baseline_id:
      role: oracle
      allowed_use: oracle_upper_bound
      not_for_main_claim_delta: true

logging_schema:
  required_keys: []
  required_timing_fields: []
  required_resource_fields: []
  required_quality_fields: []
  required_action_or_controller_fields: []
  required_run_metadata: []

execution_input_slots: []
artifact_manifest: []
```

### Step 10: Write `experiment_metric_contracts.yaml`

Use this structure:

```yaml
metrics:
  - metric_id:
    type:
    unit_or_range:
    sign:
    definition_status:
    definition_owner:
    formula_id:
    formula_ref:
    required_decision:
    default_base_metric_candidates: []
    required_inputs: []
    aggregation_policy:
    used_by_objectives: []
```

For ratio metrics add:

```yaml
numerator:
denominator:
```

For CDF or distribution metrics add:

```yaml
x_unit:
y_unit:
zero_point:
```

### Step 11: Write `research_context.md`

Use this structure:

```markdown
# Research Context: <Paper/System Name>

## Metadata

- last_verified_at:
- target_venue:
- field:

## Exported IDs

### Baseline IDs
### Workload IDs
### Metric IDs

## Current Field and Venue Patterns

## Source-Backed Anchors

### <source title>

- venue_or_year:
- link:
- relevance:
- planning_lesson:
- exported_ids:

## Alternatives and Contract Equivalences
```

## Built-In Lint Rules

Apply these checks before finalizing the five deliverables.

### File Boundary Lint

- `experiment_plan.md` exists, is English-only, and contains only the plan.
- `experiment_plan_explanation.<lang>.md` exists, uses the user's conversation
  language, and begins with the confirmed-input ledger.
- `experiment_interface_contracts.yaml` exists and contains workload, baseline,
  logging, execution-slot, and artifact-manifest contracts.
- `experiment_metric_contracts.yaml` exists and contains metric definitions.
- `research_context.md` exists and contains live-research anchors and exported
  IDs.
- Live-research anchors and source notes appear in `research_context.md`, not
  the plan.
- User-facing plan review reasoning appears in the explanation file, not the
  plan.
- If the plan contains `explanation_ref`, `research_context_ref`, or contract
  refs, the referenced file and heading or anchor must exist.

### Confirmed-Input Ledger Lint

- The explanation ledger records target system, target venue/field, core method
  claim, confirmed story roles, confirmed experiment scope, confirmed
  workloads, confirmed baselines, and confirmed exclusions when those facts are
  available.
- A fact resolved by the user, blueprint, existing evidence, or live research is
  not reintroduced as `whether`, `which`, `when available`, or any other open
  question in the plan.

### Objective Distinctness Lint

- Each objective has `unique_claim_supported`, `unique_story_role`,
  `unique_primary_artifact`, and `non_overlapping_boundary`.
- Objectives sharing more than half of their controlled factors, metrics,
  outputs, and dependencies are merged or represented as reporting views unless
  their `Boundary` fields make the distinction explicit.

### Baseline Contract Lint

Each baseline has:

- `baseline_id`
- `role`: required, diagnostic, or oracle
- `available_state`
- `state_used_by_policy`
- `forbidden_state_usage`
- `action_space`
- `resource_budget`
- `implementation_status`
- `acceptable_implementations`
- `minimum_contract`
- `implementation_owner`
- `fairness_constraint`
- `allowed_use`
- `used_by_objectives`

### Metric Contract Lint

Every named score, ratio, quality metric, waste metric, deadline metric, or
utility metric appears in `Metric Contracts` with:

- `metric_id`
- `type`
- `unit_or_range`
- `sign`
- `definition_status`: confirmed, delegated, or unresolved
- `definition_owner`
- `formula_id`
- `formula_ref` when confirmed
- `required_decision` when delegated or unresolved
- `required_inputs`
- `aggregation_policy`
- `used_by_objectives`

Ratio metrics include `numerator` and `denominator`. CDF or distribution
metrics include `x_unit`, `y_unit`, and `zero_point`.

### Derived-Analysis Lint

If an objective's core experiment aggregates logs from prior objectives and does
not require new workload runs, move it to `Derived Analyses and Artifact
Protocol`. Derived analyses can support claims, but they are not peer
experiment objectives.

### Defensive-Language Rewrite Lint

Scan the plan for:

```text
whether
if resources permit
when available
otherwise
do not
should remain
narrower claim
fail
hide cost
rebuttal-ready
boundary language
```

Rewrite these into positive plan fields. Examples:

- `whether the paper should claim...` becomes `Evidence outputs:
  supported_scene_scope, supported_trace_scope, supported_substrate_scope`.
- `when available` becomes `Scope-extension workload candidates`.
- `fail in different stress regimes` becomes `baseline-specific stress
  sensitivity`.
- `narrower claim scope` becomes `supported scope`.
- `hidden substrate cost` becomes `explicit substrate cost accounting`.
- `cannot reproduce` becomes `separated from baseline policy behavior`.
- `claim holds` becomes `supported behavior is measured`.
- `joint allocation is valuable` becomes `joint-allocation-favorable state
  regions`.

### Consumer Vocabulary Lint

Use fixed downstream consumer IDs:

- `experiment_runner`
- `code_generation`
- `result_analysis`
- `plot_planning`
- `paper_writing`
- `rebuttal_preparation`
- `reproducibility`

## Machine-Readable Summary

When writing a machine-readable summary for validation, use
`assets/experiment_plan_schema.yaml` and optionally run:

```bash
python scripts/validate_experiment_plan.py <experiment-plan-summary.json>
```

The summary is optional unless the user or pipeline asks for it. It is a
validation aid, not one of the five required deliverables.

## Final Quality Checklist

Before finalizing `experiment_plan.md`, check that:

- the file is English-only and contains only the experiment plan
- the plan does not contain the confirmation ledger, source explanations,
  live-research notes, literature review prose, skill self-description, or
  user-facing rationale
- the plan contains references to contract and research files, not full
  baseline contracts, full metric contracts, or source lists
- the plan uses `Experimental thesis`, `Primary comparison`, and `Operating
  conditions`
- every major paper claim has at least one evidence objective
- every objective has story role, evidence goal, supported claims, evidence
  outputs, writing scope outputs, boundary, target evidence artifacts, and
  target evidence pattern
- every baseline used by the plan appears in
  `experiment_interface_contracts.yaml`
- every named score, ratio, deadline, quality, waste, or utility metric appears
  in `experiment_metric_contracts.yaml`
- workload scope is expressed as required workloads and scope-extension
  candidates, not fallback language
- resource/cost metrics, waste taxonomy, logging schema, and artifact manifest
  requirements are references to contract files unless they support an
  independent claim summary
- objectives with overlapping workloads, metrics, controls, and artifacts have
  been merged, represented as reporting views, or separated by explicit
  `Boundary` fields
- analyses that only aggregate logs from prior objectives are under `Derived
  Analyses and Artifact Protocol`, not `Experiment Objectives`
- open planning items do not appear in the plan
- the plan avoids fallback language, future feedback questionnaires, and
  defensive reviewer-facing phrasing
- downstream consumers use the fixed vocabulary or explicit local skill IDs
- current baselines, datasets, benchmarks, metrics, and protocols have sources
  in the ledger, blueprint, contract files, or `research_context.md`

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

Before finalizing `experiment_interface_contracts.yaml`, check that:

- baseline contracts distinguish available state, state used by policy, and
  forbidden state usage
- oracle and diagnostic baselines have `allowed_use` values that prevent them
  from being used as main claim deltas
- named external baseline families include acceptable implementations and
  minimum behavioral contracts
- execution input slots are machine-readable handles, not user questions

Before finalizing `experiment_metric_contracts.yaml`, check that:

- every metric used by the plan or interface contracts is defined
- `confirmed` metrics have `formula_ref`
- `delegated` or `unresolved` metrics have `required_decision`
- ratio metrics have numerator and denominator
- CDF/distribution metrics have x-unit, y-unit, and zero point

Before finalizing `research_context.md`, check that:

- every exported baseline, workload, and metric ID used by the plan or
  contracts has a source-backed entry or a confirmed non-research source
- `last_verified_at` is present
- source links and venue/year metadata stay out of `experiment_plan.md`
