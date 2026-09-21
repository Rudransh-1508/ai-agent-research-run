#!/bin/bash
cd "$(dirname "$0")"
IDS=(
  "ARXIV:2408.00989|huang_2408"
  "ARXIV:2602.19843|masfire_2602"
  "ARXIV:2505.00212|whowhen_2505"
  "ARXIV:2503.13657|mast_2503"
  "ARXIV:2603.04474|sparkfire_2603"
  "ARXIV:2608.06790|agentchaos_2608"
  "ARXIV:2609.14767|loopback_2609"
  "ARXIV:2607.25446|imacs_2607"
  "ARXIV:2602.14849|atomix_2602"
  "ARXIV:2606.08919|oversight_2606"
  "ARXIV:2606.07937|hallucascade_2606"
)
for entry in "${IDS[@]}"; do
  id="${entry%%|*}"; name="${entry##*|}"
  out="meta_${name}.json"
  # refetch if missing or contains rate-limit message
  if [ -s "$out" ] && ! grep -q 'Too Many Requests' "$out"; then echo "skip $name"; continue; fi
  bash s2get.sh "https://api.semanticscholar.org/graph/v1/paper/${id}?fields=title,year,authors.name,authors.authorId,citationCount,referenceCount,externalIds,venue,publicationDate" "$out"
  sleep 8
done
