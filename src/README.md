# TypeScript Pipelines

`src` contains the local TypeScript runner for AcademicArmy skill evolution. Development-loop pipelines are imported from `developing-agent-forge`.

[中文说明](README.zh-CN.md)

## What This Code Owns

[`package.json`](../package.json) exposes these pipeline commands. The local [`cli.ts`](cli.ts) entry point also registers them for `npm run cli -- <pipeline>`:

| Pipeline           | Package script             | What it does                                                                                                                          |
| ------------------ | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `developing`       | `npm run developing`       | Runs the code development loop provided by `developing-agent-forge`; the current task focus comes from `--goal-path`.                  |
| `developing-skill` | `npm run developing-skill` | Runs the same imported development loop with a trajectory optimizer that can revise the coding-style skill from concrete feedback.    |
| `evolve-skill`     | `npm run evolve-skill`     | Runs the skill self-evolution loop implemented in `evolve-skill/`.                                                                    |

[`pipeline.ts`](pipeline.ts) provides the shared wrapper for the local `evolve-skill` pipeline. The `developing` and `developing-skill` implementations come from `developing-agent-forge`.

## Quick Start

Install dependencies once from the repository root:

```bash
npm install
```

The shared CLI shape is:

```bash
npm run cli -- <pipeline> [...args]
```

For most project workflows, use the prepared shell scripts:

```bash
bash runs/develop.sh
bash metaskills/academic-army-architect/envolve.sh
```

Before each new development task, update `output/goal.md`, which the prepared `developing` and `developing-skill` wrappers pass as `--goal-path`.

## Directory Guide

| Path                                                         | Purpose                                                                                                                                                                          |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cli.ts`](cli.ts)                                           | Selects a pipeline by name and forwards the remaining CLI arguments.                                                                                                             |
| [`pipeline.ts`](pipeline.ts)                                 | Shared pipeline definition, config loading, agent-team construction, and cleanup.                                                                                                |
| [`evolve-skill/`](evolve-skill/)                             | Runs a skill on a fixed task, evaluates the artifact against a metaskill, and asks a modifier agent to revise the skill. See [`evolve-skill/README.md`](evolve-skill/README.md). |

## How The Shared Wrapper Works

Each local pipeline provides pipeline-specific arguments and configured factories. [`pipeline.ts`](pipeline.ts) loads one or more YAML config files with `coding-agent-forge`, builds an `AgentTeam` from the configured factories, runs the selected pipeline, and closes the team afterward.

This keeps the config loading, agent-team construction, and cleanup shared across the TypeScript runners.

## Relationship To Shell Scripts

Shell scripts under [`runs/`](../runs/) and the metaskill scripts described in [`metaskills/README.md`](../metaskills/README.md) are convenience wrappers around these TypeScript pipelines.

The prepared development wrappers use `output/goal.md` as the `--goal-path` file. Development memory is split between `output/developing-memory/project-progress-memory` and `output/developing-memory/code-design-memory`; edit or delete stale files there when a new goal should not inherit old context.

| Script                                              | Calls                      |
| --------------------------------------------------- | -------------------------- |
| [`runs/develop.sh`](../runs/develop.sh)             | `npm run developing`       |
| [`runs/develop-skill.sh`](../runs/develop-skill.sh) | `npm run developing-skill` |
| `metaskills/*/envolve.sh`                           | `npm run evolve-skill`     |

## Development Checks

Run these before changing runner code:

```bash
npm run check
npm run lint
```

## Where To Go Next

- Development loop details: the `developing-agent-forge` package
- Skill evolution loop details: [`evolve-skill/README.md`](evolve-skill/README.md)
- User-facing skill evolution workflow: [`../metaskills/README.md`](../metaskills/README.md)
