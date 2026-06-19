---
name: academic-army-literate-latex-writing
description: Write and revise academic LaTeX through `.lit.md` literate Markdown. Use when drafting paper prose, updating sentence explanations, tangling with `python -m tanglemd2tex`, or preparing writing MCP review.
---

# Academic Army Literate LaTeX Writing

Write in `.lit.md`. Generate clean `.tex` with `python -m tanglemd2tex`.

## Source
Use `.lit.md` as the only editable manuscript source. Treat `.tex` as generated output.

`sections/foo.lit.md` generates `sections/foo.tex`.

## Blocks
Put manuscript text inside fenced blocks whose info string is exactly `latex`. Markdown outside those blocks explains the writing and does not enter `.tex`.

For normal prose, use one `latex` block per manuscript sentence.

````markdown
```latex
<manuscript sentence>
```

<explanation>
````

After each block, explain why the sentence is here, how it connects to nearby context, what it prepares next, and any useful cross-section connection by content.

## Workflow
Draft, revise, move, and delete text in `.lit.md`.

Keep each manuscript block and its explanation together.

Install when needed, then run the smallest command that covers the edited files:

```bash
pip install tangle-md2tex
python -m tanglemd2tex sections/foo.lit.md
python -m tanglemd2tex sections/
python -m tanglemd2tex
```

Compile afterward when the project has a compile command.

## MCP Review
Call the writing MCP when the user asks for stronger review, rewriting, polishing, or logic review.

Send `.lit.md` fragments, not generated `.tex`. Send a self-contained packet: user request, paper goal, section goal, local passage goal, preceding context, target `.lit.md` fragment, following context, relevant cross-section context, constraints, and desired output.

Ask for revised `.lit.md` blocks or concrete replacement suggestions.

Apply accepted feedback to `.lit.md`, update explanations, then run `python -m tanglemd2tex`.

## Report
Say what source changed and what was regenerated:

```text
Updated sections/foo.lit.md and regenerated sections/foo.tex with python -m tanglemd2tex.
Applied MCP feedback to the .lit.md source, updated explanations, and regenerated the .tex.
```
