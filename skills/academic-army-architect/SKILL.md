---
name: academic-army-architect
description: >-
  Create two Markdown files for a goal-oriented strategic research-paper blueprint: an English paper_blueprint.md and a user-language paper_blueprint_explanation language-suffixed Markdown file. The blueprint converts a research idea into top-level paper goals, goal decomposition, goal cards, a goal dependency map, strategic claim posture, strategic evidence posture, strategic communication posture, strategic risks, and downstream planning interfaces. Use when the user needs a stable upstream paper-goal specification for later content-planning, experiment-planning, figure-planning, method-planning, writing, or review skills. Uses `academic_army_mcp_tools.deepresearch` as the required live research MCP tool for venue, literature, exemplar-paper, evaluation-expectation, and reviewer-context evidence.
---

# Academic Army Architect

## Output Contract

The skill produces two Markdown files.

### File 1: `paper_blueprint.md`

This file is an English **Goal-Oriented Strategic Paper Blueprint**.

It defines the paper's strategic core and downstream planning constraints:

- paper identity
- top-level paper goal
- goal decomposition
- goal cards
- goal dependency map
- strategic claim posture
- strategic evidence posture
- strategic communication posture
- strategic risks
- delegation interfaces for downstream skills

The blueprint stops at strategy. It states what the paper must achieve, why the goals matter, how goals constrain claims/evidence/communication, and what later skills must preserve.

### File 2: `paper_blueprint_explanation.<lang>.md`

This file is a user-language strategic validation companion.

It helps the user validate the blueprint by showing:

- which inputs, constraints, preferences, and pipeline assumptions the user has explicitly provided
- what the important goals and goal-derived arrangements say, in compressed user-language form
- which goal motivates each arrangement
- how each arrangement follows from the goal structure
- how each goal constrains later content, experiment, figure, method, writing, or review planning
- which tactical details are intentionally delegated
- what strategic question the user should inspect when an item feels unreasonable

Use the user's conversation language. Preserve technical terms, venue names, paper titles, datasets, benchmarks, metrics, and method names in their original language when that improves precision.

## Required Research MCP

This skill's live research dependency is the `deepresearch` tool from the `academic_army_mcp_tools` MCP server.

Use the exact tool identity:

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical Codex MCP tool name, when exposed: `mcp__academic_army_mcp_tools__deepresearch`

All mentions of `deepresearch` in this skill refer to `academic_army_mcp_tools.deepresearch`.

Use `academic_army_mcp_tools.deepresearch` for current venue evidence, related-work evidence, exemplar-paper evidence, evaluation-expectation evidence, and reviewer-context evidence.

Evidence from built-in web search, browser tools, documentation search, or other MCP servers is supplemental and does not satisfy this skill's required live research dependency.

The final Markdown files should contain the paper-level conclusions derived from this evidence, not tool-call logs or MCP implementation details.

## Confirmed User Context

Start `paper_blueprint_explanation.<lang>.md` with a calibration section named `Confirmed User Context` or its natural equivalent in the user's language.

This section records only user-confirmed inputs, constraints, preferences, and pipeline assumptions. It lets the user verify that the blueprint starts from the correct context before reading the strategic decomposition.

This calibration section belongs only in `paper_blueprint_explanation.<lang>.md`. Keep `paper_blueprint.md` focused on the strategic paper blueprint itself.

Treat this section as a confirmation ledger for the rest of the explanation. Later validation questions are generated after checking what this ledger already covers.

Include user-confirmed information such as:

- research idea
- existing materials
- target field or venue preference
- intended use of the blueprint
- downstream planning skills that will consume the blueprint
- desired abstraction level
- output file requirements
- explanation-file purpose
- language and readability preferences
- content delegated to later planning skills

Separate confirmed context from working assumptions. Use a short `Current Working Assumptions` subsection only when the blueprint must proceed despite missing strategic information.

## Confirmed Context Coverage Filter

Use the confirmed context ledger to filter user-facing validation questions.

Before writing `Remaining Strategic Questions for User Confirmation`, classify candidate questions:

| Classification | Output action |
|---|---|
| `covered_by_user_confirmation` | Treat the point as settled context and omit it from remaining questions. |
| `partially_covered` | Ask only the unresolved strategic remainder. |
| `conflicts_with_user_confirmation` | Revise the blueprint or mark the inconsistency as a blueprint issue. |
| `delegated_to_downstream_skill` | Express the point as a downstream planning boundary, not a user question. |
| `unresolved_strategic_question` | Include it as a remaining strategic question. |

Across iterative runs, move newly confirmed strategic points into the confirmed context ledger. As the ledger grows, remaining strategic questions should usually shrink, except when the user changes the paper direction, venue posture, top-level goal, or strategic constraints.

## Strategic Abstraction Level

The blueprint operates only at Levels 0-2:

| Level | Scope |
|---|---|
| Level 0: Paper identity | Research area, target venue posture, paper type, research object, current input state. |
| Level 1: Paper goals | Top-level goal, goal decomposition, goal cards, goal dependency map, strategic risks. |
| Level 2: Goal-derived planning constraints | Claim posture, evidence posture, communication posture, scope posture, downstream delegation interfaces. |

Later specialized skills handle Levels 3-4:

| Level | Scope |
|---|---|
| Level 3: Tactical planning | Exact experiments, datasets, traces, workloads, baselines, metrics, figure list, layouts, section structure, algorithm variants. |
| Level 4: Execution planning | Scripts, run order, implementation tasks, plotting commands, writing tasks, rebuttal execution. |

Every detailed item in the blueprint should change the paper's strategic identity if altered. Otherwise compress it into a strategic requirement, planning constraint, acceptable design space, delegated planning variable, or decision-critical uncertainty.

## Tactical-Detail Compression

When a planning decision becomes specific, compress it into one of these strategic forms:

| Tactical impulse | Strategic form |
|---|---|
| Choose an algorithm family | Recommended method posture plus change condition. |
| List exact baselines | Comparison posture and credible comparison classes. |
| Pick datasets or traces | Data/workload posture and target setting. |
| Specify metric formulas | Outcome family and evidence standard. |
| Design figures | Visual argument requirement. |
| Outline sections | Narrative requirement. |
| Create task sequence | Strategic research priority or decision-critical uncertainty. |

Use strategic defaults over user prompting. Select a strategic default when possible and state what evidence would change it. Ask a clarification question only when the missing information blocks target venue posture, contribution posture, or central thesis.

## Core Goal-Oriented Objects

### Goal Card Object

Each major paper goal is represented as a goal card:

- goal statement
- why this goal matters
- strategic role: acceptance, positioning, contribution, novelty, evidence, scope, communication, or downstream planning
- success condition
- derived constraints
- delegated details
- failure or revision implication

Goal cards are the core output unit. Claim posture, evidence posture, communication posture, risks, and downstream interfaces should lose their source if the goal cards are removed.

### Strategic Claim Posture Object

For each claim posture item, specify:

- claim statement
- generating goal
- strategic role of the claim
- required evidence posture
- scope boundary
- downgrade condition

### Strategic Evidence Posture Object

For each evidence posture, specify:

- goal served
- evidence type at a high level
- comparison posture
- outcome family
- minimum standard for strategic viability
- delegated tactical choices
- downgrade implication

### Delegation Interface Object

For each downstream skill, specify:

- goal or goals it operationalizes
- constraints to preserve
- tactical choices delegated

## Goal-Derived Content Rule

Every major blueprint arrangement is derived from one or more paper goals:

- claim posture serves an acceptance, contribution, evidence, or scope-control goal
- evidence posture validates a goal
- novelty boundary protects a contribution or positioning goal
- communication posture helps the reader accept a problem-framing or contribution goal
- strategic risk exists because a fragile goal might fail
- downstream interface exists because a goal must be operationalized by a later specialized skill

Make these goal-to-arrangement relationships explicit.

## Semantic References

`paper_blueprint.md` uses hierarchical Markdown headings. `paper_blueprint_explanation.<lang>.md` refers to blueprint items by semantic anchors: exact headings, translated headings, concise functional names, or natural-language paraphrases.

Preferred explanation references:

- the top-level paper goal
- the contribution goal
- the novelty-boundary goal
- the evidence goal
- the communication goal
- the claim posture generated by the acceptance goal
- the evidence posture generated by the contribution goal
- the experiment-planning interface

Section numbers are secondary locators. The explanation remains readable without them.

## Evidence Gathering

Use `academic_army_mcp_tools.deepresearch` when current venue expectations, related work, exemplars, SOTA, benchmark norms, or reviewer expectations affect the strategy.

Gather evidence for:

1. Venue posture: current venue expectations, contribution categories, evidence standards, and recent accepted-paper storytelling style.
2. Literature boundary: closest work clusters, solved problems, differentiation posture, comparison posture, and overclaim boundaries.
3. Exemplar patterns: recent storytelling exemplars, canonical technical anchors, and evidence-pattern exemplars.
4. Reviewer context: strategic pressure on novelty, evidence posture, comparison posture, scope, and claims.

Use recent target-venue papers for storytelling style. Use canonical and recent papers together for methods, datasets, benchmarks, and evaluation lineage.

## Workflow

### Step 1: Parse Request

Extract topic, target venue or candidate venues, field/subfield, likely paper type, research object, available materials, pending materials, strategic constraints, output language, and output directory.

### Step 2: Build Internal Research Brief

Create a compact internal brief with:

- one-sentence paper idea
- likely target venue posture
- likely paper type
- research object
- known evidence
- likely top-level paper goal
- likely contribution goal
- likely novelty-boundary goal
- decision-critical uncertainty
- output language and output paths

### Step 3: Gather Live Evidence

Use evidence returned by `academic_army_mcp_tools.deepresearch` to establish venue posture, goal structure, related-work boundary, exemplar-derived story patterns, evidence posture, and reviewer-context pressure.

### Step 4: Compile `paper_blueprint.md`

Use this structure:

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

For each major goal, include:

**Goal statement.**
**Why this goal matters.**
**Strategic role.**
**Success condition.**
**Derived constraints.**
**Delegated details.**
**Failure or revision implication.**

## 5. Goal Dependency Map
### 5.1 Goals that directly support the top-level acceptance goal
### 5.2 Goals that protect the main contribution
### 5.3 Goals that protect the novelty boundary
### 5.4 Goals that determine evidence posture
### 5.5 Goals that determine communication posture
### 5.6 Goals that downstream planning skills must operationalize
### 5.7 Goals that are currently most fragile

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

### Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Use this structure:

```markdown
# Goal-Oriented Paper Blueprint Explanation: <Working Title>

## 0. Confirmed User Context

## Blueprint Overview: What This Paper Is Trying to Achieve

## Core Goal Set

## Derivation from Core Goals to the Blueprint

## Key Blueprint Content: Digest and Rationale

## How the Goals Support Each Other

## Fragile Goal Chains

## Remaining Strategic Questions for User Confirmation

## What Is Delegated to Later Specialized Planning
```

For each important goal or goal-derived item, first restate the content in the user's language, then explain:

1. which goal motivates it
2. how it helps the paper achieve that goal
3. how it connects to other goal-derived arrangements
4. how it constrains downstream planning
5. what strategic question the user should inspect

User validation questions should stay strategic: top-level paper goal, venue posture, contribution goal, claim strength, novelty boundary, evidence posture, scope-control goal, and delegation interface.

Before outputting these questions, apply the confirmed context coverage filter. Questions already answered by the confirmed user context should disappear; partially answered questions should be narrowed; tactical questions should become downstream planning boundaries. If no unresolved strategic question remains, say that the current confirmed context covers the strategic decisions and that remaining uncertainty belongs to later specialized planning.

The explanation should use the confirmed context as its starting point. Goal decomposition and blueprint rationale should follow from that context and the explicitly stated working assumptions.

## `academic_army_mcp_tools.deepresearch` Prompt Shape

Use this prompt shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a goal-oriented strategic paper-blueprint generator.

Return paper-relevant evidence for defining the upstream goal-oriented strategic blueprint.

Research brief:
[RESEARCH_BRIEF]

Target venue:
[VENUE]

Return four sections:

1. Venue and goal evidence
   Summarize current venue expectations, likely paper goals, contribution posture, evidence posture, and recent accepted-paper storytelling patterns.

2. Technical and literature boundary evidence
   Summarize closest work clusters, solved problems, differentiation posture, comparison posture, and overclaim boundaries.

3. Exemplar pattern evidence
   Summarize recent storytelling patterns and canonical technical/evidence patterns that affect strategic positioning.

4. Reviewer-context evidence
   Summarize strategic pressure on goals, novelty, evidence posture, comparison posture, scope, and claims.

For each source, include title, venue/year when available, source link, relevance to the proposed paper, and the lesson for goal-oriented strategic blueprint design.

Use concise evidence-facing prose.
```

## Research Tool Identity Checklist

Before using live research evidence, confirm that it came from `academic_army_mcp_tools.deepresearch` or the canonical Codex MCP tool name `mcp__academic_army_mcp_tools__deepresearch`.

If `academic_army_mcp_tools.deepresearch` is unavailable, proceed with user-provided evidence and mark live-research-dependent strategy items as needing external evidence. Describe the resulting paper-level evidence gap in the outputs, not the tool availability issue.

## Final Quality Checklist

Before finalizing `paper_blueprint.md`, check that:

- the file reads as a Strategic Paper Blueprint
- the first section identifies the research idea, venue posture, paper type, research object, and current input state
- top-level paper goal, goal decomposition, goal cards, and goal dependency map are explicit
- goal cards contain goal statement, rationale, role, success condition, derived constraints, delegated details, and revision implication
- claim posture, evidence posture, communication posture, risks, and delegation interfaces are derived from goals
- evidence posture is strategic rather than a concrete experiment protocol
- comparison posture is strategic rather than a fixed baseline list
- communication posture defines requirements rather than detailed section or figure plans
- every included detail would change the paper's strategic identity if altered

Before finalizing `paper_blueprint_explanation.<lang>.md`, check that:

- the file reads as a strategic validation companion in the user's language
- the file begins with confirmed user context
- confirmed user context records only information explicitly provided by the user
- working assumptions are separated from confirmed user context when assumptions are needed
- confirmed context is used to filter remaining strategic questions
- important goals and goal-derived items are restated before they are explained
- the explanation is organized around core goals and fragile goal chains
- remaining validation questions ask only unresolved strategy, not already confirmed context or tactical choices
- tactical topics are discussed as delegated planning areas with strategic constraints
- the explanation helps the user locate disagreement at the goal, derivation, or delegation-interface level

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
