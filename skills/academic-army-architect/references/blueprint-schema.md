# Blueprint Schema and Audit

Read this file before drafting or auditing the two blueprint artifacts.

## English Blueprint Schema

Use semantic headings and natural titles. Local numbering inside one section is
acceptable when it improves clarity; section titles should carry the meaning
without requiring lookup-heavy labels.

Use this default structure:

```markdown
# Paper Blueprint: <Working Title>

## Paper Identity
## Core Thesis and Reader Promise
## Target Venue Fit
## Problem Context and Prior-Work Gap
## Paper Goals
## Contribution Strategy
## Claim-Evidence Architecture
## High-Level Design Logic and Scope
## Candidate Method Space
## Evidence Strategy
## Downstream Planning Constraints
## Open Strategic Variables
```

Omit `Candidate Method Space` only when the method direction is strategically
settled and no experiment-dependent method route needs to be compared.

Omit `Open Strategic Variables` when no unresolved strategy-level choice
remains.

### Paper Identity

State the working title, research area, field context, research object, target
readers, venue, paper type, and closest substrate when applicable.

Keep accumulated user facts in the Chinese explanation; use the English
blueprint for the selected paper strategy and downstream contracts.

### Core Thesis and Reader Promise

State the core idea, problem pressure, high-level insight, and reviewer-facing
promise. Keep the thesis compact enough to guide later planning.

### Target Venue Fit

State why the problem matters to venue readers, how the paper matches current
venue posture, and which contribution and evidence style the fit requires. Use
live evidence rather than fixed venue stereotypes.

### Problem Context and Prior-Work Gap

State the strongest existing approaches, their key limitation relative to this
idea, and the differentiated position. Treat inherited components as
substrates. Describe nearest competing work as a comparison boundary.

Select a single best-supported paper position. Preserve alternatives only when
they are experiment-dependent candidate routes or genuine open strategic
variables.

### Paper Goals

Define three to six goals. Each goal states:

- `Objective`: target state.
- `Role in the argument`: support for the thesis or a core claim.
- `Success signal`: evidence-level condition showing the goal is met.

Each goal must guide at least one downstream planning area.

### Contribution Strategy

Name intended contribution shapes, such as method, system, dataset, benchmark,
analysis, theory, measurement, or application insight. State how each
contribution serves a claim and works with the other contributions.

Distinguish:

- selected strategic contribution direction
- inherited substrate or prior component
- candidate method route that still needs experimental convergence

### Claim-Evidence Architecture

Define one to three core claims with natural-language titles. For each claim,
state:

- claim
- why it matters
- supporting contribution components
- required evidence class
- calibration boundary if evidence is narrower than the strongest claim

Keep evidence at claim level, not experiment-protocol level.

Treat method, module, dataset, or benchmark superiority as evidence-backed only
when completed evidence is already supplied by the user; otherwise place the
choice in the candidate method space or evidence strategy.

### High-Level Design Logic and Scope

State canonical terminology, conceptual mechanism, positive scope, inherited
capabilities, explicit novelty boundary, and important risks or weak points for
later planning. Leave formulas, modules, parameters, training details, and
engineering steps to downstream skills.

Express selected strategies as decisions. Express experiment-dependent method
families in `Candidate Method Space`, not as final conclusions.

### Candidate Method Space

Use this section when method superiority depends on future experiments. This is
not a user-open question. It is a downstream method/experiment-planning
contract.

Start with:

```markdown
This section contains experiment-dependent candidate routes. Downstream method
and experiment planning must compare these routes before promoting one into the
final proposed method or converting it into a baseline, ablation, or rejected
route.
```

For each route, use:

```markdown
### <Route name>

Status: candidate; experiment-dependent.

Strategic purpose: <how this route could support the thesis or a core claim>.

Source or theoretical motivation: <source-backed or reasoning-backed basis>.

Potential contribution role: <proposed method core, supporting module,
baseline candidate, ablation variant, or risk-control mechanism>.

Evidence needed to promote: <claim-level evidence class, not a run matrix>.

Disqualifier or demotion condition: <what result or constraint would make it a
baseline, ablation, or rejected route>.

Fair comparison principle: <budget, inputs, outputs, protocol, implementation
quality, or resource-control principle>.
```

Keep this section strategic: describe route logic, evidence needs, demotion
conditions, and fair comparison principles while leaving hyperparameters,
training recipes, ablation tables, and implementation steps to downstream
planning.

### Evidence Strategy

State:

- minimum sufficient evidence chain for the core claims
- relevant effectiveness, generalization, robustness, efficiency,
  interpretability, deployment-value, or insight goals
- dataset, benchmark, baseline-family, and metric-selection principles
- method-route convergence evidence when candidate routes remain
- evidence breadth and fairness obligations
- evidence-dependent claim calibration

Explain why each evidence class is necessary. Delegate exact datasets,
baseline implementations, metrics, tables, run matrices, and resource budgets.

When candidate method routes remain, state how downstream experiments should
convert them into a proposed method, baseline, ablation variant, or rejected
route. Emphasize fair comparison principles rather than exact experiment
design.

### Downstream Planning Constraints

Add contracts for relevant planning areas:

```markdown
### <Planning Area> Contract

Preserve:
- <strategic invariant>

Delegate:
- <tactical design space>
```

Typical areas are content, method, experiment, figure, writing, and optional
review planning. Downstream skills inherit thesis, contribution boundary, claim
hierarchy, venue posture, terminology, candidate method space, evidence
requirements, and open variables. They must raise a strategic-variable update
before materially changing them.

### Open Strategic Variables

Use this section only for unresolved choices that require user/private
information and affect paper identity, claim scope, contribution boundary,
deployment boundary, evidence chain, or downstream contracts.

Place method superiority questions that require experiments in `Candidate
Method Space`; reserve this section for strategy-level variables that need
user/private information.

State once:

```markdown
Default propagation rule: downstream skills must use each variable's current
best-supported stance unless the user, private project facts, or completed
evidence resolves that variable.
```

Then use:

```markdown
### <Variable name>

Status: unresolved.

Affects: <strategic areas>.

Why unresolved: <why user facts, live evidence, and venue-oriented judgment do
not yet support a reliable best choice>.

Current best-supported stance: <default propagated to downstream skills>.

Allowed resolutions: <short strategy-level alternatives>.
```

## Chinese Explanation Schema

Use this default structure:

```markdown
# 论文蓝图说明：<Working Title>

## 当前论文方案概括
## 用户已经明确的内容
### 已确认约束
### 偏好但未锁定
## 当前工作假设
## 使用的研究信号
### 跨论文模式
### 承重信号
### 额外背景信号
## 核心出发点
## 按蓝图顺序解释论文方案
## 候选方法空间说明
## 开放验证项
## 本轮已收缩的开放项
## 证据变化时如何校准 Claim
```

Omit `候选方法空间说明` when the English blueprint has no candidate method
space.

Omit `开放验证项` when no strategy-level question remains.

Omit `本轮已收缩的开放项` on the first run or when nothing was resolved.

### Explanation Rules

- Start with a concise, independently readable paper-strategy summary.
- Accumulate explicit user facts under `用户已经明确的内容`.
- Follow English blueprint heading order under `按蓝图顺序解释论文方案`.
- Restate each blueprint decision in Chinese before explaining its rationale.
- Explain relationships among thesis, goals, claims, contribution shapes,
  candidate method routes, evidence chain, venue fit, and downstream
  constraints.
- Discuss recent high-impact storytelling patterns from the target or adjacent
  venues and connect those patterns to the blueprint's choices.
- When a materially plausible alternative was rejected, briefly explain why
  the selected strategy better serves the paper goal, venue fit, claims, or
  downstream executability.
- When method routes remain candidates, explain why the current stage should
  not select a unique final method before experiments.
- Distinguish user facts, evidence findings, preferences, assumptions,
  candidate method routes, and open validation items.
- Explain why each open item cannot yet be resolved from user facts, live
  evidence, venue posture, and paper goals; then state the current
  best-supported stance and what each resolution changes.
- Explain claim calibration separately from user-input changes.

Use Chinese sentences as the default. Preserve English terms when they are the
conventional technical name. Refer to sections by their natural headings or
plain descriptions rather than lookup-heavy labels.

## Boundary Tests

The artifacts should contain paper-design information, claim-level evidence
requirements, strategic constraints, candidate method routes, open variables,
and Chinese paper-rationale explanation.

Before delivery, rewrite tactical or process-level material into paper-level
strategy. Full paper prose, detailed section plans, run matrices, figure
layouts, implementation recipes, hyperparameter plans, user-operation advice,
artifact notes, workflow commentary, and unsupported best-result claims should
be represented only as contribution boundaries, downstream contracts, evidence
needs, candidate-route conditions, or claim-calibration rules.

## Final Audit

Check:

- exactly two Markdown files exist in the requested output directory
- `paper_blueprint.md` is English-only, declarative, strategic, and AI-facing
- `paper_blueprint.explain.md` is Chinese-first, preserves conventional
  English technical names naturally, is self-contained, and focuses on
  paper-design rationale
- accumulated user facts appear only in the Chinese explanation
- each important rationale first restates the corresponding blueprint decision
- semantic headings replace lookup-heavy identifier systems
- readers, venue fit, prior-work gap, goals, contribution strategy, one to
  three claims, minimum sufficient evidence chain, scope, downstream
  constraints, and open variables are present when applicable
- every core claim has a claim-level evidence requirement
- user facts remain constraints instead of reopened questions
- open items are strategic, deduplicated, and shrink across iterations
- experiment-dependent method choices appear as candidate routes rather than
  user-open validation items
- candidate method routes include evidence-needed, disqualifier/demotion, and
  fair-comparison principles
- selected strategies replace unnecessary menus of plausible paper positions
- tactical choices are delegated
- recent storytelling exemplars and load-bearing sources influence the Chinese
  explanation
- both files can be read back
