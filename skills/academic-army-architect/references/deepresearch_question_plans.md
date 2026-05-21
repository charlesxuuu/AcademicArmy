# DeepResearch Question Plans

DeepResearch should be called as a focused research judgment layer, not as one large all-purpose step. Codex decomposes the blueprint task, asks the right DeepResearch question, then integrates the answer into the fixed blueprint and analysis templates.

## Hard Blueprint Steps

The following blueprint sections usually require reading papers, venue documents, artifacts, or benchmarks before Codex can write responsibly:

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

Codex may handle `Basic Information`, light `Research Idea Summary`, formatting, version labels, and purely mechanical edits without DeepResearch.

## Question Types

### `venue_style_analysis`

Use when the user names or changes a target venue or journal, or asks for venue-style framing.

Ask DeepResearch:

- What does this venue or journal appear to value in recent accepted papers or official guidance?
- What contribution types, methods, evaluation styles, and paper narratives are common?
- What constraints, review criteria, author guidance, or checklist requirements matter?
- Which blueprint sections must adapt to this venue?
- What should remain `TBD` because venue evidence is insufficient?

Codex integrates into:

- `4. Target Venue / Journal`
- `6. Motivation`
- `7. Central Claim`
- `9. Proposed Contribution`
- `12. Evaluation / Validation Plan`
- `14. Paper Structure`

### `related_direction_synthesis`

Use when the user's idea is broad, the research area is unclear, or Codex needs field context.

Ask DeepResearch:

- What clusters of related work surround this idea?
- What problem formulations, assumptions, methods, and evaluation setups recur?
- What open gaps are visible without inventing a new user contribution?
- Which terms should Codex use when framing the problem?
- Which clusters should be avoided or treated as out of scope?

Codex integrates into:

- `5. Research Problem`
- `6. Motivation`
- `10. Method / Approach`
- `13. Related Work Positioning`

### `closest_work_comparison`

Use when novelty risk, overlap, or related work positioning matters.

Ask DeepResearch:

- Which papers are closest to the user's idea?
- How exactly do they overlap with the user's idea?
- How might the user's idea differ if the user-provided facts are taken literally?
- What novelty risks or overclaiming risks follow?
- What positioning statement is defensible?

Codex integrates into:

- `7. Central Claim`
- `9. Proposed Contribution`
- `13. Related Work Positioning`
- `15. Missing Information and Next Actions`

### `contribution_boundary`

Use when Codex needs to decide whether contributions are justified, too broad, or need user confirmation.

Ask DeepResearch:

- Which contribution claims are supported by user input?
- Which claims are only suggested by the literature and need user confirmation?
- Which claims would be overbroad or risky?
- What conservative contribution wording is defensible?
- What stronger wording could be used only if evidence is later provided?

Codex integrates into:

- `7. Central Claim`
- `9. Proposed Contribution`
- `15. Missing Information and Next Actions`

### `claim_strength`

Use when the main claim could be conservative, moderate, or strong.

Ask DeepResearch:

- What claim does the current evidence support?
- What would be too strong given available evidence?
- What conservative and strong versions should be distinguished?
- What evidence would be needed to upgrade the claim?
- Which assumptions must be visible in the blueprint?

Codex integrates into:

- `7. Central Claim`
- `12. Evaluation / Validation Plan`
- `15. Missing Information and Next Actions`

### `method_evaluation_design`

Use when method, baselines, metrics, ablations, robustness checks, case studies, or user studies matter.

Ask DeepResearch:

- What evaluation designs are common or defensible in this area?
- Which baselines or comparisons are expected?
- Which metrics should be considered?
- Which ablations, sensitivity checks, or robustness tests matter?
- What qualitative or case-study evidence may be needed?
- What evidence is submission-blocking versus nice-to-have?

Codex integrates into:

- `10. Method / Approach`
- `12. Evaluation / Validation Plan`
- `15. Missing Information and Next Actions`

### `artifact_landscape`

Use when datasets, code, benchmarks, tools, protocols, or reproducibility artifacts matter.

Ask DeepResearch:

- What relevant datasets, codebases, benchmarks, or tools exist?
- Which are close to the user's idea, and which are only background?
- What availability, license, maintenance, or compatibility caveats are visible?
- Which artifacts can be referenced in the blueprint?
- Which artifacts require user verification before use?

Codex integrates into:

- `11. Data, Materials, or Artifacts`
- `12. Evaluation / Validation Plan`
- `13. Related Work Positioning`

### `paper_structure_strategy`

Use when the target venue, paper type, or contribution form affects narrative order.

Ask DeepResearch:

- What section emphasis is appropriate for this paper type and venue?
- Should the paper lead with problem, system, theory, dataset, empirical finding, or user need?
- Where should limitations, ethics, reproducibility, or artifact availability be foregrounded?
- What story arc is defensible without adding new research content?

Codex integrates into:

- `14. Paper Structure`
- `6. Motivation`
- `9. Proposed Contribution`

### `revision_impact_analysis`

Use for substantive edits to an existing blueprint.

Ask DeepResearch:

- Which sections must change because of the revision?
- Which sections should remain untouched?
- Which old sources remain useful?
- Which sources should be added, removed, or deprioritized?
- How should the change log and source ledger be updated?

Codex integrates into:

- the changed blueprint sections only;
- `paper_blueprint_analysis.md` change log;
- `source_ledger.json`.

## Integration Rule

Codex should not ask DeepResearch to write the whole blueprint unless the user explicitly requests an all-in-one research run. Prefer several focused DeepResearch calls for hard sections, then have Codex render the final files.
