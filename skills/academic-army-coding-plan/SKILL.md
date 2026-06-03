---
name: academic-army-coding-plan
description: >-
  Create an English coding_plan.md and a Chinese coding_plan.explain.md from a
  paper blueprint, experiment plan, repository context, candidate methods,
  baselines, datasets, metrics, and paper-result requirements. Use when Codex
  needs to translate research and experiment requirements into a detailed,
  readable implementation plan for downstream coding, with semantic module
  boundaries, replaceable method/baseline locations, staged CLI execution,
  paper-goal harnesses, separate functional tests, raw-first result exports,
  method-freeze protocol, relative-path commands, and mandatory pre-planning
  deepresearch.
---

# Academic Army Coding Plan

## Purpose

Create a planning package that lets a downstream coding skill implement a
research experiment system without redesigning the architecture.

Produce exactly two Markdown files in the requested output directory:

- `coding_plan.md`: English, AI-facing, and only the coding plan.
- `coding_plan.explain.md`: Chinese, human-facing, and only the explanation
  and decision rationale for the coding plan.

This skill writes planning artifacts only. Code implementation, plotting, paper
prose, and final figure/table formatting belong to later skills.

## Artifact Delivery

Always write both files to the requested output directory and read them back
before responding.

For outputs under `output/evolve-*`, include a dedicated `Review Handoff`
section in the final response after a concise validation summary. Paste the
complete read-back contents of both files under their relative path headings.
Evolve outputs are often reviewed outside the local filesystem, so the pasted
handoff is part of the deliverable, not a convenience summary.

Also include the same complete handoff when the user, reviewer, or evaluator
says the artifacts cannot be inspected locally, or when the user asks to paste,
inline, or include the artifact contents.

Treat artifact-access feedback as sticky for the next successful generation in
the same thread. If prior feedback says the reviewer could not inspect
`coding_plan.md` or `coding_plan.explain.md`, the next final response for this
skill must paste both complete files even when local read-back succeeds.
If artifact-access feedback recurs, keep the same rule and make the handoff
more prominent rather than adding local troubleshooting notes to the artifacts.

Use five-backtick fences for full-file handoffs so embedded command fences
remain readable:

````markdown
## output/.../coding_plan.md

`````markdown
<full coding_plan.md content>
`````

## output/.../coding_plan.explain.md

`````markdown
<full coding_plan.explain.md content>
`````
````

For evolve outputs, keep the files detailed enough to guide coding and compact
enough to paste completely. Prefer dense semantic tables, concise bullets, and
clear ownership rules over repeated boilerplate. If the full handoff would be
too long to paste, shorten the artifacts and read them back again; do not
replace the handoff with a paths-only or summary-only response.

When pasting an evolve handoff, paste the read-back file contents, not a
regenerated approximation. The final response should remain reviewable even if
the reviewer cannot access the filesystem at all.

## Output Style

Write both files so a reader can understand them through semantic names and
local context rather than a global numbering system.

Use:

- Semantic section names, module names, method names, harness names, test
  names, output paths, and natural short names.
- Short paragraphs and bullets.
- Tables when they clarify parallel entities.
- Numbered lists only for real sequence, such as implementation order,
  experiment stages, priority, or step-by-step commands.

Prefer names such as:

- `Candidate Method Selection Harness`
- `Full-System Trace Evaluation Harness`
- `Reference Lifecycle Stress Harness`
- `Data Loading Tests`
- `Metric Computation Tests`
- `Result Export Tests`
- `CLI Smoke Tests`

When the existing repository already uses short registry keys such as `H3` or
`B2`, preserve them only as aliases beside the semantic name. The semantic name
is the primary anchor in headings, tables, cross-references, and the Chinese
explanation. For example: `Full-System Trace Evaluation Harness (existing
alias: H3)`.

In `coding_plan.explain.md`, use natural Chinese sentences. Preserve English
method names, repository names, dataset names, benchmark names, metric names,
file paths, commands, and code identifiers when exact spelling matters. When
explaining a design choice, first summarize the corresponding plan content,
then explain why it was chosen.

## Workflow

### Gather Local Context

Read the user-provided `paper_blueprint` and `experiment_plan` first. Then
inspect nearby repository context when present:

- `paper_blueprint.explain.md`
- `experiment_plan.explain.md` or `experiment_plan_explanation.*.md`
- existing coding plans, implementation notes, and code overviews
- repository README files
- package metadata such as `pyproject.toml`, `package.json`,
  `requirements.txt`, `setup.py`, `Cargo.toml`, or equivalent
- existing `src`, `configs`, `scripts`, `tests`, `notebooks`,
  `experiments`, `data`, `runs`, and `artifacts` directories
- user-provided method lists, baseline lists, metric lists, compute
  constraints, dataset constraints, and output requirements

Use repository-relative paths in both output files. Treat the project root as
the working-directory anchor. If implementation code is nested under an output
directory, name that relative implementation root, such as `output/codebase`.

If the blueprint or experiment plan is missing after checking the user-provided
paths and obvious local paths, ask for the missing content before writing the
plan.

### Run Pre-Planning DeepResearch

Before drafting `coding_plan.md`, run
`academic_army_mcp_tools.deepresearch` unless the provided context already
contains a fresh lookup artifact covering the current paper domain, method
family, experiment style, and repository design questions.

A reusable lookup artifact should include:

- lookup topic or query
- sources or repository examples
- source date, release version, or commit hash when available
- takeaways about highly engineered related codebases
- design choices affected in the coding plan
- visible retrieval date or context

Use DeepResearch to inspect high-quality related codebases and benchmark
artifacts. Let the lookup choose relevant mature repositories, official
benchmark artifacts, evaluation harnesses, experiment frameworks, paper
artifacts, configuration systems, and result-logging conventions for the
current domain. Do not hardcode a fixed source list in the skill output.

Prompt shape:

```text
You are supporting a coding-plan generator for a research paper.

Research brief:
[paper goal, system, candidate methods, baselines, datasets, metrics,
experiment-plan requirements, and local repository context]

Return concise implementation-planning evidence:

- Highly engineered related repositories or official artifacts and how they
  structure modules, configs, registries, evaluation harnesses, tests, and
  result exports.
- Canonical implementation shape for the candidate methods and baselines.
- Current benchmark or dataset protocol details that affect loaders,
  evaluators, metrics, or comparators.
- Repository or artifact conventions worth matching.
- Harness implications from traditional test harnesses and modern evaluation
  harnesses: controlled inputs, drivers, fixtures, evaluator separation,
  metrics, raw result records, smoke/full protocols, frozen variables, and
  decision rules.
- Raw result fields needed for later tables, figures, and paper claims.
- Source table with title, link, date, version, or commit when visible; role;
  whether the takeaway is a confirmed source fact or inferred design pattern;
  and the planning decision it affects.
```

Put planning consequences in `coding_plan.md`. Put lookup topic, sources,
source dates or versions, takeaways, evidence type, affected design choices,
confidence, and remaining uncertainty in `coding_plan.explain.md`.

## Draft `coding_plan.md`

Write `coding_plan.md` as an engineering contract for the downstream coding
skill. Include the sections that apply to the project:

- scope and working-directory assumptions
- inputs read and planning assumptions
- environment setup and executable entry points
- repository alignment and implementation root
- core domain model and shared interfaces
- package layout and semantic module boundaries
- replaceable method and baseline placement
- workload, dataset, trace, and config placement
- metric definitions and decision rules
- staged experiment pipeline with reusable CLI commands
- harness structure for paper goals
- testing structure for functional correctness
- method selection and freeze protocol
- experiment execution matrix or staged run matrix
- raw-first result export contract
- derivation path from raw outputs to paper tables, figures, and claims
- implementation order for the downstream coding skill
- acceptance criteria
- assumptions and open coding questions

Use existing repository patterns when present. Extend the local architecture
instead of inventing a parallel system.

## Draft `coding_plan.explain.md`

Write `coding_plan.explain.md` as a Chinese explanation of the coding plan and
its decision rationale. Use Chinese headings and Chinese body text. Preserve
technical English identifiers when exact spelling is useful.

Explain:

- which local files or user-provided contents were read
- what requirements were extracted from the paper blueprint and experiment plan
- what DeepResearch found and how it affected the design
- why modules are separated this way
- why candidate methods and baselines are replaceable components
- why the experiment stages and CLI entry points are structured this way
- why each harness exists and what paper claim, method-selection question, or
  optimization question it supports
- why testing is separate from harness execution
- why raw-first exports support later plotting, tables, and writing
- why paths and commands are relative
- which assumptions remain and what they block
- how a downstream coding skill should use the plan

Recommended shape:

```markdown
# 编码计划说明：<Paper/System Name>

## 已读取输入与需求提取

## 预规划研究（DeepResearch）

## 主要架构决策

## 方法与基线放置理由

## 实验阶段设计理由

## Harness Structure 设计理由

## Testing Structure 设计理由

## 原始结果导出理由

## 工作负载范围决策

## 相对路径与仓库对齐说明

## 假设与不确定性

## 下游 Coding Skill 使用方式
```

This outline is a guide, not a numbering system. Add, merge, or rename sections
when semantic headings would be clearer.

## Planning Requirements

### Core Domain Model and Shared Interfaces

When the system has interacting loaders, replay, controllers, methods,
baselines, evaluators, harnesses, and exporters, include a shared-domain-model
section before module details.

For each shared type, specify:

- type name
- owning module path
- purpose
- key fields
- producers
- consumers
- raw export mapping when applicable

Use shared domain types to keep schemas consistent across loaders, methods,
evaluators, harnesses, and export writers.

### Methods and Baselines as Replaceable Modules

Map every candidate method, modified variant, baseline, and oracle to a
replaceable module boundary.

For each method or baseline, specify:

- semantic method name
- role, such as proposed candidate, candidate route, headline baseline,
  diagnostic baseline, ablation, calibration-only method, or oracle
- module path
- config path
- existing registry key, only as an alias when the repository uses one
- shared interface it implements
- raw outputs needed for comparison
- harnesses or experiment stages that use it

When two baselines overlap, explain the behavioral difference and why both are
included.

### Metrics and Decision Rules

For every metric used by a harness, method-selection rule, acceptance criterion,
or paper-output derivation, define:

- metric name
- definition
- unit
- direction: `higher_is_better` or `lower_is_better`
- computation procedure or formula
- numerator and denominator for ratio metrics
- raw required fields
- upstream metric dependencies when any
- derived outputs
- aggregation rule
- missing-data behavior
- harnesses and paper outputs that use it

Decision rules should be executable. If a threshold is unknown, record a
high-blocking open question that states which harness can compute metrics but
cannot automatically select or promote a method yet.

### Harness Structure

Create a dedicated `Harness Structure` section. A harness is a controlled
experiment execution environment for paper goals, method selection, module
optimization, ablation, stress, robustness, scalability, latency, quality,
accuracy, cost, or other metrics named by the blueprint and experiment plan.

Each harness should have a semantic name and a clear research purpose. For each
harness, specify:

- purpose and associated paper claim, experiment question, method-selection
  question, or optimization question
- role, such as development, candidate selection, final validation, diagnostic
  analysis, regression, or claim calibration
- target module or replaceable method area
- allowed modification scope
- stable interfaces and frozen variables
- command entry points using relative paths
- input dataset, workload, trace, split, seed, and config protocol
- methods, modified methods, naive methods, baselines, and oracles compared
- metrics and decision rule
- raw result files and minimum fields
- derived metric files
- comparison procedure
- smoke, pilot, and full modes when useful
- relationship to other harnesses
- failure modes that should be visible in artifacts

Harnesses should support the development loop:

```text
modify module -> run harness -> inspect parseable results -> refine module
```

Harness outputs should include the least processed records needed to audit the
run: per-example predictions or decisions, raw scores, timing traces, resource
usage, intermediate decisions, error cases, method/config identifiers, dataset,
split, seed, run ID, timestamp, source metadata, and raw artifact paths.

Use harness names as references. Example: `Candidate Method Selection Harness`
feeds the `Method Freeze Protocol`; `Full-System Trace Evaluation Harness`
consumes frozen method configs.

### Testing Structure

Create a dedicated `Testing Structure` section separate from harnesses. Testing
answers whether code behaves according to its interfaces. Harnesses answer
whether a method or module change helps paper metrics.

Plan test groups by function, using semantic names such as:

- `Data Loading Tests`
- `Config Parsing Tests`
- `Method Interface Tests`
- `Metric Computation Tests`
- `Result Export Tests`
- `CLI Smoke Tests`

For each test group, specify:

- test file path under `tests/`
- module, CLI, or interface under test
- fixture, toy input, or mock data path
- command
- expected behavior, output, schema, or exception
- pass/fail criterion
- temporary artifact or debug-log location
- harness dependency covered

Tests should use small fixtures or mock data and store debug artifacts under a
test-specific temporary path, separated from paper run-result directories.

### Experiment Stages and Commands

For complex experiments, plan staged commands. Typical stages include:

- data or asset preparation
- workload or task-instance construction
- candidate method run
- module-level optimization run
- full-system evaluation
- ablation run
- robustness or stress run
- metric computation
- method freeze
- paper-output derivation

Every command should use relative paths. The same stage should be reusable
across methods, datasets, splits, seeds, and configs through command-line
parameters or config overrides.

### Method Selection and Freeze Protocol

When candidate methods, learned variants, modified variants, or stress-tuned
variants exist, include a method-selection and freeze protocol:

- which harnesses may influence method design
- which harness selects the final method
- where the frozen method config or manifest is stored
- which final-validation runs use the frozen method
- how diagnostic or stress-tuned variants are labeled separately
- how final split contamination is prevented

Paper-facing final evaluation should use a frozen method. Development,
calibration, and candidate-selection harnesses can inform the method, while
final validation results stay separated from unrestricted tuning runs.

### Raw-First Result Export

Plan export files so later analysis, plotting, and writing skills can work
without rerunning experiments.

Use these classifications:

- `raw_observation`: observed events, identifiers, timestamps, paths, bytes,
  states, labels supplied by data, component outputs, and directly measured
  values
- `metadata`: run manifests, resolved configs, environment details, dependency
  versions, source commits, command text, orchestration records
- `metric`: derived scores, rates, deltas, deadline statistics, quality scores,
  aggregate summaries, statistical summaries, and decision-rule results
- `analysis`: counterfactuals, attributions, simulated alternatives, oracle
  analyses, and generated analytical records
- `summary`: human-readable reports and validation summaries

For each important export, specify:

- relative path
- purpose
- producing stage
- required fields
- granularity
- classification
- source raw files for metrics, summaries, and analyses
- downstream consumer, such as plotting, paper writing, or coding validation
- validation checks

Metadata should live at the run root or under `metadata/`. Raw observations
should live under `raw/`. Derived metrics should live under `metrics/`.
Analyses and attributions should live under `analysis/` unless a repository has
an established raw-oracle provenance convention.

### Paper Result Derivations

Map each required paper table, figure, or claim to exported artifacts:

- paper output name
- claim or evidence role
- raw files
- metric files
- grouping or filtering
- derived quantities
- statistical summary
- expected downstream artifact path
- notes for plotting or writing skills

Keep paper-specific plotting and table formatting outside the core experiment
system.

## Readability Pass

Before writing files, revise for readability:

- Use semantic names as primary anchors for methods, modules, harnesses, tests,
  exports, and stages.
- Keep existing short registry keys only as aliases beside semantic names.
- Replace alias-only cross-references with natural references such as
  `the Reference Lifecycle Stress Harness`.
- Use numbered lists only for actual sequence or priority.
- Make `coding_plan.explain.md` understandable without repeatedly checking
  `coding_plan.md`.
- Express boundaries as ownership rules, such as `Store derived metrics under
  metrics/` and `Route code implementation to the downstream coding skill`.
- Keep local execution troubleshooting details out of both generated artifacts.

## Validation

Before the final response, confirm:

- `coding_plan.md` exists and is English-only coding plan content.
- `coding_plan.explain.md` exists and is Chinese-first explanation content.
- The output directory contains exactly these two files unless the user
  explicitly requested additional artifacts.
- Both files use project-relative paths.
- DeepResearch was run or a fresh lookup artifact was reused.
- The plan includes environment assumptions, semantic module boundaries,
  replaceable methods and baselines, metrics and decision rules, harness
  structure, testing structure, staged commands, method freeze protocol when
  needed, raw-first exports, paper-output derivations, implementation order,
  acceptance criteria, and open coding questions.
- Every harness has a semantic name, paper-goal mapping, modification scope,
  stable inputs, relative command, parseable raw outputs, metric rule, and
  relationship to other harnesses.
- Every test group has a path under `tests/`, small fixtures, a command,
  functional pass/fail criteria, and temporary outputs separated from paper
  results.
- Paper outputs can be derived from raw and metric artifacts without rerunning
  experiments.
- For `output/evolve-*` outputs or sticky artifact-access feedback, the final
  response includes a `Review Handoff` section with both complete read-back
  files under their relative path headings.

## Final Response

After writing and validating the files, summarize:

- paths written
- major plan components
- high-blocking open questions
- validation performed, including read-back result

For `output/evolve-*` outputs or when artifact access feedback requests pasted
contents, add a `Review Handoff` heading after the concise summary and paste
the complete read-back contents of both files using the five-backtick handoff
format from `Artifact Delivery`. A final response that only reports paths,
line counts, validation status, or partial excerpts is incomplete for those
cases.
