import { Agent } from "coding-agent-forge/agent";

import { quoteBlock } from "./prompts.js";

export type SkillEvaluatorVariables = {
  artifactPath: string;
  metaskill: string;
  taskDescriptions: string;
};

export class SkillEvaluatorAgent extends Agent<SkillEvaluatorVariables> {
  protected buildPrompt(variables: Readonly<SkillEvaluatorVariables>): string {
    return `
Evaluate the artifact produced by this skill.

Artifact path: ${variables.artifactPath}

Task descriptions:
${quoteBlock(variables.taskDescriptions)}

Metaskill (design goals and tips for this skill):
${quoteBlock(variables.metaskill)}

Review the artifact against the metaskill.

Useful angles include:
- problems in content or language
- missing or misleading guidance
- redundant parts
- other relevant issues...

Return a concise report that explains how this skill can be optimized.
`;
  }
}
