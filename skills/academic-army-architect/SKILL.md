---
name: academic-army-architect
description: >-
  Create two Markdown files for a research-paper design workflow: an English paper_blueprint.md containing an objective paper-design specification, and a user-language paper_blueprint_explanation.<lang>.md explaining the academic design rationale for that paper scheme. Use when the user needs venue fit, thesis shaping, problem framing, novelty boundary, method design, claim-evidence planning, experimental design, figure/table planning, paper structure, and limitation boundaries. Uses deepresearch MCP for live venue, literature, exemplar, and reviewer-context evidence.
---

# Academic Army Architect

## Output Contract

The skill produces two Markdown files.

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

Use natural section references such as `Section 7.1 Primary claim` and `Section 8.2 Main-result experiment`.

Represent uncertain evidence as claim scope, required evidence, or limitation boundaries.

Represent reviewer pressure as baseline, metric, ablation, comparison, or limitation choices.

Represent reproducibility expectations as paper-facing assets: code package, configuration, dataset or workload manifest, result tables, plotting scripts, and reproduction commands.

### File 2: `paper_blueprint_explanation.<lang>.md`

This file is a paper-strategy explanation in the user's conversation language.

It explains the paper plan itself:

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

Use descriptive section references instead of synthetic object IDs.

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

## Natural Numbering

Use natural Markdown section numbering and descriptive headings.

Preferred references:

- `Section 4.1 Closest technical lineage`
- `Section 7.1 Primary claim`
- `Section 8.2 Main-result experiment`
- `Section 9.3 Main-result figure`
- `Section 12.1 Scope boundary: limited prediction horizon`

Tables may use descriptive row labels.

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

## 2. Central Thesis
### 2.1 One-sentence thesis
### 2.2 Acceptance-critical statement
### 2.3 Contribution boundary

## 3. Problem Framing
### 3.1 Community-level pain point
### 3.2 Why the problem matters now
### 3.3 Why existing approaches are insufficient

## 4. Related-Work and Novelty Boundary
### 4.1 Closest technical lineage
### 4.2 Nearest-neighbor papers
### 4.3 Novelty boundary
### 4.4 Claims that require narrower wording

## 5. Core Idea
### 5.1 Core insight
### 5.2 Why this idea is the narrative center
### 5.3 Tradeoff changed by the idea

## 6. Method Design
### 6.1 Main mechanism
### 6.2 Method components
### 6.3 How components support the thesis
### 6.4 Method assumptions

## 7. Claims and Evidence Plan
### 7.1 Primary claim: <short natural-language claim title>
### 7.2 Mechanism claim: <short natural-language claim title>
### 7.3 Generality or scope claim: <short natural-language claim title>

## 8. Experimental Design
### 8.1 Evaluation overview
### 8.2 Main-result experiment
### 8.3 Mechanism ablation
### 8.4 Robustness, stress, or generalization test
### 8.5 Failure-case or limitation analysis

## 9. Figure and Table Plan
### 9.1 Opening problem or mechanism figure
### 9.2 Method overview figure
### 9.3 Main-result figure
### 9.4 Ablation or sensitivity figure
### 9.5 Limitation or failure-case figure

## 10. Paper Structure
### 10.1 Abstract
### 10.2 Introduction
### 10.3 Background and motivation
### 10.4 Related work
### 10.5 Method
### 10.6 Evaluation
### 10.7 Discussion and limitations
### 10.8 Conclusion

## 11. Reproducibility-Relevant Assets
### 11.1 Code and configuration assets
### 11.2 Dataset or workload assets
### 11.3 Result and plotting assets

## 12. Limitations and Scope Boundaries
### 12.1 Scope boundary: <natural-language boundary title>
### 12.2 Limitation: <natural-language limitation title>
### 12.3 Evidence requirement before broadening claims
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

### Synthetic ID Normalization

Convert synthetic labels from intermediate notes into natural section references:

| Intermediate label | Final reference |
|---|---|
| `C1` | `Section 7.1 Primary claim: <descriptive title>` |
| `E1` | `Section 8.2 Main-result experiment` |
| `F1` | `Section 9.1 Opening problem or mechanism figure` |
| `R1` | `Section 12.1 Scope boundary: <descriptive title>` |

## Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Use this structure:

```markdown
# Paper Blueprint Explanation: <Working Title>

## Overall Paper Strategy

## Target-Venue Storytelling Patterns

## Technical and Evaluation Lessons

## Paper-Plan Narrative

## Section-by-Section Explanation

## Key Design Decisions

## Evidence Gaps and Claim Scope

## Research Development Order
```

The explanation reads as a paper-strategy memo for the current research idea.

It explains:

- the paper's target-venue positioning
- the central thesis and contribution shape
- the reason for each major claim
- the related-work boundary
- the method decomposition
- the evaluation order
- the figure and manuscript strategy
- the main risks and evidence gaps
- the research development order

Use natural prose and descriptive section references.

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
- the user can understand the design without following synthetic labels or internal workflow terms
- the explanation describes why the paper plan is shaped this way

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
