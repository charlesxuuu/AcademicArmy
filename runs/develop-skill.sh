#!/usr/bin/env bash
set -euo pipefail

npm run developing-skill -- \
  --config "agent-forge.yaml" \
  --config "secret.yaml" \
  --target-path "output/codebase" \
  --achive-dir "output/developing-archives" \
  --project-progress-memory-path "output/developing/project-progress-memory" \
  --code-design-memory-path "output/developing/code-design-memory" \
  --coding-style-skill-path "skills/academic-army-coding-style" \
  --metaskill-path "metaskills/academic-army-coding-style/METASKILL.md" \
  --goal-path "output/goal.md" \
  --max-iterations "100" \
  --max-task-devloop-iterations "10" \
  --max-memory-rounds "3"
