#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-experiment-plan \
  --artifact-path output/evolve-academic-army-experiment-plan \
  --metaskill-path metaskills/academic-army-experiment-plan/METASKILL.md \
  --task-path metaskills/academic-army-experiment-plan/ENVOLVETASK.md
