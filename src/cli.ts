#!/usr/bin/env node
import { runPipelinesCli } from "coding-agent-forge";
import { developingPipeline, developingSkillPipeline } from "developing-agent-forge";
import { evolveSkillPipeline } from "./evolve-skill/index.js";

await runPipelinesCli(
  [developingPipeline, developingSkillPipeline, evolveSkillPipeline],
  process.argv.slice(2),
);
