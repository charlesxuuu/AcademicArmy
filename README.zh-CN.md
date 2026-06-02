# AcademicArmy

AcademicArmy 是一个用于完成研究论文的 multi-agent 系统。它的核心思路是把想法整理、蓝图制定、论文写作、实验代码、测试优化、图表绘制和论文评审拆分给不同的专业岗位，并让所有岗位围绕同一份论文蓝图协作。

## 项目用法

项目从一个想法开始。这个想法可以很粗略，也可以比较详细，不需要一开始就是完整的研究方案。

把这个想法交给 `ProductManager`。ProductManager 具备 AcademicArmy 运行模式的知识，会帮助你把想法组织成符合 AcademicArmy 规范的论文蓝图，也就是后续执行用的“施工图”。由于最初的想法通常还不够收敛，ProductManager 应该与你进行多轮交互，把论文蓝图逐步调整到你满意的状态。

当你对论文蓝图满意后，项目才正式进入 AcademicArmy 的运行流程。此时论文蓝图成为项目起点，后续各岗位根据它完成论文文本、实验代码、测试、优化、插图、实验结果图和论文评审等工作。

## 指导思想

AcademicArmy 的主体核心可以概括为一句话：按图施工。

ProductManager 给出的论文蓝图应该是“符合规范”的“图纸”，具体到各岗位可以直接上手执行，而不是在执行阶段重新设计项目。AcademicArmy 按照这份图纸完成一篇论文及其支撑材料。

## 规划产物语言

规划类 skills 使用固定语言分工。面向后续 AI 执行的产物，例如 `paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md`，统一使用英文，并且只放方案或规范本身。配套解释文件，例如 `paper_blueprint.explain.md`、`experiment_plan.explain.md` 和 `coding_plan.explain.md`，统一使用中文，用来帮助用户确认推导逻辑、关键取舍和当前确认状态。论文标题、会议名、数据集、benchmark、method、路径、命令和代码标识符等技术内容，可以在中文解释中保留英文。

## 设计 Tips

需要精细调研的部分，主要通过会使用 API 的 skill 调用 Deep Research 来完成。这样可以避免为了检索而在本地保存大量数据，让项目更轻量，也方便后续刷新调研结果。

## Skill 制作流程

AcademicArmy 的 skill 不是一次性写完就固定下来，而是通过一套 meta-skill 迭代流程逐步打磨。

我们会先初步编写一个 skill。这个阶段用到的相关 prompt 和记录保存在 `metaskills` 文件夹中，方便读者查看这个 skill 最初是如何被制作出来的。

随后，我们选择一个固定选题，并围绕这个选题反复运行下面的循环：

1. 执行当前版本的 skill。
2. 把 skill 的输出和 `metaskills` 中的相关记录一起交给另一个 agent。
3. 让这个 agent 仔细分析当前 skill 存在哪些问题：有没有冗余的地方，语言是否清晰，内容是否完整，结构是否适合后续 agent 稳定执行。
4. 根据这个分析，总结出 skill 可以如何优化。
5. 把修改意见交给 Codex，让 Codex 修改 skill。
6. 再次执行修改后的 skill，并继续用同一个固定选题检验效果。

这个循环的作用是让不同版本的 skill 在稳定任务条件下可比较。我们的目标是逐步减少冗余、修正表达和内容问题，并让每个 skill 更容易被后续 agent 一致地执行。

## DeepResearch MCP

AcademicArmy 在 `mcp-server` 目录下提供了本地 stdio MCP 实现。它只暴露一个工具：

- `deepresearch(prompt: str)`：把 prompt 交给 OpenAI Responses，以 `gpt-5.5-pro`、high reasoning、web search、background mode 和 source inclusion 的固定配置运行。

先在仓库根目录创建 `.env`：

```env
OPENAI_API_KEY=your_api_key_here
```

如有需要，安装 MCP server 依赖：

```powershell
cd <repo>
python -m pip install -r ./mcp-server/requirements.txt
```

项目 pipeline 会通过 `agent-forge.yaml` 使用 `academic_army_mcp_tools`。该配置会在仓库根目录以 `PYTHONPATH=.` 和 `cwd=.` 运行 `python -m mcp-server`，因此 evolve/developing runner 不需要额外执行 Codex MCP 安装步骤。

如果直接在 Codex 中运行 AcademicArmy skills，需要把同一个 MCP server 安装到 Codex 里，这样 skill 才能在项目 pipeline 之外调用 `academic_army_mcp_tools.deepresearch`：

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

Agent 和团队结构见 `AcademicArmy/README.zh-CN.md`。
