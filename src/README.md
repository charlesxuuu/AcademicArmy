# TypeScript Pipelines

`src` contains the TypeScript runners that turn AcademicArmy planning artifacts into repeatable agent workflows.

The CLI entry point is [`cli.ts`](cli.ts). It exposes two pipelines through [`package.json`](../package.json) scripts:

- `npm run developing`: runs the code development loop implemented in `developing/`.
- `npm run evolve-skill`: runs the skill self-evolution loop implemented in `evolve-skill/`.

[`pipeline.ts`](pipeline.ts) provides the shared wrapper used by both commands. It parses pipeline-specific arguments, loads one or more YAML config files with `coding-agent-forge`, builds an `AgentTeam` from the configured factories, runs the selected pipeline, and closes the team afterward.

## Directory Guide

- [`cli.ts`](cli.ts): selects a pipeline by name and forwards the remaining CLI arguments.
- [`pipeline.ts`](pipeline.ts): shared pipeline definition, config loading, agent-team construction, and cleanup.
- [`developing/`](developing/): reads `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md`, then iteratively implements the target codebase. See [`developing/README.md`](developing/README.md).
- [`evolve-skill/`](evolve-skill/): runs a skill on a fixed task, evaluates the artifact against a metaskill, and asks a modifier agent to revise the skill. See [`evolve-skill/README.md`](evolve-skill/README.md).

## Relationship To Shell Scripts

Shell scripts under [`runs/`](../runs/) and the metaskill scripts described in [`metaskills/README.md`](../metaskills/README.md) are convenience wrappers around these TypeScript pipelines.

- [`runs/develop.sh`](../runs/develop.sh) calls `npm run developing`.
- The `metaskills/*/envolve.sh` scripts described in [`metaskills/README.md`](../metaskills/README.md) call `npm run evolve-skill`.
