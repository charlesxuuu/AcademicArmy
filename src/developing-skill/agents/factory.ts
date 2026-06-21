import type { AgentFactoryMap } from "coding-agent-forge";
import { developingPipeline } from "developing-agent-forge";

import { TrajectoryOptimizerAgent } from "./trajectory-optimizer.js";

export const agentFactories: AgentFactoryMap = {
  ...developingPipeline.agentFactories,
  "trajectory-optimizer": (thread, constants) => new TrajectoryOptimizerAgent(thread, constants),
};
