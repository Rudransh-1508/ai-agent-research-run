#!/bin/bash
cd "$(dirname "$0")"
F="title,year,authors,externalIds,venue,publicationDate,citationCount"

get() {
  if [ -s "$2" ] && ! grep -q 'Too Many Requests' "$2"; then echo "skip $2"; return; fi
  bash s2get.sh "$1" "$2"
  sleep 6
}

# DamageFlow search
get "https://api.semanticscholar.org/graph/v1/paper/search?query=DamageFlow&fields=${F},abstract&limit=10" search_damageflow.json

# Backward references of LLM-era anchors (find missed papers)
get "https://api.semanticscholar.org/graph/v1/paper/89f83f692a145366aa520254f9ab1ae964a6de13/references?fields=${F}&limit=100" ref_masfire.json
get "https://api.semanticscholar.org/graph/v1/paper/c474f9b87013301b66cc921a2f7a3918d506d684/references?fields=${F}&limit=100" ref_huang.json
get "https://api.semanticscholar.org/graph/v1/paper/a0d37ec77dc2acddb223d9a7ac4f23ca10e2908f/references?fields=${F}&limit=100" ref_whowhen.json

# Forward citations of 2026 anchors (scoop detection) - IDs resolved from meta files at runtime
for name in sparkfire_2603 agentchaos_2608 loopback_2609 imacs_2607 atomix_2602 oversight_2606 hallucascade_2606; do
  pid=$(python3 -c "import json;print(json.load(open('meta_${name}.json'))['paperId'])" 2>/dev/null)
  if [ -n "$pid" ]; then
    get "https://api.semanticscholar.org/graph/v1/paper/${pid}/citations?fields=${F}&limit=100" cit_${name}.json
    get "https://api.semanticscholar.org/graph/v1/paper/${pid}/references?fields=${F}&limit=100" ref_${name}.json
  else
    echo "no paperId for $name yet"
  fi
done
echo DONE-PHASE-2
