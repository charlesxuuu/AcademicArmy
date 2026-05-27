#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --skill-path skills/academic-army-coding-plan \
  --artifact-path output/evolve-academic-army-coding-plan \
  --metaskill-path metaskills/academic-army-coding-plan/METASKILL.md \
  --runner-task-path metaskills/academic-army-coding-plan/ENVOLVETASK.md
