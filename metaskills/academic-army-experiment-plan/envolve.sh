#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --skill-path skills/academic-army-experiment-plan \
  --artifact-path output/evolve-academic-army-experiment-plan \
  --metaskill-path metaskills/academic-army-experiment-plan/METASKILL.md \
  --runner-task-path metaskills/academic-army-experiment-plan/ENVOLVETASK.md
