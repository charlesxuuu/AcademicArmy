---
name: academic-army-architect
description: >-
  Create two Markdown files for a research-paper design workflow: an English paper_blueprint.md containing an objective paper-design specification, and a user-language paper_blueprint_explanation.<lang>.md explaining only the academic design rationale for that paper scheme. Use when the user needs venue fit, thesis shaping, problem framing, novelty boundary, method design, claim-evidence planning, experimental design, figure/table planning, paper structure, and limitation boundaries. Uses deepresearch MCP for live venue, literature, exemplar, and reviewer-context research, but never exposes tool process, file-format rationale, downstream-agent usage, TODO lists, or execution logs in final outputs. Do not use for prose polishing only.
---

# Academic Army Architect

## Purpose

Generate two separate Markdown files before full paper writing:

1. `paper_blueprint.md`
   - English only.
   - Contains only the formal paper-design scheme.
   - Describes the paper's thesis, framing, method, claims, evidence plan, figures, structure, reproducibility-relevant assets, and scope boundaries.
2. `paper_blueprint_explanation.<lang>.md`
   - Uses the user's conversation language.
   - Explains only why the paper scheme is designed this way.
   - Explains academic choices: venue framing, storyline, technical lineage, method organization, evidence chain, figure logic, and limitation boundaries.

Do not produce a single mixed Markdown file unless the user explicitly requests it.

The explanation file must explain paper-design rationale, not skill behavior. It must never explain why the skill outputs two files, why the blueprint uses a specification format, how tools were called, how later agents should consume the files, or what the user should do next.

## Final Output Boundary

### `paper_blueprint.md`

This file must be written in English.

It may include:

- target venue and paper type
- central thesis
- problem framing
- related-work and novelty boundary
- core idea
- method design
- claims and evidence plan
- experimental design
- figure and table plan
- paper structure
- reproducibility-relevant assets
- limitations and scope boundaries

It must not include:

- skill workflow explanation
- file-format rationale
- user-language explanation
- tool calls or tool status
- deepresearch, MCP, web search, rate limits, probes, scraping, PDF parsing, or source extraction process
- downstream agent usage
- project-management TODOs
- execution order for the project
- user-facing advice
- cautionary prose
- second-person instructions
- reasoning summaries
- hidden chain-of-thought
- sections named `Metadata and Input State`, `Review Risk Mitigation Plan`, `Evidence Gaps and Dependencies`, or `Execution Plan`
- sections named `Artifact cautions` or `Assumptions to validate`

### `paper_blueprint_explanation.<lang>.md`

This file must use the user's conversation language.

It may explain:

- why the central thesis is framed this way
- why the problem framing fits the target venue
- why the core idea is the right narrative center
- why the method components support the thesis
- why the claims are scoped this way
- why baselines, metrics, datasets, ablations, stress tests, and qualitative examples are arranged this way
- why figure/table plan serves the story
- why limitations and scope boundaries are written this way
- how recent target-venue papers influence storytelling choices
- how canonical or high-impact technical anchors influence method, baseline, dataset, metric, and novelty boundary choices

It must not explain:

- why the skill uses a blueprint/specification/implementation-plan format
- why there are two output files
- how downstream agents should use the files
- which agent should read which section
- deepresearch, MCP, web search, rate limits, probes, scraping, PDF parsing, output directories, source extraction, or local files
- tool failures or retrieval status
- the generation process, prompt process, workflow design, or internal reasoning process
- project-management next steps, TODOs, execution order, or user recommendations
- evidence gaps as project dependencies
- reviewer risk mitigation plan as a named section

If evidence is missing and it materially affects the paper design, express it as a paper-facing scope boundary, limitation, or required evidence item inside the academic scheme. Do not present it as a user TODO or execution dependency.

## Natural Numbering Policy

Do not use artificial object IDs such as `C1`, `C2`, `E1`, `F1`, `R1`, `A1`, `B1`, `K1`, `D1`, `AR1`, or similar synthetic labels in either final Markdown file.

Use natural Markdown section numbering and descriptive headings.

Preferred references:

- `Section 4.1 Primary claim`
- `Section 7.2 Main-result experiment`
- `Section 8.3 Main-result figure`
- `Section 11.2 Scope boundary: limited prediction horizon`

Tables may use descriptive row labels, but must not introduce synthetic ID columns unless the user explicitly requests a machine-readable schema.

## Internal-Only Artifacts

The skill may maintain internal notes such as `research_trace`, `source_notes`, `tool_failures`, `retrieval_status`, `evidence_gaps`, `implementation_order`, `generation_decisions`, and `workflow_notes`.

These internal artifacts must never be written into `paper_blueprint.md` or `paper_blueprint_explanation.<lang>.md`.

Before writing final files, convert internal notes as follows:

- venue expectations become paper-facing venue and evidence standards
- related-work concerns become novelty-boundary statements
- missing evidence becomes required evidence, claim scope, or limitation boundaries
- reviewer concerns become baseline, metric, ablation, or limitation rationale
- storytelling patterns become figure/table and paper-structure choices
- tool failures and rate limits are discarded from final prose

## Language Policy

Determine `output_language` as follows:

1. If the user explicitly requests an output language, use that language for the explanation file.
2. Otherwise use the dominant language of the latest substantive user message.
3. If the user mixes languages, use the dominant natural language for explanations while preserving technical terms, paper titles, venue names, datasets, benchmarks, metrics, method names, and citation keys in their original language.
4. Keep paper titles, method names, dataset names, metric names, and venue names in their original language when translation would reduce precision.

## Workflow

### Step 1: Parse Request

Extract topic, target venue or candidate venues, field/subfield, contribution type, research stage, available paper materials, constraints, output language, and output directory.

Ask at most one blocking clarification question only when a useful blueprint cannot be produced otherwise. Otherwise make explicit paper-design assumptions and continue.

### Step 2: Build Internal Research Brief

Create a compact internal brief with:

- one-sentence paper idea
- likely paper type
- target venue candidates
- known evidence
- unknown evidence affecting claim scope
- likely novelty boundary
- likely evaluation pressure
- output language and output paths

This brief is internal. Do not write it into final Markdown files.

### Step 3: Run Live Probes with DeepResearch

Use `deepresearch` unless the user explicitly provides sufficient current evidence.

Run or combine:

1. `venue_probe`: current venue expectations, review criteria, artifact/reproducibility expectations, recent accepted-paper style.
2. `literature_probe`: closest related work, required baselines, novelty boundary.
3. `exemplar_probe`: storytelling exemplars are recent only; technical exemplars are classic plus recent; evaluation exemplars are standard plus recent.
4. `reviewer_context_probe`: likely baseline, metric, novelty, scope, and evidence pressures.

Deepresearch output is evidence input only. It must not be copied as process narration into final files.

## Exemplar Evidence Policy

Do not use a single undifferentiated list of `highly cited papers`. Separate exemplars into three categories.

Use recent papers to infer current storytelling and reviewer-facing writing style. Use canonical and recent papers together to infer methods, datasets, benchmarks, and evaluation norms.

### 1. Storytelling Exemplars

Purpose: infer current problem framing, contribution framing, abstract/introduction style, figure sequencing, limitation style, and reviewer-facing rhetoric.

Recency requirement:

- Prefer papers from the last 2-3 years or the latest 3 cycles of the target venue.
- If there are not enough relevant papers, expand to the last 5 years and mark the expansion internally.
- Do not use old classic papers as primary evidence for current writing style.
- Do not use citation count as the main signal for this category, because recent papers may not yet have high citation counts.

### 2. Technical Exemplars

Purpose: infer methods, systems, algorithms, abstractions, mechanisms, architectures, protocols, representations, theoretical ideas, or canonical baselines.

May include older canonical papers. Should include recent nearest-neighbor papers when novelty risk is high.

### 3. Evaluation Exemplars

Purpose: infer datasets, workloads, benchmarks, metrics, ablations, deployment evidence, qualitative evidence, artifact expectations, and evaluation norms.

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
Find exemplar papers that should influence the paper design. Do not return one generic list of highly cited papers. Separate exemplars into three categories.

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

Then synthesize:
1. current storytelling patterns for the target venue
2. technical patterns relevant to the proposed method
3. evaluation patterns and likely reviewer expectations
4. which paper-design decisions should change because of these patterns
5. which patterns should not be copied blindly
6. uncertainty that affects claim scope

Requirements:
- Prefer official venue pages, proceedings, ACM/IEEE/USENIX pages, arXiv, Semantic Scholar, OpenAlex, and primary papers.
- Mark uncertain claims as needs_verification.
- Do not introduce synthetic labels such as C1, E1, F1, R1, B1, A1, or K1.
- Do not write the final paper blueprint.
- Do not expose hidden chain-of-thought.
- Return evidence-facing findings only, not tool-process narration.
```

## Step 4: Compile `paper_blueprint.md`

Write the formal English paper-design scheme only.

Use natural Markdown section numbering and descriptive subsection titles. Do not assign synthetic object IDs.

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
### 4.4 Claims that should not be made

## 5. Core Idea
### 5.1 Core insight
### 5.2 Why this idea should be the narrative center
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

Do not include explanation prose, reasoning summary, exemplar analysis, tool-process notes, project-management next steps, TODOs, execution order, or file-usage guidance in this file.

For each claim, experiment, figure, limitation, and asset, use descriptive headings and compact paper-facing fields.

Example:

```markdown
### 7.1 Primary claim: <short natural-language claim title>

**Claim statement.**
...

**Why it matters to the thesis.**
...

**Required evidence.**
...

**Required baselines.**
Use descriptive baseline names, not `B1/B2/B3`.

**Required metrics.**
...

**Failure condition.**
...

**Connected paper elements.**
Main-result experiment in Section 8.2; main-result figure in Section 9.3; scope boundary in Section 12.1.
```

## Step 5: Compile `paper_blueprint_explanation.<lang>.md`

Write the user-language explanation only.

The explanation object is the paper scheme, not the skill workflow.

Use this structure, translated naturally into `output_language`:

```markdown
# Paper Blueprint Explanation: <Working Title>

## Core Judgment

## How Target-Venue Storytelling Patterns Shape the Blueprint

## How the Technical Lineage Shapes the Method Boundary

## Why the Main Line Is <core idea>

## Why the Claims Are Split This Way

## Why the Method Is Organized This Way

## Why the Experiments Are Arranged This Way

## Why the Figures and Tables Are Designed This Way

## Why These Limitations and Boundaries Are Needed
```

The explanation must discuss academic design rationale only:

- thesis shaping
- problem framing
- venue fit
- core idea selection
- novelty boundary
- method-to-claim relationship
- experiment-to-claim relationship
- baseline, dataset, metric, and ablation rationale
- figure/table narrative role
- limitation and scope rationale

Do not include:

- why the formal blueprint uses an implementation-plan or specification format
- why there are two files
- how to use the two files
- downstream agents
- tool calls, deepresearch, MCP, web search, probes, scraping, PDFs, rate limits, output directories, or local files
- generation process or internal reasoning process
- next steps, TODOs, execution order, or project status
- named sections such as `Review Risk Mitigation Plan`, `Evidence Gaps and Dependencies`, or `Execution Plan`

## Synthetic ID Normalization

If `deepresearch` or intermediate notes use synthetic IDs, remove them before writing final files.

Convert:

- `C1` into `Section 7.1 Primary claim: <descriptive title>`
- `E1` into `Section 8.2 Main-result experiment`
- `F1` into `Section 9.1 Opening problem or mechanism figure`
- `R1` into `Section 12.1 Scope boundary: <descriptive title>`
- `A1` into an internal note only, not final prose

Do not expose synthetic IDs in either final Markdown file.

## Leakage Check for Explanation

Before finalizing `paper_blueprint_explanation.<lang>.md`, reject or rewrite any paragraph that answers one of these questions:

- Why did the skill choose this output format?
- How should downstream agents use the file?
- What tools did the system call?
- Did deepresearch succeed, fail, hit rate limits, inspect PDFs, or use MCP/web search?
- What is the execution order for the project?
- What should the user do next?
- What internal files, directories, prompts, or traces were used?

Keep only paragraphs that answer:

- Why is this thesis appropriate?
- Why is this venue framing appropriate?
- Why is this method structure appropriate?
- Why are these claims scoped this way?
- Why are these experiments, baselines, metrics, and figures needed?
- Why are these limitations part of the paper's claim boundary?

## Quality Gates

### File Separation Quality Gate

Fail the output if only one Markdown file is produced, the blueprint contains user-language explanation, the blueprint contains reasoning summary or explanatory essay, the blueprint contains exemplar analysis as explanatory prose, the blueprint contains user-facing cautions, the blueprint is not English, the explanation duplicates the full blueprint, the explanation contains full claim-evidence or section-outline tables copied from the blueprint, or the explanation is in English when the user's conversation language is not English.

### Paper-Design Explanation Quality Gate

Before finalizing the explanation file, verify:

- it explains only the paper scheme's academic design rationale
- it does not explain skill workflow, file format, tool use, source retrieval, or downstream agent usage
- it does not mention deepresearch, MCP, web search, probes, rate limits, PDFs, output directories, or local file handling
- it does not include next steps, TODOs, execution order, or project-management recommendations
- it does not present evidence gaps as project dependencies
- it frames missing evidence as claim scope, required evidence, or limitations
- it is organized around thesis, venue, technical lineage, core idea, claims, method, experiments, figures, and limitations
- it contains no hidden chain-of-thought

### Natural Numbering Quality Gate

Before finalizing both Markdown files, verify:

- no synthetic object IDs appear, including `C1`, `C2`, `E1`, `F1`, `R1`, `A1`, `B1`, `D1`, `AR1`, or `K1`
- the formal blueprint is organized by natural Markdown section numbering
- each important blueprint item has a descriptive heading
- cross-references use section names or natural descriptions, not artificial IDs
- the formal blueprint remains paper-facing and objective
- the explanation file remains human-facing and focused on paper-design rationale

### Exemplar Recency Quality Gate

Fail or downgrade exemplar analysis if storytelling exemplars are primarily old classic papers, recent accepted target-venue papers were not searched, citation count is used as the main signal for recent storytelling quality, method/dataset/evaluation exemplars are forced to be recent even when older canonical references define the field, old papers are used to justify current reviewer-facing writing style, or no distinction is made between storytelling, technical, and evaluation exemplars.

When writing a machine-readable summary for validation, use `assets/blueprint_schema.yaml` and optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```
