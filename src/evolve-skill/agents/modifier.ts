import { Agent } from "coding-agent-forge/agent";

export type SkillModifierVariables = {
  skillPath: string;
  metaskill: string;
  review: string;
};

export class SkillModifierAgent extends Agent<SkillModifierVariables> {
  protected buildPrompt(variables: Readonly<SkillModifierVariables>): string {
    return `
Revise the skill at ${variables.skillPath} using the feedback below. The feedback is based on an artifact produced by this skill.

The metaskill below contains the design goals and tips of this skill:

${variables.metaskill}

Consider these design goals and tips when revising.

Feedback:

${variables.review}
`;
  }
}
