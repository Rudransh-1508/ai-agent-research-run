#!/usr/bin/env python3
"""Adapt corpus/gates.json + corpus/manual_extraction.json to the schema
analysis/fail_open.py expects. Stdlib only; regenerable artifact.

Usage: python3 analysis/corpus_adapter.py > artifact/gates_adapted.json
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "corpus")

MODE_MAP = {"open": "fail-open", "closed": "fail-closed", "partial": "partial",
            "undetermined": "unclassifiable"}

PROVENANCE_PREFIXES = ("undocumented", "copied-from-vendor-docs", "swept-on-data",
                       "documented-derivation")


def normalize_provenance(raw):
    low = str(raw or "undocumented").strip().lower()
    for p in PROVENANCE_PREFIXES:
        if low.startswith(p):
            return p
    return "undocumented"


def main():
    gates = {g["name"]: g for g in json.load(open(os.path.join(CORPUS, "gates.json")))["gates"]}
    manual = json.load(open(os.path.join(CORPUS, "manual_extraction.json")))
    manual.pop("_schema", None)

    out = []
    for name, m in sorted(manual.items()):
        g = gates.get(name)
        if not g or g.get("inclusion") != "included":
            continue
        ep = m.get("error_path", {})
        error_paths = {mode: MODE_MAP.get(ep.get(mode, "undetermined"), "unclassifiable")
                       for mode in ("timeout", "http_429", "http_5xx", "malformed_response")}
        prov_raw = str(m.get("threshold_provenance", "undocumented"))
        prov = normalize_provenance(prov_raw)
        thresholds = [] if prov_raw.strip().lower().startswith("no-threshold") else [
            {"value": t.get("value"), "provenance": prov,
             "evidence": f"{t.get('ref', '')}: {t.get('quote', '')}"}
            for t in m.get("thresholds", [])
        ]
        unsan = (m.get("attacker_text_unsanitised") or {}).get("value", "undetermined")
        cross = str(m.get("cross_evaluation", "none")).strip().lower()
        out.append({
            "repo": name,
            "url": g.get("url"),
            "sha": g.get("sha"),
            "in_pilot_set": m.get("pilot") in (True, "true", "True", "yes"),
            "primitives": m.get("primitives", []),
            "questions": m.get("questions_asked", ""),
            "action_set": m.get("action_set", []),
            "attacker_reachable_unsanitised": {"yes": True, "no": False}.get(unsan, unsan),
            "thresholds": thresholds,
            "error_paths": error_paths,
            "fail_classification": m.get("fail_classification"),
            "cites_cross_evaluation": not cross.startswith("none"),
            "evidence": ep.get("evidence", []),
        })
    print(json.dumps({"gates": out}, indent=1))


if __name__ == "__main__":
    main()
