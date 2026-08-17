#!/usr/bin/env node
import { runPipelinesCli } from "coding-agent-forge";
import { developingPipeline } from "developing-agent-forge";
import { evolveSkillPipeline } from "./evolve-skill/index.js";

await runPipelinesCli([developingPipeline, evolveSkillPipeline], process.argv.slice(2));
