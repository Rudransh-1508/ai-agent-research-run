#!/bin/bash
# Frozen-threshold validation (held-out + repeats) for each Groq judge.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
for spec in "$@"; do
  set -- $spec; tag=$1; name=$2
  python3 analysis/judge_validation.py --name "$name" --calib artifact/judge_groq_$tag.jsonl \
    --repeats artifact/judge_groq_${tag}_r2.jsonl artifact/judge_groq_${tag}_r3.jsonl \
    --heldout artifact/judge_groq_${tag}_heldout.jsonl --out-prefix artifact/validation_groq_$tag
  python3 -c "
import json; v=json.load(open('artifact/validation_groq_$tag.json'))
print('leaked held-out:', v.get('heldout',{}).get('leaked_items'), ' at vendor 0.9:', v['heldout_vendor_0.9']['leaked_items'])
print('flips:', v.get('stability',{}).get('flip_items')); print()"
done
