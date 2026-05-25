---
name: academic-army-experiment-plan
description: >-
  Create two Markdown files for a claim-driven, venue-aware academic experiment strategy: an English experiment_plan.md for downstream AI experiment, coding, plotting, writing, and review skills, plus a user-language language-suffixed experiment_plan_explanation Markdown file for human confirmation. Use when a research idea, paper_blueprint.md, paper goals, claims, storytelling blueprint, target venue, or revision feedback must be converted into experiment objectives, story placement, evidence roles, current baselines/datasets/metrics, and downstream execution interfaces. Uses academic_army_mcp_tools.deepresearch, canonical Codex MCP tool name mcp__academic_army_mcp_tools__deepresearch, for live recent-paper, target-venue, baseline, dataset, metric, benchmark, artifact, and reviewer-expectation research.
---

# Academic Army Experiment Plan

## Output Contract

Create exactly two Markdown deliverables.

### File 1: `experiment_plan.md`

Write this file in English. Make it an AI-facing strategic experiment plan for later coding, experiment-running, plotting, paper-writing, and review-feedback skills.

The plan organizes evidence around paper claims, experiment objectives, evidence roles, and story placement. It records the core information later skills need to act efficiently:

- paper-level experimental thesis
- evidence strategy for the paper story
- claim-to-evidence map
- objective groups
- current dataset, benchmark, baseline, metric, and protocol choices when live evidence supports them
- controls, variables, and stress conditions
- expected tables, figures, qualitative artifacts, logs, and result files
- downstream execution interfaces
- priority, dependencies, evidence maturity, and feedback slots

Keep the file focused on the experiment plan itself. Encode uncertainty as `Evidence maturity`, `Required confirmation`, `Selection criterion`, `Downstream dependency`, or `Revision implication` inside the relevant objective.

### File 2: `experiment_plan_explanation.<lang>.md`

Write this file in the user's conversation language. Make it a human confirmation companion that explains why the plan is structured as it is.

Start with the user-confirmed context. Then explain the paper's core experimental thesis, how target-venue and recent-paper patterns shaped the plan, and how each objective follows from the paper's claims, story placement, and reviewer expectations.

Use readable prose, objective headings, and short tables where helpful. Refer to objective headings and semantic names rather than dense cross-reference codes.

## Required Research MCP

Use the `deepresearch` tool from the `academic_army_mcp_tools` MCP server for live research.

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical Codex MCP tool name, when exposed: `mcp__academic_army_mcp_tools__deepresearch`

Use `academic_army_mcp_tools.deepresearch` whenever target venue, field, submission year, baselines, datasets, benchmarks, metrics, evaluation protocols, artifact expectations, or recent reviewer preferences affect the plan.

Evidence from built-in web search, browser tools, documentation search, or other MCP servers is supplemental. It does not replace this skill's required live research dependency.

If `academic_army_mcp_tools.deepresearch` is unavailable, proceed from user-provided and local evidence. Represent live-research-dependent choices as evidence maturity, selection criteria, required confirmations, downstream dependencies, or revision implications inside the outputs.

## Inputs to Extract

Extract or infer:

- target venue, track, and likely submission context
- research field and subfield
- research idea, method, system, dataset, benchmark, or theoretical object under evaluation
- upstream `paper_blueprint.md` or equivalent blueprint content
- paper-level goals, claims, novelty boundary, evidence posture, and storytelling blueprint
- available resources: code, data, models, compute, hardware, testbed, traces, simulator, deployment access, annotation resources, user-study access
- known constraints: time, compute, inaccessible data, required public benchmarks, privacy limits, mandatory baselines, forbidden or unavailable baselines
- existing experiment notes, failed attempts, preliminary results, or revision feedback
- user conversation language and output directory

When an upstream `paper_blueprint.md` exists, read it first and extract:

- top-level paper goal
- central research bet
- contribution and novelty-boundary goals
- strategic claim posture
- strategic evidence posture
- scope-control goal
- storytelling and communication posture
- experiment-planning interface
- fragile goals and downgrade conditions

## Planning Principle

Treat this skill as a claim-driven evidence planner.

Plan from paper claims to evidence objectives, then from objectives to venue-calibrated experimental information. Use objective groups with strategic dependencies and downstream interfaces.

Each objective should answer:

- what claim or reviewer concern it supports
- what role it plays in the paper story
- where the result should appear in the paper narrative
- what evaluation setting, comparator, metric, and control structure can make the evidence credible
- what downstream execution, plotting, and writing skills need to consume
- how later feedback should return to this objective

## Live Research Strategy

Use live research to keep the static skill short and current. Do not store changing baseline, dataset, benchmark, metric, or venue preference facts in the skill.

Run the smallest set of deepresearch passes needed for the task:

1. **Recent venue pattern scan.** Find recent strong target-venue or adjacent top-venue papers and extract what their experiments were designed to prove, where motivation/insight/final-evaluation experiments appeared, what datasets, traces, benchmarks, baselines, metrics, user studies, testbeds, deployments, ablations, stress tests, or artifacts they used, and what reviewers are likely to expect now.
2. **High-impact pattern scan.** Find high-impact papers from the last 3-5 years and extract reusable claim-to-evidence patterns. Use older papers for evidence architecture, not for stale baseline or benchmark choices.
3. **Baseline / benchmark freshness scan.** Identify current must-compare baselines, strong optional baselines, diagnostic baselines, datasets, benchmarks, metrics, evaluation protocols, and implementation availability.
4. **Storytelling experiment scan.** Identify how recent strong papers use experiments to motivate the problem, reveal design insight, justify method components, prove final effectiveness, and show scalability, robustness, perceptual quality, deployment readiness, or artifact value.

Compress live research into:

- `venue_evidence_patterns`
- `field_current_protocols`
- `storytelling_patterns`
- `freshness_or_staleness_notes`

The final files should contain synthesized planning conclusions, not tool-call logs.

## Deepresearch Prompt Shape

Use this shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a claim-driven experiment strategy planner for an academic paper.

Research brief:
[RESEARCH_BRIEF]

Target venue and field:
[TARGET_VENUE_AND_FIELD]

Return four sections:

1. Recent venue and field evidence patterns
   Find 8-12 recent papers from the last 24 months or latest target-venue cycles, prioritizing award papers, highly cited papers, and papers with strong experiment sections. Extract the experimental thesis, datasets/traces/benchmarks/testbeds/user studies/deployments, baselines, metrics, motivation or insight experiments, final evaluation experiments, ablations, stress tests, scalability tests, robustness tests, artifact signals, and reviewer expectations.

2. Current protocols for this field
   Identify current must-compare baselines, strong optional baselines, diagnostic baselines, datasets/benchmarks for main evaluation, stress/generalization settings, metrics mapped to claims, implementation availability, and stale-risk notes.

3. High-impact experiment-design patterns
   Identify 6-10 high-impact papers from the last 3-5 years whose experiment design influenced later work. Explain the reusable claim-to-evidence pattern and which parts should not be copied blindly.

4. Storytelling placement patterns
   Explain how strong recent papers use experiments for motivation, design insight, method justification, final effectiveness, scalability/efficiency, robustness, perceptual/user evidence, deployment readiness, or artifact support.

For each source, include title, venue/year when available, link, relevance to this paper, and the lesson for experiment planning.
Use concise evidence-facing prose.
```

## Workflow

### Step 1: Parse and Normalize Inputs

Build a compact internal brief:

- one-sentence paper idea
- target venue and field
- paper type and contribution type
- method, system, dataset, benchmark, or object under evaluation
- paper-level claims
- expected paper story
- available resources and constraints
- current evidence state
- decision-critical uncertainty
- output language and output paths

Use strategic defaults when information is missing. Ask the user only when the missing information blocks venue posture, central thesis, claim strength, or resource feasibility.

### Step 2: Normalize the Experimental Thesis

Write a concise paper-level thesis:

```text
The experiments are designed to show that {method/system} solves {problem} by {mechanism}, under {venue-relevant settings}, while improving {primary outcomes} relative to {current alternatives}.
```

Adapt the template to the paper. The thesis should make the evidence strategy legible to later skills.

### Step 3: Build the Claim Graph

Extract the major claims and reviewer concerns. For each claim, identify:

- required evidence
- evidence role
- likely objective group
- target story placement
- relevant dataset/workload class
- relevant comparator class
- relevant metric family
- minimum convincing result pattern
- failure or downgrade implication

### Step 4: Run Live Venue and Field Scan

Use `academic_army_mcp_tools.deepresearch` when current venue or field information matters. Prefer recent nearest-neighbor papers for actual baselines, datasets, benchmarks, metrics, protocols, and reviewer expectations. Use canonical and high-impact papers for evidence design patterns and technical lineage.

### Step 5: Create Objective Groups

Create objective groups, not low-level execution tasks. Use stable headings:

```markdown
### Objective: <human-readable objective heading>
```

Each objective group contains:

- `Purpose in the Paper Story`
- `Supported Paper Claims`
- `Evidence Role`
- `Story Placement`
- `Evaluation Setting`
- `Comparators and Baselines`
- `Metrics and Observable Evidence`
- `Controls, Variables, and Stress Conditions`
- `Expected Tables, Figures, or Qualitative Artifacts`
- `Downstream Execution Interface`
- `Evidence Maturity and Required Confirmation`
- `Priority and Dependencies`
- `Revision and Feedback Slots`

Use evidence roles from this set when possible:

- motivation
- design insight
- main effectiveness
- ablation/mechanism
- scalability/efficiency
- robustness/stress
- generalization
- human/perceptual
- deployment/realism
- artifact/reproducibility

### Step 6: Align Objectives with Storytelling

Record where each objective belongs in the paper:

- Motivation / Introduction
- Method opening
- Method design justification
- Evaluation main results
- Evaluation ablation
- Evaluation robustness/generalization
- Evaluation efficiency/scalability
- Evaluation qualitative/perceptual/user study
- Deployment, artifact, appendix, or supplementary material

Distinguish motivation and insight experiments from final evaluation experiments. Motivation and insight experiments explain why the problem or method design matters. Final evaluation experiments prove the completed method's effectiveness, scalability, robustness, quality, realism, or practical value.

### Step 7: Compile `experiment_plan.md`

Use this structure:

```markdown
# Experiment Plan: <Working Title>

## 1. Paper-level Experimental Thesis

## 2. Evidence Strategy for the Paper Story

## 3. Live Research Synthesis
### 3.1 Venue evidence patterns
### 3.2 Field current protocols
### 3.3 Storytelling patterns
### 3.4 Freshness or staleness notes

## 4. Claim-to-Evidence Map

For each claim, specify:
- claim statement
- required evidence
- objective group
- evidence role
- story placement
- comparator or baseline class
- dataset, benchmark, trace, workload, scene, user, deployment, or simulation class
- metric or observable evidence family
- minimum convincing result pattern
- failure or downgrade implication

## 5. Experiment Objective Groups

### Objective: <heading>

#### Purpose in the Paper Story
#### Supported Paper Claims
#### Evidence Role
#### Story Placement
#### Evaluation Setting
#### Comparators and Baselines
#### Metrics and Observable Evidence
#### Controls, Variables, and Stress Conditions
#### Expected Tables, Figures, or Qualitative Artifacts
#### Downstream Execution Interface
#### Evidence Maturity and Required Confirmation
#### Priority and Dependencies
#### Revision and Feedback Slots

## 6. Cross-Experiment Coherence
### 6.1 How motivation and insight evidence lead into final evaluation
### 6.2 How objective groups support or constrain each other
### 6.3 Shared datasets, baselines, metrics, controls, and logging needs
### 6.4 Claim downgrade paths if evidence is mixed

## 7. Downstream Feedback Slots
### 7.1 Experiment execution feedback
### 7.2 Result analysis feedback
### 7.3 Plotting and figure-planning feedback
### 7.4 Paper-writing feedback
### 7.5 Review or rebuttal feedback
```

### Step 8: Compile `experiment_plan_explanation.<lang>.md`

Use the user's conversation language. Include only the explanation.

Use this structure, translated naturally when appropriate:

```markdown
# Experiment Plan Explanation: <Working Title>

## 0. 用户已明确的信息

## 1. 这份实验计划的核心出发点

## 2. 目标 venue 和近期论文模式如何影响计划

## 3. 从论文 claim 到实验目标的推导

## 4. 逐项解释 experiment_plan 中的 Objective

## 5. Baseline、dataset、metric、protocol 的取舍逻辑

## 6. Motivation / insight 实验与 final evaluation 实验如何配合

## 7. 当前最脆弱的证据链

## 8. 用户仍需确认的实验战略问题

## 9. 已委派给后续执行、绘图、写作、review skill 的内容
```

For each objective, first restate what the plan says in the user's language, then explain:

- why the objective exists
- which core claim, paper goal, novelty boundary, or reviewer concern generated it
- why its story placement fits the paper narrative
- how recent venue and field patterns shaped the choice
- why the dataset, benchmark, trace, workload, user study, deployment setting, or simulation setting is appropriate
- why the comparator or baseline posture is fair and current
- why the metric or observable evidence captures the intended claim
- how the objective connects to other objectives
- how its result would affect the paper claim
- what upstream assumption or derivation step the user should inspect if the objective feels wrong

## Confirmed Context Coverage Filter

Start the explanation with a confirmed-context ledger. Record only information explicitly supplied by the user or present in provided files. Separate working assumptions from confirmed context when assumptions are needed.

Before writing remaining user-confirmation questions, classify candidate questions:

| Classification | Output action |
|---|---|
| `covered_by_user_confirmation` | Treat the point as settled context and omit it. |
| `partially_covered` | Ask only the unresolved strategic remainder. |
| `conflicts_with_user_confirmation` | Revise the plan or mark the inconsistency as a plan issue. |
| `delegated_to_downstream_skill` | Express the point as a downstream interface, dependency, or feedback slot. |
| `unresolved_strategic_question` | Include it as a remaining strategic question. |

Questions should be strategic: central claim, venue posture, evidence role, story placement, resource feasibility, baseline/dataset freshness, claim downgrade, or feedback loop. Execution details belong in downstream interfaces.

## Positive Style Rules

Use direct planning language:

- Create exactly two deliverables.
- Use English for `experiment_plan.md`.
- Use the user's conversation language for `experiment_plan_explanation.<lang>.md`.
- Organize the plan around paper claims and experiment objectives.
- Use live deepresearch for current venue-specific baselines, datasets, benchmarks, metrics, protocols, and reviewer expectations.
- Mirror objective headings in the explanation.
- Record story placement for every objective.
- Record downstream execution interfaces and strategic dependencies.
- Encode uncertainty as evidence maturity, required confirmation, dependency, selection criterion, or revision implication.

## Machine-Readable Summary

When writing a machine-readable summary for validation, use `assets/experiment_plan_schema.yaml` and optionally run:

```bash
python scripts/validate_experiment_plan.py <experiment-plan-summary.json>
```

The summary is optional unless the user or pipeline asks for it. It is a validation aid, not one of the two required deliverables.

## Final Quality Checklist

Before finalizing `experiment_plan.md`, check that:

- the file is English-only and contains only the experiment plan
- the plan is organized around claims and objective groups
- every major claim has at least one supporting objective
- every objective traces to a paper claim, paper goal, novelty boundary, or reviewer concern
- every objective has a story placement
- motivation/insight experiments are distinct from final evaluation experiments
- baseline, dataset, benchmark, metric, and protocol choices come from live research or user-provided constraints when they are current-sensitive
- every objective includes downstream execution interface information
- the plan records strategic dependencies and downstream interfaces
- uncertainty appears as evidence maturity, confirmation need, dependency, selection criterion, or revision implication
- feedback slots exist for later experiment execution, plotting, writing, review, and plan revision

Before finalizing `experiment_plan_explanation.<lang>.md`, check that:

- the file uses the user's conversation language and contains only the plan explanation
- the file begins with user-confirmed context
- working assumptions are separated from confirmed context when needed
- the explanation restates each important plan item before explaining it
- objective headings and semantic names are the main anchors
- the explanation shows how each objective follows from core claims, venue patterns, story placement, and downstream needs
- the explanation helps the user locate disagreement at the upstream premise, claim-to-evidence mapping, venue-pattern transfer, baseline/dataset/metric choice, story placement, or downstream-interface level
- remaining questions only cover unresolved strategic issues
