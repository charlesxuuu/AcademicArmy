import {
  AgentTeam,
  definePipeline,
  type PipelineArgsOptions,
  type PipelineOptions,
  type RecordCallback,
} from "coding-agent-forge";
import {
  developingArgsOptions,
  developingPipeline,
  type ProjectDevLoopAgentVariablesByName,
  type ProjectDevLoopCallbacks,
} from "developing-agent-forge";
import { readMetaskill } from "../metaskill.js";
import { agentFactories } from "./agents/index.js";
import type { TrajectoryOptimizerVariables } from "./agents/index.js";

export type DevelopingSkillAgentVariables = ProjectDevLoopAgentVariablesByName & {
  "trajectory-optimizer": TrajectoryOptimizerVariables;
};

export const developingSkillArgsOptions = {
  "metaskill-path": {
    type: "string",
    description: "Coding-style guidance path or HTTP(S) URL used by the memory injector",
  },
  ...developingArgsOptions,
} as const satisfies PipelineArgsOptions;

export type DevelopingSkillOptions = PipelineOptions<typeof developingSkillArgsOptions>;

export async function developingSkill(
  team: AgentTeam<DevelopingSkillAgentVariables>,
  options: DevelopingSkillOptions,
): Promise<void> {
  const metaskillPath = options["metaskill-path"];
  const projectProgressMemoryPath = options["project-progress-memory-path"];
  const codeDesignMemoryPath = options["code-design-memory-path"];
  if (
    metaskillPath === undefined ||
    projectProgressMemoryPath === undefined ||
    codeDesignMemoryPath === undefined
  ) {
    throw new Error(
      "--metaskill-path, --project-progress-memory-path and --code-design-memory-path are required",
    );
  }
  const metaskill = await readMetaskill(metaskillPath);

  const logRecord: RecordCallback = (thread, record) => {
    console.log(thread.recordToPrettyString(record));
  };

  const callbacks = {
    onTaskFinish: async (agentVariables, taskBrief, taskResult) => {
      const trajectoryOptimizer = await team.createAgent("trajectory-optimizer");
      const optimizerReport = (
        await trajectoryOptimizer.runStreamed(
          {
            ...agentVariables,
            projectProgressMemoryPath,
            codeDesignMemoryPath,
            taskBrief,
            taskRoundSummary: taskResult.taskRoundSummary,
            metaskill,
          },
          logRecord,
        )
      ).trim();

      console.log(`\n# Trajectory memory optimizer report\n${optimizerReport}\n`);
    },
  } as const satisfies ProjectDevLoopCallbacks;

  const developingOptions = {
    ...options,
    callbacks,
  };
  await developingPipeline.run(team, developingOptions);
}

export const developingSkillPipeline = definePipeline({
  name: "developing-skill",
  description: "Run the development loop and directly optimize its development memories.",
  argsOptions: developingSkillArgsOptions,
  agentFactories,
  async run(team: AgentTeam<DevelopingSkillAgentVariables>, options: DevelopingSkillOptions) {
    await developingSkill(team, options);
  },
});
