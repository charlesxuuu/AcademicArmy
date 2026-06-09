# Evolve Skill Pipeline

[`src/evolve-skill`](.) implements the self-evolution loop used by the metaskill evolution scripts described in [`../../metaskills/README.md`](../../metaskills/README.md). It is for improving an existing skill by repeatedly testing it on a fixed task, evaluating the produced artifact, and applying targeted revisions.

[中文说明](README.zh-CN.md)

For the overall TypeScript pipeline usage and entry points, see [`src/README.md`](../README.md).

For the user-facing optimization workflow, see [`../../metaskills/README.md`](../../metaskills/README.md).

## Quick Start

When a skill output is weak, add concrete tips to the matching metaskill file, then run that skill's evolution script from the repository root. See [`../../metaskills/README.md`](../../metaskills/README.md) for the prepared scripts and path mapping.

```bash
bash metaskills/academic-army-architect/envolve.sh
```

## Direct Command

Run the pipeline directly from the repository root:

```bash
npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-architect \
  --artifact-path output/evolve-academic-army-architect \
  --metaskill-path metaskills/academic-army-architect/METASKILL.md \
  --task-path metaskills/academic-army-architect/ENVOLVETASK.md
```

## Options Reference

Required arguments:

| Option | Description |
|---|---|
| `--skill-path` | The skill directory or file to revise. |
| `--artifact-path` | The output folder cleared and reused by each runner round. |
| `--metaskill-path` | The metaskill design document used by evaluator and modifier. |
| `--task-path` | The fixed task used by the runner to test the skill. Repeat this option to run multiple fixed tasks per round. |

Optional arguments:

```text
--rounds 5
  Number of self-evolve rounds to run.
```

`--rounds` defaults to `3`.

## Main Flow

[`pipeline.ts`](pipeline.ts) parses:

- `--skill-path`: the skill directory or file to revise.
- `--artifact-path`: the output directory cleared and reused each round.
- `--metaskill-path`: the design document and tips used to judge and revise the skill.
- `--task-path`: one or more fixed tasks used to test the skill.
- `--rounds`: the number of self-evolve rounds, defaulting to `3`.

Each round does the following:

1. Clear and recreate `--artifact-path`.
2. For each configured `--task-path`, create a fresh `skill-runner` agent to run the target skill on that fixed task and write artifacts.
3. Use `skill-evaluator` to evaluate the artifact against the current metaskill guidance file.
4. Pass the evaluator review to `skill-modifier`, which revises the target skill using the same metaskill guidance.

The fresh runner keeps each artifact independent from earlier runner context. The evaluator and modifier are invoked through the shared `AgentTeam` so their configured agent behavior is centralized in the pipeline config.

## Loop Behavior

The loop keeps skill development grounded in concrete output. Instead of rewriting a skill from vague impressions, it tests the skill on a stable task, evaluates the resulting artifact against the metaskill, and then asks Codex to revise the skill based on concrete feedback.

The pipeline keeps two long-lived Codex threads through the shared team:

1. `skill-evaluator`: reviews artifacts across rounds.
2. `skill-modifier`: edits the target skill across rounds.

Each round also creates a fresh one-time `skill-runner` thread. The runner has no memory from previous rounds, so earlier artifacts do not pollute the next run.

The loop deliberately stays simple:

1. A fresh runner thread runs the target skill for each configured task and writes artifacts to an output folder.
2. A long-lived evaluator thread reviews the artifact using the metaskill.
3. A long-lived modifier thread edits the skill according to the evaluator feedback.
4. The next round starts with a fresh runner thread.

This avoids LangGraph, state machines, registries, and defensive wrapper code. The important state lives in the long-lived evaluator/modifier Codex sessions, the current artifact folder, and the files being revised.

## Inputs And Outputs

| Item | Path source |
|---|---|
| Target skill | `--skill-path` |
| Metaskill | `--metaskill-path` |
| Fixed task | `--task-path` |
| Generated artifact folder | `--artifact-path`, cleared and reused each round |

## Important Files

| Path | Purpose |
|---|---|
| [`pipeline.ts`](pipeline.ts) | Argument parsing and round orchestration. |
| [`agents/factory.ts`](agents/factory.ts) | Registers `skill-runner`, `skill-evaluator`, and `skill-modifier`. |
| [`agents/runner.ts`](agents/runner.ts) | Reads each fixed task file configured by `--task-path` and asks the target skill to write artifacts. |
| [`agents/evaluator.ts`](agents/evaluator.ts) | Reads the metaskill file configured by `--metaskill-path` and critiques the produced artifact. |
| [`agents/modifier.ts`](agents/modifier.ts) | Reads the metaskill file and the evaluator review, then revises the target skill. |

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| Artifacts disappear between rounds | `--artifact-path` is cleared and reused each runner round. | Use a dedicated `output/evolve-*` folder. |
| The output still feels weak | The loop needs concrete metaskill guidance. | Add concrete tips to the matching metaskill file and run the script again. |
| Runner context seems to influence results | The runner should be fresh each round. | Check the pipeline config and archive the generated artifacts for comparison. |
