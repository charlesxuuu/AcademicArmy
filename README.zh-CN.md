# AcademicArmy

AcademicArmy 是一个基于 Codex 的研究工作流，用来把研究想法转成结构化论文规划产物和可持续开发的实现代码库。当前核心由一组规划类 skills，以及驱动开发和 skill evolution agents 的 TypeScript pipelines 组成。

> 当前状态：实验性工作流基础设施。生成的项目和运行产物位于 `output/`，该目录被 git 忽略。

[English README](README.md)

## 为什么需要它

AcademicArmy 的主体核心可以概括为一句话：按图施工。

这里的“施工图”就是 `paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md`。它们应该足够具体，让下游 agents 在实现阶段不需要重新设计研究方向、证据策略或代码契约。

需要精细调研的部分，主要通过会使用 API 的 skill 调用 Deep Research 来完成。这样可以避免为了检索而在本地保存大量数据，让项目更轻量，也方便后续刷新调研结果。

## 工作流如何衔接

先使用三个规划类 skill 交互生成三份面向 AI 执行的 Markdown 产物：

| 步骤                            | Artifact             | 作用                                                                                                                                                   |
| ------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `academic-army-architect`       | `paper_blueprint.md` | 论文战略蓝图，用来固定论文身份、目标 venue 姿态、核心 claims、贡献边界、候选方法空间、证据需求和下游约束。                                             |
| `academic-army-experiment-plan` | `experiment_plan.md` | 实验策略，把论文 claims 映射到证据链、数据集或 workload、指标、baselines、消融、鲁棒性检查和审稿人关心的验证点。                                       |
| `academic-army-coding-plan`     | `coding_plan.md`     | 代码实现契约，把论文蓝图和实验方案转成逻辑模块边界、接口与 entrypoint 语义、实验 harness、测试类别、raw result artifact schema 和 method freeze 规则。 |

每个规划类 skill 还会同时生成一份中文 `*.explain.md` 解释文件，方便用户审阅；但后续开发 runner 读取的是上面三份英文 Markdown。

规划类 skills 使用固定语言分工。面向后续 AI 执行的产物，例如 `paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md`，统一使用英文，并且只放方案或规范本身。配套解释文件，例如 `paper_blueprint.explain.md`、`experiment_plan.explain.md` 和 `coding_plan.explain.md`，统一使用中文，用来帮助用户确认推导逻辑、关键取舍和当前确认状态。

## 快速开始

### 1. 安装本地依赖

首次使用先安装依赖：

```bash
npm install
```

如有需要，从 [`mcp-server/requirements.txt`](mcp-server/requirements.txt) 安装 MCP server 依赖：

```bash
python -m pip install -r ./mcp-server/requirements.txt
```

### 2. 配置 AcademicArmy MCP

先在仓库根目录创建 `.env`：

```env
OPENAI_API_KEY=your_api_key_here
```

运行项目 pipeline 时，通过 [`agent-forge.yaml`](agent-forge.yaml) 使用 `academic_army_mcp_tools`。该配置会在仓库根目录以 `PYTHONPATH=.` 和 `cwd=.` 运行 `python -m mcp-server`，因此 evolve/developing runner 不需要额外执行 Codex MCP 安装步骤。

如果直接在 Codex 中运行 AcademicArmy skills，需要用 [`install_mcp.py`](install_mcp.py) 把同一个 MCP server 安装到 Codex 里，这样 skill 才能在项目 pipeline 之外调用 `academic_army_mcp_tools.deepresearch` 和 `academic_army_mcp_tools.writing_master`：

```bash
python install_mcp.py
```

### 3. 生成规划产物

从一个想法开始。这个想法可以很粗略，也可以比较详细，不需要一开始就是完整的研究方案。

使用 `academic-army-architect` 把这个想法整理成 `paper_blueprint.md`，也就是后续执行用的核心“施工图”。由于最初的想法通常还不够收敛，这一步可以通过多轮澄清和修改，把论文蓝图逐步调整到足够支撑下游工作的状态。

当你对论文蓝图满意后，继续使用后续规划类 skills 生成 `experiment_plan.md` 和 `coding_plan.md`。这三份规划产物共同构成 AcademicArmy 的施工图，成为迭代代码开发的项目起点。

### 4. 运行开发循环

三份规划产物准备好后，先把下一轮高层开发目标写进 `output/goal.md`，然后运行：

```bash
$EDITOR output/goal.md
bash runs/develop.sh
```

运行 [`runs/develop.sh`](runs/develop.sh) 来调用 `developing-agent-forge` 提供的 `developing` pipeline，读取三份规划产物和当前 `--goal-path` 文件，并在 `output/codebase` 下迭代写代码。每次想执行下一个新任务时，先更新 `output/goal.md`，再重新运行 wrapper。

开发循环会把项目进度记忆放在 `output/developing-memory/project-progress-memory`，把代码设计记忆放在 `output/developing-memory/code-design-memory`。如果新 goal 开始继承旧上下文，可以在重新运行前编辑或删除这些目录里的过期 memory 文件。

本仓库的 TypeScript 入口和目录结构见 [`src/README.zh-CN.md`](src/README.zh-CN.md)。开发循环实现来自 `developing-agent-forge` 包。

## 常见任务

### 改进规划 Skill 输出

如果 `academic-army-architect`、`academic-army-experiment-plan` 或 `academic-army-coding-plan` 直接生成的产物不满意，不建议只手工修产物本身。更好的做法是打开 [`metaskills/`](metaskills/) 下对应的 metaskill，把不满意的地方、希望偏向的写法和失败模式写进去，然后运行对应的 `envolve.sh` 脚本多迭代几轮。

运行这些脚本时，会调用 TypeScript 的 [`evolve-skill`](src/evolve-skill/README.zh-CN.md) pipeline。`evolve-skill` 不同于直接运行一次 skill，它是一个简单的 multi-agent loop：新的 runner agent 用固定任务测试 skill，evaluator agent 按 metaskill 评价产物，modifier agent 再根据评价修改 skill 本身。通常多跑几轮后，再直接运行该 skill，就能得到更接近预期的结果。

### 直接运行 TypeScript Pipelines

使用 shell scripts 作为这些 TypeScript pipeline 的便捷包装：

```bash
npm run developing
npm run developing-skill
npm run evolve-skill
```

TypeScript pipeline 的目录结构和实现说明见 [`src/README.zh-CN.md`](src/README.zh-CN.md)。

对于 `developing` 和 `developing-skill`，每次想切换到新的任务重点时，更新传给 `--goal-path` 的文件即可。预设 wrappers 使用的是 `output/goal.md`。

### 调用 MCP 工具

AcademicArmy 在 [`mcp-server`](mcp-server) 目录下提供了本地 stdio MCP 实现。它暴露这些工具：

- `deepresearch(prompt: str)`：把 prompt 交给 OpenAI Responses，以 `gpt-5.5`、high reasoning、web search、background mode 和 source inclusion 的固定配置运行。
- `writing_master(prompt: str)`：把 prompt 交给 OpenAI Responses，以 `gpt-5.5-pro`、high reasoning、web search、background mode 和 source inclusion 的固定配置运行，用于高阶学术写作咨询。

使用时只需要让 agent 给工具传入一个自包含 prompt，例如：

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## 项目结构

| 路径               | 用途                                                      |
| ------------------ | --------------------------------------------------------- |
| `agent-forge.yaml` | Agent 和团队 wiring。                                     |
| `install_mcp.py`   | 把项目 MCP server 安装到 Codex，供直接运行 skill 时使用。 |
| `mcp-server/`      | 本地 stdio MCP 实现，暴露 `deepresearch` 和 `writing_master`。 |
| `skills/`          | 已准备的 AcademicArmy skills。                            |
| `metaskills/`      | 对应的 metaskill 设计与 evolution 文件。                  |
| `runs/`            | TypeScript pipelines 的便捷 wrappers。                    |
| `src/`             | TypeScript pipeline 的目录结构和实现说明。                |
| `output/`          | 生成的规划产物、代码库输出和归档。                        |

Agent 和团队 wiring 位于 [`agent-forge.yaml`](agent-forge.yaml)。本仓库内的 TypeScript agents 实现于 [`src/evolve-skill/agents`](src/evolve-skill/agents)；developing agents 来自 `developing-agent-forge`。

已准备的 AcademicArmy skills 位于 [`skills/`](skills/)，对应的 metaskill 设计与 evolution 文件位于 [`metaskills/`](metaskills/)。

## 配置参考

| 文件或变量                | 用于               | 说明                                                                                                                     |
| ------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `.env` / `OPENAI_API_KEY` | AcademicArmy MCP   | MCP server 和 `install_mcp.py` 会读取。                                                                                  |
| `agent-forge.yaml`        | 项目 pipelines     | 以 `PYTHONPATH=.` 和 `cwd=.` 运行 `python -m mcp-server`。                                                               |
| `secret.yaml`             | 预设 shell scripts | 预设 wrappers 使用的本地忽略 config overlay。它可以包含密码、API key、runtime 凭据等不能提交或上传到 GitHub 的隐私内容。 |

如果需要覆盖或补充环境变量，可以重复使用 `-e/--env NAME=VALUE`：

```bash
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

运行安装脚本时，会刷新 Codex 中的 `academic_army_mcp_tools` 配置项，注册当前 Python 可执行文件和 `-m mcp-server`，把仓库根目录设置为 MCP 工作目录，读取 `.env`，并把这些环境变量传给 MCP server。

## 常见问题

| 问题                         | 常见原因                                                                         | 解决办法                                                                                    |
| ---------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 缺少 `OPENAI_API_KEY`        | 没有 `.env`，或没有把变量转发给 Codex MCP。                                      | 创建 `.env`；如果直接在 Codex 中跑 skill，再执行 `python install_mcp.py`。                  |
| Wrapper 找不到 `secret.yaml` | 预设脚本传入了本地 config overlay，用来放密码、API key、runtime 凭据等隐私内容。 | 创建本地 `secret.yaml`，或调整脚本使用你的 config 文件。不要把这个文件提交或上传到 GitHub。 |
| 开发输出偏离规划             | 三份规划产物还不够具体。                                                         | 先修订 `paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md`，再继续开发。         |

## 开发

修改 runner 代码前，使用常规 TypeScript 检查：

```bash
npm run check
npm run lint
```

## License

MIT. See [LICENSE](LICENSE).
