---
name: academic-army-architect
description: Use when Codex needs to transform a user's existing academic paper idea, research notes, experiment plan, or rough proposal into a fixed-format paper blueprint. This skill standardizes and clarifies the user's own idea into a Markdown blueprint or structured JSON; it must not invent research directions, fabricate contributions, add unsupported experiments, or hallucinate literature. Use for academic writing intake, paper blueprint creation, claim-evidence planning, missing-information tracking, and repeatable paper architecture outputs.
---

# Academic Army Architect

## Contract

Turn the user's existing research idea into a standardized paper blueprint. Preserve the user's substance, make the structure precise, and mark missing information as `TBD`.

Do not improve the idea by adding new research substance. Do not invent contributions, results, baselines, datasets, citations, target venues, or experiments. Do not default to web search. Search only when the user explicitly asks for venue requirements, literature checks, or external verification, and cite sources for any externally supported claims.

## Workflow

1. Parse the intake.
   Extract only what the user provided: field, subfield, paper type, venue, readers, stage, idea, problem, motivation, claim, contributions, method, evidence, validation plan, constraints, and existing materials.

2. Decide whether there is enough to draft.
   If the user gives at least a recognizable research idea, produce the blueprint immediately and place unknowns in `TBD`. If the input is too thin to identify a research idea, ask at most three questions:
   - What field or problem area is this paper in?
   - What core problem should the paper address?
   - What method, evidence, or material do you already have?

3. Fill the fixed template.
   Use `assets/blueprint_template.md` as the required section order. Do not add, remove, or rename the 12 top-level sections unless the user explicitly asks for a custom format.

4. Run the consistency check.
   Confirm that:
   - the central claim addresses the research problem;
   - each contribution is grounded in the user's input;
   - the expected evidence can plausibly support the claim.

   If evidence is missing or too weak, write `Current evidence is insufficient / TBD` rather than inventing a stronger plan.

5. Deliver the result.
   Default to Markdown. If the user asks for a saved file, create a `.md` blueprint file in the requested project location. If the product or API layer needs structured data, use `references/blueprint_schema.json` and optionally validate JSON with `scripts/validate_blueprint_json.py`.

## Output Rules

- Always use the same 12-section blueprint structure for normal output.
- Keep language academically clear but conservative.
- Use 1-3 contribution bullets unless the user already provided more.
- Phrase `Next Writing Actions` as writing or clarification tasks, not new research directions.
- Put every unknown, unsupported, or user-unconfirmed value in `TBD`.
- Include a `Missing Information` list even when it is empty.

## Required Blueprint Sections

1. Basic Information
2. One-Sentence Paper Idea
3. Research Problem
4. Motivation and Importance
5. Central Claim
6. Proposed Contribution
7. Method / Approach
8. Expected Evidence
9. Evaluation or Validation Plan
10. Paper Structure
11. Missing Information
12. Next Writing Actions

## Resource Guide

- Read `assets/blueprint_template.md` when drafting a Markdown blueprint.
- Read `references/blueprint_schema.json` when structured JSON output or API integration is needed.
- Run `scripts/validate_blueprint_json.py <blueprint.json>` when a JSON blueprint file needs a quick structural check.
