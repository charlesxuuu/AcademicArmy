# Academic Army Architect Skill 写作经验与设计说明

这份文档总结 `academic-army-architect` / `paper-blueprint` skill 的设计经验。它可以作为 prompt 交给负责写 skill 的 agent，用来从零设计或继续完善一个目标导向的论文战略蓝图 skill。

## 1. 用户真正需要的 skill

用户需要的不是普通“论文大纲生成器”，也不是“实验规划器”“绘图规划器”或“论文内容编排器”。

用户需要的是一个：

> 目标导向的论文战略蓝图生成 skill。

这个 skill 的核心任务是：

1. 接收一个 research idea、草稿、代码、实验结果、目标 venue 或候选 venue。
2. 使用指定的 live research MCP 工具获取当前 venue、相关工作、近期写作风格、技术/评估 exemplar 和 reviewer expectation。
3. 把 research idea 分解成论文层面的战略目标。
4. 从这些目标推导出 claim posture、novelty posture、evidence posture、narrative posture、visual posture、scope boundary、strategic risks 和 downstream planning interfaces。
5. 生成两个 Markdown 文件：
   - `paper_blueprint.md`
   - `paper_blueprint_explanation.<lang>.md`

一句话定义：

> `academic-army-architect` 是一个 goal-oriented strategic paper blueprint skill。它把 research idea 转化为论文目标体系和后续专项规划的战略接口，而不是提前决定具体实验、图表、算法、baseline 或章节安排。

## 2. 两个输出文件的职责

### 2.1 `paper_blueprint.md`

`paper_blueprint.md` 是英文文件，面向后续 AI planning skills。

它应该是：

- Strategic Paper Blueprint
- Core Paper Specification
- downstream planning interface
- goal-oriented paper strategy contract

它应该定义：

- paper identity
- top-level paper goal
- central research bet
- goal decomposition
- contribution goals
- claim posture
- novelty posture
- evidence posture
- communication / visual posture
- scope boundaries
- strategic risks
- delegation boundaries for downstream skills

它不应该承担：

- 具体实验矩阵规划
- 具体 baseline 选择
- 具体 dataset / trace / workload 选择
- 具体 metric 公式设计
- 具体图表数量、layout、caption 设计
- 具体章节顺序或段落结构
- 具体算法路线选择
- 具体执行步骤、脚本、run order
- 面向用户的解释、提醒或建议

判断粒度的原则：

> 如果某项内容改变后会改变论文定位、主贡献、核心 claim、novelty boundary 或 evidence posture，它属于蓝图。  
> 如果某项内容只是“怎么具体实现这个战略”，它应该交给后续专项 planning skill。

### 2.2 `paper_blueprint_explanation.<lang>.md`

`paper_blueprint_explanation.<lang>.md` 使用用户对话语言，面向用户。

它不是普通摘要，也不是 skill 运行说明。它是：

> 用户审核论文蓝图是否合理的 validation companion。

它需要帮助用户回答：

- skill 是否正确理解了用户已经明确的信息？
- 这份论文蓝图的核心目标是什么？
- 每个目标为什么存在？
- 每个蓝图安排如何从这些目标推导出来？
- 目标之间如何相互支撑？
- 如果用户觉得某个安排不合理，应该检查哪个上游目标、哪个推导环节，还是某个后续战术细节？

解释文件必须先让用户看到“它正在解释什么”，再解释“为什么”。

每个重要项目的解释模式应是：

```text
蓝图内容概括
→ 目标背后的思想
→ 它如何服务顶层论文目标
→ 它如何牵引其他目标或安排
→ 用户审核点
```

解释文件开头必须包含：

```markdown
## 0. 用户已明确的信息
```

这一节只记录用户显式提供的输入、约束、偏好和 pipeline 设定。它不记录模型推断、不记录 deepsearch 发现、不记录蓝图决策、不记录工具过程。正式蓝图 `paper_blueprint.md` 不加这一节。

## 3. Skill 背后的设计逻辑

这个 skill 的逻辑可以概括为：

```text
research idea
→ user-confirmed context
→ academic_army_mcp_tools.deepsearch live evidence
→ top-level paper goal
→ goal decomposition
→ goal dependency map
→ strategic claim posture
→ novelty posture
→ evidence posture
→ narrative / visual posture
→ strategic risks
→ downstream planning interfaces
→ user-language validation explanation
```

它背后的几个关键转变：

1. 从“论文大纲生成”转向“论文战略规格生成”。
2. 从“实验、图表、章节都提前规划”转向“定义后续 planning skill 必须满足的目标和约束”。
3. 从“蓝图解释是说明文字”转向“蓝图解释是用户审核界面”。
4. 从“高引论文模式分析”转向“按用途分层使用 exemplar”：近期论文分析 storytelling，经典和近期论文分析技术与评估 lineage。
5. 从“反向禁止清单驱动”转向“正向产物契约驱动”。
6. 从“编号式追踪”转向“语义锚点 + 自包含解释”。
7. 从“泛称 deepresearch”转向“精确指定 `academic_army_mcp_tools.deepsearch`”。

## 4. Live research 工具身份

skill 必须明确使用唯一 live research MCP 工具：

```text
academic_army_mcp_tools.deepsearch
```

在 `SKILL.md` 中应写清楚：

```markdown
## Required Research MCP

This skill's live research dependency is the `deepsearch` tool from the `academic_army_mcp_tools` MCP server.

Use the exact tool identity:

- server: `academic_army_mcp_tools`
- tool: `deepsearch`
- canonical Codex MCP tool name, when exposed: `mcp__academic_army_mcp_tools__deepsearch`

All mentions of `deepsearch` in this skill refer to `academic_army_mcp_tools.deepsearch`.

Use `academic_army_mcp_tools.deepsearch` for current venue evidence, related-work evidence, exemplar-paper evidence, evaluation-expectation evidence, and reviewer-context evidence.

Evidence from built-in web search, browser tools, documentation search, or other MCP servers is supplemental and does not satisfy this skill's required live research dependency.

The final Markdown files should contain the paper-level conclusions derived from this evidence, not tool-call logs or MCP implementation details.
```

这样可以避免系统内同时存在多个 MCP、内置 web search 或文档搜索工具时误用工具。

## 5. Exemplar evidence 策略

skill 不应该把所有论文样例都混成“高引论文”。应该明确分成三类。

### 5.1 Storytelling exemplars

用途：

- 分析当前目标 venue 或相邻 venue 的写作风格。
- 分析 introduction、problem framing、contribution framing、Figure 1、evidence sequencing、limitation style。

规则：

- 必须偏新。
- 优先最近 2-3 年或最近 3 个会议周期。
- 如果样例不足，可以扩展到最近 5 年并标记原因。
- 不以 citation count 作为主要信号，因为近期论文引用还没积累起来。

### 5.2 Technical exemplars

用途：

- 分析 method lineage、system abstraction、algorithmic pattern、representation、protocol。

规则：

- 可以包含经典高影响论文。
- 也应包含近期 nearest-neighbor work，尤其当 novelty risk 较高时。
- citation、adoption、baseline usage 和 conceptual reuse 都是有效信号。

### 5.3 Evaluation exemplars

用途：

- 分析 datasets、benchmarks、workloads、metrics、ablation、artifact expectation。

规则：

- 标准 dataset / benchmark 论文可以较老。
- 如果评估规范已经变化，必须补近期 evaluation norms。
- 输出应转化为 evidence posture，而不是具体实验计划。

## 6. Strategic abstraction level

skill 必须停在战略层。

推荐写入 `SKILL.md`：

```markdown
## Strategic Abstraction Level

The paper blueprint is a strategic core specification.

It operates at:

- Level 0: Paper identity
- Level 1: Paper strategy
- Level 2: Planning constraints

The paper blueprint stops at Level 2.

Later specialized skills handle:

- Level 3: Tactical planning
- Level 4: Execution planning
```

战略层可以定义：

- paper goal
- contribution goal
- claim posture
- novelty posture
- evidence posture
- comparison posture
- narrative posture
- visual argument requirement
- scope boundary
- strategic risk
- delegation boundary

战术层交给后续 skill：

- exact experiments
- exact datasets, traces, workloads
- exact baselines
- exact metrics
- exact figure list and layout
- exact manuscript section structure
- exact algorithm variants
- scripts and run order

当模型想输出战术细节时，应压缩成战略形式：

| Tactical impulse | Strategic form |
|---|---|
| Choose an algorithm family | Recommended method posture plus change condition |
| List exact baselines | Comparison posture and credible comparison classes |
| Pick datasets or traces | Data/workload posture and target setting |
| Specify metric formulas | Outcome family and evidence standard |
| Design figures | Visual argument requirement |
| Outline sections | Narrative requirement |
| Create task sequence | Strategic research priority or decision-critical uncertainty |

## 7. `paper_blueprint.md` 推荐结构

推荐把正式蓝图写成目标导向结构：

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

For each major goal:

### <Goal type>: <descriptive goal title>

**Goal statement.**  
...

**Why this goal matters.**  
...

**Strategic role.**  
...

**Success condition.**  
...

**Derived constraints.**  
...

**Delegated details.**  
...

**Failure implication.**  
...

## 5. Goal Dependency Map

## 6. Strategic Claim Posture

## 7. Strategic Evidence Posture

## 8. Strategic Communication and Visual Posture

## 9. Strategic Risks and Decision-Critical Uncertainties

## 10. Delegation Interfaces for Downstream Skills

### 10.1 Content-planning interface
### 10.2 Experiment-planning interface
### 10.3 Figure-planning interface
### 10.4 Method-planning interface
### 10.5 Review-planning interface
```

这份结构的关键不是标题本身，而是它表达的职责边界：

```text
定义目标和战略约束；
不替后续 skill 做具体规划。
```

## 8. Goal card 设计

每个 goal card 应回答：

```text
这个目标是什么？
为什么这个目标重要？
它在论文战略中扮演什么角色？
什么情况说明目标达成？
它约束哪些后续规划？
它留下哪些战术细节给后续 skill？
如果目标失败，论文战略如何调整？
```

典型目标类型：

- acceptance goal
- positioning goal
- problem-framing goal
- contribution goal
- novelty-boundary goal
- evidence goal
- communication goal
- scope-control goal
- downstream-planning goal

Goal card 是后续所有专项 skill 的接口。比如 experiment-planning 不应该重新判断论文目标，而应读取 evidence goal 和 claim posture；figure-planning 不应该重新发明叙事主线，而应读取 communication goal 和 visual argument requirement。

## 9. `paper_blueprint_explanation.<lang>.md` 推荐结构

```markdown
# Goal-Oriented Paper Blueprint Explanation: <Working Title>

## 0. 用户已明确的信息

只记录用户显式表达的信息，包括 research idea、目标 venue 或领域、后续 pipeline、蓝图用途、抽象层级、输出要求、解释文件功能、语言和可读性偏好。不要放模型推断、deepsearch 发现、蓝图决策或生成过程。

## 1. 蓝图速览：这篇论文试图达成什么

概括顶层论文目标、中心研究赌注、主贡献目标、证据目标和最大战略风险。

## 2. 核心目标组

逐个解释蓝图中的目标。每个目标先复述蓝图内容，再解释目标背后的思想、目标之间的联系，以及这个目标如何约束后续规划。

## 3. 从核心目标到论文蓝图的推导

解释目标如何生成 claim posture、novelty posture、evidence posture、narrative posture、risk posture 和 downstream planning interfaces。

## 4. 蓝图重点内容概括与解释

先概括蓝图重点内容，再解释它如何服务论文目标。

## 5. 目标之间如何相互支撑

说明哪些目标支撑顶层 acceptance goal，哪些目标保护 novelty，哪些目标约束 evidence，哪些目标影响后续写作和绘图。

## 6. 当前最脆弱的目标链

列出最可能出错的目标链：目标 → 派生判断 → 所需证据 → 如果失败如何改蓝图。

## 7. 用户最应该确认的战略问题

列出少量用户应优先判断的问题，帮助确认蓝图战略是否合理。
```

解释文件写作原则：

1. 先复述，再解释。
2. 用用户语言写。
3. 使用语义锚点，不依赖人工编号或章节编号。
4. 解释论文方案，不解释 skill 机制。
5. 帮助用户定位 disagreement 的来源：目标错、推导弱、还是战术细节待后续规划。

## 10. 语义锚点，而不是编号索引

不要让解释文件主要依赖：

```text
C1 / E1 / F1 / R1
Section 5.1 / Section 8.3
第 5.1 节 / 第 8.2 节
```

使用语义锚点：

```text
主贡献目标
acceptance-critical claim
evidence goal for the primary effect
novelty-boundary goal
reference-versus-Gaussian tradeoff
baseline fairness risk
visual argument requirement
experiment-planning boundary
```

自然写法示例：

```text
主 claim 要求论文同时证明画质收益和 deadline reliability。这个要求直接决定了证据目标必须覆盖动态网络、视角误差和 client compute，也决定了后续实验规划不能只看 PSNR/SSIM/LPIPS。
```

而不是：

```text
第 5.1 节影响第 8.2 节和第 9.3 节。
```

## 11. 正向产物契约，减少 defensive 文风

skill 不应该主要依靠大量反向限制，比如：

```text
Do not...
Avoid...
Banned phrases...
```

更好的写法是定义：

```text
这个文件是什么；
这个 section 应包含什么；
某类信息应如何投影；
不确定性应如何表达；
战术细节应如何 delegation；
用户应如何审核。
```

推荐加入：

```markdown
## Paper-goal projection

Convert intermediate analysis into paper-goal objects:

- venue expectations become positioning and acceptance goals
- storytelling patterns become communication goals
- technical lineage becomes contribution and novelty-boundary goals
- evaluation norms become evidence goals
- reviewer concerns become strategic risks
- uncertain items become decision-critical uncertainties
- tactical choices become delegation boundaries
```

这比堆一长串 banned phrases 更稳定，也更不容易产生 meta-discourse leakage。

## 12. 解释文件不输出的内容类型

解释文件的对象是论文方案，不是 skill。

它不应该输出：

- 为什么有两个文件
- 为什么正式蓝图采用某种格式
- 为什么这是 AI-facing
- downstream agent 怎么用文件
- deepsearch 工具调用过程
- MCP、web search、rate limit、probe、PDF parsing
- output directory
- 生成过程、prompt 过程、内部 reasoning
- skill 工作流解释

它应该输出：

- 为什么论文要这样定位
- 为什么这些目标重要
- 为什么这些目标推导出当前 claim posture
- 为什么 novelty boundary 这样画
- 为什么 evidence posture 足以支持目标 venue
- 为什么 scope boundary 能保护论文可信度
- 为什么某些战术细节留给后续 skill

## 13. 给写 skill 的 agent 的完整 prompt

下面这段可以直接交给负责写 skill 的 agent。

```text
请编写或完善一个 Codex skill，名称为 academic-army-architect。这个 skill 用于 autoresearch 工具链中的论文战略蓝图生成。

这个 skill 不是论文大纲生成器、实验规划器、绘图规划器或论文内容编排器。它是一个目标导向的论文战略蓝图 skill。

它的任务是：接收一个 research idea、草稿、代码、实验结果、目标 venue 或候选 venue，通过 academic_army_mcp_tools.deepsearch 获取当前 venue、相关工作、近期 storytelling exemplars、技术和评估 exemplars、reviewer expectation，然后把 idea 分解为论文层面的战略目标，并从这些目标推导出 claim posture、novelty posture、evidence posture、narrative posture、visual posture、scope boundary、strategic risks 和 downstream planning interfaces。

必须输出两个 Markdown 文件：

1. paper_blueprint.md
   - 英文。
   - 面向后续 AI planning skills。
   - 是 Goal-Oriented Strategic Paper Blueprint。
   - 只描述论文战略核心、目标分解、目标依赖、claim posture、evidence posture、novelty posture、communication posture、scope boundary、strategic risks 和 downstream planning interfaces。
   - 不具体决定实验矩阵、baseline 实现、dataset、trace、metric 公式、figure layout、章节结构、算法路线或执行步骤。

2. paper_blueprint_explanation.<lang>.md
   - 使用用户对话语言。
   - 面向用户审核蓝图是否合理。
   - 开头必须有“用户已明确的信息”或对应语言自然标题。
   - 该开头只记录用户显式提供的 research idea、目标 venue 或领域、后续 pipeline、蓝图用途、抽象层级、输出要求、解释文件功能、语言和可读性偏好。
   - 解释文件应先概括蓝图重点内容，再解释每个目标背后的思想、目标之间的联系，以及蓝图安排如何帮助论文达成目标。
   - 每个重要项目应采用：蓝图内容概括 → 目标背后的思想 → 它如何服务顶层论文目标 → 它如何牵引其他目标或安排 → 用户审核点。
   - 解释文件不解释 skill、MCP、工具调用、生成过程、输出格式理由或 downstream agent 使用方式。

必须明确 live research 工具身份：

- server: academic_army_mcp_tools
- tool: deepsearch
- canonical Codex MCP tool name if exposed: mcp__academic_army_mcp_tools__deepsearch

所有 live venue、literature、exemplar、evaluation expectation、reviewer-context research 都使用 academic_army_mcp_tools.deepsearch。不要用泛称 deepresearch，也不要把内置 web search、browser tools、docs search 或其他 MCP 当作替代。

exemplar evidence 必须分层：

- storytelling_exemplars：用于分析当前 venue 写作风格，必须偏新，优先最近 2-3 年或最近 3 个会议周期。
- technical_exemplars：用于分析方法和系统谱系，可以包含经典论文和近期 nearest-neighbor work。
- evaluation_exemplars：用于分析 dataset、benchmark、workload、metric、ablation、artifact expectation，可以包含仍然标准的经典论文，但应补充近期 norm。

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

For each major goal, include:
- Goal statement
- Why this goal matters
- Strategic role
- Success condition
- Derived constraints
- Delegated details
- Failure implication

## 5. Goal Dependency Map
## 6. Strategic Claim Posture
## 7. Strategic Evidence Posture
## 8. Strategic Communication and Visual Posture
## 9. Strategic Risks and Decision-Critical Uncertainties
## 10. Delegation Interfaces for Downstream Skills

paper_blueprint_explanation.<lang>.md 推荐结构：

# Goal-Oriented Paper Blueprint Explanation: <Working Title>

## 0. 用户已明确的信息
## 1. 蓝图速览：这篇论文试图达成什么
## 2. 核心目标组
## 3. 从核心目标到论文蓝图的推导
## 4. 蓝图重点内容概括与解释
## 5. 目标之间如何相互支撑
## 6. 当前最脆弱的目标链
## 7. 用户最应该确认的战略问题

写 SKILL.md 时使用正向产物契约。重点定义 skill 应生成什么、每类信息应如何投影、两个文件分别承担什么职责、战术细节如何 delegation。减少大量 defensive 的反向禁止清单。

最终质量检查：

- paper_blueprint.md 是英文目标导向战略蓝图。
- paper_blueprint.md 不抢实验规划、绘图规划、内容编排规划、method planning 或 review planning 的工作。
- 每个重要安排都服务至少一个论文目标。
- 战术细节被表达为 delegation boundary、planning constraint 或 decision-critical uncertainty。
- explanation 文件开头记录用户已明确的信息。
- explanation 文件先复述蓝图重点内容，再解释原因。
- explanation 文件帮助用户判断 disagreement 来自目标、推导还是战术细节。
- explanation 文件使用语义锚点，不依赖 C1/E1/F1/R1 或频繁章节编号。
- explanation 文件不输出工具过程、skill 过程、MCP 日志、rate limit 或文件格式 rationale。
```

## 14. 最终质量检查清单

给 skill 编写 agent 的最终检查：

### `paper_blueprint.md`

- 文件是英文。
- 文件是目标导向的战略蓝图。
- 论文目标、目标分解、目标依赖清楚。
- claim posture 从目标推导出来。
- evidence posture 是战略证据姿态，不是具体实验计划。
- novelty posture 明确但不写成 related work 全文。
- narrative / visual posture 是战略要求，不是具体章节或图表清单。
- scope boundary 防止后续 skill 过度扩张 claim。
- delegation interfaces 明确后续 content、experiment、figure、method、review planning 的自由度和约束。
- 文件没有用户语言解释。
- 文件没有 skill 过程、工具日志或面向用户提醒。

### `paper_blueprint_explanation.<lang>.md`

- 文件使用用户语言。
- 开头有用户已明确的信息。
- 用户已明确的信息只包含用户显式说过的输入、约束、偏好和 pipeline 设定。
- 文件能独立阅读，不要求用户频繁对照正式蓝图。
- 每个重要项目先复述蓝图内容，再解释目标和推导。
- 解释围绕论文目标展开，而不是围绕 skill 格式展开。
- 使用语义锚点，不使用人工编号链。
- 用户能看出不合理之处应回溯到哪个目标、哪个推导或哪个后续战术规划。

## 15. 一句话总结

这个 skill 的关键经验是：

> 不要把 paper-blueprint 写成“论文大纲 + 实验计划 + 图表计划”的混合物，而要写成“目标导向的论文战略规格”。正式蓝图服务后续 AI planning skills，定义论文目标和规划约束；解释文件服务用户审核，说明每个目标为什么存在、如何相互支撑、以及蓝图安排如何从目标推导出来。动态知识用 `academic_army_mcp_tools.deepsearch` 获取，skill 本身只保存稳定的目标分解、证据投影和输出契约。
