---
name: academic-army-coding-style
description: >-
  Maintain clean, local, low-coupling code trajectories in existing research
  repositories. Use when Codex writes or edits code, refactors modules,
  implements features, harnesses, tests, methods, baselines, metrics, result
  exports, or framework docs. This skill does not initialize template
  repositories or generate full project scaffolds from empty directories.
---

# Academic Army Coding Style

## Mission

Use this skill as a code-quality and framework-consistency layer for an
existing repository. The upstream task decides what to build; this skill decides
how to keep the implementation readable, local, low-coupling, testable, and
consistent with the current framework.

Do not use this skill to initialize a repository template or recreate a project
scaffold from an empty directory. Repository initialization is out of scope. This
skill may add files, modules, tests, harness support, or docs only when the
current task and current repository need them.

## Operating Boundary

Use the user-specified repository root as the project boundary. Do not create,
modify, or reference project files outside that root unless the user explicitly
asks.

Respect the existing source layout, naming style, language ecosystem, tests,
harnesses, docs, and project configuration. Improve local structure when it
makes the current change clearer or safer, but do not redesign the whole
repository because a plan describes future systems.

Ignore unrelated drafts, logs, historical outputs, old runs, and nearby files
unless the user makes them part of the task.

Keep these experiment directories when they already exist:

- `data/`: input data, pointers, traces, manifests, fixtures, or samples.
- `output/`: program-run outputs and intermediate artifacts.
- `results/`: experiment results and curated artifacts.
- `harness/`: harness code, contracts, configs, schemas, samples, and support.

Do not force a fixed test directory. Tests follow the repository's existing
layout, project configuration, initialization docs, or adjacent test style.

### Task Claims vs. Worktree Reality

**Treat the task's stated current-state as a claim to verify, not as ground truth.**
Before acting, check each factual premise against the worktree: the paths,
importability, or artifacts the task asserts as present or absent. When the
worktree contradicts the task, surface the contradiction first and re-scope the
remaining work to the real gap. Do not proceed on a stale premise to manufacture
work the worktree already satisfies.

This is the most important guardrail in the skill. A task brief may be written
against stale memory, an earlier snapshot, or a plan that was since executed.
Trust the worktree; memory files and task narratives are secondary.

#### Already-Complete-on-Disk Sequence

When the worktree already satisfies the task's stated objective, the task is an
**already-complete-on-disk** case — it was executed in a prior session but the
memory/trajectory layer was never advanced. The correct sequence is
verification, not re-implementation:

1. **Inspect** target files, directories, and shims to confirm on-disk state
   matches the task objective.
2. **Run scoped verification** the task requests (test suite, import smoke,
   whitespace check). Record exact pass/fail counts that are **from this
   session's rerun**, not copied from a prior slice entry or task narrative.
   Each slice entry in memory must carry re-verified counts.
3. **Update all lagging memory/trajectory files** to record the verified
   state — flip phase status, record exact test counts, shim identities,
   import findings, and advance the stale selection pointer. This is the
   primary deliverable in already-complete-on-disk cases. When memory-file
   paths referenced by the task do not exist on disk, create the directory
   chain and the files — an absent directory is a missing scaffold, not a
   blocker.
4. Do not re-execute structural work just because memory says it was never
   done. Memory is the stale surface; the worktree is the source of truth.

#### Multi-File Memory Quorum

When a project tracks the same counter or phase in multiple independent memory
files (e.g. a design-memory file, a status file, and a validation file), and
some are already correct while others lag, the **correct file is the quorum
anchor**, not the task brief alone. The pattern:

- **Identify the split**: one file may already show "N completed, M remaining"
  while others still read "N-1 completed, M+1 remaining" and lack the latest
  slice entry. The task brief may even document this drift explicitly.
- **Verify against the worktree**: the on-disk state (clean `git status`,
  absent shim, passing suite) confirms which files are correct. The worktree
  is always the final arbiter.
- **Update the lagging files**: bring them to the same counter, add the
  missing slice entry with this-session rerun counts, and remove the completed
  subject from every "remaining"/"next"/tier list they contain. Do not treat
  the lagging files as evidence that work is unfinished — they are the stale
  surface; the worktree plus the correct memory file form the quorum.
- **After updating, all memory files must agree** on the counter, the
  completed-slice list, and what the next real gap is. Any file that still
  lists a completed subject as "remaining" will cause the next agent to
  re-execute already-done work.

#### Bytecode and Order-Dependent Checks

Before running the import smoke in an already-complete-on-disk case, **clear
`__pycache__`** directories that may hold bytecode from a prior session.
Stale `.pyc` files can make an import smoke silently resolve against old paths,
masking a real resolution failure. Use the language's normal bytecode-cache
clearing mechanism (e.g. `find . -type d -name __pycache__ -exec rm -rf {} +`).

**Order-dependent test results**: a test suite that passes when modules load in
one order (e.g. alphabetical) may fail in another (e.g. entrypoint-first).
After a move that creates or repoints shims, always probe the entrypoint
import order in addition to the test suite. Isolated import probes catch
order-dependent partial-init failures that the test runner may dodge.

## Runtime Binding

Keep the skill project-agnostic. Bind names, paths, classes, functions,
datasets, methods, metrics, harnesses, artifact fields, and validation commands
from the current user request, current goal or reference context, current
repository, and existing code.

Do not carry project facts from one run into the skill. If a rule contains a
real path, symbol, dataset, method, harness, test name, artifact field, or
paper-specific claim, generalize it into a principle or remove it.

Use placeholders only for examples, such as `<method_name>`, `<metric_name>`,
`<harness_name>`, `<module_name>`, and `<artifact_type>`. Examples are
illustrative, not fixed templates.

## Pre-Edit Inventory

Before editing, establish a small task-relevant inventory:

- repository root and version-control root;
- files and directories relevant to the requested change;
- expected source, test, harness, export, docs, and dependency surfaces;
- files that must be left untouched by scope;
- any explicit allowed-file list or explicit excluded surfaces from the user
  request, treated as a hard scope fence;
- existing test and harness layout when relevant;
- current dirty or untracked files, without reverting user work;
- **import surface**: when a module will be moved, renamed, or deleted, search
  every import form that touches it — `from .<module> import`,
  `from <package>.<module> import`, `from <package> import <module>`, and any
  indirect imports through package `__init__.py` — so the full consumer set is
  known before the first edit;
- **monkeypatch surface**: when a module will be moved and replaced by a shim,
  search all test files for `monkeypatch.setattr(<module>, "name", ...)` and
  `from <module> import _<name>` — any underscore-prefixed name that a test
  imports or monkeypatches must appear in the shim's re-export list or the
  test will fail with `AttributeError`. Also audit **module-object attribute
  access**: when a test does `from <pkg> import <module>` and then accesses
  `<module>.<attr>`, the shim must expose `<attr>` (stdlib singletons like
  `subprocess`, `os` are common targets — re-export them from the canonical
  module even if no consumer does `from <module> import <attr>`);
- **relative-import depth**: when a file moves from a flat package into a
  subpackage, count the new depth. From `<pkg>.sub1.sub2`, one dot is
  `<pkg>.sub1.sub2`, two dots is `<pkg>.sub1`, three dots is `<pkg>`. Read
  every `from .X import` / `from ..X import` line in the file being moved and
  adjust each dot-count to reach the same target from the new location. A file
  with only stdlib imports needs zero changes. A file with sibling imports to
  other root-level modules needs one extra dot per subpackage level;
- accepted constructor fields, identity fields, validation owner, provenance
  fields, and export surfaces for record-backed helpers;
- accepted callable signatures, default values, aggregation or identity keys,
  empty-input behavior, non-mutation expectations, provenance expectations, and
  regression tests that must not be weakened;
- task-stated current-state claims — what the task says already exists, is
  missing, is on or off a path, or has or has not run — reconciled against the
  actual worktree before acting, with contradictions surfaced as the first
  finding. **Verify every claimed gap, not just the headline objective** — a
  task brief may assert N things are missing but the worktree may show M of
  them already done. Surface the exact subset that is complete vs. the subset
  that is genuinely missing rather than proceeding on all N as if they were
  equally stale.

Treat a suddenly empty or partially missing tree as an integrity blocker. Do not
reconstruct missing code from memory, plans, reports, or old outputs unless the
user asks for restoration from a trusted source.

If the request names an exact allowed-file set, edit only those files. Do not
touch package entrypoints, export tests, docs, registries, harnesses, artifact
writers, TODO or memory files, generated outputs, or adjacent modules unless
they are explicitly in the allowed set. Moving an out-of-scope file into a
temporary, stash, backup, or memory folder inside the repository still changes
the repository and does not satisfy the scope fence. Leave unrelated untracked
or dirty files alone; if they break imports or validation, report the blocker or
ask for an explicit scope expansion instead of repairing them under the current
task.

Do not self-expand the allowed-file list. A developer report, rationale table,
or "scope updated" note does not change the task scope by itself. Treat scope as
expanded only when the active user instruction or controlling task definition
actually supplies the expanded file list or explicitly authorizes the adjacent
contract work. Until then, out-of-scope fixes remain out of scope even if they
would make validation pass.

Guard suites and accepted integration surfaces are validation surfaces, not
edit surfaces. If a guard imports or exercises an out-of-scope module, that does
not make the module editable. Preserve it as accepted baseline unless it is in
the allowed-file list. If stale wiring in that module blocks validation, first
try to satisfy the contract from the scoped owner; otherwise report a
validation-scope conflict and the smallest needed scope expansion.

If an explicit capability ban conflicts with the allowed-file list because a
live prohibited surface already exists outside that list, do not ignore it and
do not declare the task stable. Report the scope conflict before editing, or
remove it only when the user or accepted review explicitly makes that surface a
cleanup target. The conflict should be visible in the baseline, not discovered
only after validation fails.

When a capability category is explicitly excluded, build a short removal or
absence checklist for every place that category can live in the current repo:
source files, module entrypoints, package metadata, parser or handler functions,
tests, docs, examples, and generated or helper files. "Removed" means absent
from the filesystem and changed-file list, not replaced by a comment-only stub,
empty placeholder, renamed backup, or disabled test that still sits inside the
repo. Search the excluded command names, module names, and user-facing phrases
after cleanup rather than relying on memory of earlier edits.
Also inventory aliases for the excluded capability: compatibility wrappers,
re-export modules, alternate file names, embedded handler functions inside
otherwise legitimate modules, package-script metadata, and tests named after
the command rather than the original module. Removing only the first obvious
file is incomplete when another path still exposes the same capability.

If you must undo your own accidental out-of-scope edits, make the smallest
surgical removal needed to restore the prior surface. Do not rewrite whole
entrypoints, export tests, docs, or config files as a cleanup shortcut, because
that can erase unrelated user work and expand the diff beyond the task.

For cleanup tasks, make a preservation map before deleting anything: files or
symbols explicitly requested for removal, files that only need references
removed, validation targets that must still exist, and accepted work that must
survive unchanged. Never delete required validation targets, accepted feature
modules, or their tests just because they depend on a stale excluded import.
Fix the stale reference at its owner, or report a scope conflict if the owner is
outside the allowed files.

## Task Classification

Classify the task before editing:

- **Feature or implementation**: add the smallest clear code path that satisfies
  the requested behavior.
- **Stabilization or acceptance**: compare the current draft against the
  accepted contract before deciding no edits are needed. Passing tests alone is
  not enough; verify signatures, defaults, key derivation, boundary behavior,
  non-mutation/provenance requirements, docs wording, and the tests that prove
  those behaviors.
- **Refactor or cleanup**: move, split, merge, rename, or delete code only to
  improve locality, readability, or testability for the current change.
- **Shim deletion (cleanup slice)**: migrate every consumer of a re-export shim
  to the canonical path, then delete the shim file from disk and git.
  This is the closing phase of staged package migration — the shim was a
  temporary bridge; now it is removed. Assess complexity before starting: count
  re-exported names, count consumers, check for monkeypatch bindings to the
  shim's module object, and check whether any root-level shim transitively
  imports through the target shim. A monkeypatch-free shim with few names and
  few consumers is the simplest case; monkeypatch bindings or transitive root-shim
  imports require additional care but do not block deletion.
- **Harness work**: keep harness code under the relevant `harness/` area; make
  objective, inputs, metrics, raw artifacts, and run loop explicit.
- **Test work**: place tests in the existing test system's natural location and
  keep each test focused on one behavior with small fixtures or toy inputs.
- **Method, baseline, metric, or export work**: keep the change near the owning
  extension point and update registration, docs, exports, and tests only when
  those surfaces are in scope.
- **Bounded bridge or helper work**: keep the callable in its owning module and
  avoid broadening public package exports, registries, docs, CLIs, harnesses, or
  artifact surfaces unless the request explicitly includes those surfaces.
- **Bounded runtime adapter stabilization**: keep discovery, command-plan
  construction, preflight, staging, and dry-run behavior in the owning adapter
  modules. Tests should use small local fixtures, temporary paths,
  monkeypatched imports or subprocesses, and explicit dry-run/preflight checks.
  Do not add real runtime execution, package exports, CLIs, harness runners,
  registries, generated paper artifacts, or broader integration behavior unless
  the request explicitly scopes them. When the request does explicitly scope real
  execution, treat that scope as a fence: run only the bounded slice it names,
  keep adjacent surfaces forbidden, and report a missing-input, preflight, or
  wrong-environment blocker rather than widening the command or carrying the
  authorization into a neighboring slice.

  When the task authorizes "any minimal fix needed" to make real execution
  complete, a config-only change (adding a path entry, an executable
  override, or a flag value to an existing config field that the adapter
  already accepts) stays inside the fence. It does not widen the command,
  add new source code, or create new adapter surfaces. Distinguish this from
  adding a new CLI flag, registry entry, or module export — those widen the
  surface and remain forbidden unless explicitly scoped.

  Before proceeding from dry-run to real execution, verify that the
  subprocess environment matches the in-process preflight environment.
  In-process import checks (``command_module_errors``,
  ``python_module_errors``) resolve imports with the current Python
  interpreter and ``sys.path``. A subprocess launched via
  ``subprocess.run(["python", ...])`` may invoke a different Python
  interpreter (the first ``python`` on ``PATH``) that lacks packages
  installed only in the project venv. When preflight passes but the
  subprocess fails with an import error or exit code 1, the first
  diagnostic is: "is the subprocess running the same Python?" Test the
  actual subprocess command manually before concluding the adapter logic
  is wrong. The fix — specifying the venv Python as the plan's
  ``python_executable`` — is a config-only correction, not a command
  widening.

  When transitioning a config from smoke/dry-run to real execution, audit
  which run spec each runtime plan is attached to. Smoke configs sometimes
  attach plans to a convenience spec (e.g. the first spec, or the one
  without deferred loading) because dry-run never consumes the outputs.
  Real execution may require those plans on a *different* spec — the one
  whose scheduler delivers the media objects that the generated artifacts
  are meant to annotate. The diagnostic question is: "does the downstream
  consumer of these runtime outputs receive them from the same run spec?"
  If a quality-replacement function reads ``reference_results`` from the
  current run but the reference objects are only delivered by a different
  scheduler on a different spec, the bridge silently never fires. Read the
  consumer (the quality-adjustment or annotation function that reads the
  runtime results) to confirm it receives
  the results from the right execution context before concluding the config
  is correct.

  When a downstream quality or annotation function contains a conditional
  early-return (e.g. "only adjust if delivered objects include
  reference-type media"), verify that the condition actually fires during
  real execution. A "no reference objects in frame" pass-through is
  functionally silent — the run succeeds but the measured-quality bridge
  never activates. After the first real run, inspect the frame outcomes of
  the relevant frames to confirm the adjusted fields differ from what the
  same run would produce with ``execute_runtime_plans=false``. If they are
  identical, the bridge did not fire; diagnose the condition (missing
  reference objects, frame mapping gap, missing CSV) rather than accepting
  a green run at face value.

  When replay steps (controlled by trace length parameters such as
  ``camera_limit``, ``bandwidth_limit``) and media-object frame ranges
  (controlled by ``frame_start``/``frame_end`` in options) are configured
  independently, verify that the replay covers the frames for which
  runtime-generated artifacts exist. If artifacts target frame *N* but the
  replay only executes up to frame *N-1*, the artifacts will never be
  delivered and any quality bridge depending on them will silently skip.
  The fix is a config adjustment (extend the trace limits), not a runner
  change.

  When a task requires re-running an experiment whose pipeline contains
  non-deterministic components (stochastic training with few epochs, random
  initialization, GPU non-determinism), the re-run will produce different
  numeric metrics even though the mechanism is unchanged. A task constraint
  like "the re-run must reproduce the accepted quality_score=<exact value>"
  may be physically unsatisfiable if the pipeline variance exceeds the
  tolerance implied by the constraint. Before accepting such a constraint
  at face value, check whether the pipeline is deterministic — if it is
  not, verify that the *mechanism* (parameter flow, quality bridge,
  computation formula) survived the re-run, and report that exact
  metric-level reproduction is not guaranteed. Do not try to force
  determinism through seed pinning or training changes unless the task
  explicitly scopes them.
- **Surface cleanup**: remove only the excluded surface and its named wiring.
  Preserve validation-target modules, accepted features, and unrelated behavior.
  If deleting one excluded file breaks imports, remove that file's public wiring
  rather than deleting the importer, the validation target, or the larger
  subsystem that was supposed to remain.
- **Validation-only pass**: run the exact requested command from the repository
  root. If it passes, make no source, test, docs, dependency, or export
  changes except removing artifacts created by the run. If it fails, inspect
  the failure and make only the smallest local fix to the accepted contract.
  Memory and trajectory files (progress records, status snapshots, validation
  logs, known-gap lists) are **not** source/test/docs/export changes — they
  are trajectory surfaces that record verified facts. When the task explicitly
  scopes memory-file updates as part of a validation pass, those updates are
  the primary deliverable, not a scope violation. Distinguish this from
  inventing new TODO items or selecting next tasks — recording verified state
  is maintenance, not feature work.
- **Framework or docs sync**: update framework docs when module boundaries,
  extension points, harness/test organization, artifact schemas, or repository
  responsibilities change and docs are in scope or are part of the accepted
  framework surface.
- **Trajectory or TODO maintenance**: record accepted, verified work. Select a
  next task only when the user, active workflow, or existing trajectory
  explicitly asks for one.

If a task is broad, choose a bounded slice that can be reviewed. If meaningful
progress now requires datasets, long experiments, method evidence, harness
runs, or paper results outside the request, stop at the accepted boundary and
report the blocker.

## Implementation Style

Prefer code that is short, direct, and easy to read in execution order. The data
flow should be visible: inputs, validation, transformation, calls, outputs, and
side effects should appear in a natural order.

Use names from the current domain contract and existing code semantics. Keep one
concept's spelling consistent across code, config, tests, harnesses, artifacts,
prompts, and docs.

When parsing an external schema into an internal record or value, keep source
column names separate from internal field names. If the task says to map
external `<source_field>` to internal `<target_field>`, expose and test the
internal name unless the user explicitly asks to preserve the source field as a
public output. Keep raw source names local to parsing, validation errors, or
provenance only when that is the clearest contract.

For parsers and loaders, normalize raw text at the boundary and construct
public records from already-typed values. Do not relax an existing record's
field validators because a new file format arrives as strings; parse the new
format before record construction or add a narrow local parser helper. If a
private validator is shared across old and new loaders, its contract must stay
true for every caller and must not broaden legacy public behavior unless the
task explicitly scopes that behavior change.

Keep responsibilities single:

- one file should mainly carry one interface, adapter family, metric family,
  data-processing step, harness entry/support area, export shape, or test group;
- split files that mix unrelated change reasons or abstraction levels;
- merge or simplify files that only add thin wrappers, pure forwarding, or extra
  jumps;
- avoid `utils`, `misc`, mega-runners, and all-in-one modules unless they are
  already narrow and stable.

Prefer inline or local helpers when logic is used once and remains readable.
Extract helpers, adapters, registries, factories, contexts, or interfaces only
when they provide real reuse, isolate a stable boundary, preserve an invariant,
reduce caller code, make tests simpler, or when a refactor plan separates
conceptually distinct concerns into separately named modules (even if the
helpers are currently only called from one file).

When reusing an existing private helper for a broader case, first check whether
the helper name, parameters, and doc-adjacent wording still describe every
caller. Rename the private helper to the smallest neutral name when its original
name encodes a narrower case, tail, direction, artifact type, or caller-specific
behavior that is no longer true. Do not change the public contract merely to fix
a private naming drift.

Do not add abstractions for imagined future cases. If a simple implementation
clearly satisfies the current task, keep it simple.

Reduce global state, hidden path assumptions, implicit side effects, long call
chains, repeated registration points, and heavy configuration for simple
experiments.

### Staged Package Migration (Re-Export Shim)

When a phased refactor moves a module to a new canonical location, leave the
old path as a thin re-export shim rather than hunting down and rewriting every
import site at once. The shim keeps the old module file but replaces its entire
body with a single import that re-exports the public surface from the new
location. Every existing `from <old> import X` or `from .<old> import X`
continues to resolve without change; consumers migrate to the new path in later
phases at their own pace.

A proper shim:

- imports every public name (classes, functions, type aliases) the old module
  previously exported, so no consumer sees a missing name;
- also re-exports any name that tests access as a module attribute for
  monkeypatching (`monkeypatch.setattr(module, "name", ...)`), even if no
  consumer does `from module import name` — a monkeypatch target that is absent
  from the shim will fail with `AttributeError`;
- does not import private helpers unless a consumer is confirmed to depend on
  them — but when in doubt, re-export the full surface to be safe;
- has no logic, no side effects, and no new imports beyond the re-export line;
- lives as a temporary bridge; the shim is deleted once all consumers have
  migrated to the canonical path. See the **Shim Deletion** section below for
  the full deletion protocol: consumer inventory, migration ordering,
  verification checklist, and root-shim transitive handling.

Before writing a shim, inventory the full import surface of the module being
moved: search for `from <package>.<module> import`, `from .<module> import`,
`from <package> import <module>`, and any indirect imports through package
`__init__.py`. Confirm every name that any consumer imports is present in the
shim. After writing the shim, run the full test suite — shim fidelity is the
central risk, and a missing re-export will surface as `ImportError` in
consumers.

After the move, verify import direction: the new canonical module should not
accidentally import through the shim (creating a circular path), and layered
packages should only import from layers below them.

Also verify import **depth**: when code moves from a flat package into a
subpackage N levels deeper (e.g. flat → `<pkg>/sub1/sub2/`), relative imports
to sibling top-level packages need N extra dots. From `<pkg>.sub1.sub2`, one
dot is `<pkg>.sub1.sub2`, two dots is `<pkg>.sub1`, three dots is `<pkg>`.
Count from the new file's package position up to the common ancestor, then down
to the target. A smoke test that imports every moved module immediately after
creation catches depth errors before the test suite runs.

Also verify **monkeypatch continuity** when the moved code calls a function that
tests monkeypatch through the old module's namespace. After the split, the new
canonical module has its own import binding for that function — independent of
the shim's binding — so a `monkeypatch.setattr(shim, "name", fake)` does not
affect the new module's call sites. When this pattern exists, make the new
module look up the function through the shim at call time (e.g. `import
<old_module> as _shim` and call `_shim.<name>(...)`) rather than via a direct
bare-name import. This keeps the monkeypatch-able namespace as the single
point of indirection without changing any logic.

This pattern applies when the monkeypatch target is a **repo-internal
function binding** — a function defined inside the repository that the
canonical module imports via `from <module> import <func>`. A different
mechanism applies when the monkeypatch target is a **shared stdlib singleton**
(e.g. `importlib`, `os`, `sys`). Stdlib modules are singletons cached in
`sys.modules` — every module that does `import importlib.util` receives a
reference to the same `importlib` object. When a test patches
`<shim>.importlib.util.find_spec`, it mutates `sys.modules['importlib'].util.find_spec`,
and the canonical module's own `importlib.util.find_spec(...)` calls see the
same mutation because both reference the same shared singleton. In this case
**no module-level-alias fix is needed** — the shim only needs to re-export
the stdlib module binding (e.g. `from <canonical> import importlib`) so that
`<shim>.<stdlib_module>` resolves. Before applying either fix, determine
which mechanism is in play: test `import sys; <canonical>.<module> is
sys.modules['<module>']`. If true, it's shared-singleton propagation and needs
only shim re-export. If false, it's a repo-internal function binding and needs the
module-level-alias fix.

Also verify **transitive import direction** — not just what the new module
directly imports, but what those imports drag in. A module in a restricted
layer (e.g. a summarizer that must not touch runtime) may import only result
dataclasses from a higher layer — semantically clean. But Python executes every
module-level `import`/`from` statement of the imported module, so if that
higher-layer module imports runtime adapters, scheduler registries, or config
registries at module level, the summarizer transitively pulls them all in. This
is a transitive import violation even though the summarizer's own `import` lines
look correct. Audit transitive chains by following each import target module's
own module-level imports recursively until reaching a layer boundary. When a
transitive violation exists, the narrow fix is to extract the needed result types
into a dedicated leaf module that only imports from permitted layers (typically
domain), then have both the higher-layer module and the summarizer import from
that leaf. When such extraction is out of scope, record the pre-existing
violation in memory and defer it — do not silently accept it as clean.

When a phased refactor creates a package directory that shares its name with
an existing flat module (e.g. creating `metrics/` when `metrics.py` already
exists in the same directory), Python resolves `import <pkg>.<name>` to the
package directory, making the flat file unreachable under its original import
path. Before creating the package, check for a same-name flat module. If one
exists, absorb its public surface into the package's `__init__.py` and delete
the flat file from the working tree. The absorbed content must be byte-identical
to the original — no logic changes. Consumers that imported from the flat
module (e.g. `from <pkg>.<name> import <symbol>`) will now resolve through the
package `__init__.py`; verify that every public name the flat module exported
appears in the `__init__.py`. If the flat module also has consumers that import
it as a standalone object (`import <pkg>.<name> as <alias>`), those consumers
resolve to the package module (`<pkg>/<name>/__init__.py`) transparently.
A `git rm` of the flat file is the cleanest removal — do not leave a `.bak`
rename, a comment-only stub, or an empty placeholder that would still shadow
the package in some Python import resolution orders.

When extending a package's `__init__.py` to re-export a newly added sibling
module, check for circular imports before adding the re-export line. If the
new sibling module imports from another sibling (e.g. `<new>.py` does
`from ..<old_shim> import <name>`), and the `__init__.py` already re-exports
from that other sibling (or from the shim that resolves to it), adding
`from .<new> import ...` to `__init__.py` creates a circular chain:
`__init__` → `.<new>` → `..<old_shim>` → `__init__`. When this is detected,
leave the `__init__.py` incomplete — the new sibling remains accessible
through its root re-export shim, not through the package `__init__.py`.
Document the deferred `__init__.py` re-export as a known gap for a future
dedicated decoupling pass. Do not reorder imports, add lazy imports, or
restructure sibling dependencies to force the `__init__.py` re-export — those
are behavior-sensitive changes that belong to a later phase.

**Dependency-group ordering across sub-phases**: when moving a set of related
modules into a shared subpackage, move the modules with no intra-group
dependencies first (the ones that import only domain, ports, stdlib, or
third-party code). Move modules that import other members of the same group
only after their dependencies are co-located in the subpackage. Example: if
`<b>.py` does `from .<a> import <name>` and both are intended for
`adapters/<group>/`, move `<a>.py` first. In the next sub-phase, `<b>.py` can
follow with a clean sibling `.` import. Moving `<b>` before `<a>` creates a
mixed-state `..<a>` reference to the still-flat root file, which resolves
differently under test collection and violates the co-location contract. Audit
intra-group imports before selecting the first module in any new subpackage,
and name the dependency chain in the task brief so later sub-phases have clear
ordering.

### Shim Deletion

When all consumers of a re-export shim have been migrated (or the task is to
migrate them as part of the deletion), the shim can be removed. This closes the
staged-package-migration lifecycle.

**Complexity assessment.** Before editing, inventory:

- **Re-exported names**: what the shim exports. Note the distinction between
  names the shim re-exports (often the full canonical surface — dozens of names)
  and names consumers actually import (typically a small subset). Only the
  consumer-imported names matter for migration; the canonical location already
  owns the full surface and remains available at the canonical path.
- **Consumer set**: every import site that references the shim's module path, in
  both source and test trees. Search all import forms: `from <shim_path> import`
  (absolute), `from .<shim> import` (1 dot), `from ..<shim> import` (2 dots),
  `from ...<shim> import` (3 dots), and beyond for deeper nesting. Also check
  indirect imports through package `__init__.py`. Count **sites, not files** —
  a single consumer file may have multiple import sites (e.g. a top-level import
  plus a deferred import inside a function body), and every site must be
  migrated. A consumer nested 3+ levels deep needs the corresponding dot count —
  stopping at 2 dots misses it. Note which specific names each consumer imports —
  this is the verification target, not the full shim re-export list.
- **Monkeypatch bindings**: search tests for `monkeypatch.setattr(<shim_module>, ...)`
  and `setattr(<shim_module>, ...)`. Zero hits = simplest case; no shim-module
  binding needed after deletion. Positive hits = complex case; the monkeypatch
  surface requires a shim-module binding to survive. **Memory tier labels are
  claims, not facts** — re-verify monkeypatch counts against the worktree every
  slice, even when memory files classify a shim as "easy-tier no monkeypatch."
  A memory file written in a prior session may predate the discovery of
  monkeypatch bindings; the worktree grep is the truth.
- **Deferred-shim consumers**: when a consumer of the current shim is itself a
  deferred root shim (its own deletion belongs to a future slice), its import
  line must still be redirected to prevent `ImportError` when the current shim
  is deleted. Redirect only the import line — do not delete or rewrite the
  deferred shim. Its own deletion is a separate future slice.
- **Root-shim transitives**: check whether any root-level re-export shim imports
  names from the target shim's module path. If a root shim does `from .<target_shim>
  import <name>`, trace whether it already gets those names through a canonical
  path transitively — the root shim may import from `<intermediate_module>` which
  itself imports from the target shim. If the root shim's import chain survives
  after migration (root → intermediate → canonical), the root shim needs no edit.
- **`__init__.py` gate**: check whether any package `__init__.py` imports from
  the shim. If `<pkg>/__init__.py` does `from .<shim> import (...)`, the redirect
  is a **blocking gate** — the shim cannot be deleted until `__init__.py` is
  retargeted to the canonical path. This redirect is order-sensitive:
  `__init__.py` runs first in any `import <pkg>`, so it must resolve first.
  Verify `import <pkg>` succeeds before deleting the shim. After the redirect,
  `__init__.py` must re-export the same names verbatim from the canonical path.
- **`_`-prefixed private names**: the shim may re-export underscore-prefixed
  private names that the canonical module's own public consumers don't use.
  Before deletion, grep test files for imports of any `_`-prefixed name from
  the shim path. If found, those names are part of the test contract and must
  be included in the canonical import verification. If none found (typical),
  note the result and proceed.

**Migration order.** Migrate every consumer before deleting the shim:

0. **`__init__.py` gate first** (if applicable): when any package `__init__.py`
   imports from the shim, redirect it to the canonical path before any consumer
   migration. This is order-sensitive — `__init__.py` runs first in `import <pkg>`.
   Preserve all imported names verbatim. Verify with `import <pkg>` before
   proceeding. The shim stays on disk until all consumers (including `__init__.py`)
   resolve to canonical.

1. Calculate the correct import depth for each consumer:
   - Files **inside the same subpackage** as the canonical module use a sibling
     import: `from .<canonical> import <name>` (one dot).
   - Files **outside that subpackage** import from the parent level:
     `from ..<canonical_pkg>.<canonical> import <name>` (count dots to reach the
     common ancestor, then down to the canonical module).
   - **Root-module consumers**: a root-level module in the same package as the
     shim that imports the shim by one dot (`from .<shim> import`) is still a
     consumer. After migration: `from .<subpackage>.<canonical> import` — the dot
     count stays 1, reaching into the canonical's subpackage. Root-module consumers
     are easy to miss because they aren't nested in a subdirectory; inventory them
     explicitly when the shim lives at the package root.
   - **Multi-file canonical targets**: when the shim re-exports names from
     multiple separate canonical files (e.g. one class per file under a shared
     subpackage), apply the depth rule to each file individually. The shared
     subpackage prefix sets the depth; only the filename differs per import.
   - **`as` aliases**: when a consumer imports a name with an `as` alias
     (`from <shim> import <Name> as <Alias>`), migrate the alias verbatim:
     `from <canonical> import <Name> as <Alias>`. Dropping or altering an alias
     creates a silent name mismatch — the import succeeds but downstream code
     that uses the alias name fails with `AttributeError`. Grep consumers for
     `as` clauses before editing.
   - **`import <module> as <alias>`**: when a consumer imports the entire shim
     module as an object (`import <shim> as <alias>`), the redirect is
     `from <canonical_pkg> import <canonical> as <alias>`. Preserve the alias
     verbatim — downstream code that does `<alias>.<func>(...)` must resolve to
     the same module object after migration. This pattern often co-occurs with
     `monkeypatch.setattr(<alias>, ...)` — the alias name is the continuity
     binding.
2. Edit every consumer's import line to resolve to the canonical path. Migrate
   source consumers first (if any), then test consumers. A shim with zero source
   consumers and only test consumers is valid — proceed directly to the test
   imports. Order within each group does not matter when the shim is still on
   disk during migration. For multi-file targets, edit
   only the names each consumer actually imports — do not expand a partial
   consumer to import all names just because the shim re-exports all of them.

   **Surgical migration**: when a consumer file has adjacent import blocks that
   reference different root shims (e.g. `from ..<current_shim> import (...)`
   on one line and `from ..<deferred_shim> import (...)` on the next), migrate
   only the block that references the current shim. Leave the adjacent
   deferred-shim block untouched — its migration belongs to its own future slice.

   **Bulk path-only migration**: when the slice is path-only (no aliases to
   preserve, no monkeypatch bindings, no continuity redirects — only the
   module path changes), a depth-ordered regex sweep replaces every consumer
   in a single pass. Order the sweeps by depth: 3-dot consumers first (the
   deepest), then 2-dot, then 1-dot root modules, then absolute imports.
   This prevents an earlier sweep from rewriting a deeper import into an
   incorrect intermediate form. The only exceptions are `__init__.py`
   (handled first, step 0) and `import … as <alias>` lines (continuity
   bindings requiring hand-edit). After the sweep, verify every rewritten
   import line resolves to the correct depth and preserves the same names.
3. After all consumers are migrated, delete the shim: `git rm <path_to_shim>`.
   Leave no comment-only stub, empty placeholder, or `.bak` rename.

**Verification checklist.** After deletion, run in order:

1. **Shim-gone check**: `python -c "import <shim_path>"` must fail with
   `ModuleNotFoundError`. Confirm the file does not exist on disk.
2. **Canonical-import check**: `python -c "from <canonical_path> import <exported_names>"` must succeed for every name that any consumer imports. Verify only the consumer-imported subset — the canonical location owns the full surface; checking every name the shim re-exports is unnecessary when the canonical location was not modified. **Byte-identity**: confirm the canonical file was not modified by the migration — `git diff -- <canonical_subpackage>/` must be empty. (For a single-file canonical target, `git diff -- <path_to_canonical_file>` is sufficient.) The slice only rewrites consumer import lines; the canonical source is the immutable source of truth.
3. **Scoped test suite**: run the test files that were edited plus any test files
   that exercise the deleted shim's exports. Expected count should match
   pre-migration baseline — no new failures. **When monkeypatch bindings exist**,
   this step is the continuity smoke: the scoped run must include the test file
   with the `monkeypatch.setattr(<alias>, ...)` calls, and all must pass.
   A pass here (not just import resolution) proves that the test patches the
   same module object that the canonical code calls.
4. **Full test suite**: run the repository's full test command. The pass/fail count
   must match the pre-migration baseline exactly. Any new failure is a migration
   defect.
5. **Entrypoint-order import smoke**: import modules in the order that exercises
   the package's initialization dependencies. This catches order-dependent
   partial-init failures that alphabetical test collection can mask. When the
   deleted shim was imported through an eager package `__init__.py` chain
   (e.g. `<pkg>.__init__` → `<subpkg>.__init__` → `<consumer>` → shim), the
   smoke must exercise that exact chain with the shim deleted. **Construction
   formula**: build a single import command that imports every outermost
   package entrypoint of the migrated consumers (the closest `__init__.py`
   ancestor for each consumer subpackage) plus the canonical module itself,
   ordered from the lowest-layer package upward. For example, if consumers live
   in `<pkg>.experiments`, `<pkg>.evidence.summarizers`, and the root
   `<pkg>`, the smoke imports `<pkg>.experiments`, `<pkg>.evidence.summarizers`,
   and `<pkg>.<canonical_subpackage>.<canonical>`. A pass means every module
   resolves without `ImportError`.
6. **Absence grep**: search the source and test trees for any remaining import
   of the deleted shim's module path. Use a catch-all regex that matches all
   depth forms and absolute forms at once: `from.*<shim_name> import` across
   `src/` and `tests/`. Then filter out the canonical module's own sibling
   self-import (e.g. `from .<canonical> import` inside the canonical file
   itself). Every remaining hit must be a canonical-path import — any hit that
   resolves to the old shim path is a blocking leftover. Do not rely on
   listing specific depth forms (1-dot, 2-dot, 3-dot) individually; a
   catch-all regex catches every depth at once. (Documentation references to
   the old path are not code defects — they are documentation staleness,
   tracked separately.)
7. **Root-shim transitives**: verify any root shim that previously resolved names
   through the deleted shim still imports them correctly through the new canonical
   chain. An `import <root_shim>` smoke test is sufficient when the root shim's
   own import chain was not edited.
8. **Whitespace check**: `git diff --check` from the repository root. Report
   findings in files the task did not touch as pre-existing; note them but do not
   fix them.

Treat a new test failure, a broken import smoke, or a leftover import of the
deleted shim path as a blocking defect. A pre-existing test failure that is
unchanged from baseline is not a defect.

**Stale bytecode.** After deleting the shim, clear the language's bytecode
cache under the source tree (e.g. `find <src_root> -type d -name __pycache__ -exec rm -rf {} +`).
A `.pyc` file from a prior session can make `import <shim_path>` silently
resolve against the deleted source, masking a real resolution failure. Run
the shim-gone check after clearing, not before.

**Multi-file canonical targets**: when the shim re-exports names from many
separate files (e.g. one class per file), the byte-identity check (step 2)
still applies per file. Verify each canonical file individually — the shared
subpackage prefix may mask a single-file modification when checking the whole
directory at once.

**Do not** migrate other shims in the same slice unless the task explicitly
scopes them. One shim per cleanup slice keeps review simple and defects local.
Root shims that transitively chain through the deleted shim survive without
edits when their import chain resolves through the canonical location —
verify this, do not assume it.

**Canonical importing through not-yet-deleted root shims.** In phased refactors,
a canonical module may itself import through root shims that are still on disk
(e.g. `from ..<upstream_shim> import (...)` inside `<canonical_subpackage>/<canonical>.py`).
These are the canonical module's own upstream dependencies — they were not
migrated when the canonical module was moved, and they belong to their own
future shim-deletion slices. During the current shim's deletion, the canonical
module's root-shim imports are a **frozen surface**: they must be left
untouched, and the byte-identity check (`git diff -- <canonical_subpackage>/`)
proves they were preserved. The only edits in the current slice are consumer
import lines; the canonical module's internal imports are out of scope.

Shims typically re-export every name the canonical location exposes — often
dozens of names — even when only a handful have active consumers. This is
expected: the shim was a wholesale bridge, not a curated export list. When
deleting, focus inventory and verification on the consumer-imported subset.
The full canonical surface remains available at the canonical path for any
future consumer that needs it.

### Move-Only Refactor Verification Checklist

When a task is a pure move-only refactor (files relocated, shims left behind,
no logic changes), the verification surface is specific and mechanical. After
creating the canonical files and root shims, run this checklist in order:

1. **Import smoke**: import every moved module through both the shim path and
   the canonical path in a single smoke command. For Python, use
   `python -B -c "import <shim_path>, <shim_path2>, <canonical_path>, <canonical_path2>"`.
   An `ImportError` or `ModuleNotFoundError` at this stage catches depth errors
   before the test suite runs.

2. **Scoped test suite**: run the exact test files the task brief names. Record
   the pass/fail count. The pre-existing failure count (if any) should match the
   task brief's documented baseline — no new failures introduced.

3. **Byte-identical verification**: diff each moved canonical file against the
   git-HEAD original. The only permitted difference is the import-depth line(s)
   that changed because the file moved one or more package levels deeper. No
   logic, signature, docstring, or whitespace changes. If the file has no
   relative repo-internal imports, it must be byte-identical.

4. **Whitespace check**: run `git diff --check` from the repo root. Whitespace
   findings in files the task did not touch are pre-existing and should be noted
   as such, not fixed.

5. **Import direction scan**: verify the new canonical module does not import
   back through the root shim. Grep the canonical file for any import that
   resolves to the old shim path. For Python, search for `from <shim_relative_path> import`
   patterns that would create a circular chain.

6. **Downstream `__init__.py` circular-import check**: when a flat module is
   moved and its old location becomes a shim, any package `__init__.py` that
   eagerly imports through the shim can create a circular chain that did not
   exist when the old location was a flat file. For each package `__init__.py`
   in the repository, trace whether an eager module-level import reaches the
   shim and whether the shim's canonical target imports back into that package.
   If found, classify as pre-existing (the `__init__.py` re-export and the
   shim both predate this slice) or task-induced (the current move created the
   chain). Task-induced circular imports are blocking defects. Pre-existing ones
   are recording targets — but if they block test collection in the scoped
   suite, narrow the test command to the collectable subset, record the excluded
   file and the circular chain in the verification report, and file the
   pre-existing violation as a deferred decoupling gap in memory. Do not
   silently omit uncollectable tests from the command without noting them.

7. **Root-init check**: confirm `__init__.py` of the package root has zero diff
   (not widened). Only the new subpackage's own `__init__.py` is new.

8. **Memory update**: after all checks pass, update the memory/trajectory files
   the task brief names with the verified state, exact test counts, shim
   identities, and the fact that the phase is now complete. Create the memory
   file directory if it does not yet exist.

This checklist is the minimum acceptance gate for every move-only refactor
slice. Skipping any step risks silent import failures, circular dependencies,
or stale memory that causes future rounds to re-execute completed work.

### Domain-Local Extraction vs. Cross-Module Dedup

When a task asks to extract shared helpers, distinguish two operations with
very different risk profiles:

**Domain-local extraction** — moving private helpers from one module to a
sibling within the same package. The helpers already live in the module that
owns them; the extraction just gives each concern its own named file. Call
sites stay in the same file(s); the only change is an import line switching
from local `def` to `from .sibling import`. Risk is low because the contract
does not expand to new callers.

**Cross-module dedup** — deleting copy-pasted helpers from many modules and
having them all import from a single canonical source. Risk is high when the
copies are not byte-identical: subtle differences in whitespace handling,
signature types, edge-case behavior, or sibling-helper availability mean a
mechanical unification silently changes validation behavior for some modules.
Before attempting cross-module dedup, inventory every copy and compare their
bodies. If copies differ, do not unify them under the current task — defer to
a dedicated reconciliation pass that can assess each behavioral difference
individually. The skill's rule "do not relax a shared validator; keep it true
for every caller" applies across modules too: a validator that changes behavior
for even one caller is a different validator.

When the task explicitly scopes only domain-local extraction and names
cross-module copies as deferred, do not touch those copies even if they appear
to share the same name. Record them as deferred work and move on.

Audit path-resolution chains when a value passes through multiple resolution
layers before reaching its final use site. A path written in a config file
may be resolved relative to the config directory by a config parser, stored
as a raw string in an internal record, and later resolved again relative to
the process CWD by a downstream ``resolve_executable``-style function. When
the two resolution bases differ (config-dir ≠ CWD), the result can point to
the wrong file or produce a ``FileNotFoundError``. Before committing a
relative-path fix, trace the full chain: where is the path first resolved,
where is it stored, where is it used, and what is the CWD at each stage.

When code uses both in-process import checks and out-of-process subprocess
calls, verify that they resolve to the same Python interpreter and package
set. A preflight that passes in-process (import succeeds with the current
``sys.path`` and venv packages) does not prove that a subprocess
``["python", "-m", "some.module"]`` will succeed — ``"python"`` may be a
different interpreter on ``PATH``. Test the exact subprocess command (with
the same env vars) before concluding the runtime logic is correct. When the
subprocess command is built by an adapter from configurable fields, prefer
to make the python executable configurable and default to the venv Python
when the task's environment context makes that the correct choice.

When an interface forces every caller to pass excessive parameters, consider a
small explicit context or config object. Do not turn that into a framework when
plain values remain clearer.

When a field or config contract says "finite number", validate finiteness
explicitly. Reject `NaN`, positive infinity, negative infinity, booleans when
the language treats booleans as numbers, negative values when the contract says
non-negative, and non-numeric values. Do not treat "not NaN" as equivalent to
finite. If an existing shared validator has intentionally weaker legacy
behavior, leave it unchanged unless the task scopes that contract change, and
add a local validator for the stricter new config.

## Change Locality

Before writing code, identify the natural owner of the change:

- a method change should mainly touch method code and necessary comparison or
  registration surfaces;
- a baseline change should mainly touch baseline code and focused tests;
- a metric change should mainly touch metric definition, computation, export
  normalization if needed, and tests;
- a public package export change should mainly touch the package entrypoint or
  existing export module plus a focused export-surface test;
- a harness change should mainly touch the relevant harness area plus necessary
  shared interfaces;
- a result-artifact change should mainly touch artifact schema, export logic,
  and tests;
- a loader or manifest change should mainly touch the input layer and tests.

When public exports, docs, registries, harness runners, generated artifacts, or
paper-output surfaces are explicitly excluded, treat existing mentions of the
new helper in those surfaces as defects to remove, not as consistency surfaces
to update. Tests should import scoped helpers from their owning module when the
package entrypoint is out of scope.

If one feature requires unrelated edits across many areas, treat that as a
framework-boundary risk. Do the smallest local refactor that brings related code
together, or report the coupling if a safe local refactor is outside scope.

Keep code that changes together close. Keep unrelated reasons to change in
separate modules. Public/shared layers should contain only stable capabilities
needed by multiple users; special cases should stay near their use sites.

When a fix patches a latent gap at one call site and sibling call sites share
the same pattern, they share one change reason and belong in the same change.
Audit siblings before closing the fix: if a second entry point builds and runs
the same kind of command, the same resolution, validation, or environment wiring
applies there too. Fix in-scope siblings together so behavior does not diverge
silently across entry points. When a sibling is out of scope, record the
divergence explicitly — which site, which gap, why deferred — instead of leaving
the inconsistency implicit. Change locality is not a reason to fix one site and
leave an identical latent gap unflagged at a co-located site.

## Harness And Test Discipline

Harnesses serve paper goals, performance comparison, method screening, module
optimization, and experiment evaluation. Tests serve functional correctness,
interfaces, data formats, config parsing, metrics, export behavior, and basic
module interaction.

Keep harness and test responsibilities separate:

- harnesses should expose stable entry semantics, input protocols, metric names,
  raw artifacts, seeds, splits, config snapshots, and parseable outputs;
- tests should use small fixtures, toy inputs, and clear pass/fail assertions;
- each test should have one named behavioral responsibility;
- formula, threshold, ordering, percentile, or ranking tests should use
  discriminating fixtures where a neighboring formula, adjacent threshold,
  reversed ordering, or copied existing helper would fail;
- numeric config validation tests should match the stated contract for each
  key: missing/default behavior, accepted boundary values, negative values when
  non-negative is required, non-numeric values, `NaN`, and infinities when the
  contract says finite. If multiple fields or parameters say "finite" or "not
  bool", cover each owner, not only one representative owner;
- parser and loader tests should assert internal field names, units, converted
  values, row/sample provenance, slicing semantics, immutable return shape when
  promised, and boundary normalization after any external-schema mapping. A test
  that only proves the raw source column was read does not prove the internal
  contract was respected;
- fixed-shape parser tests should make malformed structure failures explicit:
  wrong component counts for each owned tuple/vector, malformed delimiters,
  non-finite values for each finite owner, and invalid window arguments for each
  public slicing parameter. Keep these as small contract fixtures, not large
  real-data reproductions;
- budget-enforcement tests are separate from budget-configuration validation.
  When the scope asks for over-budget rejection or reason capture, use a valid
  constrained budget that lets at least one eligible candidate reach the
  selection loop and then exceed the remaining budget. Assert the rejected ID
  and exact budget-exceeded reason named by the task; an invalid budget test,
  missing-budget test, filtered candidate, cadence skip, or type rejection does
  not cover selection-time budget exhaustion;
- for ordered selectors, missing-budget or unbounded-budget behavior still
  follows the selector's ordering contract after filtering and staging. The
  expected selected IDs should be the full eligible set in sorted order, not the
  input order, unless the contract explicitly says input order is preserved;
- tie-breaker tests should make the primary sort keys equal and deliberately
  set other sort-like fields to favor the opposite order, so only the requested
  tie-break field can explain the expected result;
- for multi-key ordering, test each tie-break level separately: hold all higher
  priority keys equal, set the key under test to determine the expected order,
  and set lower-priority sort-like keys to favor the opposite order. A fixture
  does not prove a middle tie-break if the final ID/name/order key would choose
  the same winner;
- treat compound ordering phrases such as "deadline/object-id",
  "density/deadline/id", or "score/frame/deadline/id" as a checklist, not as a
  single fixture. Prove the first key with adversarial lower-priority fields,
  then add a same-higher-key fixture for each fallback key, including the final
  lexical identifier fallback when it is named;
- tie-break fixture names and object IDs are labels, not evidence. Before
  accepting an ordering test, inspect the actual tuple fields used by the sort
  and confirm the expected winner is not also favored by a lower-priority
  fallback field;
- for filtered, staged, or multi-phase selection, repeat the ordering audit for
  each accepted subset or phase, including catch-all groups such as regular,
  default, or non-special candidates. A fixture that proves the final
  identifier tie-break inside one phase does not prove that an earlier ordering
  key, subset ordering key, or phase priority is enforced;
- for partitioned budgets, lanes, quotas, queues, or resource pools, isolation
  tests should leave spare capacity in one partition while a candidate in
  another partition exceeds its own limit. A fixture where every partition is
  fully consumed does not prove that borrowing, sharing, or leakage is absent;
- no-mutation tests should inspect the same objects or mutable containers passed
  into the implementation;
- export-surface assertions belong in export tests, invalid-state assertions in
  invalid-state tests, and identity/schema assertions in clearly named identity
  or schema tests;
- for a new private helper with two or more mutually exclusive branches (a
  relative-versus-bare path resolver, a presence-versus-absence dispatcher, an
  enabled-versus-disabled switch), pin each branch with its own focused
  assertion unless the project's test design explicitly forbids that test
  category. A branch taken only when a condition holds is untested when every
  fixture takes the other branch; a deterministic test of a pure helper is not
  the same as a forbidden real-execution or real-data test and should not be
  skipped on that basis. A branch-pinning assertion only counts as coverage if
  the repository's normal validation command actually executes it: a doctest
  embedded in a source module, a test guarded by a non-default flag, or a test
  file outside the configured test path is not exercised by the requested
  command and gives no evidence under it. Place the assertion where the suite
  runs it, or explicitly label it as an unexecuted extra guard; do not count an
  unrun doctest toward the green-suite total;
- harness code should not become functional test code;
- test code should not become paper-performance evaluation.

When a harness grows, split support modules inside that harness's own folder
before pushing special logic into shared layers. When tests grow, split them in
the existing test system's style.

## Framework Docs

Maintain framework docs only when docs are in scope, the active workflow
requires docs, or the accepted change would leave a current documented surface
materially misleading. Keep docs about current reality, not template
initialization, aspirational status, or skill mechanics.

Framework docs should explain where future local changes should happen:

- stable boundaries and extension points;
- change map from feature type to module, harness, test, or export area;
- harness purposes, metrics, and raw artifacts;
- test organization actually used by the repository;
- raw-first export approach and downstream analysis boundary;
- framework risks where future changes cannot yet stay local.

For README-style or package docs, read the requested files first and classify
surfaces as current, stale, or historical. Edit only stale current surfaces
needed for the accepted change. If all requested docs are current, report a
no-op docs sync and the readback/search checks that proved it.

When a bounded harness or smoke API is added and an in-scope harness README,
contract note, or config/example doc already describes a broader runner,
registry, paper experiment, or framework-level entrypoint, include that surface
in the docs map. Either narrow the current entrypoint/output wording to the
accepted bounded API, or mark the broader text as planned or historical if that
is true in the repository. Do not leave full-runner or paper-output semantics as
the current contract for a module-level helper.

When one accepted symbol, artifact, metric, method, or helper is documented in
multiple parallel surfaces, build a small surface map before editing: helper or
API lists, emitted names, package/module summaries, layout rows, test summaries,
and absence clauses. Update each stale parallel surface consistently, but do
not add new public exports, runtime behavior, or future-plan claims just because
the docs mention the accepted bounded surface.
For module-level adapter surfaces, map both source/module rosters and test
rosters. If a scoped test file exists, every current README-style test roster
that lists comparable sibling tests should include it at the same hierarchy and
translation level. If a scoped module has no direct test file and the task does
not request one, do not invent an out-of-scope test solely for roster symmetry;
report the indirect or absent coverage honestly and keep edits inside scope.
Bind the surface map to the current selected subject. Neighboring helpers,
methods, tests, metrics, or earlier accepted features in the same document are
context, not part of the sync, unless the user explicitly scopes them or the
same sentence/list must change to stay truthful. Do not carry predecessor tokens
or coverage details from a previous task into the current docs pass when the
current request names a different stale predecessor or surface boundary.

For each subject-specific surface in that map, carry the full scoped contract
when the user names it: accepted inputs or candidate classes, rejection reasons,
configuration or budget keys, ordering or priority rules, emitted metadata, and
validation behavior. Do not rely on a neighboring surface, a shared-helper
phrase, or an absence clause to imply a detail that the current subject's
surface must state explicitly.
If the scope gives an exact callable signature, return annotation, record
shape, output container, or immutability promise, reproduce that contract on
every requested API, package-summary, module-summary, and translated surface
that names the callable or record. Generic phrases such as "sample values",
"helper output", or "bounded parser" are not substitutes for a named return
shape when the user supplied one.

When a docs-sync request says a surface currently lists through a previous
accepted subject, search that predecessor token in every requested document
before editing. Treat each occurrence as a current surface or historical note.
Update stale current rosters and scoped surfaces; leave historical notes alone
after confirming they are not current-surface lists.

Write docs at the stable contract level by default. Summarize behavior,
metadata, configuration, rejection reasons, ordering, artifact shape, and test
coverage clearly enough for future maintainers to find the right code. Do not
copy full fixture ID lists, exhaustive invalid-value matrices, or lengthy test
expectations into README-style docs unless the user explicitly requests that
level of detail, the existing docs already use that convention for the same
surface, or review feedback depends on an exact fixture detail.

Keep priority, visibility, partition, and ordering terms separate from filters.
If an item outside a priority group remains eligible, document it as lower
priority or off-priority, not as rejected or as an invalid type. Rejection
wording should describe the actual contract owner: type filters reject types,
validation rejects invalid inputs, and budget handling rejects otherwise
eligible over-limit items.

When the user scopes specific test-coverage details for README-style docs,
turn those details into a per-document checklist for every requested test
summary surface. Preserve the exact behavioral distinction that made the test
valuable: discriminating fixture setup, tie-break owner, invalid-input owner,
metadata value, provenance field, non-mutation target, or same mutable object
when those are named. A generic sentence such as "covers tie-breaking" or
"covers non-mutation" is not enough when the scope names the fixture condition
or the object whose mutation must be rejected.

For staged, filtered, or multi-path behavior in README-style docs, document the
behavior by responsibility: accepted subset definitions, phase priority, primary
ordering for each accepted subset, tie-break fixtures, metadata, and each
rejection reason's owner. Do not let a tie-break fixture stand in for the
primary ordering case, and do not describe one rejection reason as applying to
all rejected items when another rejection path, such as budget or validation,
uses a different reason.

When a README section groups multiple symbols, helpers, schedulers, metrics, or
tests under one sentence or bullet list, the group label must be true for every
item in that list. If a metadata value, rejection reason, config key, fixture,
or coverage case belongs to only one grouped subject, split it into a
subject-specific bullet or paragraph instead of relying on a shared block.

Write absence clauses narrowly. Before saying a broad category is absent, check
the current code and docs for accepted bounded surfaces in that category. If a
small in-memory conversion, helper, adapter, or test surface exists, qualify the
missing surface precisely, such as "file-based", "result", "additional",
"runtime", "full", "real-data", or "paper-output" capability. Do not let a
negative sentence contradict an implemented helper documented elsewhere.
When the accepted feature is a bounded or partial member of a broader algorithm,
model, runtime, or framework family, absence wording should name only the
unimplemented larger surface, such as "full", "additional", "beyond the
accepted bounded formula", or "runtime integration". Do not use the broad
family name alone as absent when the current docs also document an accepted
bounded implementation in that family.
Prefer narrow positive absence sentences such as "This bounded surface does not
add <capability>" or "<capability> remains unimplemented." Avoid double
negatives and "No <capability> is not ..." constructions, especially after
rewriting a long absence clause.

Do not automatically queue a docs-only task after every source/test change.
Queue or perform docs sync only when docs are explicitly requested, are part of
the active workflow, or the accepted change would leave a current documented
surface materially misleading. If docs are excluded from the source/test task,
do not promote stale documentation found during validation or TODO maintenance
into the next developer task unless the user, active workflow, or existing
trajectory explicitly selects docs sync. Record possible docs staleness as a
caveat or candidate, not as a selected handoff.

## Trajectory And TODO Maintenance

Trajectory files record accepted facts: exact validation commands and results,
cache findings, and explicit exclusions that preserve scope.

**Do not invent the next task.** Select a next task only when the user,
workflow, or active trajectory explicitly selects one. Otherwise leave a
neutral waiting state.

Listing **candidate next phases** ("Next slice options: <phase_a> or <phase_b>")
documents real gaps without selecting one. A memory file that ends with a
candidate list and no explicit selection is in a neutral waiting state. When
updating memory after completing a phase, advance the stale pointer past the
completed phase and list remaining real gaps as candidates.

**Excluded surfaces stay excluded.** If the current task explicitly excluded
docs, exports, harnesses, or a capability category, preserve that exclusion in
trajectory files. A later TODO-only pass may record accepted work but must not
select excluded surfaces as follow-up work without explicit task selection.

**Record exact validation results.** For each run, record the command, exact
pass/fail counts, pre-existing failures documented separately from new
failures, and cache cleanup findings. A green validation run confirms current
contracts; it does not create new feature, docs, or experiment work.

## Naming, State, And References

Names must reflect real meaning and data shape. Do not keep historical,
placeholder, or overgeneral names after the concept changes.

Use content names for content and reference names for paths, handles, IDs, URLs,
or external resources. Do not let a variable named like a reference carry loaded
content, or a content name carry a location.

Place each variable, state object, config, and data structure at the layer that
actually owns it. Local intermediate content should stay local. Only stable
cross-boundary data should enter shared structures.

When outer orchestration owns saving, archiving, or exporting, inner business
logic should return values rather than also writing files. Write, save, export,
and return responsibilities should be single-owner.

## Prompts And Comments

If repository code includes prompts, task instructions, or embedded agent text,
write them as direct task instructions. Clearly distinguish external references
from direct content and state who returns, saves, or exports each output.

Use code comments sparingly. Comments should explain non-obvious decisions,
constraints, provenance, or special cases. If clearer names or structure make a
comment unnecessary, simplify the code instead.

Do not write skill rules, debugging process, generation process, or style
analysis into code comments.

## Open-Source Reuse

When the task needs mature existing functionality, first decide whether legal,
appropriate, low-maintenance reuse is better than custom implementation.

Reuse preference:

1. direct dependency with stable packaging and compatible license;
2. adapter around a stable API;
3. small copied or ported snippet when license permits;
4. custom implementation when reuse would add more cost than value.

Before copying or porting external code, check license compatibility. Preserve
required notices and add a short source/provenance comment near copied or
ported code. Maintain a third-party notice file or equivalent when the
repository accumulates copied external code.

Do not vendor large unrelated projects or import heavy dependencies to satisfy a
small local feature.

## Deep Research

Use deep research when the current task involves unfamiliar language
conventions, framework organization, harness/test practice, open-source reuse,
or ecosystem-specific style. Use it to learn transferable patterns, not to copy
a public repository's structure mechanically.

If the current repository already has clear conventions, prefer the local style
and improve it only when a concrete readability, locality, or testability
problem appears.

## Validation

Use the user's requested validation command when provided. Before running, check
that every explicitly requested target exists; a missing target is a blocker to
report, not permission to silently narrow the command or create the target.
Run the command literally from the repository root unless the user gave another
working directory. Do not substitute a broader suite, omit arguments, add
environment variables, or rely on an unreported install/import workaround as
evidence for the requested command. If setup is required before the exact
command can run, state that setup separately and then rerun and report the exact
command result.
When reporting validation, keep each requested command's result separate unless
you have explicitly deduplicated overlapping tests. Do not invent a combined
total from overlapping suites, and check that any subtotals you report add up.
If a command was run twice because suites overlap, say that clearly instead of
presenting the repeated tests as additional coverage.
The headline status must match the worst required validation result. Do not say
"all validations pass", "all clean", "accepted as-is", or "complete" when any
required command failed, collected errors, or was skipped. If a failure appears
pre-existing or out of scope, label the command as failed with a pre-existing or
scope caveat; do not convert it into a passing validation summary.
If you run extra tests beyond the user's requested validation, label them as
extra guards and keep them out of the required-command total. Do not describe an
unrequested test file or suite as part of the scoped validation surface unless
the task or review explicitly added it.

For a pure structural move (no logic change), verify byte-level identity between
the new file and the original content — via diff, checksum, or file-copy
confirmation. When the task allows exactly one import-path line to differ, diff
the two files and confirm only that line changed. Verify import direction after
the move: the new canonical module should not import through the old shim path,
and layered packages should only import from lower layers. An AST-level import
scan or a focused grep for `from <wrong_direction> import` catches wrong-way
dependencies that tests may not exercise.

For source or test changes, prefer the smallest relevant test target that proves
the accepted contract, unless the user asked for a broader suite. Use command
forms that avoid repository cache or bytecode artifacts when the project allows.
When tests are intentionally removed because they covered an excluded surface,
the expected test count should decrease. Treat an unchanged or unexpectedly
higher count as a signal to re-check for stale tests. A full-suite pass is useful
context but does not replace the exact requested validation result.
If the exact validation command names files or directories, those paths are
preserved targets unless the user explicitly says to remove them. A missing
target is not a successful cleanup; restore the accepted target or report the
conflict instead of narrowing the command, deleting dependent modules, or
substituting a broader suite.
If required validation fails because an out-of-scope dependency, record,
adapter, metric, parser, or export contract is missing or incompatible, do not
repair that external contract inside the current task. Report a
validation-scope conflict with the import or call chain, the smallest candidate
scope expansion, and any in-scope validation that still passes. Passing the
requested command after unapproved out-of-scope edits is still not a successful
completion.

When a verification or refactor task discovers a **pre-existing architectural
violation** — an import direction violation, a transitive runtime dependency, a
god-module leak, a structural inconsistency — that predates the current task
scope, do not fix it and do not let it block acceptance. Classify it: is it
pre-existing (flat-module-era code that was never layered) or task-induced (the
current move/split created a new wrong-way dependency)? Pre-existing violations
are recording targets: document them in memory as deferred reconciliation work
with the specific import chain, the layer rule violated, and the suggested
narrow fix. Task-induced violations are blocking defects that must be fixed
before acceptance. The test for pre-existing: if reverting the current task's
changes would leave the violation intact, it is pre-existing. If the violation
appears only because of the current task's module move or import change, it is
task-induced.
For stabilization tasks, inspect whether the tests still prove the named
contract. A green run is weak evidence when assertions were loosened, regression
cases were removed, or only happy-path behavior remains. Restore or add focused
coverage for every user-named behavior before reporting that the surface was
already stable.
When a stabilization task says to add or verify focused tests, treat "verify"
literally. First map the existing test names, fixtures, and assertions to each
user-named behavior. If the behavior is already covered and the exact requested
validation passes, do not add duplicate tests just to create activity. Add or
restore tests only for missing, weakened, or ambiguous coverage, then report the
coverage map and exact command results.
When a stabilization pass makes no edits, the coverage map is the main
deliverable. Do not stop at "no changes needed" plus a validation table; name
the existing source, test, and docs assertions that prove each user-named
contract item, and call out any item that is intentionally only indirectly
covered.
When the scope asks for non-mutation "where applicable", treat it as a concrete
coverage item. For each helper or adapter, identify caller-owned inputs that
could be mutated, such as mappings, sequences, records, dataclasses, configs, and
fixture objects. Add a focused non-mutation assertion for every mutable or
caller-owned input, including optional scoped keys or fields, or explicitly
report why mutation is not applicable.

After validation, check for generated cache/build/test artifacts created by the
run and remove only those generated artifacts. Do not clean unrelated dirty or
untracked user work.

Before reporting success after source, test, config, or docs edits, run the
repository's normal formatting or whitespace check when one exists. If no
project-specific check is known, run the version-control whitespace check, such
as `git diff --check`, from the repository root. Treat trailing whitespace,
conflict markers, and blank-line-at-EOF warnings as blockers even when all
tests pass. This check is especially important after deleting duplicate tests,
merging adjacent blocks, or editing the end of a file.
Report whitespace checks exactly: "clean" means no output or findings. If the
check reports a pre-existing out-of-scope finding, say that it is a separate
scope conflict or pre-existing blocker; do not call the command clean and do
not fix the out-of-scope file unless the active task permits it.
In validation tables, keep the status label and note consistent: use "passed
with pre-existing warnings" or "blocked by pre-existing findings" as
appropriate, not "clean", whenever the command emits any warning or finding.

When the task has an explicit allowed-file set or excluded surface list, run a
changed-file check before reporting success. The only newly modified,
untracked, moved, deleted, or created repository paths should be the allowed
paths plus disposable validation artifacts that were removed. Also search for
the accepted symbol or capability in excluded surfaces such as package
entrypoints, export tests, docs, registries, harnesses, memory/TODO files, and
artifact writers when those surfaces were named as exclusions. Passing tests do
not override an out-of-scope changed file or stale excluded-surface reference.
If you report that a file or capability was removed, verify the file path no
longer exists, no untracked placeholder remains, and no package metadata or
module entrypoint still references it.
If you report that a file was rewritten, replaced, or reduced to a narrower
surface, re-open the final file from disk and verify the exact callable
signature, key result fields, line-level absence of prohibited imports or
helpers, and expected line-count direction before reporting success. Do not rely
on an editor buffer, generated patch text, prior session output, or developer
report as evidence that the rewrite persisted.
For importable modules, also verify that the code loaded by the validation
environment is the same final source file when stale behavior has appeared
before. Use the language's normal inspection tools when cheap, such as checking
the loaded file path and public signature. If the test runner imports an older
surface than the file you think you wrote, stop and resolve that mismatch before
claiming validation success.
When the user gives an absence or stale-reference search, run that command
literally. If no command is given, search every plausible surface for the banned
capability: tracked and untracked source, tests, docs, package metadata, module
entrypoints, examples, configs, and harness descriptors. Do not limit the search
to the files you edited or to the modules you expected to change.
For docs-only cleanup with an exact absence command and scoped file list, treat
that command as the primary acceptance gate. Run it before editing to build the
hit list, and rerun it after every docs pass until it returns zero hits across
all scoped files. Do not mark unedited files as "unaffected", "already clean",
or "persisted" from memory; the final absence output and targeted readback must
prove every scoped file is clean. If the absence command still has hits, report
the remaining stale surfaces instead of using passing tests as a completion
claim.
Exact absence searches are literal, not semantic. A banned phrase still fails
when it appears in a negative boundary statement, future-plan note, heading, or
historical sentence. Rephrase scoped docs so the exact tokens disappear while
preserving the boundary meaning, or report a scope conflict if the stale phrase
must remain in an out-of-scope historical surface.
If an exact absence command matches accepted baseline surfaces or unrelated
scoped documentation, keep the original command as the failing task evidence and
report the scope conflict. A narrowed or corrected regex can be useful as a
diagnostic, but it is not a substitute for the user's required validation
command unless the user or reviewer revises the task. Do not remove accepted
baseline documentation, exports, tests, or API names only to satisfy an
overbroad absence pattern.
Rerun absence searches after the final edit, not before the last deletion. For
file deletion, verify each requested path individually with a filesystem check;
glob output, command success text, or a prior deletion attempt is not proof that
the file is absent.

For docs-only or TODO-only work, do not run tests unless executable code or
test files changed accidentally. Re-read edited docs/TODO files and run targeted
text searches for the accepted names, stale predecessor names, and broad absence
phrases that were in scope.

When README-style docs must describe focused test coverage, include targeted
readback checks for the scoped coverage nouns and discriminators, not only the
new public symbol. Search for the tie-break field, opposite-order fixture clue,
metadata key or value, provenance field, invalid-input category, and exact
non-mutation target when the user named them.

For multi-surface docs, do not rely on whole-file search alone. Check the
specific edited section or paragraph type that was in scope, especially test
summary paragraphs in translated docs, so a term present elsewhere in the same
file does not mask a stale summary.

For Markdown docs with nested bullets or long copied list blocks, audit the
local hierarchy after editing. Read the lines around every edited heading and
the next sibling heading or bullet. Confirm top-level file, module, test, or
artifact bullets remain siblings rather than becoming children of the previous
coverage block, and confirm nested bullets are nested only where intended.
For each edited bullet, compare its literal indentation prefix with the nearest
same-level sibling and nearest child bullet in the same list. A child entry
under a module/test/feature parent should keep the same prefix as neighboring
children; a new sibling module/test/file entry should keep the same prefix as
neighboring siblings. Do this line-level check before reporting docs-only
validation complete.

For README-style docs that extend a roster from a previous accepted subject,
search both the predecessor token and the new token after editing. Read every
remaining predecessor occurrence in local context and confirm either that the
new token appears in the same current roster, layout row, summary, or coverage
block, or that the predecessor occurrence is intentionally historical and not a
current-surface list.

When scoped details reuse strings already present for other subjects, validate
with local context: the current subject name and the required fixture, metadata,
reason, or config term should appear in the same bullet, paragraph, or clearly
bounded coverage block.

When the scope names an exact callable signature, return type, output container,
or record immutability contract, validate that exact contract in every requested
surface that names the callable. Read local context around the callable in each
document; a whole-file hit for the record name or helper name does not prove the
API surface carries the return contract.

When a scoped invalid-value matrix names multiple keys or inputs, validate each
owner separately in local context. Search/read back for every named key or input
together with the invalid-value class or explicit invalid values in the same
test-summary bullet, paragraph, or bounded coverage block.

When a docs-sync scope includes both default and non-default configured
fixtures, read back those bullets separately. Confirm the config value or
"default" label matches the expected selected/rejected IDs and reasons in that
same local context.

When the user names specific excluded capability categories, include those
terms or close equivalents in docs/TODO readback searches. The check should
confirm that absence wording stayed narrow for every explicitly scoped
exclusion, not only that the new accepted name appears.

For README-style docs, include a quick local prose cleanup pass on edited
paragraphs: remove duplicated adjacent words or lines, stale sentence tails left
after rewriting a clause, and grammar artifacts that can make a scoped absence
claim ambiguous.

## Review Guidance

When reviewing, lead with defects that harm readability, locality, naming,
state ownership, interface clarity, harness/test separation, artifact shape, or
framework consistency.

Prefer review suggestions that delete, inline, move to the use site, rename,
align ordering, split responsibilities, clarify ownership, or reduce caller
burden. Do not default to adding wrappers, registries, config layers, factories,
or defensive branches unless they solve a concrete defect.

For bounded helpers, verify that the implementation:

- reads only the accepted inputs and fields;
- maps external source fields to the requested internal output names without
  leaking raw source names into public records unless explicitly scoped;
- rejects invalid inputs at the intended validation owner;
- implements numeric contracts literally, including rejecting infinities when a
  value must be finite and preserving weaker legacy validators unless changing
  them is explicitly in scope;
- returns the accepted record or value shape;
- preserves provenance when requested;
- does not mutate source records or inputs unless mutation is the contract;
- keeps identity behavior delegated to the accepted record or schema type;
- keeps any reused private helper name semantically true for all current
  callers;
- avoids adjacent runtime surfaces such as loaders, registries, exporters,
  harnesses, CLI, experiments, or paper outputs unless explicitly in scope.

When reviewing a scoped change with an allowed-file list, compare the actual
changed-file list against that list before reviewing behavior. Flag any package
export, export-surface test, documentation, registry, harness, artifact writer,
TODO/memory note, stash/backup directory, generated file, or adjacent module as
blocking when the request excluded it. Do not accept in-repository stash folders
as cleanup; out-of-scope work must be removed from the task's worktree state or
explicitly separated outside the repository by user-approved workflow.
For cleanup reviews, compare deletions against the preservation map and the
requested validation command. Deleting a validation target, accepted feature, or
unrelated subsystem is blocking even when the stale excluded search becomes
clean. Import errors after removing an excluded file usually mean stale public
wiring remains; they do not justify deleting the importer or collapsing the
larger surface.
When the developer claims an excluded capability was removed, verify with the
filesystem, full untracked status, and targeted search. Comment-only stubs,
empty files, disabled tests, parser branches, package metadata entries, module
entrypoints, and docs that still mention the capability are still present
surfaces. Treat mismatches between the report and the worktree as blocking
until the worktree is the source of truth.

When a parameter, option, command, or public surface is removed, search its
literal name across implementation, tests, docs, configs, and examples, then
read the caller chain around remaining hits. A stale signature, forwarded
keyword, config key, fixture assertion, or README command is blocking unless it
is explicitly outside the task and reported as a scope conflict.
For command-like surfaces, search both structural names and user-visible
actions: module names, compatibility aliases, entrypoint functions, parser or
handler helpers, package metadata keys, command strings, and tests that import
or exercise those handlers. A wrapper that only re-exports the removed handler
is still the removed surface.

When reviewing a stabilization report that says no changes were needed, still
compare implementation and tests against the accepted contract. Flag drift in
call signatures, default arguments, derived keys, empty-input handling,
non-mutation or provenance behavior, and removed regression tests even if the
requested commands pass.

For documentation reviews, compare every newly edited absence clause against
the implemented-surface list, package/module summaries, layout rows, and test
summaries. Treat broad "no <category>" wording as a defect when a narrower
bounded surface in that category is already accepted; ask for the smallest
wording fix instead of reopening source or tests.
If a file is meant to be a static config or example, docs should not describe it
as a runner, entrypoint, command surface, managed artifact generator, or paper
output path. Replace execution-surface wording with the narrow API or config
semantics that the task actually accepts.
Also treat leftover duplicated words, duplicated sentence tails, or malformed
negative clauses as docs defects when they change or obscure the intended
scope.

Also compare every requested test-coverage detail against each edited test
summary surface, including translated README surfaces. If one document keeps a
generic coverage phrase while another contains the precise discriminating
fixture or non-mutation target, request the smallest wording fix in the stale
document only.

Treat cross-surface leakage as a docs defect: a required rejection reason,
metadata value, fixture ID, provenance field, or mutation target is still
missing if it appears only in a helper/API list while the scoped test-summary
paragraph omits it.

Treat exact-contract leakage as a docs defect: if the user supplied a callable
signature, return annotation, output container, or frozen/immutable record
promise, every requested API or module surface that names the callable must
state that exact contract or a direct equivalent in the same local context.

Treat roster leakage as a docs defect: when a request extends an implemented
surface that was previously listed through an older subject, any current
helper list, module summary, package summary, layout row, parenthetical roster,
or test summary that still stops at the predecessor is stale even if another
surface in the same file already includes the new subject.

Treat subject leakage as a docs defect too: a required fixture, metadata value,
rejection reason, or config key is still missing if it appears only under a
neighboring helper, scheduler, method, metric, or test block.

Treat unrelated-subject drift as a docs defect. If a docs-sync task is scoped
to one accepted symbol, helper, parser, method, metric, artifact, or test, do
not accept rewrites to neighboring subjects merely because they are nearby in
the same README. Request the smallest revert or wording trim unless the
neighboring edit is necessary to keep a shared sentence, roster, or absence
clause truthful.

Treat validation-owner leakage as a docs defect: if a scoped invalid-value set
applies to multiple named keys, fields, modes, or inputs, the test-summary
surface is stale when it documents the invalid set for only one owner or hides
the owner list behind a vague "invalid config" phrase.

Treat validation-owner leakage as a test defect too: when the implementation
contract names multiple finite values, integer fields, or parameters that must
reject booleans, require at least one focused test per owner or a compact
parametrized test that names each owner. Do not accept a single neighboring
owner's `NaN`, infinity, or boolean test as coverage for the whole helper.

Treat default/config leakage as a docs defect: a test-summary surface is stale
when it labels a fixture with an explicit non-default configuration as default,
or when it documents the configured fixture but omits the separate default
fixture expectation named by the scope.

For documentation reviews, also check the scope sentence or heading that
introduces grouped bullets. A fact is misdocumented if it appears under a group
where one or more named subjects do not own that metadata value, rejection
reason, config key, fixture, or coverage case, even if the fact is present
somewhere in the requested file.

Treat Markdown hierarchy drift as a docs defect. If an edited file, module,
test, artifact, or capability bullet becomes nested under a neighboring
coverage block or subject, request a smallest-possible indentation fix even
when the words themselves are correct.

For docs that describe staged, filtered, or multi-path behavior, verify that the
primary ordering coverage, phase priority, subset definition, and each
rejection reason are all present in the correct test-summary surface. A broad
"rejected with <reason>" phrase is a defect when only one filtered subset uses
that reason and another path uses budget, validation, or a different rejection
contract.

Review tests against their fixture values and names. If a test name says
"all-zero", "empty", "single", "all", or "none", the fixture should actually
match that case. Passing tests are not enough when naming, boundary, or
provenance contracts are misleading.

For variants added next to an existing formula or helper, check that at least
one focused test distinguishes the new variant from the nearest existing one.
Do not accept a mixed fixture that would still pass if the implementation used
the previous threshold, percentile, sort direction, condition, or field.

For sort-chain tests, trace the expected order through the exact sort tuple.
Reject a fixture if the expected winner is also favored by a lower-priority
fallback key or by an unrelated aligned field. Each named tie-break level should
have at least one fixture that would fail if that level were omitted.
Do not trust helper names, object IDs, or comments that say "earlier", "later",
"best", or "tie" unless the underlying field values prove that relationship and
the fallback fields are adversarial where needed.
If review scope asks for a combined fallback chain, such as `<primary>/<id>` or
`<primary>/<secondary>/<id>`, verify there is both a dominance fixture for each
non-final key and a same-higher-key fixture for the final identifier fallback.

For staged, filtered, or partitioned-lane schedulers, review the sort tuple for
every stage, lane, or accepted subset separately, including default or regular
subsets. If a phase says it orders by one key and then a fallback key, require
one discriminator for the first key and a separate same-key fixture for the
fallback; do not accept a same-key fixture as evidence that the first key is
implemented.

For resource-isolation claims, check the fixture has unused capacity in at least
one non-borrowing partition and an over-limit item in another partition. A test
where each lane, quota, queue, or resource pool exactly consumes its own budget
does not prove that unused capacity cannot leak across boundaries.

For budgeted selectors, review invalid-budget tests separately from
over-budget selection tests. If the task asked for budget rejection and reason
capture, require a valid-budget fixture where an otherwise eligible candidate
is rejected only because remaining budget is insufficient, and assert that
candidate's exact rejection reason. Do not count missing-budget behavior,
invalid-budget exceptions, filtered objects, cadence skips, or type rejections
as over-budget coverage.

For ordered selectors, review missing-budget or unbounded-budget assertions
against the same filtering, staging, and sort tuple used by constrained-budget
selection. Selecting every eligible candidate should still prove the accepted
ordering contract unless the requested behavior explicitly preserves input
order.

When addressing review feedback in a file with repeated tests or similar helper
fixtures, verify the exact named test, helper, or caller cited by the review was
changed. Do not treat a similar edit in a neighboring existing test as
satisfying feedback for the new surface.

## Readability Audit

After edits, audit:

- names match real meaning and data shape;
- data flow is direct and naturally ordered;
- functions, files, and modules have clear responsibilities;
- abstractions reduce real complexity rather than add jumps;
- no avoidable global state, hidden paths, repeated registration points, or
  heavy config burden were added;
- the change stayed local to the natural owner;
- stabilization preserved accepted callable signatures, defaults, key
  derivation, boundary behavior, provenance, non-mutation, and regression
  coverage;
- cleanup preserved validation targets and accepted work instead of deleting
  dependent modules, tests, or subsystems to avoid stale references;
- harness and test responsibilities remain separate;
- artifact schemas, exporters, docs, and tests agree when any changed;
- framework docs were updated or confirmed current when in scope;
- external reused code has compatible license and attribution;
- explicit allowed-file and excluded-surface scope was preserved, including no
  in-repository stash, backup, memory, TODO, export, docs, harness, registry, or
  artifact files created as cleanup side effects;
- edited files pass the repository whitespace or diff check; test
  deduplication, file-end edits, and copied docs blocks left no trailing
  whitespace, conflict markers, or extra blank lines at EOF;
- excluded capabilities are absent from source files, tests, docs, package
  metadata, parser or handler branches, module entrypoints, and untracked files,
  with no explanatory stubs or placeholders left behind;
- no generated cache/build/test/output/result artifacts were left behind unless
  explicitly requested.

For skill edits, also perform a project leakage audit. Remove or generalize any
real project path, symbol, dataset, method, metric, harness, test, artifact
field, historical output, or one-off debug lesson that does not hold across
repositories.

## Final Response

Keep the final response concise: changed paths, behavior or contract covered,
validation performed, and caveats that affect the user's next action.

A round's real delta includes verification runs, memory-record flips, and
docs/config syncs, not only source/test edits. Report the real delta verified
against prior on-disk state, not against memory or a task narrative. A
verification run plus a status/memory flip IS a deliverable — not "no work."

For a pure verification pass where no new edits are needed, describe the checks
performed and their results, and state "no new changes made" or "prior work
confirmed intact on disk."

Do not explain skill internals, tool mechanics, or style theory unless the user
asked for a skill optimizer report.
