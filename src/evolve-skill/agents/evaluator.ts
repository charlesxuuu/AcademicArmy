import { Agent } from "coding-agent-forge/agent";

export type SkillEvaluatorVariables = {
  artifactPath: string;
  metaskillPath: string;
  extraPrompt: string;
};

export class SkillEvaluatorAgent extends Agent<SkillEvaluatorVariables> {
  protected buildPrompt(variables: Readonly<SkillEvaluatorVariables>): string {
    return `
Evaluate the artifact at ${variables.artifactPath}. This artifact was produced by a skill.
The metaskill at ${variables.metaskillPath} contains the design goals and tips of this skill.
Based on these goals and tips, are there any problems in the artifact produced by this skill? Are there any redundant parts?
Carefully inspect both the language and the content, and use that analysis to explain how this skill can be optimized.

${variables.extraPrompt}
`;
  }
}
