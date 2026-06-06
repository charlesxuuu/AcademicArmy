# Repo Init Contract

Use this reference when `SKILL.md` needs more detail. Keep generated repositories
paper-driven, target-path scoped, statically checkable, and free of generic
template clutter.

## Input Scope

Read only:

- paper blueprint
- experiment plan
- coding plan
- user-specified target repository path and explicit constraints
- initialization-relevant files already inside the target repository

Ignore nearby drafts, logs, old outputs, unrelated repositories, and historical
artifacts. If the target path already has content, preserve it and make only
minimal initialization edits.

## Repository Shape

Always keep the fixed experiment inventory at the target root:

```text
data/
output/
results/
harness/
test/
README.md
FRAMEWORK.md
FRAMEWORK.zh-CN.md
```

Select the language-specific structure after reading the plans and research
evidence. Source layout, package name, dependency file, build system, config
format, entrypoint style, linter, formatter, type checker, and test framework
are dynamic choices. Configure test discovery to use top-level `test/`.

Use semantic names from the paper, experiment plan, and coding plan. Avoid
abstract numbering such as `c1`, `b2`, `h3`, or `t4`.

## DeepResearch Use

Run one domain/tooling lookup before creating files and one focused ecosystem
lookup after choosing a likely language/framework. Capture decisions, not long
literature summaries:

- related engineered repositories and benchmark harnesses worth learning from
- packaged tools suitable as dependencies
- repositories useful only as structural references, with license cautions
- official or well-maintained ecosystem practices for project layout, CLI,
  configs, logging, tests, static checks, and raw artifacts
- adopt/reject rationale tied to this paper task

Use research evidence to adapt a structure. Do not copy a public repository
tree mechanically.

## Minimum Scaffold Logic

Create enough real code for the next coding skill to continue:

- configuration loader or parser
- domain records or schema objects
- method/baseline interface
- loader or substrate adapter boundary
- metric contract
- harness-shaped entrypoint or runner boundary
- raw artifact writer or schema validator
- small fixture or mock input
- functional test entrypoints
- dependency and static-quality configuration

Do not implement final methods, custom optimization, full metrics, real external
system integrations, plotting, training, experiments, CI, dashboards, databases,
services, or distributed infrastructure unless the planning artifacts require
them.

## Harness Contract

Each `harness/<semantic-name>/` must state or encode:

- paper claim, experiment question, method-selection question, ablation, stress
  condition, or reproducibility goal
- target module and allowed modification scope
- input protocol and sample/mock input location
- compared methods, baselines, ablations, or oracles when known
- metric names and decision direction when known
- raw artifact classes and minimum fields

Harnesses produce raw, parseable evidence: decisions, predictions, scores,
timings, resource usage, intermediate states, errors, config snapshot, method,
dataset, split, seed, and metric values. Figure/table generation belongs
downstream.

## Test Contract

Each `test/<semantic-name>/` must state or encode:

- functional behavior under test
- target module/interface/config/CLI/export/metric contract
- toy input or fixture
- expected behavior, output schema, or expected exception
- pass/fail criterion

Tests validate correctness. Harnesses evaluate research goals.

## Artifact Contract

Prefer raw-first schemas with stable names from the plans. Common fields:

- run, harness, stage, method, baseline, dataset, split, seed
- example/frame/query id
- decision, prediction, score, timing, resource, error, or lifecycle fields
- metric name, value, direction, and status
- config snapshot or source metadata reference

Each schema should have a purpose, producer, granularity, required fields,
format tendency such as JSONL/JSON/CSV/Parquet, downstream consumer, and static
validation rule.

## Placeholder Contract

A placeholder is valid only if it is useful to a future implementer. It must
make clear:

- owning interface
- accepted inputs
- required output type
- artifact fields it must emit
- harness or test that will exercise it
- intentionally absent behavior

Raise a clear error or emit a clearly labeled placeholder record. Do not make
stub logic look like a completed method, metric, baseline, harness, or adapter.

## Documentation Contract

`README.md` stays brief: purpose, quick entrypoint semantics, and top-level
directory map.

`FRAMEWORK.md` and `FRAMEWORK.zh-CN.md` are handoff docs. They describe only
real generated paths, commands, modules, interfaces, harnesses, tests,
placeholders, artifact schemas, dependency choices, copied-code status, and
extension points. Use repo-relative paths only.

Do not include skill internals, sandbox notes, command failures, absolute local
paths, or generic template explanations.

## Self-Audit Manifest

Create `output/repo-init-self-audit.json` or an equivalent compact manifest
with:

- required top-level path status
- documented paths and existence status
- harness/test/module/config/artifact inventory
- placeholder contracts
- dependency/layout rationale tied to research and paper needs
- artifact schema fields and consistency locations
- copied-code attribution status
- docs-relative-path status
- unrelated-infrastructure status
- duplication-pass status
- static-validation status

## Duplication Pass

Before final validation, remove or justify:

- empty files except ecosystem markers such as `py.typed` or `.gitkeep`
- repeated documentation sections
- placeholder files without distinct semantic roles
- forwarding-only helpers
- duplicate registries/adapters for the same boundary
- duplicate schema/type definitions
- duplicate harness/test descriptions without distinct goals
- generic infrastructure unrelated to the plans
- sample modules not connected to a harness, test, config, or artifact schema

## Static Validation

Prefer:

```bash
python skills/academic-army-repo-init/scripts/repo_init_audit.py <target-repo>
```

Equivalent manual static validation must check fixed paths, docs, documented
paths, self-audit, syntax or parseability, `test/` discovery, honest
placeholders, raw artifact schema consistency, attribution, and redundancy.

Never run installs, tests, harnesses, experiments, training, benchmark
downloads, project CLI runtime commands, or notebooks as repo-init validation.
