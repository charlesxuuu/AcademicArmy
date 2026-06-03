---
name: academic-army-experiment-plan
description: >-
  Create a strategic, evidence-driven academic experiment plan from a research
  idea, paper_blueprint.md, paper claims, storytelling blueprint, target venue,
  existing results, prior plans, or revision feedback. Produces exactly two
  Markdown files: an English AI-facing experiment_plan.md and a Chinese
  human-facing experiment_plan.explain.md. Uses
  academic_army_mcp_tools.deepresearch for live target-venue, influential-paper,
  baseline, dataset/workload, metric, artifact, autoresearch, and reviewer
  expectation research before making claim-to-evidence planning choices.
---

# Academic Army Experiment Plan

## Contract

Create a strategic experiment plan for an academic paper. The plan is for later
AI skills that will implement code, run experiments, plan figures, and write
paper sections. This skill designs the evidence strategy; it does not execute
experiments, write code, fabricate results, prescribe shell commands, or produce
final figures.

Create exactly two Markdown files in the requested output directory:

1. `experiment_plan.md`
   - English.
   - AI-facing.
   - Contains only the strategic experiment plan.
   - Uses stable experiment names, registries, and fields that downstream skills
     can inherit.

2. `experiment_plan.explain.md`
   - Chinese.
   - Human-facing.
   - Explains why the experiment portfolio is reasonable for the paper.
   - Starts with the concrete inputs and artifacts actually read.
   - Explains choices from the paper thesis, blueprint, target venue, live
     research, existing evidence, and storytelling needs.

Do not create `experiment_plan_explanation.<lang>.md`. Do not put provenance,
source summaries, user-facing review notes, or skill-internal process comments
inside `experiment_plan.md`.

## Required Research

Use `academic_army_mcp_tools.deepresearch` for every nontrivial plan or revision
after local paper/artifact context is available.

- Server: `academic_army_mcp_tools`
- Tool: `deepresearch`
- Canonical MCP name when exposed:
  `mcp__academic_army_mcp_tools__deepresearch`

Ask deepresearch for concise planning lessons, not a literature review. Include:

- current or recent target-venue experiment expectations
- high-impact or high-citation papers from the target venue and adjacent top
  venues such as SIGGRAPH, CVPR, SIGCOMM, NSDI, INFOCOM, MMSys, CHI, NeurIPS,
  ICML, ICLR, ACL, or domain-specific venues when relevant
- recent methods, datasets, workloads, baselines, metrics, benchmarks, artifacts,
  and result-presentation patterns in the paper's subfield
- motivation or design-insight experiment patterns that make the core intuition
  visible before full-system evaluation
- autoresearch, scientific-discovery, paper-writing-agent, benchmark, and
  experiment-automation workflow lessons when they improve the skill's planning
  behavior or handoff structure

For each live-research anchor that changes the plan, record this in
`experiment_plan.explain.md`:

- `source`: title and link
- `date`: visible publication, submission, event, metadata, or page date
- `venue_status`: one of `official_proceedings`, `arxiv_only`,
  `project_page_claim`, `secondary_metadata`, or `classic_background`
- `影响到的规划决定`: the baseline, metric, workload, experiment placement,
  evidence style, artifact expectation, or claim boundary it changed

Use `official_proceedings` only when the venue is confirmed by conference,
proceedings, publisher, DOI metadata, or official venue pages. Use
`arxiv_only` for arXiv records. Use `project_page_claim` for author/lab/project
claims not confirmed elsewhere. Use `secondary_metadata` for aggregators or
institutional pages. Use `classic_background` for older foundational precedents.

## Context Acquisition

Read local and supplied context before planning.

1. Read `paper_blueprint.md` first when present.
2. Read prior `experiment_plan.md`, prior `experiment_plan.explain.md`,
   previous explanation variants, preliminary results, revision feedback, and
   current artifact directories when the task is a revision or evolution.
3. If the target artifact path is a directory, enumerate it and read every
   Markdown file under it before judging or revising the produced artifact.
4. When invoked through a metaskill or runner-task workflow, read the relevant
   metaskill, task file, or pasted design goals when available.
5. Use MCP resource fallbacks only when local shell/file access is unavailable
   and a suitable repository-file MCP resource exists.

Treat access failures as provenance facts, not as evidence about the plan. A
shell, MCP, permission, sandbox, or path error means the contents could not be
read through that channel; it does not mean the artifact is absent or defective.
Retry through the available local channels before asking the user to paste
anything.

Ask for pasted contents only when all are true:

- the required local contents cannot be read after available local and MCP paths
  have been tried
- the missing contents are indispensable to the thesis, revision, or artifact
  judgment
- a defensible plan or revision cannot be inferred from already available
  context
- the request names the smallest necessary files or excerpts

Do not use live research as a substitute for unavailable paper blueprints, prior
artifacts, metaskill text, or revision artifacts. Use live research to improve
methodology, baselines, metrics, and evidence style after the project-specific
context has been acquired or explicitly bounded.

For repeated access failures, return a concise structured request:

- `missing_required_contents`: exact file paths and directories
- `attempts_already_made`: shell, artifact listing, MCP resources/templates, or
  other attempted channels
- `why_no_revision_can_be_inferred`: which missing contents control the plan
- `paste_bundle_request`: copy-ready request for the missing Markdown files and
  metaskill text

If feedback only says another reviewer could not inspect local files, treat it
as access/provenance feedback. Read the files yourself when possible. If you can
read them, do not ask the user to paste them and do not change experiments,
baselines, workloads, or metrics from that access report. If an artifact or
skill revision is still needed, limit it to provenance, file-contract,
readback, or missing-context instructions.

## What To Extract

From the paper blueprint or supplied context, extract:

- paper goal, title, field, subfield, and target venue
- central research bet and novelty boundary
- main claims and expected reviewer concerns
- storytelling posture: motivation, method insight, main evidence, claim
  boundary, and reader journey
- required or preferred datasets, workloads, baselines, metrics, hardware,
  traces, code, artifact, or deployment access
- known constraints: compute, privacy, data access, unavailable baselines,
  human-subject constraints, deadline, target track, or reproducibility needs
- existing evidence: preliminary numbers, pilot studies, prior figures, logs,
  notes, old experiment plans, reviews, rebuttal feedback, or artifact feedback

Infer missing nonblocking details from the blueprint, venue norms, live research,
and paper goals. Ask only when the missing fact blocks a defensible plan.

## Decision Sufficiency Policy

Make goal-oriented choices. Do not transfer obvious decisions to the user.

When user input, the blueprint, existing evidence, and deepresearch make one
choice clearly better for the paper, write that choice into `experiment_plan.md`
and explain the reasoning in Chinese in `experiment_plan.explain.md`.

Keep open validation items only when all are true:

- the information cannot be inferred reliably from current inputs or live
  research
- the choice materially changes experiment objectives, claim coverage, workload
  scale, baseline fairness, ethics, or story placement
- downstream skills cannot proceed sensibly without inheriting the uncertainty

Do not create broad lists of "questions to validate". Represent nonblocking
unknowns as assumptions, dependencies, optional claim-expansion modules, or
handoff notes. As user-confirmed content and research accumulate, open items
should shrink.

## Strategic Plan Boundary

`experiment_plan.md` should include:

- experimental thesis, primary comparison, and operating conditions
- venue/storytelling evidence posture
- claim-to-evidence map
- workload or dataset registry
- metric registry
- baseline registry
- experiment objectives organized by evidence role
- ablation, sensitivity, robustness, and claim-boundary objectives when needed
- optional claim-expansion modules for broader scope
- main-paper versus supplemental presentation intent at a strategic level
- objective dependency graph

`experiment_plan.md` should not include:

- source summaries or literature review prose
- confirmed-input ledger or user-facing explanation
- implementation owners
- shell commands, scripts, hyperparameter grids, exact run matrices, or code
- concrete output paths, logging schemas, manifest fields, or final figure files
- fabricated numeric results or claims that experiments have succeeded
- user reminders, disclaimers, or sections such as `Assumptions to validate`,
  `Artifact cautions`, or `Do not assume reviewers will run code`

Use logical handles for outputs, such as `substitution_surface`,
`main_qoe_table`, or `stress_regime_matrix`. Later skills choose concrete file
names, logging formats, implementation details, and plotting layouts.

## Objective Design

Start from paper claims, not a generic evaluation checklist. For each experiment
objective, decide:

- which claim it supports
- which reviewer concern it answers
- where it belongs in the paper story: motivation, method insight, main
  evaluation, mechanism/ablation, robustness, generalization, contribution
  boundary, human/perceptual evidence, deployment realism, cost/scalability, or
  reproducibility
- what evidence output downstream plotting/writing should produce
- how readers should interpret the result
- which workloads, metrics, baselines, controlled factors, and comparators are
  necessary
- which choices are strategic and which belong to execution skills

Motivation and design-insight experiments should make the core intuition visible
early. Use them to show an existing-system defect or a core-mechanism feasibility
signal before full-system evaluation. Their planned result should be immediately
readable: a curve separation, small table, heatmap, qualitative grid, timeline,
breakdown, representative case, or before/after panel.

Merge objectives that do not have a distinct claim, story role, reader takeaway,
or primary evidence output. Represent secondary needs as metric slices,
reporting views, or shared protocols.

## Registries

Define shared registries once and reference IDs in objectives.

### Workload or Dataset Registry

Separate:

- `Required workloads/datasets`: committed by user input, blueprint, existing
  evidence, or live-research-selected venue protocol.
- `Scope-extension candidates`: broaden scene, data, benchmark, substrate,
  device, deployment, user-study, or contention claims.

Name workload classes or dataset families unless exact datasets are confirmed or
venue norms make a dataset clearly required. Do not use fallback phrases like
`when available` in the main plan; place non-required items under scope-extension
candidates or open items in the explanation.

### Metric Registry

Group metrics by evidence role, for example:

- primary claim quality/effectiveness
- latency/deadline/responsiveness
- cost/resource/efficiency
- robustness/stress/generalization
- mechanism/control/action behavior
- statistical reporting
- human/perceptual signal, when relevant

Objectives reference metric IDs only. Do not repeat definitions inside every
objective.

### Baseline Registry

Use compact entries:

```markdown
- `baseline_id`:
  - Burden: minimum | diagnostic | optional_expensive
  - Baseline role: canonical | recent_strong | simple | ablated_self | status_quo | oracle | deployment
  - Comparison purpose:
  - Fairness principle:
```

Use baseline ladders:

- canonical baselines expected by reviewers
- recent strong baselines from live research
- simple baselines that test whether complexity is justified
- ablated self-baselines that isolate mechanism
- status-quo or deployment baselines for systems papers
- oracle or upper-bound baselines only when they clarify headroom

Objectives own baseline usage through their `Comparators` field. The registry
defines each baseline once.

## Positive Evidence Language

Write the main plan as a positive evidence specification. Use fields such as:

- `Evidence goal`
- `Evidence scope`
- `Evidence role`
- `Story placement`
- `Reviewer concern answered`
- `Presentation intent`
- `Reader takeaway`
- `Claim calibration output`
- `Expected evidence outputs`
- `Handled by later skills`

Use positive limitation language: `limitation regime`, `unsupported regime`,
`claim boundary`, `stress sensitivity`, and `adaptation attribution`. Use
`failure` only for explicit diagnostic objectives where a failure analysis
artifact is part of the evidence.

For engineering papers, do not organize the plan around fallback paths or weak
results. Plan how the core intuition should be shown and verified. Express risks
as dependencies, open variables, stress regimes, or claim-boundary objectives.

## `experiment_plan.md` Template

```markdown
# Experiment Plan: <Paper/System Name>

## 1. Experimental Thesis

- Experimental thesis:
- Primary comparison:
- Operating conditions:
- Venue/story evidence posture:

## 2. Claim-to-Evidence Map

| Claim | Reviewer Concern | Evidence Objective | Story Placement | Expected Evidence Output |
|---|---|---|---|---|

## 3. Workload and Dataset Registry

- Required workloads/datasets:
- Scope-extension candidates:

## 4. Metric Registry

- `<metric_id>`:

## 5. Baseline Registry

- `<baseline_id>`:
  - Burden:
  - Baseline role:
  - Comparison purpose:
  - Fairness principle:

## 6. Resource, Cost, and Reproducibility Principles

- Resource/cost reporting:
- Statistical reporting:
- Artifact/reproducibility principle:

## 7. Core Experiment Objectives

### <Experiment Name>

- Story placement:
- Evidence goal:
- Claims supported:
- Reviewer concern answered:
- Evidence scope:
- Evidence role:
- Workloads/datasets:
- Controlled factors:
- Comparators:
- Metrics:
- Presentation intent:
- Expected evidence outputs:
- Reader takeaway:
- Claim calibration output:
- Handled by later skills:
- Dependencies:
- Priority:

## 8. Optional Claim-Expansion Modules

### <Module Name>

- Module type: claim_expansion_module
- Scope expanded:
- Activation condition:
- Use objective fields only when the module is activated.

## 9. Objective Dependency Graph

- <experiment/output> -> <experiment/output>:
```

Omit empty sections. Keep identifiers natural and readable; avoid abstract ID
systems such as `c1`, `c2`, `b1`, or `m1` unless the source paper already uses
them.

## `experiment_plan.explain.md` Template

Write this file in natural Chinese. English paper titles, venue names, method
names, datasets, benchmarks, and technical terms may remain in English when that
is clearer.

```markdown
# 实验计划说明：<论文/系统名>

## 用户已经明确的内容

记录本轮实际读取的本地文件、用户指令、论文蓝图、旧计划、反馈、工件目录和实时调研入口。

## 论文核心出发点

解释这篇论文想让审稿人相信什么，以及为什么实验必须围绕这些论点组织。

## 实时调研如何影响实验取舍

| 来源 | 日期 | venue_status | 影响到的规划决定 |
|---|---:|---|---|

## 实验故事线

用自然语言说明 motivation、method insight、main evaluation、ablation、
robustness、boundary、artifact evidence 如何串起来。

## 为什么选择这些实验

逐个实验解释：它支撑哪个 claim、解决哪个 reviewer concern、放在论文哪个叙事位置、预期结果如何帮助读者理解核心思想。

## 为什么选择这些基线

说明 canonical、recent strong、simple、self-ablation、status quo、oracle 等基线各自排除哪个疑虑。

## 为什么选择这些指标和工作负载

解释指标和 workload 如何服务论文论点，不要只解释字段含义。

## 结果展示策略

说明哪些结果适合主文，哪些适合补充材料；只做战略层面的图表/表格/案例意图，不设计最终图。

## 仍需继承的开放变量

只列真正影响实验规模、claim 覆盖、伦理/数据访问、baseline 公平性或 story placement 的未知项，并说明为什么当前信息不足以决定。
```

The explanation is for user confirmation, not for downstream execution. It
should let the user identify whether a questionable experiment comes from the
core thesis, target-venue prior, live-research pattern, or an inference step.
When access or provenance issues affect a revision, record only the relevant
readback facts in this explanation: what files were actually read, what could
not be read, and which planning choices were left unchanged because the feedback
was access-only. Do not copy full artifact contents into the explanation unless
the user explicitly asks for a pasted bundle.

## Workflow

1. Gather context and read required local files.
2. If local context needed for the thesis or revision is unavailable, stop with
   the structured missing-content request.
3. Run deepresearch for venue norms, influential papers, current baselines,
   workloads, metrics, result-presentation patterns, and relevant autoresearch
   workflow lessons.
4. Build a sufficiency ledger for yourself: resolved by user, blueprint,
   existing evidence, live research, or clear inference; downstream execution
   detail; genuinely open variable.
5. Normalize the paper into an experimental thesis, primary comparison,
   operating conditions, and venue/story evidence posture.
6. Build the claim-to-evidence map before writing individual objectives.
7. Define workload, metric, and baseline registries once.
8. Write core objectives and optional claim-expansion modules.
9. Write the Chinese explanation as causal rationale, not as field definitions.
10. Run the lint rules below before finalizing.

## Revision Behavior

When revising an artifact:

- Read all Markdown files in the artifact directory before deciding what to
  change.
- Classify feedback as substantive, access/provenance, file-contract,
  over-defensive/open-question, language/filename, or non-controlling.
- Apply a reviewer access-failure gate before changing plan content. If the
  feedback only says another reviewer could not inspect local files, shell or
  fallback tools failed, or the user should paste files, and it names no
  concrete defect in the artifact contents, classify it as access-only feedback.
  Then inspect `experiment_plan.md` and `experiment_plan.explain.md` yourself
  through available local/MCP channels. If you can read them and they satisfy
  the contract, report that no artifact-content change is implied. Do not revise
  experiment objectives, output schema, filenames, language split, or open
  variables solely from access-only feedback.
- Stop repeated access-only feedback loops. When the same access-only report
  recurs and this agent can read the artifacts, treat it as non-controlling
  after local inspection. Do not keep adding access-handling layers, changing
  plan/schema content, or asking for pasted files. Report that the local files
  are readable in this session and that no substantive artifact defect was
  provided.
- Make the smallest skill or artifact change that addresses the feedback.
- If feedback says files could not be read, first try to read those exact files
  locally and through available MCP fallbacks. If you can read them, classify
  the feedback as access/provenance, document that fact in the explanation or
  final response, and avoid any paste request.
- If feedback asks the user to paste artifact contents because another agent's
  tools failed, do not echo that request unless your own local and MCP access
  also fail and the contents are indispensable.
- If access-only feedback reveals that the skill prompt encouraged premature
  paste requests or unclear file provenance, revise the skill's
  missing-context/readback instructions rather than the experiment portfolio.
- Do not change experiments, baselines, workloads, or metrics based only on an
  access failure report.

## Lint Rules

Before finalizing, check:

- Exactly two Markdown files are produced: `experiment_plan.md` and
  `experiment_plan.explain.md`.
- `experiment_plan.md` is English-only and contains only the strategic plan.
- `experiment_plan.explain.md` is Chinese-first and begins with actual inputs
  read.
- The main plan defines workload/dataset, metric, and baseline registries once.
- Objectives reference registry IDs rather than redefining baselines or metrics.
- Every baseline has `Burden: minimum | diagnostic | optional_expensive`.
- Every objective has claim support, story placement, reviewer concern,
  presentation intent, expected evidence output, reader takeaway, and priority.
- Motivation/design-insight experiments make the core intuition visible before
  full evaluation when the paper needs them.
- Main-paper versus supplemental presentation intent is strategic, not a final
  figure design.
- Open variables appear only in the explanation and only when they materially
  affect plan quality.
- Facts resolved by user input, blueprint, existing evidence, live research, or
  clear inference are not restated as user questions.
- Every live-research anchor in the explanation has source, date,
  `venue_status`, and the planning decision it changed.
- The plan contains no source prose, literature review, user-facing warnings,
  shell commands, code, fabricated results, concrete output paths, logging
  schemas, manifest fields, implementation owners, or exact run scripts.
- Objectives with overlapping claims, workloads, metrics, comparators, and
  outputs are merged or represented as reporting views.
- Access-failure feedback is handled as provenance/file-contract feedback, not
  as substantive experiment-plan criticism.
- Access-only review feedback with no concrete artifact-content defect does not
  trigger output-schema, filename, language-boundary, experiment-objective, or
  open-variable changes.
- Repeated access-only feedback is stopped as non-controlling after the current
  agent verifies that the artifacts are locally readable and no content defect
  is supplied.
- Paste requests are only issued after the access threshold is met and name the
  smallest indispensable files or excerpts.
