import { Agent } from "coding-agent-forge/agent";
import type { DevelopingAgentVariables } from "developing-agent-forge/agents";

import { quoteBlock } from "./prompts.js";

export type TrajectoryOptimizerVariables = DevelopingAgentVariables & {
  codingStyleSkillPath: string;
  taskBrief: string;
  taskRoundSummary: string;
  metaskill: string;
};

export class TrajectoryOptimizerAgent extends Agent<TrajectoryOptimizerVariables> {
  protected buildPrompt(variables: Readonly<TrajectoryOptimizerVariables>): string {
    return `
Evaluate and revise the skill so it produces better development trajectories.

Skill path: ${variables.codingStyleSkillPath}
Project root: ${variables.targetPath}/.

Current goal:
${quoteBlock(variables.goal)}

Task brief:
${quoteBlock(variables.taskBrief)}

Round summary:
${quoteBlock(variables.taskRoundSummary)}

Metaskill (design goals and tips for this skill):
${quoteBlock(variables.metaskill)}

Evaluate whether the skill produced a good modification trajectory, then revise the skill directly.

Focus on:
- missing guidance
- misleading guidance
- redundant guidance
- effects on task selection, coding, or review
`;
  }
}
