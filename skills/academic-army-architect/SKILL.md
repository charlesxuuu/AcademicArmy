---
name: academic-army-architect
description: >-
  Create rigorous research-paper blueprints from ideas, drafts, codebases, experiment results, references, or target venues. Use for venue fit, related-work positioning, claim-evidence mapping, evaluation planning, figure planning, reviewer-risk analysis, and user-language explanation. Uses deepresearch MCP to analyze current venue expectations, closest related work, and high-impact papers from the target venue/field, then distills transferable excellence patterns to justify blueprint decisions. Do not use for prose polishing only.
---

# Academic Army Architect

## Purpose

Generate a structured paper blueprint before full paper writing.

This skill is an evidence-aware blueprint compiler. It stores only stable decision protocol: how to ask for evidence, constrain claims, mine exemplar patterns, validate structure, and produce an actionable output. It is not a venue database, paper-case library, SOTA tracker, or literature survey cache.

The workflow has four stages:

1. `research_brief`: understand the user's paper idea.
2. `evidence_probe`: use `deepresearch` for venue, related work, benchmark, artifact, and reviewer evidence.
3. `exemplar_pattern_mining`: use `deepresearch` to analyze high-impact papers and distill transferable excellence patterns.
4. `blueprint_compiler`: align the current blueprint with evidence and exemplar patterns, then explain decisions in the user's language.

The final output has two layers:

1. `Blueprint`: the formal research-paper blueprint.
2. `Explanation`: a user-facing reasoning summary / decision log in the user's conversation language.

The explanation layer must summarize auditable decisions, not reveal raw chain-of-thought, hidden scratchpad content, or private internal reasoning.

## Core Policy

Fetch live information through `deepresearch` for:

- venue CFPs, author instructions, review criteria, artifact policies, and reproducibility expectations
- latest or closest related work
- recent SOTA, benchmarks, datasets, leaderboards, and implementation artifacts
- high-impact papers from the target venue and related field
- common reviewer expectations for the venue or subfield

Do not invent citations, venue rules, paper claims, benchmark status, influence claims, or related-work deltas. If a fact is not verified by user input or `deepresearch`, mark it `needs_verification`.

Treat `deepresearch` output as evidence input, not as final blueprint text. High-impact paper analysis informs explanation and design tradeoffs; it must not replace claim evidence from the user's own work.

## Language and Explanation Policy

Determine `output_language` as follows:

1. If the user explicitly requests an output language, use that language.
2. Otherwise use the dominant language of the latest substantive user message.
3. If the user mixes languages, use the dominant natural language for explanations while preserving technical terms, paper titles, venue names, datasets, benchmarks, metrics, method names, and citation keys in their original language.
4. Keep YAML/JSON field names in English for downstream compatibility. Field values may use `output_language`.

When `deepresearch` returns evidence in another language, synthesize and explain it in `output_language`, but do not mistranslate proper nouns, paper titles, benchmark names, model names, conference names, or quoted terminology.

Always include a visible reasoning summary. Use the heading `Reasoning Summary` translated into `output_language` when appropriate.

The reasoning summary is a concise decision log covering:

- how the user request was interpreted
- assumptions made
- whether `deepresearch` was called and why
- what external evidence materially affected the blueprint
- what high-impact paper patterns were extracted
- why the target venue or contribution framing was selected
- why each main claim was promoted, downgraded, or marked unsupported
- why recommended experiments, baselines, metrics, and figures were chosen
- what uncertainty remains
- what evidence would change the blueprint

Do not output raw chain-of-thought, hidden scratchpad content, private step-by-step internal reasoning, or unverified speculation chains.

## Inputs to Extract

Extract:

- topic
- target venue or candidate venues
- field and subfield
- current stage: idea, prototype, experiments, draft, rebuttal
- contribution type: algorithm, system, dataset, benchmark, measurement, theory, experience, tool, mixed
- available artifacts: code, data, plots, draft, notes, references
- constraints: deadline, page limit, compute budget, anonymity, reproducibility requirements
- requested output language, if any
- requested explanation depth: `brief`, `standard`, or `detailed`

If explanation depth is not specified, use `standard`. If missing information is not blocking, make a labeled assumption. Ask at most one blocking clarification question only when a useful blueprint cannot be produced otherwise.

## Workflow

### 1. Build a Compact Research Brief

Create an internal brief with:

- one-sentence idea
- expected contribution type
- target audience
- likely venue candidates
- known evidence
- unknowns
- highest-risk novelty or evaluation issue
- output language

### 2. Gather Live Evidence

Use `deepresearch` unless all three are true:

1. the user explicitly provided venue expectations
2. the user provided closest related work
3. the user only wants structural reformatting

Use `fast` mode when the user provides target venue, related work, and an experimental setup. Use `thorough` mode when the idea is early stage, venue is unclear, novelty risk is high, target venue is strong, or exemplar-pattern explanation is requested.

Fast mode uses one combined call:

```text
You are supporting a paper-blueprint compiler.

Research brief:
[RESEARCH_BRIEF]

Target venue(s):
[VENUES]

Return a concise, citation-backed report with:
1. Current venue expectations and review criteria relevant to this work.
2. 10-15 closest related works with problem, method, evidence, limitation, and likely delta.
3. Strong baselines and evaluation norms for this subfield.
4. Common reviewer objections for this venue/subfield.
5. Evidence that the proposed novelty claim is weak, already solved, or needs reframing.
6. Key decision factors that should affect the final paper blueprint.

Requirements:
- Prefer official venue pages, proceedings pages, arXiv/ACM/USENIX/IEEE pages, benchmark pages, and primary papers.
- Mark uncertainty explicitly.
- Include citations for factual claims.
- Do not write the blueprint.
- Do not produce hidden chain-of-thought. Provide only evidence-facing decision summaries.
```

Thorough mode uses focused calls:

- `venue_probe`: current CFP, author instructions, review criteria, contribution types, evaluation and reproducibility expectations, artifact expectations, and acceptance patterns.
- `literature_probe`: closest related work, novelty boundary, likely baselines, and verification status.
- `exemplar_probe`: high-impact paper pattern mining.
- `reviewer_probe`: novelty, evaluation, baseline, claim-overreach, assumption, reproducibility, and framing risks.

Keep `literature_probe` and `exemplar_probe` separate when possible: literature probing defines novelty boundaries and baselines; exemplar mining extracts excellence patterns.

## Exemplar Pattern Mining

Use `deepresearch` to analyze high-impact papers from the target venue and related field.

This step must not merely list highly cited papers. It must extract reusable excellence patterns and use them to explain current blueprint decisions.

Collect three groups:

1. `target_venue_exemplars`: high-impact papers from the target venue or closest venues. Purpose: infer venue-specific contribution and evidence patterns.
2. `field_exemplars`: high-impact papers from the same research area, regardless of venue. Purpose: infer field-level patterns of durable influence.
3. `nearest_neighbor_exemplars`: papers most similar to the proposed work. Purpose: identify reviewer comparison points, novelty risks, and baseline expectations.

Use 3-8 papers per group depending on available time and requested explanation depth.

Exemplar selection rules:

- Prefer primary papers, official proceedings, best-paper or test-of-time award pages, widely cited papers with clear technical influence, papers used as baselines or conceptual references, and recent nearest-neighbor papers likely to be cited by reviewers.
- Avoid surveys unless the current work is a survey or benchmark.
- Avoid papers that are highly cited but technically irrelevant.
- Do not use citation count alone as proof of quality.
- Mark uncertain influence claims as `needs_verification`.

For each exemplar, extract:

- title, venue, year, source/citation
- why it is considered influential
- problem framing
- core insight and contribution type
- named abstraction or reusable mechanism
- key tradeoff changed
- evidence strategy
- baselines, datasets, workloads, or metrics
- figure/table/storytelling pattern
- limitation or threat model
- adoption reason
- transferable lesson for the current paper
- non-transferable warning that should not be copied blindly

After individual paper analysis, synthesize:

- `exemplar_patterns`: recurring excellence patterns across exemplars
- `venue_style_lessons`: what the target venue appears to reward
- `field_style_lessons`: what the field appears to reuse or cite
- `nearest_neighbor_expectations`: likely reviewer comparison points
- `current_blueprint_alignment`: how the proposed paper matches these patterns
- `current_blueprint_gaps`: where the proposed paper falls short
- `blueprint_decisions_influenced`: claim, evaluation, figure, section, and risk decisions affected by exemplar analysis

Use this `exemplar_probe` prompt shape:

```text
You are supporting a paper-blueprint compiler.

Task: Analyze high-impact papers from the target venue and related research field, then extract reusable excellence patterns for blueprint design.

Research brief:
[RESEARCH_BRIEF]

Target venue(s):
[VENUES]

Research area:
[FIELD]

Candidate contribution type:
[CONTRIBUTION_TYPE]

Find and analyze three groups of papers:
1. target_venue_exemplars: 5-8 high-impact papers from the target venue or closest venues.
2. field_exemplars: 5-8 high-impact papers from the same research area, regardless of venue.
3. nearest_neighbor_exemplars: 5-8 papers most similar to the proposed work, even if not the most cited.

For each paper, return title, authors if available, venue and year, source URL or citation, citation signal if available, why it is influential, problem framing, core contribution, named abstraction or reusable mechanism, key tradeoff changed, evidence strategy, important baselines/datasets/workloads/metrics, figure/table/storytelling pattern, limitation or threat model, adoption reason, transferable lesson, and non-transferable warning.

Then synthesize recurring excellence patterns, target venue style lessons, field-level influence patterns, nearest-neighbor reviewer expectations, how the proposed paper should adapt claims/evaluation/figures/sections, and risks if it fails to match these patterns.

Requirements:
- Prefer official venue pages, proceedings, ACM/IEEE/USENIX pages, arXiv, Semantic Scholar, OpenAlex, benchmark pages, and primary papers.
- Mark uncertain claims as needs_verification.
- Do not write the final blueprint.
- Do not expose hidden chain-of-thought.
- Return an evidence-facing decision summary.
```

## Compile the Blueprint

Produce:

1. machine-readable YAML summary
2. formal blueprint
3. user-language explanation / reasoning summary

The YAML summary must include `output_language`, `reasoning_summary_mode: decision_log`, `exemplar_analysis`, `distilled_excellence_patterns`, `blueprint_decision_log`, and `reasoning_summary`.

Formal blueprint sections:

1. Executive Summary
2. Target Venue and Contribution Type
3. Acceptance Hypothesis
4. Core Claims
5. Related-Work Positioning
6. Exemplar Pattern Mining
7. Method Blueprint
8. Evaluation Blueprint
9. Figure and Table Storyboard
10. Section-by-Section Outline
11. Reviewer Risk Register
12. Reproducibility and Artifact Plan
13. Missing Evidence
14. Next Actions

Use `assets/blueprint_schema.yaml` as the output field guide.

## Claim-Evidence Mapping

Every main claim must include:

- claim ID
- exact claim statement
- why it matters
- required evidence
- dataset, workload, or environment
- metrics
- baselines or why no baseline applies
- ablations or controls
- expected figure/table
- exemplar patterns that influenced the claim, if any
- failure condition
- confidence level
- likely reviewer attack
- status: `supported`, `unsupported`, `needs_experiment`, or `needs_verification`

If a claim lacks evidence, label it `unsupported` and keep it out of the main contribution summary.

## Related-Work Positioning

Build a related-work matrix. For each work include:

- source
- problem
- method
- evidence
- limitation
- delta
- role: `required_baseline`, `required_citation`, or `contextual`
- verification status: `verified`, `tentative`, or `needs_verification`

Never overstate novelty. If the delta depends on uncertain interpretation, mark it `tentative`.

## Venue Fit and Reviewer Simulation

For each candidate venue, score 1-5 on audience fit, contribution fit, evidence fit, novelty fit, and risk level. Explain the score in concrete evidence terms.

Simulate:

- supportive expert
- skeptical related-work expert
- evaluation-focused reviewer

For each reviewer, list likely strengths, weaknesses, questions, and fixes.

## DeepResearch Consumption Rules

1. Treat citations as evidence, not authority.
2. Separate verified facts from synthesis and speculation.
3. If sources conflict, report the conflict.
4. If `deepresearch` gives a novelty claim without primary-paper support, downgrade it to `tentative`.
5. If a related-work delta is vague, rewrite it into a precise comparison or mark `needs_verification`.
6. Never use citation count alone as evidence of quality.
7. Never claim SOTA unless benchmark, dataset, metric, and timestamp are clear.

## Exemplar Analysis Consumption Rules

1. Use exemplar patterns as design guidance, not as proof that the current paper's claims are true.
2. Keep target-venue exemplars, field exemplars, and nearest-neighbor exemplars separate.
3. Balance older high-citation papers with recent nearest-neighbor papers.
4. Treat citation count as a signal, not as evidence of technical quality.
5. Exclude surveys unless the user is writing a survey or benchmark paper.
6. Extract patterns more specific than `clear writing` or `strong experiments`.
7. Include at least one non-transferable warning when borrowing a pattern.
8. Each blueprint decision influenced by exemplars must point to a concrete pattern, not vague prestige.

## Quality Gate

Before final output, check:

- acceptance hypothesis is specific and falsifiable
- each claim maps to evidence
- baselines are fair and strong, or absence is justified
- novelty boundary is grounded in related work
- venue expectations are current or marked `needs_verification`
- limitations are explicit
- each figure/table supports at least one claim
- exemplar analysis is relevant, sourced, and used only as decision guidance
- each exemplar-derived decision names a concrete transferable pattern
- next actions are concrete

If a gate fails, include it under `Missing Evidence` or `Reviewer Risk Register`.

When writing files, optionally run:

```bash
python scripts/validate_blueprint.py <blueprint-summary.json>
```

## Final Output Format

Always output two layers.

### Layer 1: Blueprint

Include:

1. YAML Summary
2. Executive Summary
3. Target Venue and Contribution Type
4. Acceptance Hypothesis
5. Core Claims
6. Related-Work Positioning
7. Exemplar Pattern Mining
8. Method Blueprint
9. Evaluation Blueprint
10. Figure and Table Storyboard
11. Section-by-Section Outline
12. Reviewer Risk Register
13. Reproducibility and Artifact Plan
14. Missing Evidence
15. Next Actions

### Layer 2: Explanation

Use `output_language`. Include:

1. Task Understanding
2. External Evidence Used
3. High-Impact Paper Pattern Analysis
4. How the Blueprint Uses These Patterns
5. Reasoning Summary
6. Key Decisions
7. Main Risks and Uncertainty
8. Evidence That Would Change the Blueprint

This layer is a decision log, not a transcript of internal reasoning.

## Output Style

Be precise and non-promotional. Use compact tables. Mark assumptions and uncertainty explicitly, but keep caveats short.

Use the user's language for explanations. Preserve technical names and citation labels. Do not write long literature-review prose. Do not write the full paper. Produce an actionable blueprint plus a user-readable decision log.
