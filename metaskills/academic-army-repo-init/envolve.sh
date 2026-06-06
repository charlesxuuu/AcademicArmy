#!/usr/bin/env bash
set -euo pipefail

npm run evolve-skill -- \
  --config agent-forge.yaml \
  --skill-path skills/academic-army-repo-init \
  --artifact-path output/evolve-academic-army-repo-init \
  --metaskill-path metaskills/academic-army-repo-init/METASKILL.md \
  --task-path metaskills/academic-army-repo-init/ENVOLVETASK.md
