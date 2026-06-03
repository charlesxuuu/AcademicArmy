import type { AgentFactoryMap } from "coding-agent-forge";

import { SkillEvaluatorAgent } from "./evaluator.js";
import { SkillModifierAgent } from "./modifier.js";
import { SkillRunnerAgent } from "./runner.js";

export const agentFactories: AgentFactoryMap = {
  "skill-runner": (thread, constants) => new SkillRunnerAgent(thread, constants),
  "skill-evaluator": (thread, constants) => new SkillEvaluatorAgent(thread, constants),
  "skill-modifier": (thread, constants) => new SkillModifierAgent(thread, constants),
};
