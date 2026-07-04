import { Agent } from "coding-agent-forge/agent";
import { readFileSync } from "node:fs";

import { quoteBlock } from "./prompts.js";

export type SkillRunnerVariables = {
  skillPath: string;
  artifactPath: string;
  taskPath: string;
};

export class SkillRunnerAgent extends Agent<SkillRunnerVariables> {
  protected buildPrompt(variables: Readonly<SkillRunnerVariables>): string {
    const task = readFileSync(variables.taskPath, "utf8");
    return `
Use the skill to complete the task.

Skill path: ${variables.skillPath}
Artifact path: ${variables.artifactPath}

Task:
${quoteBlock(task)}

Save all relevant output files in the artifact path.
`;
  }
}
