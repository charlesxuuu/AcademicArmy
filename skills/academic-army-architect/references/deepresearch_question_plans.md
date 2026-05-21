# DeepResearch Question Plans

DeepResearch is used as a focused research judgment layer. The workflow decomposes the blueprint task, asks the relevant DeepResearch question, then integrates the answer into the fixed blueprint and analysis templates.

## Hard Blueprint Steps

The following blueprint sections typically use evidence from papers, venue documents, artifacts, or benchmarks:

1. `Target Venue / Journal`
2. `Research Problem`
3. `Central Claim`
4. `Proposed Contribution`
5. `Method / Approach`
6. `Data, Materials, or Artifacts`
7. `Evaluation / Validation Plan`
8. `Related Work Positioning`
9. `Paper Structure` when target venue or paper type strongly affects narrative
10. substantive revisions to any of the above

The orchestration layer handles `Basic Information`, light `Research Idea Summary`, formatting, version labels, and purely mechanical edits.

## Question Types

### `venue_style_analysis`

Use when the user names or changes a target venue or journal, or asks for venue-style framing.

Ask DeepResearch:

- What does this venue or journal appear to value in recent accepted papers or official guidance?
- What contribution types, methods, evaluation styles, and paper narratives are common?
- What constraints, review criteria, author guidance, or checklist requirements matter?
- Which blueprint sections adapt to this venue?
- Which points remain `TBD` based on available venue evidence?

Integration targets:

- `4. Target Venue / Journal`
- `6. Motivation`
- `7. Central Claim`
- `9. Proposed Contribution`
- `12. Evaluation / Validation Plan`
- `14. Paper Structure`

### `related_direction_synthesis`

Use when the user's idea is broad, the research area is unclear, or field context is needed.

Ask DeepResearch:

- What clusters of related work surround this idea?
- What problem formulations, assumptions, methods, and evaluation setups recur?
- What open gaps are visible without inventing a new user contribution?
- Which terms should be used when framing the problem?
- Which clusters are out of scope?

Integration targets:

- `5. Research Problem`
- `6. Motivation`
- `10. Method / Approach`
- `13. Related Work Positioning`

### `closest_work_comparison`

Use when novelty, overlap, or related work positioning matters.

Ask DeepResearch:

- Which papers are closest to the user's idea?
- How exactly do they overlap with the user's idea?
- How might the user's idea differ if the user-provided facts are taken literally?
- What novelty or overclaiming issues appear?
- What positioning statement fits the evidence?

Integration targets:

- `7. Central Claim`
- `9. Proposed Contribution`
- `13. Related Work Positioning`
- `15. Missing Information and Next Actions`

### `contribution_boundary`

Use when contribution claims need evidence-based boundaries.

Ask DeepResearch:

- Which contribution claims are supported by user input?
- Which claims are suggested by the literature and need user confirmation?
- Which claims are broader than the evidence supports?
- What contribution wording fits the current evidence?
- What stronger wording would require additional evidence?

Integration targets:

- `7. Central Claim`
- `9. Proposed Contribution`
- `15. Missing Information and Next Actions`

### `claim_strength`

Use when the main claim needs a strength level.

Ask DeepResearch:

- What claim does the current evidence support?
- What exceeds the available evidence?
- What lower-commitment and stronger versions are useful?
- What evidence would be needed to upgrade the claim?
- Which assumptions belong in the blueprint?

Integration targets:

- `7. Central Claim`
- `12. Evaluation / Validation Plan`
- `15. Missing Information and Next Actions`

### `method_evaluation_design`

Use when method, baselines, metrics, ablations, robustness checks, case studies, or user studies matter.

Ask DeepResearch:

- What evaluation designs are common in this area?
- Which baselines or comparisons fit the field?
- Which metrics fit the task?
- Which ablations, sensitivity checks, or robustness tests matter?
- What qualitative or case-study evidence may be needed?
- What evidence is central versus optional?

Integration targets:

- `10. Method / Approach`
- `12. Evaluation / Validation Plan`
- `15. Missing Information and Next Actions`

### `artifact_landscape`

Use when datasets, code, benchmarks, tools, protocols, or reproducibility artifacts matter.

Ask DeepResearch:

- What relevant datasets, codebases, benchmarks, or tools exist?
- Which are close to the user's idea, and which are background?
- What availability, license, maintenance, or compatibility caveats are visible?
- Which artifacts can be referenced in the blueprint?
- Which artifacts need user verification before use?

Integration targets:

- `11. Data, Materials, or Artifacts`
- `12. Evaluation / Validation Plan`
- `13. Related Work Positioning`

### `paper_structure_strategy`

Use when the target venue, paper type, or contribution form affects narrative order.

Ask DeepResearch:

- What section emphasis is appropriate for this paper type and venue?
- Does the paper lead with problem, system, theory, dataset, empirical finding, or user need?
- Where do limitations, ethics, reproducibility, or artifact availability belong?
- What story arc fits the current research content?

Integration targets:

- `14. Paper Structure`
- `6. Motivation`
- `9. Proposed Contribution`

### `revision_impact_analysis`

Use for substantive edits to an existing blueprint.

Ask DeepResearch:

- Which sections change because of the revision?
- Which sections stay unchanged?
- Which old sources remain useful?
- Which sources are added, removed, or deprioritized?
- How are the change log and source ledger updated?

Integration targets:

- changed blueprint sections;
- `paper_blueprint_analysis.md` change log;
- `source_ledger.json`.

## Integration Rule

Use several focused DeepResearch calls for hard sections, then render the final files through the templates.
