# Metaskills

`metaskills` stores the design notes and self-evolve workflow used to build and improve AcademicArmy skills.

[中文说明](README.zh-CN.md)

## Why This Directory Exists

The core design idea is skill self-evolve: use one evaluator agent to judge the output produced by a skill, pass that evaluation to a modifier agent, let the modifier revise the skill, and repeat the loop until the skill becomes better through concrete output, critique, and revision.

A normal skill describes how an agent should complete a research-planning task. A metaskill describes how that skill itself should be designed: its goals, writing style, expected outputs, and the issues to watch for when revising it. During self-evolve, the evaluator uses the metaskill as the standard for judging the artifact, and the modifier uses it as the standard for revising the skill.

## When To Use This Workflow

If a skill's output is unsatisfactory, improve the matching metaskill first instead of editing the skill from vague impressions.

This is especially useful for the three planning skills used at the start of the AcademicArmy workflow: `academic-army-architect`, `academic-army-experiment-plan`, and `academic-army-coding-plan`. When their direct outputs are not what you want, write the dissatisfaction into the matching metaskill and run several `envolve.sh` rounds.

## Quick Start

### 1. Pick the matching metaskill

Prepared AcademicArmy skill metaskills:

| Skill                           | Edit this file                                                                             | Run this script                                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `academic-army-architect`       | [`academic-army-architect/METASKILL.md`](academic-army-architect/METASKILL.md)             | [`academic-army-architect/envolve.sh`](academic-army-architect/envolve.sh) with `bash`             |
| `academic-army-experiment-plan` | [`academic-army-experiment-plan/METASKILL.md`](academic-army-experiment-plan/METASKILL.md) | [`academic-army-experiment-plan/envolve.sh`](academic-army-experiment-plan/envolve.sh) with `bash` |
| `academic-army-coding-plan`     | [`academic-army-coding-plan/METASKILL.md`](academic-army-coding-plan/METASKILL.md)         | [`academic-army-coding-plan/envolve.sh`](academic-army-coding-plan/envolve.sh) with `bash`         |
| `academic-army-coding-style`    | [`academic-army-coding-style/METASKILL.md`](academic-army-coding-style/METASKILL.md)       | [`../runs/develop.sh`](../runs/develop.sh) with `bash`                                             |

Before calling `evolve-skill` for `academic-army-architect`, create or confirm [`academic-army-architect/ENVOLVETASK.md`](academic-army-architect/ENVOLVETASK.md). This fixed task is what the runner uses to test the architect skill across evolution rounds.

The `academic-army-coding-style` metaskill defines the code structure and style preferences used by code-writing agents. Add any durable preference about concise code, module boundaries, dependency choices, review standards, naming, or repository-local style to [`academic-army-coding-style/METASKILL.md`](academic-army-coding-style/METASKILL.md). [`agent-forge.yaml`](../agent-forge.yaml) loads it for both the developer and code reviewer on every [`runs/develop.sh`](../runs/develop.sh) run.

### 2. Add concrete tips

Open the corresponding metaskill file and add concrete tips about the failure mode: what the artifact did wrong, what the skill should prefer, and what it should avoid next time.

The metaskill design document for a target skill should describe what the skill is trying to produce, what good output looks like, what common failure modes matter, and what should stay out of the skill.

### 3. Run the prepared script

Install dependencies once:

```bash
npm install
```

Run a prepared skill evolution script from the repository root:

```bash
bash metaskills/academic-army-architect/envolve.sh
```

Run the prepared script to call the `evolve-skill` pipeline with that skill's paths. See [`src/evolve-skill/README.md`](../src/evolve-skill/README.md) for what the script runs and how the loop behaves.

### 4. Inspect the new artifact

Inspect the new artifact and repeat if the skill is still not stable enough.

Running the linked evolution scripts calls the TypeScript `evolve-skill` pipeline. See [`src/README.md`](../src/README.md) for the TypeScript entry points and [`src/evolve-skill/README.md`](../src/evolve-skill/README.md) for the evolution loop implementation.

## What The Evolution Loop Does

AcademicArmy skills are developed through an iterative meta-skill workflow rather than written once and treated as final.

We first draft an initial version of the skill. The prompts and notes used for this initial drafting process are kept in the matching [`metaskills`](.) directory, so readers can inspect how the skill itself was produced.

After that, we choose a fixed test topic and repeatedly run the following loop:

1. Execute the skill on the fixed topic.
2. Give the skill output, together with the relevant records from `metaskills`, to an evaluator agent.
3. Ask that agent to analyze the skill carefully: what problems it has, which parts are redundant, and where its language, structure, or content can be improved.
4. Give the resulting revision suggestions to Codex and ask Codex to update the skill.
5. Execute the revised skill again on the same fixed topic.

This loop lets us compare different versions under a stable task setting. The goal is to make each skill more precise, less redundant, and easier for future agents to execute consistently.

Running the scripts calls the TypeScript [`evolve-skill`](../src/evolve-skill/README.md) pipeline, which is different from a direct single skill run: it uses fresh runner agents to produce artifacts on fixed tasks, an evaluator agent to judge those artifacts against the metaskill, and a modifier agent to revise the skill itself. Repeating that loop usually improves the next direct output from the skill.

## Directory Layout

Each skill can have a matching folder under `metaskills`:

```text
metaskills/
  academic-army-architect/
    METASKILL.md
    ENVOLVETASK.md
    envolve.sh
```

[`METASKILL.md`](academic-army-architect/METASKILL.md) records the skill's design goals and tips.

[`ENVOLVETASK.md`](academic-army-architect/ENVOLVETASK.md) is the fixed task used to test the skill during evolution.

[`envolve.sh`](academic-army-architect/envolve.sh) runs the evolution loop for that skill. The file name is kept as `envolve.sh` to match the current project convention.

The shared runner is the `evolve-skill` pipeline, not part of each individual skill's metaskill folder. See [`src/evolve-skill/README.md`](../src/evolve-skill/README.md) for the TypeScript implementation.

In this structure, [`METASKILL.md`](academic-army-architect/METASKILL.md) and [`ENVOLVETASK.md`](academic-army-architect/ENVOLVETASK.md) provide the required inputs to the `evolve-skill` pipeline. The local [`envolve.sh`](academic-army-architect/envolve.sh) file is only a convenience command that fills in those paths for one specific skill, including the artifact output folder.

## Language Contract

When a metaskill designs or revises a planning skill, keep the artifact-language contract fixed: the AI-facing plan is English, and the human-facing explanation is Chinese. For the current planning skills this means `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` stay English-only, while `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md` use Chinese explanations with English technical identifiers preserved when useful.

## Add A New Metaskill

Create a folder under `metaskills` with:

```text
METASKILL.md
ENVOLVETASK.md
envolve.sh
```

Write the fixed evolution task as a representative task. It should be stable enough that different skill versions can be compared across rounds.

Copy an existing [`envolve.sh`](academic-army-architect/envolve.sh) and update the paths.

## Troubleshooting

| Problem                                     | Likely cause                                             | Fix                                                                       |
| ------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- |
| The skill output is still not stable enough | The metaskill guidance is still too vague or incomplete. | Add concrete tips about the failure mode and repeat the evolution script. |
| Different versions are hard to compare      | The fixed evolution task is not stable enough.           | Rewrite `ENVOLVETASK.md` as a representative fixed task.                  |
| The script fails before the loop starts     | Dependencies or pipeline config are missing.             | Run `npm install` and check the TypeScript entry points and config paths. |
