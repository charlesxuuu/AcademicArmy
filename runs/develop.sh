#!/usr/bin/env bash
set -euo pipefail

npm run developing -- \
  --config "agent-forge.yaml" \
  --config "secret.yaml" \
  --target-path "output/codebase" \
  --achive-dir "output/developing-archives" \
  --project-progress-memory-path "output/developing/project-progress-memory" \
  --code-design-memory-path "output/developing/code-design-memory" \
  --coding-style-skill-path "skills/academic-army-coding-style" \
  --goal-path "output/goal.md" \
  --max-iterations "100" \
  --max-task-devloop-iterations "10" \
  --max-memory-rounds "3"
