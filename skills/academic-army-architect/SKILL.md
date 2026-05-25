---
name: academic-army-architect
description: >-
  Create two Markdown files for an upstream research-paper strategy workflow: an English paper_blueprint.md containing a Strategic Paper Blueprint, and a user-language paper_blueprint_explanation language-suffixed Markdown file that starts with user-confirmed context, then restates the blueprint's strategic content and explains how each item follows from the paper's premises so the user can validate the strategy. Use when the user needs venue posture, thesis shaping, problem framing, contribution boundaries, claim strategy, evidence posture, novelty boundary, method abstraction strategy, scope constraints, delegation boundaries, and strategic defaults for later content-planning, experiment-planning, figure-planning, method-planning, writing, or review skills. Uses `academic_army_mcp_tools.deepsearch` as the required live research MCP tool for venue, literature, exemplar, and reviewer-context evidence.
---

# Academic Army Architect

## Output Contract

The skill produces two Markdown files.

### File 1: `paper_blueprint.md`

This file is an English **Strategic Paper Blueprint**.

It defines the paper's strategic core and downstream planning constraints:

- paper identity
- core strategy premises
- central research bet
- contribution contract
- claim strategy
- novelty and comparison strategy
- method abstraction strategy
- evidence posture
- narrative and visual strategy
- strategic risks and decision-critical uncertainties
- delegation boundaries for downstream skills
- strategic defaults and change conditions

The blueprint stops at strategy. It states what the paper must prove, why it matters, what boundaries hold, what evidence posture is required, and what later skills must preserve.

### File 2: `paper_blueprint_explanation.<lang>.md`

This file is a user-language strategic validation companion.

It helps the user validate the blueprint by showing:

- which inputs, constraints, preferences, and pipeline assumptions the user has explicitly provided
- what the important strategic items say, in compressed user-language form
- which premise motivates each item
- how each item follows from the premises
- how each item constrains later content, experiment, figure, method, writing, or review planning
- which tactical details are intentionally delegated
- what strategic question the user should inspect when an item feels unreasonable

Use the user's conversation language. Preserve technical terms, venue names, paper titles, datasets, benchmarks, metrics, and method names in their original language when that improves precision.

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

## Confirmed User Context

Start `paper_blueprint_explanation.<lang>.md` with a calibration section named `Confirmed User Context` or its natural equivalent in the user's language.

This section records only user-confirmed inputs, constraints, preferences, and pipeline assumptions. It lets the user verify that the blueprint starts from the correct context before reading the strategic decomposition.

This calibration section belongs only in `paper_blueprint_explanation.<lang>.md`. Keep `paper_blueprint.md` focused on the strategic paper blueprint itself.

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

## Strategic Abstraction Level

The blueprint operates only at Levels 0-2:

| Level | Scope |
|---|---|
| Level 0: Paper identity | Research area, target venue posture, paper type, research object, current input state. |
| Level 1: Paper strategy | Core premises, central research bet, contribution contract, claim strategy, novelty boundary, scope boundary, strategic risks. |
| Level 2: Planning constraints | Evidence posture, comparison posture, narrative requirements, visual argument requirements, downstream delegation boundaries. |

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

## Core Strategic Objects

### Claim Strategy Object

For each strategic claim, specify:

- claim statement
- strategic role: acceptance-critical, mechanism, scope, supporting, or deferred
- evidence posture
- scope boundary
- downgrade condition

### Evidence Posture Object

For each evidence posture, specify:

- strategic claim supported
- evidence type at a high level
- comparison posture
- outcome family
- minimum standard for strategic viability
- delegated tactical choices
- downgrade implication

### Delegation Boundary Object

For each downstream skill, specify:

- strategic boundary
- constraints to preserve
- tactical choices delegated
- strategic default to begin from
- condition that would change the default

## Semantic References

`paper_blueprint.md` uses hierarchical Markdown headings. `paper_blueprint_explanation.<lang>.md` refers to blueprint items by semantic anchors: exact headings, translated headings, concise functional names, or natural-language paraphrases.

Preferred explanation references:

- the central research bet
- the acceptance-critical claim
- the evidence posture for the primary claim
- the comparison posture against related work
- the method abstraction strategy
- the visual argument requirement
- the experiment-planning boundary
- the strategic default for contribution posture

Section numbers are secondary locators. The explanation remains readable without them.

## Evidence Gathering

Use `academic_army_mcp_tools.deepsearch` when current venue expectations, related work, exemplars, SOTA, benchmark norms, or reviewer expectations affect the strategy.

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
- likely contribution posture
- likely novelty boundary
- decision-critical uncertainty
- output language and output paths

### Step 3: Gather Live Evidence

Use evidence returned by `academic_army_mcp_tools.deepsearch` to establish venue posture, related-work boundary, exemplar-derived story patterns, evidence posture, and reviewer-context pressure.

### Step 4: Compile `paper_blueprint.md`

Use this structure:

```markdown
# Strategic Paper Blueprint: <Working Title>

## 1. Paper Identity
### 1.1 Research object
### 1.2 Target venue posture
### 1.3 Paper type
### 1.4 Current input state

## 2. Core Strategy Premises
### 2.1 Venue premise
### 2.2 Problem premise
### 2.3 Contribution premise
### 2.4 Novelty premise
### 2.5 Evidence premise
### 2.6 Scope premise

## 3. Central Research Bet
### 3.1 One-sentence thesis
### 3.2 Acceptance-critical bet
### 3.3 What would downgrade the bet

## 4. Contribution Contract
### 4.1 Primary contribution
### 4.2 Secondary contribution roles
### 4.3 Non-contributions and boundaries

## 5. Claim Strategy
### 5.1 Acceptance-critical claim
### 5.2 Mechanism claim
### 5.3 Scope claim
### 5.4 Claims to defer

## 6. Novelty and Comparison Strategy
### 6.1 Closest work clusters
### 6.2 Differentiation posture
### 6.3 Comparison posture
### 6.4 Overclaim boundary

## 7. Method Abstraction Strategy
### 7.1 Core abstraction
### 7.2 Mechanism class
### 7.3 Decision space at a strategic level
### 7.4 Constraints and invariants
### 7.5 Tactical method details delegated to later planning

## 8. Evidence Posture
### 8.1 Evidence posture for the primary claim
### 8.2 Evidence posture for the mechanism claim
### 8.3 Evidence posture for scope and robustness
### 8.4 Evidence posture for feasibility and cost
### 8.5 Tactical experiment design delegated to later planning

## 9. Narrative and Visual Strategy
### 9.1 Opening tension
### 9.2 Central abstraction to foreground
### 9.3 Story arc
### 9.4 Visual argument requirements
### 9.5 Tactical content and figure planning delegated to later planning

## 10. Strategic Risks and Decision-Critical Uncertainties
### 10.1 Highest-risk premise
### 10.2 Highest-risk claim
### 10.3 Highest-risk novelty boundary
### 10.4 Highest-risk evidence gap
### 10.5 How the paper strategy changes if each risk materializes

## 11. Delegation Boundaries for Downstream Skills
### 11.1 Content-planning boundary
### 11.2 Experiment-planning boundary
### 11.3 Figure-planning boundary
### 11.4 Method-planning boundary
### 11.5 Review-planning boundary

## 12. Strategic Defaults
### 12.1 Recommended venue posture
### 12.2 Recommended contribution posture
### 12.3 Recommended evidence posture
### 12.4 Recommended narrative posture
### 12.5 Conditions that would change these defaults
```

### Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Use this structure:

```markdown
# Strategic Paper Blueprint Explanation: <Working Title>

## 0. Confirmed User Context

## Strategic Blueprint Overview

## Key Strategic Content and Validation Entry Points

## Core Premises

## Derivation from Premises to Strategy

## Item-by-Item Strategic Validation

## What Is Delegated to Later Specialized Planning

## Strategic Defaults and Change Conditions

## Fragile Strategic Chains

## Priority Questions for User Review
```

For each important strategic item, first restate the content in the user's language, then explain:

1. which premise motivates it
2. how it follows from the premise
3. how it constrains downstream planning
4. what strategic question the user should inspect

User validation questions should stay strategic: venue posture, problem premise, contribution contract, claim strength, novelty boundary, evidence posture, scope boundary, and delegation boundary.

The explanation should use the confirmed context as its starting point. Goal decomposition and blueprint rationale should follow from that context and the explicitly stated working assumptions.

## `academic_army_mcp_tools.deepsearch` Prompt Shape

Use this prompt shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepsearch

You are supporting a strategic paper-blueprint generator.

Return paper-relevant evidence for defining the upstream strategic blueprint.

Research brief:
[RESEARCH_BRIEF]

Target venue:
[VENUE]

Return four sections:

1. Venue posture evidence
   Summarize current venue expectations, contribution posture, evidence posture, and recent accepted-paper storytelling patterns.

2. Technical and literature boundary evidence
   Summarize closest work clusters, solved problems, differentiation posture, comparison posture, and overclaim boundaries.

3. Exemplar pattern evidence
   Summarize recent storytelling patterns and canonical technical/evidence patterns that affect strategic positioning.

4. Reviewer-context evidence
   Summarize strategic pressure on novelty, evidence posture, comparison posture, scope, and claims.

For each source, include title, venue/year when available, source link, relevance to the proposed paper, and the lesson for strategic blueprint design.

Use concise evidence-facing prose.
```

## Research Tool Identity Checklist

Before using live research evidence, confirm that it came from `academic_army_mcp_tools.deepsearch` or the canonical Codex MCP tool name `mcp__academic_army_mcp_tools__deepsearch`.

If `academic_army_mcp_tools.deepsearch` is unavailable, proceed with user-provided evidence and mark live-research-dependent strategy items as needing external evidence. Describe the resulting paper-level evidence gap in the outputs, not the tool availability issue.

## Final Quality Checklist

Before finalizing `paper_blueprint.md`, check that:

- the file reads as a Strategic Paper Blueprint
- the first section identifies the paper object, venue posture, paper type, and current input state in concise specification form
- the central research bet, contribution contract, claim strategy, novelty boundary, and scope boundary are clear
- evidence posture is strategic rather than a concrete experiment protocol
- comparison posture is strategic rather than a fixed baseline list
- narrative and visual strategy define requirements rather than detailed section or figure plans
- delegation boundaries state which tactical choices later skills will decide
- strategic defaults replace tactical option questionnaires
- every included detail would change the paper's strategic identity if altered

Before finalizing `paper_blueprint_explanation.<lang>.md`, check that:

- the file reads as a strategic validation companion in the user's language
- the file begins with confirmed user context
- confirmed user context records only information explicitly provided by the user
- working assumptions are separated from confirmed user context when assumptions are needed
- important strategic items are restated before they are explained
- validation questions ask the user to confirm strategy, not tactical choices
- tactical topics are discussed as delegated planning areas with strategic constraints
- the explanation helps the user locate disagreement at the premise, derivation, or strategic-default level

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
