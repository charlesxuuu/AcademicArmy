---
name: academic-army-coding-plan
description: >-
  Create an English coding_plan.md and a user-language coding_plan.explain.md
  from a paper blueprint, experiment plan, repository context, candidate
  methods, baselines, datasets, metrics, and paper-result requirements. Use
  when Codex needs to translate research and experiment requirements into a
  modular implementation plan with replaceable method/baseline locations,
  staged CLI execution, optimization/evaluation harnesses, validation checks,
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

## Research Tool

Use `academic_army_mcp_tools.deepresearch` when current or method-specific
external information affects the coding plan.

- Server: `academic_army_mcp_tools`
- Tool: `deepresearch`
- Canonical Codex MCP name when exposed:
  `mcp__academic_army_mcp_tools__deepresearch`

Use live research for:

- canonical implementation details of candidate methods and baselines
- current benchmark protocols, dataset schemas, or metric definitions
- recent repositories, model APIs, datasets, leaderboards, or artifact
  conventions
- unclear terminology from the blueprint or experiment plan
- current evaluation-harness or experiment-tracking patterns that affect the
  plan

Put only planning consequences in `coding_plan.md`. Put source provenance,
uncertainty, and rationale in `coding_plan.explain.md` when it helps the user
review the plan.

Use this prompt shape when live research is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a coding-plan generator for a research paper.

Research brief:
[paper goal, system, candidate methods, baselines, datasets, metrics, and
experiment-plan requirements]

Return concise implementation-planning evidence:

1. Canonical implementation shape for each method or baseline.
2. Current benchmark or dataset protocol details that affect loaders,
   evaluators, metrics, or comparators.
3. Existing repository/artifact conventions worth matching.
4. Evaluation harness implications: controllable variables, frozen components,
   smoke/full protocols, metrics, and decision rules.
5. Raw result fields needed for later tables, figures, and paper claims.
6. Source table with title, link, date or version when visible, role, and the
   planning decision it affects.
```

## Planning Boundary

The coding plan is an engineering contract, not a code implementation.

Plan these items:

- package layout and module boundaries
- public interfaces and adapter contracts
- config structure and CLI override model
- candidate method and baseline placement
- staged experiment pipeline
- optimization/evaluation harnesses
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

## Workflow

### 1. Inventory Research and Experiment Requirements

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

### 2. Inspect Repository Context

Identify:

- current package layout
- existing data-loading, method, model, evaluation, configuration, logging,
  script, test, and notebook conventions
- reusable modules and gaps
- natural package name and command entry point
- current dependency stack and likely framework choices
- existing artifact and result directories

If the repository already has conventions, align the plan with them. If no
implementation structure exists, propose a clean layout that downstream coding
can create.

### 3. Design Replaceable Methods and Baselines

Every candidate method and baseline from the blueprint or experiment plan gets
a stable code location and config location.

For each method or baseline, specify:

- name
- role: `naive_baseline`, `candidate_method`, `modified_candidate`,
  `proposed_method`, `ablation_variant`, `oracle`, or `diagnostic_baseline`
- proposed module path
- config path
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

### 4. Design the Staged Experiment System

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

### 5. Design Harnesses

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
- Research question
- Optimization target
- Module under test
- Public interface and config group
- Allowed modification scope
- Frozen modules and dependencies
- Candidate methods, naive baselines, modified variants, and ablations covered
- Smoke dataset, full dataset, splits, seeds, and budget
- Primary selection metric
- Secondary metrics
- Guardrail metrics
- Required statistical summary
- Smoke command
- Full command
- Sweep command when useful
- Raw output files and required fields
- Decision rule for promotion, rejection, or further modification
- Failure modes to monitor
- Downstream implementation tasks

Harness decision rules should be concrete enough for iterative coding:

```text
Promote the modified variant with the highest mean <primary_metric> across
seeds, subject to <guardrail_metric> staying within <threshold> of the strongest
naive baseline. Keep unmodified variants as baselines for final experiments.
```

### 6. Design Raw-First Result Export

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
    raw/
      predictions.jsonl
      examples.jsonl
      events.jsonl
      timings.jsonl
      costs.jsonl
    metrics/
      aggregate_metrics.json
      per_slice_metrics.jsonl
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

Plan raw per-example records before high-level summaries. Keep table/figure
transformations as documented derivations from raw files so later plotting and
paper-writing skills can transform the data without depending on experiment
system internals.

### 7. Design Validation and Acceptance Checks

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

The downstream coding skill should be able to turn these checks into tests,
scripts, or CI commands.

### 8. Write `coding_plan.md`

Use this structure. Omit sections only when they are genuinely inapplicable and
state the reason under `Planning Assumptions`.

```markdown
# Coding Plan: <Paper/System Name>

## 1. Scope and Planning Assumptions

## 2. Repository Context

## 3. Research Requirements Inventory

## 4. Target System Architecture

## 5. Module Plan

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

## 6. Method and Baseline Placement

For each method or baseline:
- Name
- Role
- Proposed module path
- Config path
- Adapter/interface
- Replaceability boundary
- Used by experiments
- Used by harnesses
- Raw outputs required

## 7. Experiment Stages and CLI Plan

For each stage:
- Stage name
- Command
- Inputs
- Outputs
- Config overrides
- Idempotency/caching
- Failure checks
- Smoke/full mode

## 8. Harness Plan

For each harness:
- Harness ID
- Name
- Research question
- Optimization target
- Module under test
- Allowed modification scope
- Frozen modules
- Candidates
- Baselines
- Metrics
- Smoke command
- Full command
- Raw output schema
- Decision rule
- Downstream coding tasks

## 9. Raw Result Export Contract

## 10. Deriving Paper Results from Raw Outputs

For each table, figure, qualitative example, or claim:
- Required raw files
- Grouping/filtering logic
- Metrics or derived quantities
- Expected downstream artifact

## 11. Implementation Order for the Coding Skill

## 12. Acceptance Criteria

## 13. Open Questions and Research Lookups

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
- Every candidate method can be selected through a shared interface, registry,
  adapter, or config group.
- Every complex experiment has smoke and full execution commands.
- Every harness defines an optimization point, modification scope, metrics, raw
  outputs, and decision rule.
- Every required paper table, figure, qualitative example, or claim has a
  derivation path from raw outputs.
- The implementation order builds from infrastructure to data, methods,
  baselines, harnesses, proposed variants, full experiments, and validation.

### Harness Entry Schema

Use this schema inside `coding_plan.md` for each harness:

```markdown
### Harness <ID>: <Name>

**Research question:**  
<What optimization or method-selection question this harness answers.>

**Optimization target:**  
<The exact algorithmic or module-level behavior to improve.>

**Module under test:**  
- Path:
- Interface:
- Config group:

**Allowed modification scope:**  
- Files/directories:
- Config keys:
- Method internals:

**Frozen system components:**  
- Data loader:
- Preprocessing:
- Evaluator:
- Logger:
- External model/API:
- Prompt/template if applicable:

**Candidates and baselines:**  
- Candidate methods:
- Naive baselines:
- Modified variants:
- Ablation variants:

**Evaluation protocol:**  
- Smoke dataset:
- Full dataset:
- Splits:
- Seeds:
- Budget:
- Caching policy:

**Metrics:**  
- Primary selection metric:
- Secondary metrics:
- Guardrail metrics:
- Required statistical summary:

**Commands:**  
- Smoke:
- Full:
- Sweep:

**Raw outputs:**  
- Required files:
- Required fields:
- Run metadata:
- Per-example records:
- Aggregate records:

**Decision rule:**  
<Exact rule for promotion, rejection, or further modification.>

**Failure modes:**  
- Metric artifacts:
- Data leakage:
- Instability across seeds:
- Latency/cost regressions:
- Invalid comparison risks:

**Downstream implementation tasks:**  
1. ...
2. ...
3. ...
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

### Raw Export Entry Schema

Use this schema for each raw output file:

```markdown
### `<path>`

- Purpose:
- Producing stage:
- Required fields:
- Granularity: run | dataset | seed | example | event | slice
- Consuming downstream skill:
- Paper result derivations:
- Validation checks:
```

### Paper Result Derivation Schema

Use this schema for each required paper result:

```markdown
### <Table/Figure/Claim ID>: <Name>

- Paper role:
- Required raw files:
- Grouping/filtering:
- Derived quantities:
- Statistical summary:
- Expected downstream artifact:
- Notes for plotting/writing skill:
```

### 9. Write `coding_plan.explain.md`

Write in the user's conversation language. Preserve method names, dataset names,
metric identifiers, file paths, command names, and code identifiers exactly.

Use this structure, localized into the user's language:

```markdown
# Coding Plan Explanation: <Paper/System Name>

## 1. Inputs Read and Requirement Extraction

## 2. Main Architectural Decisions

## 3. Method and Baseline Placement Rationale

## 4. Experiment Stage Rationale

## 5. Harness Design Rationale

## 6. Raw Result Export Rationale

## 7. Assumptions and Uncertainty

## 8. How the Downstream Coding Skill Should Use the Plan
```

The explanation should make the plan reviewable. Include:

- which local files or user-provided contents were read
- what requirements were extracted
- why modules were separated this way
- why methods and baselines are represented as replaceable components
- why each harness exists and how it supports method selection or optimization
- why the raw export contract is enough for later figures, tables, and paper
  claims
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
- `coding_plan.explain.md` uses the user's conversation language.
- The filenames are exactly `coding_plan.md` and `coding_plan.explain.md`.

### Completeness Check

- Every experiment-plan requirement is represented in the plan.
- Every candidate method and baseline has a module path and config path.
- Every method/baseline uses a shared replaceability boundary.
- Every complex experiment has staged CLI commands.
- Every harness has target module, modification scope, frozen dependencies,
  metrics, commands, raw outputs, and decision rule.
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
- Smoke and full commands are present.

### Raw Export Check

- Per-run metadata and resolved config are exported.
- Per-example records are exported for later slicing.
- Aggregate metrics are exported as convenience summaries.
- Table/figure transformations are documented as derivations from raw outputs.
- Core experiment modules are not burdened with paper-specific plotting logic.

### Positive Language Check

- The plan states what to build, where to place it, how to call it, and how to
  validate it.
- Open items are written as assumptions, lookups, or blocking levels.
- Broad disclaimers are replaced by actionable planning commitments.

## Final Response

After writing the files, summarize:

- paths written
- major plan components
- any high-blocking open questions
- validation performed
