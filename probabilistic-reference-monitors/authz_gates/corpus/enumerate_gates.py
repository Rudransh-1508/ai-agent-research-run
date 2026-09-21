#!/usr/bin/env python3
"""Enumerate candidate Jev authorization-gate projects from yibie/awesome-jev.

Fetches the awesome-jev README plus the category source files, parses entries,
selects candidates (all of "Verification & Guardrails" + decision-gate keyword
matches in "Agent Decisions", "Infra / SDKs / Integrations", and
"Content Moderation"), and applies the PREREGISTRATION.md inclusion criteria as
far as automatable:

  (a) gate semantics      -> keyword pre-filter only; final decision is manual
                             (FINAL_DECISIONS below, filled in after code read)
  (b) runnable code       -> needs a clonable URL; verified in clone_corpus.py
  (c) public before 2026-10-01 -> GitHub API created_at (fallback: `gh api`)
  (d) listed in awesome-jev -> true by construction

Writes gates.json: name, url, category, one-line purpose, inclusion status +
reason. Stdlib only (urllib/subprocess/json/re).

Re-running reproduces gates.json deterministically except for the GitHub API
fields (created_at) and the FINAL_DECISIONS block, which records manual calls.
"""

import json
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import date

BASE = "https://raw.githubusercontent.com/yibie/awesome-jev/main"
CATEGORIES = {
    "Verification & Guardrails": "categories/verification-guardrails.md",
    "Agent Decisions": "categories/agent-decisions.md",
    "Infra / SDKs / Integrations": "categories/infra-sdks-integrations.md",
    "Content Moderation": "categories/content-moderation.md",
}
OUT = "gates.json"
TODAY = "2026-09-21"
CUTOFF = "2026-10-01"  # inclusion criterion (c)

# Decision-gate keywords for the non-Verification categories (criterion (a)
# pre-filter; every hit is still manually reviewed).
GATE_KEYWORDS = re.compile(
    r"\b(gate|gating|gates|permission|approval|approvals|block|blocks|blocking|"
    r"guard|guardrail|hook|stop hook|authori[sz]ation|moderat\w+|verif\w+|"
    r"pre-commit|commit|deny|denied|allow|escalat\w+|risk|inject\w+|safety|"
    r"safe|screen\w+|veto|abort\w+|completion)\b",
    re.IGNORECASE,
)

# Entries that match keywords but are not authorization gates (manual review,
# 2026-09-21): they route, rank, prune context, or expose Jev as a tool without
# themselves deciding whether an agent action proceeds.
NOT_A_GATE = {
    "pi-typesafe-jev": "exposes Jev judgments as Pi tools; thresholds/actions stay with the caller",
    "pi-quiet-ask": "decision layer for judgments, no action gate",
    "jev-judgment": "skill that forwards judgments; no allow/deny path of its own",
    "yoshi": "context pruning, not authorization",
    "pi-fast-jev-compaction": "context compaction, not authorization",
    "fast-jev-compaction": "context compaction, not authorization",
    "fast-dev-compaction": "context compaction, not authorization",
    "jev-pruner": "output trimming, not authorization",
    "jev-agent-skill": "offloads judgments; no gate",
    "jev-skill-suggester": "recommends skills, does not gate actions",
    "jevify": "skill that designs Jev loops; no gate",
    "jev-architect": "design skill; no gate",
    "grok-bot-jev": "decision layer bridge; usage gates are rate limits, not action authorization",
    "jev-usecases": "reference harnesses; confidence-gated logic but no agent-action gate",
    "Jev Moderation Bot": "Discord message moderation; not an agent-action gate",
    "profanity-checker": "text classification service; not an agent-action gate",
    "PlotVeil": "spoiler cover on YouTube comments; not an agent-action gate",
    "jev_antispam_bot": "Telegram anti-spam; not an agent-action gate",
    "Jev Chat for Twitch": "chat filtering display; not an agent-action gate",
    "jev-spam-eval": "spam classification benchmark; no gate",
    "jev-experiments": "demo collection; shell-guard demo checked separately (see notes)",
    "Smithers": "workflow session checker is a health check, not action authorization",
    "jev-mcp (jkudish)": "exposes Jev as MCP tools; no gate of its own",
    "jev-mcp (blakestone-x)": "exposes Jev as MCP tools; no gate of its own",
    "jev-mcp (burnigtm)": "exposes Jev as MCP tools; no gate of its own",
    "decide-mcp": "decision server; routing/bias profiles, not action authorization",
    "Jevbridge": "adapter; no gate",
    "openrouter-jev-mcp": "gateway; no gate",
    "JarvisCore": "agent framework with an injection filter on RAG passages; checked manually (see notes)",
    # Excluded after reading the cloned code (2026-09-21):
    "stanley-code": "advisory-only review tool, verified in code: src/cli/output.ts:36 'advisory only', line 48 'this is not an approval', line 15 'Exit codes 1 and 2 are never used: exit 2 is a blocking signal in some agent hooks' — it decides nothing about whether an action proceeds (criterion a)",
    "jev-superpowers": "never calls the Jev API itself (no api.typesafe/systemone reference anywhere in the repo); its hooks are deterministic bash (hooks/stop, hooks/pre-commit) or delegate to jev-git/limpet/supercov — a composition layer, not a gate (criteria a/b)",
    "jev-agent-browser": "delegates bounded browser tasks; no allow/deny of agent actions",
    "augustus": "skill mapping Jev primitives onto classical methods; no gate",
    "jev-canvas": "voice drawing UI; thresholds gate drawing commands, not agent authorization",
    "Jev for Chrome": "browser automation loop; no authorization gate",
    "DataJev": "loop-direction control (continue/switch/stop) for a data-analysis agent; not authorization of actions",
    "laravel-typesafe-jev": "SDK/integration; no gate",
    "advocaat": "dataset query client; no gate",
}

# Known-bad entries (existence verified 2026-09-21).
KNOWN_NONEXISTENT = {"harshwasan/jev-sentinel"}

# Entries the keyword filter misses but the study scope explicitly covers.
FORCE_INCLUDE = {
    "super-jev": "decision harness turning Jev answers into bounded actions",
    "jev-superpowers": "completion gates for AI coding agents",
    "wakegate": "gates whether a sleeping agent is woken (pilot-set member)",
}

# Confirmed included after the 2026-09-21 code read (extraction in
# manual_extraction.json). These get final status "included".
FINAL_INCLUDED = {
    "is-malicious", "jev-review", "pi-jev", "OpenWork", "jev-guard", "Foreman",
    "opencompany", "jev-git", "pi-heed", "Hunch", "Abide", "fx", "Sniff Test",
    "jev-pref", "jev-axi", "pi-verdict", "jev-commit", "hermes-jev-approvals",
    "taste-lint", "jev-engineering", "Reflex", "r2r-jev", "limpet",
    "dsh-auto-mode", "super-jev", "wakegate", "jev-belay", "JevLoop", "jev-use",
    "mastra-jev-moderation", "jev-harness",
}

ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\) - (?:(\w[^:]{0,60}): )?(.*)$")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "authz-gates-corpus/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse_entries(text: str, category: str):
    out = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ENTRY_RE.match(line.strip())
        if m:
            name, url, industry, desc = m.groups()
            out.append({
                "name": name.strip(),
                "url": url.strip(),
                "industry": (industry or "").strip(),
                "purpose": desc.strip(),
                "category": category,
            })
    return out


def github_created_at(owner_repo: str):
    """Return (created_at, exists) via GitHub API; fall back to gh CLI."""
    url = f"https://api.github.com/repos/{owner_repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "authz-gates-corpus/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data.get("created_at"), True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, False
    except Exception:
        pass
    try:
        p = subprocess.run(
            ["gh", "api", f"repos/{owner_repo}", "--jq", ".created_at"],
            capture_output=True, text=True, timeout=30,
        )
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip(), True
        return None, False
    except Exception:
        return None, None


def main():
    entries = []
    for cat, path in CATEGORIES.items():
        text = fetch(f"{BASE}/{path}")
        entries.extend(parse_entries(text, cat))

    # Preserve fields added by later phases (pinned_sha, clone_date, repo_dir,
    # auto_evidence) when re-running enumeration over an existing gates.json.
    prior = {}
    try:
        with open(OUT) as f:
            prior = {g["name"]: g for g in json.load(f)["gates"]}
    except (OSError, json.JSONDecodeError):
        pass

    gates = []
    for e in entries:
        in_vg = e["category"] == "Verification & Guardrails"
        kw_hit = bool(GATE_KEYWORDS.search(e["purpose"]) or GATE_KEYWORDS.search(e["name"]))
        forced = e["name"] in FORCE_INCLUDE
        if not in_vg and not kw_hit and not forced:
            continue
        if e["name"] in NOT_A_GATE:
            gates.append({**e, "inclusion": "excluded",
                          "reason": f"not an agent-action authorization gate: {NOT_A_GATE[e['name']]}"})
            continue

        m = re.match(r"https://github\.com/([^/]+/[^/#?]+)", e["url"])
        gh = m.group(1).rstrip("/") if m else None

        if gh and gh in KNOWN_NONEXISTENT:
            gates.append({**e, "inclusion": "excluded", "reason": "repository does not exist (verified 2026-09-21)"})
            continue

        if not gh:
            if re.match(r"https?://git\.", e["url"]) or e["url"].endswith(".git"):
                gates.append({**e, "inclusion": "included-pending-code-read",
                              "reason": "non-GitHub git host; clone attempted in clone_corpus.py; criterion (c) checked manually"})
            else:
                gates.append({**e, "inclusion": "excluded",
                              "reason": "no public source repository URL (website only); cannot verify runnable code (criterion b)"})
            continue

        created, exists = github_created_at(gh)
        if exists is False:
            gates.append({**e, "inclusion": "excluded", "reason": "GitHub repository not found (404) on 2026-09-21"})
            continue
        rec = dict(e)
        rec["github"] = gh
        if created:
            rec["created_at"] = created
            if created[:10] >= CUTOFF:
                gates.append({**rec, "inclusion": "excluded",
                              "reason": f"created {created[:10]}, not public before {CUTOFF} (criterion c)"})
                continue
        else:
            rec["created_at"] = "unchecked (API unavailable)"
        gates.append({**rec, "inclusion": "included-pending-code-read",
                      "reason": "listed in awesome-jev; gate semantics and runnable code verified in clone/extract phases"})

    for g in gates:
        if g["name"] in FINAL_INCLUDED and g["inclusion"] == "included-pending-code-read":
            g["inclusion"] = "included"
            g["reason"] = "code read 2026-09-21; per-field extraction with file:line evidence in manual_extraction.json"

    KEEP = ("pinned_sha", "clone_date", "repo_dir", "auto_evidence")
    for g in gates:
        old = prior.get(g["name"])
        if old:
            for k in KEEP:
                if k in old:
                    g[k] = old[k]

    with open(OUT, "w") as f:
        json.dump({"generated": TODAY, "source": "https://github.com/yibie/awesome-jev",
                   "gates": gates}, f, indent=2)
    inc = [g for g in gates if g["inclusion"].startswith("included")]
    exc = [g for g in gates if g["inclusion"] == "excluded"]
    print(f"candidates: {len(gates)}  included-pending: {len(inc)}  excluded: {len(exc)}")
    for g in exc:
        print(f"  EXCLUDED {g['name']}: {g['reason']}")


if __name__ == "__main__":
    sys.exit(main())
