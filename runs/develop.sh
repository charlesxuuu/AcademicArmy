#!/usr/bin/env bash
set -euo pipefail

npm run developing -- \
  --config "agent-forge.yaml" \
  --config "secret.yaml" \
  --target-path "workspace/codebase" \
  --archive-root "workspace/archives" \
  --project-progress-memory-path "workspace/memory/project-progress" \
  --code-design-memory-path "workspace/memory/code-design" \
  --goal-path "workspace/plan/paper_blueprint.md" \
  --goal-path "workspace/plan/experiment_plan.md" \
  --goal-path "workspace/plan/coding_plan.md" \
  --goal-path "workspace/plan/goal.md" \
  --max-iterations "100" \
  --max-task-devloop-iterations "10" \
  --max-memory-rounds "3" \
  --memory-clean-interval "0"
