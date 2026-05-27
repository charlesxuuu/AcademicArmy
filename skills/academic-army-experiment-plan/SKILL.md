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
   - Uses the user's conversation language for headings, table titles, field
     labels, and body text.
   - Human-facing confirmation companion.
   - Explains how the plan follows from user inputs, the paper blueprint,
     existing evidence, live research, and the paper's core thesis.

Create an optional `experiment_plan_execution_contract.md` only when the user
explicitly asks for execution contracts or when an existing workflow artifact
already requires one. Put metric implementation handles, logging schemas,
output file paths, manifest fields, owners, and concrete artifact paths there,
not in `experiment_plan.md`.

The explanation file should also make the run reviewable. At the start of the
confirmation ledger, record the concrete local or supplied inputs that were
actually read, including paper blueprint paths, prior plan/explanation files,
artifact feedback, and live-research anchors. This provenance belongs only in
the explanation file; never place it in `experiment_plan.md`.

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
- `venue_status`: one of `official_proceedings`, `arxiv_only`,
  `project_page_claim`, `secondary_metadata`, or `classic_background`
- `why_it_affects_this_plan`: the planning decision it changes

Use `official_proceedings` when the venue is confirmed by conference,
proceedings, publisher, or DOI metadata. Use `arxiv_only` when the visible
metadata is an arXiv record or arXiv paper. Use `project_page_claim` when a
venue or artifact claim appears only on a project, lab, or author page. Use
`secondary_metadata` for aggregator or institutional metadata pages that are not
primary proceedings records. Use `classic_background` for older foundational
baselines or precedent papers that explain evaluation lineage but do not
establish current protocol freshness.

Prefer official proceedings, arXiv records, DOI/publisher pages, conference
pages, and author-hosted PDFs. Secondary metadata may support background
context, but it should not be used as the highest-confidence venue status when a
primary source is available. Keep current 3DGS/volumetric evidence anchors
separate from classic ABR or networking background anchors in the explanation
file.

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

## Context Acquisition and Missing-Input Handling

Before planning or revising, actively gather the required local context instead
of assuming it is unavailable.

1. Read `paper_blueprint.md` first when present.
2. Read prior `experiment_plan.md`, prior explanation files, revision feedback,
   and current artifact directories when the task is a revision or evolution.
   If the artifact path is a directory such as
   `output/evolve-academic-army-experiment-plan`, enumerate it and read every
   Markdown file under it before judging the produced artifact.
3. When invoked through a metaskill/evolution workflow, read the relevant
   metaskill or runner-task file if its path is provided or obvious from the
   task.
4. Use MCP fallback tools when local shell/file access is unavailable and a
   suitable repository-file MCP resource is available.

If a required input cannot be read after the available local and MCP paths have
been tried, stop before producing or revising the plan and ask the user to paste
the missing contents. Name the exact missing files or directories. Do not
generate placeholder plans, simulated reviews, or broad generic advice from
memory when the missing input controls the paper thesis, objective structure,
or artifact revision.

Treat local-access failures such as shell spawn/setup errors, empty MCP
resource listings, missing repository templates, or cancelled repository
fallbacks as evidence that the artifact contents are unavailable in that run.
Live research and `deepresearch` can supply field knowledge, but they cannot
replace missing local files such as a metaskill, blueprint, prior plan, or
artifact directory.

For repeated access-failure feedback, do not keep cycling through the same
attempted reads or produce a new non-review. Give a concise stop response with:

- `missing_required_contents`: exact file paths and directories needed
- `attempts_already_made`: local shell, artifact directory listing, MCP
  resources/templates, repository MCP fallback, or other attempted channels
- `why_no_revision_can_be_inferred`: the missing contents control artifact
  language, content gaps, redundancy checks, or skill optimization decisions
- `paste_bundle_request`: a copy-ready request for the metaskill text and all
  Markdown files under the named artifact output directory

If feedback only says the reviewer lacked access to local files, treat that as
an access/provenance issue rather than a substantive experiment-plan critique.
Resolve it by reading the named files yourself when possible; otherwise ask for
their contents. Do not change objectives, baselines, workloads, or metrics based
solely on a missing-context report.

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

For revision tasks, add a compact `artifact_feedback_consumed` entry in the
ledger. Separate:

- substantive feedback that changes the plan
- access/provenance feedback that only changes how inputs are documented
- non-controlling feedback that does not affect the experiment strategy

This prevents "could not inspect the artifact" messages from being converted
into artificial open experiment questions.

## Strategic Plan Boundary

`experiment_plan.md` should include:

- experimental thesis, primary comparison, and operating conditions
- claim-to-evidence map
- workload registry
- metric registry
- baseline registry
- core objective definitions
- optional claim-expansion objective definitions when they affect scope
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
- ID-only summaries that duplicate registries

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

Use positive limitation language. Prefer `limitation regime`, `unsupported
regime`, `claim boundary`, `stress sensitivity`, and `adaptation attribution`.
Use `failure` or `failure-mode attribution` only when the objective is explicitly
diagnostic and the paper needs a failure diagnosis artifact.

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
- contribution boundary
- human/perceptual evidence
- deployment realism
- cost/scalability/reproducibility protocol

Merge objectives that do not support an independent claim, story role, or
primary evidence output. Represent secondary needs as reporting views, metric
slices, or shared protocol entries.

Separate objectives into:

- `core_objectives`: required evidence for the current paper thesis and claim
  scope.
- `optional_claim_expansion_objectives`: conditional scope-calibration modules
  that expand supported scene, workload, substrate, deployment, or contention
  claims.

Use `optional_claim_expansion_objectives` for workloads such as new dynamic
scene classes, mobile-device profiles, multi-client contention, deployment
profiles, or extra dataset families when they broaden the claim rather than
support the core thesis. Mark their trigger as `claim_expansion_module` and
state which claim scope they would expand.

For substrate-boundary or adaptation-attribution objectives, use the story role
`mechanism/ablation; contribution boundary`. Put generalization,
cost/scalability, and deployment scope into optional claim-expansion modules
unless those claims are part of the confirmed core thesis.

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
  - Burden: minimum | diagnostic | optional_expensive
  - Comparison purpose:
  - Fairness principle:
```

Keep observation access, action space, resource budget, and implementation owner
out of the main plan unless they change the strategic comparison. Put those
details in the optional execution contract when needed.

Objectives own baseline usage through their `Comparators` field. The baseline
registry defines each baseline family once and does not list objective usage.

Apply the baseline burden rule:

- `minimum`: small comparator set required to substantiate the core claim.
- `diagnostic`: comparator used to isolate mechanism, attribution, or claim
  boundary.
- `optional_expensive`: costly, hard-to-implement, or broad-scope comparator
  such as RL policies, complex oracle bounds, or full recent-system ports.

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

Use a workload registry, not an ID-only research context list. Add a compact
generated index only when the plan becomes long enough that downstream skills
would otherwise struggle to locate identifiers.

Name workload classes, not implementation commitments. For trace classes, use
phrasing such as `real, replayed, or collected if unavailable` unless the user,
blueprint, or existing evidence already confirms exact trace sources or new
data collection.

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

Use the smallest set of deepresearch passes needed. Ask for current protocols,
recent evidence patterns, motivation/design-insight patterns, and planning
commitments for this paper. Require each source to include title, link, date,
visible venue metadata, provenance category, relevance, and planning lesson.
Separate current field evidence from classic background precedent.

## Workflow

0. Gather required context. Read the paper blueprint, prior artifacts, provided
   feedback, and metaskill/runner-task files when they are part of the current
   request. If required contents cannot be accessed, ask for the exact missing
   contents before writing outputs. For artifact-review or skill-evolution
   requests, read the metaskill and every file in the named artifact output
   directory before deciding which skill instructions to change. If the same
   access failure has already been reported, return the structured
   `missing_required_contents` paste request and stop.
1. Build the explanation ledger in the user's language. Localize headings,
   table titles, and field labels. For Chinese, use headings such as
   `已确认的用户输入`, `论文蓝图已确认的信息`, `现有证据输入`,
   `本轮读取的工件与反馈`, `本轮使用的实时研究背景`,
   `Skill 推导出的规划承诺`, and `剩余开放规划项`.
2. Normalize the thesis into `Experimental thesis`, `Primary comparison`, and
   `Operating conditions`.
3. Build the claim-to-evidence map with only claim, objective, story role, and
   expected evidence output.
4. Define workload, metric, and baseline registries once. Avoid ID-only
   summaries unless the plan is long enough to need a generated index.
5. Write required evidence under `Core Objectives`. Put conditional scope
   modules under `Optional Claim-Expansion Objectives` with `Module type:
   claim_expansion_module`, `Scope expanded`, and `Activation condition`.
6. Write the explanation causally. Include compact localized traceability
   tables for baseline families, metric families, workload classes, and open
   variables that affect experiment scale or claim coverage.

## `experiment_plan.md` Template

```markdown
# Experiment Plan: <Paper/System Name>

## 1. Experimental Thesis

- Experimental thesis:
- Primary comparison:
- Operating conditions:

## 2. Claim-to-Evidence Map

| Claim | Evidence Objective | Story Role | Expected Evidence Output |
|---|---|---|---|

## 3. Workload Registry

- Required workloads:
- Scope-extension workload candidates:

## 4. Metric Registry

- `<metric_id>`:

## 5. Baseline Registry

- `<baseline_id>`:
  - Burden:
  - Comparison purpose:
  - Fairness principle:

## 6. Resource, Cost, and Reproducibility Principles

- Resource/cost reporting:
- Reproducibility/artifact principle:

## 7. Core Objectives

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

## 8. Optional Claim-Expansion Objectives

### Optional Module 1: <Name>

- Module type: claim_expansion_module
- Scope expanded:
- Activation condition:
- Use the same objective fields as core objectives when the module is activated.

## 9. Objective Dependency Graph

- <objective/output> -> <objective/output>:
```

Omit empty optional fields. Keep the dependency graph short.

## `experiment_plan_explanation.<lang>.md` Template

Translate every heading, table title, and field label into the user's
conversation language. For Chinese, use Chinese headings rather than English.

```markdown
# <Localized title>: <Paper/System Name>

## <localized confirmed-input ledger sections>

## <localized current field and target-venue experiment patterns>

## <localized core experimental logic>

## <localized why these baselines are necessary>
| <baseline family> | <reviewer concern answered> | <link to plan> |

## <localized why these metrics are necessary>
| <metric family> | <claim or evidence role> | <link to plan> |

## <localized which workloads change scope>
| <workload class> | <scope decision affected> | <plan treatment> |

## <localized which open variables change experiment scale>
| <open variable> | <effect on experiment scale or claim coverage> |

## <localized derivation of each objective>

## <localized evidence chain across objectives>
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
- Every baseline has `Burden: minimum | diagnostic | optional_expensive`.
- Objective-level metric and comparator fields do not repeat registry
  definitions.
- Objectives use `Evidence scope`, `Evidence role`, and `Handled by later
  skills`.
- Substrate-boundary objectives use `mechanism/ablation; contribution boundary`
  unless generalization or deployment is part of the confirmed core thesis.
- `Expected evidence outputs` uses logical artifact names, not filenames.
- Workloads name strategic classes and do not commit to new trace collection or
  exact datasets unless confirmed.
- Open planning items appear only in the explanation file.
- A fact resolved by user input, blueprint, existing evidence, or live research
  is not restated as an open question.
- Every live-research anchor in the explanation has source, date,
  `venue_status`, and why it affects the plan.
- Venue labels are not upgraded beyond the source confidence available.
- `venue_status` uses only `official_proceedings`, `arxiv_only`,
  `project_page_claim`, `secondary_metadata`, or `classic_background`.
- The plan uses `limitation regime`, `unsupported regime`, and `claim boundary`
  instead of repeated failure language except in explicit diagnostic objectives.
- The explanation is causal and readable, not an administrative checklist.
- The explanation uses the user's language and begins with the confirmation
  ledger.
- The explanation names the concrete blueprint, prior artifacts, feedback, and
  metaskill/runner-task files that shaped the run, or explicitly says which
  required contents were unavailable and stops before fabricating a plan.
- Missing local artifact access is treated as provenance feedback, not as a
  reason to invent new experiment objectives or open research questions.
- Live research is not used as a substitute for unavailable repository files;
  it only supplies current external venue, baseline, dataset, metric, and
  reviewer-expectation context after the local paper/artifact inputs are known.
- Artifact-review revisions enumerate and read all Markdown files under the
  referenced output directory before making concrete skill changes.
- Repeated access-failure reviews return a structured missing-content request
  with paths, attempted channels, and paste-bundle instructions, instead of
  producing a generic critique or another paraphrase of the same failure.
- Each objective has a distinct claim, story role, or primary evidence output.
- Overlapping objectives are merged or represented as reporting views.
