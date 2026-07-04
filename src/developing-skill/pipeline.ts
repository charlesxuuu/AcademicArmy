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
  "coding-style-skill-path": {
    type: "string",
    description: "Coding-style skill directory or file revised by the optimizer",
  },
  "metaskill-path": {
    type: "string",
    description: "Metaskill design document path or HTTP(S) URL used by the trajectory optimizer",
  },
  ...developingArgsOptions,
} as const satisfies PipelineArgsOptions;

export type DevelopingSkillOptions = PipelineOptions<typeof developingSkillArgsOptions>;

export async function developingSkill(
  team: AgentTeam<DevelopingSkillAgentVariables>,
  options: DevelopingSkillOptions,
): Promise<void> {
  const codingStyleSkillPath = options["coding-style-skill-path"];
  const metaskillPath = options["metaskill-path"];
  if (codingStyleSkillPath === undefined || metaskillPath === undefined) {
    throw new Error("--coding-style-skill-path and --metaskill-path are required");
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
            codingStyleSkillPath,
            taskBrief,
            taskRoundSummary: taskResult.taskRoundSummary,
            metaskill,
          },
          logRecord,
        )
      ).trim();

      console.log(`\n# Skill trajectory optimizer report\n${optimizerReport}\n`);
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
  description: "Run the code development loop and evolve its skill.",
  argsOptions: developingSkillArgsOptions,
  agentFactories,
  async run(team: AgentTeam<DevelopingSkillAgentVariables>, options: DevelopingSkillOptions) {
    await developingSkill(team, options);
  },
});
