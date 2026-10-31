#!/usr/bin/env python3
"""Pinned Jev API client for the Probabilistic Reference Monitors study.

API (verified against the LIVE endpoint, 2026-09-21):
  POST {base_url}/v1/systemone
  Body: {"model": ..., "state": <str>, "questions": {name: typed-question, ...}}
  Typed question primitives (request format: type/instructions/criteria):
    choice  — one of N options, N <= 255
    score   — L ordered levels, 2 <= L <= 10; levels are 0-INDEXED
    noul    — probability a yes/no claim is true
  Response (verified live): {"model": ..., "usage": {"input_tokens", ...},
    "answers": {name: per-type answer}} where
    choice: {"type","choice","probabilities","confidence"}
    score:  {"type","score","legend","probabilities","confidence"} (0-indexed keys)
    noul:   {"type","noul"}  — NO probabilities, NO confidence (the client
            synthesizes probabilities and derives confidence; see parser)
  There is NO top-level "confidence" field.

The model id is PINNED to jev-1.13.0 for all measurements. The aliases
jev-latest / jev-preview exist and are refused here: measurements taken under an
alias are not reproducible and must never enter the paper.

Every HTTP attempt (including retries and failures) is logged as one JSONL
record to artifact/. 429 / 5xx / timeout / malformed-response are first-class
RECORDED OUTCOMES (the fail-open analysis needs them), not just exceptions:
a call that ultimately fails returns a GateResponse with outcome != "ok" and
the full attempt history, and every attempt is in the log.

Gateways (base_url + env key):
  typesafe    https://api.typesafe.ai            TYPESAFE_API_KEY        (default)
  openrouter  https://openrouter.ai/api/v1       OPENROUTER_API_KEY
  vercel      https://ai-gateway.vercel.sh/v1    VERCEL_AI_GATEWAY_KEY
  cloudflare  (account-specific; set base_url)   CLOUDFLARE_AI_GATEWAY_KEY

No API key is required for development: MockJevProvider scripts responses
(including failure modes) so all downstream code runs offline.

Stdlib only.
"""

from __future__ import annotations

import json
import os
import random
import socket
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

PINNED_MODEL = "jev-1.13.0"
FORBIDDEN_ALIASES = ("jev-latest", "jev-preview")

API_PATH = "/v1/systemone"

GATEWAYS = {
    "typesafe": {
        "base_url": "https://api.typesafe.ai",
        "key_env": "TYPESAFE_API_KEY",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
    },
    "vercel": {
        "base_url": "https://ai-gateway.vercel.sh/v1",
        "key_env": "VERCEL_AI_GATEWAY_KEY",
    },
    "cloudflare": {
        # Cloudflare AI Gateway URLs are account/gateway specific:
        # https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/...
        # Pass --base-url or set CLOUDFLARE_AI_GATEWAY_BASE_URL.
        "base_url": None,
        "key_env": "CLOUDFLARE_AI_GATEWAY_KEY",
    },
}

# Outcome classes. Everything except "ok" is a recorded failure outcome.
OUTCOME_OK = "ok"
OUTCOME_HTTP_429 = "http_429"
OUTCOME_HTTP_5XX = "http_5xx"
OUTCOME_HTTP_4XX = "http_4xx"          # non-retryable client error
OUTCOME_TIMEOUT = "timeout"
OUTCOME_NETWORK = "network_error"
OUTCOME_MALFORMED = "malformed_response"

RETRYABLE = {OUTCOME_HTTP_429, OUTCOME_HTTP_5XX, OUTCOME_TIMEOUT, OUTCOME_NETWORK}

# Probability distributions are accepted if they sum to 1 within this tolerance
# (gateways sometimes round to 3 decimals).
PROB_SUM_TOL = 0.02


# --------------------------------------------------------------------------
# Typed question builders (with vendor constraint validation)
# --------------------------------------------------------------------------
def choice(options, instructions=None):
    """Choice primitive: one of N options, N <= 255.

    Emits the verified live request format (type/instructions/criteria), as
    accepted by POST /v1/systemone on 2026-09-21.
    """
    options = [str(o) for o in options]
    if not 1 <= len(options) <= 255:
        raise ValueError(f"Choice needs 1..255 options, got {len(options)}")
    return {"type": "choice",
            "instructions": instructions or "Choose exactly one option.",
            "criteria": {o: o for o in options}}


def score(levels, instructions=None, labels=None):
    """Score primitive: L ordered levels, 2 <= L <= 10.

    Levels are 0-indexed (the live response legend/probabilities keys are
    "0".."L-1"). `labels` optionally names each level, lowest first.
    """
    levels = int(levels)
    if not 2 <= levels <= 10:
        raise ValueError(f"Score needs 2..10 levels, got {levels}")
    criteria = list(labels) if labels is not None else [f"Level {i}" for i in range(levels)]
    if len(criteria) != levels:
        raise ValueError(f"Score labels must match levels ({levels}), got {len(criteria)}")
    return {"type": "score",
            "instructions": instructions or "Rate on the given scale.",
            "criteria": criteria}


def noul(claim, criteria=None):
    """Noul primitive: probability that a yes/no claim is true."""
    if not isinstance(claim, str) or not claim.strip():
        raise ValueError("Noul needs a non-empty claim string")
    return {"type": "noul",
            "instructions": claim,
            "criteria": criteria or {"true": "The claim is true",
                                     "false": "The claim is false"}}


# --------------------------------------------------------------------------
# Provider layer
# --------------------------------------------------------------------------
@dataclass
class ProviderResponse:
    """One raw HTTP attempt result, before any parsing."""
    status: int | None = None        # HTTP status, None if no response arrived
    body_text: str | None = None     # raw response text
    error: str | None = None         # "timeout" / "network_error" / ...


class HttpProvider:
    """Real HTTP transport (urllib, stdlib only)."""

    def __init__(self, endpoint, api_key, timeout_s=60.0):
        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout_s = timeout_s

    def post(self, payload, request_id=None):
        req = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as r:
                return ProviderResponse(status=r.status, body_text=r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                body = None
            return ProviderResponse(status=e.code, body_text=body)
        except (socket.timeout, TimeoutError):
            return ProviderResponse(error=OUTCOME_TIMEOUT)
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", e)
            if isinstance(reason, (socket.timeout, TimeoutError)):
                return ProviderResponse(error=OUTCOME_TIMEOUT)
            return ProviderResponse(error=OUTCOME_NETWORK)
        except OSError:
            return ProviderResponse(error=OUTCOME_NETWORK)


class MockJevProvider:
    """Scripted offline provider. NOT a model: produces no behavioral evidence.

    Two ways to script it:
      - `script`: a list of response specs consumed in order (repeats the last
        spec when exhausted), or
      - `responder`: callable(payload_dict) -> response spec, for content-
        dependent behavior (e.g. the benchmark's heuristic mock gate).

    Response spec forms:
      {"status": 200, "body": {...}}     normal JSON response
      {"status": 200, "raw": "not-json{"} malformed JSON body
      {"status": 429} / {"status": 503, "body": {...}}
      {"error": "timeout"} / {"error": "network_error"}
    """

    def __init__(self, script=None, responder=None, latency_s=0.0):
        if script is None and responder is None:
            raise ValueError("MockJevProvider needs a script or a responder")
        self.script = list(script) if script is not None else None
        self.responder = responder
        self.latency_s = latency_s
        self.calls = []  # every payload received, for test assertions

    def post(self, payload, request_id=None):
        self.calls.append(payload)
        if self.latency_s:
            time.sleep(self.latency_s)
        spec = (self.responder(payload, request_id=request_id)
                if self.responder else self._next_spec())
        if spec.get("error"):
            return ProviderResponse(error=spec["error"])
        status = int(spec.get("status", 200))
        if "raw" in spec:
            return ProviderResponse(status=status, body_text=spec["raw"])
        return ProviderResponse(status=status, body_text=json.dumps(spec.get("body", {})))

    def _next_spec(self):
        i = min(len(self.calls) - 1, len(self.script) - 1)
        return self.script[i]


def mock_noul(p):
    """Real-schema noul answer: NO probabilities map, NO confidence."""
    return {"type": "noul", "noul": p}


def mock_choice(value, probabilities, confidence):
    """Real-schema choice answer."""
    return {"type": "choice", "choice": value,
            "probabilities": probabilities, "confidence": confidence}


def mock_score(value, probabilities, confidence, labels=None):
    """Real-schema score answer; probabilities/legend keys are 0-indexed strings."""
    entry = {"type": "score", "score": value,
             "probabilities": probabilities, "confidence": confidence}
    if labels is not None:
        entry["legend"] = {str(i): lab for i, lab in enumerate(labels)}
    return entry


def mock_ok_body(answers, model=PINNED_MODEL, usage=None):
    """Build a well-formed mock response body in the verified live schema.

    answers: {question_name: <real-schema answer dict>} — use mock_noul /
    mock_choice / mock_score. There is NO top-level confidence field in the
    live schema; usage {input_tokens, output_tokens} IS present.
    """
    return {"model": model, "answers": dict(answers),
            "usage": usage or {"input_tokens": 0, "output_tokens": 0}}


# --------------------------------------------------------------------------
# Response parsing / validation
# --------------------------------------------------------------------------
class MalformedResponse(Exception):
    pass


def _question_type(name, q, a):
    """Dispatch on the REQUEST question's type; fall back to the answer's."""
    raw = q.get("type") or q.get("primitive") or a.get("type")
    if raw is None:
        raise MalformedResponse(f"cannot determine primitive type for question {name!r}")
    t = str(raw).lower()
    if t not in ("choice", "score", "noul"):
        raise MalformedResponse(f"unknown primitive type {raw!r} for question {name!r}")
    return t


def _parse_probabilities(name, a):
    probs = a.get("probabilities")
    if not isinstance(probs, dict) or not probs:
        raise MalformedResponse(f"answer for {name!r} lacks a probabilities distribution")
    try:
        probs = {str(k): float(v) for k, v in probs.items()}
    except (TypeError, ValueError) as e:
        raise MalformedResponse(f"probabilities for {name!r} are not numeric: {e}") from e
    total = sum(probs.values())
    if abs(total - 1.0) > PROB_SUM_TOL:
        raise MalformedResponse(
            f"probabilities for {name!r} sum to {total:.4f}, not 1")
    return probs


def _parse_vendor_confidence(name, a):
    if "confidence" not in a:
        raise MalformedResponse(f"answer for {name!r} lacks vendor confidence")
    try:
        conf = float(a["confidence"])
    except (TypeError, ValueError) as e:
        raise MalformedResponse(f"confidence for {name!r} is not numeric") from e
    if not 0.0 <= conf <= 1.0:
        raise MalformedResponse(f"confidence for {name!r} out of range: {conf}")
    return conf


def _parse_noul(name, a):
    # Live schema: {"type": "noul", "noul": p} — NO probabilities, NO confidence.
    if "noul" not in a:
        raise MalformedResponse(f"noul answer for {name!r} lacks a 'noul' value")
    try:
        p = float(a["noul"])
    except (TypeError, ValueError) as e:
        raise MalformedResponse(f"noul value for {name!r} is not numeric") from e
    if not 0.0 <= p <= 1.0:
        raise MalformedResponse(f"noul value for {name!r} out of range: {p}")
    # Vendor returns no confidence for noul; derive the binary case of the
    # vendor's documented formula (k*p_max - 1)/(k - 1) with k = 2.
    conf = 2.0 * max(p, 1.0 - p) - 1.0
    return {"answer": "true" if p >= 0.5 else "false",
            "probabilities": {"true": p, "false": 1.0 - p},
            "confidence": conf, "confidence_derived": True}


def _parse_choice(name, a):
    # Live schema: {"type", "choice", "probabilities", "confidence"}.
    ch = a.get("choice")
    if not isinstance(ch, str) or not ch:
        raise MalformedResponse(f"choice answer for {name!r} lacks a 'choice' field")
    probs = _parse_probabilities(name, a)
    if ch not in probs:
        raise MalformedResponse(
            f"choice {ch!r} for {name!r} is not a key of its probabilities")
    return {"answer": ch, "probabilities": probs,
            "confidence": _parse_vendor_confidence(name, a),
            "confidence_derived": False}


def _parse_score(name, a):
    # Live schema: {"type", "score", "legend", "probabilities", "confidence"};
    # legend/probabilities keys are 0-indexed level strings ("0".."L-1").
    if "score" not in a:
        raise MalformedResponse(f"score answer for {name!r} lacks a 'score' value")
    try:
        sc = float(a["score"])
    except (TypeError, ValueError) as e:
        raise MalformedResponse(f"score value for {name!r} is not numeric") from e
    probs = _parse_probabilities(name, a)
    out = {"answer": max(probs, key=lambda k: probs[k]),  # argmax level key, as returned
           "probabilities": probs,
           "confidence": _parse_vendor_confidence(name, a),
           "confidence_derived": False,
           "score": sc}
    if "legend" in a:
        out["legend"] = a["legend"]
    return out


_PARSERS = {"noul": _parse_noul, "choice": _parse_choice, "score": _parse_score}


def parse_response_body(body_text, requested_questions):
    """Validate and normalize a /v1/systemone response body (verified live
    schema, 2026-09-21).

    Per-question parsing dispatches on the REQUEST question's type (fallback:
    the answer's "type" field). Every parsed answer exposes the downstream
    contract {"answer": str, "probabilities": dict, "confidence": float} plus
    "confidence_derived" (True only for noul, where the vendor returns no
    confidence); score answers also pass through "score" and "legend".

    Raises MalformedResponse on any structural problem; the client records that
    as a first-class outcome rather than crashing.
    """
    try:
        data = json.loads(body_text)
    except (json.JSONDecodeError, TypeError) as e:
        raise MalformedResponse(f"body is not valid JSON: {e}") from e
    if not isinstance(data, dict):
        raise MalformedResponse("body is not a JSON object")

    answers = data.get("answers")
    if not isinstance(answers, dict):
        raise MalformedResponse("missing 'answers' object")

    parsed = {}
    for name, q in requested_questions.items():
        if name not in answers:
            raise MalformedResponse(f"no answer for question {name!r}")
        a = answers[name]
        if not isinstance(a, dict):
            raise MalformedResponse(f"answer for {name!r} is not an object")
        parsed[name] = _PARSERS[_question_type(name, q, a)](name, a)

    # The live schema has no top-level confidence; aggregate per-question values.
    top_conf = (sum(p["confidence"] for p in parsed.values()) / len(parsed)) if parsed else None

    return {"model": data.get("model"), "answers": parsed, "confidence": top_conf,
            "usage": data.get("usage"), "raw": data}


# --------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------
@dataclass
class GateResponse:
    """Aggregate result of one logical gate query (after any retries)."""
    request_id: str
    outcome: str                       # OUTCOME_* constant
    answers: dict = field(default_factory=dict)
    confidence: float | None = None
    model_requested: str = PINNED_MODEL
    model_echoed: str | None = None
    model_mismatch: bool = False
    attempts: int = 0
    latency_ms_total: float = 0.0
    error: str | None = None
    raw_response: dict | None = None

    @property
    def ok(self):
        return self.outcome == OUTCOME_OK


class JevClient:
    def __init__(self, gateway="typesafe", model=PINNED_MODEL, api_key=None,
                 base_url=None, log_path=None, provider=None,
                 max_attempts=4, base_delay_s=1.0, max_delay_s=30.0,
                 retry_malformed=1, timeout_s=60.0, rng=None):
        if model in FORBIDDEN_ALIASES:
            raise ValueError(
                f"model alias {model!r} is forbidden for measurements; "
                f"pin {PINNED_MODEL!r}")
        if gateway not in GATEWAYS:
            raise ValueError(f"unknown gateway {gateway!r}; choose from {sorted(GATEWAYS)}")
        self.gateway = gateway
        self.model = model
        self.max_attempts = max(1, int(max_attempts))
        self.base_delay_s = base_delay_s
        self.max_delay_s = max_delay_s
        self.retry_malformed = retry_malformed
        self.rng = rng or random.Random()

        gw = GATEWAYS[gateway]
        if base_url:
            self.base_url = base_url
        elif gateway == "cloudflare":
            self.base_url = os.environ.get("CLOUDFLARE_AI_GATEWAY_BASE_URL")
        else:
            self.base_url = gw["base_url"]
        if provider is None and not self.base_url:
            raise ValueError("cloudflare gateway needs --base-url or "
                             "CLOUDFLARE_AI_GATEWAY_BASE_URL")
        self.endpoint = self._endpoint(self.base_url) if self.base_url else None

        if provider is not None:
            self.provider = provider
            self.provider_kind = "mock"
        else:
            key = api_key or os.environ.get(gw["key_env"], "")
            if not key:
                raise ValueError(
                    f"no API key: set {gw['key_env']} (or pass api_key= / use mock mode)")
            self.provider = HttpProvider(self.endpoint, key, timeout_s=timeout_s)
            self.provider_kind = "http"

        self.log_path = log_path
        self._log_fp = open(log_path, "a") if log_path else None

    @staticmethod
    def _endpoint(base_url):
        base = base_url.rstrip("/")
        return base + ("/systemone" if base.endswith("/v1") else API_PATH)

    def close(self):
        if self._log_fp:
            self._log_fp.close()
            self._log_fp = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # -- logging -----------------------------------------------------------
    def _log(self, record):
        if self._log_fp:
            self._log_fp.write(json.dumps(record, sort_keys=True) + "\n")
            self._log_fp.flush()

    # -- main entry point ---------------------------------------------------
    def query(self, state, questions, request_id=None, meta=None):
        """Send state + typed questions; return a GateResponse.

        Never raises for API/transport problems: every failure mode is returned
        as a recorded outcome (and logged per attempt).
        """
        request_id = request_id or uuid.uuid4().hex[:12]
        payload = {"model": self.model, "state": state, "questions": questions}
        resp = GateResponse(request_id=request_id, outcome=OUTCOME_OK,
                            model_requested=self.model)
        malformed_retries_left = self.retry_malformed

        for attempt in range(self.max_attempts):
            t0 = time.monotonic()
            pr = self.provider.post(payload, request_id=request_id)
            latency_ms = (time.monotonic() - t0) * 1000.0
            resp.attempts += 1
            resp.latency_ms_total += latency_ms

            record = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "request_id": request_id,
                "attempt": attempt,
                "gateway": self.gateway,
                "provider": self.provider_kind,
                "endpoint": self.endpoint,
                "model_requested": self.model,
                "model_echoed": None,
                "latency_ms": round(latency_ms, 2),
                "http_status": pr.status,
                "request": payload,
                "meta": meta or {},
            }

            if pr.error:
                outcome = pr.error
                record.update(outcome=outcome, error=pr.error, response_body=None,
                              final=False)
            elif pr.status == 429:
                outcome = OUTCOME_HTTP_429
                record.update(outcome=outcome, error=None,
                              response_body=_safe_json(pr.body_text), final=False)
            elif pr.status is not None and 500 <= pr.status < 600:
                outcome = OUTCOME_HTTP_5XX
                record.update(outcome=outcome, error=None,
                              response_body=_safe_json(pr.body_text), final=False)
            elif pr.status is not None and pr.status != 200:
                outcome = OUTCOME_HTTP_4XX
                record.update(outcome=outcome, error=None,
                              response_body=_safe_json(pr.body_text), final=False)
            else:
                try:
                    parsed = parse_response_body(pr.body_text, questions)
                except MalformedResponse as e:
                    outcome = OUTCOME_MALFORMED
                    record.update(outcome=outcome, error=str(e),
                                  response_body=_safe_json(pr.body_text), final=False)
                else:
                    outcome = OUTCOME_OK
                    resp.outcome = OUTCOME_OK
                    resp.answers = parsed["answers"]
                    resp.confidence = parsed["confidence"]
                    resp.model_echoed = parsed["model"]
                    resp.model_mismatch = bool(parsed["model"]) and parsed["model"] != self.model
                    resp.raw_response = parsed["raw"]
                    record.update(outcome=outcome, error=None,
                                  model_echoed=parsed["model"],
                                  model_mismatch=resp.model_mismatch,
                                  usage=parsed.get("usage"),
                                  response_body=parsed["raw"], final=True)
                    self._log(record)
                    return resp

            # failure path: decide whether to retry
            will_retry = False
            if attempt + 1 < self.max_attempts:
                if outcome in RETRYABLE:
                    will_retry = True
                elif outcome == OUTCOME_MALFORMED and malformed_retries_left > 0:
                    malformed_retries_left -= 1
                    will_retry = True
            record["final"] = not will_retry
            self._log(record)
            if not will_retry:
                resp.outcome = outcome
                resp.error = record.get("error")
                return resp
            self._sleep_before_retry(attempt)

        # attempts exhausted without a conclusive attempt
        resp.outcome = outcome
        resp.error = record.get("error")
        return resp

    def _sleep_before_retry(self, attempt):
        # exponential backoff with full jitter
        cap = min(self.max_delay_s, self.base_delay_s * (2 ** attempt))
        delay = self.rng.uniform(0, cap)
        if delay > 0:
            time.sleep(delay)


def _safe_json(text):
    if text is None:
        return None
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {"_raw": text[:4000]}


# --------------------------------------------------------------------------
# CLI smoke check (mock mode only; never touches the network without a key)
# --------------------------------------------------------------------------
def main():
    import argparse

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--gateway", default="typesafe", choices=sorted(GATEWAYS))
    p.add_argument("--base-url", default=None)
    p.add_argument("--model", default=PINNED_MODEL)
    p.add_argument("--log", default=None, help="JSONL call log path (artifact/)")
    p.add_argument("--mock", action="store_true",
                   help="use a built-in scripted mock provider (no API key needed)")
    p.add_argument("--state", default="Agent proposes: run_shell(command='ls -la /tmp')")
    args = p.parse_args()

    questions = {"gate": choice(["allow", "ask", "deny"])}
    if args.mock:
        provider = MockJevProvider(script=[{
            "status": 200,
            "body": mock_ok_body({"gate": mock_choice(
                "allow", {"allow": 0.9, "ask": 0.08, "deny": 0.02}, 0.9)}),
        }])
        client = JevClient(gateway=args.gateway, model=args.model,
                           log_path=args.log, provider=provider)
    else:
        client = JevClient(gateway=args.gateway, model=args.model,
                           base_url=args.base_url, log_path=args.log)
    with client:
        r = client.query(args.state, questions)
    print(json.dumps({"outcome": r.outcome, "answers": r.answers,
                      "confidence": r.confidence, "model_echoed": r.model_echoed,
                      "attempts": r.attempts}, indent=2))


if __name__ == "__main__":
    main()
