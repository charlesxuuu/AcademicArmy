# AcademicArmy

AcademicArmy is a multi-agent system for producing research papers. Its core idea is to separate ideation, blueprinting, writing, coding, testing, optimization, visualization, and review into specialized roles that work from a shared paper blueprint.

## How To Use

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Give the idea to `ProductManager`. ProductManager understands the AcademicArmy workflow and helps organize the idea into a paper blueprint, also called the construction plan. Because an early idea is usually underspecified, ProductManager should interact with you over multiple rounds to converge the blueprint toward what you actually want.

Once you are satisfied with the paper blueprint, the formal AcademicArmy workflow begins. The blueprint becomes the project starting point for writing the paper, implementing experiments, running tests, optimizing code, drawing illustrations, plotting results, and reviewing the manuscript.

## Guiding Principle

The central principle of AcademicArmy is: build according to the blueprint.

The blueprint produced by ProductManager should be specific enough for each role to start working without needing to redesign the project. AcademicArmy then follows that standardized plan to complete the paper and its supporting artifacts.

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

Before registering it, create `.env` in the repository root:

```env
OPENAI_API_KEY=your_api_key_here
```

Install dependencies in the bundled virtual environment if needed:

```powershell
cd <repo>
python -m pip install -r ./mcp-server/requirements.txt
```

Register the MCP server in Codex:

```powershell
python install_mcp.py
```

The installer refreshes the `academic_army_mcp_tools` Codex entry with the Python executable that runs the installer. It also reads `.env` from the repository root and passes those values to the MCP server through Codex `--env`.

To override or add environment variables directly, repeat `-e/--env NAME=VALUE`:

```powershell
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

For another MCP client, register it as a stdio server:

- Name: `academic_army_mcp_tools`
- Command: `python`
- Arguments: `-m mcp-server`
- Working directory: `<repo>`

Make sure the MCP client's working directory is the repository root, because the server loads `.env` from the current directory. You can also pass environment variables directly with `-e/--env NAME=VALUE`; these values are applied after `.env` is loaded, so they override matching values from `.env`.

After registration, restart the MCP client. Then call the `deepresearch` tool with a single self-contained prompt. For example:

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## Project Structure

See `AcademicArmy/README.md` for the agent and team structure.
