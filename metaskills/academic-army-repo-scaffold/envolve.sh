#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-repo-scaffold \
  --artifact-path output/evolve-academic-army-repo-scaffold \
  --metaskill-path metaskills/academic-army-repo-scaffold/METASKILL.md \
  --task-path metaskills/academic-army-repo-scaffold/ENVOLVETASK.md
