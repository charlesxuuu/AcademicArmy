# AcademicArmy Structure

`AcademicArmy` is organized as a set of paper-production roles. Each folder represents one agent or team that participates in turning a paper blueprint into a complete research paper.

Top-level roles:

- `ProductManager` receives an initial research idea and helps refine it into a standardized paper blueprint before the formal workflow begins.
- `Author` writes and revises the manuscript text based on the blueprint, experimental evidence, figures, and review feedback.
- `Coding` is the Coding Team. It turns the paper blueprint into code blueprints, implementation modules, tests, reviews, and performance optimization.
- `Illustrator` creates explanatory diagrams for methods, workflows, systems, and concepts.
- `Plotter` creates experiment result figures from metrics, logs, and statistical outputs.
- `Reviewer` evaluates the manuscript and gives Author actionable revision feedback.

Coding Team positions:

- `Coding/Architect` creates or revises the code blueprint.
- `Coding/Developer` implements functional modules and test scripts.
- `Coding/CodeReviewer` reviews Developer's code and gives feedback on quality, maintainability, and readability.
- `Coding/PerformanceEngineer` runs tests and optimizes code for assigned metrics. Each test item is handled by a dedicated Performance Engineer.
