import { Agent } from "coding-agent-forge/agent";
import { readFileSync } from "node:fs";

export type SkillModifierVariables = {
  skillPath: string;
  metaskillPath: string;
  review: string;
};

export class SkillModifierAgent extends Agent<SkillModifierVariables> {
  protected buildPrompt(variables: Readonly<SkillModifierVariables>): string {
    const metaskill = readFileSync(variables.metaskillPath, "utf8");
    return `
Following is feedback on ${variables.skillPath} based on a artifact produced by that skill.
Please revise this skill according to the feedback.
The following metaskill contains the design goals and tips of this skill:

${metaskill}

Consider these design goals and tips when revising.

${variables.review}
`;
  }
}
