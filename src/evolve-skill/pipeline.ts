import {
  AgentTeam,
  definePipeline,
  type PipelineArgsOptions,
  type PipelineOptions,
  type RecordCallback,
} from "coding-agent-forge";
import { mkdir, readFile, rm } from "node:fs/promises";
import { readMetaskill } from "../metaskill.js";
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

export async function evolveSkill(
  team: AgentTeam<EvolveSkillAgentVariables>,
  options: EvolveSkillOptions,
): Promise<void> {
  const logRecord: RecordCallback = (thread, record) => {
    console.log(thread.recordToPrettyString(record));
  };
  const taskDescriptions = (
    await Promise.all(
      options.taskPaths.map(async (taskPath, index) => {
        const task = await readFile(taskPath, "utf8");
        return `Task ${String(index + 1)}: ${task}`;
      }),
    )
  ).join("\n\n");
  const metaskill = await readMetaskill(options.metaskillPath);

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
          metaskill,
          taskDescriptions,
        },
        logRecord,
      )
    ).trim();

    console.log(`\n# Review\n${review}\n`);

    const edit = await team.runStreamed(
      "skill-modifier",
      {
        skillPath: options.skillPath,
        metaskill,
        review,
      },
      logRecord,
    );

    console.log(`# Edit\n${edit}\n`);
  }
}

export const evolveSkillArgsOptions = {
  "skill-path": {
    type: "string",
    description: "Skill directory or file to revise",
  },
  "artifact-path": {
    type: "string",
    description: "Output folder cleared and reused by each runner round",
  },
  "metaskill-path": {
    type: "string",
    description: "Metaskill design document path or HTTP(S) URL used by the evaluator and modifier",
  },
  "task-path": {
    type: "string",
    multiple: true,
    description: "Fixed task used by the runner to test the skill",
  },
  rounds: {
    type: "string",
    default: "3",
    description: "Number of self-evolve rounds to run",
  },
} as const satisfies PipelineArgsOptions;

export const evolveSkillPipeline = definePipeline({
  name: "evolve-skill",
  description: "Run the skill evolution loop.",
  argsOptions: evolveSkillArgsOptions,
  agentFactories,
  async run(
    team: AgentTeam<EvolveSkillAgentVariables>,
    options: PipelineOptions<typeof evolveSkillArgsOptions>,
  ) {
    const {
      "skill-path": skillPath,
      "artifact-path": artifactPath,
      "metaskill-path": metaskillPath,
      "task-path": taskPaths,
      rounds,
    } = options;
    if (
      skillPath === undefined ||
      artifactPath === undefined ||
      metaskillPath === undefined ||
      taskPaths === undefined
    ) {
      throw new Error(
        "--skill-path, --artifact-path, --metaskill-path and --task-path are required",
      );
    }

    await evolveSkill(team, {
      skillPath,
      artifactPath,
      metaskillPath,
      taskPaths,
      rounds: Number(rounds),
    });
  },
});
