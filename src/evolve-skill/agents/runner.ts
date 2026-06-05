import { Agent } from "coding-agent-forge/agent";
import { readFileSync } from "node:fs";

export type SkillRunnerVariables = {
  skillPath: string;
  artifactPath: string;
  taskPath: string;
};

export class SkillRunnerAgent extends Agent<SkillRunnerVariables> {
  protected buildPrompt(variables: Readonly<SkillRunnerVariables>): string {
    const task = readFileSync(variables.taskPath, "utf8");
    return `
Use the skill at ${variables.skillPath} to complete the task below. Save all relevant output files in ${variables.artifactPath}.

${task}
`;
  }
}
