import {
  AgentTeam,
  isPlainObject,
  loadYamls,
  mergeConfig,
  type AgentFactoryMap,
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
  agentFactories: AgentFactoryMap;
  parseArgs: (args: readonly string[]) => ParsedPipelineArgs<Options>;
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

function buildPipelineAgentTeam<
  VariablesByName extends AgentVariablesByName,
  Options,
>(
  rawConfig: PlainObject,
  definition: PipelineDefinition<VariablesByName, Options>,
): AgentTeam<VariablesByName> {
  if (!isPlainObject(rawConfig.agents)) {
    throw new Error("Config must define an agents object");
  }

  for (const name of Object.keys(rawConfig.agents)) {
    if (!Object.hasOwn(definition.agentFactories, name)) {
      delete rawConfig.agents[name];
    }
  }

  const agents = Object.fromEntries(
    Object.keys(definition.agentFactories).map((name) => [
      name,
      { kind: name },
    ]),
  );

  return new AgentTeam<VariablesByName>(
    mergeConfig(rawConfig, { agents }),
    definition.agentFactories,
  );
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
  const team = buildPipelineAgentTeam(rawConfig, definition);

  try {
    await definition.run(team, runningOptions);
  } finally {
    await team.close();
  }
}
