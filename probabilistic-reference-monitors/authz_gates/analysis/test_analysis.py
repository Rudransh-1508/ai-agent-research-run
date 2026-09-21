#!/usr/bin/env python3
"""Tests for the analysis scripts (fixture data, small bootstrap resamples)."""

import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fail_open
import threshold_analysis as ta


class TestChowRule(unittest.TestCase):
    def test_thresholds(self):
        t_allow, t_deny = ta.chow_thresholds(L=10, c=0.2)
        self.assertAlmostEqual(t_allow, 0.02)
        self.assertAlmostEqual(t_deny, 0.8)
        self.assertAlmostEqual(ta.chow_allow_threshold_on_p_safe(10, 0.2), 0.98)

    def test_decisions(self):
        self.assertEqual(ta.chow_decision(0.001, 10, 0.2), "allow")
        self.assertEqual(ta.chow_decision(0.9, 10, 0.2), "deny")
        self.assertEqual(ta.chow_decision(0.5, 10, 0.2), "ask")

    def test_action_loss(self):
        self.assertEqual(ta.action_loss("allow", "destructive", 25, 0.2), 25.0)
        self.assertEqual(ta.action_loss("deny", "destructive", 25, 0.2), 0.0)
        self.assertEqual(ta.action_loss("deny", "safe", 25, 0.2), 1.0)
        self.assertEqual(ta.action_loss("ask", "safe", 25, 0.2), 0.2)
        with self.assertRaises(ValueError):
            ta.action_loss("allow", "ambiguous", 25, 0.2)

    def test_vendor_rule(self):
        self.assertEqual(ta.vendor_decision(0.95), "allow")
        self.assertEqual(ta.vendor_decision(0.89), "deny")


class TestStats(unittest.TestCase):
    def test_bootstrap_detects_clear_difference(self):
        a = [1.0] * 50
        b = [0.0] * 50
        point, lo, hi, p = ta.bootstrap_diff_ci(a, b, n_resamples=200, seed=1)
        self.assertEqual(point, 1.0)
        self.assertGreater(lo, 0)
        self.assertLess(p, 0.05)

    def test_bootstrap_no_difference(self):
        a = [0.0, 1.0] * 25
        b = [1.0, 0.0] * 25
        point, lo, hi, p = ta.bootstrap_diff_ci(a, b, n_resamples=200, seed=1)
        self.assertEqual(point, 0.0)

    def test_holm(self):
        adj = ta.holm_adjust([0.01, 0.04, 0.5])
        self.assertAlmostEqual(adj[0], 0.03)   # 0.01 * 3
        self.assertAlmostEqual(adj[1], 0.08)   # 0.04 * 2
        self.assertAlmostEqual(adj[2], 0.5)    # 0.5 * 1
        self.assertTrue(all(a >= p for a, p in zip(adj, [0.01, 0.04, 0.5])))


def fixture_result_rows():
    """50 safe (high p_safe) + 50 destructive (low p_safe) + 20 ambiguous (mid)."""
    rows = []
    for i in range(50):
        rows.append({"item_id": f"s{i}", "tier": "clearly_safe", "label": "safe",
                     "correct_action": "allow", "outcome": "ok", "disputable": False,
                     "p_safe": 0.95, "p_destructive": 0.05, "decision": "allow"})
    for i in range(50):
        rows.append({"item_id": f"d{i}", "tier": "clearly_destructive",
                     "label": "destructive", "correct_action": "deny",
                     "outcome": "ok", "disputable": False,
                     "p_safe": 0.85, "p_destructive": 0.15, "decision": "allow"})
    for i in range(20):
        rows.append({"item_id": f"a{i}", "tier": "ambiguous", "label": "ambiguous",
                     "correct_action": "ask", "outcome": "ok", "disputable": False,
                     "p_safe": 0.5, "p_destructive": 0.5, "decision": "ask"})
    # one failed call: must be excluded by load_results
    rows.append({"item_id": "x", "tier": "clearly_safe", "label": "safe",
                 "correct_action": "allow", "outcome": "http_429",
                 "disputable": False, "p_safe": None, "p_destructive": None})
    return rows


class TestThresholdAnalysis(unittest.TestCase):
    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "results.jsonl")
            with open(path, "w") as f:
                for r in fixture_result_rows():
                    f.write(json.dumps(r) + "\n")
            rows = ta.load_results(path)
            self.assertEqual(len(rows), 120)  # failed call excluded
            result = ta.analyze(rows, n_resamples=200, seed=1)
            self.assertEqual(result["n_definite_items"], 100)
            self.assertEqual(result["n_ambiguous_items"], 20)
            self.assertEqual(len(result["cells"]), 12)
            for cell in result["cells"]:
                self.assertIn("p_holm", cell)
                self.assertIn("ci95", cell)
            # vendor 0.9 allows the destructive items (p_safe=0.85 < 0.9? no:
            # 0.85 < 0.9 -> vendor DENIES them, so vendor is fine here; Chow with
            # small c/L allows p_destructive=0.15? 0.15 > c/L for all cells, and
            # 0.15 < 1-c, so Chow says ASK. Vendor loss 0, Chow loss c -> diff < 0.
            L10 = [c for c in result["cells"] if c["L"] == 10 and c["c"] == 0.2][0]
            self.assertLess(L10["loss_diff_vendor_minus_chow"], 0)
            self.assertIn("supported", result["P6"])

    def test_vendor_worse_when_destructive_looks_safe(self):
        rows = fixture_result_rows()
        for r in rows:
            if r["label"] == "destructive":
                r["p_safe"], r["p_destructive"] = 0.95, 0.05  # vendor allows -> cost L
        result = ta.analyze([r for r in rows if r["outcome"] == "ok"],
                            n_resamples=200, seed=1)
        cell = [c for c in result["cells"] if c["L"] == 100 and c["c"] == 0.5][0]
        self.assertGreater(cell["mean_loss_vendor"], cell["mean_loss_chow"])
        self.assertTrue(cell["vendor_significantly_worse"])


FIXTURE_GATES = [
    {"repo": "acme/gate-a", "sha": "abc", "in_pilot_set": True,
     "primitives": ["Noul"], "thresholds": [{"value": 0.9, "provenance": "copied-from-vendor-docs"}],
     "error_paths": {"timeout": "fail-open", "429": "fail-closed",
                     "5xx": "undocumented", "malformed": "fail-open"},
     "cites_cross_evaluation": False},
    {"repo": "acme/gate-b", "sha": "def", "in_pilot_set": False,
     "primitives": ["Choice"], "thresholds": [{"value": 0.7, "provenance": "swept-on-data"}],
     "error_paths": {"timeout": "fail-closed", "http_429": "fail-closed",
                     "http_5xx": "fail-closed", "malformed_response": "fail-closed"},
     "cites_cross_evaluation": False},
    {"repo": "acme/gate-c", "sha": "012", "in_pilot_set": False,
     "primitives": ["Score"], "thresholds": [{"value": 0.5}],
     "error_paths": {"timeout": "fail-open"},
     "cites_cross_evaluation": True},
]


class TestFailOpen(unittest.TestCase):
    def test_normalize_aliases_and_defaults(self):
        g = fail_open.normalize_gate(FIXTURE_GATES[0], 0)
        self.assertEqual(g["error_paths_norm"]["http_429"], "fail-closed")
        self.assertEqual(g["error_paths_norm"]["http_5xx"], "undocumented")
        self.assertEqual(g["error_paths_norm"]["malformed_response"], "fail-open")
        g3 = fail_open.normalize_gate(FIXTURE_GATES[2], 2)
        self.assertEqual(g3["thresholds_norm"][0]["provenance"], "undocumented")

    def test_predictions(self):
        gates = [fail_open.normalize_gate(g, i) for i, g in enumerate(FIXTURE_GATES)]
        res = fail_open.compute_predictions(gates)
        # P1: gates a,b,c all determinable; a and c fail open on >=1 mode
        self.assertEqual(res["P1"]["n_determinable"], 3)
        self.assertEqual(res["P1"]["n_fail_open"], 2)
        self.assertTrue(res["P1"]["supported"])
        # P2: 3 thresholds; 0.9 copied-from-vendor-docs + 0.5 undocumented = 2/3
        self.assertAlmostEqual(res["P2"]["fraction"], round(2 / 3, 4))
        self.assertTrue(res["P2"]["supported"])
        # P3: gate-a ships 0.9, gate-c ships 0.5
        self.assertEqual(res["P3"]["gates"], ["acme/gate-a", "acme/gate-c"])
        self.assertTrue(res["P3"]["supported"])
        # P4: gate-c cites a cross-evaluation -> P4 falsified
        self.assertFalse(res["P4"]["supported"])

    def test_held_out_remainder_split(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "gates.json")
            with open(path, "w") as f:
                json.dump({"gates": FIXTURE_GATES}, f)
            out = os.path.join(d, "fail_open")
            sys.argv = ["fail_open.py", "--gates", path, "--out-prefix", out]
            fail_open.main()
            report = json.load(open(out + ".json"))
            self.assertEqual(report["full_corpus"]["n_gates"], 3)
            self.assertEqual(report["held_out_remainder"]["n_gates"], 2)
            self.assertTrue(os.path.exists(out + ".md"))


if __name__ == "__main__":
    unittest.main()
