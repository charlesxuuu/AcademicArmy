# Metaskills

`metaskills` 用来保存 AcademicArmy skills 的设计说明和 self-evolve 工作流。

核心设计思想是 skill self-evolve：用一个 evaluator agent 评价某个 skill 产出的 artifact，把评价交给一个 modifier agent，让 modifier 根据评价修改这个 skill，然后不断循环。这样 skill 不是靠一次性手工编写变好，而是通过稳定任务下的真实输出、具体评价和针对性修改逐轮提升。

普通 skill 描述 agent 应该如何完成某个研究规划任务。metaskill 描述这个 skill 本身应该如何设计：它的目标、写作方式、预期输出，以及修改时需要重点检查的问题。在 self-evolve 中，evaluator 用 metaskill 作为评价 artifact 的标准，modifier 用 metaskill 作为修改 skill 的标准。

## Evolve Runner

`evolve-skill` pipeline 是实现 self-evolve loop 的共享 Codex SDK runner。

它保留两个长生命周期 Codex thread：

1. `evaluator`：跨轮次评价 artifact。
2. `modifier`：跨轮次修改目标 skill。

每一轮还会新建一个一次性的 runner thread。runner 不保留上一轮上下文，避免旧 artifact 或旧对话污染下一轮输出。

可以在仓库根目录直接运行：

```bash
npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-architect \
  --artifact-path output/evolve-academic-army-architect \
  --metaskill-path metaskills/academic-army-architect/METASKILL.md \
  --task-path metaskills/academic-army-architect/ENVOLVETASK.md
```

必填参数：

```text
--skill-path       要修改的 skill 目录或文件。
--artifact-path    每轮 runner 清空并复用的输出文件夹。
--metaskill-path   evaluator 和 modifier 使用的 metaskill 设计文档。
--task-path        runner 用来测试 skill 的固定任务文件。
```

可选参数：

```text
--rounds 5
  要运行的 self-evolve 轮数。
```

`--rounds` 默认是 `3`。

## 目录结构

每个 skill 可以在 `metaskills` 下有一个对应目录：

```text
metaskills/
  academic-army-architect/
    METASKILL.md
    ENVOLVETASK.md
    envolve.sh
```

`METASKILL.md` 记录这个 skill 的设计目标和 tips。

`ENVOLVETASK.md` 是 evolution 时固定使用的测试任务。

`envolve.sh` 用来运行这个 skill 的 evolution loop。文件名保留为 `envolve.sh`，和当前项目约定一致。

共享 runner 是 `evolve-skill` pipeline，不属于每个 skill 自己的 metaskill 目录。

在这个目录结构里，`METASKILL.md` 和 `ENVOLVETASK.md` 为 `evolve-skill` pipeline 提供必需输入。当前目录下的 `envolve.sh` 只是一个便捷命令：它把某个具体 skill 的 `--skill-path`、`--artifact-path` 输出文件夹、`--metaskill-path` 和 `--task-path` 填好，然后调用共享 runner。

## Loop 行为

metaskills 的作用是让 skill 的迭代有稳定依据。我们不凭模糊感觉重写 skill，而是让 skill 在一个固定任务上产出 artifact，再根据 metaskill 检查这个 artifact，最后让 Codex 根据具体反馈修改 skill。

整个 loop 保持简单：

1. 新建一次性的 runner thread，运行目标 skill，并把产物写入输出文件夹。
2. 长生命周期的 evaluator thread 根据 metaskill 评价 artifact。
3. 长生命周期的 modifier thread 根据评价修改 skill。
4. 下一轮重新新建 runner thread，避免上一轮产物和上下文污染下一轮。

这里刻意不引入 LangGraph、状态机、registry 或复杂的 defensive wrapper。关键状态只保留在 evaluator/modifier 两个长期 Codex session 里，以及被修改的文件里。

## 预设指令

首次使用先安装依赖：

```bash
npm install
```

在仓库根目录运行某个已经准备好的 evolution 脚本：

```bash
bash metaskills/academic-army-architect/envolve.sh
```

这个脚本会用该 skill 对应的路径调用 `evolve-skill` pipeline。runner 会在每轮开始时清空 artifact 输出文件夹，所以 `--artifact-path` 应该指向一个专用输出文件夹。

## 新增 Metaskill

在 `metaskills` 下创建一个新目录，包含：

```text
METASKILL.md
ENVOLVETASK.md
envolve.sh
```

`METASKILL.md` 应该写成目标 skill 的设计文档，说明这个 skill 想产出什么、什么样的输出算好、哪些常见失败模式需要避免，以及哪些内容不应该写进 skill。

`ENVOLVETASK.md` 应该是一个有代表性的固定任务，方便不同版本的 skill 在多轮迭代中进行对比。

可以复制已有的 `envolve.sh`，然后修改其中的路径。
