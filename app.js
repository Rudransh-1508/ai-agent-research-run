/* ============================================================
   Research Gap Finder — Pipeline Implementation
   Follows: research-gap-finder-pipeline.md
   LLM: Groq (llama-3.3-70b-versatile)  instead of Claude
   ============================================================ */

// ─── CONFIG ───────────────────────────────────────────────────
const CONFIG = {
  FETCH_BATCH_SIZE: 12,      // parallel arXiv fetches
  ANALYZE_BATCH_SIZE: 10,    // papers per Groq call
  MODEL: 'llama-3.3-70b-versatile',
  MAX_TOKENS: 2048,
  GROQ_ENDPOINT: 'https://api.groq.com/openai/v1/chat/completions',
};

// ─── STATE ────────────────────────────────────────────────────
let _reportData = null;

// ─── DOM HELPERS ──────────────────────────────────────────────
const $ = id => document.getElementById(id);

function log(msg, level = 'info') {
  const box = $('log-lines');
  const now = new Date();
  const ts = now.toTimeString().slice(0, 8);
  const el = document.createElement('div');
  el.className = `log-line ${level}`;
  el.innerHTML = `<span class="log-time">${ts}</span><span class="log-msg">${escHtml(msg)}</span>`;
  box.appendChild(el);
  box.scrollTop = box.scrollHeight;
}

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function setStage(n, state, statusText) {
  const el = $(`stage-${n}`);
  el.className = `stage-item ${state}`;
  el.querySelector('.stage-status').textContent = statusText;
}

function showError(msg) {
  const b = $('error-banner');
  $('error-msg').textContent = msg;
  b.style.display = 'flex';
}

function hideError() {
  $('error-banner').style.display = 'none';
}

// ─── EYE TOGGLE ───────────────────────────────────────────────
$('toggle-key').addEventListener('click', () => {
  const inp = $('groq-key');
  const isPass = inp.type === 'password';
  inp.type = isPass ? 'text' : 'password';
  $('eye-icon').innerHTML = isPass
    ? `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>`
    : `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>`;
});

// ─── MAIN ENTRY ───────────────────────────────────────────────
async function runPipeline() {
  const ghUrl = $('gh-url').value.trim();
  const apiKey = $('groq-key').value.trim();

  if (!ghUrl) { showError('Please enter a GitHub markdown URL.'); return; }
  if (!apiKey) { showError('Please enter your Groq API key.'); return; }
  if (!ghUrl.includes('github.com')) { showError('URL must be a GitHub link.'); return; }

  hideError();

  // Reset UI
  $('results-section').style.display = 'none';
  $('progress-section').style.display = 'block';
  $('log-lines').innerHTML = '';
  for (let i = 1; i <= 4; i++) setStage(i, '', 'Waiting…');

  const btn = $('run-btn');
  btn.disabled = true;
  btn.innerHTML = `<div class="spinner"></div> Analyzing…`;

  try {
    // ── STAGE 1 ──────────────────────────────────────────────
    setStage(1, 'active', 'Fetching…');
    log('Stage 1 — Parsing paper list from GitHub…');

    const papers = await stage1_parsePaperList(ghUrl);
    setStage(1, 'done', `${papers.length} papers found`);
    log(`Found ${papers.length} arXiv papers.`, 'ok');

    if (papers.length === 0) throw new Error('No arXiv papers found in this markdown file.');

    // ── STAGE 2 ──────────────────────────────────────────────
    setStage(2, 'active', 'Fetching abstracts…');
    log(`Stage 2 — Fetching abstracts in batches of ${CONFIG.FETCH_BATCH_SIZE}…`);

    const papersWithAbstracts = await stage2_fetchAbstracts(papers, (done, total) => {
      setStage(2, 'active', `${done}/${total} fetched`);
    });

    const withAbs = papersWithAbstracts.filter(p => p.abstract);
    setStage(2, 'done', `${withAbs.length}/${papers.length} abstracts retrieved`);
    log(`Abstracts retrieved: ${withAbs.length}/${papers.length}`, 'ok');

    if (withAbs.length === 0) throw new Error('Could not fetch any abstracts. Check your network connection.');

    // ── STAGE 3 ──────────────────────────────────────────────
    setStage(3, 'active', 'Analyzing batches…');
    log(`Stage 3 — Batch analysis (${CONFIG.ANALYZE_BATCH_SIZE} papers/call via Groq)…`);

    const topic = extractTopicFromUrl(ghUrl);
    const batchResults = await stage3_batchAnalysis(withAbs, topic, apiKey, (b, total) => {
      setStage(3, 'active', `Batch ${b}/${total} done`);
    });

    setStage(3, 'done', `${batchResults.length} batches analyzed`);
    log(`Batch analysis complete — ${batchResults.length} batches.`, 'ok');

    // ── STAGE 4 ──────────────────────────────────────────────
    setStage(4, 'active', 'Synthesizing gaps…');
    log('Stage 4 — Running gap synthesis via Groq…');

    const report = await stage4_gapSynthesis(batchResults, withAbs.length, topic, apiKey);
    setStage(4, 'done', `${report.gaps.length} gaps identified`);
    log(`Gap synthesis complete — ${report.gaps.length} gaps found.`, 'ok');

    // ── RENDER ───────────────────────────────────────────────
    _reportData = report;
    renderResults(report, withAbs.length, topic);

  } catch (err) {
    log(`ERROR: ${err.message}`, 'error');
    showError(err.message);
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg> Analyze Research Gaps`;
  }
}

// ══════════════════════════════════════════════════════════════
// STAGE 1 — Parse Paper List
// ══════════════════════════════════════════════════════════════
async function stage1_parsePaperList(ghUrl) {
  const rawUrl = githubToRaw(ghUrl);
  log(`Fetching raw markdown: ${rawUrl}`);

  const resp = await fetch(rawUrl);
  if (!resp.ok) throw new Error(`GitHub fetch failed: ${resp.status} ${resp.statusText}`);

  const md = await resp.text();
  return parsePapers(md);
}

function githubToRaw(url) {
  // https://github.com/user/repo/blob/main/path → https://raw.githubusercontent.com/user/repo/main/path
  return url
    .replace('https://github.com/', 'https://raw.githubusercontent.com/')
    .replace('/blob/', '/');
}

function parsePapers(md) {
  // Normalize common typos
  const text = md.replace(/ppaer/g, 'paper').replace(/Ppaer/g, 'Paper');

  const papers = [];
  const lines = text.split('\n');

  // Match lines with arXiv links
  const arxivRe = /https:\/\/arxiv\.org\/abs\/([\d.]+)/g;
  const dateRe = /\[([A-Za-z]+ \d{4})\]/;

  for (const line of lines) {
    const dateMatch = line.match(dateRe);
    const date = dateMatch ? dateMatch[1] : '';

    let match;
    arxivRe.lastIndex = 0;

    while ((match = arxivRe.exec(line)) !== null) {
      const arXivId = match[1];

      // Extract bold title from **...** or just grab the text between [[ and ]](url)
      let title = extractTitle(line);

      papers.push({
        id: arXivId,
        title: title || `Paper ${arXivId}`,
        url: `https://arxiv.org/abs/${arXivId}`,
        date,
        abstract: null,
      });
    }
  }

  // Deduplicate by arXiv ID
  const seen = new Set();
  return papers.filter(p => {
    if (seen.has(p.id)) return false;
    seen.add(p.id);
    return true;
  });
}

function extractTitle(line) {
  // Try **Title** pattern
  const boldMatch = line.match(/\*\*(.+?)\*\*/);
  if (boldMatch) return boldMatch[1].trim();

  // Try [Title](url) markdown link pattern
  const linkMatch = line.match(/\[([^\]]+)\]\(https:\/\/arxiv\.org/);
  if (linkMatch) return linkMatch[1].trim();

  // Try plain text before the URL
  const beforeUrl = line.split('https://arxiv.org')[0].replace(/[-*\[\]]/g, '').trim();
  if (beforeUrl.length > 5 && beforeUrl.length < 200) return beforeUrl;

  return '';
}

function extractTopicFromUrl(url) {
  // e.g. safety.md → "Safety", capability-papers/memory.md → "Memory"
  const parts = url.split('/');
  const filename = parts[parts.length - 1].replace('.md', '');
  return filename
    .split(/[-_]/)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

// ══════════════════════════════════════════════════════════════
// STAGE 2 — Fetch Abstracts  (arXiv Atom API — batch per round)
// ══════════════════════════════════════════════════════════════
async function stage2_fetchAbstracts(papers, onProgress) {
  const result = [...papers];
  let done = 0;

  // Fetch CONFIG.FETCH_BATCH_SIZE IDs per API call instead of one at a time.
  // The arXiv /api/query endpoint supports comma-separated id_list and has CORS headers.
  for (let i = 0; i < result.length; i += CONFIG.FETCH_BATCH_SIZE) {
    const batch = result.slice(i, i + CONFIG.FETCH_BATCH_SIZE);
    const ids = batch.map(p => p.id).join(',');

    let abstractMap = {};
    try {
      abstractMap = await fetchAbstractsBatch(ids, batch.length);
    } catch (err) {
      log(`⚠ Batch fetch failed (${err.message}), will mark as null`, 'warn');
    }

    for (const paper of batch) {
      // arXiv API may return versioned IDs like "2401.10019v3" — strip version
      const abs = abstractMap[paper.id] || abstractMap[paper.id + 'v1'] || null;
      paper.abstract = abs;
      if (!abs) log(`⚠ No abstract for ${paper.id}`, 'warn');
      done++;
      onProgress(done, result.length);
    }
  }

  return result;
}

/**
 * Fetch abstracts for a comma-separated list of arXiv IDs in one API call.
 * Uses the arXiv Atom/OpenSearch API which returns XML with CORS headers.
 * Falls back to allorigins proxy if direct fetch is blocked.
 */
async function fetchAbstractsBatch(idList, maxResults) {
  const apiUrl = `https://export.arxiv.org/api/query?id_list=${idList}&max_results=${maxResults}`;

  let xmlText = null;

  // 1) Try direct fetch — arXiv API usually allows CORS
  try {
    const resp = await fetch(apiUrl, { mode: 'cors' });
    if (resp.ok) {
      xmlText = await resp.text();
    }
  } catch (_) { /* CORS blocked — fall through */ }

  // 2) Fallback: allorigins CORS proxy
  if (!xmlText) {
    try {
      const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(apiUrl)}`;
      const resp = await fetch(proxyUrl, { signal: AbortSignal.timeout(15000) });
      if (resp.ok) {
        const data = await resp.json();
        xmlText = data.contents || null;
      }
    } catch (_) {}
  }

  // 3) Fallback 2: corsproxy.io
  if (!xmlText) {
    const proxyUrl = `https://corsproxy.io/?${encodeURIComponent(apiUrl)}`;
    const resp = await fetch(proxyUrl, { signal: AbortSignal.timeout(15000) });
    if (resp.ok) xmlText = await resp.text();
  }

  if (!xmlText) throw new Error('All proxy attempts failed');

  return parseArxivXML(xmlText);
}

/**
 * Parse arXiv Atom XML and return a map of { arxivId: abstractText }
 */
function parseArxivXML(xml) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(xml, 'text/xml');
  const entries = doc.querySelectorAll('entry');
  const result = {};

  for (const entry of entries) {
    const idEl = entry.querySelector('id');
    const summaryEl = entry.querySelector('summary');
    if (!idEl || !summaryEl) continue;

    // Full ID looks like: http://arxiv.org/abs/2401.10019v3
    const fullId = idEl.textContent || '';
    const match = fullId.match(/abs\/(\d{4}\.\d+)/);
    if (match) {
      const id = match[1];  // e.g. "2401.10019"
      result[id] = summaryEl.textContent.trim().replace(/\s+/g, ' ');
    }
  }

  return result;
}

// ══════════════════════════════════════════════════════════════
// STAGE 3 — Batch Analysis
// ══════════════════════════════════════════════════════════════
async function stage3_batchAnalysis(papers, topic, apiKey, onProgress) {
  const results = [];
  const batches = [];

  for (let i = 0; i < papers.length; i += CONFIG.ANALYZE_BATCH_SIZE) {
    batches.push(papers.slice(i, i + CONFIG.ANALYZE_BATCH_SIZE));
  }

  log(`Processing ${batches.length} batch(es) of ~${CONFIG.ANALYZE_BATCH_SIZE} papers…`);

  for (let b = 0; b < batches.length; b++) {
    const batch = batches[b];
    log(`Sending batch ${b + 1}/${batches.length} to Groq (${batch.length} papers)…`);

    try {
      const result = await analyzeBatch(batch, topic, apiKey);
      results.push(result);
      log(`Batch ${b + 1} ✓ — ${result.themes?.length ?? 0} themes found`, 'ok');
    } catch (err) {
      log(`Batch ${b + 1} failed: ${err.message} — skipping`, 'warn');
    }

    onProgress(b + 1, batches.length);
  }

  return results;
}

async function analyzeBatch(papers, topic, apiKey) {
  const abstracts = papers.map((p, i) =>
    `[${i + 1}] "${p.title}" (${p.date})\n${p.abstract}`
  ).join('\n\n---\n\n');

  const prompt = `You are a research analyst. Here are abstracts from ${papers.length} papers on ${topic}.
Identify the key research themes, methodologies used, and what problems they address.

${abstracts}

Respond ONLY with valid JSON (no markdown fences, no explanation):
{
  "themes": [{ "name": "string", "papers": ["string"], "description": "string" }],
  "methods": ["string"],
  "problems_addressed": ["string"]
}`;

  const raw = await groqCall(prompt, apiKey);
  return parseJSON(raw);
}

// ══════════════════════════════════════════════════════════════
// STAGE 4 — Gap Synthesis
// ══════════════════════════════════════════════════════════════
async function stage4_gapSynthesis(batchResults, totalPapers, topic, apiKey) {
  // Aggregate and deduplicate
  const allThemes = batchResults.flatMap(b => (b.themes || []).map(t => `${t.name}: ${t.description}`));
  const allMethods = [...new Set(batchResults.flatMap(b => b.methods || []))];
  const allProblems = [...new Set(batchResults.flatMap(b => b.problems_addressed || []))];

  log(`Aggregated: ${allThemes.length} themes, ${allMethods.length} methods, ${allProblems.length} problems`);

  const prompt = `You are a senior researcher. Based on findings from ${totalPapers} papers on ${topic}, identify the most significant research gaps — areas that are under-explored, contradictory, or missing entirely.

THEMES COVERED:
${allThemes.slice(0, 40).join('\n')}

METHODS USED:
${allMethods.slice(0, 30).join(', ')}

PROBLEMS ADDRESSED:
${allProblems.slice(0, 30).join('\n')}

Respond ONLY with valid JSON (no markdown fences, no explanation):
{
  "gaps": [{
    "title": "string",
    "severity": "high|medium|low",
    "description": "string (2-3 sentences)",
    "why_matters": "string (1 sentence, real-world implication)",
    "direction": "string (1 sentence, suggested research direction)",
    "related_themes": ["string"]
  }],
  "summary": "string (3-5 sentences overview)",
  "dominant_areas": ["string"],
  "neglected_areas": ["string"]
}`;

  let raw;
  try {
    raw = await groqCall(prompt, apiKey);
  } catch (err) {
    log('Gap synthesis failed, retrying once…', 'warn');
    raw = await groqCall(prompt, apiKey);
  }

  return parseJSON(raw);
}

// ══════════════════════════════════════════════════════════════
// GROQ API CALL
// ══════════════════════════════════════════════════════════════
async function groqCall(prompt, apiKey) {
  const resp = await fetch(CONFIG.GROQ_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: CONFIG.MODEL,
      max_tokens: CONFIG.MAX_TOKENS,
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
    }),
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(`Groq API error ${resp.status}: ${err?.error?.message || resp.statusText}`);
  }

  const data = await resp.json();
  return data.choices?.[0]?.message?.content || '';
}

// ──────────────────────────────────────────────────────────────
// JSON Parse Helper (strips markdown fences)
// ──────────────────────────────────────────────────────────────
function parseJSON(raw) {
  // Strip markdown code fences
  let text = raw.trim()
    .replace(/^```(?:json)?\s*/i, '')
    .replace(/\s*```$/, '')
    .trim();

  // Find first { and last } to extract JSON object
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start !== -1 && end !== -1) {
    text = text.slice(start, end + 1);
  }

  return JSON.parse(text);
}

// ══════════════════════════════════════════════════════════════
// RENDER RESULTS
// ══════════════════════════════════════════════════════════════
function renderResults(report, paperCount, topic) {
  $('results-meta').textContent = `${paperCount} papers analyzed · ${report.gaps?.length ?? 0} gaps identified · Topic: ${topic}`;

  // Summary
  const sc = $('summary-card');
  sc.innerHTML = `
    <div class="summary-card-title">📋 Executive Summary</div>
    <p>${escHtml(report.summary || 'No summary generated.')}</p>
  `;

  // Dominant / Neglected
  const ar = $('areas-row');
  ar.innerHTML = `
    <div class="area-card dominant">
      <div class="area-card-title">🔥 Dominant Areas</div>
      <div>${(report.dominant_areas || []).map(a => `<span class="area-tag">${escHtml(a)}</span>`).join('')}</div>
    </div>
    <div class="area-card neglected">
      <div class="area-card-title">🕳 Neglected Areas</div>
      <div>${(report.neglected_areas || []).map(a => `<span class="area-tag">${escHtml(a)}</span>`).join('')}</div>
    </div>
  `;

  // Sort gaps: high → medium → low
  const sevOrder = { high: 0, medium: 1, low: 2 };
  const gaps = [...(report.gaps || [])].sort((a, b) =>
    (sevOrder[a.severity] ?? 3) - (sevOrder[b.severity] ?? 3)
  );

  const grid = $('gaps-grid');
  grid.innerHTML = gaps.map((gap, i) => `
    <div class="gap-card ${gap.severity || 'low'}" id="gap-${i}">
      <div class="gap-card-head">
        <div class="gap-card-title">${escHtml(gap.title)}</div>
        <span class="sev-badge ${gap.severity || 'low'}">${gap.severity || 'unknown'}</span>
      </div>
      <div class="gap-description">${escHtml(gap.description)}</div>
      <div class="gap-meta-grid">
        <div class="gap-meta-item">
          <div class="gap-meta-label">💡 Why it matters</div>
          <div class="gap-meta-text">${escHtml(gap.why_matters || '—')}</div>
        </div>
        <div class="gap-meta-item">
          <div class="gap-meta-label">🧭 Research direction</div>
          <div class="gap-meta-text">${escHtml(gap.direction || '—')}</div>
        </div>
      </div>
      ${gap.related_themes?.length ? `
        <div class="gap-themes">
          ${gap.related_themes.map(t => `<span class="theme-tag">${escHtml(t)}</span>`).join('')}
        </div>` : ''}
    </div>
  `).join('');

  $('results-section').style.display = 'block';
  $('results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ─── DOWNLOAD JSON ─────────────────────────────────────────────
function downloadJSON() {
  if (!_reportData) return;
  const blob = new Blob([JSON.stringify(_reportData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'research-gap-report.json';
  a.click();
  URL.revokeObjectURL(url);
}
