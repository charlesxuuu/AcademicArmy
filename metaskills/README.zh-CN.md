# Metaskills

`metaskills` 用来保存 AcademicArmy skills 的设计说明和 self-evolve 工作流。

核心设计思想是 skill self-evolve：用一个 evaluator agent 评价某个 skill 产出的 artifact，把评价交给一个 modifier agent，让 modifier 根据评价修改这个 skill，然后不断循环。这样 skill 不是靠一次性手工编写变好，而是通过稳定任务下的真实输出、具体评价和针对性修改逐轮提升。

普通 skill 描述 agent 应该如何完成某个研究规划任务。metaskill 描述这个 skill 本身应该如何设计：它的目标、写作方式、预期输出，以及修改时需要重点检查的问题。在 self-evolve 中，evaluator 用 metaskill 作为评价 artifact 的标准，modifier 用 metaskill 作为修改 skill 的标准。

## AcademicArmy 如何制作 Skill

AcademicArmy 的 skill 不是一次性写完就固定下来，而是通过一套 meta-skill 迭代流程逐步打磨。

我们会先初步编写一个 skill。这个阶段用到的相关 prompt 和记录保存在对应的 [`metaskills`](.) 目录中，方便读者查看这个 skill 最初是如何被制作出来的。

随后，我们选择一个固定选题，并围绕这个选题反复运行下面的循环：

1. 执行当前版本的 skill。
2. 把 skill 的输出和 `metaskills` 中的相关记录一起交给 evaluator agent。
3. 让 evaluator agent 仔细分析当前 skill 存在哪些问题：有没有冗余的地方，语言是否清晰，内容是否完整，结构是否适合后续 agent 稳定执行。
4. 把修改意见交给 Codex，让 Codex 修改 skill。
5. 再次执行修改后的 skill，并继续用同一个固定选题检验效果。

这个循环的作用是让不同版本的 skill 在稳定任务条件下可比较。我们的目标是逐步减少冗余、修正表达和内容问题，并让每个 skill 更容易被后续 agent 一致地执行。

## 优化已有 Skill

如果觉得某个 skill 的输出不满意，先修改对应的 metaskill，而不是凭模糊印象直接改 skill。

1. 打开对应的 metaskill 文件；三个主要路径见下面的链接。
2. 在里面补充具体 tips：这次 artifact 哪里不好、后续应该更偏向什么写法、应该避免什么问题。
3. 在仓库根目录运行对应的 evolution 脚本；三个主要脚本见下面的链接。
4. 检查新一轮 artifact；如果还不稳定，就继续补充 tips 并再次运行。

三个主要规划类 skill 对应关系如下：

- `academic-army-architect`：修改 [`metaskills/academic-army-architect/METASKILL.md`](academic-army-architect/METASKILL.md)，然后用 `bash` 运行它的脚本 [`metaskills/academic-army-architect/envolve.sh`](academic-army-architect/envolve.sh)。
- `academic-army-experiment-plan`：修改 [`metaskills/academic-army-experiment-plan/METASKILL.md`](academic-army-experiment-plan/METASKILL.md)，然后用 `bash` 运行它的脚本 [`metaskills/academic-army-experiment-plan/envolve.sh`](academic-army-experiment-plan/envolve.sh)。
- `academic-army-coding-plan`：修改 [`metaskills/academic-army-coding-plan/METASKILL.md`](academic-army-coding-plan/METASKILL.md)，然后用 `bash` 运行它的脚本 [`metaskills/academic-army-coding-plan/envolve.sh`](academic-army-coding-plan/envolve.sh)。

这些已链接的 evolution 脚本会调用 TypeScript 的 `evolve-skill` pipeline。TypeScript 入口和目录结构见 [`src/README.zh-CN.md`](../src/README.zh-CN.md)，skill evolution loop 的实现见 [`src/evolve-skill/README.zh-CN.md`](../src/evolve-skill/README.zh-CN.md)。

## 语言契约

metaskill 在设计或修改规划类 skill 时，固定采用同一个产物语言契约：面向 AI 执行的主计划使用英文，面向用户确认的解释文件使用中文。当前规划类 skills 中，`paper_blueprint.md`、`experiment_plan.md` 和 `coding_plan.md` 保持 English-only；`paper_blueprint.explain.md`、`experiment_plan.explain.md` 和 `coding_plan.explain.md` 使用中文解释，并在有助于准确表达时保留英文技术标识符。

## Evolve Runner

共享 runner 是 TypeScript 的 `evolve-skill` pipeline。CLI 参数、loop 行为和实现细节见 [`src/evolve-skill/README.zh-CN.md`](../src/evolve-skill/README.zh-CN.md)。

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

## 预设指令

首次使用先安装依赖：

```bash
npm install
```

在仓库根目录运行某个已经准备好的 evolution 脚本：

```bash
bash metaskills/academic-army-architect/envolve.sh
```

这个脚本会用该 skill 对应的路径调用 `evolve-skill` pipeline。脚本实际运行内容和 loop 行为见 [`src/evolve-skill/README.zh-CN.md`](../src/evolve-skill/README.zh-CN.md)。

## 新增 Metaskill

在 `metaskills` 下创建一个新目录，包含：

```text
METASKILL.md
ENVOLVETASK.md
envolve.sh
```

metaskill 设计文档应该说明目标 skill 想产出什么、什么样的输出算好、哪些常见失败模式需要避免，以及哪些内容不应该写进 skill。

固定 evolution task 应该是一个有代表性的固定任务，方便不同版本的 skill 在多轮迭代中进行对比。

可以复制已有的 [`envolve.sh`](academic-army-architect/envolve.sh)，然后修改其中的路径。
