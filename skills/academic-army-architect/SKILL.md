---
name: academic-army-architect
description: >-
  Create two Markdown files for a rigorous research-paper blueprint: an English-only paper_blueprint.md containing the formal blueprint, and a user-language paper_blueprint_explanation.<lang>.md explaining blueprint decisions with core-focus summary and blueprint traceability commentary. Use for venue fit, related-work positioning, claim-evidence mapping, experiment planning, figure planning, reviewer-risk analysis, and explanation grounded in recent target-venue storytelling exemplars plus technical/evaluation exemplars. Uses deepresearch MCP for live venue, literature, exemplar, and reviewer research. Do not use for prose polishing only.
---

# Academic Army Architect

## Purpose

Generate two separate Markdown files before full paper writing:

1. `paper_blueprint.md`
   - English only.
   - Contains the formal research-paper blueprint.
   - Intended for downstream research, writing, experiment, and review agents.
2. `paper_blueprint_explanation.<lang>.md`
   - Uses the user's conversation language.
   - Contains only the explanation of the blueprint decisions.
   - Intended for the human user.

Do not produce a single mixed Markdown file unless the user explicitly requests it.

The blueprint is a falsifiable research contract: every major claim must map to evidence, baselines, metrics, figures, and reviewer risks.

The explanation is an evidence-facing decision log plus traceability commentary. It explains why the blueprint is designed this way and how each major blueprint component maps to core focus items, exemplar-derived patterns, claim-evidence links, reviewer risks, and next actions. Do not reveal raw chain-of-thought or hidden scratchpad reasoning.

## Output File Contract

Always create or return exactly two main Markdown files:

- `paper_blueprint.md`
- `paper_blueprint_explanation.<lang>.md`

If an output directory is provided, write both files there. If no output directory is provided, use:

```text
paper_blueprint_outputs/
  paper_blueprint.md
  paper_blueprint_explanation.<lang>.md
```

Use a normalized BCP-47-like language suffix when possible:

- Chinese Simplified: `zh-CN`
- Chinese Traditional: `zh-TW`
- English: `en`
- Japanese: `ja`
- Korean: `ko`
- French: `fr`
- German: `de`

If the language is uncertain, infer it from the user's latest substantive message.

## Strict Content Separation

### `paper_blueprint.md`

This file must be written in English.

It may include metadata, target venue and contribution type, acceptance hypothesis, core claims, claim-evidence matrix, related-work positioning matrix, method blueprint, evaluation blueprint, figure/table storyboard, section-by-section outline, reviewer risk register, reproducibility and artifact plan, missing evidence, and next actions.

It must not include user-language explanation, reasoning summary, `why I chose this` narrative, detailed exemplar paper analysis, deepresearch process notes, raw search logs, hidden chain-of-thought, or long prose about famous papers unless directly needed in the related-work matrix.

### `paper_blueprint_explanation.<lang>.md`

This file must use the user's conversation language.

It may include interpretation of the user's idea, assumptions, target venue expectations, recent storytelling patterns, technical/evaluation patterns, how those patterns influenced the blueprint, why claims were promoted/downgraded/unsupported, why experiments/baselines/metrics/figures/sections were chosen, what was not copied from exemplar papers, uncertainty, missing evidence, and recommended next steps.

It must not include the full blueprint duplicated from `paper_blueprint.md`, the full claim-evidence matrix, the full section-by-section outline, machine-oriented YAML intended for downstream agents, raw chain-of-thought, or hidden scratchpad content.

The explanation file may reference blueprint IDs such as `C1`, `C2`, `E1`, `F3`, or `R2`.

## Explanation Depth Policy

The explanation file must contain two layers:

1. `Core Focus Summary`
   - A concise summary of the main blueprint priorities, such as venue fit, contribution framing, novelty boundary, claim-evidence alignment, evaluation validity, storytelling structure, reviewer risk, reproducibility, and next actions.
2. `Blueprint Traceability Commentary`
   - A detailed walkthrough of the formal blueprint.
   - Explains how each major section of `paper_blueprint.md` relates to core focus items and how sections depend on each other.

The explanation file must not duplicate the formal blueprint. It should explain relationships, rationale, dependencies, and usage.

Use stable IDs from the blueprint, such as `C1`, `E2`, `F3`, `R1`, `M2`, and `A1`, to refer to blueprint objects.

### Core Focus IDs

Define core focus IDs in the explanation file:

- `K1`: Venue fit and reviewer expectations
- `K2`: Recent storytelling pattern
- `K3`: Contribution framing
- `K4`: Novelty boundary
- `K5`: Claim-evidence alignment
- `K6`: Evaluation validity
- `K7`: Figure-first storytelling
- `K8`: Reviewer risk, limitation, and reproducibility control
- `K9`: Execution path and next actions

Adapt names if the user's domain requires more specific focus items, but keep the `K` ID scheme.

### Blueprint Walkthrough Requirements

For every major section in `paper_blueprint.md`, the explanation file must explain:

- what the section is for
- which core focus IDs it supports
- which exemplar patterns or venue expectations influenced it
- which claims, experiments, figures, risks, or actions it connects to
- how the user should use this section
- what would change if new evidence appears

The walkthrough must cover at least Metadata, Target Venue and Contribution Type, Acceptance Hypothesis, Core Claims, Related-Work Positioning, Method Blueprint, Evaluation Blueprint, Figure and Table Storyboard, Section-by-Section Outline, Reviewer Risk Register, Reproducibility and Artifact Plan, Missing Evidence, and Next Actions.

### Traceability Matrices

The explanation file must include at least two traceability tables.

First, a section-level mapping:

| Blueprint Section | Core Focus IDs | Related Blueprint IDs | Why This Section Exists | Downstream Impact |
|---|---|---|---|---|

Second, a claim-level mapping:

| Claim ID | Core Focus IDs | Supporting Experiments | Supporting Figures/Tables | Main Reviewer Risks | Explanation |
|---|---|---|---|---|---|

Do not copy the full claim-evidence matrix from `paper_blueprint.md`. Summarize the relationship and rationale only.

## Language Policy

Determine `output_language` as follows:

1. If the user explicitly requests an output language, use that language for the explanation file.
2. Otherwise use the dominant language of the latest substantive user message.
3. If the user mixes languages, use the dominant natural language for explanations while preserving technical terms, paper titles, venue names, datasets, benchmarks, metrics, method names, and citation keys in their original language.
4. Keep any machine-readable field names in English for downstream compatibility.

## Workflow

### Step 1: Parse Request

Extract topic, target venue or candidate venues, field/subfield, contribution type, research stage, available artifacts, constraints, output language, output directory, and explanation depth.

If explanation depth is not specified, use `standard`. Ask at most one blocking clarification question only when a useful blueprint cannot be produced otherwise. Otherwise make explicit assumptions and continue.

### Step 2: Build Research Brief

Create an internal compact brief with one-sentence idea, likely contribution type, known evidence, unknowns, likely venue candidates, highest novelty risk, highest evaluation risk, output language, and output paths.

### Step 3: Run Live Probes with DeepResearch

Use `deepresearch` unless the user explicitly provides sufficient current evidence.

Run or combine:

1. `venue_probe`: current venue expectations, review criteria, artifact/reproducibility expectations, recent accepted-paper style.
2. `literature_probe`: closest related work, required baselines, novelty boundary.
3. `exemplar_probe`: storytelling exemplars are recent only; technical exemplars are classic plus recent; evaluation exemplars are standard plus recent.
4. `reviewer_probe`: likely objections, missing evidence, overclaim risks.

## Exemplar Evidence Policy

Use `deepresearch` MCP to gather exemplar papers unless the user explicitly provides sufficient exemplars.

Do not use a single undifferentiated list of `highly cited papers`. Separate exemplars into three categories.

Use recent papers to infer current storytelling and reviewer-facing writing style; use canonical and recent papers together to infer methods, datasets, benchmarks, and evaluation norms.

### 1. Storytelling Exemplars

Purpose: analyze current storytelling, writing style, paper organization, contribution framing, figure sequencing, abstract/introduction style, limitation style, and reviewer-facing rhetoric.

Recency requirement:

- Prefer papers from the last 2-3 years or the latest 3 cycles of the target venue.
- If there are not enough relevant papers, expand to the last 5 years and explicitly mark this expansion in `paper_blueprint_explanation.<lang>.md`.
- Do not use old classic papers as primary evidence for current writing style.
- Do not use citation count as the main signal for this category, because recent papers may not yet have high citation counts.

### 2. Technical Exemplars

Purpose: analyze methods, systems, algorithms, abstractions, mechanisms, architectures, protocols, representations, or theoretical ideas.

May include older canonical papers. Should include recent nearest-neighbor papers when novelty risk is high. Use classic papers when they define the core technical lineage or standard abstraction.

### 3. Evaluation Exemplars

Purpose: analyze datasets, workloads, benchmarks, metrics, ablations, deployment evidence, artifact expectations, and evaluation norms.

May include older dataset or benchmark papers if they remain standard. Must include recent evaluation papers when benchmarks, datasets, workloads, or metrics have shifted.

### Exemplar Probe Prompt

Use this prompt shape:

```text
You are supporting a paper-blueprint generator.

Research brief:
[RESEARCH_BRIEF]

Target venue(s):
[VENUES]

Research area:
[FIELD]

Candidate contribution type:
[CONTRIBUTION_TYPE]

Task:
Find exemplar papers that should influence the paper blueprint. Do not return one generic list of highly cited papers. Separate exemplars into three categories.

Category A: storytelling_exemplars
Purpose: infer current reviewer-facing storytelling and writing style.
Requirements:
- Prefer papers from the last 2-3 years or the latest 3 cycles of the target venue.
- If insufficient, expand to the last 5 years and state that expansion.
- Prefer target-venue accepted papers, award papers, oral/spotlight papers, or recent influential papers.
- Do not rely on citation count as the primary signal.
For each paper, extract title, venue, year, source, why it is a useful storytelling exemplar, problem framing style, contribution statement style, abstract/introduction pattern, Figure 1 / teaser pattern, evidence sequencing, limitation/discussion style, transferable storytelling lesson, and non-transferable warning.

Category B: technical_exemplars
Purpose: infer method/system/algorithm/design lineage.
Requirements:
- May include older canonical papers.
- Include recent nearest-neighbor papers when novelty risk is high.
For each paper, extract title, venue, year, source, core technical idea, reusable abstraction or mechanism, assumptions, technical contribution pattern, likely baseline or citation role, and technical lesson for the proposed work.

Category C: evaluation_exemplars
Purpose: infer datasets, workloads, benchmarks, metrics, ablations, and evaluation norms.
Requirements:
- May include older dataset or benchmark papers if still standard.
- Include recent evaluation norms when the field has shifted.
For each paper, extract title, venue, year, source, datasets/workloads, baselines, metrics, ablation design, robustness/scalability/failure analysis, artifact/reproducibility expectations, and evaluation lesson for the proposed work.

Then synthesize current storytelling patterns, technical patterns, evaluation patterns, blueprint decisions affected, patterns that should not be copied blindly, uncertainty, and missing evidence.

Requirements:
- Prefer official venue pages, proceedings, ACM/IEEE/USENIX pages, arXiv, Semantic Scholar, OpenAlex, and primary papers.
- Mark uncertain claims as needs_verification.
- Do not write the final paper blueprint.
- Do not expose hidden chain-of-thought.
- Return an evidence-facing decision summary only.
```

## Step 4: Compile `paper_blueprint.md`

Write the formal English blueprint only.

Assign stable IDs to all important objects:

- Claims: `C1`, `C2`, ...
- Research questions: `RQ1`, `RQ2`, ...
- Experiments: `E1`, `E2`, ...
- Figures and tables: `F1`, `F2`, `T1`, ...
- Reviewer risks: `R1`, `R2`, ...
- Missing evidence items: `M1`, `M2`, ...
- Next actions: `A1`, `A2`, ...

Use this structure:

```markdown
# Paper Blueprint: <Working Title>

## 1. Metadata
## 2. Target Venue and Contribution Type
## 3. Acceptance Hypothesis
## 4. Core Claims
## 5. Related-Work Positioning
## 6. Method Blueprint
## 7. Evaluation Blueprint
## 8. Figure and Table Storyboard
## 9. Section-by-Section Outline
## 10. Reviewer Risk Register
## 11. Reproducibility and Artifact Plan
## 12. Missing Evidence
## 13. Next Actions
```

Do not include explanation prose, reasoning summary, exemplar analysis, or deepresearch process notes in this file.

## Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Write the user-language explanation only.

Use this structure, translated naturally into `output_language`:

```markdown
# Paper Blueprint Explanation: <Working Title>

## 1. Task Understanding
## 2. Core Focus Summary
## 3. Recent Target-Venue Storytelling Patterns
## 4. Technical and Evaluation Patterns from Relevant Papers
## 5. Overall Blueprint Design Logic
## 6. Blueprint Traceability Commentary
## 7. Claim / Experiment / Figure / Risk Mapping
## 8. How the Blueprint Uses These Patterns
## 9. Patterns the Blueprint Does Not Copy
## 10. Key Tradeoff Decisions
## 11. Main Risks and Uncertainty
## 12. Next Steps
```

Explain how the task was interpreted, assumptions made, current venue storytelling patterns found, technical/evaluation patterns found, how those patterns affected the blueprint, why specific claims/experiments/figures/sections were chosen, how each major blueprint section maps to core focus IDs, which evidence and exemplar patterns each section depends on, which downstream claims/experiments/figures/risks/missing evidence/next actions each section affects, which claims were downgraded, and what risks remain.

Do not duplicate the full blueprint. Reference blueprint IDs such as `C1`, `E2`, `F3`, and `S4`.

## Claim-Evidence Mapping

Every main claim in `paper_blueprint.md` must include claim ID, exact claim statement, why it matters, required evidence, dataset/workload/environment, metrics, baselines or why no baseline applies, ablations or controls, expected figure/table, failure condition, confidence level, likely reviewer attack, and status.

If a claim lacks evidence, label it `unsupported` and keep it out of the main contribution summary.

## Quality Gates

### Blueprint Quality Gate

Before final output, check: acceptance hypothesis is specific and falsifiable; each claim maps to evidence; baselines are fair and strong, or absence is justified; novelty boundary is grounded in related work; venue expectations are current or marked `needs_verification`; limitations are explicit; each figure/table supports at least one claim; next actions are concrete.

### File Separation Quality Gate

Fail the output if only one Markdown file is produced, the blueprint contains user-language explanation, the blueprint contains reasoning summary or explanatory essay, the blueprint contains exemplar analysis as explanatory prose, the blueprint is not English, the explanation duplicates the full blueprint, the explanation contains full claim-evidence or section-outline tables copied from the blueprint, or the explanation is in English when the user's conversation language is not English.

### Exemplar Recency Quality Gate

Fail or downgrade exemplar analysis if storytelling exemplars are primarily old classic papers, recent accepted target-venue papers were not searched, citation count is used as the main signal for recent storytelling quality, method/dataset/evaluation exemplars are forced to be recent even when older canonical references define the field, old papers are used to justify current reviewer-facing writing style, or no distinction is made between storytelling, technical, and evaluation exemplars.

### Explanation Traceability Quality Gate

Before finalizing, verify:

- the explanation file contains a `Core Focus Summary`
- the explanation file contains a section-level traceability table
- the explanation file contains a claim-level traceability table
- every major section of `paper_blueprint.md` is explained
- every main claim is mapped to core focus IDs, experiments, figures/tables, and risks
- the explanation file explains relationships and rationale, not just summaries
- the explanation file does not duplicate the full blueprint
- the blueprint file remains English-only and contains no user-language explanation
- the explanation file uses the user's language and contains no hidden chain-of-thought

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
