---
name: academic-army-coding-plan
description: >-
  Create an English coding_plan.md and a user-language coding_plan.explain.md
  from a paper blueprint, experiment plan, repository context, candidate
  methods, baselines, datasets, metrics, and paper-result requirements. Use
  when Codex needs to translate research and experiment requirements into a
  modular implementation plan with shared domain models, replaceable
  method/baseline locations, staged CLI execution, metric definitions,
  optimization/evaluation harnesses, method-freeze protocol, validation checks,
  and a raw-first result export contract for downstream coding, plotting, and
  paper-writing skills.
---

# Academic Army Coding Plan

## Purpose

Create an implementation planning package that lets a downstream coding skill
build the experiment system without redesigning the architecture.

Produce exactly two Markdown files:

1. `coding_plan.md`
   - English.
   - AI-facing.
   - Contains only the coding plan.
   - Specifies modules, interfaces, replaceable method and baseline placement,
     staged experiment commands, harnesses, raw result exports, validation
     checks, implementation order, and acceptance criteria.

2. `coding_plan.explain.md`
   - Uses the user's conversation language for headings, labels, and body text.
   - Human-facing.
   - Contains only the explanation and decision rationale for the coding plan.
   - Explains the extracted requirements, architectural choices, harness
     rationale, raw-export rationale, assumptions, and downstream usage.

This skill writes planning artifacts. The coding skill that runs later
implements code from the plan.

## Required Context

Gather local context before writing the files.

Read, when present:

- `paper_blueprint.md`
- `paper_blueprint.explain.md`
- `experiment_plan.md`
- `experiment_plan_explanation.*.md`
- existing coding plans or implementation notes
- repository README files
- package metadata such as `pyproject.toml`, `package.json`, `requirements.txt`,
  `setup.py`, `Cargo.toml`, or equivalent
- existing `src`, `configs`, `scripts`, `tests`, `notebooks`, `experiments`,
  `data`, and `runs` directories
- user-provided blueprint text, experiment-plan text, method lists, baseline
  lists, metric lists, compute constraints, dataset constraints, and output
  requirements

If the blueprint or experiment plan is unavailable after checking obvious local
paths and user-provided text, ask for the exact missing content before writing a
final plan. Live research can supply external method, benchmark, dataset, or
metric facts, but the local paper blueprint and experiment plan control the
planning task.

## Required Pre-Planning Research

Begin planning with `academic_army_mcp_tools.deepresearch` unless a fresh lookup
artifact already exists in the provided context and clearly covers the current
paper domain, method family, experiment style, and repository design question.

A lookup artifact is fresh enough only when it includes:

- the lookup topic or query
- sources or repository examples
- source date, release version, or commit hash when available
- takeaways about highly engineered related codebases
- design choices affected in this coding plan
- visible date, version, or retrieval context when available

If no such artifact exists, run a new lookup before drafting
`coding_plan.md`. The lookup should inspect how strong, well-engineered related
research or benchmark codebases organize package layout, configs, registries,
evaluation harnesses, result exports, and tests. Prefer mature repositories,
official benchmark artifacts, widely used frameworks, or paper artifacts with
clear modular engineering over one-off scripts.

- Server: `academic_army_mcp_tools`
- Tool: `deepresearch`
- Canonical Codex MCP name when exposed:
  `mcp__academic_army_mcp_tools__deepresearch`

Also use live research for:

- canonical implementation details of candidate methods and baselines
- current benchmark protocols, dataset schemas, or metric definitions
- recent repositories, model APIs, datasets, leaderboards, or artifact
  conventions
- unclear terminology from the blueprint or experiment plan
- current evaluation-harness or experiment-tracking patterns that affect the
  plan

Put only planning consequences in `coding_plan.md`. Record the lookup topic,
sources, dates or versions, engineering takeaways, affected design choices,
confidence, whether each takeaway is a confirmed source fact or an inferred
design pattern, and remaining uncertainty in `coding_plan.explain.md`.
When no fresh lookup artifact is available, the generated explanation should
show the new lookup results. It should not state that no live research was
performed unless `deepresearch` was attempted and unavailable; in that case,
record the unavailable tool as a high-blocking open question.

Use this prompt shape:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a coding-plan generator for a research paper.

Research brief:
[paper goal, system, candidate methods, baselines, datasets, metrics, and
experiment-plan requirements]

Return concise implementation-planning evidence:

1. Highly engineered related repositories or official artifacts and how they
   structure modules, configs, registries, harnesses, exports, and tests.
2. Canonical implementation shape for each method or baseline.
3. Current benchmark or dataset protocol details that affect loaders,
   evaluators, metrics, or comparators.
4. Existing repository/artifact conventions worth matching.
5. Evaluation harness implications: controllable variables, frozen components,
   smoke/full protocols, metrics, and decision rules.
6. Raw result fields needed for later tables, figures, and paper claims.
7. Source table with title, link, date, version, or commit when visible; role;
   whether the takeaway is confirmed source fact or inferred design pattern;
   and the planning decision it affects.
```

## Planning Boundary

The coding plan is an engineering contract, not a code implementation.

Plan these items:

- package layout and module boundaries
- environment setup and executable entry points
- core domain models and shared serialized schemas
- public interfaces and adapter contracts
- config structure and CLI override model
- candidate method and baseline placement
- workload and experiment config placement
- metric definitions and decision-rule thresholds
- staged experiment pipeline
- optimization/evaluation harnesses
- method selection and freeze protocol
- experiment execution matrix
- raw-first result export contract
- validation, smoke tests, and acceptance criteria
- implementation order for the downstream coding skill
- derivation path from raw outputs to paper tables, figures, and claims

Route later work clearly:

- code implementation belongs to the downstream coding skill
- figure generation belongs to plotting/visualization skills
- paper prose belongs to writing skills
- statistical reporting, aggregation, and plotting transformations are described
  as derivations from raw outputs rather than embedded as core experiment-system
  logic

## Positive Planning Style

Write with direct, positive constraints. State the required artifact, interface,
module boundary, command, metric, or export field. Use assumptions and blocking
levels when information is missing.

Prefer:

- `Use a shared method registry so every candidate and baseline is selected by
  config.`
- `Treat unmodified candidate methods as naive baselines and scenario-adapted
  variants as proposed-method candidates.`
- `Export per-example JSONL records and aggregate metrics so later skills can
  derive paper tables and figures outside the core experiment system.`

Use defensive language sparingly. Replace broad caveats with actionable
planning state:

- `Planning assumption`
- `Open coding question`
- `DeepResearch lookup`
- `Validation check`
- `Blocking level: low | medium | high`

State placement rules positively. Prefer:

- `Place experiment-system code under src/<pkg>; keep orchestration assets in
  AcademicArmy-managed directories.`
- `Store run metadata in metadata/ and direct observations in raw/.`
- `Reference registry IDs in harness sections and put full definitions in the
  registries.`

## Additional Quality Requirements

### Core Domain Model Requirement

When the planned system contains interacting modules for data loading,
simulation/replay, policy decisions, evaluation, harnesses, and export, include
a `Core Domain Model and Shared Interfaces` section before module-level
implementation details.

For each shared type, specify:

- type name
- owning module path
- purpose
- key fields
- producing modules
- consuming modules
- raw export mapping, if applicable

Use shared domain types to prevent duplicate schemas across loaders, methods,
evaluators, harnesses, and export writers.

### Environment and Entry-Point Requirement

Include an `Environment and Entry-Point Plan` whenever commands use package
module entry points such as `python -m <pkg>.run`.

Specify:

- package root
- install command
- working directory assumption
- import validation command
- test command
- config discovery path
- run-root path

Every CLI command in the plan should be executable under the stated setup.

### Metric Definition Requirement

For every metric used by a harness, decision rule, acceptance criterion, or
paper-result derivation, include:

- metric ID
- definition
- unit
- direction: `higher_is_better` or `lower_is_better`
- formula or computation procedure
- raw required fields
- upstream metric dependencies, when this metric uses another derived metric
- derived outputs produced by the metric
- aggregation rule
- missing-data behavior
- harnesses using the metric
- paper outputs using the metric

A decision rule is executable only when all referenced metrics are defined. If
a required threshold is not known, record a high-blocking open question that
states which harness can run metrics but cannot automatically select or promote
a method.

### Harness Role and Method-Freeze Protocol

Assign each harness one or more roles:

- `development`
- `selection`
- `final_validation`
- `diagnostic`
- `regression`
- `claim_calibration`

When a harness is used to modify, tune, or select a method, define the
development/calibration split and the held-out final split.

When the plan contains candidate methods, modified variants, learned variants,
or stress-tuned variants, include a `Method Selection and Freeze Protocol` that
states:

- which harnesses may influence method design
- which harness selects the final method
- where the frozen method config is stored
- which final-validation runs are performed after the method is frozen
- how stress-tuned or diagnostic variants are labeled separately from the main
  proposed method

Paper-facing final evaluation should use a frozen method. Development or
selection harnesses can produce planning evidence, pilot results, or diagnostic
results, but final-validation results should be reported separately from
unrestricted method-tuning runs.

### Raw-vs-Derived Export Boundary

Raw files contain observed events, identifiers, timestamps, paths, bytes,
states, externally supplied labels, component outputs, and directly measured
component values.

Metadata files contain run manifests, resolved configs, environment details,
dependency versions, source commits, command text, and orchestration records.

Metric files contain derived quality scores, QoE scores, deltas, rates, deadline
statistics, waste quantities, aggregate summaries, statistical summaries, and
decision-rule results.

Analysis files contain generated counterfactuals, simulated alternatives,
oracle analyses, attributions, and other derived analytical records that are
not direct observations.

Place image-comparison metrics, QoE scores, quality deltas, statistical
summaries, and harness decision outputs under `metrics/`, not `raw/`, unless
they are explicitly labeled as cached derived metadata with a source field.
Place run metadata under `metadata/` or the run root. Place counterfactual and
other generated analytical outputs under `analysis/` unless they are direct
oracle outputs with provenance.

### Experiment Execution Matrix

For each major experiment or harness, include an execution matrix with:

- datasets
- scenes or workloads
- traces or splits
- methods
- baselines
- seeds
- stress factors or controlled factors
- budget modes
- expected number of runs
- approximate artifact volume when relevant
- minimum smoke subset
- full-run scope
- parallelization or batching notes

The matrix should make the smallest useful run set, pilot set, and full paper
run set visible.

### Baseline Disambiguation

When two baselines or variants have overlapping behavior, define:

- behavioral difference
- reason both are included
- harnesses requiring each baseline
- whether each baseline is headline, diagnostic, oracle, ablation, or
  calibration-only

### Canonical Registry and Length Control Requirement

Use canonical registries to prevent repeated prose. Define each workload,
method, baseline, metric, harness, and paper output once, then reference the
registry IDs in objective maps, execution matrices, harnesses, acceptance
criteria, and derivation maps.

Create these canonical tables when the corresponding entities exist:

- `Workload Registry`
- `Optional Workload Scope Table`
- `Method and Baseline Registry`
- `Metric Registry`
- `Harness Registry`
- `Paper Output Derivation Registry`

Each registry row should contain the stable ID, owner path or config path,
role, key fields, and cross-references needed by downstream coding. Later
sections should use compact references such as `workloads: W1, W2`,
`methods: M1, B1`, `metrics: Q1, L2`, `harnesses: H1`, and
`paper_outputs: P1, P2`.

Use "canonical definition once, references thereafter" as the length-control
rule. The plan should be detailed enough to implement but should avoid
restating the same method/baseline/workload/metric mappings in multiple
sections. Prefer compact tables over repeated bullet blocks.

Treat `coding_plan.md` as an engineering contract, not an expanded design
memo. For typical projects, target roughly 6k-8k words. For unusually complex
projects, exceed that target only when the extra text introduces new
implementation obligations rather than repeating registry mappings. If a plan
would become long, compress objective maps, harnesses, execution matrices, and
paper derivations into ID references plus the smallest stage-specific notes.

For metric definitions, include `Numerator` and `Denominator` only when the
metric is ratio-like. Omit those fields for non-ratio metrics instead of
writing `not applicable`.

### Optional Workload Scope Requirement

When the blueprint or experiment plan contains optional, stretch, or
scope-extension workloads, include an `Optional Workload Scope Table`.

For each optional workload, assign exactly one scope status:

- `core`: required for the main implementation and paper claims
- `optional-planned`: implemented if time/compute permits and included in
  configs with smoke/full commands
- `deferred`: inventoried for future work, with no required builder,
  command, or acceptance criterion in the current plan

For every row, provide the rationale, implementation impact, required config
or builder path if in scope, and the paper outputs or claims it can support.
If a workload is only inventoried, state that it is `deferred` so downstream
coding does not treat it as an unimplemented requirement.
Use `deferred` for workloads that are out of scope for the first
implementation.

### Research Lookup Recording Requirement

Record every pre-planning lookup and any later live research lookup in
`coding_plan.explain.md`, even when the result only confirms the local plan.

Use a short research-impact table. For each lookup, include:

- topic or query
- sources or repository examples inspected
- source date, release version, or commit hash when available
- key takeaway
- evidence type: `confirmed_source_fact` or `inferred_design_pattern`
- design decision affected
- confidence
- remaining uncertainty
- whether it affects implementation, experiment protocol, or claims

## Workflow

### 1. Run or Reuse Pre-Planning DeepResearch

Before drafting architecture, run `deepresearch` to inspect highly engineered
related codebases and artifact conventions, unless a fresh lookup artifact is
already present in context.

Use the results to choose:

- package and module layout patterns
- config and registry conventions
- method/baseline adapter boundaries
- harness execution style
- raw and metric export layout
- validation and smoke/full testing patterns

Record the lookup in `coding_plan.explain.md` with localized headings and
labels. If the tool is unavailable after attempting to discover or call it,
record a high-blocking open question named `DeepResearch lookup unavailable`
and explain which architecture decisions remain less grounded.

### 2. Inventory Research and Experiment Requirements

Extract from the blueprint, experiment plan, and user text:

- proposed system or method
- research questions and hypotheses
- required experiments
- candidate methods
- baselines
- proposed-method variants
- ablation variants
- datasets, splits, preprocessing, and constraints
- metrics and expected comparisons
- efficiency, cost, latency, robustness, scalability, reproducibility, or
  resource measurements
- required paper tables, figures, qualitative examples, and claims
- compute, runtime, API, privacy, hardware, or deployment constraints
- existing preliminary code, data, models, traces, or results

Map every experiment-plan requirement to at least one planned module, stage,
command, harness, raw output, or validation check.

### 3. Inspect Repository Context

Identify:

- current package layout
- existing data-loading, method, model, evaluation, configuration, logging,
  script, test, and notebook conventions
- reusable modules and gaps
- natural package name and command entry point
- current dependency stack and likely framework choices
- existing artifact and result directories
- package roots, install commands, editable-install conventions, and import
  validation commands
- config roots and run-output roots

If the repository already has conventions, align the plan with them. If no
implementation structure exists, propose a clean layout that downstream coding
can create.

### 4. Define Core Domain Models and Shared Interfaces

Define the stable typed objects that cross module boundaries before defining
the modules that use them.

Include core types for:

- episodes, traces, examples, scenes, splits, and workloads
- decision states, actions, feedback, and policy outputs
- method inputs and outputs
- external requests, tickets, events, and outcomes
- substrate/model outputs
- raw export records
- metric records and aggregate metrics
- harness results and validation results

For each type, specify owner module, key fields, producers, consumers, and raw
serialization mapping.

### 5. Design Objective, Workload, and Config Placement

Create an `Experiment Objective Map` when the experiment plan names objectives,
claim-to-evidence entries, required paper outputs, or numbered experiments.

For each objective, specify:

- objective ID and name
- claim or evidence role
- workload IDs from the `Workload Registry`
- method and baseline IDs from the `Method and Baseline Registry`
- harness IDs from the `Harness Registry`
- stage IDs or stage names
- raw output file IDs from the export contract
- metric IDs from the `Metric Registry`
- paper output IDs from the `Paper Output Derivation Registry`

Create a `Workload Registry` when the plan has workload suites, trace suites,
stress suites, controlled factor grids, or benchmark families.

For each workload or experiment config, specify:

- config ID
- scope status: `core`, `optional-planned`, or `deferred`
- config path
- builder module path
- required factors
- used-by harnesses
- used-by objectives
- raw required fields

For `deferred` workloads, omit implementation obligations and commands. Keep
only the rationale and future integration note.

### 6. Design Replaceable Methods and Baselines

Every candidate method and baseline from the blueprint or experiment plan gets
a stable code location and config location.

For each method or baseline, specify:

- name
- role: `naive_baseline`, `candidate_method`, `modified_candidate`,
  `proposed_method`, `ablation_variant`, `oracle`, or `diagnostic_baseline`
- proposed module path
- config path
- registry name
- adapter/interface to implement
- inputs and outputs
- dependencies
- replaceability boundary
- CLI/config selector
- experiments and harnesses that use it
- raw outputs required for comparison

Use a shared interface, registry, or adapter layer so experiments can switch
`method=<name>` without changing scripts.

A typical Python layout:

```text
src/<pkg>/
  methods/
    base.py
    registry.py
    <baseline>.py
    <candidate>.py
    <proposed_variant>.py
configs/
  method/
    <baseline>.yaml
    <candidate>.yaml
    <proposed_variant>.yaml
```

Equivalent layouts are acceptable when they match the repository's language and
framework.

Disambiguate overlapping baselines directly in this section. If two baselines
disable the same capability, state whether one is a headline baseline and the
other is a diagnostic condition, ablation, or internal harness variant.

For learned or trained baselines, specify:

- train split
- validation split
- held-out test split
- feature schema
- label or reward schema
- checkpoint path
- policy loading rule
- random seed handling
- test-time exploration policy
- exported model identifiers such as `model_id`, `checkpoint_hash`,
  `train_split_id`, `validation_split_id`, and `test_split_id`

### 7. Define Metrics and Decision Rules

Define every metric before it is used in harness decision rules, acceptance
criteria, or paper-result derivations.

For each metric, include:

- metric ID
- definition
- unit
- direction
- numerator and denominator when applicable
- formula or computation procedure
- raw required fields
- upstream metric dependencies, when this metric composes other metrics
- derived outputs produced by this metric
- missing-data behavior
- aggregation rule
- harnesses using it
- paper outputs using it

For each decision rule, provide numeric default thresholds or a high-blocking
open question. Thresholds can be config-overridable, but the coding plan should
state defaults whenever a reasonable default is available.

### 8. Design the Staged Experiment System

Break complex experiments into callable stages. Each stage has one command and
supports parameterized execution across datasets, splits, methods, seeds,
budgets, and variants.

Use this stage set as the default:

- `prepare_data`
- `build_artifacts`
- `train_or_fit`
- `run_inference`
- `evaluate`
- `run_harness`
- `export_raw`
- `validate_outputs`

For each stage, specify:

- command example
- inputs
- outputs
- config keys or CLI overrides
- idempotency and caching behavior
- dependencies on earlier stages
- failure checks
- smoke-run mode
- full-run mode

Plan a config-driven CLI with equivalent capability to:

```bash
python -m <pkg>.run stage=prepare_data dataset=<dataset> split=<split>
python -m <pkg>.run stage=build_artifacts dataset=<dataset> method=<method>
python -m <pkg>.run stage=train_or_fit experiment=<id> dataset=<dataset> method=<method> seed=<seed>
python -m <pkg>.run stage=run_inference experiment=<id> dataset=<dataset> method=<method> seed=<seed>
python -m <pkg>.run stage=evaluate run_id=<run_id>
python -m <pkg>.run stage=export_raw experiment=<id>
python -m <pkg>.run -m stage=run_inference experiment=<id> dataset=d1,d2 method=m1,m2 seed=0,1,2
python -m <pkg>.harness harness=<harness_id> method=<candidate> budget=smoke
```

Adapt the syntax to the repository's framework. Preserve the capability to
change dataset, split, method, seed, budget, and variant from command-line
parameters or config overrides.

### 9. Design Harnesses

A harness is a controlled evaluation plan for an implementation modification.
It identifies a module under test, defines the allowed modification scope,
fixes the surrounding system, runs metrics, exports raw records, and gives a
decision rule.

Use harnesses to support:

- candidate-method selection
- scenario-specific modification of existing methods
- proposed-method promotion
- ablation validation
- performance/quality/cost trade-off testing
- regression checks for baselines and fixed modules

For each harness, include:

- Harness ID
- Name
- Role: one or more of `development`, `selection`, `final_validation`,
  `diagnostic`, `regression`, `claim_calibration`
- Purpose or research question
- Module under test
- Allowed modification scope
- Registry references for methods, baselines, workloads, metrics, raw outputs,
  metric outputs, and execution matrix row
- Command examples: smoke, full, and sweep when useful
- Decision rule for promotion, rejection, or further modification
- Failure modes to monitor

Keep each harness entry compact. The canonical registries and execution matrix
own the full workload/method/metric/output mappings. A harness entry should add
only the stage-specific purpose, module under test, allowed modification scope,
commands, decision rule, and failure modes.

Harness decision rules should be concrete enough for iterative coding:

```text
Promote the modified variant with the highest mean <primary_metric> across
seeds, subject to <guardrail_metric> staying within <threshold> of the strongest
naive baseline. Keep unmodified variants as baselines for final experiments.
```

### 10. Design Method Selection and Freeze Protocol

When methods are selected, tuned, or promoted through harnesses, define:

- development harnesses
- selection harnesses
- pilot/calibration data
- held-out final-validation data
- frozen method config path
- final-validation harnesses
- diagnostic/stress variants reported separately from the main method
- rules for learned baseline training/validation/test isolation

### 11. Design Raw-First Result Export

Plan result export as a small contract that minimally touches system internals
and maximizes later reuse.

Use this default directory contract unless the repository already has a strong
alternative:

```text
runs/
  <run_id>/
    manifest.json
    config.resolved.yaml
    command.txt
    metadata/
      run_metadata.json
      environment.json
      source_versions.json
    raw/
      predictions.jsonl
      examples.jsonl
      events.jsonl
      timings.jsonl
      costs.jsonl
    metrics/
      per_example_metrics.jsonl
      aggregate_metrics.json
      per_slice_metrics.jsonl
      harness_decisions.jsonl
    analysis/
      counterfactuals.jsonl
    artifacts/
      checkpoints/
      caches/
      logs/
```

For each file, define:

- purpose
- required fields
- producing stage
- consuming downstream skill
- relationship to paper tables, figures, or claims
- export classification: `raw_observation`, `direct_component_output`,
  `metadata`, `metric`, `summary`, `analysis`, or `cached_derived_metadata`
- source raw files for every metric, summary, analysis, or cached derived file

Plan raw per-example records before high-level summaries. Keep table/figure
transformations as documented derivations from raw files so later plotting and
paper-writing skills can transform the data without depending on experiment
system internals.

Respect the export classification boundary. Put observed events, identifiers,
states, paths, timings, bytes, and direct component outputs under `raw/`. Put computed
quality metrics, QoE scores, deltas, rates, statistical summaries, and harness
decision results under `metrics/`. Put run metadata, resolved configs,
environment details, dependency versions, source commits, and orchestration
metadata under `metadata/` or at the run root, not under `raw/`.

Put counterfactuals, simulated alternatives, oracle analyses, attribution
records, and other generated analytical outputs under `analysis/` unless they
are direct externally supplied oracle outputs captured during the run. If a
counterfactual-like file is treated as direct raw output, require provenance
fields that identify the producing oracle, timestamp, input raw file IDs, and
why it is a direct observation rather than a derived analysis artifact.

When a harness produces both raw observations and computed scores, list them in
separate blocks:

- `Raw outputs`: only raw files and raw fields
- `Metric outputs`: metric files, aggregate summaries, decision-rule records,
  and their source raw files

Metric files such as `metrics/per_example_metrics.jsonl`,
`metrics/aggregate_metrics.json`, `metrics/per_slice_metrics.jsonl`, and
`metrics/harness_decisions.jsonl` must not appear under a `Raw outputs` block.

### 12. Design Validation and Acceptance Checks

Include checks for:

- imports and package entry points
- config validation
- method registry completeness
- method/baseline instantiation
- dataset schema validation
- smoke runs for each required stage
- harness smoke and full execution
- raw output schema validation
- metric sanity checks
- reproducibility across seeds or cached artifacts
- baseline regression behavior
- result completeness for required paper tables, figures, and claims
- cross-reference integrity across modules, harnesses, metrics, workloads,
  commands, and generated paths

The downstream coding skill should be able to turn these checks into tests,
scripts, or CI commands.

### 13. Write `coding_plan.md`

Use this structure. Omit sections only when they are genuinely inapplicable and
state the reason under `Planning Assumptions`.

```markdown
# Coding Plan: <Paper/System Name>

## 1. Scope and Planning Assumptions

## 2. Repository Context

## 3. Research Requirements Inventory

## 4. Environment and Entry-Point Plan

Include:
- Package root
- Install command
- Working directory assumption
- Import validation command
- Test command
- Config discovery path
- Run-root path

## 5. Target System Architecture

## 6. Core Domain Model and Shared Interfaces

For each shared type:
- Type name
- Owning module path
- Purpose
- Key fields
- Producing modules
- Consuming modules
- Raw export mapping

## 7. Canonical Registries

Include these subsections when applicable:
- Workload Registry
- Optional Workload Scope Table
- Method and Baseline Registry
- Metric Registry
- Harness Registry
- Paper Output Derivation Registry

Define each workload, method, baseline, metric, harness, and paper output once.
Use the registry IDs in later sections.

## 8. Experiment Objective Map

For each objective, reference registry IDs:
- Objective ID
- Claim or evidence role
- Workload IDs
- Method and baseline IDs
- Harness IDs
- Stage names
- Raw output file IDs
- Metric IDs
- Paper output IDs

## 9. Workload and Experiment Config Placement

For each workload or experiment config:
- Config ID
- Scope status: core | optional-planned | deferred
- Config path
- Builder module path
- Required factors
- Used by objectives
- Used by harnesses
- Raw required fields

## 10. Module Plan

For each module:
- Purpose
- Proposed path
- Existing path if applicable
- Public interface
- Inputs
- Outputs
- Config keys
- Dependencies
- Implementation notes
- Tests or validation checks

## 11. Method and Baseline Placement

For each method or baseline:
- Name
- Role
- Proposed module path
- Config path
- Registry name
- Adapter/interface
- Replaceability boundary
- Behavioral difference from similar baselines, if applicable
- Used by experiments
- Used by harnesses
- Raw outputs required for comparison

## 12. Metric Definitions

For each metric:
- Metric ID
- Definition
- Unit
- Direction
- Formula or computation procedure
- Raw required fields
- Upstream metric dependencies, when any
- Derived outputs
- Aggregation rule
- Missing-data behavior
- Used by harnesses
- Used by paper outputs

## 13. Experiment Stages and CLI Plan

For each stage:
- Stage name
- Command
- Inputs
- Outputs
- Config overrides
- Idempotency/caching
- Failure checks
- Smoke/full mode

## 14. Method Selection and Freeze Protocol

## 15. Harness Plan

For each harness:
- Harness ID
- Name
- Role
- Purpose or research question
- Module under test
- Allowed modification scope
- Registry references: method IDs, baseline IDs, workload IDs, metric IDs,
  raw output IDs, metric output IDs, execution matrix row ID
- Command examples
- Decision rule
- Failure modes

## 16. Experiment Execution Matrix

For each major experiment or harness:
- Datasets
- Scenes/workloads
- Traces/splits
- Methods
- Baselines
- Seeds
- Stress or controlled factors
- Budget modes
- Expected number of runs
- Approximate artifact volume
- Minimum smoke subset
- Full-run scope
- Parallelization or batching notes

## 17. Raw Result Export Contract

## 18. Deriving Paper Results from Raw Outputs

Extend the `Paper Output Derivation Registry` with operational notes instead of
repeating full registry definitions. For each table, figure, qualitative
example, or claim:
- Raw file IDs
- Grouping/filtering logic
- Metric IDs or derived quantities
- Expected downstream artifact

## 19. Implementation Order for the Coding Skill

## 20. Acceptance Criteria

## 21. Open Questions and Research Lookups

For each item:
- Missing information
- Why it matters
- Suggested deepresearch query or repository inspection step
- Blocking level: low | medium | high
```

Quality bar for `coding_plan.md`:

- Every experiment-plan requirement maps to a module, stage, command, harness,
  raw output, or validation check.
- Every candidate method and baseline has a code location and config location.
- Every shared type used by multiple modules appears in the core domain model.
- Every workload suite has a config path and builder path.
- Every metric used by a harness, decision rule, acceptance criterion, or paper
  output has a complete definition.
- Every candidate method can be selected through a shared interface, registry,
  adapter, or config group.
- Optional workloads are explicitly marked `core`, `optional-planned`, or
  `deferred`, with deferred workloads excluded from implementation obligations.
- Every complex experiment has smoke and full execution commands.
- Every harness defines purpose, module under test, modification scope,
  registry references, command examples, decision rule, and failure modes.
- Every required paper table, figure, qualitative example, or claim has a
  derivation path from raw outputs.
- Final evaluation is separated from unrestricted method tuning.
- Raw, metadata, metric, summary, and analysis files follow the export
  classification boundary.
- Canonical definitions appear once in registries, and later sections reference
  IDs instead of repeating the same mapping prose.
- The implementation order builds from infrastructure to data, methods,
  baselines, harnesses, proposed variants, full experiments, and validation.

### Canonical Registry Table Schemas

Use compact Markdown tables for registries. Add only columns needed for the
paper and repository at hand.

`Workload Registry` columns:

- ID
- Scope: `core`, `optional-planned`, or `deferred`
- Config path
- Builder path
- Factors
- Raw required fields
- Used by objectives
- Used by harnesses

`Method and Baseline Registry` columns:

- ID
- Name
- Role
- Module path
- Config path
- Registry key
- Interface
- Comparison raw outputs
- Used by objectives
- Used by harnesses

`Metric Registry` columns:

- ID
- Definition
- Unit
- Direction
- Raw required fields
- Upstream metric dependencies
- Derived outputs
- Aggregation
- Used by harnesses
- Used by paper outputs

`Harness Registry` columns:

- ID
- Role
- Module under test
- Candidate method IDs
- Baseline IDs
- Primary metric ID
- Guardrail metric IDs
- Raw output IDs
- Metric output IDs
- Freeze relationship

`Paper Output Derivation Registry` columns:

- ID
- Paper output type
- Claim or evidence role
- Raw file IDs
- Metric IDs
- Grouping or filtering
- Statistical summary
- Downstream artifact

Detailed module, harness, metric, and export schemas may follow these tables
when implementation details are needed. Do not repeat a registry row in prose;
reference its ID and add only the extra operational detail required in that
section.

### Harness Entry Schema

Use this compact schema inside `coding_plan.md` for each harness. Keep full
method, baseline, workload, metric, output, split, and seed mappings in the
canonical registries and execution matrix. Harness entries should reference IDs
and add only harness-specific instructions.

```markdown
### Harness <ID>: <Name>

**Role:**  
<development | selection | final_validation | diagnostic | regression | claim_calibration>

**Purpose:**
<What method-selection, optimization, validation, diagnostic, or claim-calibration question this harness answers.>

**Module under test:**  
- Path:
- Interface:
- Config group:

**Allowed modification scope:**  
- Files/directories:
- Config keys:
- Method internals:

**Registry references:**
- Method IDs:
- Baseline IDs:
- Workload IDs:
- Metric IDs:
- Raw output IDs:
- Metric output IDs:
- Execution matrix row ID:
- Freeze-protocol reference:

**Commands:**  
- Smoke:
- Full:
- Sweep:

**Decision rule:**  
<Exact rule for promotion, rejection, or further modification.>

**Failure modes:**  
- Metric or analysis artifacts:
- Data leakage:
- Instability across seeds:
- Latency/cost regressions:
- Invalid comparison risks:
```

### Module Entry Schema

Use this level of detail for important modules:

```markdown
### Module: <Name>

Purpose:
<What responsibility this module owns.>

Proposed path:
`src/<pkg>/<area>/<file>.py`

Existing path if applicable:
`<existing/path>`

Public interface:
- `<function_or_class_signature>`

Inputs:
- ...

Outputs:
- ...

Config keys:
- ...

Dependencies:
- ...

Implementation notes:
- ...

Validation checks:
- ...
```

### Metric Definition Schema

Use this schema for each metric:

```markdown
### `<metric_id>`

- Definition:
- Unit:
- Direction:
- Formula or computation procedure:
- Numerator, only for ratio-like metrics:
- Denominator, only for ratio-like metrics:
- Raw required fields:
- Upstream metric dependencies:
- Derived outputs:
- Missing-data behavior:
- Aggregation rule:
- Used by harnesses:
- Used by paper outputs:
```

For non-ratio metrics, omit the numerator and denominator lines entirely.

### Export Entry Schema

Use this schema for each exported raw, metric, summary, or cached derived file:

```markdown
### `<path>`

- Purpose:
- Producing stage:
- Required fields:
- Granularity: run | dataset | seed | example | event | slice
- Consuming downstream skill:
- Paper result derivations:
- Export classification: raw_observation | direct_component_output | metadata | metric | summary | analysis | cached_derived_metadata
- Source raw files, for metric/summary/analysis/cached derived files:
- Validation checks:
```

### Paper Result Derivation Schema

Use this schema for each required paper result:

```markdown
### <Table/Figure/Claim ID>: <Name>

- Paper role:
- Raw file IDs:
- Metric IDs:
- Grouping/filtering:
- Derived quantities:
- Statistical summary:
- Expected downstream artifact:
- Notes for plotting/writing skill:
```

### 14. Write `coding_plan.explain.md`

Write headings, labels, and body text in the user's conversation language.
Preserve method names, dataset names, metric identifiers, file paths, command
names, and code identifiers exactly.

Use this structure, translated into the user's language. The headings below are
semantic labels, not literal English headings to copy:

```markdown
# <Localized title for "Coding Plan Explanation">: <Paper/System Name>

## 1. <Localized heading for "Inputs Read and Requirement Extraction">

## 2. <Localized heading for "Pre-Planning DeepResearch Lookup">

## 3. <Localized heading for "Main Architectural Decisions">

## 4. <Localized heading for "Method and Baseline Placement Rationale">

## 5. <Localized heading for "Experiment Stage Rationale">

## 6. <Localized heading for "Harness Design Rationale">

## 7. <Localized heading for "Raw Result Export Rationale">

## 8. <Localized heading for "Optional Workload Scope Decisions">

## 9. <Localized heading for "Assumptions and Uncertainty">

## 10. <Localized heading for "How the Downstream Coding Skill Should Use the Plan">
```

When the user's language is Chinese, for example, use headings such as
`已读取输入与需求提取`, `预规划研究（DeepResearch）`, `主要架构决策`,
`工作负载（Workload）范围决策`, `方法与基线放置理由`,
`测试方案（Harness）设计理由`, `原始结果导出理由`, and
`下游编码技能（Coding Skill）使用方式`.
Technical identifiers such as `MethodRegistry`, `stage=run_harness`, `H1`, or
`raw/predictions.jsonl` can remain in English.

Do not leave general headings or labels such as `External Research Lookup
Impact`, `Method`, `Baseline`, `Stage`, `Harness`, or `Raw Result Export` in
English when the user's language has a natural translation. Keep only technical
identifiers and code-facing names unchanged.
For Chinese, headings should be Chinese-first with English terms in
parentheses only when the English term is a useful technical anchor, such as
`预规划研究（DeepResearch）` rather than `DeepResearch 影响`.

The explanation should make the plan reviewable. Include:

- which local files or user-provided contents were read
- what requirements were extracted
- why modules were separated this way
- why methods and baselines are represented as replaceable components
- why each harness exists and how it supports method selection or optimization
- how development/selection harnesses are separated from final validation
- why the raw export contract is enough for later figures, tables, and paper
  claims
- a short research-impact table for pre-planning DeepResearch and any later
  external research, with columns: lookup topic, sources or repositories, key
  takeaway, source date/version/commit when available, evidence type, affected
  design choice, confidence, remaining uncertainty, and impact area
- which optional workloads are `core`, `optional-planned`, or `deferred`
- which assumptions matter, their impact, and the next lookup or inspection step

Write rationale at a summary level. The explanation should expose decision
logic and trade-offs, while keeping the operational plan in `coding_plan.md`.

## Internal Validation Pass

Before finalizing, audit the artifacts.

### File Contract Check

- `coding_plan.md` exists and contains only the coding plan.
- `coding_plan.explain.md` exists and contains only the explanation and decision
  rationale.
- `coding_plan.md` is English.
- `coding_plan.explain.md` uses the user's conversation language for headings,
  labels, and body text, while preserving technical identifiers.
- The filenames are exactly `coding_plan.md` and `coding_plan.explain.md`.

### DeepResearch Check

- A fresh pre-planning `deepresearch` lookup was run or a fresh lookup artifact
  was reused.
- The lookup inspected highly engineered related codebases or official
  artifacts, not only method definitions.
- `coding_plan.explain.md` records the lookup topic, sources or repositories,
  source dates, versions or commits when available, takeaways, evidence type,
  affected design choices, confidence, and remaining uncertainty.
- DeepResearch summaries distinguish confirmed API or repository facts from
  inferred design patterns.
- When no fresh lookup artifact existed, `coding_plan.explain.md` contains new
  lookup results rather than saying no live research was performed.
- If `deepresearch` was unavailable, the plan records a high-blocking open
  question and identifies which architecture decisions need external grounding.

### Completeness Check

- Every experiment-plan requirement is represented in the plan.
- Environment setup makes all CLI examples executable.
- Shared core types are defined before module interfaces reference them.
- Every candidate method and baseline has a module path and config path.
- Every workload has config placement and builder placement.
- Optional workloads have explicit scope status: `core`, `optional-planned`, or
  `deferred`.
- Every metric has definition, unit, direction, raw required fields, upstream
  metric dependencies when any, derived outputs, aggregation rule, and
  missing-data behavior.
- Every method/baseline uses a shared replaceability boundary.
- Every complex experiment has staged CLI commands.
- Every harness has purpose, target module, modification scope, registry
  references, command examples, decision rule, and failure modes.
- Every required paper output has a raw-data derivation path.
- Acceptance criteria are concrete enough for downstream tests and smoke runs.

### Repository Alignment Check

- Proposed paths match existing repository conventions when they exist.
- Existing useful code is reused through planned interfaces.
- New structure is scoped to experiment-system needs.
- Config and CLI design follows the local framework when one is already present.

### Harness Quality Check

- Harnesses are tied to paper-relevant performance, quality, cost, robustness,
  or scalability metrics.
- Harnesses isolate one optimization point at a time when possible.
- Allowed modification scope is precise.
- Frozen components make comparisons fair.
- Decision rules identify how a candidate becomes the proposed method or remains
  a baseline.
- Decision rules include numeric thresholds or high-blocking open questions.
- Harness roles separate development, selection, final validation, diagnostics,
  regression, and claim calibration.
- Method-freeze protocol prevents final evaluation from doubling as unrestricted
  tuning data.
- Smoke and full commands are present.

### Raw Export Check

- Per-run metadata and resolved config are exported.
- Metadata files are stored at the run root or under `metadata/`, not under
  `raw/`.
- Per-example records are exported for later slicing.
- Aggregate metrics are exported as convenience summaries.
- Derived quality scores, QoE scores, deltas, rates, and statistical summaries
  are placed under `metrics/`.
- Counterfactuals, simulated alternatives, oracle analyses, and attribution
  records are placed under `analysis/` unless they are explicitly direct oracle
  outputs with provenance.
- No file under `metrics/` appears in a section labeled `Raw outputs`.
- Metric definitions distinguish `Raw required fields`, `Upstream metric
  dependencies`, and `Derived outputs`.
- Table/figure transformations are documented as derivations from raw outputs.
- Core experiment modules are not burdened with paper-specific plotting logic.

### Cross-Reference Integrity Check

- Every module referenced by a harness appears in the Module Plan.
- Every method and baseline has a module path, config path, registry name, role,
  and raw output requirement.
- Every workload suite has a config path, builder path, required factors, and
  used-by harness list.
- Every metric used by a decision rule has a complete metric definition.
- Every paper output maps to raw files, metrics, grouping logic, and a
  downstream artifact.
- Every command references an executable stage and resolvable config key.
- Every generated file path is consistent with the repository layout.
- Raw, metadata, metric, summary, and analysis files follow the export
  classification boundary.
- Final evaluation is separated from unrestricted method tuning.

### Length and Redundancy Check

- Each workload, method, baseline, metric, harness, and paper output is defined
  once in a canonical registry or definition section.
- Later objective maps, harnesses, execution matrices, acceptance criteria, and
  paper derivations reference stable IDs instead of repeating full definitions.
- Harness sections are capped to purpose, module under test, allowed
  modification scope, registry references, command examples, decision rule, and
  failure modes.
- Repeated "raw required fields", "used by harnesses", and "used by paper
  outputs" prose blocks are replaced by compact tables when they restate
  registry information.
- The plan stays near the 6k-8k word target for typical projects, or any excess
  text introduces new implementation obligations.
- Metric entries omit numerator and denominator fields unless the metric is
  ratio-like.
- The explanation summarizes rationale and downstream use instead of duplicating
  the implementation order from `coding_plan.md`.

### Positive Language Check

- The plan states what to build, where to place it, how to call it, and how to
  validate it.
- Placement guidance is written as positive ownership rules such as `Place X
  under path Y` and `Reserve path Z for orchestration assets`.
- Open items are written as assumptions, lookups, or blocking levels.
- Broad disclaimers are replaced by actionable planning commitments.

### Final Self-Audit Before Writing Files

Revise the artifacts until:

- no harness references an undefined module
- no method references an undefined config path or registry name
- no workload references an undefined builder path or config path
- no metric appears in a decision rule without a definition
- no raw file contains derived metrics unless explicitly labeled as cached
  derived metadata with a source field
- no metadata file such as run metadata, resolved config, environment details,
  dependency versions, or source commits is placed under `raw/`
- no counterfactual, simulated alternative, oracle analysis, attribution record,
  or other generated analytical output is placed under `raw/` unless it is
  explicitly classified as a direct oracle output with provenance
- no metric file appears under a `Raw outputs` heading
- no metric definition treats another derived metric as a raw required field
  without listing it under `Upstream metric dependencies`
- no final evaluation harness is also used for unrestricted method tuning
- no command depends on an unstated installation or working-directory assumption
- no paper output lacks a raw-file, metric, grouping, and downstream-artifact
  derivation path
- no optional workload lacks a `core`, `optional-planned`, or `deferred` scope
  status
- no user-language explanation heading remains in English except preserved
  technical identifiers
- no major method/baseline/workload/metric mapping is restated in full after its
  canonical definition
- no harness section repeats full workload/method/metric/output mappings already
  present in registries or the execution matrix
- no placement rule is phrased as a negative prohibition when it can be written
  as a positive ownership rule

## Final Response

After writing the files, summarize:

- paths written
- major plan components
- any high-blocking open questions
- validation performed
