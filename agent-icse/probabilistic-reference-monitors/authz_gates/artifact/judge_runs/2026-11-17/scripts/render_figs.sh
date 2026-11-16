#!/bin/bash
# Regenerate the judge figures into the scratch preview dir and rasterize page 1.
set -e
S=/private/tmp/claude-501/-Users-rudranshrathore-research-gap-agentic/8b8960b8-47eb-48cd-82be-205cd59771ed/scratchpad
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
python3 analysis/judge_figures.py --outdir "${OUTDIR:-$S/fig}" "$@" > /dev/null
cd "${OUTDIR:-$S/fig}"
cp "$S/fig/preview.tex" . 2>/dev/null || true
tectonic preview.tex 2>&1 | grep -iE "^error|overfull" || true
pdftoppm -r 220 -png -f 1 -l 1 preview.pdf page
ls page*.png
