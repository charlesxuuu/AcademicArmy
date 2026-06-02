import {
  AgentTeam,
  loadYamls,
  type AgentVariablesByName,
  type PlainObject,
} from "coding-agent-forge";

export type ParsedPipelineArgs<Options> = {
  configPaths: readonly string[];
  runningOptions: Options;
};

export type PipelineDefinition<
  VariablesByName extends AgentVariablesByName,
  Options,
> = {
  parseArgs: (args: readonly string[]) => ParsedPipelineArgs<Options>;
  buildAgentTeam: (rawConfig: PlainObject) => AgentTeam<VariablesByName>;
  run: (team: AgentTeam<VariablesByName>, options: Options) => Promise<void>;
};

export function definePipeline<
  VariablesByName extends AgentVariablesByName,
  Options,
>(
  definition: PipelineDefinition<VariablesByName, Options>,
): PipelineDefinition<VariablesByName, Options> {
  return definition;
}

export async function runPipelineCli<
  VariablesByName extends AgentVariablesByName,
  Options,
>(
  definition: PipelineDefinition<VariablesByName, Options>,
  args: readonly string[],
): Promise<void> {
  const { configPaths, runningOptions } = definition.parseArgs(args);
  const rawConfig = await loadYamls(...configPaths);
  const team = definition.buildAgentTeam(rawConfig);

  try {
    await definition.run(team, runningOptions);
  } finally {
    await team.close();
  }
}
