#!/usr/bin/env bash
set -euo pipefail

npm run developing -- \
  --config "agent-forge.yaml" \
  --config "secret.yaml" \
  --target-path "workspace/codebase" \
  --achive-dir "workspace/developing-archives" \
  --project-progress-memory-path "workspace/developing-memory/project-progress-memory" \
  --code-design-memory-path "workspace/developing-memory/code-design-memory" \
  --goal-path "workspace/goal.md" \
  --max-iterations "100" \
  --max-task-devloop-iterations "10" \
  --max-memory-rounds "3"
