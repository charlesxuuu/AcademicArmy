import { type AgentTeam, type RecordCallback } from "coding-agent-forge";
import { mkdir, rm } from "node:fs/promises";

import type {
  SkillEvaluatorVariables,
  SkillModifierVariables,
  SkillRunnerVariables,
} from "./agents/index.js";

export type EvolveSkillAgentVariables = {
  runner: SkillRunnerVariables;
  evaluator: SkillEvaluatorVariables;
  modifier: SkillModifierVariables;
};

export type EvolveSkillOptions = {
  skillPath: string;
  artifactPath: string;
  metaskillPath: string;
  taskPath: string;
  rounds: number;
};

export async function evolveSkill(
  team: AgentTeam<EvolveSkillAgentVariables>,
  options: EvolveSkillOptions,
): Promise<void> {
  const logRecord: RecordCallback = (thread, record) => {
    console.log(thread.recordToPrettyString(record));
  };

  for (let round = 1; round <= options.rounds; round++) {
    await rm(options.artifactPath, { recursive: true, force: true });
    await mkdir(options.artifactPath, { recursive: true });

    const runner = await team.createAgent("runner");
    await runner.runStreamed(
      {
        skillPath: options.skillPath,
        artifactPath: options.artifactPath,
        taskPath: options.taskPath,
      },
      logRecord,
    );

    const review = (
      await team.runStreamed(
        "evaluator",
        {
          artifactPath: options.artifactPath,
          metaskillPath: options.metaskillPath,
        },
        logRecord,
      )
    ).trim();

    console.log(`\n# Review ${round}\n${review}\n`);

    const edit = await team.runStreamed(
      "modifier",
      {
        skillPath: options.skillPath,
        metaskillPath: options.metaskillPath,
        review,
      },
      logRecord,
    );

    console.log(`# Edit ${round}\n${edit}\n`);
  }
}
