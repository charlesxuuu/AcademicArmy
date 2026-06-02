# Metaskills

`metaskills` stores the design notes and self-evolve workflow used to build and improve AcademicArmy skills.

The core design idea is skill self-evolve: use one evaluator agent to judge the output produced by a skill, pass that evaluation to a modifier agent, let the modifier revise the skill, and repeat the loop until the skill becomes better through concrete output, critique, and revision.

A normal skill describes how an agent should complete a research-planning task. A metaskill describes how that skill itself should be designed: its goals, writing style, expected outputs, and the issues to watch for when revising it. During self-evolve, the evaluator uses the metaskill as the standard for judging the artifact, and the modifier uses it as the standard for revising the skill.

## Language Contract

When a metaskill designs or revises a planning skill, keep the artifact-language contract fixed: the AI-facing plan is English, and the human-facing explanation is Chinese. For the current planning skills this means `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` stay English-only, while `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md` use Chinese explanations with English technical identifiers preserved when useful.

## Evolve Runner

The `evolve-skill` pipeline is the shared Codex SDK runner for this self-evolve loop.

It keeps two long-lived Codex threads:

1. `evaluator`: reviews artifacts across rounds.
2. `modifier`: edits the target skill across rounds.

Each round also creates a fresh one-time runner thread. The runner has no memory from previous rounds, which keeps each artifact from being contaminated by earlier outputs.

Run it directly from the repository root:

```bash
npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-architect \
  --artifact-path output/evolve-academic-army-architect \
  --metaskill-path metaskills/academic-army-architect/METASKILL.md \
  --task-path metaskills/academic-army-architect/ENVOLVETASK.md
```

Required arguments:

```text
--skill-path       The skill directory or file to revise.
--artifact-path    The output folder cleared and reused by each runner round.
--metaskill-path   The metaskill design document used by evaluator and modifier.
--task-path        The fixed task used by the runner to test the skill.
```

Optional arguments:

```text
--rounds 5
  Number of self-evolve rounds to run.
```

`--rounds` defaults to `3`.

## Directory Layout

Each skill can have a matching folder under `metaskills`:

```text
metaskills/
  academic-army-architect/
    METASKILL.md
    ENVOLVETASK.md
    envolve.sh
```

`METASKILL.md` records the skill's design goals and tips.

`ENVOLVETASK.md` is the fixed task used to test the skill during evolution.

`envolve.sh` runs the evolution loop for that skill. The file name is kept as `envolve.sh` to match the current project convention.

The shared runner is the `evolve-skill` pipeline, not part of each individual skill's metaskill folder.

In this structure, `METASKILL.md` and `ENVOLVETASK.md` provide the required inputs to the `evolve-skill` pipeline. The local `envolve.sh` file is only a convenience command that fills in those paths for one specific skill, including the artifact output folder.

## Loop Behavior

Metaskills keep skill development grounded. Instead of rewriting a skill from vague impressions, the loop tests the skill on a stable task, evaluates the resulting artifact against the metaskill, and then asks Codex to revise the skill based on concrete feedback.

The loop deliberately stays simple:

1. A fresh runner thread runs the target skill and writes artifacts to an output folder.
2. A long-lived evaluator thread reviews the artifact using the metaskill.
3. A long-lived modifier thread edits the skill according to the evaluator feedback.
4. The next round starts with a fresh runner thread, so prior artifacts do not pollute the next run.

This avoids LangGraph, state machines, registries, and defensive wrapper code. The important state lives in the two long-lived evaluator/modifier Codex sessions and in the files being revised.

## Prepared Commands

Install dependencies once:

```bash
npm install
```

Run a prepared skill evolution script from the repository root:

```bash
bash metaskills/academic-army-architect/envolve.sh
```

The prepared script calls the `evolve-skill` pipeline with that skill's paths. The runner clears the artifact output path at the start of each round, so keep the artifact path inside a dedicated output directory.

## Adding A New Metaskill

Create a folder under `metaskills` with:

```text
METASKILL.md
ENVOLVETASK.md
envolve.sh
```

Write `METASKILL.md` as a design document for the target skill. It should describe what the skill is trying to produce, what good output looks like, what common failure modes matter, and what should stay out of the skill.

Write `ENVOLVETASK.md` as a representative task. It should be stable enough that different skill versions can be compared across rounds.

Copy an existing `envolve.sh` and update the paths.
