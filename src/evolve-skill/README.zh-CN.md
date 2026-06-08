# Evolve Skill Pipeline

[`src/evolve-skill`](.) 实现 [`../../metaskills/README.zh-CN.md`](../../metaskills/README.zh-CN.md) 中说明的 metaskill evolution scripts 所使用的 self-evolution loop。它用于优化已有 skill：反复在固定任务上测试该 skill，评价产出的 artifact，并根据评价进行有针对性的修改。

TypeScript pipeline 的整体用法和入口见 [`src/README.zh-CN.md`](../README.zh-CN.md)。

面向用户的优化流程见 [`../../metaskills/README.zh-CN.md`](../../metaskills/README.zh-CN.md)。

## 直接运行

可以在仓库根目录直接运行 pipeline：

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
--task-path        runner 用来测试 skill 的固定任务文件；可重复传入多个固定任务。
```

可选参数：

```text
--rounds 5
  要运行的 self-evolve 轮数。
```

`--rounds` 默认是 `3`。

## 主流程

[`pipeline.ts`](pipeline.ts) 解析以下参数：

- `--skill-path`：要修改的 skill 目录或文件。
- `--artifact-path`：每轮都会清空并复用的输出目录。
- `--metaskill-path`：用于评价和修改 skill 的设计文档与 tips。
- `--task-path`：用于测试 skill 的一个或多个固定任务。
- `--rounds`：self-evolve 轮数，默认是 `3`。

每一轮执行以下步骤：

1. 清空并重新创建 `--artifact-path`。
2. 对每个配置的 `--task-path` 创建新的 `skill-runner` agent，让目标 skill 在该固定任务上运行并写出 artifacts。
3. 使用 `skill-evaluator` 根据当前 metaskill 指导文件评价 artifact。
4. 把 evaluator review 交给 `skill-modifier`，让它基于同一份 metaskill 指导修改目标 skill。

新建 runner 可以避免前一轮 runner 上下文污染下一轮 artifact。evaluator 和 modifier 通过共享的 `AgentTeam` 调用，因此它们的 agent 配置集中在 pipeline config 中。

## Loop 行为

这个 loop 让 skill 的迭代基于具体产物，而不是凭模糊感觉重写 skill。它会让 skill 在一个固定任务上产出 artifact，再根据 metaskill 检查这个 artifact，最后让 Codex 根据具体反馈修改 skill。

pipeline 通过共享 team 保留两个长生命周期 Codex thread：

1. `skill-evaluator`：跨轮次评价 artifact。
2. `skill-modifier`：跨轮次修改目标 skill。

每一轮还会新建一个一次性的 `skill-runner` thread。runner 不保留上一轮上下文，避免旧 artifact 或旧对话污染下一轮输出。

整个 loop 保持简单：

1. 针对每个配置的 task 新建一次性的 runner thread，运行目标 skill，并把产物写入输出文件夹。
2. 长生命周期的 evaluator thread 根据 metaskill 评价 artifact。
3. 长生命周期的 modifier thread 根据评价修改 skill。
4. 下一轮重新新建 runner thread。

这里刻意不引入 LangGraph、状态机、registry 或复杂的 defensive wrapper。关键状态只保留在 evaluator/modifier 两个长期 Codex session、当前 artifact 文件夹，以及被修改的文件里。

## 重要文件

- [`pipeline.ts`](pipeline.ts)：参数解析和轮次编排。
- [`agents/factory.ts`](agents/factory.ts)：注册 `skill-runner`、`skill-evaluator` 和 `skill-modifier`。
- [`agents/runner.ts`](agents/runner.ts)：读取每个 `--task-path` 配置的固定任务文件，并要求目标 skill 写出 artifacts。
- [`agents/evaluator.ts`](agents/evaluator.ts)：读取 `--metaskill-path` 配置的 metaskill 文件，并评价产出的 artifact。
- [`agents/modifier.ts`](agents/modifier.ts)：读取 metaskill 文件和 evaluator review，然后修改目标 skill。

## 从 Metaskills 使用

当某个 skill 的输出不理想时，先把具体 tips 加到对应的 metaskill 文件，然后在仓库根目录运行该 skill 的 evolution 脚本。预设脚本和路径对应关系见 [`../../metaskills/README.zh-CN.md`](../../metaskills/README.zh-CN.md)。
