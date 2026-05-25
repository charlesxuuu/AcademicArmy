---
name: academic-army-experiment-plan
description: >-
  Create two Markdown files for a venue-calibrated empirical evidence plan: an English experiment_plan.md for downstream AI planning, execution, analysis, figure, writing, and review agents, plus a user-language language-suffixed experiment_plan_explanation Markdown file for human audit. Use academic_army_mcp_tools.deepresearch, canonical Codex tool name mcp__academic_army_mcp_tools__deepresearch, for live target-venue, recent-literature, baseline, dataset, metric, benchmark, exemplar-paper, artifact, and reviewer-context research. Consumes a research idea and/or paper_blueprint.md, then converts paper goals, claims, contribution posture, novelty boundary, and evidence posture into claim-to-evidence maps, Experiment Cards, dataset/workload choices, comparator choices, metric choices, ablations, robustness tests, efficiency evaluation, interpretation rules, figure/table interfaces, and downstream execution interfaces.
---

# Academic Army Experiment Plan

## Output Contract

This skill produces two Markdown files.

### File 1: `experiment_plan.md`

This file is an English **Venue-Calibrated Empirical Evidence Plan**.

It is written for downstream AI planning, execution, result-analysis, figure-planning, writing, and review-preparation agents. It specifies the empirical evidence system needed to support the paper's claims:

- experiment plan identity
- empirical evidence thesis
- claim-to-evidence map
- venue- and field-calibrated evaluation posture
- experiment inventory
- experiment cards
- execution dependency graph
- result interpretation rules
- figure and table interface
- downstream interfaces

The plan fixes concrete experimental commitments when current literature and user inputs support them: datasets, workloads, traces, benchmarks, baselines, comparator classes, metrics, ablation axes, robustness tests, stress tests, efficiency/scalability measurements, fairness controls, interpretation rules, and output artifacts.

It remains an experiment-planning document. It specifies what an execution agent must implement fairly; it does not become a shell-command script, training launcher, manuscript draft, reviewer response, artifact checklist, or project-management TODO list.

### File 2: `experiment_plan_explanation.<lang>.md`

This file is a user-language validation companion.

It helps the user audit whether `experiment_plan.md` is reasonable by showing:

- which inputs, constraints, preferences, and pipeline assumptions the user has explicitly provided
- what the experiment plan is trying to prove
- how target-venue and recent-field norms shaped the plan
- how paper goals, claims, contribution posture, novelty boundary, and evidence posture become concrete evidence obligations
- why each important experiment, baseline, dataset/workload, metric, ablation, robustness test, efficiency test, and figure/table output exists
- how experiments support each other
- which evidence chains are fragile
- which unresolved strategic questions would change the plan or paper claim

Use the user's conversation language. Preserve technical terms, venue names, paper titles, dataset names, benchmark names, metric names, and method names in their original language when that improves precision.

## Required Research MCP

This skill's live research dependency is the `deepresearch` tool from the `academic_army_mcp_tools` MCP server.

Use the exact tool identity:

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical Codex MCP tool name, when exposed: `mcp__academic_army_mcp_tools__deepresearch`

All mentions of `deepresearch` in this skill refer to `academic_army_mcp_tools.deepresearch`.

Use `academic_army_mcp_tools.deepresearch` for current venue norms, recent nearest-neighbor papers, exemplar experiment patterns, baseline lists, dataset/workload norms, metric norms, benchmark protocols, artifact expectations, and reviewer-context pressure.

Evidence from built-in web search, browser tools, documentation search, or other MCP servers is supplemental and does not satisfy this skill's required live research dependency.

The final Markdown files should contain the experiment-level conclusions derived from this evidence, not tool-call logs or MCP implementation details.

## Recent Literature Policy

For actual experiment planning, recent nearest-neighbor papers dominate baseline, dataset, benchmark, metric, ablation, robustness, and reporting choices.

Use these source classes:

| Source class | Planning role |
|---|---|
| Recent evaluation exemplars | Choose current baselines, datasets, workloads, metrics, ablation norms, robustness tests, efficiency reporting, and result presentation. Prefer the last 2-3 years or latest 3 target-venue cycles; expand to the last 5 years only when needed and state why in the explanation. |
| Canonical technical exemplars | Establish method lineage, benchmark lineage, unavoidable classic baselines, or long-lived comparison anchors. Pair older anchors with recent nearest-neighbor papers. |
| High-impact historical papers | Extract experiment-design patterns such as mechanism proof, workload realism, tradeoff evidence, scalability evidence, and artifact-backed evaluation. They do not replace current reviewer-facing evaluation norms. |

Use old high-citation papers to learn patterns, not to freeze current baseline, dataset, or metric decisions.

## Confirmed User Context

Start `experiment_plan_explanation.<lang>.md` with a calibration section named `用户已明确的信息`, `Confirmed User Context`, or the natural equivalent in the user's language.

This section records only user-confirmed inputs, constraints, preferences, and pipeline assumptions. Include information such as:

- research idea
- upstream `paper_blueprint.md` or paper-blueprint outputs
- target venue, track, field, or subfield
- method or system description
- available implementation, data, benchmark, compute, hardware, annotation, simulator, deployment access, or other resources
- user-confirmed constraints and experiment preferences
- output file requirements
- downstream pipeline assumptions
- explanation language and readability preferences

Separate confirmed context from working assumptions. Use a short `Current Working Assumptions` subsection only when the plan must proceed despite missing strategic information.

The confirmed-context section belongs only in `experiment_plan_explanation.<lang>.md`. Keep `experiment_plan.md` focused on the formal empirical evidence specification.

## Confirmed Context Coverage Filter

Use the confirmed context ledger to filter user-facing strategic questions.

Before writing `用户仍需确认的实验战略问题`, `Remaining Strategic Experiment Questions`, or the natural equivalent, classify candidate questions:

| Classification | Output action |
|---|---|
| `covered_by_user_confirmation` | Treat the point as settled context and omit it from remaining questions. |
| `partially_covered` | Ask only the unresolved strategic remainder. |
| `conflicts_with_user_confirmation` | Revise the plan or mark the plan inconsistency in the explanation. |
| `delegated_to_downstream_skill` | Express the point as a downstream boundary, dependency, or execution interface. |
| `unresolved_strategic_question` | Include it as a remaining strategic question. |

Across iterative runs, move newly confirmed strategic points into the confirmed context ledger. As the ledger grows, remaining strategic questions should usually shrink unless the user changes the idea, venue, claim strength, resource constraints, or paper goal.

## Planning Granularity

This skill operates at experiment-planning granularity:

| Level | Scope |
|---|---|
| Level 2 input | Paper goals, claim posture, novelty boundary, evidence posture, and downstream experiment-planning interface from the paper blueprint. |
| Level 3 output | Concrete experiment families, experiment cards, baselines/comparators, datasets/workloads, metrics, controls, interpretation rules, figure/table interfaces, and execution dependencies. |
| Level 4 delegated | Shell commands, training scripts, exact hyperparameter sweeps, plotting code, data download commands, annotation task execution, manuscript prose, and reviewer-response text. |

Make concrete experimental commitments when live research and user inputs support them. When a choice remains unresolved, represent it as one of these formal plan objects:

- experiment dependency
- current evidence status
- selection criterion
- diagnostic branch
- revision implication

Represent artifact relevance as output artifacts inside Experiment Cards, figure/table interfaces, and downstream execution/result-analysis interfaces.

Represent reviewer pressure as `Venue/reviewer pressure addressed` inside each Experiment Card.

## Core Experiment-Planning Objects

### Claim-to-Evidence Map Object

For each claim, specify:

- claim statement
- required evidence
- experiment family
- required comparator class
- required dataset/workload class
- required metric family
- expected result pattern
- failure implication

### Experiment Card Object

Experiment Cards are the core output unit. For each experiment, specify:

- evidence objective
- claim supported
- venue/reviewer pressure addressed
- evaluation setting
- comparators
- metrics
- protocol
- controls and fairness constraints
- expected result pattern
- interpretation rule
- output artifact
- dependencies
- revision implication

The `Interpretation rule` field is mandatory. It states how to read strong, mixed, weak, and negative results so later agents do not overclaim from misleading or unfair comparisons.

### Fairness and Comparability Object

Every primary comparison and important ablation should state the fairness controls that make its results interpretable:

- data preprocessing and splits
- training or optimization budget
- model size or capacity controls
- tuning budget and search protocol
- hardware and runtime protocol
- random seeds, repeats, uncertainty reporting, or statistical tests
- workload generation or trace-selection controls
- deployment, simulator, or user-study controls when relevant

### Result Interpretation Object

Each major claim should have minimum evidence conditions, downgrade conditions, and redesign conditions. The plan should make clear when evidence supports the central claim, when the claim becomes narrower, and when the experiment design itself needs revision.

## Evidence Gathering

Use `academic_army_mcp_tools.deepresearch` for up to four live research passes when information is not already supplied:

1. **Venue and field norms.** Find the recent target-venue and subfield expectations for datasets, workloads, baselines, metrics, ablations, robustness, efficiency, reproducibility, and reporting.
2. **Closest recent papers.** Find nearest-neighbor papers from the last 2-3 years or latest 3 target-venue cycles; extract their experiment matrices, baselines, benchmarks, metrics, ablations, robustness tests, and failure analyses.
3. **High-impact exemplar patterns.** Extract reusable evidence-design patterns from canonical papers. Use them for plan architecture, not as a substitute for current baselines.
4. **Artifact, benchmark, and execution requirements.** Identify materials needed to support reported results: data, hardware, software, proof/model artifacts, test suites, benchmark logs, qualitative panels, traces, or evaluation images. Convert these into output artifacts and downstream interfaces.

## Workflow

### Step 1: Parse Request and Inputs

Extract research idea, upstream blueprint path/content, target venue/track/field, method or system description, available materials, resource constraints, user-confirmed experiment preferences, output language, and output directory.

When an upstream `paper_blueprint.md` is available, read it first and extract:

- top-level paper goal
- central research bet
- contribution goal
- novelty-boundary goal
- strategic claim posture
- strategic evidence posture
- scope-control goal
- experiment-planning interface
- fragile goals and downgrade conditions

### Step 2: Build Internal Research Brief

Create a compact internal brief with:

- one-sentence paper idea
- target venue and field
- paper type
- method or system under evaluation
- central empirical claim
- likely claim set
- novelty boundary
- available implementation/data/resource state
- decision-critical uncertainty
- output language and output paths

### Step 3: Gather Live Evidence

Use `academic_army_mcp_tools.deepresearch` to calibrate the plan to current target-venue and field norms. Prefer recent nearest-neighbor evidence for actual choices. Use canonical and high-impact evidence for design-pattern guidance and technical lineage.

If `academic_army_mcp_tools.deepresearch` is unavailable, proceed from user-provided and local evidence. Express live-research-dependent choices as current evidence status, selection criteria, dependencies, or revision implications inside the plan.

### Step 4: Compile `experiment_plan.md`

Use this structure:

```markdown
# Venue-Calibrated Experiment Plan: <Working Title>

## 1. Experiment Plan Identity
### 1.1 Research idea
### 1.2 Target venue and field
### 1.3 Upstream paper goals
### 1.4 Method or system under evaluation
### 1.5 Available implementation, data, and resource state
### 1.6 Experiment planning scope

## 2. Empirical Evidence Thesis
### 2.1 Central empirical claim
### 2.2 Acceptance-critical evidence
### 2.3 Novelty-protecting evidence
### 2.4 Practical-value evidence
### 2.5 Evidence boundary

## 3. Claim-to-Evidence Map

For each claim, specify claim statement, required evidence, experiment family, required comparator class, required dataset/workload class, required metric family, expected result pattern, and failure implication.

## 4. Venue- and Field-Calibrated Evaluation Posture
### 4.1 Recent exemplar pattern
### 4.2 Dataset / workload posture
### 4.3 Baseline and comparator posture
### 4.4 Metric and outcome posture
### 4.5 Ablation and diagnostic posture
### 4.6 Robustness, generalization, and stress-test posture
### 4.7 Efficiency, scalability, and resource posture
### 4.8 Qualitative, perceptual, user-study, or deployment posture

Include qualitative, perceptual, user-study, or deployment posture only when the paper's claim or venue requires it.

## 5. Experiment Inventory
### 5.1 Primary claim experiments
### 5.2 Baseline comparison experiments
### 5.3 Ablation experiments
### 5.4 Diagnostic mechanism experiments
### 5.5 Robustness and generalization experiments
### 5.6 Efficiency / scalability / resource experiments
### 5.7 Qualitative, visual, user-facing, or deployment experiments
### 5.8 Negative, failure-mode, or boundary experiments

## 6. Experiment Cards

For each experiment, use the Experiment Card format.

## 7. Execution Dependency Graph
### 7.1 Experiments that must run first
### 7.2 Experiments that depend on primary comparison results
### 7.3 Diagnostic branches triggered by weak or mixed results
### 7.4 Experiments that can be parallelized

## 8. Result Interpretation Rules
### 8.1 Minimum evidence for the central empirical claim
### 8.2 Minimum evidence for the novelty claim
### 8.3 Minimum evidence for the practical-value claim
### 8.4 Conditions for claim downgrade
### 8.5 Conditions for experiment redesign

## 9. Figure and Table Interface
### 9.1 Main paper figures implied by experiments
### 9.2 Main paper tables implied by experiments
### 9.3 Supplementary figures and tables
### 9.4 Result summaries required by writing/planning agents

## 10. Downstream Interfaces
### 10.1 Experiment-execution interface
### 10.2 Result-analysis interface
### 10.3 Figure-planning interface
### 10.4 Paper-writing interface
### 10.5 Review-preparation interface
```

Use this Experiment Card format:

```markdown
### E<n>. <Experiment title>

**Evidence objective.**  
State what this experiment must prove.

**Claim supported.**  
State which paper claim, contribution, novelty boundary, or practical-value argument this experiment supports.

**Venue/reviewer pressure addressed.**  
State which target-venue review concern this experiment is designed to satisfy.

**Evaluation setting.**  
Specify dataset, benchmark, trace, workload, scene set, user population, deployment setting, simulation environment, or data-generation protocol.

**Comparators.**  
Specify named baselines when current literature supports them. Otherwise specify comparator classes and selection criteria.

**Metrics.**  
Specify primary metrics, secondary metrics, efficiency/resource metrics, uncertainty/statistical reporting, and direction of improvement.

**Protocol.**  
Specify the procedure at a level sufficient for a downstream execution agent to implement fairly.

**Controls and fairness constraints.**  
Specify training budget, model size, hardware, preprocessing, hyperparameter tuning budget, random seeds, workload generation, deployment controls, or other fairness controls.

**Expected result pattern.**  
State the result pattern that would support the claim.

**Interpretation rule.**  
State how to interpret strong, mixed, weak, or negative results.

**Output artifact.**  
State the expected table, figure, plot, log, qualitative panel, trace summary, statistical report, or result file produced by this experiment.

**Dependencies.**  
State required code, data, model, benchmark, hardware, annotation, simulator, deployment access, or previous experiment.

**Revision implication.**  
State how the experiment plan or paper claim changes if this experiment fails.
```

### Step 5: Compile `experiment_plan_explanation.<lang>.md`

Use this structure:

```markdown
# Experiment Plan Explanation: <Working Title>

## 0. 用户已明确的信息

## 1. 实验方案速览：这套实验要证明什么

## 2. 目标 venue 和近期论文的实验模式

## 3. 从论文目标到证据义务的推导

## 4. 逐项解释 experiment_plan 中的实验

## 5. Baseline、dataset、metric 的取舍解释

## 6. 实验之间如何相互支撑

## 7. 当前最脆弱的证据链

## 8. 用户仍需确认的实验战略问题

## 9. 已委派给后续执行/绘图/写作的问题
```

For each important experiment, first restate the formal plan content in the user's language, then explain:

1. the claim it supports
2. the paper goal or novelty boundary that generated the evidence obligation
3. the venue/reviewer pressure it addresses
4. why the dataset/workload is appropriate
5. why the baseline/comparator is fair
6. why the metric captures the intended outcome
7. how it relates to other experiments
8. how its result would affect the paper claim
9. what the user should audit

Use experiment titles, semantic names, and natural-language paraphrases as primary references. Section numbers are secondary locators. The explanation should be readable without artificial chains such as `E1 -> C2 -> M3 -> R4`.

## `academic_army_mcp_tools.deepresearch` Prompt Shape

Use this prompt shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a venue-calibrated empirical evidence planner for a research paper.

Return evidence for converting paper claims and paper goals into a concrete experiment plan.

Research brief:
[RESEARCH_BRIEF]

Target venue and field:
[VENUE_AND_FIELD]

Return four sections:

1. Recent venue and field evaluation norms
   Summarize current reviewer-facing expectations for datasets, workloads, traces, benchmarks, baselines, metrics, ablations, robustness/generalization/stress tests, efficiency/scalability/resource reporting, qualitative/user/deployment evidence when relevant, and result presentation.

2. Closest recent papers
   Identify nearest-neighbor papers from the last 2-3 years or latest 3 target-venue cycles. Extract their experiment matrix, baselines, datasets/workloads, metrics, ablations, robustness tests, efficiency measurements, failure analysis, and reporting style.

3. Canonical and high-impact experiment-design patterns
   Identify canonical or high-impact papers only insofar as they teach evidence-design patterns, method lineage, benchmark lineage, or unavoidable classic baselines. State how each pattern should influence this plan without replacing recent norms.

4. Artifact, benchmark, and execution interface expectations
   Identify data, software, hardware, proof/model, simulator, trace, test-suite, benchmark, qualitative panel, evaluation-image, or statistical-report artifacts needed to support the planned results.

For each source, include title, venue/year when available, source link, relevance to the proposed paper, and the lesson for experiment-plan design.

Use concise evidence-facing prose.
```

## Research Tool Identity Checklist

Before using live research evidence, confirm that it came from `academic_army_mcp_tools.deepresearch` or the canonical Codex MCP tool name `mcp__academic_army_mcp_tools__deepresearch`.

If `academic_army_mcp_tools.deepresearch` is unavailable, express the affected choices as current evidence status, selection criteria, dependencies, diagnostic branches, or revision implications inside the outputs.

## Final Quality Checklist

Before finalizing `experiment_plan.md`, check that:

- the file reads as a formal empirical evidence specification
- concrete baseline, dataset/workload, metric, ablation, robustness, and efficiency choices are fixed when evidence supports them
- each claim maps to required evidence, experiment family, comparator class, dataset/workload class, metric family, expected result pattern, and failure implication
- each Experiment Card contains every required field
- every primary comparison has fairness controls
- every major claim has interpretation and downgrade rules
- experiment dependencies and diagnostic branches are explicit
- figure/table outputs are specified as interfaces for later agents
- uncertainty appears as dependency, current evidence status, selection criterion, diagnostic branch, or revision implication
- artifact relevance appears as output artifact, figure/table interface, or downstream interface

Before finalizing `experiment_plan_explanation.<lang>.md`, check that:

- the file reads as a human audit companion in the user's language
- the file starts with user-confirmed context
- confirmed context records only information explicitly provided by the user
- working assumptions are separated when needed
- important experiments and choices are restated before they are explained
- recent venue/field evidence is summarized as design rationale, not as tool logs
- explanation references use experiment titles and semantic names, not artificial traceability codes
- remaining questions ask only unresolved strategic questions that would change the plan or claim
- downstream execution, plotting, analysis, and writing details are delegated cleanly

When writing a machine-readable summary for validation, use `assets/experiment_plan_schema.yaml` and optionally run:

```bash
python scripts/validate_experiment_plan.py <experiment-plan-summary.json>
```
