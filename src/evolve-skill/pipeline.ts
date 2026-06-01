import {
  AgentTeam,
  mergeConfig,
  type PlainObject,
  type RecordCallback,
} from "coding-agent-forge";
import { mkdir, rm } from "node:fs/promises";
import { agentFactories } from "./agents/index.js";
import type {
  SkillEvaluatorVariables,
  SkillModifierVariables,
  SkillRunnerVariables,
} from "./agents/index.js";

export type EvolveSkillAgentVariables = {
  "skill-runner": SkillRunnerVariables;
  "skill-evaluator": SkillEvaluatorVariables;
  "skill-modifier": SkillModifierVariables;
};

export type EvolveSkillOptions = {
  skillPath: string;
  artifactPath: string;
  metaskillPath: string;
  taskPath: string;
  rounds: number;
};

export function buildEvolveSkillAgentTeam(
  rawConfig: PlainObject,
): AgentTeam<EvolveSkillAgentVariables> {
  return new AgentTeam<EvolveSkillAgentVariables>(
    mergeConfig(rawConfig, {
      agents: {
        "skill-runner": {
          kind: "skill-runner",
        },
        "skill-evaluator": {
          kind: "skill-evaluator",
        },
        "skill-modifier": {
          kind: "skill-modifier",
        },
      },
    }),
    agentFactories,
  );
}

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

    const runner = await team.createAgent("skill-runner");
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
        "skill-evaluator",
        {
          artifactPath: options.artifactPath,
          metaskillPath: options.metaskillPath,
        },
        logRecord,
      )
    ).trim();

    console.log(`\n# Review ${round}\n${review}\n`);

    const edit = await team.runStreamed(
      "skill-modifier",
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
