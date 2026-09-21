#!/bin/bash
cd "$(dirname "$0")"
F="title,year,authors,externalIds,venue,publicationDate,citationCount"

get() { # url out
  if [ -s "$2" ] && ! grep -q 'Too Many Requests' "$2"; then echo "skip $2"; return; fi
  bash s2get.sh "$1" "$2"
  sleep 6
}

# --- remaining metadata ---
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2603.04474?fields=${F},referenceCount,abstract" meta_sparkfire_2603.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2608.06790?fields=${F},referenceCount,abstract" meta_agentchaos_2608.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2609.14767?fields=${F},referenceCount,abstract" meta_loopback_2609.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2607.25446?fields=${F},referenceCount,abstract" meta_imacs_2607.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2602.14849?fields=${F},referenceCount,abstract" meta_atomix_2602.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2606.08919?fields=${F},referenceCount,abstract" meta_oversight_2606.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2606.07937?fields=${F},referenceCount,abstract" meta_hallucascade_2606.json

# --- forward citations ---
get "https://api.semanticscholar.org/graph/v1/paper/c474f9b87013301b66cc921a2f7a3918d506d684/citations?fields=${F}&limit=100&offset=0" cit_huang_p0.json
get "https://api.semanticscholar.org/graph/v1/paper/c474f9b87013301b66cc921a2f7a3918d506d684/citations?fields=${F}&limit=100&offset=100" cit_huang_p1.json
get "https://api.semanticscholar.org/graph/v1/paper/89f83f692a145366aa520254f9ab1ae964a6de13/citations?fields=${F}&limit=100" cit_masfire.json
get "https://api.semanticscholar.org/graph/v1/paper/a0d37ec77dc2acddb223d9a7ac4f23ca10e2908f/citations?fields=${F}&limit=100&offset=0" cit_whowhen_p0.json
get "https://api.semanticscholar.org/graph/v1/paper/a0d37ec77dc2acddb223d9a7ac4f23ca10e2908f/citations?fields=${F}&limit=100&offset=100" cit_whowhen_p1.json
# MAST 610 citers: 7 pages
for off in 0 100 200 300 400 500 600; do
  get "https://api.semanticscholar.org/graph/v1/paper/c83b6a023a5c5ec71b44920a41b41fc007266c44/citations?fields=${F}&limit=100&offset=${off}" cit_mast_p${off}.json
done
echo DONE-BATCH-1
