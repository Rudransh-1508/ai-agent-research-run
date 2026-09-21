#!/bin/bash
# Fetch S2 metadata for all anchors
cd "$(dirname "$0")"
IDS=(
  "DOI:10.1109/ICMAS.2000.858440|dellarocas_klein_2000"
  "ARXIV:2408.00989|huang_2408"
  "ARXIV:2602.19843|masfire_2602"
  "ARXIV:2505.00212|whowhen_2505"
  "ARXIV:2503.13657|mast_2503"
  "ARXIV:2603.04474|sparkfire_2603"
  "ARXIV:2608.06790|agentchaos_2608"
  "DOI:10.1109/ICERA72709.2026.11666599|ctc_icera2026"
  "ARXIV:2609.14767|loopback_2609"
  "ARXIV:2607.25446|imacs_2607"
  "ARXIV:2602.14849|atomix_2602"
  "ARXIV:2606.08919|oversight_2606"
  "ARXIV:2606.07937|hallucascade_2606"
  "DOI:10.1145/2168260.2168261|kota_taas2012"
)
for entry in "${IDS[@]}"; do
  id="${entry%%|*}"; name="${entry##*|}"
  out="meta_${name}.json"
  if [ -s "$out" ]; then echo "skip $name"; continue; fi
  curl -s "https://api.semanticscholar.org/graph/v1/paper/${id}?fields=title,year,authors.name,authors.authorId,citationCount,referenceCount,externalIds,venue,publicationDate,abstract" -o "$out"
  echo "fetched $name: $(head -c 120 "$out")"
  sleep 2
done
