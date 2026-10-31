#!/usr/bin/env python3
"""Automated first-pass feature extraction over the cloned gate corpus.

For every gate in gates.json with a cloned repo_dir, scans source files for:

  - threshold-like float constants near decision keywords
    (threshold/confidence/deny/allow/block/risk/score/prob)
  - Jev primitive usage (noul/choice/score/systemone, /v1/systemone endpoint)
  - error-path candidates (try/except or .catch near HTTP calls, exit codes,
    timeout handling, "fail open/closed" comments)
  - whether raw tool-call / diff text is passed to the model (heuristic:
    tool input / diff content interpolated into the state/questions payload)

Output is CANDIDATE evidence with file:line refs, written into gates.json under
"auto_evidence". Every field is verified by manual reading afterwards; nothing
here is paper-ready on its own. Stdlib only (os/re/json).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATES = os.path.join(HERE, "gates.json")

CODE_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".rs", ".go",
            ".rb", ".java", ".kt", ".swift", ".sh", ".bash", ".lua", ".ex",
            ".exs", ".php", ".cs", ".toml", ".yaml", ".yml", ".json", ".md"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "target",
             "__pycache__", ".venv", "venv", "coverage"}
MAX_FILE_BYTES = 400_000
MAX_HITS_PER_KIND = 25

FLOAT_RE = re.compile(r"(?<![\w.])(0?\.\d{1,4}|1\.0{1,4})(?![\w.])")
KEYWORD_RE = re.compile(
    r"threshold|confidence|deny|denied|allow|block|risk|score|prob|min_?conf|"
    r"cutoff|above|below|min_?prob", re.IGNORECASE)
PRIMITIVE_RE = re.compile(
    r"\b(noul|choice|score|systemone|system_one|/v1/systemone|boolean)\b",
    re.IGNORECASE)
HTTP_RE = re.compile(
    r"fetch\(|axios|requests\.|httpx|urllib|reqwest|http::|\.post\(|got\(|"
    r"undici|ofetch|\$http|curl", re.IGNORECASE)
ERROR_RE = re.compile(
    r"try\b|except\b|catch\b|rescue\b|timeout|timed?\s*out|exit\s*\(?\s*\d|"
    r"process\.exit|os\.exit|sys\.exit|429|5\d\d\b|fail[ -]?(open|closed|safe)|"
    r"on error|on failure|fallback|malformed|invalid json|parse error",
    re.IGNORECASE)
RAW_TEXT_RE = re.compile(
    r"tool_?(input|call|use|args|parameters)|command|diff|patch|staged|"
    r"transcript|file_?content|snippet|chunk", re.IGNORECASE)
STATE_PAYLOAD_RE = re.compile(
    r"state[\"']?\s*[:=]|questions[\"']?\s*[:=]|\"state\"|\'state\'", re.IGNORECASE)


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in CODE_EXT:
                p = os.path.join(dirpath, fn)
                try:
                    if os.path.getsize(p) <= MAX_FILE_BYTES:
                        yield p
                except OSError:
                    pass


def scan_repo(root):
    thresholds, primitives, error_paths, raw_text = [], [], [], []
    for path in iter_files(root):
        rel = os.path.relpath(path, root)
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if len(thresholds) < MAX_HITS_PER_KIND:
                for m in FLOAT_RE.finditer(line):
                    window = line[max(0, m.start() - 80): m.end() + 80]
                    if KEYWORD_RE.search(window):
                        thresholds.append({
                            "file": rel, "line": i,
                            "constant": m.group(1),
                            "text": line.strip()[:200]})
                        break
            if len(primitives) < MAX_HITS_PER_KIND and PRIMITIVE_RE.search(line):
                primitives.append({"file": rel, "line": i, "text": line.strip()[:200]})
            if len(error_paths) < MAX_HITS_PER_KIND and ERROR_RE.search(line):
                error_paths.append({"file": rel, "line": i, "text": line.strip()[:200]})
            if len(raw_text) < MAX_HITS_PER_KIND and RAW_TEXT_RE.search(line) and (
                    STATE_PAYLOAD_RE.search(line) or "state" in line.lower()
                    or "question" in line.lower()):
                raw_text.append({"file": rel, "line": i, "text": line.strip()[:200]})
    return {
        "threshold_candidates": thresholds,
        "primitive_usage": primitives,
        "error_path_candidates": error_paths,
        "raw_text_to_model_candidates": raw_text,
    }


def main():
    with open(GATES) as f:
        data = json.load(f)
    for g in data["gates"]:
        rd = g.get("repo_dir")
        if not rd:
            continue
        root = os.path.join(HERE, rd)
        if not os.path.isdir(root):
            continue
        g["auto_evidence"] = scan_repo(root)
        n = {k: len(v) for k, v in g["auto_evidence"].items()}
        print(f"{g['name']:<28} thresholds={n['threshold_candidates']:<3} "
              f"prims={n['primitive_usage']:<3} errpath={n['error_path_candidates']:<3} "
              f"rawtext={n['raw_text_to_model_candidates']:<3}")
    with open(GATES, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    sys.exit(main())
