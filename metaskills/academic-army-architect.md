# Academic Army Architect Metaskill: Paper Blueprint Skill Design Brief

这份文档总结 `academic-army-architect` / `paper-blueprint` skill 的设计经验，可直接作为 prompt 交给另一个编写 skill 的 agent，用来创建或重构一个高质量的论文蓝图 skill。

## 1. 目标需求

需要的 skill 不是普通论文大纲生成器，也不是自动写论文工具。它的任务是在正式写论文前，把一个研究 idea、草稿、代码库、实验结果、目标 venue 或相关材料，转化成一份可实施的论文方案，并生成一份供用户审核该方案是否合理的解释文件。

最终产物必须是两个 Markdown 文件：

```text
paper_blueprint.md
paper_blueprint_explanation.<lang>.md
```

其中：

- `paper_blueprint.md` 是英文论文蓝图，主要给后续 AI agent 使用。它是客观、结构化、可执行的论文方案规格。
- `paper_blueprint_explanation.<lang>.md` 使用用户对话语言，主要给用户审核蓝图是否合理。它是自包含的蓝图审核说明，不是普通摘要，也不是 skill 运行说明。

一句话定义：

```text
用 live research evidence 生成一份英文、AI 可执行的论文方案；
再用用户语言生成一份可独立阅读的蓝图审核说明，
让用户看懂每个蓝图细节如何从核心论文出发点推导出来，
并能判断哪里合理、哪里需要改。
```

## 2. 这个 Skill 背后的核心判断

优秀顶会论文通常不是简单展示一个方法或一个指标提升。它们通常具备以下特征：

1. 重新定义了社区正在卡住的问题，而不是只说“我们做了一个系统/模型”。
2. 有一个可传播、可复用的核心贡献，例如 abstraction、mechanism、benchmark framing、evaluation perspective、optimization formulation 或 representation。
3. 改变了一个关键 tradeoff，例如 quality vs latency、accuracy vs speed、scalability vs simplicity、bandwidth vs visual quality、deadline vs utility、generality vs specialization。
4. 每个强 claim 都绑定证据。算法论文需要 benchmark、baseline、ablation、failure analysis；系统论文需要 workload、prototype、scalability、failure behavior、deployment realism；图形或视觉论文需要视觉质量、速度、消融、定性结果和可复现性。
5. 相关工作不是综述堆砌，而是建立 novelty boundary：哪些必须引用，哪些必须比较，哪些差异不能夸大。
6. 图表不是结果堆叠，而是论文叙事的一部分。优秀论文通常能从 figure/table storyboard 反推出整体结构。
7. 论文要让审稿人快速判断：如果这篇论文成立，领域中的哪个抽象、方法、系统能力或评估方式会被改变。

因此，这个 skill 的核心逻辑是：

```text
live evidence + paper strategy premises
  -> implementable paper blueprint
  -> user-facing validation explanation
```

skill 本身不要存大量静态会议知识、论文案例、最新 SOTA、CFP 或 related work 数据库。动态信息应该通过 `deepresearch` MCP 现场获取。skill 应保存的是稳定工作流、输出契约、证据投影规则和质量标准。

## 3. DeepResearch MCP 的角色

系统已有 `deepresearch` MCP 工具，可以把 prompt 转发给 GPT-5.5 + web search。这个 skill 应把它作为 live evidence retriever，而不是让它直接写最终蓝图。

应使用 deepresearch 获取：

- 当前目标 venue 的 CFP、review criteria、author instructions、artifact/reproducibility expectations。
- 目标 venue 或相邻 venue 的近期强论文，用于分析当前 storytelling、Introduction、Figure 1、contribution framing、limitation style 和 evidence sequencing。
- 当前研究领域的经典与近期技术论文，用于分析 method lineage、datasets、benchmarks、baselines、metrics 和 evaluation norms。
- nearest-neighbor related work，用于判断 novelty boundary、required baselines 和 reviewer comparison points。
- 可能的 reviewer objections，用于设计 review-risk mitigation 和 evidence gaps。

deepresearch prompt 应要求返回 paper-relevant evidence，例如：

```text
1. Venue and storytelling evidence
2. Technical lineage evidence
3. Related-work boundary evidence
4. Evaluation and reviewer expectation evidence
```

deepresearch 的输出只是证据输入。skill 负责把证据编译成 `paper_blueprint.md` 和 `paper_blueprint_explanation.<lang>.md`。

## 4. Exemplar 论文的时效规则

不要把所有“高引论文”混成一个列表。不同用途的论文样例有不同筛选标准。

### 4.1 Storytelling Exemplars

用途：分析当前目标 venue 或相邻 venue 的叙事方式、写作风格、Introduction 结构、Figure 1 / teaser 设计、contribution framing、limitation 写法和 evidence sequencing。

时效要求：

- 优先最近 2-3 年，或目标 venue 最近 3 个 cycle。
- 如果不足，可以扩展到最近 5 年，并把它视为 evidence coverage limitation。
- 不主要依赖 citation count，因为近期论文尚未充分积累引用。

优先来源：

- target venue accepted papers
- best paper / honorable mention / oral / spotlight
- 近期被广泛讨论或频繁作为 framing/baseline 的论文
- 相邻 venue 中与当前任务非常接近的近期论文

### 4.2 Technical / Method / Dataset / Evaluation Exemplars

用途：分析技术谱系、方法边界、benchmark、dataset、metric、baseline、ablation 和 evaluation norm。

这类论文可以更老：

- foundational papers
- test-of-time papers
- 标准 benchmark/dataset 论文
- 长期作为 baseline 的论文
- 经典系统、算法、表示、优化或评估范式论文

如果当前领域的 evaluation norm 已经变化，也要加入近期 nearest-neighbor papers。

### 4.3 Nearest-Neighbor Exemplars

用途：判断当前工作的 novelty risk、baseline requirement 和 reviewer comparison point。

这类论文不一定最高引，但必须和当前研究 idea 最接近。

## 5. `paper_blueprint.md` 的设计

### 5.1 文件定位

`paper_blueprint.md` 是英文文件，主要给后续 AI agent 使用。它应该像一份可实施的论文方案规格，而不是面向用户的建议书、教程、反思记录或工具运行报告。

它应客观描述：

- 论文定位是什么
- 核心出发点是什么
- 主 thesis 是什么
- 贡献是什么
- claim 是什么
- 每个 claim 需要什么证据
- 相关工作边界在哪里
- 方法如何拆解
- 实验如何设计
- 图表如何服务故事
- 论文结构如何展开
- 审稿风险如何缓解
- artifact 和可复现材料需要哪些
- 哪些证据还缺
- 研究执行顺序是什么

### 5.2 内容投影规则

中间分析中的自然语言判断要投影成论文方案对象：

| 中间信息 | 蓝图中的落点 |
|---|---|
| venue expectations | scope and evidence standards |
| storytelling patterns | manuscript and figure specifications |
| technical lineage | method positioning and related-work differentiation |
| evaluation norms | datasets, workloads, baselines, metrics, ablations |
| uncertainty | evidence gaps and dependencies |
| reviewer concerns | review-risk mitigation plan |
| reproducibility expectations | artifact deliverables |
| missing experiments | evaluation specification or research execution steps |
| next steps | research execution plan |

例如：

- “数据集多样性还没验证”应写成 evidence gap / dependency。
- “审稿人可能认为 baseline 太弱”应写成 review-risk mitigation。
- “不要假设 reviewers 会跑代码”不应作为提醒出现；如果相关，就转成 reproducibility-relevant assets。

### 5.3 推荐结构

`paper_blueprint.md` 推荐结构：

```markdown
# Paper Blueprint: <Working Title>

## 1. Metadata and Input State

## 2. Paper Strategy Premises

### 2.1 Target-venue premise
### 2.2 Problem premise
### 2.3 Contribution premise
### 2.4 Novelty premise
### 2.5 Evidence premise
### 2.6 Storytelling premise
### 2.7 Execution premise

## 3. Venue and Scope Specification

## 4. Paper Thesis and Contribution Shape

## 5. Claim and Evidence Plan

## 6. Related-Work Differentiation Plan

## 7. Method Specification

## 8. Evaluation Specification

## 9. Figure and Table Specification

## 10. Manuscript Structure Specification

## 11. Review-Risk Mitigation Plan

## 12. Artifact and Reproducibility Specification

## 13. Evidence Gaps and Dependencies

## 14. Research Execution Plan
```

`Paper Strategy Premises` 是关键部分。它应客观写出论文方案的核心出发点，后续所有 claim、method、evaluation、figures、risks、evidence gaps 和 execution plan 都从这些 premises 推导出来。

### 5.4 标题与对象定位

正式蓝图可以使用 Markdown 自然章节编号，但不使用人工对象编号，例如：

```text
C1, C2
E1, E2
F1, F2
R1, R2
B1, B2
K1, K2
```

每个重要项目使用自解释的描述性标题。标题应同时说明项目角色和具体内容。

好标题示例：

```markdown
### 5.1 Primary claim: Reference-aware adaptation improves visible QoE under dynamic bandwidth and viewport uncertainty

### 8.2 Main-result experiment: Compare RefABR with CAGS, tuned CAGS, Gaussian-only ABR, fixed-reference strategies, and oracle variants under dynamic network traces

### 11.1 Risk: The improvement may look like CAGS parameter tuning rather than a new ABR abstraction

### 13.3 Evidence gap: The reference-versus-Gaussian utility crossover has not been measured
```

## 6. `paper_blueprint_explanation.<lang>.md` 的设计

### 6.1 文件定位

`paper_blueprint_explanation.<lang>.md` 使用用户对话语言。它的主要功能是帮助用户确认 `paper_blueprint.md` 中的项目是否合理。

它不是：

- 普通摘要
- 工具运行日志
- skill 工作流说明
- “为什么生成两个文件”的解释
- deepresearch / MCP 调用过程说明
- 下游 agent 使用说明

它是一个 self-contained validation companion。用户不应频繁打开 `paper_blueprint.md` 对照才能理解它。

### 6.2 核心写法：Digest + Rationale

解释文件对每个重要蓝图项目都应先复述内容，再解释来源和关系。

每个重要项目使用以下结构：

```text
蓝图内容概括
  -> 该项目在正式蓝图中具体写了什么

为什么这样设计
  -> 它从哪些核心出发点推导出来

它和其他部分的关系
  -> 它支持、约束或依赖哪些其他蓝图项目

用户审核点
  -> 如果用户觉得它不合理，应检查哪个上游 premise、推导环节或执行细节
```

示例：

```markdown
### 主 claim：reference-aware adaptation 同时改善可见质量和 deadline reliability

**蓝图内容概括。**  
蓝图把主 claim 写成：RefABR 在动态网络、视角预测误差和 client compute 约束下，通过联合调度 Gaussian enhancement layer 与 reference image，提升 visible quality，同时降低 deadline miss 和 motion-to-photon latency。

**为什么这样设计。**  
这条 claim 来自两个核心出发点：论文应被定位为 INFOCOM 风格的网络系统论文；reference image 在这里不是固定 restoration 辅助输入，而是一种有带宽、视角、deadline 和计算成本的 adaptive streaming object。因此主 claim 必须同时包含质量和实时性，不能只写成 PSNR/SSIM/LPIPS 提升。

**它和其他部分的关系。**  
这个主 claim 牵引主实验、主结果图、baseline 设计和主要审稿风险。主实验需要覆盖动态网络 trace、视角误差和 client compute；主结果图需要同时展示可见质量、deadline miss、latency 和 bandwidth utilization；baseline 风险则主要保护这条 claim，避免审稿人认为收益只是 CAGS 参数调优。

**用户审核点。**  
如果用户觉得这条主 claim 不合理，最应该检查的是目标 venue 判断和贡献判断：RefABR 是否确实应该作为 deadline-aware reference adaptation 的网络系统论文，而不是 CAGS 的 graphics/compression extension。
```

### 6.3 语义引用方式

解释文件应使用标题、译名、功能近义词来指代蓝图项目，而不是依赖章节号或人工编号。

优先使用：

- 主 claim
- 主实验
- 主结果图
- baseline 风险
- reference-versus-Gaussian utility sweep
- CAGS reproduction evidence gap
- per-frame instrumentation execution step
- opening scheduling-decision figure

可在第一次提到时引用正式蓝图标题，例如：

```text
主 claim（正式蓝图中标题为 “Primary claim: ...”）……
```

之后使用自然名称，例如：

```text
这个主 claim
reference-aware adaptation 这个判断
主实验
baseline 风险
```

### 6.4 推荐结构

`paper_blueprint_explanation.<lang>.md` 推荐结构：

```markdown
# Paper Blueprint Explanation: <Working Title>

## 1. 论文蓝图速览

用用户语言概括正式蓝图的论文定位、中心 thesis、主贡献、主 claim、方法方向、评估主线、主要风险、证据缺口和研究推进顺序。

## 2. 蓝图重点内容与审核入口

| 蓝图重点内容 | 为什么重要 | 用户主要审核点 |
|---|---|---|
| ... | ... | ... |

## 3. 核心出发点

解释 target venue 判断、problem framing 判断、contribution framing 判断、novelty boundary 判断、evidence standard 判断、storytelling strategy 判断和 execution strategy 判断。

## 4. 从核心出发点到论文方案的总体推导

用自然语言串起：目标 venue -> 论文类型 -> 中心 thesis -> 主 claims -> related-work boundary -> method -> evaluation -> figures -> risks -> evidence gaps -> research execution order。

## 5. 论文蓝图逐项解释

每个重要项目都要先复述蓝图内容，再解释为什么这样设计、它和其他部分的关系、用户应如何审核。

推荐覆盖：

- 论文定位与范围
- 中心 thesis 与贡献形态
- 主 claim
- 机制 claim
- 泛化或范围 claim
- 相关工作边界
- 方法设计
- 主实验
- 机制消融或 utility analysis
- 鲁棒性或压力测试
- 开场图与主结果图
- 论文结构
- 审稿风险
- 证据缺口
- 研究推进顺序

## 6. 关键设计取舍的推导

解释 venue 定位、贡献 framing、claim scope、baseline 选择、evaluation 顺序、figure strategy 和 evidence gaps 的关键取舍。

## 7. 当前最容易出错的推导链

每条写成：核心出发点 -> 蓝图设计 -> 所需证据 -> 可能失败点 -> 如果失败如何改蓝图。

## 8. 用户审核时最应该确认的问题

列出用户最需要判断的 paper-level questions。
```

## 7. 正向 Instruction 风格

这个 skill 应尽量使用正向产物契约，而不是过度 defensive 的禁止清单。

优先写：

- The blueprint contains ...
- The explanation contains ...
- Represent uncertainty as evidence gaps.
- Represent reviewer concerns as review-risk mitigation.
- Represent reproducibility expectations as artifact deliverables.
- Use semantic headings and natural prose.
- Explain each blueprint item as content digest + premise derivation + connection + validation point.

少写：

- Do not include ...
- Do not mention ...
- Avoid ...
- Banned phrases ...

必要边界可以保留，但整体控制方式应是“定义应该输出什么”，而不是“列出不能输出什么”。

## 8. 最终质量标准

### 8.1 `paper_blueprint.md`

应满足：

- 使用英文。
- 是 objective paper-plan specification。
- 包含 `Paper Strategy Premises`。
- 使用自然 Markdown 章节编号和描述性标题。
- 不使用人工对象编号。
- 每个重要 claim 都有 required evidence、baselines、metrics、expected figure/table、failure condition、current evidence status。
- 每个 experiment 都服务于具体 claim。
- 每个 figure/table 都有明确 message 和 placement。
- reviewer concerns 被转成 risk mitigation。
- uncertainty 被转成 evidence gap / dependency。
- next steps 被转成 research execution step。

### 8.2 `paper_blueprint_explanation.<lang>.md`

应满足：

- 使用用户对话语言。
- 是 standalone validation companion。
- 开头有论文蓝图速览。
- 有“蓝图重点内容与审核入口”。
- 明确解释核心出发点。
- 每个重要蓝图项目先复述内容，再解释原因、关联和用户审核点。
- 使用语义标题或功能近义词指代蓝图项目。
- 不依赖 section number 或人工编号链。
- 不解释 skill、工具、MCP、deepresearch 调用过程、rate limit 或后续 agent 使用方式。
- 用户读完后能判断某个不合理之处来自核心出发点错误、推导错误，还是具体执行细节错误。

## 9. 可直接交给写 Skill Agent 的 Prompt

```text
请为一个基于 Codex 的 autoresearch 系统编写或重构一个 skill，名称建议为 paper-blueprint 或 academic-army-architect。

这个 skill 的任务不是写论文，也不是生成普通论文大纲，而是把用户给出的研究 idea、草稿、代码、初步实验结果或目标 venue，转化成一份可执行的论文方案，以及一份供用户审核该方案是否合理的解释文件。

最终必须生成两个 Markdown 文件：

1. paper_blueprint.md
2. paper_blueprint_explanation.<lang>.md

paper_blueprint.md 是英文文件，主要给后续 AI agent 使用。它应该是客观、结构化、可执行的论文方案规格，描述论文应该如何定位、主 thesis 是什么、有哪些 claims、每个 claim 需要什么证据、相关工作边界在哪里、方法如何拆解、实验如何设计、图表如何服务故事、审稿风险如何缓解、artifact 和可复现材料需要什么、当前还缺哪些证据、下一步研究如何推进。

paper_blueprint_explanation.<lang>.md 是用户语言文件，主要给用户确认蓝图是否合理。它不是普通摘要，也不是对 skill、工具、MCP 或生成流程的解释。它的功能是让用户理解整个论文方案的核心出发点，并看清楚蓝图中的每个重要细节如何从这些核心出发点推导出来。如果用户觉得某个蓝图项目不合理，应能通过解释文件判断是核心出发点错了、推导过程错了，还是具体执行细节需要改。

系统已有 deepresearch MCP 工具，可以现场调用 GPT-5.5 + web search。skill 不需要内置大量 venue 规则、高引论文列表、CFP、最新 SOTA 或 related work 数据库。动态信息应通过 deepresearch 获取。skill 应使用 deepresearch 获取当前 venue expectations、近期 storytelling exemplars、经典和近期 technical/evaluation exemplars、nearest-neighbor related work 和 reviewer-context evidence。deepresearch 只返回证据和分析，不直接生成最终蓝图。

分析写作手法和 storytelling 时，必须优先使用近期论文：最近 2-3 年或目标 venue 最近 3 个 cycle；不足时扩展到最近 5 年。分析 method、dataset、benchmark、baseline、metric、evaluation lineage 时，可以使用更老的经典论文，也要加入近期 nearest-neighbor papers。

paper_blueprint.md 推荐结构：

# Paper Blueprint: <Working Title>

## 1. Metadata and Input State
## 2. Paper Strategy Premises
### 2.1 Target-venue premise
### 2.2 Problem premise
### 2.3 Contribution premise
### 2.4 Novelty premise
### 2.5 Evidence premise
### 2.6 Storytelling premise
### 2.7 Execution premise
## 3. Venue and Scope Specification
## 4. Paper Thesis and Contribution Shape
## 5. Claim and Evidence Plan
## 6. Related-Work Differentiation Plan
## 7. Method Specification
## 8. Evaluation Specification
## 9. Figure and Table Specification
## 10. Manuscript Structure Specification
## 11. Review-Risk Mitigation Plan
## 12. Artifact and Reproducibility Specification
## 13. Evidence Gaps and Dependencies
## 14. Research Execution Plan

正式蓝图可以使用 Markdown 自然章节编号，但不要使用 C1/E1/F1/R1/B1/K1 这类人工对象编号。每个重要项目应该有自解释的描述性标题，例如 Primary claim: <specific claim>、Main-result experiment: <specific comparison and condition>、Risk: <specific reviewer concern>、Evidence gap: <specific missing evidence>。

paper_blueprint_explanation.<lang>.md 必须是 self-contained validation companion。用户不应频繁打开 paper_blueprint.md 对照才能理解它。每个重要蓝图项目都应先复述蓝图内容，再解释设计原因、关联关系和用户审核点。

解释文件推荐结构：

# Paper Blueprint Explanation: <Working Title>

## 1. 论文蓝图速览
## 2. 蓝图重点内容与审核入口
## 3. 核心出发点
## 4. 从核心出发点到论文方案的总体推导
## 5. 论文蓝图逐项解释
## 6. 关键设计取舍的推导
## 7. 当前最容易出错的推导链
## 8. 用户审核时最应该确认的问题

对每个重要蓝图项目，解释文件使用：

1. 蓝图内容概括：用用户语言压缩复述该项目的具体内容。
2. 为什么这样设计：说明它来自哪个核心出发点。
3. 它和其他部分的关系：说明它支持、约束或依赖哪些其他蓝图项目。
4. 用户审核点：说明如果用户觉得这一项不合理，应检查哪个上游 premise、哪个中间推导或哪个执行细节。

解释文件应通过语义标题、译名、功能近义词指代蓝图项目，而不是依赖 section number 或人工编号。例如使用“主 claim”“主实验”“主结果图”“baseline 风险”“reference-versus-Gaussian utility sweep”“CAGS reproduction evidence gap”等。

解释文件只解释论文方案本身，不解释 skill、MCP、deepresearch 调用、rate limit、两个文件用途、下游 agent 使用方式或生成流程。

请尽量使用正向产物契约来写 skill：定义 blueprint 应包含什么、explanation 应包含什么、uncertainty 如何投影成 evidence gaps、reviewer concerns 如何投影成 risk mitigation、reproducibility expectations 如何投影成 artifact deliverables。少用大段禁止清单。

最终 skill 要简洁，但必须明确两个输出文件的职责、deepresearch 使用方式、exemplar 时效规则、正式蓝图结构、解释文件的 validation companion 功能、语义引用方式、内容复述要求和正向 instruction 风格。
```
