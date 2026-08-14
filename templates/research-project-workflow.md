# AcademicArmy Research Workflow

Copy this file to the root of a research repository as `ACADEMICARMY.md`, then
replace the placeholders in **Project Identity**. Keep the remainder stable
unless the project has a documented reason to change the workflow.

## Project Identity

- Repository: `[ABSOLUTE PROJECT REPOSITORY PATH]`
- AcademicArmy: `[ABSOLUTE ACADEMICARMY PATH]`
- Working title: `[PROJECT TITLE]`
- Target venue: `[TARGET VENUE]`
- Research domain: `[RESEARCH DOMAIN]`
- Primary research question: `[CENTRAL SCIENTIFIC QUESTION]`
- Available datasets and code: `[CONFIRMED RESOURCES]`
- Compute resources: `[GPU / CPU / STORAGE / CLUSTER]`
- Non-negotiable constraints: `[USER-SPECIFIED CONSTRAINTS]`

Explicit user facts in this file and `idea_brief.md` take precedence over agent
assumptions. Unknown information must remain open rather than being invented.

## Repository Boundary

The current repository is the complete research project and the primary Codex
workspace. AcademicArmy is an external planning and execution engine.

All paper material, source code, experiment configurations, validated results,
and research decisions belong in this repository. Do not place project output
inside the AcademicArmy repository or its default `workspace/codebase`
directory.

AcademicArmy may be read and invoked from the path recorded in **Project
Identity**. Do not modify AcademicArmy unless the current goal explicitly
concerns its skills, agents, or runner.

## Source-of-Truth Artifacts

Maintain these project-level artifacts:

1. `idea_brief.md`
   Confirmed scientific motivation, resources, preliminary observations,
   constraints, and unresolved questions.
2. `paper_blueprint.md`
   Stable paper identity, thesis, claims, novelty boundary, method direction,
   and required evidence.
3. `experiment_plan.md`
   Claim-to-evidence map, datasets, baselines, metrics, ablations, robustness
   studies, and statistical protocol.
4. `coding_plan.md`
   Architecture, interfaces, experiment harness, artifact schemas, tests, and
   reproducibility contract.
5. `evidence_ledger.md`
   Status of every paper claim and the validated evidence supporting it.
6. `STATUS.md`
   Current project state, completed work, active blockers, and the next
   highest-value objective.

Corresponding `*.explain.md` files contain Chinese explanations for user
review. English planning files are execution contracts for downstream agents.

## Initialization Procedure

When asked to initialize this repository:

1. Verify that the current workspace root is this repository.
2. Inspect Git status and existing files without overwriting user work.
3. Read `AGENTS.md`, this file, and `idea_brief.md`.
4. Inspect relevant datasets, source code, documentation, and preliminary
   results already present in the repository.
5. Read the AcademicArmy skills under `[ACADEMICARMY PATH]/skills/`:
   - `academic-army-architect/SKILL.md`
   - `academic-army-experiment-plan/SKILL.md`
   - `academic-army-coding-plan/SKILL.md`
   - `academic-army-literate-latex-writing/SKILL.md`
6. Use current literature research to establish the nearest prior work,
   scientific gap, venue expectations, datasets, and credible baselines.
7. Generate or revise `paper_blueprint.md` and
   `paper_blueprint.explain.md`.
8. Once the paper strategy is coherent, generate or revise
   `experiment_plan.md` and its explanation.
9. Generate `coding_plan.md` only after claims and evidence requirements are
   sufficiently stable.
10. Scaffold or adapt the implementation around the approved plans and the
    target ecosystem already present in the repository.
11. Create a reproducible environment and run a minimal smoke test.
12. Record the verified state and next objective in `STATUS.md`.

Do not start expensive experiments during initialization. First verify the
environment, data access, metric implementation, and one minimal end-to-end
execution path.

## Recommended Repository Layout

```text
project/
|-- AGENTS.md
|-- ACADEMICARMY.md
|-- idea_brief.md
|-- paper_blueprint.md
|-- experiment_plan.md
|-- coding_plan.md
|-- evidence_ledger.md
|-- STATUS.md
|-- src/
|-- configs/
|-- harness/
|-- tests/
|-- scripts/
|-- data/
|   |-- README.md
|   `-- manifests/
|-- output/
|-- results/
|   |-- validated/
|   |-- tables/
|   `-- figures/
|-- paper/
|-- goals/
|   |-- current.md
|   `-- archive/
`-- .academicarmy/
```

## Experiment Contract

Use the following separation:

- `data/`: manifests and local dataset access; large datasets remain ignored.
- `configs/`: versioned experiment and baseline configurations.
- `harness/`: orchestration, baseline adapters, evaluation, and artifact
  validation.
- `output/`: unvalidated run artifacts; ignored by Git.
- `results/validated/`: checked paper-facing evidence; committed to Git.
- `results/tables/`: generated tables.
- `results/figures/`: generated scientific figures.
- `paper/`: manuscript, bibliography, supplementary material, and paper assets.

Every run must record:

- run identifier and Git commit;
- dataset manifest and version;
- exact configuration and command;
- environment and compute information;
- random seed when applicable;
- start time, completion status, and failure reason when relevant;
- raw artifact location and checksums when needed;
- metric summary and validation status.

Paper numbers must originate from validated result artifacts. Do not manually
invent, estimate, or silently replace results in the manuscript.

## Development Loop

The current objective lives in `goals/current.md`. Each objective must identify:

- the paper claim it serves;
- the evidence gap it closes;
- the implementation and validation scope;
- expected artifacts;
- completion criteria;
- commands that must pass.

Invoke AcademicArmy with this repository as `--target-path`. Store generated
agent memory and archives under `.academicarmy/`. Keep durable scientific state
in committed planning files, the evidence ledger, validated results, and the
goal archive.

Recommended runner mapping:

```text
--target-path                    [PROJECT REPOSITORY PATH]
--archive-root                   [PROJECT]/.academicarmy/archives
--project-progress-memory-path   [PROJECT]/.academicarmy/project-memory
--code-design-memory-path        [PROJECT]/.academicarmy/code-memory
--goal-path                      [PROJECT]/paper_blueprint.md
--goal-path                      [PROJECT]/experiment_plan.md
--goal-path                      [PROJECT]/coding_plan.md
--goal-path                      [PROJECT]/goals/current.md
```

## Evidence Ledger Contract

Organize `evidence_ledger.md` by claim rather than by chronological run:

```text
Claim ID and paper statement
Required evidence
Completed experiments
Validated result artifacts
Statistical status
Paper table, figure, or section destination
Remaining evidence gap
```

Failed and negative experiments remain part of the scientific record. They may
redirect the method or claim, but must not be silently removed from project
history.

## Writing Contract

Start the manuscript structure early while distinguishing proposed claims from
validated claims. Before materially rewriting the paper, read:

- `paper_blueprint.md`;
- `evidence_ledger.md`;
- `results/validated/`;
- the current manuscript.

Use `academic-army-literate-latex-writing` for manuscript generation and major
revisions so prose remains connected to the blueprint and validated evidence.

Preserve the established high-level contribution unless new evidence supports
a documented strategic revision. Frame the work around the largest scientific
problem supported by the evidence. Avoid defensive prose, component-list
narrative, fabricated generality, and claims disconnected from validated
results.

Tables and figures should be reproducibly generated from validated artifacts
whenever possible. Record manual visual editing and source assets when a figure
cannot be generated entirely by code.

## Git and Data Rules

- Keep `main` runnable and the paper compilable.
- Use focused branches for experiments or substantial manuscript revisions.
- Bind every promoted result to a Git commit and dataset manifest.
- Do not commit raw datasets, secrets, machine-specific paths, large model
  checkpoints, or unvalidated run directories.
- Add `.academicarmy/` to the target repository's `.gitignore`; agent memory
  and development archives are recoverable runtime state, not scientific truth.
- Pin external repositories or dependencies to explicit versions or commits.
- Never revert unrelated user changes.

## Completion Standard

A task is complete only when:

- the requested implementation or writing change is present;
- focused tests or validations pass;
- output artifacts are inspectable;
- provenance is recorded;
- `evidence_ledger.md` is updated when evidence changes;
- `STATUS.md` records the new state and next highest-value step;
- no required process remains running.

## First-Session Prompt

Use this prompt after opening Codex from the target repository root:

```text
Read AGENTS.md, ACADEMICARMY.md, and idea_brief.md. Initialize this research
repository using the AcademicArmy skills at the path specified in
ACADEMICARMY.md.

Treat this repository as the only project output location. Inspect existing
work first. Establish the paper strategy through current literature research,
then create the paper blueprint, experiment plan, and coding plan in dependency
order. Scaffold the environment and finish with one minimal end-to-end smoke
test. Do not launch expensive experiments yet. Record the verified state and
next objective in STATUS.md.
```
