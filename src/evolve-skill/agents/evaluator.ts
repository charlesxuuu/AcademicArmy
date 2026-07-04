import { Agent } from "coding-agent-forge/agent";

export type SkillEvaluatorVariables = {
  artifactPath: string;
  metaskill: string;
  taskDescriptions: string;
};

export class SkillEvaluatorAgent extends Agent<SkillEvaluatorVariables> {
  protected buildPrompt(variables: Readonly<SkillEvaluatorVariables>): string {
    return `
Evaluate the artifact at ${variables.artifactPath}. It was produced by a skill.

The artifacts were created based on the following task descriptions:

${variables.taskDescriptions}

The metaskill below contains the design goals and tips of this skill:

${variables.metaskill}

Based on these goals and tips, are there any problems in the artifact produced by this skill? Are there any redundant parts?
Carefully inspect both the language and the content, and use that analysis to explain how this skill can be optimized.
`;
  }
}
