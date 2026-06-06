---
name: academic-army-excellent-repo
description: >-
  Create, complete, or improve a static, low-friction, maintainable research
  code repository from an Academic Army paper blueprint, experiment plan,
  coding plan, and user-specified repository path. Use when Codex must turn
  upstream research planning artifacts into real repository files, directories,
  code interfaces, harness entries, test entries, documentation, configuration,
  and raw-result artifact contracts, or when Codex must revise an existing
  research repository while preserving user work. Use
  academic_army_mcp_tools.deepresearch to choose current language, framework,
  packaging, tooling, and high-quality repository practices at invocation time.
---

# Academic Army Excellent Repo

## Mission

Create or revise a real research code repository under the user-specified
repository path. The repository should be static, orderly, low-friction,
extensible, and maintainable. Treat repository structure quality and code shape
quality as one target:

- Carry forward the paper blueprint, experiment plan, and coding plan into
  concrete files, directories, interfaces, harnesses, tests, and artifact
  contracts.
- Keep code short, direct, clearly named, low-state, low-conversion, and
  minimally layered.
- Preserve existing user files and make the smallest change that satisfies the
  repository goal.

This skill owns repository creation and static framework modification. It does
not run installs, tests, harnesses, experiments, or full execution pipelines.

## Required Inputs

Use the user-specified repository path as the root for all project files. Create,
modify, and reference project files only inside that path. Use repository-relative
paths inside generated documentation and final summaries.

Use only task-relevant input scope:

- Read user-provided paper blueprint, experiment plan, coding plan, and explicit
  constraints.
- If conventional upstream artifact names are present and the user does not
  provide exact paths, locate the closest matching blueprint, experiment plan,
  and coding plan.
- Read existing repository files only when modifying an existing repository or
  when a required input explicitly references them.
- Ignore unrelated drafts, old outputs, logs, notebooks, or nearby files unless
  the user explicitly makes them part of the task.

If an input is missing but a defensible repository skeleton can still be built,
record the assumption in repository documentation and leave precise method or
experiment details as extension points. Ask the user only when the missing fact
would materially change the repository root, selected stack, data contracts, or
research workflow.

## Required DeepResearch

Before creating a new repository or making a substantial repository redesign,
run `academic_army_mcp_tools.deepresearch`.

Use DeepResearch to choose the current stack and repository structure from the
actual task. Do not hardcode a language, framework, package manager, test
runner, source layout, config format, or public repository template into this
skill or into generic tips.

Research should cover:

- high-quality related research repositories, official artifacts, benchmark
  repositories, and paper code
- installable tools with stable interfaces versus tools that are only useful as
  design references
- license and attribution implications when any code or pattern may be copied
- current best practices for the selected language and framework: dependency
  declaration, project structure, configuration, CLI or entrypoint design,
  logging, typing, formatting, linting, testing, and result artifact management
- which structures are ecosystem conventions, which are project-specific, and
  which reduce or increase friction for this repository

Use this prompt shape:

```text
You are supporting a research-code repository builder.

Research brief:
[paper goal, experiment requirements, coding plan, user constraints,
candidate methods, baselines, datasets, metrics, harnesses, tests, and any
existing repository facts]

Return concise repository-building evidence:

- Relevant high-quality repositories or official artifacts and what their
  structure teaches about source layout, configs, harnesses, tests, result
  exports, and documentation.
- Stable installable tools that should be used as dependencies, with reasons.
- Tools or repositories that should only be referenced or carefully reused,
  including license and attribution notes when relevant.
- Current best practices for the selected language and framework, including
  dependency declaration, static quality tooling, entrypoints, configuration,
  test discovery, and artifact organization.
- Friction risks: hidden path assumptions, excessive config, complex build
  steps, unnecessary aliases, repeated registration points, thin wrappers, or
  test/harness calling overhead.
- Repository decisions recommended for this specific paper workflow.
- Source table with title, link, visible date/version/commit when available,
  source role, evidence type, and affected repository decision.
```

When the user already specifies a stack, research best practices for that stack.
When the stack is not specified, select one from the paper workflow, coding plan,
and DeepResearch evidence.

## Repository Layout Principles

Use a hybrid layout:

- Fixed research workflow top-level structure:
  - `data/`: input datasets, traces, manifests, fixtures, or links
  - `output/`: program-run outputs and intermediate artifacts
  - `results/`: experiment result records intended for analysis
  - `harness/`: research harnesses
  - `test/`: functional tests
  - `README.md`: concise repository entry
  - `FRAMEWORK.md`: English framework handoff
  - `FRAMEWORK.zh-CN.md`: Chinese framework handoff
- Dynamic ecosystem structure:
  - source directories, package names, dependency files, build files, config
    files, quality-tool config, and entrypoint organization chosen from the
    selected stack and DeepResearch evidence

Coordinate the fixed research directories with the selected ecosystem structure.
The repository should look natural for the chosen stack while preserving the
research workflow top level.

For `harness/`, create one semantic subfolder per harness. Each harness folder
should identify its research goal, target module or replaceable method area,
input protocol, metrics, result artifacts, and intended development loop.

For `test/`, create one semantic subfolder per test capability. Tests should
cover functional correctness, interface contracts, data formats, config parsing,
metrics, result export, entrypoints, and core module interactions using small
fixtures or mock data. Keep tests separate from paper-goal harnesses.

## Core Repository Content

Create enough real structure that the repository is not an empty shell. Include
only the amount of code needed to establish clear extension points and static
contracts.

Prefer project-specific modules for:

- configuration or parameter parsing
- shared domain objects or schemas
- replaceable method and baseline interfaces
- dataset, workload, trace, or input adapters
- metric computation boundaries
- harness runner boundaries
- raw-first result writing
- static entrypoint semantics

Use placeholder implementations only when the downstream method logic is not yet
owned by this skill. Make placeholders explicit and honest:

- label method adapters, baselines, metrics, loaders, and harnesses as
  placeholders when their algorithmic behavior is not implemented
- state the interface contract and expected behavior
- do not imply that a candidate method, baseline, metric, or experiment result
  has already been implemented or validated

Avoid generic infrastructure that the paper workflow does not need, such as
deployment systems, dashboards, database layers, or distributed orchestration,
unless the upstream plans or DeepResearch evidence make them necessary.

## Documentation Contract

Maintain three root documents:

- `README.md`: short entry document with repository purpose, quick entrypoints,
  and major directories.
- `FRAMEWORK.md`: English framework explanation for downstream coding agents and
  human developers.
- `FRAMEWORK.zh-CN.md`: Chinese framework explanation. Keep conventional module,
  method, metric, command, and code identifiers in English when exact spelling
  matters.

`FRAMEWORK.md` and `FRAMEWORK.zh-CN.md` should describe the actual repository,
not a generic template. Cover:

- how the framework inherits the paper blueprint, experiment plan, and coding
  plan
- why the selected ecosystem structure and source layout fit this project and
  reduce friction
- meaning of the fixed research directories
- core modules, ownership boundaries, interfaces, and data flow
- method and baseline extension points
- harness structure, paper goals served, metrics, raw artifacts, and the
  "modify module -> run harness -> inspect results -> refine module" loop
- testing structure, fixture style, pass/fail purpose, and separation from
  paper harnesses
- raw-first result export schema and downstream use by plotting, paper writing,
  and analysis
- placeholder locations and what later implementation should fill
- real or explicitly reserved entrypoints only

Do not put skill workflow, runtime tool failures, sandbox details, or generation
process commentary into repository files.

## Code Style

Write and revise code in the Academic Army direct style:

- Prefer short, straight-line logic and shallow call chains.
- Add helpers only when they express a stable boundary, remove real duplication,
  or name a meaningful invariant.
- Delete or avoid helpers that only wrap, rename, split, reassemble, or forward
  data.
- Keep local state local. Put shared state only where it is stable across
  module boundaries.
- Name content as content and references as references. Do not let path, handle,
  content, config, result, and status names blur together.
- Keep names aligned across code, config, docs, harnesses, tests, metrics, and
  result artifacts.
- Put related code near its use site unless it is truly shared.
- Order inputs, validation, construction, execution, and output in natural
  reading order.
- Align field order, parameter order, and documentation order for related
  objects.
- Use comments only for non-obvious constraints, placeholder contracts, or
  design decisions that cannot be made clear through naming and structure.

When revising existing code, follow the repository's good local patterns, but do
not preserve bad abstraction, stale naming, misplaced ownership, or unclear
data flow merely for consistency.

## Workflow

1. Confirm the target repository root and keep all project operations inside it.
2. Read only the required upstream planning artifacts and task-relevant existing
   repository files.
3. Run DeepResearch for the selected or candidate stack, related repositories,
   dependencies, harness practices, testing practices, and result artifacts.
4. Form an internal repository decision: selected stack, fixed research
   directories, ecosystem source structure, harness folders, test folders,
   configuration mechanism, interfaces, artifact schema, entrypoints, and static
   quality tooling.
5. Create missing fixed top-level directories and root documents.
6. Create or revise the selected ecosystem structure, dependency declaration,
   static-quality configuration, source interfaces, harness entries, tests,
   fixtures, and result artifact contracts.
7. Preserve existing user work. Apply minimal changes for existing repositories
   and avoid unrelated cleanup.
8. Update `README.md`, `FRAMEWORK.md`, and `FRAMEWORK.zh-CN.md` so their content
   matches the actual repository.
9. Perform static validation only.
10. Respond with a concise summary of created or modified repository abilities,
    extension points, static validation, and any code-level caveats.

## Static Validation

Do not run install commands, tests, harnesses, or experiments. Use static checks
appropriate to the selected stack and repository state.

Validate:

- all created, modified, and referenced project paths are inside the repository
  root
- `data/`, `output/`, `results/`, `harness/`, `test/`, `README.md`,
  `FRAMEWORK.md`, and `FRAMEWORK.zh-CN.md` exist
- the selected ecosystem structure follows DeepResearch-supported best
  practices without unnecessary config or hidden path assumptions
- dependency declarations, configuration entrypoints, source interfaces,
  harness entries, tests, fixtures, and result artifact contracts exist when
  required by the upstream plans
- documentation matches the actual repository structure
- placeholders are clearly labeled and do not pretend to be completed
  algorithms
- harness folders and test folders are semantic and separate
- artifact schemas use stable fields aligned with method, metric, dataset,
  split, seed, harness, and stage names
- names are consistent across docs, code, config, harnesses, tests, and
  artifacts
- code avoids thin wrappers, repeated registration points, unnecessary
  conversions, over-split modules, path aliases, hidden environment assumptions,
  and long calling paths that make harnesses or tests harder to use

## Final Response

Keep the final response short. State:

- the repository-relative paths or capabilities created or modified
- the selected stack and why it fits this project, in one concise sentence
- key extension points for later implementation
- static validation performed
- any remaining project-level caveats

Do not paste full files unless the user explicitly requests it. Do not explain
skill internals, template mechanics, tool failures, or runtime workarounds.
