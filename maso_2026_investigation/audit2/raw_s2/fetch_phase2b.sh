#!/bin/bash
cd "$(dirname "$0")"
F="title,year,authors,externalIds,venue,publicationDate,citationCount"
get() {
  if [ -s "$2" ] && ! grep -q 'Too Many Requests' "$2"; then echo "skip $2"; return; fi
  bash s2get.sh "$1" "$2"; sleep 6
}
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2602.14849?fields=${F},referenceCount" meta_atomix_2602.json
get "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2603.04474?fields=${F},referenceCount" meta_sparkfire_2603.json
bash fetch_phase2.sh
