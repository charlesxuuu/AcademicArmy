# AcademicArmy

AcademicArmy is a Codex-based workflow for turning research ideas into structured paper-planning artifacts and an implementation codebase. Its current core is a sequence of planning skills, a repository scaffold skill, and TypeScript pipelines that run development and skill-evolution agents from those artifacts.

> Status: experimental workflow infrastructure. The generated project lives under `output/`, which is ignored by git.

[中文说明](README.zh-CN.md)

## Why It Exists

The central principle of AcademicArmy is: build according to the planning artifacts.

`paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` should be specific enough that downstream agents can implement the project without redesigning its research direction, evidence strategy, or code contract during development.

Parts that require fine-grained research should mainly be handled by skills that know how to call Deep Research through APIs. This avoids saving large amounts of local data only for retrieval, keeping the project lighter and making research updates easier to refresh.

## How The Workflow Fits Together

First use three planning skills to produce three AI-facing Markdown artifacts:

| Step                            | Artifact             | Role                                                                                                                                                                                                                              |
| ------------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `academic-army-architect`       | `paper_blueprint.md` | The strategic paper blueprint that fixes the paper identity, target venue posture, claims, contribution boundary, candidate method space, evidence needs, and downstream constraints.                                             |
| `academic-army-experiment-plan` | `experiment_plan.md` | The experiment strategy that maps paper claims to evidence, datasets or workloads, metrics, baselines, ablations, robustness checks, and reviewer-facing validation needs.                                                        |
| `academic-army-coding-plan`     | `coding_plan.md`     | The implementation contract that turns the blueprint and experiment plan into logical module boundaries, interface and entrypoint semantics, harnesses, testing categories, raw-result artifact schemas, and method-freeze rules. |

Each planning skill also writes a Chinese `*.explain.md` companion for human review, but the development runner consumes the three English Markdown files above.

Planning skills use a fixed language split. AI-facing artifacts such as `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` are written in English and contain only the plan or specification. Their companion explanation files, such as `paper_blueprint.explain.md`, `experiment_plan.explain.md`, and `coding_plan.explain.md`, are written in Chinese so the user can review the reasoning, trade-offs, and confirmation state.

## Quick Start

### 1. Install local dependencies

Install package dependencies once:

```bash
npm install
```

Install MCP server dependencies from [`mcp-server/requirements.txt`](mcp-server/requirements.txt) if needed:

```bash
python -m pip install -r ./mcp-server/requirements.txt
```

### 2. Configure DeepResearch MCP

Create `.env` in the repository root:

```env
OPENAI_API_KEY=your_api_key_here
```

For project pipeline runs, use the `academic_army_mcp_tools` server through [`agent-forge.yaml`](agent-forge.yaml). That config launches the server as `python -m mcp-server` with `PYTHONPATH=.` and `cwd=.` from the repository root, so the evolve/developing runners do not need a separate Codex MCP installation step.

When running AcademicArmy skills directly in Codex, use [`install_mcp.py`](install_mcp.py) to install the same MCP server into Codex so the skill can call `academic_army_mcp_tools.deepresearch` outside the project pipeline:

```bash
python install_mcp.py
```

### 3. Generate the planning artifacts

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Use `academic-army-architect` to turn the idea into `paper_blueprint.md`. Because an early idea is usually underspecified, this step may involve multiple rounds of clarification and revision before the blueprint is specific enough to guide downstream work.

Once you are satisfied with the paper blueprint, continue with the next planning skills to derive `experiment_plan.md` and `coding_plan.md`. Those three artifacts become the project starting point for repository scaffolding and iterative code development.

### 4. Initialize the codebase scaffold

After the three planning artifacts are ready, use `academic-army-repo-scaffold` to initialize a real starter repository for the codebase. It uses DeepResearch to choose a template, official initializer, or high-quality template repository, generates the starter repository, then adds the fixed experiment directories `data/`, `output/`, `results/`, and `harness/`. It writes dependency declarations and repo-local installation instructions, records installable dependencies and reference-only sources in `REFERENCES.md` and `REFERENCES.zh-CN.md`, preserves the template's test layout, and keeps README text focused on the current repository structure and usage.

The repo scaffold skill does not implement paper methods, harness logic, tests, metrics, loaders, exporters, or experiment runners. Those belong to later implementation work.

### 5. Run the development loop

After the planning artifacts are ready, run:

```bash
bash runs/develop.sh
```

Run [`runs/develop.sh`](runs/develop.sh) to call the TypeScript `developing` pipeline, which reads the three planning artifacts and iteratively writes code under `output/codebase`. See [`src/README.md`](src/README.md) for the TypeScript entry points and [`src/developing/README.md`](src/developing/README.md) for the development loop implementation.

## Common Tasks

### Improve a planning skill output

If the direct output from `academic-army-architect`, `academic-army-experiment-plan`, or `academic-army-coding-plan` is not satisfactory, do not only patch the generated artifact by hand. Add the concrete dissatisfaction, preferred behavior, and failure pattern to the matching metaskill under [`metaskills/`](metaskills/), then run the corresponding `envolve.sh` script for several rounds.

Running those scripts calls the TypeScript [`evolve-skill`](src/evolve-skill/README.md) pipeline. Unlike directly running a skill once, `evolve-skill` is a small multi-agent loop: fresh runner agents test the skill on fixed tasks, an evaluator agent judges the produced artifacts against the metaskill, and a modifier agent revises the skill itself from that review. A few rounds usually make the next direct skill output much closer to the desired shape.

### Run TypeScript pipelines directly

Use the shell scripts as convenience wrappers around these TypeScript pipelines:

```bash
npm run developing
npm run developing-skill
npm run evolve-skill
```

For the shared CLI and pipeline structure, see [`src/README.md`](src/README.md).

### Call DeepResearch

AcademicArmy includes a local stdio MCP implementation in the [`mcp-server`](mcp-server) directory. It exposes one tool:

- `deepresearch(prompt: str)`: runs the prompt with OpenAI Responses using `gpt-5.5`, high reasoning, web search, background mode, and source inclusion.

Agents should call the `deepresearch` tool with a single self-contained prompt. For example:

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## Project Structure

| Path               | Purpose                                                           |
| ------------------ | ----------------------------------------------------------------- |
| `agent-forge.yaml` | Agent and team wiring.                                            |
| `install_mcp.py`   | Installs the project MCP server into Codex for direct skill runs. |
| `mcp-server/`      | Local stdio MCP implementation that exposes `deepresearch`.       |
| `skills/`          | Prepared AcademicArmy skills.                                     |
| `metaskills/`      | Matching metaskill design/evolution files.                        |
| `runs/`            | Convenience wrappers around TypeScript pipelines.                 |
| `src/`             | TypeScript pipeline structure and implementation notes.           |
| `output/`          | Generated planning artifacts, codebase output, and archives.      |

Agent and team wiring lives in [`agent-forge.yaml`](agent-forge.yaml). The current TypeScript agents are implemented under [`src/developing/agents`](src/developing/agents) and [`src/evolve-skill/agents`](src/evolve-skill/agents).

Prepared AcademicArmy skills live under [`skills/`](skills/), and their matching metaskill design/evolution files live under [`metaskills/`](metaskills/).

## Configuration Reference

| File or variable          | Required for           | Notes                                                                                                                                                                                          |
| ------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.env` / `OPENAI_API_KEY` | DeepResearch MCP       | Read by the MCP server and by `install_mcp.py`.                                                                                                                                                |
| `agent-forge.yaml`        | Project pipelines      | Launches `academic_army_mcp_tools` as `python -m mcp-server` with `PYTHONPATH=.` and `cwd=.`.                                                                                                  |
| `secret.yaml`             | Prepared shell scripts | Local ignored config overlay used by the prepared wrappers. It may contain passwords, API keys, runtime credentials, or other private values that must not be committed or uploaded to GitHub. |

To override or add environment variables directly when installing MCP into Codex, repeat `-e/--env NAME=VALUE`:

```bash
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

Running the installer refreshes the Codex `academic_army_mcp_tools` entry, registers the current Python executable with `-m mcp-server`, sets the repository root as the MCP working directory, reads `.env`, and forwards those values to the MCP server.

## Troubleshooting

| Problem                             | Likely cause                                                                                                                    | Fix                                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `OPENAI_API_KEY` is missing         | `.env` is not present or was not forwarded to Codex MCP.                                                                        | Create `.env`; when running skills directly in Codex, rerun `python install_mcp.py`.                                   |
| A wrapper cannot find `secret.yaml` | The prepared shell scripts pass a local config overlay for private values such as passwords, API keys, and runtime credentials. | Create local `secret.yaml` or adjust the script to use your config files. Do not commit or upload this file to GitHub. |
| Development output is drifting      | The planning artifacts are not specific enough.                                                                                 | Revise `paper_blueprint.md`, `experiment_plan.md`, and `coding_plan.md` before continuing development.                 |

## Development

Use the normal TypeScript checks before changing runner code:

```bash
npm run check
npm run lint
```

## License

MIT. See [LICENSE](LICENSE).
