# TypeScript Pipelines

`src` 存放 AcademicArmy 的 TypeScript runner，用来把规划产物转成可重复运行的 agent workflow。

[English README](README.md)

## 这层代码负责什么

CLI 入口是 [`cli.ts`](cli.ts)。它通过 [`package.json`](../package.json) scripts 暴露三个 pipeline：

| Pipeline           | Package script             | 作用                                                                                       |
| ------------------ | -------------------------- | ------------------------------------------------------------------------------------------ |
| `developing`       | `npm run developing`       | 运行 `developing/` 中实现的代码开发循环；当前任务重点来自 `--goal-path`。                  |
| `developing-skill` | `npm run developing-skill` | 运行同一个 goal-driven 开发循环，并用 `trajectory-optimizer` 根据具体反馈优化 coding-style skill。 |
| `evolve-skill`     | `npm run evolve-skill`     | 运行 `evolve-skill/` 中实现的 skill self-evolution 循环。                                  |

[`pipeline.ts`](pipeline.ts) 是这些命令共用的封装层。它解析各 pipeline 自己的参数，使用 `coding-agent-forge` 加载一个或多个 YAML 配置文件，根据配置好的 factories 创建 `AgentTeam`，运行选中的 pipeline，并在结束后关闭 team。

## 快速开始

在仓库根目录先安装依赖：

```bash
npm install
```

共享 CLI 形态是：

```bash
npm run cli -- <pipeline> [...args]
```

多数项目 workflow 直接使用预设 shell scripts：

```bash
bash runs/develop.sh
bash metaskills/academic-army-architect/envolve.sh
```

每次开始新的开发任务前，先更新 `output/goal.md`；预设的 `developing` 和 `developing-skill` wrapper 会把它作为 `--goal-path` 传入。

## 目录说明

| 路径                                                         | 作用                                                                                                                                                           |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cli.ts`](cli.ts)                                           | 根据名称选择 pipeline，并把剩余 CLI 参数传给对应 pipeline。                                                                                                    |
| [`pipeline.ts`](pipeline.ts)                                 | 共享的 pipeline 定义、配置加载、agent team 构建和清理逻辑。                                                                                                    |
| [`developing/`](developing/)                                 | 读取 `paper_blueprint.md`、`experiment_plan.md`、`coding_plan.md` 和 `--goal-path` 中的目标，然后迭代实现目标代码库。详见 [`developing/README.zh-CN.md`](developing/README.zh-CN.md)。 |
| [`developing/pipelineskill.ts`](developing/pipelineskill.ts) | 给同一个 goal-driven 开发循环叠加 `trajectory-optimizer` hooks，用于在开发过程中优化 coding-style skill。                                                                         |
| [`evolve-skill/`](evolve-skill/)                             | 在固定任务上运行某个 skill，根据 metaskill 评价产物，并让 modifier agent 修改 skill。详见 [`evolve-skill/README.zh-CN.md`](evolve-skill/README.zh-CN.md)。     |

## 共享 Wrapper 如何工作

每个 pipeline 提供自己的参数和配置好的 factories。[`pipeline.ts`](pipeline.ts) 使用 `coding-agent-forge` 加载一个或多个 YAML 配置文件，根据配置好的 factories 创建 `AgentTeam`，运行选中的 pipeline，并在结束后关闭 team。

这样 TypeScript runners 可以共享配置加载、agent team 构建和清理逻辑。

## 和 Shell 脚本的关系

[`runs/`](../runs/) 和 [`metaskills/README.zh-CN.md`](../metaskills/README.zh-CN.md) 中说明的 metaskill scripts 是这些 TypeScript pipeline 的便捷包装。

预设开发 wrapper 使用 `output/goal.md` 作为 `--goal-path` 文件。如果新一轮不希望继承当前临时任务上下文，可以在重新运行前删除 `output/developing/TODO.md`；pipeline 会自动重新创建它。这个基于 TODO 的记忆机制是临时方案，之后会实现更高级的记忆机制来替代或扩展它。

| Script                                              | 调用                       |
| --------------------------------------------------- | -------------------------- |
| [`runs/develop.sh`](../runs/develop.sh)             | `npm run developing`       |
| [`runs/develop-skill.sh`](../runs/develop-skill.sh) | `npm run developing-skill` |
| `metaskills/*/envolve.sh`                           | `npm run evolve-skill`     |

## 开发检查

修改 runner code 前运行：

```bash
npm run check
npm run lint
```

## 下一步阅读

- 开发循环细节：[`developing/README.zh-CN.md`](developing/README.zh-CN.md)
- Skill evolution loop 细节：[`evolve-skill/README.zh-CN.md`](evolve-skill/README.zh-CN.md)
- 面向用户的 skill evolution workflow：[`../metaskills/README.zh-CN.md`](../metaskills/README.zh-CN.md)
