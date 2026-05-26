import { Codex } from "@openai/codex-sdk";
import { mkdir, rm, stat } from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";

const TASK_PROMPT = `
Use the skill on a small but representative research-planning task.

Task:
Design a concise paper blueprint for a systems or AI research idea. The output
should make the core claim, paper goals, evidence strategy, and downstream
planning needs clear enough for later AcademicArmy skills to continue from it.
`;

const RUNNER_PROMPT = (
  skillName: string,
  task: string,
  artifactPath: string,
  skillPath: string,
) => `
Use $${skillName} to complete the task below.

Task:
${task}

Write the final artifact to:
${artifactPath}

Do not edit ${skillPath} or any other skill file.
`;

const EVALUATOR_PROMPT = (
  artifactPath: string,
  task: string,
  skillPath: string,
) => `
Evaluate the artifact at ${artifactPath}.

Task:
${task}

Rubric:
- Correctness and completeness.
- Output quality.
- Whether the current skill instructions caused avoidable mistakes.
- Whether the artifact exposes ambiguous, missing, or over-defensive behavior.

Do not modify files.

First line must be exactly one of:
APPROVED score=<0-10>
CHANGES_REQUIRED score=<0-10>

Then give concise evidence and concrete changes needed in ${skillPath}.
`;

const MODIFIER_PROMPT = (skillPath: string, review: string) => `
Update only ${skillPath} to address this review.

Rules:
- Make the smallest useful change.
- Do not rewrite the whole skill.
- Do not add helper functions unless the logic is reused at least twice.
- Do not add generic wrappers, catch-all fallbacks, silent defaults, or "best effort" branches.
- Prefer fail-fast, explicit errors over swallowed failures.
- Keep the skill focused on the task's public inputs and outputs.
- Inaction is acceptable if the review does not identify a concrete defect; explain why instead of editing.

Review:
${review}
`;

const { values } = parseArgs({
  options: {
    "skill-path": { type: "string" },
    "artifact-path": { type: "string" },
    rounds: { type: "string" },
  },
});

const repo = process.cwd();
const rawSkillPath = values["skill-path"];
const rawArtifactPath = values["artifact-path"];
const rounds = Number(values.rounds);

if (!rawSkillPath || !rawArtifactPath || !values.rounds) {
  throw new Error(
    "Usage: npm run evolve-skill -- --skill-path <path> --artifact-path <path> --rounds <positive-integer>",
  );
}

if (!Number.isInteger(rounds) || rounds < 1) {
  throw new Error("ROUNDS must be a positive integer.");
}

const skillPath = rawSkillPath;
const artifactPath = rawArtifactPath;
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
  for (let round = 1; round <= rounds; round++) {
    await rm(artifactPath, { recursive: true, force: true });
    await mkdir(path.dirname(artifactPath), { recursive: true });

    const runner = codex.startThread({
      ...commonThreadOptions,
      sandboxMode: "workspace-write",
    });

    await runner.run(
      RUNNER_PROMPT(skillName, TASK_PROMPT, artifactPath, skillPath),
    );

    await stat(artifactPath);

    const review = (
      await evaluator.run(
        EVALUATOR_PROMPT(artifactPath, TASK_PROMPT, skillPath),
      )
    ).finalResponse.trim();

    console.log(`\n# Review ${round}\n${review}\n`);

    if (review.startsWith("APPROVED")) {
      break;
    }

    const edit = await modifier.run(MODIFIER_PROMPT(skillPath, review));

    console.log(`# Edit ${round}\n${edit.finalResponse}\n`);
  }
}

void main();
