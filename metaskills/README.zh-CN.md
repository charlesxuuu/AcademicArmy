# Metaskills

`metaskills` 用来保存 AcademicArmy skills 的设计说明和 self-evolve 工作流。

[English README](README.md)

## 为什么有这个目录

核心设计思想是 skill self-evolve：用一个 evaluator agent 评价某个 skill 产出的 artifact，把评价交给一个 modifier agent，让 modifier 根据评价修改这个 skill，然后不断循环。这样 skill 不是靠一次性手工编写变好，而是通过稳定任务下的真实输出、具体评价和针对性修改逐轮提升。

普通 skill 描述 agent 应该如何完成某个研究规划任务。metaskill 描述这个 skill 本身应该如何设计：它的目标、写作方式、预期输出，以及修改时需要重点检查的问题。在 self-evolve 中，evaluator 用 metaskill 作为评价 artifact 的标准，modifier 用 metaskill 作为修改 skill 的标准。

## 什么时候使用

如果觉得某个 skill 的输出不满意，先修改对应的 metaskill，而不是凭模糊印象直接改 skill。

这对 AcademicArmy 开头使用的三个规划类 skill 尤其重要：`academic-army-architect`、`academic-army-experiment-plan` 和 `academic-army-coding-plan`。如果它们直接生成的产物不满意，就把不满意点写进对应 metaskill，再运行几轮 `envolve.sh`。

## 快速开始

### 1. 找到对应 metaskill

当前已准备的 AcademicArmy skill metaskill 如下：

| Skill | 修改这个文件 | 运行这个脚本 |
|---|---|---|
| `academic-army-architect` | [`academic-army-architect/METASKILL.md`](academic-army-architect/METASKILL.md) | 用 `bash` 运行 [`academic-army-architect/envolve.sh`](academic-army-architect/envolve.sh) |
| `academic-army-experiment-plan` | [`academic-army-experiment-plan/METASKILL.md`](academic-army-experiment-plan/METASKILL.md) | 用 `bash` 运行 [`academic-army-experiment-plan/envolve.sh`](academic-army-experiment-plan/envolve.sh) |
| `academic-army-coding-plan` | [`academic-army-coding-plan/METASKILL.md`](academic-army-coding-plan/METASKILL.md) | 用 `bash` 运行 [`academic-army-coding-plan/envolve.sh`](academic-army-coding-plan/envolve.sh) |
| `academic-army-repo-scaffold` | [`academic-army-repo-scaffold/METASKILL.md`](academic-army-repo-scaffold/METASKILL.md) | 用 `bash` 运行 [`academic-army-repo-scaffold/envolve.sh`](academic-army-repo-scaffold/envolve.sh) |

对 `academic-army-architect` 调用 `evolve-skill` 前，先创建或确认 [`academic-army-architect/ENVOLVETASK.md`](academic-army-architect/ENVOLVETASK.md)（Windows 路径：`metaskills\academic-army-architect\ENVOLVETASK.md`）。这个固定任务是 runner 在 evolution 轮次中测试 architect skill 的输入。

`academic-army-repo-scaffold` 这个 metaskill 定义 template-first 的仓库初始化 skill：先用选定 initializer 或 template 生成真实 starter repo，再叠加 `data/`、`output/`、`results/` 和 `harness/`；写出 repo-local 安装说明；配置可安装依赖但不执行安装；记录只能作为参考的外部来源；保留模板决定的测试结构；README 只客观说明当前仓库结构和用法。

### 2. 补充具体 tips

打开对应的 metaskill 文件，在里面补充具体 tips：这次 artifact 哪里不好、后续应该更偏向什么写法、应该避免什么问题。

metaskill 设计文档应该说明目标 skill 想产出什么、什么样的输出算好、哪些常见失败模式需要避免，以及哪些内容不应该写进 skill。

### 3. 运行预设脚本

首次使用先安装依赖：

```bash
npm install
```

在仓库根目录运行某个已经准备好的 evolution 脚本：

```bash
bash metaskills/academic-army-architect/envolve.sh
```

运行这个脚本时，会用该 skill 对应的路径调用 `evolve-skill` pipeline。脚本实际运行内容和 loop 行为见 [`src/evolve-skill/README.zh-CN.md`](../src/evolve-skill/README.zh-CN.md)。

### 4. 检查新一轮 artifact

检查新一轮 artifact；如果还不稳定，就继续补充 tips 并再次运行。

运行这些已链接的 evolution 脚本时，会调用 TypeScript 的 `evolve-skill` pipeline。TypeScript 入口和目录结构见 [`src/README.zh-CN.md`](../src/README.zh-CN.md)，skill evolution loop 的实现见 [`src/evolve-skill/README.zh-CN.md`](../src/evolve-skill/README.zh-CN.md)。

## Evolution loop 做什么

AcademicArmy 的 skill 不是一次性写完就固定下来，而是通过一套 meta-skill 迭代流程逐步打磨。

我们会先初步编写一个 skill。这个阶段用到的相关 prompt 和记录保存在对应的 [`metaskills`](.) 目录中，方便读者查看这个 skill 最初是如何被制作出来的。

随后，我们选择一个固定选题，并围绕这个选题反复运行下面的循环：

1. 执行当前版本的 skill。
2. 把 skill 的输出和 `metaskills` 中的相关记录一起交给 evaluator agent。
3. 让 evaluator agent 仔细分析当前 skill 存在哪些问题：有没有冗余的地方，语言是否清晰，内容是否完整，结构是否适合后续 agent 稳定执行。
4. 把修改意见交给 Codex，让 Codex 修改 skill。
5. 再次执行修改后的 skill，并继续用同一个固定选题检验效果。

这个循环的作用是让不同版本的 skill 在稳定任务条件下可比较。我们的目标是逐步减少冗余、修正表达和内容问题，并让每个 skill 更容易被后续 agent 一致地执行。

运行这些脚本时，会调用 TypeScript 的 [`evolve-skill`](../src/evolve-skill/README.zh-CN.md) pipeline；它不同于直接运行一次 skill，而是一个简单的 multi-agent loop：新的 runner agents 在固定任务上生成产物，evaluator agent 按 metaskill 评价这些产物，modifier agent 根据评价修改 skill 本身。这个循环多跑几轮，通常能让下一次直接运行 skill 的输出更接近预期。

## 目录结构

每个 skill 可以在 `metaskills` 下有一个对应目录：

```text
metaskills/
  academic-army-architect/
    METASKILL.md
    ENVOLVETASK.md
    envolve.sh
```

[`METASKILL.md`](academic-army-architect/METASKILL.md) 记录这个 skill 的设计目标和 tips。

[`ENVOLVETASK.md`](academic-army-architect/ENVOLVETASK.md) 是 evolution 时固定使用的测试任务。

[`envolve.sh`](academic-army-architect/envolve.sh) 用来运行这个 skill 的 evolution loop。文件名保留为 `envolve.sh`，和当前项目约定一致。

共享 runner 是 `evolve-skill` pipeline，不属于每个 skill 自己的 metaskill 目录。TypeScript 实现见 [`src/evolve-skill/README.zh-CN.md`](../src/evolve-skill/README.zh-CN.md)。

在这个目录结构里，[`METASKILL.md`](academic-army-architect/METASKILL.md) 和 [`ENVOLVETASK.md`](academic-army-architect/ENVOLVETASK.md) 为 `evolve-skill` pipeline 提供必需输入。当前目录下的 [`envolve.sh`](academic-army-architect/envolve.sh) 只是一个便捷命令：它把某个具体 skill 的 `--skill-path`、`--artifact-path` 输出文件夹、`--metaskill-path` 和 `--task-path` 填好，然后调用共享 runner。

## 语言契约

metaskill 在设计或修改规划类 skill 时，固定采用同一个产物语言契约：面向 AI 执行的主计划使用英文，面向用户确认的解释文件使用中文。当前规划类 skills 中，`paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md` 保持 English-only；`paper_blueprint.explain.md`、`experiment_plan.explain.md` 和 `coding_plan.explain.md` 使用中文解释，并在有助于准确表达时保留英文技术标识符。

## 新增 Metaskill

在 `metaskills` 下创建一个新目录，包含：

```text
METASKILL.md
ENVOLVETASK.md
envolve.sh
```

固定 evolution task 应该是一个有代表性的固定任务，方便不同版本的 skill 在多轮迭代中进行对比。

可以复制已有的 [`envolve.sh`](academic-army-architect/envolve.sh)，然后修改其中的路径。

## 常见问题

| 问题 | 常见原因 | 解决办法 |
|---|---|---|
| Skill 输出仍然不稳定 | Metaskill guidance 仍然太模糊或不完整。 | 继续补充具体 failure mode 和 tips，然后再次运行 evolution 脚本。 |
| 不同版本难以比较 | 固定 evolution task 不够稳定。 | 把 `ENVOLVETASK.md` 改成更有代表性的固定任务。 |
| 脚本在 loop 开始前失败 | 依赖或 pipeline config 缺失。 | 运行 `npm install`，并检查 TypeScript 入口和 config 路径。 |
