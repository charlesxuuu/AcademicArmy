import { type AgentVariablesByName } from "coding-agent-forge";
import { type PipelineDefinition, runPipelineCli } from "./pipeline.js";
import { developingPipeline } from "./developing/index.js";
import { evolveSkillPipeline } from "./evolve-skill/index.js";

function defineCli<
  VariablesByName extends AgentVariablesByName,
  Options,
>(entry: {
  name: string;
  description: string;
  definition: PipelineDefinition<VariablesByName, Options>;
}) {
  return {
    name: entry.name,
    description: entry.description,
    run: (args: readonly string[]) => runPipelineCli(entry.definition, args),
  };
}

const cliDefinitions = [
  defineCli({
    name: "developing",
    description: "Run the code development loop.",
    definition: developingPipeline,
  }),
  defineCli({
    name: "evolve-skill",
    description: "Run the skill evolution loop.",
    definition: evolveSkillPipeline,
  }),
] as const;

function buildHelp(): string {
  const pipelineList = cliDefinitions
    .map((pipeline) => `  ${pipeline.name.padEnd(16)} ${pipeline.description}`)
    .join("\n");

  return `Usage: npm run cli -- <pipeline> [...args]

Available pipelines:
${pipelineList}`;
}

const [pipelineName, ...pipelineArgs] = process.argv.slice(2);
const pipelineDefinition = cliDefinitions.find(
  (pipeline) => pipeline.name === pipelineName,
);

if (pipelineDefinition === undefined) {
  console.log(buildHelp());
  process.exitCode = 1;
} else {
  await pipelineDefinition.run(pipelineArgs);
}
