# AcademicArmy

AcademicArmy 是一个基于 Codex 的研究工作流，用来把研究想法转成结构化论文规划产物和可持续开发的实现代码库。当前核心由一组规划类 skills、一个仓库 scaffold skill，以及驱动开发和 skill evolution agents 的 TypeScript pipelines 组成。

## 项目用法

项目从一个想法开始。这个想法可以很粗略，也可以比较详细，不需要一开始就是完整的研究方案。

使用 `academic-army-architect` 把这个想法整理成 `paper_blueprint.md`，也就是后续执行用的核心“施工图”。由于最初的想法通常还不够收敛，这一步可以通过多轮澄清和修改，把论文蓝图逐步调整到足够支撑下游工作的状态。

当你对论文蓝图满意后，后续规划类 skills 会继续生成 `experiment_plan.md` 和 `coding_plan.md`。这三份规划产物共同构成 AcademicArmy 的施工图，成为仓库初始化和迭代代码开发的项目起点。

## 运行流程

当前项目流程会先和三个规划类 skill 交互，得到三份面向 AI 执行的 Markdown 产物：

1. `academic-army-architect` 生成 `paper_blueprint.md`，也就是论文战略蓝图，用来固定论文身份、目标 venue 姿态、核心 claims、贡献边界、候选方法空间、证据需求和下游约束。
2. `academic-army-experiment-plan` 生成 `experiment_plan.md`，也就是实验策略，把论文 claims 映射到证据链、数据集或 workload、指标、baselines、消融、鲁棒性检查和审稿人关心的验证点。
3. `academic-army-coding-plan` 生成 `coding_plan.md`，也就是代码实现契约，把论文蓝图和实验方案转成逻辑模块边界、接口与 entrypoint 语义、实验 harness、测试类别、raw result artifact schema 和 method freeze 规则。

每个规划类 skill 还会同时生成一份中文 `*.explain.md` 解释文件，方便用户审阅；但后续开发 runner 读取的是上面三份英文 Markdown。

如果 `academic-army-architect`、`academic-army-experiment-plan` 或 `academic-army-coding-plan` 直接生成的产物不满意，不建议只手工修产物本身。更好的做法是打开 [`metaskills/`](metaskills/) 下对应的 metaskill，把不满意的地方、希望偏向的写法和失败模式写进去，然后运行对应的 `envolve.sh` 脚本多迭代几轮。这些脚本会调用 TypeScript 的 [`evolve-skill`](src/evolve-skill/README.zh-CN.md) pipeline。`evolve-skill` 不同于直接运行一次 skill，它是一个简单的 multi-agent loop：新的 runner agent 用固定任务测试 skill，evaluator agent 按 metaskill 评价产物，modifier agent 再根据评价修改 skill 本身。通常多跑几轮后，再直接运行该 skill，就能得到更接近预期的结果。

三份规划产物准备好后，`academic-army-repo-scaffold` 可以为代码库初始化一个真实 starter repository。它会使用 DeepResearch 选择合适的 template、官方 initializer 或高质量 template repository，生成 starter repository，然后叠加固定实验目录 `data/`、`output/`、`results/` 和 `harness/`。它会写入依赖声明和 repo-local 安装说明，在 `REFERENCES.md` 和 `REFERENCES.zh-CN.md` 中记录可安装依赖和仅作参考的外部来源，保留模板决定的测试结构，并让 README 聚焦当前仓库结构和用法。

repo scaffold skill 不实现论文方法、harness 逻辑、测试、metric、loader、exporter 或实验 runner；这些属于后续实现工作。

三份规划产物准备好后，运行：

```bash
bash runs/develop.sh
```

[`runs/develop.sh`](runs/develop.sh) 会调用 TypeScript 的 `developing` pipeline，读取三份规划产物，并在 `output/codebase` 下迭代写代码。TypeScript 入口和目录结构见 [`src/README.zh-CN.md`](src/README.zh-CN.md)，开发循环实现见 [`src/developing/README.zh-CN.md`](src/developing/README.zh-CN.md)。

## 指导思想

AcademicArmy 的主体核心可以概括为一句话：按图施工。

这里的“施工图”就是 `paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md`。它们应该足够具体，让下游 agents 在实现阶段不需要重新设计研究方向、证据策略或代码契约。

## 规划产物语言

规划类 skills 使用固定语言分工。面向后续 AI 执行的产物，例如 `paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md`，统一使用英文，并且只放方案或规范本身。配套解释文件，例如 `paper_blueprint.explain.md`、`experiment_plan.explain.md` 和 `coding_plan.explain.md`，统一使用中文，用来帮助用户确认推导逻辑、关键取舍和当前确认状态。论文标题、会议名、数据集、benchmark、method、entrypoint 语义、代码标识符和用户明确给出的既有路径等技术内容，可以在中文解释中保留英文。

## 设计 Tips

需要精细调研的部分，主要通过会使用 API 的 skill 调用 Deep Research 来完成。这样可以避免为了检索而在本地保存大量数据，让项目更轻量，也方便后续刷新调研结果。

## Skill 开发

AcademicArmy 制作和迭代 skill 的 meta-skill 工作流见 [`metaskills/README.zh-CN.md`](metaskills/README.zh-CN.md)。

## DeepResearch MCP

AcademicArmy 在 [`mcp-server`](mcp-server) 目录下提供了本地 stdio MCP 实现。它只暴露一个工具：

- `deepresearch(prompt: str)`：把 prompt 交给 OpenAI Responses，以 `gpt-5.5`、high reasoning、web search、background mode 和 source inclusion 的固定配置运行。

先在仓库根目录创建 `.env`：

```env
OPENAI_API_KEY=your_api_key_here
```

如有需要，从 [`mcp-server/requirements.txt`](mcp-server/requirements.txt) 安装 MCP server 依赖：

```powershell
cd <repo>
python -m pip install -r ./mcp-server/requirements.txt
```

项目 pipeline 会通过 [`agent-forge.yaml`](agent-forge.yaml) 使用 `academic_army_mcp_tools`。该配置会在仓库根目录以 `PYTHONPATH=.` 和 `cwd=.` 运行 `python -m mcp-server`，因此 evolve/developing runner 不需要额外执行 Codex MCP 安装步骤。

如果直接在 Codex 中运行 AcademicArmy skills，需要用 [`install_mcp.py`](install_mcp.py) 把同一个 MCP server 安装到 Codex 里，这样 skill 才能在项目 pipeline 之外调用 `academic_army_mcp_tools.deepresearch`：

```powershell
python install_mcp.py
```

安装脚本会刷新 Codex 中的 `academic_army_mcp_tools` 配置项，注册当前 Python 可执行文件和 `-m mcp-server`，把仓库根目录设置为 MCP 工作目录，读取 `.env`，并把这些环境变量传给 MCP server。

如果需要覆盖或补充环境变量，可以重复使用 `-e/--env NAME=VALUE`：

```powershell
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

使用时只需要让 agent 给 `deepresearch` 传入一个自包含 prompt，例如：

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## 项目结构

Agent 和团队 wiring 位于 [`agent-forge.yaml`](agent-forge.yaml)。当前 TypeScript agents 分别实现于 [`src/developing/agents`](src/developing/agents) 和 [`src/evolve-skill/agents`](src/evolve-skill/agents)。

TypeScript pipeline 的目录结构和实现说明见 [`src/README.zh-CN.md`](src/README.zh-CN.md)。

已准备的 AcademicArmy skills 位于 [`skills/`](skills/)，对应的 metaskill 设计与 evolution 文件位于 [`metaskills/`](metaskills/)。
