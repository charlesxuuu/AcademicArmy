#!/usr/bin/env bash
set -euo pipefail

npm run developing-loop -- \
  --codebase-path "output/codebase" \
  --coding-plan-path "output/coding_plan.md" \
  --code-overview-path "output/code_overview.md" \
  --response-path "output/developing-response.md" \
  --response-archive-path "output/developing-response-archive" \
  --max-rounds "10"
