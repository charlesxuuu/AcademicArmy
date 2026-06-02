# AcademicArmy

AcademicArmy is a multi-agent system for producing research papers. Its core idea is to separate ideation, blueprinting, writing, coding, testing, optimization, visualization, and review into specialized roles that work from a shared paper blueprint.

## How To Use

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Give the idea to `ProductManager`. ProductManager understands the AcademicArmy workflow and helps organize the idea into a paper blueprint, also called the construction plan. Because an early idea is usually underspecified, ProductManager should interact with you over multiple rounds to converge the blueprint toward what you actually want.

Once you are satisfied with the paper blueprint, the formal AcademicArmy workflow begins. The blueprint becomes the project starting point for writing the paper, implementing experiments, running tests, optimizing code, drawing illustrations, plotting results, and reviewing the manuscript.

## Guiding Principle

The central principle of AcademicArmy is: build according to the blueprint.

The blueprint produced by ProductManager should be specific enough for each role to start working without needing to redesign the project. AcademicArmy then follows that standardized plan to complete the paper and its supporting artifacts.

## Planning Artifact Language

Planning skills use a fixed language split. AI-facing artifacts such as `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` are written in English and contain only the plan or specification. Their companion explanation files, such as `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md`, are written in Chinese so the user can review the reasoning, trade-offs, and confirmation state. Technical terms, paper titles, venue names, datasets, benchmarks, methods, paths, commands, and code identifiers may remain in English when that is clearer.

## Design Tips

Parts that require fine-grained research should mainly be handled by skills that know how to call Deep Research through APIs. This avoids saving large amounts of local data only for retrieval, keeping the project lighter and making research updates easier to refresh.

## How We Build Skills

AcademicArmy skills are developed through an iterative meta-skill workflow rather than written once and treated as final.

We first draft an initial version of the skill. The prompts and notes used for this initial drafting process are kept in the `metaskills` directory, so readers can inspect how the skill itself was produced.

After that, we choose a fixed test topic and repeatedly run the following loop:

1. Execute the skill on the fixed topic.
2. Give the skill output, together with the relevant records from `metaskills`, to another agent.
3. Ask that agent to analyze the skill carefully: what problems does it have, which parts are redundant, and where can its language, structure, or content be improved?
4. Give the resulting revision suggestions to Codex and ask Codex to update the skill.
5. Execute the revised skill again on the same fixed topic.

This loop lets us compare different versions under a stable task setting. The goal is to make each skill more precise, less redundant, and easier for future agents to execute consistently.

## DeepResearch MCP

AcademicArmy includes a local stdio MCP implementation in the `mcp-server` directory. It exposes one tool:

- `deepresearch(prompt: str)`: runs the prompt with OpenAI Responses using `gpt-5.5-pro`, high reasoning, web search, background mode, and source inclusion.

Create `.env` in the repository root:

```env
OPENAI_API_KEY=your_api_key_here
```

Install MCP server dependencies if needed:

```powershell
cd <repo>
python -m pip install -r ./mcp-server/requirements.txt
```

The project pipelines use the `academic_army_mcp_tools` server through `agent-forge.yaml`. That config launches the server as `python -m mcp-server` with `PYTHONPATH=.` and `cwd=.` from the repository root, so the evolve/developing runners do not need a separate Codex MCP installation step.

When running AcademicArmy skills directly in Codex, install the same MCP server into Codex so the skill can call `academic_army_mcp_tools.deepresearch` outside the project pipeline:

```powershell
python install_mcp.py
```

The installer refreshes the Codex `academic_army_mcp_tools` entry, registers the current Python executable with `-m mcp-server`, sets the repository root as the MCP working directory, reads `.env`, and forwards those values to the MCP server.

To override or add environment variables directly, repeat `-e/--env NAME=VALUE`:

```powershell
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

Agents should call the `deepresearch` tool with a single self-contained prompt. For example:

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## Project Structure

See `AcademicArmy/README.md` for the agent and team structure.
