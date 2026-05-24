---
name: academic-army-architect
description: >-
  Create two Markdown files for an upstream research-paper planning workflow: an English paper_blueprint.md containing a Core Paper Specification, and a user-language paper_blueprint_explanation language-suffixed Markdown file that restates the blueprint's core content and explains how each item follows from the paper's premises so the user can validate the plan. Use when the user needs venue fit, thesis shaping, problem framing, contribution boundaries, claim hierarchy, evidence obligations, novelty boundary, method abstraction, scope constraints, open planning variables, and downstream interfaces for later content-planning, experiment-planning, figure-planning, writing, or review skills. Uses deepresearch MCP for live venue, literature, exemplar, and reviewer-context evidence.
---

# Academic Army Architect

## Output Contract

The skill produces two Markdown files.

### File 1: `paper_blueprint.md`

This file is an English **Core Paper Specification**.

It defines the paper's stable upstream information for later planning skills:

- paper identity and research object
- target venue and contribution posture
- core strategy premises
- central thesis
- contribution contract
- claim hierarchy
- related-work and novelty boundary
- method abstraction
- evidence obligations
- narrative requirements
- visual argument requirements
- scope and constraint boundaries
- research risks and dependency signals
- open planning variables
- downstream planning interfaces

Write at the level of obligations, constraints, interfaces, and open variables. The blueprint states what the paper must prove and what later planning must satisfy.

Use hierarchical Markdown headings with descriptive titles.

### File 2: `paper_blueprint_explanation.<lang>.md`

This file is a user-language validation companion for the Core Paper Specification.

It helps the user judge whether the blueprint is reasonable by showing:

- what the important blueprint items actually say, in compressed user-language form
- which core premise motivates each item
- how each item follows from the premises
- how items support or constrain later content, experiment, figure, writing, and review planning
- what the user should inspect when an item feels unreasonable
- which details are intentionally left to specialized downstream planning skills

Use the user's conversation language. Preserve venue names, paper titles, method names, datasets, benchmarks, metrics, and key terms in their original language when that improves precision.

## Blueprint Abstraction Level

Use this distinction:

| Level | Purpose |
|---|---|
| Blueprint level | Define what the paper must prove, why it matters, which boundaries hold, which evidence classes are required, and what later skills must satisfy. |
| Later planning level | Turn blueprint obligations into concrete experiments, figures, section outlines, prose, implementation tasks, and review responses. |

Represent future planning detail as:

- evidence obligations instead of concrete experiment protocols
- visual argument requirements instead of fixed figure lists
- narrative requirements instead of full manuscript outlines
- baseline classes instead of exact baseline implementations
- data or workload classes instead of exact datasets or traces
- research risks and dependency signals instead of project task sequences
- open planning variables instead of prematurely fixed choices

## Core Blueprint Objects

### Claim Object

For each major claim, specify:

- statement
- role in the paper: acceptance-critical, supporting, optional, or deferred
- evidence obligation
- acceptable proof modes
- required comparison class
- metric family
- scope boundary
- current support status
- failure implication

### Evidence Obligation Object

For each evidence obligation, specify:

- supported claim
- required evidence type
- metric family
- baseline or comparison class
- data or workload class
- minimum acceptable support
- planning freedom delegated to later skills
- failure implication

### Narrative Requirement Object

For each narrative requirement, specify:

- paper-level story function
- reader belief to establish
- core concepts to foreground
- claims to avoid foregrounding
- planning freedom delegated to content-planning

### Visual Argument Requirement Object

For each visual argument requirement, specify:

- message that must become visible
- why the message matters
- related thesis or claim
- planning freedom delegated to figure-planning

### Downstream Interface Object

For each downstream skill, specify:

- information it should use from the blueprint
- constraints it should preserve
- output it should produce later
- variables it is allowed to decide

## Semantic Anchor References

`paper_blueprint.md` uses hierarchical Markdown headings for structure.

`paper_blueprint_explanation.<lang>.md` refers to blueprint items by semantic anchors: exact headings, translated headings, concise functional names, or natural-language paraphrases.

Preferred explanation references:

- the target-venue premise
- the primary claim about reference-aware adaptation
- the evidence obligation for the primary effect
- the visual requirement for showing the main tradeoff
- the novelty boundary against CAGS-style restoration
- the open variables for experiment planning
- the interface for figure-planning

Section numbers are secondary locators. The explanation remains understandable when the reader ignores all section numbers.

## Evidence Gathering

Use `deepresearch` when current venue expectations, related work, exemplars, SOTA, benchmark norms, or reviewer expectations affect the blueprint.

Gather four evidence groups:

1. Venue evidence: current CFP, review criteria, contribution categories, artifact expectations, and recent accepted-paper style.
2. Literature evidence: closest related work, required comparison classes, novelty boundary, and overclaim risks.
3. Exemplar evidence: recent storytelling exemplars, technical exemplars, and evaluation exemplars.
4. Reviewer-context evidence: likely pressure on novelty, evidence type, baselines, metrics, scope, and claims.

Use recent target-venue papers for storytelling style. Use canonical and recent papers together for methods, datasets, benchmarks, and evaluation lineage.

## Workflow

### Step 1: Parse Request

Extract topic, target venue or candidate venues, field/subfield, likely paper type, research artifact, available materials, pending materials, constraints, output language, and output directory.

Ask at most one clarification question when the paper specification would otherwise be misleading. Otherwise make explicit paper-design assumptions and continue.

### Step 2: Build Internal Research Brief

Create a compact internal brief with:

- one-sentence paper idea
- likely paper type
- research artifact
- target venue candidates
- known evidence
- evidence that controls claim scope
- likely novelty boundary
- likely evidence obligations
- likely downstream planning needs
- output language and output paths

### Step 3: Gather Live Evidence

Use deepresearch evidence to establish venue expectations, related-work boundaries, exemplar-derived patterns, evidence norms, and reviewer-context pressure.

### Step 4: Compile `paper_blueprint.md`

Use this structure:

```markdown
# Core Paper Blueprint: <Working Title>

## 1. Paper Identity
### 1.1 Working title
### 1.2 Research area
### 1.3 Target venue candidates
### 1.4 Paper type
### 1.5 Research artifact
### 1.6 Current input state

## 2. Target Venue and Contribution Posture
### 2.1 Primary target venue
### 2.2 Alternative venues
### 2.3 Expected reviewer audience
### 2.4 Accepted contribution type
### 2.5 Venue-specific evidence standard
### 2.6 Paper positioning

## 3. Core Strategy Premises
### 3.1 Target-venue premise
### 3.2 Problem premise
### 3.3 Contribution premise
### 3.4 Novelty premise
### 3.5 Evidence premise
### 3.6 Storytelling premise
### 3.7 Scope premise

## 4. Central Thesis
### 4.1 One-sentence thesis
### 4.2 Acceptance-critical paper bet
### 4.3 What would falsify or downgrade the thesis

## 5. Contribution Contract
### 5.1 Primary contribution
### 5.2 Secondary contributions
### 5.3 Supporting contributions
### 5.4 Non-contributions and boundaries

## 6. Claim Hierarchy
### 6.1 Primary claim: <descriptive claim>
### 6.2 Mechanism claim: <descriptive claim>
### 6.3 Scope or generality claim: <descriptive claim>
### 6.4 Claims to defer

## 7. Related-Work and Novelty Boundary
### 7.1 Closest work cluster: <cluster name>
### 7.2 Closest work cluster: <cluster name>
### 7.3 Required differentiation points
### 7.4 Comparison obligations
### 7.5 Overclaim boundaries

## 8. Method Abstraction
### 8.1 Core idea
### 8.2 Mechanism class
### 8.3 Inputs and outputs
### 8.4 Decision variables
### 8.5 Constraints
### 8.6 Assumptions and invariants
### 8.7 Method details delegated to later planning

## 9. Evidence Obligations
### 9.1 Evidence obligation for the primary effect
### 9.2 Evidence obligation for the mechanism
### 9.3 Evidence obligation for scope and robustness
### 9.4 Evidence obligation for cost and feasibility
### 9.5 Evidence obligation for baseline fairness

## 10. Narrative Requirements
### 10.1 Opening tension
### 10.2 Central abstraction
### 10.3 Story arc
### 10.4 Terms and concepts to foreground
### 10.5 Claims to avoid foregrounding
### 10.6 Detailed content planning delegated to later planning

## 11. Visual Argument Requirements
### 11.1 Core visual messages
### 11.2 Tradeoffs that must become visually clear
### 11.3 Evidence that likely needs visual support
### 11.4 Detailed figure planning delegated to later planning

## 12. Scope and Constraint Boundaries
### 12.1 In-scope setting
### 12.2 Out-of-scope setting
### 12.3 Accepted assumptions
### 12.4 Allowed claims
### 12.5 Deferred claims
### 12.6 Claims avoided by design

## 13. Research Risks and Dependency Signals
### 13.1 Highest-risk premise
### 13.2 Highest-risk claim
### 13.3 Highest-risk related-work boundary
### 13.4 Highest-risk evidence gap
### 13.5 What changes if each risk materializes

## 14. Open Planning Variables
### 14.1 Variables for content planning
### 14.2 Variables for experiment planning
### 14.3 Variables for figure planning
### 14.4 Variables for method planning
### 14.5 Variables for related-work planning
### 14.6 Variables for review-risk planning

## 15. Downstream Planning Interfaces
### 15.1 Interface for content-planning skill
### 15.2 Interface for experiment-planning skill
### 15.3 Interface for figure-planning skill
### 15.4 Interface for writing skill
### 15.5 Interface for review-risk skill
```

### Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Use this structure:

```markdown
# Core Paper Blueprint Explanation: <Working Title>

## Blueprint Overview

## Key Blueprint Content and Validation Entry Points

## Core Strategy Premises

## Overall Derivation from Premises to Core Specification

## Item-by-Item Blueprint Validation

## What Is Delegated to Later Planning Skills

## Key Design Tradeoffs and Their Derivations

## Fragile Derivation Chains

## Disagreement Diagnosis

## Priority Questions for User Review
```

The explanation is a standalone validation document. For each important blueprint item, first restate the essential content in the user's language, then explain the derivation and validation point:

1. Blueprint content digest: what the item says.
2. Derivation from core premises: why the item follows from the paper's premises.
3. Connections to downstream planning: how the item constrains content, experiment, figure, writing, or review planning.
4. User validation point: what the user should inspect if the item seems wrong.

Include a short table after the overview:

| Key blueprint content | Why it matters | Main user validation question |
|---|---|---|

Use semantic content labels rather than section numbers.

## DeepResearch Prompt Shape

Use this prompt shape when live evidence is needed:

```text
You are supporting a core paper-blueprint generator.

Return paper-relevant evidence for defining the upstream Core Paper Specification.

Research brief:
[RESEARCH_BRIEF]

Target venue:
[VENUE]

Return four sections:

1. Venue and storytelling evidence
   Summarize current venue expectations, contribution posture, evidence standards, and recent accepted-paper storytelling patterns.

2. Technical lineage evidence
   Summarize canonical and recent work that defines the method, system, dataset, benchmark, or evaluation lineage.

3. Related-work boundary evidence
   Summarize closest work clusters, existing solved problems, required differentiation points, comparison obligations, and overclaim boundaries.

4. Evidence and reviewer-context evidence
   Summarize evidence classes, metric families, baseline classes, data/workload classes, artifact expectations, and likely reviewer pressure.

For each source, include title, venue/year when available, source link, relevance to the proposed paper, and the lesson for blueprint design.

Use concise evidence-facing prose.
```

## Final Quality Checklist

Before finalizing `paper_blueprint.md`, check that:

- the file reads as an upstream Core Paper Specification
- the thesis, contribution contract, claim hierarchy, novelty boundary, and scope boundaries are clear
- each claim has evidence obligations, acceptable proof modes, metric families, comparison classes, support status, and failure implications
- evidence obligations define evidence types and constraints without fixing exact experimental protocols
- narrative requirements define story constraints without fixing a full manuscript outline
- visual argument requirements define messages without fixing the figure list or layout
- open planning variables identify what later skills may decide
- downstream interfaces state what each later planning skill should consume and produce

Before finalizing `paper_blueprint_explanation.<lang>.md`, check that:

- the file reads as a standalone validation companion in the user's language
- the file includes a compact overview of the core blueprint
- each important blueprint item is restated before it is explained
- each restatement contains enough concrete content for the user to evaluate the item without opening `paper_blueprint.md`
- the explanation shows how blueprint items derive from core premises
- the explanation explains how each item constrains later content, experiment, figure, writing, or review planning
- the explanation identifies which details are intentionally left to later planning skills
- the explanation helps the user locate disagreement at the premise, derivation, or detail level

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
