import { Codex, type Thread } from "@openai/codex-sdk";
import { mkdir, readFile, rm, stat } from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";

const RUNNER_PROMPT = (
  skillName: string,
  artifactPath: string,
  runnerTask: string,
) => `
Use the ${skillName} skill to help me complete the following task, and output the related files to the ${artifactPath} folder.

${runnerTask}
`;

const EVALUATOR_PROMPT = (
  artifactPath: string,
  metaskillPath: string,
  extraPrompt: string,
) => `
Evaluate the artifact at ${artifactPath}. This artifact was produced by a skill.
The metaskill at ${metaskillPath} contains the design goals and tips of this skill.
Based on these goals and tips, are there any problems in the artifact produced by this skill? Are there any redundant parts?
Carefully inspect both the language and the content, and use that analysis to explain how this skill can be optimized.

${extraPrompt}
`;

const MODIFIER_PROMPT = (
  skillPath: string,
  metaskillPath: string,
  review: string,
) => `
Following is feedback on ${skillPath} based on a artifact produced by that skill.
Please revise this skill according to the feedback.
The metaskill at ${metaskillPath} contains the design goals and tips of this skill.
Consider these design goals and tips when revising.

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

async function runAndPrint(thread: Thread, prompt: string) {
  const { events } = await thread.runStreamed(prompt);
  let finalResponse = "";

  for await (const event of events) {
    if (event.type !== "item.completed") {
      continue;
    }

    const item = event.item;

    if (item.type === "agent_message") {
      console.log(item.text);
      finalResponse = item.text;
    }

    if (item.type === "command_execution") {
      console.log(`$ ${item.command}`);
      console.log(item.aggregated_output);
    }
  }

  return finalResponse;
}

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

    await runAndPrint(
      runner,
      RUNNER_PROMPT(skillName, artifactPath, runnerTask),
    );

    await stat(artifactPath);

    const review = (
      await runAndPrint(
        evaluator,
        EVALUATOR_PROMPT(
          artifactPath,
          checkedMetaskillPath,
          evaluatorExtraPrompt,
        ),
      )
    ).trim();

    console.log(`\n# Review ${round}\n${review}\n`);

    const edit = await runAndPrint(
      modifier,
      MODIFIER_PROMPT(skillPath, checkedMetaskillPath, review),
    );

    console.log(`# Edit ${round}\n${edit}\n`);
  }
}

void main();
