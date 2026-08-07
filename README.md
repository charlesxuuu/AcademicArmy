# AcademicArmy

AcademicArmy is a Codex-based workflow for turning research ideas into structured paper-planning artifacts and an implementation codebase. Its current core is a sequence of planning skills and TypeScript pipelines that run development and skill-evolution agents from those artifacts.

> Status: experimental workflow infrastructure. The generated project lives under `workspace/`, which is ignored by git.

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

Install the MCP server into the local virtual environment:

```bash
.venv/bin/python -m pip install -e .
```

### 2. Configure AcademicArmy MCP

Create `.env` in the repository root:

```env
OPENAI_API_KEY=your_api_key_here
```

For project pipeline runs, use the `academic_army_mcp_tools` server through [`agent-forge.yaml`](agent-forge.yaml). That config launches the installed package with `.venv/bin/python -m academic_army_mcp_tools`, independent of each agent thread's working directory.

When running AcademicArmy skills directly in Codex, use [`install_mcp.py`](install_mcp.py) to install the same MCP server into Codex so the skills can call `academic_army_mcp_tools.deepresearch` and `academic_army_mcp_tools.writing_master` outside the project pipeline:

```bash
python install_mcp.py
```

### 3. Generate the planning artifacts

Start with an idea. The idea can be rough or detailed; it does not need to be a complete research plan.

Use `academic-army-architect` to turn the idea into `paper_blueprint.md`. Because an early idea is usually underspecified, this step may involve multiple rounds of clarification and revision before the blueprint is specific enough to guide downstream work.

Once you are satisfied with the paper blueprint, continue with the next planning skills to derive `experiment_plan.md` and `coding_plan.md`. Those three artifacts become the project starting point for iterative code development.

### 4. Run the development loop

After the planning artifacts are ready, write the next high-level development objective into `workspace/plan/goal.md`, then run:

```bash
$EDITOR workspace/plan/goal.md
bash runs/develop.sh
```

Run [`runs/develop.sh`](runs/develop.sh) to call the `developing-agent-forge` development pipeline, which reads the three planning artifacts plus the current `--goal-path` file and iteratively writes code under `workspace/codebase`. Its developer and code reviewer receive Ponytail plus the local [`academic-army-coding-style`](metaskills/academic-army-coding-style/METASKILL.md) guidance from [`agent-forge.yaml`](agent-forge.yaml). Each time you want the next new task, update `workspace/plan/goal.md` before rerunning the wrapper.

The development loop stores project progress memory under `workspace/memory/project-progress` and code design memory under `workspace/memory/code-design`. Memory agents run from the codebase working directory with `workspace/memory` mounted as an additional directory, so they can read implementation context while keeping persistent writes scoped to the memory tree. If a new goal starts inheriting old context, edit or delete stale memory files in those directories before rerunning.

See [`src/README.md`](src/README.md) for the local TypeScript entry points. The development loop implementation lives in the `developing-agent-forge` package.

## Common Tasks

### Improve a planning skill output

If the direct output from `academic-army-architect`, `academic-army-experiment-plan`, or `academic-army-coding-plan` is not satisfactory, do not only patch the generated artifact by hand. Add the concrete dissatisfaction, preferred behavior, and failure pattern to the matching metaskill under [`metaskills/`](metaskills/), then run the corresponding `envolve.sh` script for several rounds.

Running those scripts calls the TypeScript [`evolve-skill`](src/evolve-skill/README.md) pipeline. Unlike directly running a skill once, `evolve-skill` is a small multi-agent loop: fresh runner agents test the skill on fixed tasks, an evaluator agent judges the produced artifacts against the metaskill, and a modifier agent revises the skill itself from that review. A few rounds usually make the next direct skill output much closer to the desired shape.

### Run TypeScript pipelines directly

Use the shell scripts as convenience wrappers around these TypeScript pipelines:

```bash
npm run developing
npm run evolve-skill
```

For the shared CLI and pipeline structure, see [`src/README.md`](src/README.md).

For `developing`, update the file passed to `--goal-path` when you want to run a new task focus. The prepared wrapper uses `workspace/plan/goal.md`. The development loop and its agents come from `developing-agent-forge`; repository-specific coding guidance is injected through `agent-forge.yaml`.

### Call MCP Tools

AcademicArmy includes an installable stdio MCP package in [`academic_army_mcp_tools`](academic_army_mcp_tools). It exposes these tools:

- `deepresearch(prompt: str)`: runs the prompt with OpenAI Responses using `gpt-5.5`, high reasoning, web search, background mode, and source inclusion.
- `writing_master(prompt: str)`: runs the prompt with OpenAI Responses using `gpt-5.5-pro`, high reasoning, web search, background mode, and source inclusion for high-end academic writing review.

Agents should call these tools with a single self-contained prompt. For example:

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## Project Structure

| Path                       | Purpose                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------- |
| `agent-forge.yaml`         | Agent and team wiring.                                                                 |
| `install_mcp.py`           | Installs the project MCP server into Codex for direct skill runs.                      |
| `academic_army_mcp_tools/` | Installable stdio MCP implementation that exposes `deepresearch` and `writing_master`. |
| `skills/`                  | Prepared AcademicArmy skills.                                                          |
| `metaskills/`              | Matching metaskill design/evolution files.                                             |
| `runs/`                    | Convenience wrappers around TypeScript pipelines.                                      |
| `src/`                     | TypeScript pipeline structure and implementation notes.                                |
| `workspace/`               | Generated planning artifacts, codebase workspace, memory, and archives.                |

Agent and team wiring lives in [`agent-forge.yaml`](agent-forge.yaml). The local TypeScript agents are implemented under [`src/evolve-skill/agents`](src/evolve-skill/agents); developing agents come from `developing-agent-forge`.

Prepared AcademicArmy skills live under [`skills/`](skills/), and their matching metaskill design/evolution files live under [`metaskills/`](metaskills/).

## Configuration Reference

| File or variable          | Required for           | Notes                                                                                                                                                                                          |
| ------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.env` / `OPENAI_API_KEY` | AcademicArmy MCP       | Read by the MCP server and by `install_mcp.py`.                                                                                                                                                |
| `agent-forge.yaml`        | Project pipelines      | Launches installed `.venv` package `academic_army_mcp_tools`; run `.venv/bin/python -m pip install -e .` after changing MCP package code.                                                      |
| `secret.yaml`             | Prepared shell scripts | Local ignored config overlay used by the prepared wrappers. It may contain passwords, API keys, runtime credentials, or other private values that must not be committed or uploaded to GitHub. |

To override or add environment variables directly when installing MCP into Codex, repeat `-e/--env NAME=VALUE`:

```bash
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

Running the installer refreshes the Codex `academic_army_mcp_tools` entry, registers the current Python executable with `-m academic_army_mcp_tools`, sets the repository root as the MCP working directory, reads `.env`, and forwards those values to the MCP server.

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
