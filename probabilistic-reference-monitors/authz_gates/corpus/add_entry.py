#!/usr/bin/env python3
"""Merge one manual-extraction entry (JSON on stdin, keyed by gate name) into manual_extraction.json."""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(HERE, "manual_extraction.json")
with open(path) as f:
    m = json.load(f)
update = json.load(sys.stdin)
m.update(update)
with open(path, "w") as f:
    json.dump(m, f, indent=2)
print("added:", ", ".join(update))
