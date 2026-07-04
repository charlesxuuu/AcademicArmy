import { Agent } from "coding-agent-forge/agent";
import type { DevelopingAgentVariables } from "developing-agent-forge/agents";

export type TrajectoryOptimizerVariables = DevelopingAgentVariables & {
  codingStyleSkillPath: string;
  taskBrief: string;
  taskRoundSummary: string;
  metaskill: string;
};

export class TrajectoryOptimizerAgent extends Agent<TrajectoryOptimizerVariables> {
  protected buildPrompt(variables: Readonly<TrajectoryOptimizerVariables>): string {
    return `
Revise the skill at ${variables.codingStyleSkillPath} so it produces better development trajectories.

The metaskill below contains the design goals and tips of this skill:

${variables.metaskill}

The sections below describe the task this skill just executed and what happened during that round.

Target repository at ${variables.targetPath}/.

Goal:
${variables.goal}

Task Brief:
${variables.taskBrief}

Reality-aware task round summary:
${variables.taskRoundSummary}

Evaluate whether the skill produced a good modification trajectory, then edit the skill directly. Focus on missing, misleading, or redundant guidance that affected task selection, coding, or review.

Output a concise optimizer report with the main skill changes.
`;
  }
}
