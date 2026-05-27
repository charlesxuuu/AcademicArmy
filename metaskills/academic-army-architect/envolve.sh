#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --skill-path skills/academic-army-architect \
  --artifact-path output/evolve-academic-army-architect \
  --metaskill-path metaskills/academic-army-architect/METASKILL.md \
  --runner-task-path metaskills/academic-army-architect/ENVOLVETASK.md
