import { Agent } from "coding-agent-forge/agent";

import { quoteBlock } from "./prompts.js";

export type SkillModifierVariables = {
  skillPath: string;
  metaskill: string;
  review: string;
};

export class SkillModifierAgent extends Agent<SkillModifierVariables> {
  protected buildPrompt(variables: Readonly<SkillModifierVariables>): string {
    return `
Revise the skill using the evaluation feedback.

Skill path: ${variables.skillPath}

Metaskill (design goals and tips for this skill):
${quoteBlock(variables.metaskill)}

Consider these design goals and tips when revising.

Evaluation feedback:
${quoteBlock(variables.review)}

Edit the skill directly.
`;
  }
}
