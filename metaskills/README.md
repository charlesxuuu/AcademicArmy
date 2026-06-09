# Metaskills

`metaskills` stores the design notes and self-evolve workflow used to build and improve AcademicArmy skills.

The core design idea is skill self-evolve: use one evaluator agent to judge the output produced by a skill, pass that evaluation to a modifier agent, let the modifier revise the skill, and repeat the loop until the skill becomes better through concrete output, critique, and revision.

A normal skill describes how an agent should complete a research-planning task. A metaskill describes how that skill itself should be designed: its goals, writing style, expected outputs, and the issues to watch for when revising it. During self-evolve, the evaluator uses the metaskill as the standard for judging the artifact, and the modifier uses it as the standard for revising the skill.

## How AcademicArmy Skills Are Built

AcademicArmy skills are developed through an iterative meta-skill workflow rather than written once and treated as final.

We first draft an initial version of the skill. The prompts and notes used for this initial drafting process are kept in the matching [`metaskills`](.) directory, so readers can inspect how the skill itself was produced.

After that, we choose a fixed test topic and repeatedly run the following loop:

1. Execute the skill on the fixed topic.
2. Give the skill output, together with the relevant records from `metaskills`, to an evaluator agent.
3. Ask that agent to analyze the skill carefully: what problems it has, which parts are redundant, and where its language, structure, or content can be improved.
4. Give the resulting revision suggestions to Codex and ask Codex to update the skill.
5. Execute the revised skill again on the same fixed topic.

This loop lets us compare different versions under a stable task setting. The goal is to make each skill more precise, less redundant, and easier for future agents to execute consistently.

## Optimizing An Existing Skill

If a skill's output is unsatisfactory, improve the matching metaskill first instead of editing the skill from vague impressions.

1. Open the corresponding metaskill file; the prepared paths are linked below.
2. Add concrete tips about the failure mode: what the artifact did wrong, what the skill should prefer, and what it should avoid next time.
3. Run the corresponding evolution script from the repository root; the prepared scripts are linked below.
4. Inspect the new artifact and repeat if the skill is still not stable enough.

This is especially useful for the three planning skills used at the start of the AcademicArmy workflow: `academic-army-architect`, `academic-army-experiment-plan`, and `academic-army-coding-plan`. When their direct outputs are not what you want, write the dissatisfaction into the matching metaskill and run several `envolve.sh` rounds. The scripts call the TypeScript [`evolve-skill`](../src/evolve-skill/README.md) pipeline, which is different from a direct single skill run: it uses fresh runner agents to produce artifacts on fixed tasks, an evaluator agent to judge those artifacts against the metaskill, and a modifier agent to revise the skill itself. Repeating that loop usually improves the next direct output from the skill.

Prepared AcademicArmy skill metaskills:

- `academic-army-architect`: edit [`metaskills/academic-army-architect/METASKILL.md`](academic-army-architect/METASKILL.md), then run its script [`metaskills/academic-army-architect/envolve.sh`](academic-army-architect/envolve.sh) with `bash`.
- `academic-army-experiment-plan`: edit [`metaskills/academic-army-experiment-plan/METASKILL.md`](academic-army-experiment-plan/METASKILL.md), then run its script [`metaskills/academic-army-experiment-plan/envolve.sh`](academic-army-experiment-plan/envolve.sh) with `bash`.
- `academic-army-coding-plan`: edit [`metaskills/academic-army-coding-plan/METASKILL.md`](academic-army-coding-plan/METASKILL.md), then run its script [`metaskills/academic-army-coding-plan/envolve.sh`](academic-army-coding-plan/envolve.sh) with `bash`.
- `academic-army-repo-scaffold`: edit [`metaskills/academic-army-repo-scaffold/METASKILL.md`](academic-army-repo-scaffold/METASKILL.md), then run its script [`metaskills/academic-army-repo-scaffold/envolve.sh`](academic-army-repo-scaffold/envolve.sh) with `bash`. This metaskill defines the template-first repository initialization skill: generate a real starter repo from a selected initializer or template, overlay `data/`, `output/`, `results/`, and `harness/`, write repo-local installation instructions, configure installable dependencies without running installation, record reference-only sources, preserve the template's test layout, and keep README text objective and present-state.

The linked evolution scripts call the TypeScript `evolve-skill` pipeline. See [`src/README.md`](../src/README.md) for the TypeScript entry points and [`src/evolve-skill/README.md`](../src/evolve-skill/README.md) for the evolution loop implementation.

## Language Contract

When a metaskill designs or revises a planning skill, keep the artifact-language contract fixed: the AI-facing plan is English, and the human-facing explanation is Chinese. For the current planning skills this means `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` stay English-only, while `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md` use Chinese explanations with English technical identifiers preserved when useful.

## Evolve Runner

The shared runner is the TypeScript `evolve-skill` pipeline. For CLI arguments, loop behavior, and implementation details, see [`src/evolve-skill/README.md`](../src/evolve-skill/README.md).

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

## Prepared Commands

Install dependencies once:

```bash
npm install
```

Run a prepared skill evolution script from the repository root:

```bash
bash metaskills/academic-army-architect/envolve.sh
```

The prepared script calls the `evolve-skill` pipeline with that skill's paths. See [`src/evolve-skill/README.md`](../src/evolve-skill/README.md) for what the script runs and how the loop behaves.

## Adding A New Metaskill

Create a folder under `metaskills` with:

```text
METASKILL.md
ENVOLVETASK.md
envolve.sh
```

Write the metaskill design document for the target skill. It should describe what the skill is trying to produce, what good output looks like, what common failure modes matter, and what should stay out of the skill.

Write the fixed evolution task as a representative task. It should be stable enough that different skill versions can be compared across rounds.

Copy an existing [`envolve.sh`](academic-army-architect/envolve.sh) and update the paths.
