# AcademicArmy

AcademicArmy is a multi-agent system for producing research papers. Its core idea is to separate ideation, blueprinting, writing, coding, testing, optimization, visualization, and review into specialized roles that work from a shared paper blueprint.

## How To Use

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Give the idea to `ProductManager`. ProductManager understands the AcademicArmy workflow and helps organize the idea into a paper blueprint, also called the construction plan. Because an early idea is usually underspecified, ProductManager should interact with you over multiple rounds to converge the blueprint toward what you actually want.

Once you are satisfied with the paper blueprint, the formal AcademicArmy workflow begins. The blueprint becomes the project starting point for writing the paper, implementing experiments, running tests, optimizing code, drawing illustrations, plotting results, and reviewing the manuscript.

## Running Workflow

The current project workflow first uses three planning skills to produce three AI-facing Markdown artifacts:

1. `academic-army-architect` creates `paper_blueprint.md`, the strategic paper blueprint that fixes the paper identity, target venue posture, claims, contribution boundary, candidate method space, evidence needs, and downstream constraints.
2. `academic-army-experiment-plan` creates `experiment_plan.md`, the experiment strategy that maps paper claims to evidence, datasets or workloads, metrics, baselines, ablations, robustness checks, and reviewer-facing validation needs.
3. `academic-army-coding-plan` creates `coding_plan.md`, the implementation contract that turns the blueprint and experiment plan into module boundaries, CLIs, harnesses, tests, raw-result exports, and method-freeze rules.

Each planning skill also writes a Chinese `*.explain.md` companion for human review, but the development runner consumes the three English Markdown files above.

After the three planning artifacts are ready, run:

```bash
bash runs/develop.sh
```

[`runs/develop.sh`](runs/develop.sh) calls the TypeScript `developing` pipeline, which reads the three planning artifacts and iteratively writes code under `output/codebase`. See [`src/README.md`](src/README.md) for the TypeScript entry points and [`src/developing/README.md`](src/developing/README.md) for the development loop implementation.

## Guiding Principle

The central principle of AcademicArmy is: build according to the blueprint.

The blueprint produced by ProductManager should be specific enough for each role to start working without needing to redesign the project. AcademicArmy then follows that standardized plan to complete the paper and its supporting artifacts.

## Planning Artifact Language

Planning skills use a fixed language split. AI-facing artifacts such as `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` are written in English and contain only the plan or specification. Their companion explanation files, such as `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md`, are written in Chinese so the user can review the reasoning, trade-offs, and confirmation state. Technical terms, paper titles, venue names, datasets, benchmarks, methods, paths, commands, and code identifiers may remain in English when that is clearer.

## Design Tips

Parts that require fine-grained research should mainly be handled by skills that know how to call Deep Research through APIs. This avoids saving large amounts of local data only for retrieval, keeping the project lighter and making research updates easier to refresh.

## Skill Development

For the meta-skill workflow used to build and evolve AcademicArmy skills, see [`metaskills/README.md`](metaskills/README.md).

## DeepResearch MCP

AcademicArmy includes a local stdio MCP implementation in the [`mcp-server`](mcp-server) directory. It exposes one tool:

- `deepresearch(prompt: str)`: runs the prompt with OpenAI Responses using `gpt-5.5-pro`, high reasoning, web search, background mode, and source inclusion.

Create `.env` in the repository root:

```env
OPENAI_API_KEY=your_api_key_here
```

Install MCP server dependencies from [`mcp-server/requirements.txt`](mcp-server/requirements.txt) if needed:

```powershell
cd <repo>
python -m pip install -r ./mcp-server/requirements.txt
```

The project pipelines use the `academic_army_mcp_tools` server through [`agent-forge.yaml`](agent-forge.yaml). That config launches the server as `python -m mcp-server` with `PYTHONPATH=.` and `cwd=.` from the repository root, so the evolve/developing runners do not need a separate Codex MCP installation step.

When running AcademicArmy skills directly in Codex, use [`install_mcp.py`](install_mcp.py) to install the same MCP server into Codex so the skill can call `academic_army_mcp_tools.deepresearch` outside the project pipeline:

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

See [`AcademicArmy/README.md`](AcademicArmy/README.md) for the agent and team structure.

See [`src/README.md`](src/README.md) for the TypeScript pipeline structure and implementation notes.
