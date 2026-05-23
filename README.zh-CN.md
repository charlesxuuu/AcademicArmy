# AcademicArmy

AcademicArmy 是一个用于完成研究论文的 multi-agent 系统。它的核心思路是把想法整理、蓝图制定、论文写作、实验代码、测试优化、图表绘制和论文评审拆分给不同的专业岗位，并让所有岗位围绕同一份论文蓝图协作。

## 项目用法

项目从一个想法开始。这个想法可以很粗略，也可以比较详细，不需要一开始就是完整的研究方案。

把这个想法交给 `ProductManager`。ProductManager 具备 AcademicArmy 运行模式的知识，会帮助你把想法组织成符合 AcademicArmy 规范的论文蓝图，也就是后续执行用的“施工图”。由于最初的想法通常还不够收敛，ProductManager 应该与你进行多轮交互，把论文蓝图逐步调整到你满意的状态。

当你对论文蓝图满意后，项目才正式进入 AcademicArmy 的运行流程。此时论文蓝图成为项目起点，后续各岗位根据它完成论文文本、实验代码、测试、优化、插图、实验结果图和论文评审等工作。

## 指导思想

AcademicArmy 的主体核心可以概括为一句话：按图施工。

ProductManager 给出的论文蓝图应该是“符合规范”的“图纸”，具体到各岗位可以直接上手执行，而不是在执行阶段重新设计项目。AcademicArmy 按照这份图纸完成一篇论文及其支撑材料。

## 设计 Tips

需要精细调研的部分，主要通过会使用 API 的 skill 调用 Deep Research 来完成。这样可以避免为了检索而在本地保存大量数据，让项目更轻量，也方便后续刷新调研结果。

## DeepResearch MCP

AcademicArmy 在 `mcp-server` 目录下提供了本地 stdio MCP 实现。它只暴露一个工具：

- `deepresearch(prompt: str)`：把 prompt 交给 OpenAI Responses，以 `gpt-5.5-pro`、high reasoning、web search、background mode 和 source inclusion 的固定配置运行。

注册前，先在仓库根目录创建 `.env`：

```env
OPENAI_API_KEY=your_api_key_here
```

如有需要，安装虚拟环境依赖：

```powershell
cd <repo>
python -m pip install -r ./mcp-server/requirements.txt
```

注册到 Codex：

```powershell
python install_mcp.py
```

安装脚本会刷新 Codex 中的 `academic_army_mcp_tools` 配置项，然后用运行脚本的 Python 可执行文件注册它。它还会从仓库根目录读取 `.env`，并通过 Codex `--env` 把这些值传给 MCP server。

如果需要覆盖或补充环境变量，可以重复使用 `-e/--env NAME=VALUE`：

```powershell
python install_mcp.py -e OPENAI_API_KEY=your_api_key_here
```

在其它 MCP client 中把它注册成 stdio server：

- 名称：`academic_army_mcp_tools`
- 命令：`python`
- 参数：`-m mcp-server`
- 工作目录：`<repo>`

注意 MCP client 的工作目录必须是仓库根目录，因为 server 会从当前目录加载 `.env`。也可以通过 `-e/--env NAME=VALUE` 直接传入环境变量；这些值会在 `.env` 加载之后写入，因此会覆盖 `.env` 中同名配置。

注册后重启 MCP client。使用时只需要给 `deepresearch` 传入一个自包含 prompt，例如：

```text
Use deepresearch with prompt:
Find the closest papers to this research idea, compare their methods, and return a cited structured report.
```

## 项目结构

Agent 和团队结构见 `AcademicArmy/README.zh-CN.md`。
