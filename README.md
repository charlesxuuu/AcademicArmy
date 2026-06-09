# AcademicArmy

AcademicArmy is a Codex-based workflow for turning research ideas into structured paper-planning artifacts and an implementation codebase. Its current core is a sequence of planning skills, a repository scaffold skill, and TypeScript pipelines that run development and skill-evolution agents from those artifacts.

## How To Use

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Use `academic-army-architect` to turn the idea into `paper_blueprint.md`. Because an early idea is usually underspecified, this step may involve multiple rounds of clarification and revision before the blueprint is specific enough to guide downstream work.

Once you are satisfied with the paper blueprint, the next planning skills derive `experiment_plan.md` and `coding_plan.md`. Those three artifacts become the project starting point for repository scaffolding and iterative code development.

## Running Workflow

The current project workflow first uses three planning skills to produce three AI-facing Markdown artifacts:

1. `academic-army-architect` creates `paper_blueprint.md`, the strategic paper blueprint that fixes the paper identity, target venue posture, claims, contribution boundary, candidate method space, evidence needs, and downstream constraints.
2. `academic-army-experiment-plan` creates `experiment_plan.md`, the experiment strategy that maps paper claims to evidence, datasets or workloads, metrics, baselines, ablations, robustness checks, and reviewer-facing validation needs.
3. `academic-army-coding-plan` creates `coding_plan.md`, the implementation contract that turns the blueprint and experiment plan into logical module boundaries, interface and entrypoint semantics, harnesses, testing categories, raw-result artifact schemas, and method-freeze rules.

Each planning skill also writes a Chinese `*.explain.md` companion for human review, but the development runner consumes the three English Markdown files above.

If the direct output from `academic-army-architect`, `academic-army-experiment-plan`, or `academic-army-coding-plan` is not satisfactory, do not only patch the generated artifact by hand. Add the concrete dissatisfaction, preferred behavior, and failure pattern to the matching metaskill under [`metaskills/`](metaskills/), then run the corresponding `envolve.sh` script for several rounds. Those scripts call the TypeScript [`evolve-skill`](src/evolve-skill/README.md) pipeline. Unlike directly running a skill once, `evolve-skill` is a small multi-agent loop: fresh runner agents test the skill on fixed tasks, an evaluator agent judges the produced artifacts against the metaskill, and a modifier agent revises the skill itself from that review. A few rounds usually make the next direct skill output much closer to the desired shape.

After the three planning artifacts are ready, `academic-army-repo-scaffold` can initialize a real starter repository for the codebase. It uses DeepResearch to choose a template, official initializer, or high-quality template repository, generates the starter repository, then adds the fixed experiment directories `data/`, `output/`, `results/`, and `harness/`. It writes dependency declarations and repo-local installation instructions, records installable dependencies and reference-only sources in `REFERENCES.md` and `REFERENCES.zh-CN.md`, preserves the template's test layout, and keeps README text focused on the current repository structure and usage.

The repo scaffold skill does not implement paper methods, harness logic, tests, metrics, loaders, exporters, or experiment runners. Those belong to later implementation work.

After the planning artifacts are ready, run:

```bash
bash runs/develop.sh
```

[`runs/develop.sh`](runs/develop.sh) calls the TypeScript `developing` pipeline, which reads the three planning artifacts and iteratively writes code under `output/codebase`. See [`src/README.md`](src/README.md) for the TypeScript entry points and [`src/developing/README.md`](src/developing/README.md) for the development loop implementation.

## Guiding Principle

The central principle of AcademicArmy is: build according to the planning artifacts.

`paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` should be specific enough that downstream agents can implement the project without redesigning its research direction, evidence strategy, or code contract during development.

## Planning Artifact Language

Planning skills use a fixed language split. AI-facing artifacts such as `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` are written in English and contain only the plan or specification. Their companion explanation files, such as `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md`, are written in Chinese so the user can review the reasoning, trade-offs, and confirmation state. Technical terms, paper titles, venue names, datasets, benchmarks, methods, entrypoint semantics, code identifiers, and user-provided existing paths may remain in English when that is clearer.

## Design Tips

Parts that require fine-grained research should mainly be handled by skills that know how to call Deep Research through APIs. This avoids saving large amounts of local data only for retrieval, keeping the project lighter and making research updates easier to refresh.

## Skill Development

For the meta-skill workflow used to build and evolve AcademicArmy skills, see [`metaskills/README.md`](metaskills/README.md).

## DeepResearch MCP

AcademicArmy includes a local stdio MCP implementation in the [`mcp-server`](mcp-server) directory. It exposes one tool:

- `deepresearch(prompt: str)`: runs the prompt with OpenAI Responses using `gpt-5.5`, high reasoning, web search, background mode, and source inclusion.

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

Agent and team wiring lives in [`agent-forge.yaml`](agent-forge.yaml). The current TypeScript agents are implemented under [`src/developing/agents`](src/developing/agents) and [`src/evolve-skill/agents`](src/evolve-skill/agents).

See [`src/README.md`](src/README.md) for the TypeScript pipeline structure and implementation notes.

Prepared AcademicArmy skills live under [`skills/`](skills/), and their matching metaskill design/evolution files live under [`metaskills/`](metaskills/).
