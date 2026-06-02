---
name: academic-army-architect
description: >-
  Create exactly two Markdown files for an upstream research-paper strategy:
  an English AI-facing `paper_blueprint.md` and a user-language
  `paper_blueprint.explain.md` that helps the user validate every
  decision-bearing blueprint item. Use for refining a paper idea, positioning
  a submission for a target venue, defining strategic novelty and scope, or
  preparing a stable specification for later content, method, experiment,
  figure, writing, and review-planning skills. Use
  `academic_army_mcp_tools.deepresearch` for live venue and literature
  evidence.
---

# Academic Army Architect

## Purpose

Convert a research idea into an upstream paper-strategy specification for downstream AI planning.

Produce:

- an English blueprint that objectively defines the proposed paper
- a user-language explanation that helps the user confirm how each blueprint choice follows from the idea, evidence, and current assumptions

Keep the blueprint strategic and goal-oriented. Route tactical planning to specialized downstream skills.

## Output Contract

Produce exactly two Markdown files:

- `paper_blueprint.md`
- `paper_blueprint.explain.md`

### `paper_blueprint.md`

Write in English. Treat this file as an AI-facing specification.

Include:

1. `Paper Identity`
2. `Strategic Thesis`
3. `Canonical Model and Terminology`
4. `Core Strategic Goals`
5. `Claim and Scope Architecture`
6. `Evidence Objectives`
7. `Downstream Skill Contract`
8. `Open Strategic Variables`, only when strategy-level decisions remain unresolved

Reserve this file for objective paper strategy: goals, claims, problem definition, mechanism intuition, contribution boundary, success signals, evidence objectives, and downstream planning interfaces.

Place rationale, source analysis, user-confirmation state, and process-facing explanation in `paper_blueprint.explain.md`.

### `paper_blueprint.explain.md`

Write in the user's conversation language. Preserve precise technical terms, paper titles, venue names, datasets, benchmarks, and method names when useful.

Use this file as a validation companion. Help the user trace:

`confirmed inputs + preferences + working assumptions + research patterns + unresolved strategic variables -> blueprint strategy`

Restate each decision-bearing blueprint item before explaining:

- which starting point or research pattern produced it
- how it supports the central thesis and goals
- which downstream planning areas inherit it
- which strategic uncertainty remains, when applicable

Use semantic titles and natural-language references. Use section numbers only as document structure.

## Strategic Boundary

Keep the blueprint at Levels 0-2. Delegate Levels 3-4.

| Level | Responsibility |
|---|---|
| Level 0: paper identity | research area, venue posture, paper type, research object |
| Level 1: thesis and goals | main thesis, central bet, acceptance target, core strategic goals |
| Level 2: strategic constraints | canonical model, novelty boundary, scope, evidence objectives, downstream contracts |
| Level 3: tactical planning | exact algorithms, datasets, traces, devices, baselines, metrics, figures, section outline |
| Level 4: execution planning | scripts, run order, implementation tasks, plotting commands, writing tasks |

Translate tactical ideas into strategic constraints:

| Tactical input | Blueprint-level form |
|---|---|
| controller, model, or proof technique | required method property |
| exact baseline list | comparison families and fairness obligations |
| datasets, traces, devices | evidence dimensions and workload breadth |
| metric formulas | outcome families |
| figure ideas | visual argument that figure planning should make legible |
| section outline | story movement that content planning should preserve |

## Confirmation State and Shrinking Questions

Maintain four mutually exclusive buckets in `paper_blueprint.explain.md`.

### Confirmed

Record explicit user-locked strategy facts: research idea, target venue, closest substrate, novelty boundary, scope, paper type, required strategic direction, and existing system foundation.

### Preferred but Not Locked

Record user-mentioned preferences that guide the default stance: likely method posture, desired implementation posture, candidate evidence dimensions, and candidate comparison families.

### Working Assumptions

Record conservative defaults used to create a coherent blueprint when the user has not locked a strategy point.

### Still to Confirm

Record only unresolved choices that change paper identity, claim scope, deployment boundary, or downstream planning contracts.

Use this precedence:

1. explicit confirmation
2. unresolved strategic variable
3. preference
4. working assumption

Filter each potential question:

| Classification | Action |
|---|---|
| covered by confirmed input | treat as settled |
| partially covered | keep only the unresolved strategic remainder |
| tactical choice | route to a downstream contract |
| unresolved strategic variable | include once under `Remaining Strategic Choices` |

Across iterative runs, move newly confirmed strategy points into `Confirmed`. The remaining-choice list should naturally shrink.

## Required Live Research

Use the exact MCP tool:

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical name: `mcp__academic_army_mcp_tools__deepresearch`

Use live research for:

- target-venue posture and current CFP scope
- closest technical substrate and literature boundary
- closest competing systems
- recent high-impact storytelling exemplars from the target venue, adjacent top venues, and the relevant field
- canonical method, dataset, benchmark, and evaluation precedents

Use recent papers, preferably from the last 1-3 years, to infer current storytelling style. Use older papers when they remain load-bearing method or evaluation precedents.

Ask `academic_army_mcp_tools.deepresearch` for:

```text
Research brief:
[IDEA, KNOWN SUBSTRATE, TARGET PROBLEM, USER-CONFIRMED BOUNDARIES]

Target venue:
[VENUE]

Return concise evidence in seven sections:
1. Venue posture
2. Closest technical substrate and literature boundary
3. Closest competing systems
4. Recent high-impact storytelling exemplars and why their framing works
5. Cross-paper synthesis
6. Method and evaluation precedents
7. Source-role table with title, venue/year, link, role, persuasive pattern, and blueprint lesson

Separate source-supported facts from inference. Prioritize sources that materially change the strategy.
```

In the explanation, begin `Research Signals Used` with 3-5 cross-paper patterns. Then present 6-8 load-bearing sources. For each source, state what it establishes, why its framing or evidence style is effective, and which blueprint choice it influenced.

## Blueprint Structure

Use this default structure and adapt domain-specific subheadings as needed:

```markdown
# Paper Blueprint: <Working Title>

## 1. Paper Identity
## 2. Strategic Thesis
## 3. Canonical Model and Terminology
## 4. Core Strategic Goals
## 5. Claim and Scope Architecture
## 6. Evidence Objectives
## 7. Downstream Skill Contract
## 8. Open Strategic Variables
```

### Core Strategic Goals

Define 3-6 goals. Each goal states:

- `Objective`: target state
- `Strategic function`: role in the paper argument
- `Success signal`: evidence-level condition for success

### Claim and Scope Architecture

State:

- the main claim
- supporting claims
- the novelty scope
- the positive scope boundary
- evidence-dependent claim calibration

Treat inherited components as substrate. Describe adjacent systems as the comparison boundary.

### Evidence Objectives

State:

- phenomena to establish
- outcome families
- comparison posture
- evidence breadth

Separate substrate benefit, proposed-contribution benefit, and evidence-dependent claim strength.

### Downstream Skill Contract

Add a contract for each referenced planning area:

```markdown
### <Skill Area> Contract
Preserve:
- <strategic invariant>

Delegate:
- <tactical design space>
```

Typical areas: content, method, experiment, figure, writing, and optional review planning.

### Open Strategic Variables

Use this section only when unresolved strategy-level decisions remain.

State once:

```markdown
Default propagation rule: downstream skills must use each variable's current conservative stance unless the user or evidence resolves that variable.
```

Then use:

```markdown
### <Variable name>
Status: unresolved.
Affects: <strategic areas>.
Current conservative stance: <neutral default>.
Allowed resolutions: <short semicolon-separated strategy resolutions>.
```

## Explanation Structure

Use localized headings. For Chinese:

```markdown
# 论文蓝图说明：<Working Title>
## 0. 当前默认立场
## 1. 确认状态
### 已确认
### 偏好但未锁定
### 仍需确认
## 2. 工作假设
## 3. 使用的研究信号
### 跨论文模式
### 承重信号
### 额外背景信号
## 4. 核心起点
## 5. 蓝图条目与理由
## 6. 剩余战略选择
## 7. 已确认输入变化时的影响
## 8. 证据依赖的 Claim 校准
```

Keep `当前默认立场` to 3-5 short lines. Explain a small set of core starting points. Under `蓝图条目与理由`, cover every top-level blueprint section, every goal, every downstream contract, and every open strategic variable.

For each remaining strategic choice, state:

```markdown
### <Strategic variable>
已确认部分：<settled context>
未确认部分：<remaining strategy choice>
当前默认立场：<conservative default>
不同选择会改变什么：<identity, scope, evidence, or downstream impact>
```

Keep user-input changes separate from evidence-dependent claim calibration.

## Workflow

1. Parse confirmed inputs, preferences, and unresolved strategy variables.
2. Run `academic_army_mcp_tools.deepresearch`.
3. Synthesize core starting points and cross-paper patterns.
4. Define the paper identity, thesis, canonical model, and 3-6 goals.
5. Calibrate claims and evidence objectives at the strategic level.
6. Route tactical choices into downstream contracts.
7. Write the two Markdown files.
8. Read both files back and audit them.
9. Return paths and a concise delivery summary.

## Final Audit

Check:

- exactly two output files exist
- `paper_blueprint.md` is English, declarative, strategic, and AI-facing
- `paper_blueprint.explain.md` uses the user's language and restates decision-bearing blueprint items before explaining them
- confirmation buckets are mutually exclusive
- remaining strategic choices correspond one-to-one with open variables
- tactical choices are routed into downstream contracts
- recent storytelling exemplars influence the explanation
- source roles and links are clear
- both files can be read back

## Delivery and Access Fallback

Return clickable paths, a short identity summary, unresolved strategic-variable names when present, and the readback result.

When the caller explicitly requests a portable payload, or when local artifact access fails in the active session, append the complete contents of both Markdown files in separate fenced blocks. Label in-memory content as `unverified` when readback did not complete.
