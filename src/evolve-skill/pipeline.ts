import { AgentTeam, type RecordCallback } from "coding-agent-forge";
import { mkdir, rm } from "node:fs/promises";
import { parseArgs } from "node:util";
import { definePipeline } from "../pipeline.js";
import type { ParsedPipelineArgs } from "../pipeline.js";
import { agentFactories } from "./agents/index.js";
import type {
  SkillEvaluatorVariables,
  SkillModifierVariables,
  SkillRunnerVariables,
} from "./agents/index.js";

export type EvolveSkillAgentVariables = {
  "skill-runner": SkillRunnerVariables;
  "skill-evaluator": SkillEvaluatorVariables;
  "skill-modifier": SkillModifierVariables;
};

export type EvolveSkillOptions = {
  skillPath: string;
  artifactPath: string;
  metaskillPath: string;
  taskPaths: readonly string[];
  rounds: number;
};

const USAGE =
  "Usage: npm run evolve-skill -- --config <path> --skill-path <path> --artifact-path <folder> --metaskill-path <path> --task-path <path> [--task-path <path> ...] [--rounds <positive-integer>]";

export function parseEvolveSkillArgs(
  args: readonly string[],
): ParsedPipelineArgs<EvolveSkillOptions> {
  const {
    values: {
      config,
      "skill-path": skillPath,
      "artifact-path": artifactPath,
      "metaskill-path": metaskillPath,
      "task-path": taskPath,
      rounds,
    },
  } = parseArgs({
    args: [...args],
    options: {
      config: { type: "string", multiple: true },
      "skill-path": { type: "string" },
      "artifact-path": { type: "string" },
      "metaskill-path": { type: "string" },
      "task-path": { type: "string", multiple: true },
      rounds: { type: "string" },
    },
  });

  if (
    config === undefined ||
    skillPath === undefined ||
    artifactPath === undefined ||
    metaskillPath === undefined ||
    taskPath === undefined
  ) {
    throw new Error(USAGE);
  }

  return {
    configPaths: config,
    runningOptions: {
      skillPath,
      artifactPath,
      metaskillPath,
      taskPaths: taskPath,
      rounds: Number(rounds ?? 3),
    },
  };
}

export async function evolveSkill(
  team: AgentTeam<EvolveSkillAgentVariables>,
  options: EvolveSkillOptions,
): Promise<void> {
  const logRecord: RecordCallback = (thread, record) => {
    console.log(thread.recordToPrettyString(record));
  };

  for (let round = 1; round <= options.rounds; round++) {
    await rm(options.artifactPath, { recursive: true, force: true });
    await mkdir(options.artifactPath, { recursive: true });

    for (const taskPath of options.taskPaths) {
      const runner = await team.createAgent("skill-runner");
      await runner.runStreamed(
        {
          skillPath: options.skillPath,
          artifactPath: options.artifactPath,
          taskPath,
        },
        logRecord,
      );
    }

    const review = (
      await team.runStreamed(
        "skill-evaluator",
        {
          artifactPath: options.artifactPath,
          metaskillPath: options.metaskillPath,
        },
        logRecord,
      )
    ).trim();

    console.log(`\n# Review\n${review}\n`);

    const edit = await team.runStreamed(
      "skill-modifier",
      {
        skillPath: options.skillPath,
        metaskillPath: options.metaskillPath,
        review,
      },
      logRecord,
    );

    console.log(`# Edit\n${edit}\n`);
  }
}

export const evolveSkillPipeline = definePipeline({
  agentFactories,
  parseArgs: parseEvolveSkillArgs,
  run: evolveSkill,
});
