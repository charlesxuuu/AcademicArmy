---
name: academic-army-repo-scaffold
description: >-
  Initialize scaffold-only research code repositories for the Academic Army
  autoresearch workflow from a paper_blueprint, experiment plan, coding plan,
  and user-specified repository path. Use when Codex needs to create or adapt a
  repository skeleton with fixed experiment directories, template-informed
  project structure, README files, REFERENCES files, and reserved harness/test
  folders without implementing methods, experiments, metrics, runners, loaders,
  exporters, or business logic.
---

# Academic Army Repo Scaffold

## Purpose

Initialize a research repository scaffold from upstream Academic Army planning
artifacts. This skill owns the repository template layer only: directory
structure, placeholder documentation, template provenance, and clear handoff
surfaces for later implementation skills.

Do not implement the paper method, experiment workflow, data loaders, metrics,
result exporters, harness logic, tests, configuration parsing, or runners. Do
not install dependencies, run code, run tests, run harnesses, or execute
experiments.

## Required Inputs

Require a user-specified target repository path. If the path is missing, ask for
that path before creating files.

Use only the inputs needed to scaffold the repository:

- `paper_blueprint`
- experiment plan
- coding plan
- explicit user constraints about language, framework, template, repository
  path, or existing repository adaptation

If explicit paths are provided, read those files. Otherwise locate the closest
conventional planning artifacts by name, then stop. Do not explore unrelated
nearby files, logs, source trees, notebooks, dependency manifests, or old
outputs merely because they are present.

Read files inside the target repository only when the user explicitly asks to
initialize or adapt an existing repository, or when a needed scaffold file
already exists and must be preserved.

## Hard Boundaries

Keep every created or modified file under the target repository path. Use
absolute path resolution before writing, and reject any path that escapes the
target repository. Inside repository documents, use paths relative to the
repository root.

Protect existing user content:

- Create missing scaffold files and folders.
- Merge or minimally update existing scaffold documentation when safe.
- Avoid overwriting non-placeholder content.
- Ask before destructive replacement when preservation is ambiguous.

Keep runtime mechanics out of generated repository documents. Do not write
about sandbox limits, shell failures, MCP failures, dependency installation
problems, local permission workarounds, or file-access troubleshooting unless
the user explicitly asks for operational notes outside the scaffold.

## Required DeepResearch

Run `academic_army_mcp_tools.deepresearch` before choosing the dynamic template
or ecosystem structure, unless the current task includes a fresh, directly
relevant lookup artifact.

Use DeepResearch to study current, high-quality examples of:

- project template tools and template repositories
- research code repositories in the paper's domain
- benchmark or harness repositories with clear evaluation organization
- experiment-project layouts and test/harness separation patterns
- relevant language/runtime ecosystem conventions

Treat tools such as Cookiecutter, Copier, GitHub template repositories, Yeoman,
or framework-specific starters as research seeds only. Do not hardcode any one
tool, language, framework, package manager, test framework, config filename, or
source layout into this skill. Select at invocation time based on the paper,
experiment plan, coding plan, user constraints, template quality, license
clarity, community adoption, maintainability, and downstream implementation
cost.

Prefer sources with clear license, active maintenance, simple structure, strong
relevance to the target experiment workflow, and enough maturity to guide a
future implementation. Do not copy code or template files from unclear,
incompatible, stale, overcomplicated, or irrelevant sources.

Use a prompt like:

```text
Research repository scaffolding options for an Academic Army research-code
project.

Project context:
[paper goal, field, candidate methods, experiment plan harness needs, coding
plan logical modules, explicit language/framework/template preferences, target
repository constraints]

Return concise scaffold-planning evidence:
- high-quality related research repositories, benchmark repositories, harness
  projects, and template repositories
- template or ecosystem structure lessons relevant to this project
- license, version, commit, or release information when visible
- which files or structural ideas are safe to reuse, adapt, or only cite
- recommended scaffold shape for this project, separating fixed experiment
  directories from language/ecosystem-specific structure
```

## Scaffold Design

Use a hybrid layout:

- fixed experiment directories and documentation required for every scaffold
- dynamic language, runtime, dependency, build, source, script, and test
  ecosystem structure selected from user input and DeepResearch

Always create or preserve these top-level entries:

- `data/`: input data and future dataset assets
- `output/`: program run outputs and intermediate artifacts
- `results/`: experiment result records and paper-facing summaries
- `harness/`: all research/evaluation harnesses
- `test/`: all functional test categories
- `README.md`: English repository overview
- `README.zh-CN.md`: Chinese repository overview
- `REFERENCES.md`: English provenance and external references
- `REFERENCES.zh-CN.md`: Chinese provenance and external references

The fixed directories define top-level experiment workflow semantics only. Do
not use this skill to prescribe a universal source layout. Let the project
language, runtime, template, and downstream implementation needs determine any
additional source directories or ecosystem files.

When a selected template provides useful base files, keep only files that are
necessary for this scaffold and whose license is clear. Trim unrelated sample
apps, demo code, business logic, example algorithms, metric implementations,
data loaders, runners, result exporters, and experiment scripts.

## Harness And Test Placeholders

Derive harness categories from the experiment plan and coding plan. Create one
semantic subfolder under `harness/` for each harness. Use readable names that
state the task, such as `candidate-method-selection` or
`full-system-robustness`, not abstract labels such as `c1`, `c2`, `b1`, or
`h3`.

Each harness subfolder must contain a short explanation file. Use `README.md`
unless an existing repository convention clearly uses another single
documentation filename. The explanation must describe:

- harness purpose
- associated experiment goal or paper claim
- future entrypoint that should be implemented later
- expected inputs
- expected metrics
- expected output artifacts
- implementation placeholder and ownership boundary

The harness explanation describes reserved structure only. It must not include
working harness code or imply the harness is implemented.

Derive test categories from the coding plan's testing structure. Create one
semantic subfolder under `test/` for each test category. Use names such as
`data-loading`, `metric-computation`, `result-export`, or `cli-smoke`, not
abstract IDs.

Each test subfolder must contain a short explanation file. Use `README.md`
unless an existing repository convention clearly uses another single
documentation filename. The explanation must describe:

- functional behavior to validate
- future fixtures or toy inputs
- expected outputs or exceptions
- pass/fail meaning
- harness or implementation area protected by the tests
- implementation placeholder and ownership boundary

The test explanation describes reserved structure only. It must not include
working test code or imply the tests are implemented.

## README Contract

Create both `README.md` and `README.zh-CN.md`.

`README.md` is English. `README.zh-CN.md` is Chinese. Both should describe the
actual generated scaffold, not a generic template, and should cover:

- project purpose and upstream planning inputs
- fixed top-level directories and their intended use
- selected template, language/runtime, or ecosystem structure
- current scaffold tree at a concise level
- reserved harness and test locations
- what later implementation skills should fill in
- scaffold-only boundary

Do not claim that the paper method, experiment pipeline, harnesses, tests,
metrics, loaders, exporters, or runners already work.

## REFERENCES Contract

Create both `REFERENCES.md` and `REFERENCES.zh-CN.md`.

`REFERENCES.md` is English. `REFERENCES.zh-CN.md` is Chinese. They do not need
to be literal translations, but they must cover the same provenance:

- project or tool name
- link
- license
- version, release, or commit when visible
- what was referenced: template source, structure pattern, harness
  organization, test organization, dependency candidate, or later
  implementation reference
- why it was selected or rejected
- whether anything from the source was retained, adapted, or only cited

If a template tool or repository generates the scaffold, record it explicitly
with license and visible version or commit. If template files are retained or
rewritten, state which source they came from and what scaffold-level changes
were made.

If DeepResearch finds useful external implementation code, cite it as a future
implementation reference only. Do not copy or port implementation code during
this scaffold stage.

## Workflow

1. Confirm the target repository path and resolve it to an absolute path.
2. Read the paper blueprint, experiment plan, coding plan, and explicit user
   constraints only.
3. Extract scaffold requirements: experiment types, harness categories, test
   categories, input data expectations, output/result artifact families,
   candidate language/runtime signals, and downstream implementation needs.
4. Run DeepResearch for template, repository, harness, and ecosystem lessons.
5. Choose a scaffold approach: template-generated, template-adapted, or
   manually assembled from documented patterns.
6. Create or minimally update fixed top-level directories and required
   bilingual documents.
7. Create semantic `harness/` and `test/` subfolders with explanation files.
8. Add only necessary dynamic ecosystem files or folders from the selected
   scaffold approach.
9. Trim unrelated template residue and avoid any concrete business logic.
10. Run static scaffold validation.

## Static Validation

Perform static checks only. Do not lint, format, type check, install
dependencies, run tests, run harnesses, run scripts, or execute experiments.

Confirm:

- every created or modified path is inside the target repository
- `data/`, `output/`, `results/`, `harness/`, and `test/` exist
- `README.md`, `README.zh-CN.md`, `REFERENCES.md`, and
  `REFERENCES.zh-CN.md` exist
- each harness has one semantic subfolder and an explanation file
- each test category has one semantic subfolder and an explanation file
- README files match the actual scaffold and do not describe unimplemented
  functionality as complete
- REFERENCES files record sources, links, licenses, versions or commits when
  visible, reference roles, and reuse/adaptation choices
- README and REFERENCES agree with the actual directories, template source, and
  harness/test placeholders
- generated docs focus on scaffold, template source, and downstream handoff

## Final Response

Summarize:

- target repository path
- scaffold files and directories created or updated
- template or reference sources adopted
- harness and test placeholders reserved
- static validation performed
- important preservation decisions or skipped overwrites
- next implementation handoff point

Keep the response focused on scaffold capabilities and handoff. Do not present
dependency installation, runtime execution, test results, or experiment results
unless the user explicitly requested separate operational work outside this
skill.
