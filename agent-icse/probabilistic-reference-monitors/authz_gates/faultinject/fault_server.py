#!/usr/bin/env python3
"""Local stand-in for the Jev endpoint that answers in one fault mode.

Every request is appended to --log as one JSON line (path, question names and
types), so a trial can prove the gate actually reached the model. A gate that
decides without calling the model is a different finding from a gate that
survives a fault.

Modes:
  yes            200, every question answered at its "true"/first/highest pole
  no             200, every question answered at its "false"/last/lowest pole
  http_400_max_tokens  400 max_tokens_exceeded (what an oversized state gets live)
  http_429       429 with Retry-After: 1
  http_500       500
  http_503       503
  timeout        accept the request, never answer (sleeps --hang seconds)
  malformed      200 with a non-JSON body
  schema_drift   200 with valid JSON but an empty answers map
The runner simulates connection refusal by pointing the redirect at a closed
port, so it needs no server mode.

Besides the Jev API, two other decision services are spoken, by path:
  /v1/messages            Anthropic Messages (LLM-judge gates); control text from
                          the recipe spec's "_anthropic_text"
  /v1/actions/authorize   AgentGuards authorize; control body from "_authorize"
In schema_drift mode each gets its own empty-but-valid body. When FI_MARKER is
set, each logged request records whether the request body contained it, so a
trial can show whether the dangerous part of a padded command reached the model.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODES = ("yes", "no", "http_400_max_tokens", "http_429", "http_500", "http_503", "timeout", "malformed",
         "schema_drift")


def _options(q):
    crit = q.get("criteria") or q.get("options") or q.get("choices") or []
    if isinstance(crit, dict):
        return list(crit)
    return [c if isinstance(c, str) else json.dumps(c) for c in crit]


def answer(q, pole):
    """Answer one typed question at the given pole ("yes" or "no")."""
    qtype = str(q.get("type") or q.get("primitive") or "noul").lower()
    hi = pole == "yes"
    if qtype in ("noul", "boolean", "bool"):
        p = 0.99 if hi else 0.01
        return {"type": qtype, "noul": p, "probability": p}
    opts = _options(q) or ["0", "1"]
    if qtype == "score":
        n = len(opts)
        level = n - 1 if hi else 0
        probs = {str(i): (0.96 if i == level else round(0.04 / (n - 1), 4)) for i in range(n)}
        return {"type": "score", "score": float(level), "probabilities": probs,
                "legend": {str(i): o for i, o in enumerate(opts)}, "confidence": 0.95}
    pick = opts[0] if hi else opts[-1]
    probs = {o: (0.96 if o == pick else round(0.04 / max(1, len(opts) - 1), 4)) for o in opts}
    return {"type": "choice", "choice": pick, "probabilities": probs, "confidence": 0.95}


def answer_from_spec(name, q, spec, pole):
    """A recipe may pin control answers per question name ("*" = any other);
    each value is merged over the generic pole answer."""
    base = answer(q, pole)
    over = spec.get(name, spec.get("*"))
    if over:
        base.update(over)
    return base


def chat_completion(content):
    """OpenAI-compatible body, for gates whose OpenRouter path uses chat completions."""
    return {"id": "fi", "object": "chat.completion", "model": "fi",
            "choices": [{"index": 0, "finish_reason": "stop",
                         "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": 1, "completion_tokens": 1}}


def make_handler(mode, log_path, hang_s, spec=None):
    spec = spec or {}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _record(self, body):
            try:
                req = json.loads(body or b"{}")
            except ValueError:
                req = {"_unparsed": body[:200].decode("utf-8", "replace")}
            qs = req.get("questions") or {}
            marker = os.environ.get("FI_MARKER")
            rec = {"ts": time.time(), "method": self.command, "path": self.path, "mode": mode,
                   "model": req.get("model"), "bytes": len(body or b""),
                   "has_marker": (marker.encode() in (body or b"")) if marker else None,
                   "questions": {k: str((v or {}).get("type")) for k, v in qs.items()}
                   if isinstance(qs, dict) else str(type(qs))}
            with open(log_path, "a") as f:
                f.write(json.dumps(rec) + "\n")
            return req

        def _send(self, status, body, ctype="application/json", extra=None):
            data = body if isinstance(body, bytes) else json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self._record(b"")
            self._send(200, {"data": [{"id": "jev-1.13.0"}, {"id": "claude-haiku-4-5"}]})

        def _empty_body(self):
            if self.path.endswith("/v1/messages"):
                return {"id": "fi", "type": "message", "role": "assistant", "content": []}
            if self.path.endswith("/v1/actions/authorize"):
                return {}
            return {"model": "jev-1.13.0", "answers": {}}

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            req = self._record(self.rfile.read(n) if n else b"")
            if mode in ("yes", "no"):
                if self.path.endswith("/v1/messages"):
                    text = spec.get("_anthropic_text", "[]")
                    self._send(200, {"id": "fi", "type": "message", "role": "assistant",
                                     "model": req.get("model") or "fi",
                                     "content": [{"type": "text", "text": text}],
                                     "stop_reason": "end_turn",
                                     "usage": {"input_tokens": 1, "output_tokens": 1}})
                    return
                if self.path.endswith("/v1/actions/authorize"):
                    self._send(200, spec.get("_authorize", {"decision": "allow"}))
                    return
                if self.path.endswith("/chat/completions"):
                    self._send(200, chat_completion(json.dumps(spec.get("_chat", {}))))
                    return
                qs = req.get("questions") or {}
                answers = ({k: answer_from_spec(k, v or {}, spec, mode) for k, v in qs.items()}
                           if isinstance(qs, dict) else {})
                self._send(200, {"model": req.get("model") or "jev-1.13.0", "answers": answers,
                                 "usage": {"input_tokens": 1, "output_tokens": 1}})
            elif mode == "http_429":
                self._send(429, {"error": {"type": "rate_limit", "message": "rate limited"}},
                           extra={"Retry-After": "1"})
            elif mode == "http_400_max_tokens":
                # Verbatim live response to an oversized state (jev-1.13.0, 2026-09-28):
                # attacker-sized tool input alone triggers it.
                self._send(400, {"detail": {"error_type": "max_tokens_exceeded"}})
            elif mode == "http_500":
                self._send(500, {"error": {"type": "internal", "message": "internal error"}})
            elif mode == "http_503":
                self._send(503, {"error": {"type": "unavailable", "message": "overloaded"}})
            elif mode == "timeout":
                time.sleep(hang_s)
            elif mode == "malformed":
                self._send(200, b"<html><body>502 Bad Gateway</body></html>")
            elif mode == "schema_drift":
                self._send(200, self._empty_body())
            else:
                self._send(500, {"error": f"unknown mode {mode}"})

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", required=True, choices=MODES)
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--hang", type=float, default=600.0)
    ap.add_argument("--spec", default=None, help="JSON file of per-question control answers")
    args = ap.parse_args()
    spec = json.load(open(args.spec)) if args.spec else None
    server = ThreadingHTTPServer(("127.0.0.1", args.port),
                                 make_handler(args.mode, args.log, args.hang, spec))
    server.daemon_threads = True
    print("ready", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
