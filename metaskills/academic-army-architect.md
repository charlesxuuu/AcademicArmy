# Academic Army Architect Metaskill

本文档总结 `academic-army-architect` / `paper-blueprint` skill 的设计经验，用于指导后续编写或重构同类 Codex skill。

它不是原始对话记录，而是从多轮迭代中提炼出的产品需求、设计逻辑、输出契约和可直接交给 skill 编写 agent 的 prompt。

## 1. 这个 Skill 到底是什么

这个 skill 是 autoresearch pipeline 的上游论文战略规划器。

它不是：

- 论文写作器
- 实验规划器
- 绘图规划器
- 章节编排器
- 审稿意见模拟器
- 项目执行计划生成器

它应该是：

```text
goal-oriented strategic paper blueprint skill
```

也就是说，它把用户的 research idea 转化为一组论文目标，并从这些目标推导出后续规划需要遵守的战略信息：

- target venue posture
- top-level paper goal
- central research bet
- contribution goal
- claim posture
- novelty posture
- evidence posture
- narrative posture
- visual argument posture
- scope boundary
- strategic risks
- downstream planning interfaces

这个 skill 的核心价值是为后续专项 planning skills 提供稳定上游接口。后续可以继续运行：

- content-planning skill
- experiment-planning skill
- figure-planning skill
- method-planning skill
- review-planning skill
- writing skill

因此，`paper-blueprint` 不应提前替这些 skill 做战术决策。它只定义论文战略核心和下游约束。

## 2. 总体设计逻辑

这个 skill 背后的核心链条是：

```text
research idea
→ user-confirmed context
→ paper goals
→ goal dependencies
→ strategic claim posture
→ novelty posture
→ evidence posture
→ narrative / visual posture
→ strategic risks
→ downstream planning interfaces
```

它不应该变成：

```text
research idea
→ full paper outline
→ experiment matrix
→ figure storyboard
→ implementation tasks
→ writing task list
```

判断粒度的总原则是：

```text
如果一个细节改变后不会改变论文的顶层目标、venue posture、主贡献、主 claim、新颖性边界或证据姿态，它就不应该在 paper-blueprint 阶段定死。
```

例如：

| 事项 | 是否属于 paper-blueprint | 应该如何表达 |
|---|---|---|
| 论文顶层目标 | 是 | top-level paper goal |
| 主贡献目标 | 是 | contribution goal |
| 主 claim 姿态 | 是 | strategic claim posture |
| 需要哪类证据 | 是 | evidence posture |
| 具体实验矩阵 | 否 | delegated to experiment-planning |
| 具体 baseline 实现 | 否 | comparison posture / baseline class |
| 具体 metric 公式 | 否 | outcome family |
| 具体图表数量和 layout | 否 | visual argument requirement |
| 具体 Introduction 段落结构 | 否 | narrative requirement |
| 具体算法族选择 | 通常否 | method abstraction / acceptable design space |

## 3. 两个输出文件

这个 skill 必须输出两个 Markdown 文件。

### 3.1 `paper_blueprint.md`

`paper_blueprint.md` 是英文正式论文战略蓝图。

它面向后续 AI planning skills，而不是面向用户解释。

它应当：

- 只包含论文战略规格
- 使用英文
- 定义论文目标和目标分解
- 定义 claim / novelty / evidence / narrative / visual / risk posture
- 定义后续 planning skill 的接口和约束
- 保持 objective strategic specification 风格

它不应承载：

- 用户语言解释
- skill 工作流说明
- 工具调用日志
- deepresearch / MCP 运行过程
- 为什么输出两个文件
- 为什么蓝图采用某种格式
- 具体实验安排
- 具体图表安排
- 具体章节安排
- 具体算法、baseline、metric、dataset 选择
- `用户已明确的信息` section

### 3.2 `paper_blueprint_explanation.<lang>.md`

`paper_blueprint_explanation.<lang>.md` 是用户语言的蓝图审核说明。

它面向人类用户，核心功能不是“解释 skill 怎么工作”，而是帮助用户确认 `paper_blueprint.md` 是否合理。

它应当：

- 使用用户对话语言
- 开头记录用户已明确的信息
- 概括蓝图重点内容
- 解释每个目标背后的思想
- 说明每个安排如何从目标推导出来
- 说明目标之间如何相互支撑
- 帮助用户判断不合理之处来自哪里
- 只保留未被用户确认内容覆盖的战略确认问题

它不应变成：

- skill 运行说明
- 文件格式说明
- downstream agent 使用说明
- deepresearch 过程报告
- 项目 TODO 清单
- 战术选项问卷

## 4. `paper_blueprint.md` 推荐结构

正式蓝图应围绕目标组织。

推荐结构如下：

```markdown
# Goal-Oriented Strategic Paper Blueprint: <Working Title>

## 1. Paper Identity

### 1.1 Research idea

### 1.2 Target venue posture

### 1.3 Paper type

### 1.4 Research object

### 1.5 Current input state

## 2. Top-Level Paper Goal

### 2.1 Acceptance goal

### 2.2 Central research bet

### 2.3 Strategic success condition

### 2.4 Strategic downgrade condition

## 3. Goal Decomposition

### 3.1 Positioning goal: <descriptive goal>

### 3.2 Problem-framing goal: <descriptive goal>

### 3.3 Contribution goal: <descriptive goal>

### 3.4 Novelty-boundary goal: <descriptive goal>

### 3.5 Evidence goal: <descriptive goal>

### 3.6 Communication goal: <descriptive goal>

### 3.7 Scope-control goal: <descriptive goal>

### 3.8 Downstream-planning goal: <descriptive goal>

## 4. Goal Cards

For each major goal, write:

- goal statement
- why this goal matters
- strategic role
- success condition
- derived constraints
- delegated details
- failure or revision implication

## 5. Goal Dependency Map

Explain:

- goals that support the top-level acceptance goal
- goals that protect the main contribution
- goals that protect the novelty boundary
- goals that determine evidence posture
- goals that determine narrative and visual posture
- goals that downstream planning skills must operationalize
- goals that are currently most fragile

## 6. Strategic Claim Posture

### 6.1 Claim implied by the acceptance goal

### 6.2 Claim implied by the contribution goal

### 6.3 Claim implied by the evidence goal

### 6.4 Claims deferred by the scope-control goal

## 7. Strategic Evidence Posture

### 7.1 Evidence required to satisfy the top-level paper goal

### 7.2 Evidence required to satisfy the contribution goal

### 7.3 Evidence required to satisfy the novelty-boundary goal

### 7.4 Evidence delegated to experiment-planning

## 8. Strategic Communication Posture

### 8.1 Reader belief that must be established first

### 8.2 Central abstraction that must become clear

### 8.3 Story movement from problem to contribution

### 8.4 Visual argument requirements delegated to figure-planning

### 8.5 Content sequencing delegated to content-planning

## 9. Strategic Risks

### 9.1 Goal most likely to fail

### 9.2 Goal most likely to be challenged by reviewers

### 9.3 Goal most dependent on missing evidence

### 9.4 How the blueprint changes if each fragile goal fails

## 10. Delegation Interfaces for Downstream Skills

### 10.1 Content-planning interface

### 10.2 Experiment-planning interface

### 10.3 Figure-planning interface

### 10.4 Method-planning interface

### 10.5 Review-planning interface
```

## 5. Goal Card 是核心输出单元

每个目标应使用 goal card，而不是普通 bullet list。

推荐格式：

```markdown
### <Goal type>: <descriptive goal title>

**Goal statement.**  
State what the paper must achieve.

**Why this goal matters.**  
Explain the strategic reason this goal is necessary.

**Strategic role.**  
State whether the goal supports acceptance, positioning, contribution, novelty, evidence, scope, communication, or downstream planning.

**Success condition.**  
State what must be true for this goal to be considered satisfied.

**Derived constraints.**  
State what this goal constrains in claims, evidence, narrative, method abstraction, scope, or downstream planning.

**Delegated details.**  
State what later skills should decide.

**Failure or revision implication.**  
State how the paper strategy changes if this goal fails.
```

Goal Card 的作用是让后续 skill 明确知道：

- 这个目标是什么
- 为什么这个目标重要
- 它约束哪些后续规划
- 哪些细节仍然有自由度
- 如果这个目标失败，整篇论文如何调整

## 6. 战略粒度控制

`paper-blueprint` 最容易跑偏的地方，是把战略蓝图写成轻量版实验规划、绘图规划或内容规划。

因此需要强制使用战略粒度。

当模型想输出战术细节时，应压缩成战略表述：

| 战术内容 | 蓝图层表达 |
|---|---|
| exact experiment matrix | evidence posture |
| exact baseline list | comparison posture |
| exact dataset / trace / workload | data or workload class |
| exact metric formula | outcome family |
| exact figure list | visual argument requirement |
| exact figure layout | delegated to figure-planning |
| exact section outline | narrative requirement |
| exact algorithm choice | method abstraction / acceptable design space |
| exact implementation steps | strategic risk / downstream planning interface |

例如不要写：

```text
Compare against CAGS, tuned CAGS, Gaussian-only ABR, BOLA, Pensieve, and oracle variants.
```

应写：

```text
The comparison posture must protect the novelty boundary by including credible fixed-reference, tuned base-system, Gaussian-only adaptation, related adaptation, and upper-bound comparison classes. Exact baseline implementations are delegated to experiment-planning.
```

不要写：

```text
Figure 1 should be a scheduling decision tree and Figure 2 should be a method overview.
```

应写：

```text
The visual argument must make the central abstraction and the evidence logic visible. Exact figure count, layout, and visual encoding are delegated to figure-planning.
```

## 7. `paper_blueprint_explanation.<lang>.md` 推荐结构

解释文件必须是用户可独立阅读的蓝图审核说明。

推荐结构：

```markdown
# Goal-Oriented Paper Blueprint Explanation: <Working Title>

## 0. 用户已明确的信息

记录用户已经明确表达的输入、约束、偏好和 pipeline 设定。  
这些内容用于过滤后面的待确认问题。

## 1. 蓝图速览：这篇论文试图达成什么

概括顶层论文目标、中心研究赌注、主贡献目标、证据目标和最大战略风险。

## 2. 核心目标组

逐个解释蓝图中的目标。每个目标先复述蓝图内容，再解释目标背后的思想、目标之间的联系，以及这个目标如何约束后续规划。

## 3. 从核心目标到论文蓝图的推导

解释目标如何生成 claim posture、novelty posture、evidence posture、narrative posture、risk posture 和 downstream planning interfaces。

## 4. 蓝图重点内容概括与解释

对重要蓝图项目采用：

- 蓝图内容概括
- 目标背后的思想
- 它如何生成蓝图安排
- 它和其他目标或安排的关系
- 用户审核点

## 5. 目标之间如何相互支撑

说明哪些目标支撑顶层 acceptance goal，哪些目标保护 novelty，哪些目标约束 evidence，哪些目标影响后续写作和绘图。

## 6. 当前最脆弱的目标链

写出：目标 → 派生判断 → 所需证据 → 可能失败点 → 如果失败如何改蓝图。

## 7. 用户仍需确认的战略问题

只列出未被“用户已明确的信息”覆盖、且会影响论文战略的少量问题。

## 8. 已委派给后续专项规划的问题

可选。只在必要时说明哪些问题属于内容编排、实验规划、绘图规划、方法规划或审稿规划。
```

## 8. 用户已明确的信息是 Confirmation Ledger

解释文件开头必须有：

```markdown
## 0. 用户已明确的信息
```

这个 section 只出现在解释文件中，不出现在正式蓝图中。

它不是普通摘要，而是 confirmation ledger。它记录用户已经明确表达的输入、约束、偏好和 pipeline 设定，并用于过滤后面的待确认问题。

它可以记录：

- research idea
- target venue / field preference
- existing materials
- output file requirements
- blueprint purpose
- downstream planning skill pipeline
- abstraction level
- explanation-file purpose
- language and readability preference
- content the user wants delegated to later planning
- user-confirmed strategic decisions

它不应记录：

- 模型推断
- deepresearch / deepsearch 检索结果
- 蓝图内部决策
- 工具调用过程
- generation logs
- skill 工作流解释

如果必须基于推断继续生成蓝图，应在后文作为 working assumption 处理，不应写进“用户已明确的信息”。

## 9. Confirmed Context Coverage Filter

解释文件中的“用户仍需确认的战略问题”必须先经过 confirmed context coverage filter。

流程：

```text
用户已明确的信息
→ 候选战略确认问题
→ 覆盖检查
→ 只输出剩余未确认的战略问题
```

候选问题分类：

| 分类 | 处理方式 |
|---|---|
| `covered_by_user_confirmation` | 用户已明确回答，不再输出 |
| `partially_covered` | 只问剩余未确认部分 |
| `conflicts_with_user_confirmation` | 修改蓝图或标记蓝图不一致，不作为问题输出 |
| `delegated_to_downstream_skill` | 转为 downstream planning boundary，不作为用户确认问题 |
| `unresolved_strategic_question` | 输出到“用户仍需确认的战略问题” |

这个机制的目标是让解释文件随迭代自然收敛：

```text
用户明确的信息越来越多
→ 待确认问题越来越少
```

除非用户改变论文方向、目标 venue、顶层目标或战略约束，否则不应反复询问已经确认过的内容。

## 10. 解释文件的写作风格

解释文件应自然、可读、面向用户。

推荐：

- 先复述蓝图内容，再解释为什么
- 用标题、近义词和自然语言指代蓝图项目
- 用“目标如何推导安排”作为主线
- 帮用户判断不合理之处来自哪个上游目标或推导链
- 保持 self-contained，不要求用户不断对照正式蓝图

不推荐：

- 密集 traceability table
- 人工编号链，例如 `C1/E1/F1/R1/A1/K1`
- 频繁使用 `第 5.1 节` / `Section 7.2` 作为主要指代方式
- 解释 skill 为什么这样输出
- 解释 deepresearch / MCP 调用过程
- 把“用户仍需确认的问题”写成战术问卷

自然写法示例：

```text
主 claim 要求论文同时证明画质收益和 deadline reliability。这个要求直接决定了后续 evidence posture：实验规划必须覆盖目标场景中的动态变化和实时性约束，图表规划也必须让画质收益和 deadline 可靠性处在同一条证据链上。
```

而不是：

```text
第 5.1 节影响第 8.2 节和第 9.3 节。
```

## 11. Recent Storytelling vs Technical Exemplars

这个 skill 需要用 live research 提取目标 venue 和相关领域的优秀模式，但不应在 skill 里保存固定论文知识库。

样例论文应分层使用：

### Storytelling Exemplars

用途：

- current reviewer-facing style
- Introduction framing
- Figure 1 / teaser pattern
- contribution framing
- evidence sequencing
- limitation style

规则：

- 必须偏新
- 优先最近 2-3 年或最近 3 个 target venue cycles
- 如果不足再扩展到最近 5 年并标记
- 不以 citation count 作为主要信号

### Technical Exemplars

用途：

- method lineage
- system / algorithm abstraction
- representation or protocol lineage
- required technical comparison

规则：

- 可以包含经典老论文
- 应结合 recent nearest-neighbor work
- citation count、adoption、baseline role 和 conceptual reuse 都可以作为信号

### Evaluation Exemplars

用途：

- dataset / workload / benchmark / metric norm
- ablation expectation
- robustness / scalability / artifact norm

规则：

- 可以包含经典 benchmark / dataset paper
- 当 evaluation norm 已变化时必须包含近期规范

这些 exemplar 的长篇分析应主要进入解释文件，用于说明目标和战略取舍。正式蓝图只保留战略结论。

## 12. Live Research Tool

这个 skill 应明确指定 live research 工具，避免误用系统中其他 MCP 或搜索工具。

工具身份：

```text
server: academic_army_mcp_tools
tool: deepresearch
canonical Codex MCP tool name: mcp__academic_army_mcp_tools__deepresearch
```

skill 中应明确写：

```text
Use academic_army_mcp_tools.deepresearch for live venue, literature, exemplar, and reviewer-context evidence.
```

用途：

- venue expectations
- recent storytelling exemplars
- technical exemplars
- evaluation exemplars
- closest related work
- reviewer-context pressure

最终输出文件不写工具调用日志。若工具不可用，应把影响转化为论文层面的 evidence gap 或 verification need，而不是输出 rate limit、MCP failure、web search logs。

## 13. Positive Contract Style

这个 skill 应尽量使用正向产物契约，而不是堆反向限制。

推荐写法：

```text
The blueprint contains...
The explanation contains...
Represent uncertainty as...
Represent tactical detail as delegated planning space...
Represent reviewer pressure as strategic risk...
Represent storytelling evidence as communication goals...
```

少用：

```text
Do not...
Avoid...
Never...
```

原因是过多反向限制容易激活 defensive output、meta-discourse leakage 和免责声明式写法。正向契约更容易让生成结果像目标文档本身。

## 14. Frontmatter Description 建议

`SKILL.md` 的 description 很重要，因为 Codex 会先看 description 决定是否触发 skill。

建议 description：

```yaml
description: Create two Markdown files for a goal-oriented strategic research-paper blueprint: an English paper_blueprint.md and a user-language paper_blueprint_explanation.<lang>.md. Use the required MCP tool academic_army_mcp_tools.deepresearch for live venue, literature, exemplar-paper, and reviewer-expectation research. The blueprint converts a research idea into paper goals and derives strategic claim posture, novelty posture, evidence posture, narrative posture, scope boundaries, strategic risks, and downstream planning interfaces. It delegates tactical experiment, figure, algorithm, baseline, metric, and manuscript-section planning to later specialized skills.
```

## 15. 可直接交给 Skill 编写 Agent 的 Prompt

下面这段可以直接交给编写 skill 的 agent 使用。

```text
请编写或重构一个 Codex skill，名称为 academic-army-architect 或 paper-blueprint。这个 skill 用于一套基于 Codex 的 autoresearch pipeline。它不是论文写作器、实验规划器、绘图规划器或章节编排器，而是一个 goal-oriented strategic paper blueprint skill。

这个 skill 的职责是：把用户的 research idea 转化为论文目标，并从这些目标推导出 claim posture、novelty posture、evidence posture、narrative posture、risk posture 和 downstream planning interfaces。

它应该确定论文战略层面能确定的内容，并把具体实验、具体图表、具体 baseline、具体算法、具体章节结构、具体写作文本留给后续专项 skill，例如 content-planning、experiment-planning、figure-planning、method-planning、review-planning 和 writing skills。

必须输出两个 Markdown 文件：

1. paper_blueprint.md
   - 英文。
   - 只包含正式目标导向战略论文蓝图。
   - 面向后续 AI planning skills。
   - 围绕 paper goals、goal decomposition、claim posture、novelty posture、evidence posture、narrative posture、risk posture 和 downstream planning interfaces 组织。
   - 不包含用户语言解释。
   - 不包含“用户已明确的信息”section。
   - 不提前固定具体实验、具体图表、具体 baseline、具体算法、具体 metric、具体数据集或具体章节结构。

2. paper_blueprint_explanation.<lang>.md
   - 使用用户对话语言。
   - 是用户审核 paper_blueprint.md 是否合理的 validation companion。
   - 开头必须包含“用户已明确的信息”或该语言下的自然等价标题。
   - 先复述蓝图重点内容，再解释这些内容如何从论文目标推导出来。
   - 说明目标之间如何相互支撑。
   - 说明每个安排服务哪个目标，约束哪些后续规划。
   - 说明如果某个安排不合理，用户应检查哪个上游目标、推导链或战略前提。
   - 使用标题、近义词和自然语言指代蓝图项目，不依赖 C1/E1/F1/R1/K1 这类人工编号，也不频繁使用 section number 跳转。
   - 不解释 skill 流程、不解释为什么输出两个文件、不输出工具调用日志。

paper_blueprint.md 推荐结构：

# Goal-Oriented Strategic Paper Blueprint: <Working Title>

## 1. Paper Identity
### 1.1 Research idea
### 1.2 Target venue posture
### 1.3 Paper type
### 1.4 Research object
### 1.5 Current input state

## 2. Top-Level Paper Goal
### 2.1 Acceptance goal
### 2.2 Central research bet
### 2.3 Strategic success condition
### 2.4 Strategic downgrade condition

## 3. Goal Decomposition
### 3.1 Positioning goal: <descriptive goal>
### 3.2 Problem-framing goal: <descriptive goal>
### 3.3 Contribution goal: <descriptive goal>
### 3.4 Novelty-boundary goal: <descriptive goal>
### 3.5 Evidence goal: <descriptive goal>
### 3.6 Communication goal: <descriptive goal>
### 3.7 Scope-control goal: <descriptive goal>
### 3.8 Downstream-planning goal: <descriptive goal>

## 4. Goal Cards
For each major goal, include goal statement, why this goal matters, strategic role, success condition, derived constraints, delegated details, and failure or revision implication.

## 5. Goal Dependency Map
Explain how goals support the top-level acceptance goal, protect the main contribution, protect novelty, determine evidence posture, determine narrative/visual posture, constrain downstream skills, and reveal fragile goals.

## 6. Strategic Claim Posture
Explain claims implied by the acceptance goal, contribution goal, evidence goal, and scope-control goal.

## 7. Strategic Evidence Posture
Explain evidence required to satisfy the top-level paper goal, contribution goal, novelty-boundary goal, and evidence delegated to experiment-planning.

## 8. Strategic Communication Posture
Explain reader belief, central abstraction, story movement, visual argument requirements, and content sequencing requirements.

## 9. Strategic Risks
Explain fragile goals, reviewer-challenged goals, evidence-dependent goals, and how the blueprint changes if each fragile goal fails.

## 10. Delegation Interfaces for Downstream Skills
Define interfaces for content-planning, experiment-planning, figure-planning, method-planning, and review-planning.

Goal Card format:

### <Goal type>: <descriptive goal title>

**Goal statement.**
**Why this goal matters.**
**Strategic role.**
**Success condition.**
**Derived constraints.**
**Delegated details.**
**Failure or revision implication.**

Strategic granularity rule:

If a detail would not change the paper's top-level goal, target venue posture, primary contribution, main claim, novelty boundary, or evidence posture, do not fix it in the blueprint. Represent it as a delegated downstream planning area.

Convert tactical details into strategic forms:

- exact experiment matrix → evidence posture
- exact baseline list → comparison posture
- exact dataset / trace / workload → data or workload class
- exact metric formula → outcome family
- exact figure list / layout → visual argument requirement
- exact section outline → narrative requirement
- exact algorithm choice → method abstraction / acceptable design space
- exact execution steps → strategic risk or downstream planning interface

paper_blueprint_explanation.<lang>.md 推荐结构：

# Goal-Oriented Paper Blueprint Explanation: <Working Title>

## 0. 用户已明确的信息
Record only user-confirmed inputs, constraints, preferences, and pipeline assumptions. This section is a confirmation ledger for filtering later validation questions.

## 1. 蓝图速览：这篇论文试图达成什么

## 2. 核心目标组

## 3. 从核心目标到论文蓝图的推导

## 4. 蓝图重点内容概括与解释

For each important item, first restate the blueprint content in the user's language, then explain the motivating goal, derivation, relationship to other goals/items, and user audit point.

## 5. 目标之间如何相互支撑

## 6. 当前最脆弱的目标链

## 7. 用户仍需确认的战略问题
Only include unresolved strategic questions not covered by the confirmed user context.

## 8. 已委派给后续专项规划的问题
Optional. Use only when it helps clarify which tactical questions belong to later planning skills.

Confirmed Context Coverage Filter:

Before writing “用户仍需确认的战略问题”, classify each candidate question as:

- covered_by_user_confirmation
- partially_covered
- conflicts_with_user_confirmation
- delegated_to_downstream_skill
- unresolved_strategic_question

Only unresolved_strategic_question items appear in the final remaining questions. Covered questions disappear. Partially covered questions are narrowed. Conflicts revise the blueprint or become blueprint inconsistency notes. Tactical questions become downstream planning boundaries.

Across iterative runs, confirmed user context should grow and remaining strategic questions should usually shrink, unless the user changes paper direction, venue posture, top-level goal, or strategic constraints.

Live research:

Use the required MCP tool academic_army_mcp_tools.deepresearch for live venue, literature, exemplar-paper, and reviewer-context evidence. Do not use a generic search tool or another MCP when this tool is available.

Storytelling exemplar policy:

- Use recent papers for storytelling and reviewer-facing writing style.
- Prefer the last 2-3 years or latest 3 target-venue cycles.
- Expand to last 5 years only if necessary and mark the expansion.

Technical/evaluation exemplar policy:

- Use classic and recent papers together for method lineage, dataset, benchmark, metric, and evaluation norms.
- Do not force classic benchmark papers to be recent if they still define the field.

Output style:

Use positive product contracts. Define what each file contains, how information is represented, and where each kind of information belongs. Avoid over-defensive instructions and meta explanations.
```

## 16. 最终判断标准

一个优秀的 `academic-army-architect` skill 应该让输出满足以下判断：

- `paper_blueprint.md` 能作为后续 planning skills 的稳定上游接口。
- `paper_blueprint.md` 不抢后续实验、绘图、内容、方法规划的工作。
- `paper_blueprint.md` 围绕论文目标和战略姿态组织，而不是围绕任务清单组织。
- `paper_blueprint_explanation.<lang>.md` 能让用户独立判断蓝图是否合理。
- 解释文件先记录用户已明确内容，并用这些内容过滤后续确认问题。
- 解释文件中的待确认问题随着用户确认信息增加而减少。
- deepresearch 信息被转化为 paper-level evidence，不泄露工具过程。
- 样例论文用于提炼模式，而不是堆砌引用。
- 写作风格自然、目标导向、战略层清晰，不 defensive。

一句话总结：

```text
这个 skill 的核心不是“生成论文大纲”，而是把 research idea 变成一组可审核、可追踪、可被后续专项 skill 消费的论文战略目标。
```
