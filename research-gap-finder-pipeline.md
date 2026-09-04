# Research Gap Finder — Implementation Pipeline

## Overview

A tool that ingests a GitHub markdown list of research papers (arXiv links), fetches their abstracts, and uses an LLM to identify research gaps across the corpus.

---

## Pipeline Stages

```
GitHub Markdown URL
        │
        ▼
  [1] Parse Paper List
        │
        ▼
  [2] Fetch Abstracts (arXiv API)
        │
        ▼
  [3] Batch Analysis (Claude API)
        │
        ▼
  [4] Gap Synthesis (Claude API)
        │
        ▼
  Structured Gap Report
```

---

## Stage 1 — Parse Paper List

**Input:** GitHub raw markdown URL (e.g. `capability-papers/safety.md`)  
**Output:** List of `{ title, arXiv_id, date }` objects

**Steps:**
1. Fetch raw markdown via `GET https://raw.githubusercontent.com/{repo}/main/{path}`
2. Regex match all arXiv links: `/https:\/\/arxiv\.org\/abs\/([\d.]+)/g`
3. Extract paper title from the surrounding markdown bold text
4. Extract date from the `[Mon YYYY]` prefix on each line

**Notes:**
- The GitHub HTML page is not needed; always fetch the raw file to avoid parsing GitHub UI chrome
- Some entries have typos (`ppaer` instead of `paper`) — normalize before matching
- Skip non-arXiv links (e.g. `papers.ssrn.com`)

---

## Stage 2 — Fetch Abstracts

**Input:** List of arXiv IDs  
**Output:** Same list with `abstract` field populated

**Method:** arXiv HTML scrape (CORS-safe from browser)

```
GET https://export.arxiv.org/abs/{id}
```

Parse the `.abstract` DOM element, strip the `"Abstract:"` prefix.

**Batching:** Fetch 12 papers in parallel per round (`Promise.all`), then next round. This avoids rate limits while keeping it fast.

**Fallback:** If abstract is null (network error, bad ID), mark `abstract: null` and skip in analysis — don't abort the pipeline.

---

## Stage 3 — Batch Analysis

**Input:** Groups of 10 papers with abstracts  
**Output:** Per-batch `{ themes, methods, problems_addressed }`

**Prompt structure:**

```
You are a research analyst. Here are abstracts from N papers on [topic].
Identify the key research themes, methodologies used, and what problems they address.

[paper abstracts]

Respond ONLY with JSON:
{
  "themes": [{ "name", "papers", "description" }],
  "methods": ["string"],
  "problems_addressed": ["string"]
}
```

**Why batch at 10:** Keeps each Claude call within a focused context window. Larger batches risk dilution; smaller batches increase API cost.

**Error handling:** If a batch fails to parse as JSON, skip it and continue — partial coverage is better than a full abort.

---

## Stage 4 — Gap Synthesis

**Input:** All themes, methods, and problems aggregated across batches  
**Output:** Structured gap report

**Prompt structure:**

```
You are a senior researcher. Based on findings from N papers on [topic],
identify the most significant research gaps — areas that are under-explored,
contradictory, or missing entirely.

THEMES COVERED: [...]
METHODS USED: [...]
PROBLEMS ADDRESSED: [...]

Respond ONLY with JSON:
{
  "gaps": [{
    "title": string,
    "severity": "high|medium|low",
    "description": string,
    "why_matters": string,
    "direction": string,
    "related_themes": [string]
  }],
  "summary": string,
  "dominant_areas": [string],
  "neglected_areas": [string]
}
```

**Deduplication:** Before sending, deduplicate methods and problems with `[...new Set(arr)]` to reduce noise and token use.

---

## Data Schema

### Paper object
```ts
{
  title: string
  url: string
  id: string          // arXiv ID, e.g. "2401.10019"
  date: string        // e.g. "Jan 2024"
  abstract: string | null
}
```

### Gap object
```ts
{
  title: string
  severity: "high" | "medium" | "low"
  description: string      // 2–3 sentences
  why_matters: string      // 1 sentence, real-world implication
  direction: string        // 1 sentence, suggested research direction
  related_themes: string[]
}
```

### Final report
```ts
{
  gaps: Gap[]
  summary: string
  dominant_areas: string[]
  neglected_areas: string[]
}
```

---

## Error Handling Strategy

| Failure point | Behaviour |
|---|---|
| GitHub fetch fails | Show error, abort |
| arXiv fetch fails for a paper | Skip paper, continue |
| Claude batch analysis fails | Skip batch, continue with rest |
| Claude gap synthesis fails | Retry once, then show error |
| JSON parse error from Claude | Strip markdown fences, retry parse |

---

## Configuration

| Parameter | Default | Notes |
|---|---|---|
| `FETCH_BATCH_SIZE` | 12 | Parallel arXiv fetches per round |
| `ANALYZE_BATCH_SIZE` | 10 | Papers per Claude analysis call |
| `MODEL` | `claude-sonnet-4-6` | Synthesis model |
| `MAX_TOKENS` | 1000 | Per Claude call |

---

## Extending to Other Paper Lists

The only input that changes per corpus is the GitHub markdown URL. To support other categories (e.g. `planning.md`, `memory.md`):

1. Accept URL as user input
2. Fetch raw markdown
3. Run the same pipeline — stages 2–4 are fully generic

The analysis prompt can optionally be seeded with the category name (e.g. "AI agent planning papers") for more contextually relevant gap identification.
