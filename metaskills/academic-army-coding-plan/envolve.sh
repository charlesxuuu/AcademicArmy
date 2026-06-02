#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-coding-plan \
  --artifact-path output/evolve-academic-army-coding-plan \
  --metaskill-path metaskills/academic-army-coding-plan/METASKILL.md \
  --task-path metaskills/academic-army-coding-plan/ENVOLVETASK.md
