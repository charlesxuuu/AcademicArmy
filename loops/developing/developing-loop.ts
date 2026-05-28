import { Codex, type Thread } from "@openai/codex-sdk";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";

const START_PROMPT = (
  codingPlanPath: string,
  codeOverviewPath: string,
  extraPrompt: string,
) => `
Read the coding plan at ${codingPlanPath} and the code overview at ${codeOverviewPath}.
Implement one core unfinished feature from the coding plan.

Update the code overview concisely.
Besides modifying or adding descriptions of implemented behavior, explain how the implemented feature can support future features.
Future plans may not predict the simplest and clearest code design, so revise unreasonable future-feature notes when needed.

${extraPrompt}

At the end, if there are no more features from the coding plan left to implement, your final response must be exactly:
Finished

Otherwise, briefly state what is now implemented and what should be implemented next.
`;

const CONTINUE_PROMPT = (
  codingPlanPath: string,
  codeOverviewPath: string,
  previousResponse: string,
  extraPrompt: string,
) => `
Read the coding plan at ${codingPlanPath}, the code overview at ${codeOverviewPath}, the current codebase, and the previous response below.

${previousResponse}

Treat the previous response as the handoff from the last round. It may contain completed work, remaining work, implementation notes, caveats, and suggested next steps.
Reconcile that handoff with the current code, the coding plan, and the code overview. Then choose and implement one important unfinished feature from the coding plan.
Do not redo work that is already implemented unless it is necessary to fix or complete it.

Update the code overview concisely. Besides modifying or adding descriptions of implemented behavior, explain how the implemented feature can support future features. Future plans may not predict the simplest and clearest code design, so revise unreasonable future-feature notes when needed.

${extraPrompt}

At the end, if there are no more features from the coding plan left to implement, your final response must be exactly:
Finished

Otherwise, briefly state what is now implemented and what should be implemented next.
`;

const { values } = parseArgs({
  options: {
    "codebase-path": { type: "string" },
    "coding-plan-path": { type: "string" },
    "code-overview-path": { type: "string" },
    "response-path": { type: "string" },
    "response-archive-path": { type: "string" },
    "extra-prompt-path": { type: "string" },
    "max-rounds": { type: "string" },
  },
});

const repo = process.cwd();
const rawCodebasePath = values["codebase-path"];
const rawCodingPlanPath = values["coding-plan-path"];
const rawCodeOverviewPath = values["code-overview-path"];
const rawResponsePath = values["response-path"];
const rawResponseArchivePath = values["response-archive-path"];
const rawExtraPromptPath = values["extra-prompt-path"];
const maxRounds = values["max-rounds"] ? Number(values["max-rounds"]) : 10;

if (
  !rawCodebasePath ||
  !rawCodingPlanPath ||
  !rawCodeOverviewPath ||
  !rawResponsePath ||
  !rawResponseArchivePath
) {
  throw new Error(
    "Usage: npm run developing-loop -- --codebase-path <path> --coding-plan-path <path> --code-overview-path <path> --response-path <path> --response-archive-path <folder> [--extra-prompt-path <path>] [--max-rounds <positive-integer>]",
  );
}

if (!Number.isInteger(maxRounds) || maxRounds < 1) {
  throw new Error("MAX_ROUNDS must be a positive integer.");
}

const codebasePath = path.resolve(repo, rawCodebasePath);
const codingPlanPath = path.resolve(repo, rawCodingPlanPath);
const codeOverviewPath = path.resolve(repo, rawCodeOverviewPath);
const responsePath = path.resolve(repo, rawResponsePath);
const responseArchivePath = path.resolve(repo, rawResponseArchivePath);
const extraPromptPath = rawExtraPromptPath
  ? path.resolve(repo, rawExtraPromptPath)
  : undefined;
const relativeCodingPlanPath = path.relative(codebasePath, codingPlanPath);
const relativeCodeOverviewPath = path.relative(codebasePath, codeOverviewPath);
const codex = new Codex();

async function readOptionalText(filePath: string) {
  try {
    return await readFile(filePath, "utf8");
  } catch (error) {
    if (
      typeof error === "object" &&
      error !== null &&
      "code" in error &&
      error.code === "ENOENT"
    ) {
      return "";
    }

    throw error;
  }
}

async function ensureCodeOverview(filePath: string) {
  try {
    await readFile(filePath, "utf8");
  } catch (error) {
    if (
      typeof error === "object" &&
      error !== null &&
      "code" in error &&
      error.code === "ENOENT"
    ) {
      await mkdir(path.dirname(filePath), { recursive: true });
      await writeFile(filePath, "# Code Overview\n", "utf8");
      return;
    }

    throw error;
  }
}

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


async function saveResponseArchive(response: string) {
  await mkdir(responseArchivePath, { recursive: true });

  const archiveFile = path.join(
    responseArchivePath,
    `${(new Date()).toISOString().replace(/[:.]/g, "-")}.md`,
  );

  await writeFile(archiveFile, `${response}\n`, "utf8");
  return archiveFile;
}

async function main() {
  await mkdir(codebasePath, { recursive: true });
  await ensureCodeOverview(codeOverviewPath);
  const extraPrompt = extraPromptPath
    ? await readFile(extraPromptPath, "utf8")
    : "";

  for (let round = 1; round <= maxRounds; round++) {
    const previousResponse = (await readOptionalText(responsePath)).trim();
    const prompt = previousResponse
      ? CONTINUE_PROMPT(
        relativeCodingPlanPath,
        relativeCodeOverviewPath,
        previousResponse,
        extraPrompt,
      )
      : START_PROMPT(
        relativeCodingPlanPath,
        relativeCodeOverviewPath,
        extraPrompt,
      );

    console.log(`\n# Developing round ${round}\n`);

    const agent = codex.startThread({
      workingDirectory: codebasePath,
      approvalPolicy: "never",
      sandboxMode: "danger-full-access",
    });

    const response = (await runAndPrint(agent, prompt)).trim();

    if (response === "Finished") {
      console.log("\n# Finished\n");
      return;
    }

    await mkdir(path.dirname(responsePath), { recursive: true });
    await writeFile(responsePath, `${response}\n`, "utf8");

    console.log(`\n# Saved response ${round} to ${responsePath}\n`);

    const archiveFile = await saveResponseArchive(response);

    console.log(`\n# Archived response ${round} to ${archiveFile}\n`);
  }

  throw new Error(
    `Reached --max-rounds ${maxRounds} before the agent returned Finished.`,
  );
}

void main();
