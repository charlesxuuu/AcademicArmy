import { Agent } from "coding-agent-forge/agent";

export type SkillRunnerVariables = {
  skillPath: string;
  artifactPath: string;
  runnerTask: string;
};

export class SkillRunnerAgent extends Agent<SkillRunnerVariables> {
  protected buildPrompt(variables: Readonly<SkillRunnerVariables>): string {
    return `
Use the skill at ${variables.skillPath} to help me complete the following task, and output the related files to the ${variables.artifactPath} folder.

${variables.runnerTask}
`;
  }
}
