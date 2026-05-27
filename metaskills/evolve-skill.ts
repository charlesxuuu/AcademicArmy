import { Codex } from "@openai/codex-sdk";
import { mkdir, readFile, rm, stat } from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";

const RUNNER_PROMPT = (
  skillName: string,
  artifactPath: string,
  runnerTask: string,
) => `
Use ${skillName} to complete the task below. Write the final artifact to ${artifactPath}.

${runnerTask}
`;

const EVALUATOR_PROMPT = (
  artifactPath: string,
  metaskillPath: string,
  extraPrompt: string,
) => `
Evaluate the artifact at ${artifactPath}.

The metaskill file at ${metaskillPath} contains important guidance about what to consider when writing and improving this skill.

${extraPrompt}
`;

const MODIFIER_PROMPT = (
  skillPath: string,
  metaskillPath: string,
  review: string,
) => `
Update ${skillPath} to address this review.

The metaskill file at ${metaskillPath} contains important guidance about what to consider when writing and improving this skill.

Review:
${review}
`;

const { values } = parseArgs({
  options: {
    "skill-path": { type: "string" },
    "artifact-path": { type: "string" },
    "metaskill-path": { type: "string" },
    "runner-task-path": { type: "string" },
    "evaluator-extra-prompt-path": { type: "string" },
    rounds: { type: "string" },
  },
});

const repo = process.cwd();
const rawSkillPath = values["skill-path"];
const rawArtifactPath = values["artifact-path"];
const metaskillPath = values["metaskill-path"];
const runnerTaskPath = values["runner-task-path"];
const evaluatorExtraPromptPath = values["evaluator-extra-prompt-path"];
const rounds = Number(values.rounds);

if (
  !rawSkillPath ||
  !rawArtifactPath ||
  !metaskillPath ||
  !runnerTaskPath
) {
  throw new Error(
    "Usage: npm run evolve-skill -- --skill-path <path> --artifact-path <path> --metaskill-path <path> --runner-task-path <path> [--evaluator-extra-prompt-path <path>] [--rounds <positive-integer>]",
  );
}

const checkedRounds = values.rounds ? rounds : 3;

if (!Number.isInteger(checkedRounds) || checkedRounds < 1) {
  throw new Error("ROUNDS must be a positive integer.");
}

const skillPath = rawSkillPath;
const artifactPath = rawArtifactPath;
const checkedMetaskillPath = metaskillPath;
const checkedRunnerTaskPath = runnerTaskPath;
const skillName = path.basename(skillPath);
const codex = new Codex();
const commonThreadOptions = {
  workingDirectory: repo,
  approvalPolicy: "never" as const,
};

const evaluator = codex.startThread({
  ...commonThreadOptions,
  sandboxMode: "read-only",
});

const modifier = codex.startThread({
  ...commonThreadOptions,
  sandboxMode: "workspace-write",
});

async function main() {
  const runnerTask = await readFile(checkedRunnerTaskPath, "utf8");
  const evaluatorExtraPrompt = evaluatorExtraPromptPath
    ? await readFile(evaluatorExtraPromptPath, "utf8")
    : "";

  for (let round = 1; round <= checkedRounds; round++) {
    await rm(artifactPath, { recursive: true, force: true });
    await mkdir(artifactPath, { recursive: true });

    const runner = codex.startThread({
      ...commonThreadOptions,
      sandboxMode: "workspace-write",
    });

    await runner.run(
      RUNNER_PROMPT(skillName, artifactPath, runnerTask),
    );

    await stat(artifactPath);

    const review = (
      await evaluator.run(
        EVALUATOR_PROMPT(
          artifactPath,
          checkedMetaskillPath,
          evaluatorExtraPrompt,
        ),
      )
    ).finalResponse.trim();

    console.log(`\n# Review ${round}\n${review}\n`);

    const edit = await modifier.run(
      MODIFIER_PROMPT(skillPath, checkedMetaskillPath, review),
    );

    console.log(`# Edit ${round}\n${edit.finalResponse}\n`);
  }
}

void main();
