#!/usr/bin/env python3
"""Tests for the pinned Jev client (all offline, via MockJevProvider)."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import jev_client
from jev_client import (JevClient, MockJevProvider, choice, mock_choice,
                        mock_noul, mock_ok_body, mock_score, noul, score,
                        PINNED_MODEL)

QUESTIONS = {"gate": choice(["allow", "ask", "deny"])}
OK_BODY = mock_ok_body({"gate": mock_choice(
    "allow", {"allow": 0.9, "ask": 0.08, "deny": 0.02}, 0.9)})


def make_client(script=None, responder=None, log_path=None, **kw):
    kw.setdefault("base_delay_s", 0)
    provider = MockJevProvider(script=script, responder=responder)
    return JevClient(log_path=log_path, provider=provider, **kw)


class TestPrimitives(unittest.TestCase):
    def test_choice_bounds(self):
        q = choice(["a"])
        self.assertEqual(q["type"], "choice")
        self.assertEqual(list(q["criteria"].keys()), ["a"])
        with self.assertRaises(ValueError):
            choice([])
        with self.assertRaises(ValueError):
            choice([str(i) for i in range(256)])

    def test_score_bounds(self):
        q = score(5)
        self.assertEqual(q["type"], "score")
        self.assertEqual(len(q["criteria"]), 5)
        with self.assertRaises(ValueError):
            score(1)
        with self.assertRaises(ValueError):
            score(11)
        with self.assertRaises(ValueError):
            score(5, labels=["a", "b"])

    def test_noul_requires_claim(self):
        q = noul("safe?")
        self.assertEqual(q["type"], "noul")
        self.assertEqual(q["instructions"], "safe?")
        with self.assertRaises(ValueError):
            noul("")

    def test_alias_rejected(self):
        for alias in ("jev-latest", "jev-preview"):
            with self.assertRaises(ValueError):
                JevClient(model=alias, provider=MockJevProvider(script=[]))


class TestQuery(unittest.TestCase):
    def test_ok_call_parses_and_logs(self):
        with tempfile.TemporaryDirectory() as d:
            log = os.path.join(d, "calls.jsonl")
            with make_client(script=[{"status": 200, "body": OK_BODY}],
                             log_path=log) as c:
                r = c.query("state text", QUESTIONS, request_id="t1")
            self.assertTrue(r.ok)
            self.assertEqual(r.answers["gate"]["answer"], "allow")
            self.assertAlmostEqual(r.answers["gate"]["probabilities"]["allow"], 0.9)
            self.assertEqual(r.model_echoed, PINNED_MODEL)
            self.assertFalse(r.model_mismatch)
            self.assertEqual(r.attempts, 1)
            records = [json.loads(l) for l in open(log)]
            self.assertEqual(len(records), 1)
            rec = records[0]
            for key in ("ts", "request_id", "attempt", "gateway", "provider",
                        "model_requested", "model_echoed", "latency_ms",
                        "http_status", "request", "response_body", "outcome", "final"):
                self.assertIn(key, rec)
            self.assertEqual(rec["outcome"], "ok")
            self.assertTrue(rec["final"])
            self.assertEqual(rec["request"]["state"], "state text")

    def test_429_then_success_retries_and_records(self):
        with tempfile.TemporaryDirectory() as d:
            log = os.path.join(d, "calls.jsonl")
            script = [{"status": 429}, {"status": 200, "body": OK_BODY}]
            with make_client(script=script, log_path=log) as c:
                r = c.query("s", QUESTIONS)
            self.assertTrue(r.ok)
            self.assertEqual(r.attempts, 2)
            outcomes = [json.loads(l)["outcome"] for l in open(log)]
            self.assertEqual(outcomes, ["http_429", "ok"])

    def test_persistent_5xx_is_recorded_outcome(self):
        with make_client(script=[{"status": 503, "body": {"error": "x"}}],
                         max_attempts=3) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "http_5xx")
        self.assertEqual(r.attempts, 3)
        self.assertFalse(r.ok)

    def test_timeout_is_recorded_outcome(self):
        with make_client(script=[{"error": "timeout"}], max_attempts=2) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "timeout")
        self.assertEqual(r.attempts, 2)

    def test_malformed_json_retried_once_then_recorded(self):
        with make_client(script=[{"status": 200, "raw": "not-json{"}], max_attempts=4) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "malformed_response")
        self.assertEqual(r.attempts, 2)  # 1 initial + retry_malformed=1

    def test_malformed_schema_probabilities_not_summing(self):
        bad = {"model": PINNED_MODEL,
               "answers": {"gate": {"type": "choice", "choice": "allow",
                                    "probabilities": {"allow": 0.5, "deny": 0.1},
                                    "confidence": 0.5}}}
        with make_client(script=[{"status": 200, "body": bad}], max_attempts=2) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "malformed_response")
        self.assertIn("sum", r.error)

    def test_missing_question_answer_is_malformed(self):
        bad = {"model": PINNED_MODEL, "answers": {}}
        with make_client(script=[{"status": 200, "body": bad}], max_attempts=1) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "malformed_response")

    def test_choice_missing_choice_field_is_malformed(self):
        bad = {"model": PINNED_MODEL,
               "answers": {"gate": {"type": "choice",
                                    "probabilities": {"allow": 0.9, "ask": 0.05, "deny": 0.05},
                                    "confidence": 0.9}}}
        with make_client(script=[{"status": 200, "body": bad}], max_attempts=1) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "malformed_response")
        self.assertIn("choice", r.error)

    def test_choice_value_not_in_probabilities_is_malformed(self):
        bad = {"model": PINNED_MODEL,
               "answers": {"gate": {"type": "choice", "choice": "yolo",
                                    "probabilities": {"allow": 0.9, "ask": 0.05, "deny": 0.05},
                                    "confidence": 0.9}}}
        with make_client(script=[{"status": 200, "body": bad}], max_attempts=1) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "malformed_response")

    def test_noul_parses_without_probabilities_and_derives_confidence(self):
        # live schema: noul answers are just {"type": "noul", "noul": p}
        body = mock_ok_body({"gate": mock_noul(0.95)})
        with make_client(script=[{"status": 200, "body": body}]) as c:
            r = c.query("s", {"gate": noul("Is this safe?")})
        self.assertTrue(r.ok)
        ans = r.answers["gate"]
        self.assertEqual(ans["answer"], "true")
        self.assertAlmostEqual(ans["probabilities"]["true"], 0.95)
        self.assertAlmostEqual(ans["probabilities"]["false"], 0.05)
        self.assertTrue(ans["confidence_derived"])
        self.assertAlmostEqual(ans["confidence"], 2 * 0.95 - 1)

    def test_noul_out_of_range_is_malformed(self):
        body = mock_ok_body({"gate": mock_noul(1.7)})
        with make_client(script=[{"status": 200, "body": body}], max_attempts=1) as c:
            r = c.query("s", {"gate": noul("Is this safe?")})
        self.assertEqual(r.outcome, "malformed_response")

    def test_score_legend_keys_stay_zero_indexed(self):
        probs = {"0": 0.0, "1": 0.0, "2": 0.04, "3": 0.96}
        body = mock_ok_body({"gate": mock_score(
            2.96, probs, 0.96,
            labels=["No risk", "Minor risk", "Moderate risk", "Severe risk"])})
        with make_client(script=[{"status": 200, "body": body}]) as c:
            r = c.query("s", {"gate": score(4)})
        self.assertTrue(r.ok)
        ans = r.answers["gate"]
        self.assertEqual(ans["answer"], "3")          # argmax key, 0-indexed string
        self.assertEqual(ans["legend"]["0"], "No risk")
        self.assertEqual(ans["legend"]["3"], "Severe risk")
        self.assertAlmostEqual(ans["score"], 2.96)
        self.assertFalse(ans["confidence_derived"])
        self.assertAlmostEqual(ans["confidence"], 0.96)

    def test_usage_logged(self):
        body = mock_ok_body({"gate": mock_choice(
            "allow", {"allow": 0.9, "ask": 0.08, "deny": 0.02}, 0.9)},
            usage={"input_tokens": 459, "output_tokens": 71})
        with tempfile.TemporaryDirectory() as d:
            log = os.path.join(d, "calls.jsonl")
            with make_client(script=[{"status": 200, "body": body}], log_path=log) as c:
                c.query("s", QUESTIONS)
            rec = json.loads(open(log).read().strip())
            self.assertEqual(rec["usage"], {"input_tokens": 459, "output_tokens": 71})

    def test_model_mismatch_flagged(self):
        body = mock_ok_body({"gate": mock_choice(
            "allow", {"allow": 0.9, "ask": 0.05, "deny": 0.05}, 0.9)},
            model="jev-1.12.0")
        with make_client(script=[{"status": 200, "body": body}]) as c:
            r = c.query("s", QUESTIONS)
        self.assertTrue(r.ok)
        self.assertTrue(r.model_mismatch)
        self.assertEqual(r.model_echoed, "jev-1.12.0")

    def test_non_retryable_4xx_not_retried(self):
        with make_client(script=[{"status": 400, "body": {"error": "bad request"}}],
                         max_attempts=4) as c:
            r = c.query("s", QUESTIONS)
        self.assertEqual(r.outcome, "http_4xx")
        self.assertEqual(r.attempts, 1)

    def test_responder_receives_request_id(self):
        seen = []
        def responder(payload, request_id=None):
            seen.append((payload["state"], request_id))
            return {"status": 200, "body": OK_BODY}
        with make_client(responder=responder) as c:
            c.query("hello", QUESTIONS, request_id="rid-1")
        self.assertEqual(seen, [("hello", "rid-1")])

    def test_no_key_raises_without_provider(self):
        for var in ("TYPESAFE_API_KEY",):
            os.environ.pop(var, None)
        with self.assertRaises(ValueError):
            JevClient(gateway="typesafe")


if __name__ == "__main__":
    unittest.main()
