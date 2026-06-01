import { Agent } from "coding-agent-forge/agent";

export type SkillModifierVariables = {
  skillPath: string;
  metaskillPath: string;
  review: string;
};

export class SkillModifierAgent extends Agent<SkillModifierVariables> {
  protected buildPrompt(variables: Readonly<SkillModifierVariables>): string {
    return `
Following is feedback on ${variables.skillPath} based on a artifact produced by that skill.
Please revise this skill according to the feedback.
The metaskill at ${variables.metaskillPath} contains the design goals and tips of this skill.
Consider these design goals and tips when revising.

${variables.review}
`;
  }
}
