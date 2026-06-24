#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-architect \
  --artifact-path workspace/evolve-academic-army-architect \
  --metaskill-path metaskills/academic-army-architect/METASKILL.md \
  --task-path metaskills/academic-army-architect/ENVOLVETASK.md
