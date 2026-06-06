---
name: academic-army-repo-init
description: >-
  Initialize a static, orderly, extensible research-code repository skeleton
  from a paper blueprint, experiment plan, coding plan, and user-specified
  target repository path. Use when Codex must create concrete directories,
  dependency/config files, source interfaces, harness folders, test folders,
  result-artifact contracts, README plus FRAMEWORK handoff docs, a compact
  self-audit manifest, and deterministic static validation for an Academic Army
  autoresearch project without implementing final paper methods, running
  installs, executing tests, running harnesses, or placing project files outside
  the requested repository path.
---

# Academic Army Repo Init

Read [`references/repo-init-contract.md`](references/repo-init-contract.md) only
when a detail below needs expansion. Use
[`scripts/repo_init_audit.py`](scripts/repo_init_audit.py) for the final static
audit when Python is available.

## Generation Contract

1. Read only the required inputs: paper blueprint, experiment plan, coding plan,
   target repository path, explicit user constraints, and initialization-relevant
   files already inside the target path.
2. Use `academic_army_mcp_tools.deepresearch` before choosing language,
   framework, tooling, and related-code references, unless fresh equivalent
   evidence already covers the paper domain, ecosystem practices, packaging,
   harnesses, tests, and raw artifacts.
3. Decide the repository frame from paper needs plus research evidence:
   language/toolchain, ecosystem source layout, config mechanism, entrypoint
   style, static tools, core interfaces, harnesses, tests, and artifact schema.
4. Create or preserve the fixed experimental inventory at the target root:
   `data/`, `output/`, `results/`, `harness/`, `test/`, `README.md`,
   `FRAMEWORK.md`, and `FRAMEWORK.zh-CN.md`.
5. Create the ecosystem-specific source/config/dependency structure selected in
   step 3. Do not hardcode Python, TypeScript, or any other language layout.
6. Add real scaffold logic: config parsing, domain records, method/baseline
   boundary, metric boundary, loader or adapter boundary, harness-shaped
   entrypoint, artifact writer/schema, and functional test entrypoints.
7. Add one semantic subfolder per harness under `harness/`, tied to a concrete
   claim/question, target module, input protocol, metrics, and raw artifact
   schema.
8. Add one semantic subfolder per test group under `test/`, tied to a functional
   contract with toy input, expected behavior, and pass/fail criterion.
9. Add concise `README.md`, complete English/Chinese `FRAMEWORK` handoff docs,
   and `output/repo-init-self-audit.json` describing real generated paths,
   placeholders, dependencies, artifact fields, attribution, and static status.
10. Run static audit only. Do not install dependencies, execute project tests,
    run harnesses, run experiments, train models, download benchmarks, or use
    notebooks as validation.

## Hard Requirements

- Keep every created, modified, and referenced project file under the target
  repository path. Repository docs use repo-relative paths only.
- Preserve existing target-repo user content; add missing initialization
  structure with minimal edits.
- Keep `harness/` and `test/` separate: harnesses evaluate paper goals, tests
  validate functional contracts.
- Configure the chosen test tool to use top-level `test/` if its ecosystem
  default differs.
- Prefer packaged, maintained tools as dependencies. Copy code only when it is
  necessary, small, license-compatible, and attributed in the repository.
- Make placeholders honest: name the interface, accepted inputs, required
  outputs, emitted artifact fields, and intentionally absent behavior.
- Keep raw artifacts low-processing and parseable. Figure/table generation is
  downstream analysis, not core scaffold logic.

## Redundancy Rejection

Before final output, remove or justify:

- empty template files with no future contract
- repeated sections between `README.md`, `FRAMEWORK.md`, and
  `FRAMEWORK.zh-CN.md`
- placeholder modules without distinct semantic roles
- pass-through helpers that only rename, wrap, unwrap, forward, or reassemble
  values
- multiple registries/adapters for the same method boundary
- duplicate schema/type definitions
- duplicate harness/test descriptions that do not map to separate research or
  functional goals
- generic CI, web dashboard, database, service, or distributed infrastructure
  unless required by the planning artifacts and research evidence
- sample modules not connected to a harness, test, config, or artifact schema

## Static Audit Checklist

Run `python skills/academic-army-repo-init/scripts/repo_init_audit.py <target-repo>`
or perform equivalent static checks. Confirm:

- fixed top-level inventory exists
- `README.md` is short and framework docs describe only real generated paths
  and supported or reserved commands
- every documented harness/test/module/config/artifact path exists
- every harness maps to a claim/question, metric set, input protocol, and raw
  artifact schema
- every test group maps to a functional contract and small fixture or toy input
- placeholders are labeled and tied to concrete interface contracts
- dependency/layout choices are tied to deepresearch and paper needs, not a
  fixed template
- docs contain no absolute local paths or runtime workaround notes
- source/config files are syntactically plausible for the selected ecosystem
- artifact schema names are consistent across code, configs, docs, harnesses,
  tests, and self-audit
- copied or adapted external code has source, license, and attribution
- unrelated infrastructure and redundant wrappers/templates are absent

## Final Response

Report the target repo path, selected language/tooling, created fixed inventory,
ecosystem directories, framework docs, self-audit manifest, harness/test groups,
raw artifact/config contracts, placeholders left for later coding skills, and
static audit result. Do not include tool logs, sandbox narratives, or unrelated
local context unless they directly block repository creation.
