---
name: academic-army-architect
description: >-
  Create two Markdown files for a strategic research-paper blueprint: an English, AI-facing paper_blueprint.md and a user-language paper_blueprint.explain.md. The blueprint is a concise paper strategy specification for downstream content, method, experiment, figure, writing, and review-planning skills. It uses `academic_army_mcp_tools.deepresearch` as the required live research MCP tool for venue, literature, exemplar-paper, evaluation-expectation, and reviewer-context evidence.
---

# Academic Army Architect

## Output Contract

The skill produces exactly two Markdown files with strict separation of responsibilities:

- `paper_blueprint.md`
- `paper_blueprint.explain.md`

Do not add language suffixes, translated filename components, or auxiliary explanation files.

### File 1: `paper_blueprint.md`

This file is an English, AI-facing strategic paper blueprint. It contains only the paper strategy and downstream planning constraints.

Allowed content:

1. `Paper Identity`
2. `Strategic Thesis`
3. `Canonical Resource Model and Terminology`
4. `Core Strategic Goals`
5. `Claim and Scope Architecture`
6. `Evidence Objectives`
7. `Downstream Skill Contract`
8. `Open Strategic Variables`, only as unresolved variables with machine-consumable status fields

The blueprint answers:

- what kind of paper this is
- what the core claim and strategic bet are
- which goals later skills must preserve
- what evidence-level phenomena the paper must establish
- what content, method, experiment, and figure planning must inherit

The blueprint is not a user-facing explanation. Do not put user-confirmation ledgers, research-process notes, review-defense language, source analysis, or rationale paragraphs in this file.

`Open Strategic Variables` may appear in the blueprint, but only as planning state. Do not write user-facing confirmation prompts there. State the default propagation rule once at the start of the section, then use this format for each variable:

```markdown
Default propagation rule: downstream skills must use each variable's current conservative stance unless the user or evidence resolves that variable.

### <Variable name>
Status: unresolved.
Affects: <paper identity, claim scope, method planning, experiment planning, figure planning, or related downstream areas>
Current conservative stance: <neutral stance to use until the variable is resolved>
Allowed resolutions: <short semicolon-separated set of strategic resolutions>
```

Any corresponding user-facing question, when the variable remains unresolved, belongs only in `paper_blueprint.explain.md`.

### File 2: `paper_blueprint.explain.md`

This file is a user-language validation companion. Its function is to help the user confirm whether the blueprint items are reasonable.

Allowed content:

1. A short first-check summary of unresolved strategic decisions
2. Confirmation state, with separate buckets for confirmed facts, preferences not locked, and unresolved strategic variables
3. Working assumptions, separated from confirmed facts and preferences
4. Research signals used, compressed to load-bearing sources and grouped by source role
5. Core starting points behind the blueprint, each with rationale and only unresolved confirmation targets
6. Item-by-item explanation of the blueprint, including each core goal, open strategic variable, and downstream contract
7. Remaining strategic choices for confirmation, deduplicated against confirmed inputs
8. Change impact if confirmed inputs change
9. Evidence-dependent claim calibration, separated from user-input changes

Use the user's conversation language for the full explanation file, including section headings, field labels, table column labels, and repeated phrases. Preserve technical terms, venue names, paper titles, datasets, benchmarks, metrics, and method names in their original language when that improves precision.

The explanation explains the paper strategy, not the skill's workflow. For example, explain why the paper is positioned as reference-aware ABR; do not explain why this skill uses a particular file format.

## Required Research MCP

This skill's live research dependency is the `deepresearch` tool from the `academic_army_mcp_tools` MCP server.

Use the exact tool identity:

- server: `academic_army_mcp_tools`
- tool: `deepresearch`
- canonical Codex MCP tool name, when exposed: `mcp__academic_army_mcp_tools__deepresearch`

All mentions of `deepresearch` in this skill refer to `academic_army_mcp_tools.deepresearch`.

Use `academic_army_mcp_tools.deepresearch` for current venue evidence, related-work evidence, exemplar-paper evidence, evaluation-expectation evidence, and reviewer-context evidence.

Evidence from built-in web search, browser tools, documentation search, or other MCP servers is supplemental and does not satisfy this skill's required live research dependency.

The final Markdown files should contain paper-level conclusions derived from evidence, not tool-call logs, MCP implementation details, or search-process narration.

## Confirmed-Inputs Mechanism

Start `paper_blueprint.explain.md` with a short first-check summary, then a confirmation-state section with the user's-language equivalents of `Confirmed`, `Preferred but Not Locked`, and `Still to Confirm`. Translate all generic labels in these sections; do not leave English headings such as `Role`, `What it showed`, or `User-Confirmed Inputs` in a Chinese or other non-English explanation unless they are paper terms.

For Chinese explanations, use these bucket labels: `已确认`, `偏好但未锁定`, and `仍需确认`.

`Confirmed` records only paper-strategy information explicitly provided or locked by the user, such as:

- research idea
- target venue or venue preference
- intended paper type
- existing technical substrate or method foundation
- existing experiment or prototype foundation
- preferred or prohibited strategic directions
- intended downstream planning skills
- desired abstraction level
- explanation-file purpose

Use three mutually exclusive confirmation-state buckets:

- `User-confirmed facts`: explicit locked paper-strategy facts. These are settled context.
- `User preferences, not locked`: preferences, expectations, likely directions, or desired evidence that the user mentioned but did not lock as final strategy.
- `Unresolved strategic variables`: decisions still open because they affect paper identity, claim scope, evidence posture, or downstream contracts.

An item can appear in only one bucket. If a statement includes uncertainty words such as `expected`, `preferred`, `likely`, `should include`, `if possible`, or equivalent user-language phrasing, treat it as a preference or working assumption unless the user explicitly locked it. If a preference affects a strategic variable, keep the preference in the preference bucket and put only the unresolved remainder in `Remaining Strategic Choices for Confirmation`.

Do not include output paths, workspace paths, generated file locations, tool names, or execution environment details in the explanation file. Keep those in internal execution metadata or final run logs.

Keep user-mentioned but unresolved preferences separate from confirmed inputs. Use `Preferred but Not Locked` for items the user mentioned or leaned toward but did not lock as final paper strategy. Use `Working Assumptions` for defaults the skill uses to produce a coherent blueprint despite missing strategic information.

Examples:

- Confirmed: target venue is INFOCOM; CAGS is the closest substrate; novelty is not a restoration model.
- User-mentioned preference: method should remain interpretable; evidence should go beyond average PSNR.
- Working assumption: prototype-anchored systems paper; segment/chunk-level plus visible-region control until granularity is resolved.
- Open strategic variable: deployment boundary, control granularity, dynamic-scene breadth, claim strength.

Before writing any remaining confirmation question, check whether `Confirmed` already covers it. If a fact appears in `Confirmed`, treat it as settled context everywhere in the explanation. Do not ask the user to confirm it again in the first-check summary, item rationales, open-variable explanations, or remaining choices.

The first-check summary should shrink as the confirmed-inputs ledger grows. It may contain:

- unresolved strategic variables that still affect paper identity, claim scope, or downstream contracts
- derived consequences of confirmed inputs that the user may want to inspect for reasonableness

It should not contain direct re-confirmation of confirmed inputs. Keep it to 3-5 short lines that summarize the unresolved decision space. Put the detailed reasoning, confirmed portion, default stance, and downstream impact only in `Remaining Strategic Choices for Confirmation`. Do not phrase the same unresolved decision twice.

Question filtering:

| Classification | Output action |
|---|---|
| `covered_by_user_confirmation` | Treat it as settled context and omit it from remaining questions. |
| `partially_covered` | Ask only the unresolved strategic remainder. |
| `conflicts_with_user_confirmation` | Revise the blueprint or mark the inconsistency as a blueprint issue. |
| `delegated_to_downstream_skill` | Express it as a downstream planning boundary, not a user question. |
| `unresolved_strategic_variable` | Include it under `Remaining Strategic Choices for Confirmation`. |

Across iterative runs, move newly confirmed strategic points into the confirmed-inputs ledger. As confirmed inputs grow, remaining strategic choices should shrink unless the user changes the paper direction, venue posture, top-level claim, or strategic boundary.

Before finalizing, compare the three buckets. If the same semantic item appears in more than one bucket, resolve it by this precedence:

1. explicit user confirmation
2. unresolved strategic variable, when the user has not locked it and it changes paper strategy
3. preference or working assumption, when it guides but does not settle strategy

Open questions may ask about target venue, core novelty, system boundary, deployment boundary, dynamic-scene breadth, control granularity, claim strength, paper type, or evidence posture. Do not ask tactical questions about exact algorithms, datasets, traces, figure counts, statistical tests, device setups, baseline implementations, section order, or plotting choices.

## Strategic Abstraction Level

The blueprint operates only at Levels 0-2:

| Level | Scope |
|---|---|
| Level 0: Paper identity | Research area, target venue posture, paper type, research object. |
| Level 1: Strategic thesis and goals | Main thesis, central bet, acceptance target, core strategic goals. |
| Level 2: Goal-derived constraints | Canonical resource model, terminology, claim architecture, scope boundary, evidence objectives, downstream contracts. |

Later specialized skills handle Levels 3-4:

| Level | Scope |
|---|---|
| Level 3: Tactical planning | Exact experiments, datasets, traces, workloads, baselines, metrics, figure list, layouts, section structure, algorithm variants. |
| Level 4: Execution planning | Scripts, run order, implementation tasks, plotting commands, writing tasks, rebuttal execution. |

Every item in `paper_blueprint.md` must directly constrain later planning or change the paper's strategic identity if altered. Compress lower-level details into strategic requirements, acceptable design spaces, delegated planning variables, or evidence-dependent claim calibration.

Keep only strategic invariants in the blueprint:

- thesis
- novelty boundary
- resource model
- strategic goals
- claim and scope calibration
- evidence objectives
- downstream contracts

Move detailed controller choices, exact experiment options, exact metric lists, exact figure choices, reference-generation alternatives, implementation variants, and proof-form options into later planning skills unless the detail changes the paper's strategic identity or has been explicitly confirmed by the user.

## Strategic/Tactical Filter

Use this filter before writing blueprint content:

| Tactical impulse | Blueprint-level form |
|---|---|
| Choose a controller family | State the required control property and leave controller family open. |
| List exact baselines | State baseline families or comparison posture. |
| Pick datasets or traces | State the uncertainty or workload dimension that evidence must cover. |
| Specify metric formulas | State the outcome family and evidence objective. |
| Set figure count or layout | State the visual argument that figures must make legible. |
| Outline sections | State the story movement content planning must preserve. |
| Create task sequence | State the strategic dependency or decision-critical uncertainty. |
| Commit to tile-based organization | State spatial-unit or visible-region priority and leave the concrete unit open. |

Examples:

- Blueprint-level: `The method must model deadline feasibility across server rendering, transfer, restoration, and display.`
- Too tactical: `Use robust MPC, Lyapunov optimization, online primal-dual, or structured bandit/RL.`
- Blueprint-level: `Evidence must isolate the marginal value of joint adaptation across Gaussian resources and reference resources.`
- Too tactical: `Compare against fixed-FoV reference, perfect-viewport oracle, and bandwidth oracle.`
- Blueprint-level: `Baseline families should separate substrate benefit from adaptation benefit.`
- Too tactical: `Include baseline A, B, C, and D with exact oracle variants.`
- Blueprint-level: `The visual strategy must make the Gaussian/reference resource surface legible.`
- Too tactical: `Use one decision-surface figure, one pipeline figure, and one evaluation figure.`

If a tactical detail is explicitly specified by the user, record it in the explanation's confirmed-inputs ledger and preserve it as confirmed context. Otherwise, delegate it.

## Positive Scope and Claim Calibration

Write scope boundaries in positive, proposal-shaped language.

Preferred language:

- `Novelty scope. The paper contributes a reference-aware network control layer over existing compression and restoration substrates.`
- `Claim calibration. The breadth of the final system claim is determined by the measured strength and robustness of the target phenomenon.`
- `Opening communication priority. Introduce the central resource-control abstraction before implementation details.`

Avoid defensive phrasing in the blueprint, including long lists of what the paper does not claim. Replace rejection-risk language with contribution boundary, novelty scope, evidence-dependent scope, or claim calibration.

Use positive constraint language in `paper_blueprint.md`, especially in goals and downstream contracts. Prefer action-oriented strategic constraints:

- `Frame the contribution as a reference-aware control layer over the CAGS/restoration substrate.`
- `Treat CAGS and restoration quality improvement as substrate; claim the paper contribution in resource-control decisions.`
- `Preserve the Gaussian/reference resource tradeoff as the first visible abstraction.`

Limit `must` to strict machine-contract invariants where a downstream skill would otherwise violate the paper identity. Replace defensive forms such as `must be X rather than Y`, `not restoration`, `not generic ABR`, and `not graphics-only` with positive boundaries such as `Frame as X`, `Treat Y as substrate`, `Scope the claim to Z`, or `Calibrate breadth by evidence`.

## Source-Use Rules

Source analysis belongs in `paper_blueprint.explain.md`, not in `paper_blueprint.md`.

In the explanation, include a `Research Signals Used` section. Classify each source by role and explain how it influenced the blueprint:

- `Closest technical substrate`: work that establishes the usable technical base.
- `Venue posture`: current venue CFPs, accepted-paper patterns, or systems expectations that justify the target positioning.
- `Closest competing systems`: recent work that already covers adjacent axes such as viewport prediction, saliency-aware tiling, layered/progressive delivery, segment-level adaptation, or learned QoE/ABR.
- `Storytelling exemplars`: recent target-venue or adjacent top-venue papers, preferably from the last 1-3 years, used to infer current story movement and writing style.
- `Method precedents`: canonical or recent method/control/optimization precedents. These may be older when they are field-standard.
- `Evaluation precedents`: benchmark, metric, dataset, trace, prototype, or measurement precedents. These may mix older standards and recent domain work.

For writing style and storytelling, prefer recent papers. For methods, datasets, baselines, and metrics, older canonical sources are acceptable when they remain standard.

Do not put a bare source list in either file. Every cited source in the explanation must have a source role and a concise lesson for the blueprint.

Research-signal synthesis must extract patterns, not only summarize papers. For recent high-impact or target-venue exemplars, explain why they are persuasive for this blueprint:

- how they define a new control abstraction or resource model
- how their first figure, opening claim, or introduction makes the core idea legible
- how they calibrate claim breadth against evidence strength
- how they separate substrate contributions from the paper's own contribution
- how their evaluation style supports a systems or networking claim

Use these patterns to justify blueprint choices such as thesis shape, novelty boundary, evidence posture, and downstream contracts.

Write research signals pattern-first. Each load-bearing signal should contribute a reusable writing or evidence pattern, then connect that pattern to a blueprint decision. Use this shape in the user's language:

- Pattern: the transferable lesson from the paper or venue.
- Source basis: the source evidence supporting the pattern.
- Blueprint consequence: the thesis, goal, scope boundary, evidence objective, or contract changed by the pattern.

If a source only supports background context and does not yield a reusable pattern, move it to `Additional background signals` or omit it. Example pattern: strong INFOCOM-style systems papers make a new resource-control abstraction visible before implementation details, then use evidence to calibrate claim breadth.

Source budget rule for the explanation:

- The main `Research Signals Used` section should contain at most 6-8 load-bearing signals.
- Each load-bearing signal must state localized equivalents of `role`, `what it showed`, `persuasive pattern`, and `which blueprint choice it influenced`.
- Additional sources should be compressed into `Additional background signals` with at most one sentence per role, or omitted when they do not change a blueprint choice.
- Avoid long raw URL stacks. Keep links only when source traceability helps the user verify the blueprint.
- `Storytelling exemplars` must be recent, preferably from the last 1-3 years or the latest 3 venue cycles, and must explain their introduction/story movement influence.
- Older works may be `Method precedents` or `Evaluation precedents`, but they cannot support claims about current reviewer-facing writing style.

In `paper_blueprint.md`, at most include brief `Context anchors` lines inside `Paper Identity`, such as:

- `Closest substrate: CAGS-style 3DGS volumetric streaming with VQ-based Gaussian LoD/compression layers and server-rendered low-resolution reference images for client-side color restoration.`
- `Closest competing control axis: recent 3DGS streaming systems already study saliency/viewport-aware spatial partitioning, progressive or layered Gaussian delivery, segment-level DASH-style adaptation, and learned bitrate/QoE optimization. The paper's boundary is not generic 3DGS bitrate adaptation; it is the Gaussian/reference resource substitution decision under deadline, coverage, and compute constraints.`

## Terminology Stabilization

When the research idea introduces a new control object or resource dimension, define it once in `Canonical Resource Model and Terminology`, then reuse the same term throughout.

For RefABR-like ideas, prefer `Gaussian resource` and `reference resource` as canonical terms. Use `bits` only when discussing bandwidth consumption. A `reference resource` may include resolution, viewpoint match, FoV coverage, render timing, transfer priority, restoration compute, and deadline usefulness; it is not only a bit allocation.

Use neutral scope terminology when dynamic breadth is not confirmed. Prefer `interactive 3DGS volumetric media streaming` until the user confirms static-scene, dynamic-sequence, or combined scope. In `Research object`, use this two-part shape when breadth is open:

```markdown
Current conservative object: interactive 3DGS volumetric media streaming over a CAGS-compatible reference-assisted substrate.
Claim expansion variable: whether the first submission claims static 3DGS scenes, dynamic 3DGS video, or both is governed by Open Strategic Variable: Dynamic-scene breadth.
```

Define these interface terms when relevant:

- `Delivery unit`: a placeholder abstraction for the scheduling granularity used by downstream method planning. Until control granularity is resolved, it denotes a segment/chunk-level decision horizon with visible-region subpriorities.
- `Reference state`: the lifecycle status of a reference resource, including requested, rendered, queued, transferred, decoded, restored, consumed, stale, mismatched, or unusable.
- `Reference usefulness`: the expected visible-region quality gain of a reference resource conditioned on view match, coverage, timeliness, restoration cost, and deadline feasibility.

Use stable metric families before examples. Prefer:

- `Visible-region fidelity`
- `Deadline reliability`
- `Interaction responsiveness`
- `Resource and compute efficiency`
- `Risk and waste behavior`

Use precise but not over-specific terminology. If a detail is not confirmed by the user or the closest source, write a broader strategic term. For example, prefer `VQ-based Gaussian LoD/compression layers` when the source only confirms VQ. Introduce specialized acronyms such as `SVQ` only when the user has confirmed them or the source evidence explicitly supports them.

Use `spatial-unit priority` or `visible-region priority` instead of `tile priority` unless tile-based organization is user-confirmed or evidence-confirmed. Tiles can remain an open tactical implementation choice for method or experiment planning.

## Strategic Consistency Rules

Do not assert a final resolution for any variable that is listed in `Open Strategic Variables`.

Common consistency cases:

- If deployment boundary is open, describe the paper as `prototype-anchored` rather than `end-to-end deployed`. Example: `Prototype-anchored networking systems paper with an explicit online control formulation, trace-driven evaluation, measured system components, and evidence toward interactive end-to-end feasibility.`
- If controller proof posture is open, use `explicit online control formulation`, not `formal control model`.
- If dynamic-scene breadth is open, use neutral `volumetric media` wording and reference `Open Strategic Variable: Dynamic-scene breadth`.
- If control granularity is open, describe control at the segment/chunk plus visible-region level until implementation granularity is fixed.
- If controller proof posture is open, state required control properties rather than proof form or algorithm family.

Open-variable consistency rule: any variable listed as unresolved must not be asserted as final elsewhere. Earlier sections may only state the current conservative stance or reference the open variable.

Claim calibration rule: do not repeat claim breadth logic in multiple places. If `Claim strength` is an open variable, write:

```markdown
The final claim level is governed by Open Strategic Variable: Claim strength. Evidence planning should preserve enough measurement coverage to distinguish among the allowed claim-strength resolutions.
```

Baseline fairness rule: baseline families may be listed strategically, but baseline instantiation details are delegated. If classic ABR baselines are mentioned, specify that they require a fair mapping from bitrate choices to Gaussian/reference resource choices.

For RefABR-like blueprints, include `Control granularity` as an open strategic variable when not user-confirmed:

```markdown
### Control granularity
Status: unresolved.
Affects: online state/action definition, deadline model, evaluation trace format, prototype instrumentation.
Current conservative stance: describe control at the segment/chunk plus visible-region level until the implementation granularity is fixed.
Allowed resolutions: chunk-level; frame-level; spatial-unit-level; hybrid chunk-level Gaussian resource control plus frame-level reference resource scheduling.
```

## Downstream Skill Contract

The `Downstream Skill Contract` section should be concise and machine-consumable. For each downstream skill, use this schema:

```markdown
### <Skill Area> Contract
Purpose: <one sentence>
Preserve:
- <strategic constraint>
- <strategic constraint>
Open tactical choices:
- <delegated choice>
- <delegated choice>
```

Use the relevant subset of these contract areas:

- `Content-Planning Contract`
- `Method-Planning Contract`
- `Experiment-Planning Contract`
- `Figure-Planning Contract`
- `Review-Planning Contract`, only when the user has requested review planning or the downstream skill list includes review-planning
- `Writing-Planning Contract`, only when it adds constraints not already covered by the content-planning contract

The contract should not repeat full goal definitions. It should reference goal titles or concise strategic phrases already defined in `Core Strategic Goals`. Merge or omit contracts whose preserve lists would substantially duplicate another contract. In particular, do not create both content-planning and writing-planning contracts merely to repeat venue-facing story, abstract framing, introduction framing, or related-work organization.

Contract closure rule: every downstream skill area named anywhere in the blueprint must have a corresponding contract in `Downstream Skill Contract`, or the obligation must be explicitly routed into a defined contract. For example, baseline-planning obligations usually belong under `Experiment-Planning Contract` unless the user has a separate baseline-planning skill. If the blueprint mentions review planning, include `Review-Planning Contract` or remove the review-planning reference. Do not leave undefined downstream names such as `Baseline planning`, `Review planning`, or `Writing planning` in goals or evidence objectives without a matching contract or routing sentence.

For `Writing-Planning Contract`, prefer venue-fit and contribution-legibility phrasing:

```markdown
Purpose: Preserve venue-fit and contribution legibility in title, abstract, introduction, and related work.
```

## Workflow

### Step 1: Parse Request

Extract topic, target venue or candidate venues, field/subfield, likely paper type, research object, available materials, pending materials, confirmed inputs, working assumptions, strategic constraints, output language, and output directory.

### Step 2: Build Internal Research Brief

Create a compact internal brief with:

- one-sentence paper idea
- user-confirmed inputs
- working assumptions
- likely target venue posture
- likely paper type
- research object
- likely strategic thesis
- likely core strategic goals
- decision-critical strategic uncertainty
- downstream planning skills expected to consume the blueprint
- output language and output paths

### Step 3: Gather Live Evidence

Use evidence returned by `academic_army_mcp_tools.deepresearch` to establish venue posture, related-work boundary, recent storytelling patterns, evidence posture, and source-role lessons.

### Step 4: Compile `paper_blueprint.md`

Use this structure:

```markdown
# Paper Blueprint: <Working Title>

## 1. Paper Identity
### Research idea
### Target venue posture
### Paper type
### Research object
### Context anchors

## 2. Strategic Thesis
### Main thesis
### Central bet
### Acceptance target

## 3. Canonical Resource Model and Terminology
### Canonical resource terms
### Control object
### Delivery unit
### Reference state
### Reference usefulness
### Deadline feasibility model
### Metric families

## 4. Core Strategic Goals

### <Goal Title>
Objective: <one sentence>
Strategic function: <one sentence>
Downstream constraints:
- <constraint>
- <constraint>
Success signal: <strategic success signal>

## 5. Claim and Scope Architecture
### Main claim
### Supporting claims
### Novelty scope
### Positive scope boundary
### Evidence-dependent claim calibration

## 6. Evidence Objectives
### Outcome families to test
### Phenomena to establish
### System-level outcomes
### Baseline families
### Evidence dimensions to cover
### Tactical choices delegated to experiment planning

## 7. Downstream Skill Contract
### Content-Planning Contract
### Method-Planning Contract
### Experiment-Planning Contract
### Figure-Planning Contract
### <Optional referenced contract, only if the blueprint references that downstream skill>

## 8. Open Strategic Variables
Default propagation rule: downstream skills must use each variable's current conservative stance unless the user or evidence resolves that variable.

### <Variable name>
Status: unresolved.
Affects: <downstream planning areas>
Current conservative stance: <neutral stance until resolved>
Allowed resolutions: <resolution set>
```

Use 5-6 core strategic goals unless the paper truly needs fewer or more. Each goal appears once with its full definition. Later sections may refer to goal titles or short phrases, but should not rewrite the full goal.

Do not include `Current input state`, `Why this goal matters`, `Failure or revision implication`, `Strategic Risks`, `Goal Dependency Map`, `Sources Used`, `Confirmation prompt`, `Confirm whether`, or user-facing process notes in the blueprint.

### Step 5: Compile `paper_blueprint.explain.md`

Use this structure in the user's language. The English names below are semantic placeholders; translate them and all local field labels in the actual file:

```markdown
# <User-language title equivalent to "Paper Blueprint Explanation">: <Working Title>

## 0. <User-language title equivalent to "What You Should Check First">

## 1. <User-language title equivalent to "Confirmation State">
### <User-language title equivalent to "Confirmed">
### <User-language title equivalent to "Preferred but Not Locked">
### <User-language title equivalent to "Still to Confirm">

## 2. <User-language title equivalent to "Working Assumptions">

## 3. <User-language title equivalent to "Research Signals Used">
### <User-language title equivalent to "Load-bearing signals">
### <User-language title equivalent to "Additional background signals">

## 4. <User-language title equivalent to "Core Starting Points">

## 5. <User-language title equivalent to "Blueprint Items and Rationale">

## 6. <User-language title equivalent to "Remaining Strategic Choices for Confirmation">

## 7. <User-language title equivalent to "Change Impact if Confirmed Inputs Change">

## 8. <User-language title equivalent to "Evidence-Dependent Claim Calibration">
```

`What You Should Check First` should be a 3-5 line strategic status snapshot, not a second confirmation section. Summarize the unresolved decision space in compact prose or bullets. Do not include detailed rationale, confirmed portions, downstream impacts, or direct confirmation wording here; those belong in `Remaining Strategic Choices for Confirmation`.

The confirmation-state section must use three visible buckets in the user's language:

- `Confirmed`: explicit locked facts only.
- `Preferred but Not Locked`: user preferences or expectations that guide the default stance but do not settle strategy.
- `Still to Confirm`: unresolved strategic variables only, named briefly without detailed reasoning.

`Working Assumptions` contains defaults inferred by the skill to make a coherent blueprint. Do not mix inferred defaults into confirmed facts.

For each core starting point, include:

1. the starting point
2. why it matters for the paper strategy
3. the remaining strategic uncertainty, only if it is not already covered by confirmed inputs

For each important blueprint item, first restate the blueprint content in the user's language, then explain:

1. which core starting point produced it
2. how it supports the paper strategy
3. which other blueprint items it constrains
4. which downstream skills must inherit it
5. what strategic confirmation point remains, if any and only if not already confirmed

`Blueprint Items and Rationale` must explain at item level, not only section level. Include separate explanation items for:

- each top-level blueprint section
- each core strategic goal
- each open strategic variable
- each downstream contract

Write these explanations as short prose blocks, not as a fixed five-line template. Each block should naturally:

- restate the blueprint item before explaining it
- explain the core reason or research-signal pattern behind it
- connect it to the thesis, goals, claim scope, evidence objectives, or downstream contracts
- mention actionable uncertainty only when the item still depends on an unresolved strategic variable

Avoid repeated labels such as `blueprint restatement`, `derivation source`, `relationship to other parts`, `downstream skill constraints`, and `user should check` for every item. Use semantic anchors such as exact headings, translated headings, concise functional names, or natural-language paraphrases. Avoid relying on section numbers.

When explaining English blueprint sections in a Chinese or other non-English explanation, use localized headings with the English blueprint term in parentheses on first mention, such as `论文身份（Paper Identity）` or `下游规划契约（Downstream Skill Contract）`. Avoid English-only explanation headings like `Paper Identity`, `Strategic Thesis`, or `Downstream Contract` unless the user's dialogue language is English.

`Remaining Strategic Choices for Confirmation` must use this template:

```markdown
### <Strategic variable>

已确认部分：<what the Confirmed bucket already settles>

未确认部分：<the remaining strategic variable>

当前默认立场：<the blueprint's current conservative stance>

不同选择会改变什么：<paper identity, claim scope, method, evidence, figure, or writing implications>
```

Omit any strategic variable from this section when the `Confirmed` bucket fully resolves it. If the confirmed inputs partially resolve it, ask only about the unresolved remainder and explicitly state why it remains unresolved.

Separate `Change Impact if Confirmed Inputs Change` from `Evidence-Dependent Claim Calibration`. The former covers changes in user-provided inputs such as venue, scope, deployment boundary, or novelty boundary. The latter covers experiment-outcome contingencies, such as reference usefulness being broad, narrow, or deployment-specific.

Do not create a long standalone `Downstream Planning Implications` section. Downstream implications belong inside each item-level explanation and each downstream-contract explanation. If a summary is useful, keep it to at most five short lines and avoid repeating the contract.

Before finalizing the explanation, read the confirmation sections together and remove repeated questions. Most item-level rationales should be rationale statements, not confirmation prompts.

## `academic_army_mcp_tools.deepresearch` Prompt Shape

Use this prompt shape when live evidence is needed:

```text
Tool: academic_army_mcp_tools.deepresearch

You are supporting a strategic paper-blueprint generator.

Return paper-relevant evidence for defining an upstream AI-facing paper strategy specification and a user-language validation explanation.

Research brief:
[RESEARCH_BRIEF]

Target venue:
[VENUE]

Return six sections:

1. Venue posture
   Summarize current venue expectations, likely contribution categories, evidence standards, and recent accepted-paper storytelling patterns.

2. Closest technical substrate and literature boundary
   Summarize closest work clusters, solved problems, strategic differentiation, comparison posture, and positive novelty scope.

3. Closest competing systems
   Summarize recent systems that already cover adjacent control axes such as viewport prediction, saliency-aware tiling, layered/progressive Gaussian delivery, segment-level adaptation, and learned QoE/ABR.

4. Storytelling exemplars
   Use recent target-venue or adjacent top-venue papers when available. Extract persuasive patterns: control abstraction, first-figure or opening-claim legibility, claim calibration, substrate-vs-contribution separation, and evidence style.

5. Method and evaluation precedents
   Summarize canonical and recent precedents that affect method posture, evaluation posture, metrics, workloads, and comparison families.

6. Source-role table
   For each source, include title, venue/year when available, source link, role among closest technical substrate / venue posture / closest competing system / storytelling exemplar / method precedent / evaluation precedent, persuasive pattern when relevant, and the lesson for blueprint design.

Use concise evidence-facing prose.
```

## Internal Validation Pass

Before finalizing, run these checks mentally.

### File Separation Check

`paper_blueprint.md` contains only the paper strategy. It does not contain:

- user-confirmed inputs
- `the user has provided`
- `current input state`
- `why this matters`
- `this blueprint uses`
- `this skill`
- `reviewers may otherwise`
- `failure implication`
- `confirmation prompt`
- `confirm whether`
- `the user should confirm`
- source lists or source-role analysis

The explanation contains user confirmation, derivation, and source-role analysis.

### Redundancy Check

Each core strategic goal has one complete definition. Other sections reference the goal title or short strategic phrase instead of repeating the full definition.

Run a deduplication pass across both files before finalizing:

- metric families appear once in canonical terminology; later sections reference or group them instead of relisting them
- central claim language appears once in the thesis or claim section; goals and explanations paraphrase only as needed
- Gaussian/reference substitution or equivalent core novelty is compactly stated once, then referenced by title or short phrase
- clean substrate boundary is stated once in novelty scope, then referenced instead of repeating in identity, context anchors, goals, and contracts
- downstream contracts do not duplicate each other, especially content-planning and writing-planning contracts
- content-planning and figure-planning contracts do not repeat the same resource-tradeoff legibility instruction; one owns story movement and the other owns visual argument
- `Default propagation rule` appears once globally in `Open Strategic Variables`
- confirmation questions appear only in the opening check list or remaining strategic choices, and only for unresolved strategic variables

### Tactical Leakage Check

If the blueprint names a concrete algorithm family, controller proof option, dataset, trace, metric formula, figure count, required figure, statistical test, device setup, reference-generation alternative, exact baseline, or concrete spatial partition such as tiles, verify that the user explicitly specified it and that it affects strategic identity. If not, move it to an open tactical choice in the downstream contract or to the explanation as delegated detail.

### Contradiction Check

If a variable appears in `Open Strategic Variables`, earlier blueprint sections use the current conservative stance and do not assert one allowed resolution as final. Pay special attention to deployment boundary, dynamic-scene breadth, controller proof posture, and control granularity.

### Overcommitment Check

Terms such as `formal model`, `end-to-end prototype`, `dynamic video`, `mobile/edge`, `theorem`, `regret`, or `multi-user` require either confirmed input or an open-variable conservative stance. Otherwise rewrite them as unresolved variables, current conservative stance, or delegated tactical choices.

### Terminology Check

Canonical terms are defined once and reused consistently. Specialized acronyms such as `SVQ` are introduced only when confirmed by the user or source evidence. `Reference resource` is not collapsed into `reference bits` except when discussing bandwidth consumption.

The canonical model defines Gaussian resource, reference resource, reference usefulness, reference state, delivery unit, deadline feasibility, and metric families.

### Metric and Claim Redundancy Check

Metric families and claim-strength levels are defined once and referenced thereafter. If `Claim strength` is open, `Evidence-dependent claim calibration` references that open variable instead of restating a separate claim ladder.

### Baseline Fairness Check

Baseline families remain strategic. Exact baselines, traces, datasets, devices, and statistics remain delegated unless user-confirmed. Classic ABR baselines require a fair action-space mapping to Gaussian/reference resource choices.

### Defensive Tone Check

Rewrite defensive language into positive scope and claim calibration:

- `must not` -> `novelty scope` or `contribution boundary`
- `avoid` -> `communication priority` or `scope priority`
- `downgrade` -> `claim calibration` or `evidence-dependent scope`
- `reviewers can reject` -> `acceptance target` or `evidence standard`

### Question Deduplication Check

Each remaining confirmation question in the explanation corresponds to an unresolved strategic variable not covered by the `Confirmed` bucket. Remove tactical questions and questions already answered by confirmed context. Search the explanation for repeated confirmation verbs and collapse duplicates into one remaining-choice item.

### Source-Role Check

Every source in the explanation is categorized as venue posture, closest technical substrate, closest competing system, storytelling exemplar, method precedent, or evaluation precedent, with a concise lesson. A bare source list is not valid. For recent high-impact or target-venue exemplars, include the persuasive pattern used by the blueprint, not only a source summary.

### Explanation Alignment Check

Every open strategic variable in the blueprint appears in the explanation. It becomes a user confirmation point only when it is not already covered by the `Confirmed` bucket; otherwise explain it as settled context or remove it from open variables.

### Confirmed-Input Hygiene Check

Only user-explicit paper-strategy facts appear under `Confirmed`. User-mentioned but unresolved preferences move to `Preferred but Not Locked`; inferred assumptions move to `Working Assumptions`; output paths and execution metadata stay out of the explanation file.

### Open-Question Deduplication Check

A remaining strategic choice cannot ask for something already confirmed. If partially confirmed, it must state `confirmed part` and `unresolved part`.

### Source Budget and Freshness Check

The main `Research Signals Used` section contains at most 6-8 load-bearing signals. Storytelling exemplars are recent and influence story movement; older works are used only as method or evaluation precedents.

### Skill-Meta Language Check

Remove phrases that explain the skill implementation, such as `from the skill's terminology stabilization rule`, `from the skill file contract`, `this skill decided`, or equivalent translations. Explain the paper rationale instead.

### Item-Level Explanation Check

Every top-level blueprint section, every core strategic goal, every open strategic variable, and every downstream contract has a corresponding explanation item.

### Evidence-vs-Input Separation Check

User input changes and experimental outcome contingencies appear in separate sections: `Change Impact if Confirmed Inputs Change` and `Evidence-Dependent Claim Calibration`.

### Explanation Compression Check

Each core judgment is explained fully once. Later sections refer to the relevant starting point, source role, metric family, novelty boundary, or contract instead of restating it in full.

### Final Artifact Audit

Before delivery, audit the generated files as artifacts, not only as prose:

- filenames are exactly `paper_blueprint.md` and `paper_blueprint.explain.md`
- `paper_blueprint.md` is English and AI-facing; `paper_blueprint.explain.md` uses the user's dialogue language for headings, labels, and explanatory prose
- the explanation's first-check summary is 3-5 short lines and does not duplicate the detailed `Remaining Strategic Choices for Confirmation`
- confirmed facts, preferences not locked, unresolved variables, and working assumptions are mutually exclusive
- no confirmed fact is repeated as a question
- every downstream skill area referenced anywhere in the blueprint has a matching contract or is explicitly routed into a defined contract
- baseline obligations are routed through experiment planning unless a baseline-planning contract is explicitly defined
- review-planning references appear only when a review-planning contract is present or the user requested review planning
- repeated metric lists, novelty-boundary statements, Gaussian/reference substitution statements, and confirmation prompts have been merged or replaced by references
- blueprint constraints use positive boundaries and strategic verbs; `must` appears only for strict machine-contract invariants

## Final Quality Checklist

Before finalizing `paper_blueprint.md`, check that:

- it uses the required strategic structure, with optional open strategic variables
- it is English, declarative, specification-like, and AI-facing
- open strategic variables state one section-level `Default propagation rule`; each variable uses `Status`, `Affects`, `Current conservative stance`, and `Allowed resolutions`, not user-facing prompts
- each item directly constrains later planning or the paper's strategic identity
- no goal's full definition appears more than once
- canonical resource terms, delivery unit, reference state, reference usefulness, and metric families are defined once and referenced later
- scope is written as positive contribution boundary and claim calibration
- evidence objectives stay above exact experiment protocol
- baseline guidance stays at the baseline-family level unless user-confirmed
- visual and content guidance states strategic requirements, not exact figure or section plans

Before finalizing `paper_blueprint.explain.md`, check that:

- it is in the user's language
- it starts with a localized first-check summary, then a localized confirmation-state section with `Confirmed`, `Preferred but Not Locked`, and `Still to Confirm`
- all generic headings, labels, and table columns are in the user's language
- confirmed facts, preferences not locked, unresolved variables, and working assumptions are separated
- output paths and execution metadata are absent from the explanation file
- research signals are limited to load-bearing sources, categorized by role, and linked to blueprint choices
- each major blueprint item is restated before its rationale
- every core goal, open variable, and downstream contract receives item-level explanation
- the explanation helps the user locate disagreement at the starting-point, derivation, or downstream-contract level
- remaining strategic choices state confirmed part, unresolved part, current default, and impact
- evidence-dependent claim calibration is separate from user-input change impact
- remaining strategic choices are filtered by confirmed inputs and do not ask tactical questions
