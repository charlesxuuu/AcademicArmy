# TypeScript Pipelines

`src` contains the local TypeScript runner for AcademicArmy pipelines. The development loop is imported from `developing-agent-forge`; the skill evolution loop is implemented locally.

[中文说明](README.zh-CN.md)

## What This Code Owns

[`package.json`](../package.json) exposes these pipeline commands. The local [`cli.ts`](cli.ts) entry point also dispatches them for `npm run cli -- <pipeline>`:

| Pipeline       | Package script         | What it does                                                                                                          |
| -------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `developing`   | `npm run developing`   | Runs the code development loop provided by `developing-agent-forge`; the current task focus comes from `--goal-path`. |
| `evolve-skill` | `npm run evolve-skill` | Runs the skill self-evolution loop implemented in `evolve-skill/`.                                                    |

The `developing` implementation and agents come from `developing-agent-forge`. [`agent-forge.yaml`](../agent-forge.yaml) supplies Ponytail and the local coding-style metaskill to its developer and code reviewer. [`evolve-skill/pipeline.ts`](evolve-skill/pipeline.ts) implements the local skill evolution pipeline.

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

Before each new development task, update `workspace/plan/goal.md`, which the prepared `developing` wrapper passes as `--goal-path`.

## Directory Guide

| Path                             | Purpose                                                                                                                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cli.ts`](cli.ts)               | Selects a pipeline by name and forwards the remaining CLI arguments.                                                                                                             |
| [`evolve-skill/`](evolve-skill/) | Runs a skill on a fixed task, evaluates the artifact against a metaskill, and asks a modifier agent to revise the skill. See [`evolve-skill/README.md`](evolve-skill/README.md). |

## How The CLI Works

[`cli.ts`](cli.ts) dispatches each pipeline through `coding-agent-forge`, which loads one or more YAML config files, builds an `AgentTeam` from the selected pipeline's factories, runs it, and closes the team afterward.

## Relationship To Shell Scripts

Shell scripts under [`runs/`](../runs/) and the metaskill scripts described in [`metaskills/README.md`](../metaskills/README.md) are convenience wrappers around these TypeScript pipelines.

The prepared development wrappers use `workspace/plan/goal.md` as the `--goal-path` file. Development memory is split between `workspace/memory/project-progress` and `workspace/memory/code-design`; edit or delete stale files there when a new goal should not inherit old context.

| Script                                  | Calls                  |
| --------------------------------------- | ---------------------- |
| [`runs/develop.sh`](../runs/develop.sh) | `npm run developing`   |
| `metaskills/*/envolve.sh`               | `npm run evolve-skill` |

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
