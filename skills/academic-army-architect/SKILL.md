---
name: academic-army-architect
description: >-
  Create two Markdown files for a research-paper design workflow: an English paper_blueprint.md containing an objective paper-design specification, and a user-language paper_blueprint_explanation.<lang>.md explaining the academic design rationale for that paper scheme. Use when the user needs venue fit, thesis shaping, problem framing, novelty boundary, method design, claim-evidence planning, experimental design, figure/table planning, paper structure, and limitation boundaries. Uses deepresearch MCP for live venue, literature, exemplar, and reviewer-context evidence.
---

# Academic Army Architect

## Output Contract

The skill produces two Markdown files.

The explanation file is not a summary of the blueprint. It is a validation companion that reconstructs the paper-level derivation from core strategy premises to blueprint details, so the user can inspect whether each item is reasonable and locate the source of disagreement.

### File 1: `paper_blueprint.md`

This file is an English paper-design specification.

It describes the research plan for the paper:

- target venue and paper type
- central thesis and contribution shape
- problem framing
- related-work and novelty boundary
- core idea
- method design
- claim and evidence plan
- experimental design
- figure and table plan
- paper structure
- reproducibility-relevant assets
- limitations and scope boundaries

Write this file in objective paper-plan prose.

Use hierarchical Markdown headings and descriptive subsection titles.

Use descriptive headings that can serve as semantic anchors in the explanation file.

Represent uncertain evidence as claim scope, required evidence, or limitation boundaries.

Represent reviewer pressure as baseline, metric, ablation, comparison, or limitation choices.

Represent reproducibility expectations as paper-facing assets: code package, configuration, dataset or workload manifest, result tables, plotting scripts, and reproduction commands.

### File 2: `paper_blueprint_explanation.<lang>.md`

This file is a paper-strategy explanation in the user's conversation language.

It explains the paper plan itself:

- what core strategy premises the plan depends on
- how each major blueprint item is derived from those premises
- how blueprint items support or constrain each other
- where the user should look when a blueprint item feels unreasonable
- how the blueprint would change if a premise, derivation, or implementation detail changes
- why the paper is positioned for the target venue
- why the central thesis is framed this way
- why the core idea is the narrative center
- why the main claims are scoped this way
- why the related-work boundary is drawn this way
- why the method is decomposed this way
- why the evaluation plan follows this order
- why the figures and tables support the story
- why the limitations and scope boundaries strengthen the claim

Write this file as a natural design memo for the current research idea.

Use semantic anchors instead of numeric section references as the main way to discuss blueprint items.

The explanation should let the user diagnose disagreement at three levels:

1. Core premise level: the target venue, problem framing, contribution framing, novelty boundary, evidence standard, storytelling style, or research strategy is wrong.
2. Derivation level: the premise is plausible, but the blueprint item does not follow from it.
3. Implementation-detail level: the item direction is right, but the concrete claim, baseline, metric, figure, or limitation needs revision.

## Content Placement Map

Place each type of information in the appropriate final object.

| Information type | Final placement |
|---|---|
| Target venue expectations | `paper_blueprint.md`, Target Venue and Paper Type |
| Recent storytelling patterns | `paper_blueprint_explanation.<lang>.md`, target-venue storytelling section |
| Technical lineage | concise positioning in the blueprint; explanatory synthesis in the explanation |
| Evaluation norms | executable evaluation plan in the blueprint; evidence-chain rationale in the explanation |
| Unverified evidence | claim scope, required evidence, or limitation boundaries |
| Reviewer concerns | baseline, metric, ablation, comparison, or limitation choices |
| Artifact requirements | reproducibility-relevant assets |
| Paper-strategy rationale | `paper_blueprint_explanation.<lang>.md` |
| User validation checkpoints | `paper_blueprint_explanation.<lang>.md`, diagnostic derivation chains and disagreement diagnosis |

## Semantic Anchor References

`paper_blueprint.md` uses hierarchical Markdown headings for structure.

`paper_blueprint_explanation.<lang>.md` refers to blueprint items by semantic anchors rather than by section numbers.

A semantic anchor can be:

- the exact blueprint heading
- a translated heading
- a concise functional name
- a natural-language paraphrase of the item

Preferred explanation references:

- the primary claim about reference-aware adaptation
- the reference-versus-Gaussian utility sweep
- the main-result experiment under dynamic network traces
- the opening scheduling-decision figure
- the baseline insufficiency risk
- the CAGS reproduction evidence gap
- the per-frame instrumentation step

Section numbers are secondary locators. Place them after the semantic anchor when useful, not before it.

The explanation should remain understandable when the reader ignores all section numbers.

## Descriptive Heading Requirement

Each important subsection in `paper_blueprint.md` has a self-contained descriptive heading.

A heading identifies both the role of the item and its substantive content.

Use headings like:

- `Primary claim: <specific claim>`
- `Mechanism claim: <specific mechanism>`
- `Main-result experiment: <specific comparison and condition>`
- `Ablation experiment: <specific mechanism being tested>`
- `Scope boundary: <specific limitation>`
- `Evidence requirement: <specific missing evidence before broadening claims>`

The heading should be meaningful enough that the explanation file can discuss it without relying on the section number.

## Internal Evidence Handling

Use live research as evidence input.

Convert intermediate notes into paper-facing objects:

- venue findings become paper type, audience, and evidence standard
- storytelling findings become introduction, figure, and paper-structure choices
- technical findings become method positioning and related-work boundary
- evaluation findings become datasets, workloads, baselines, metrics, ablations, and stress tests
- uncertainty becomes claim scope, required evidence, or limitation boundaries
- reviewer pressure becomes comparison, metric, ablation, or scope design

Final Markdown prose contains only the paper scheme and the paper-design rationale.

## Language Policy

Determine `output_language` as follows:

1. If the user explicitly requests an output language, use that language for the explanation file.
2. Otherwise use the dominant language of the latest substantive user message.
3. If the user mixes languages, use the dominant natural language for explanations while preserving technical terms, paper titles, venue names, datasets, benchmarks, metrics, method names, and citation keys in their original language.

## Workflow

### Step 1: Parse Request

Extract topic, target venue or candidate venues, field/subfield, contribution type, research stage, available paper materials, constraints, output language, and output directory.

Ask at most one clarification question when the paper design would otherwise be misleading. Otherwise make explicit paper-design assumptions and continue.

### Step 2: Build Internal Research Brief

Create a compact internal brief with:

- one-sentence paper idea
- likely paper type
- target venue candidates
- known evidence
- evidence that controls claim scope
- likely novelty boundary
- likely evaluation pressure
- output language and output paths

### Step 3: Gather Live Evidence

Use `deepresearch` when current venue expectations, related work, exemplars, SOTA, benchmark norms, or reviewer expectations affect the blueprint.

Gather four evidence groups:

1. Venue evidence: current CFP, review criteria, artifact expectations, recent accepted-paper style.
2. Literature evidence: closest related work, required baselines, novelty boundary.
3. Exemplar evidence: recent storytelling exemplars, technical exemplars, and evaluation exemplars.
4. Reviewer-context evidence: likely baseline, metric, novelty, scope, and evidence pressure.

### Step 4: Compile `paper_blueprint.md`

Use this structure:

```markdown
# Paper Blueprint: <Working Title>

## 1. Target Venue and Paper Type
### 1.1 Target venue fit
### 1.2 Expected paper type
### 1.3 Audience and evidence standard

## 2. Paper Strategy Premises
### 2.1 Target-venue premise
### 2.2 Problem premise
### 2.3 Contribution premise
### 2.4 Novelty premise
### 2.5 Evidence premise
### 2.6 Storytelling premise
### 2.7 Research-strategy premise

## 3. Central Thesis
### 3.1 One-sentence thesis
### 3.2 Acceptance-critical statement
### 3.3 Contribution boundary

## 4. Problem Framing
### 4.1 Community-level pain point
### 4.2 Why the problem matters now
### 4.3 Why existing approaches are insufficient

## 5. Related-Work and Novelty Boundary
### 5.1 Closest technical lineage
### 5.2 Nearest-neighbor papers
### 5.3 Novelty boundary
### 5.4 Claims that require narrower wording

## 6. Core Idea
### 6.1 Core insight
### 6.2 Why this idea is the narrative center
### 6.3 Tradeoff changed by the idea

## 7. Method Design
### 7.1 Main mechanism
### 7.2 Method components
### 7.3 How components support the thesis
### 7.4 Method assumptions

## 8. Claims and Evidence Plan
### 8.1 Primary claim: <short natural-language claim title>
### 8.2 Mechanism claim: <short natural-language claim title>
### 8.3 Generality or scope claim: <short natural-language claim title>

## 9. Experimental Design
### 9.1 Evaluation overview
### 9.2 Main-result experiment
### 9.3 Mechanism ablation
### 9.4 Robustness, stress, or generalization test
### 9.5 Failure-case or limitation analysis

## 10. Figure and Table Plan
### 10.1 Opening problem or mechanism figure
### 10.2 Method overview figure
### 10.3 Main-result figure
### 10.4 Ablation or sensitivity figure
### 10.5 Limitation or failure-case figure

## 11. Paper Structure
### 11.1 Abstract
### 11.2 Introduction
### 11.3 Background and motivation
### 11.4 Related work
### 11.5 Method
### 11.6 Evaluation
### 11.7 Discussion and limitations
### 11.8 Conclusion

## 12. Reproducibility-Relevant Assets
### 12.1 Code and configuration assets
### 12.2 Dataset or workload assets
### 12.3 Result and plotting assets

## 13. Limitations and Scope Boundaries
### 13.1 Scope boundary: <natural-language boundary title>
### 13.2 Limitation: <natural-language limitation title>
### 13.3 Evidence requirement before broadening claims
```

For each claim subsection, include:

- claim statement
- why it matters to the thesis
- required evidence
- required baselines
- required metrics
- expected figure or table
- failure condition
- current evidence status
- connection to the thesis

For each experiment subsection, include:

- purpose
- dataset or workload
- baselines
- metrics
- evidence role
- expected paper result

For each figure/table subsection, include:

- message
- narrative role
- data source
- paper placement
- claim supported

### Synthetic Label Normalization

Convert synthetic labels from intermediate notes into descriptive headings or functional names:

| Intermediate label | Final reference |
|---|---|
| `C1` | `Primary claim: <specific claim>` |
| `E1` | `Main-result experiment: <specific comparison and condition>` |
| `F1` | `Opening problem or mechanism figure: <specific message>` |
| `R1` | `Scope boundary: <specific limitation>` |

## Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Use this structure:

```markdown
# Paper Blueprint Explanation: <Working Title>

## Core Strategy Premises

## Overall Derivation from Premises to Paper Plan

## Section-by-Section Blueprint Validation

## Key Design Tradeoffs and Their Derivations

## Fragile Derivation Chains

## Disagreement Diagnosis

## Priority Questions for User Review
```

The explanation reads as a paper-strategy memo for the current research idea.

It explains:

- the core premises behind the paper plan
- how the major blueprint items are derived from those premises
- how the blueprint items support or constrain each other
- how the user can locate the source of disagreement
- the paper's target-venue positioning
- the central thesis and contribution shape
- the reason for each major claim
- the related-work boundary
- the method decomposition
- the evaluation order
- the figure and manuscript strategy
- the main risks and evidence gaps
- the research development order

Use natural prose and semantic anchors.

### Blueprint Item Explanation Pattern

For every major section and important subsection of `paper_blueprint.md`, explain it as a derivation from the core premises.

Each explanation should cover:

- item summary: what the blueprint item says, named by title or functional phrase
- premise source: which core paper-strategy premise motivates the item
- derivation: why that premise leads to this item
- connections: which other blueprint parts depend on it or constrain it, using semantic item names
- user validation point: what the user should inspect if the item seems unreasonable
- revision consequence: what parts of the blueprint would need to change if the item is revised

Write this as natural prose, not as a rigid field list.

Use relationship language such as:

- this claim requires...
- this experiment tests...
- this figure makes visible...
- this scope boundary protects...
- this evidence requirement controls...

Use semantic item names as the connective tissue. Section numbers may appear once as optional locators.

### Diagnostic Derivation Chains

The explanation file highlights the most important derivation chains in the paper plan.

Each chain explains:

- the starting premise
- the blueprint decisions derived from it
- the evidence needed for the chain to hold
- the most likely failure point
- which blueprint sections change if the chain fails

### Disagreement Diagnosis

The explanation file helps the user locate the source of disagreement.

Use paper-level diagnosis:

- if target venue framing seems wrong, explain which thesis, claim, evidence, and paper-structure choices depend on it
- if contribution framing seems wrong, explain which method and claim choices depend on it
- if the primary claim seems too strong, explain which evidence premise and scope boundary control it
- if baselines seem excessive or insufficient, explain which novelty boundary controls them
- if evaluation feels misaligned, explain which evidence premise controls the experiment order and metrics
- if a limitation feels too narrow or too broad, explain which claim boundary it protects

## DeepResearch Prompt Shape

Use this prompt shape when live evidence is needed:

```text
You are supporting a paper-blueprint generator.

Return paper-relevant evidence for designing the research plan.

Research brief:
[RESEARCH_BRIEF]

Target venue:
[VENUE]

Return four sections:

1. Venue and storytelling evidence
   Summarize recent target-venue or adjacent-venue papers that show current problem framing, contribution framing, figure sequencing, evidence sequencing, and limitation style.

2. Technical lineage evidence
   Summarize canonical and recent papers that define the method, system, dataset, benchmark, or evaluation lineage.

3. Related-work boundary evidence
   Summarize the closest works, their methods, their evidence, and the precise comparison points for the proposed paper.

4. Evaluation and reviewer expectation evidence
   Summarize expected baselines, datasets, workloads, metrics, ablations, robustness checks, artifact expectations, and likely reviewer concerns.

For each source, include title, venue/year when available, source link, relevance to the proposed paper, and the lesson for blueprint design.

Use concise evidence-facing prose.
```

## Final Quality Checklist

Before finalizing `paper_blueprint.md`, check that:

- the file reads as an English paper-design specification
- every major claim has required evidence, baselines, metrics, and a failure condition
- every evaluation item is tied to a paper claim
- every figure or table has a defined message and paper placement
- every limitation is tied to claim scope
- reproducibility-relevant assets support claims or figures
- section headings are descriptive and naturally numbered

Before finalizing `paper_blueprint_explanation.<lang>.md`, check that:

- the file reads as a paper-strategy memo in the user's language
- the explanation focuses on paper positioning, venue fit, storytelling, technical lineage, evaluation design, risks, evidence gaps, and research order
- each major blueprint section is explained in natural prose
- the user can understand the design through semantic item names rather than numbered-section lookup
- the explanation describes why the paper plan is shaped this way
- the explanation helps the user judge whether each major blueprint item is reasonable
- the explanation identifies whether disagreement points to a premise, a derivation, or an implementation detail

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
