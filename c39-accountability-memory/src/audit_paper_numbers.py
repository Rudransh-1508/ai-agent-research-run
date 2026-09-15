"""Audit: every number printed in the paper against the artifact that produced it.

verify_all.py checks that the mathematics is right. This script checks something
different and just as easy to get wrong -- that the numbers written into the
LaTeX are the numbers the experiments actually returned, and not values typed
from memory or left behind by an earlier run.

It reads the .tex sources directly, pulls out the claims, and compares each
against the JSON artifact it is supposed to come from. A claim with no artifact
behind it is reported as UNSOURCED rather than passed over.

    python audit_paper_numbers.py        # exit 0 iff every claim matches

Numbers that are derived rather than measured (compression ratios, bit counts,
the tilted threshold) are covered by verify_all.py blocks F and G and are not
repeated here.
"""
import io, json, re, sys
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

SEC = "paper/sections/"   # resolved via data()
FAILS, UNSOURCED = [], []


def claim(name, ok, detail=""):
    print(f"  [{'OK  ' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


def tex(fname):
    return io.open(data(SEC + fname), encoding="utf-8").read()


def present(fname, needle, label):
    """The paper must actually contain the string we are validating."""
    if needle in tex(fname):
        return True
    UNSOURCED.append(f"{label}: '{needle[:40]}...' not found in {fname}")
    print(f"  [MISS] {label} -- the paper no longer contains this text")
    return False


# ------------------------------------------------------------------ Table 1
print("Table 1 (one-bit frontier) against exp1b_results.json")
exp1b = json.load(open(data("exp1b_results.json")))
onebit = tex("04-onebit.tex")
# Parse the table out of the LaTeX rather than restating it here. A constant
# copied into this file would only check my transcription against itself.
ROW = re.compile(r"^\s*(\d+)\s*&\s*([0-9.]+)\s*&\s*\$\[0, 1/\d+\]\$\s*&\s*(.+?)\s*\\\\",
                 re.MULTILINE)
rows_printed = {int(m.group(1)): (m.group(2), m.group(3))
                for m in ROW.finditer(tex("04-onebit.tex"))}
claim("Table 1 has a parsed row for each of n = 3,5,7,9",
      set(rows_printed) == {3, 5, 7, 9}, f"parsed {sorted(rows_printed)}")


def dev_value(cell):
    """'$0$' -> 0.0;  '$4.4\\times10^{-16}$' -> 4.4e-16."""
    cell = cell.replace("$", "").strip()
    if cell in ("0", "0.0"):
        return 0.0
    m = re.match(r"([0-9.]+)\\times10\^\{(-?\d+)\}", cell)
    return None if not m else float(m.group(1)) * 10 ** int(m.group(2))


for n in (3, 5, 7, 9):
    if n not in rows_printed:
        continue
    mn_printed, dev_cell = rows_printed[n]
    row = exp1b[str(n)]
    mn = row["M_n"]
    claim(f"n={n}: M_n in Table 1 matches the artifact",
          f"{mn:.6f}" == mn_printed, f"paper {mn_printed}  artifact {mn:.6f}")
    dev_printed = dev_value(dev_cell)
    worst = max(abs(r["gap"]) for r in row["rows"])
    ok = dev_printed is not None and (
        (worst == 0.0 and dev_printed == 0.0)
        or (dev_printed > 0 and 0.5 <= worst / dev_printed <= 2.0))
    claim(f"n={n}: max deviation in Table 1 matches the artifact", ok,
          f"paper {dev_cell}  artifact {worst:.2e}")
    claim(f"n={n}: every LP landed on the conjectured record",
          all(r["q_matches_conjecture"] for r in row["rows"]))
claim("orientation spread at n=3 is 0 as stated",
      exp1b["orientation_spread_n3"] == 0.0, f"{exp1b['orientation_spread_n3']}")

# ------------------------------------------------------------------ Table 2
print("\nTable 2 (certificate chain) against shell_exclusion.json and the MILP logs")
shell = json.load(open(data("shell_exclusion.json")))
thr = tex("05-threshold.tex")
for n, kmax in [(3, 3), (5, 9), (7, 28), (9, 93)]:
    rows = shell[str(n)]["rows"]
    excluded = {int(k) for k, v in rows.items() if v["excluded_shell"]}
    survivors = [K for K in range(2, kmax + 1) if K not in excluded]
    claim(f"n={n}: shell bound excludes every K <= {kmax} (as Table 2 says)",
          not survivors, f"survivors {survivors}" if survivors else "")
    present("05-threshold.tex", f"$K \\le {kmax}$ (shell)", f"n={n} shell entry")

seq = json.load(open(data("gamma2_sequence.json")))
infeasible7 = {r["K"] for r in seq["n7"]["milp_rows"]
               if not r.get("feasible") and r["status"] == 2}
claim("n=7: K = 29,30,31 proved MILP-infeasible (status 2)",
      {29, 30, 31} <= infeasible7, f"artifact {sorted(infeasible7)}")
claim("n=7: K = 32 is the feasible witness",
      any(r["K"] == 32 and r.get("feasible") for r in seq["n7"]["milp_rows"]))

n9 = json.load(open(data("gamma2_n9_lb_rerun.json")))
proved9 = {int(k) for k, v in n9["rows"].items()
           if not v["feasible"] and v["status"] == 2}
claim("n=9: K = 94,95,96 proved infeasible in the PINNED environment",
      {94, 95, 96} <= proved9, f"artifact {sorted(proved9)}")
claim("n=9: the pinned re-run agrees with the pre-pin log",
      n9["all_agree_with_prepinned"] is True)

# ------------------------------------------------------ section 5 prose claims
print("\nSection 5 prose against the artifacts")
cert = json.load(open(data("certified_codes.json")))["codes"]
for key, n, K, margin, dmin in [("n7", 7, 32, 0.5, 2)]:
    c = cert[key]
    claim(f"n={n} K={K}: certified code has min_deg_outside = {dmin}",
          c["min_deg_outside"] == dmin, f"artifact {c['min_deg_outside']}")
dr = json.load(open(data("n9_destroy_repair.json")))
claim("n=9 destroy-and-repair ran 70,685 trials, as Section 5 states",
      dr["trials"] == 70685, f"artifact {dr['trials']}")
present("05-threshold.tex", "70{,}685", "destroy-and-repair trial count")
claim("n=9 explicit code: D = D_0 = 0.75, margin 2/3, min_deg 3",
      abs(dr["verify"]["D0"] - 0.75) < 1e-12
      and abs(dr["verify"]["min_margin"] - 2 / 3) < 1e-9
      and dr["check"]["min_deg_outside"] == 3,
      f"D0={dr['verify']['D0']} margin={dr['verify']['min_margin']:.6f} "
      f"min_deg={dr['check']['min_deg_outside']}")
claim("n=9 code has zero internal edges (the reason shrink search cannot move)",
      dr["check"]["internal_edges"] == 0, f"artifact {dr['check']['internal_edges']}")
present("05-threshold.tex", "zero internal edges", "internal-edge claim")

# the Fink-Jacobson bound values quoted in Section 5
import math
for n, quoted in [(7, 28.44), (9, 93.09)]:
    fj = 2 ** (n + 1) / (n + 2)
    claim(f"n={n}: Fink-Jacobson bound quoted as {quoted}",
          abs(fj - quoted) < 0.05, f"computed {fj:.2f}")
    present("05-threshold.tex", f"${quoted}$", f"n={n} Fink-Jacobson value")

# gamma_2 vs gamma coincidence, and the n=5 counterexample that kills it
print("\nSection 5: the coincidence disarmed in the text")
GAMMA = {4: 4, 6: 12, 7: 16, 8: 32}          # Ostergard-Blass / classical values
G2 = {3: seq["n3"]["method_M"], 5: seq["n5"]["method_M"],
      6: seq["n6"]["method_M"], 7: seq["n7"]["method_M"]}
claim("gamma_2(Q_3)=4, gamma_2(Q_6)=16, gamma_2(Q_7)=32 come from the artifact",
      (G2[3], G2[6], G2[7]) == (4, 16, 32), f"artifact {G2}")
claim("they match gamma(Q_4), gamma(Q_7), gamma(Q_8)",
      (G2[3], G2[6], G2[7]) == (GAMMA[4], GAMMA[7], GAMMA[8]))
claim("and the pattern is FALSE at n=5, exactly as the paper says",
      G2[5] == 10 and GAMMA[6] == 12, f"gamma_2(Q_5)={G2[5]}  gamma(Q_6)={GAMMA[6]}")

# ------------------------------------------------------ section 6 prose claims
print("\nSection 6 prose")
ag = tex("06-agent-systems.tex")
lo20 = math.ceil(2 ** 21 / 22)
printed20 = re.search(r"flatness requires \$K\$ between \$([0-9{},]+)\$", ag)
claim("n=20 lower end in the text equals ceil(2^21/22)",
      printed20 is not None
      and printed20.group(1).replace("{,}", "") == str(lo20),
      f"paper {printed20.group(1) if printed20 else 'NOT FOUND'}  computed {lo20}")
present("06-agent-systems.tex", "$95{,}326$", "n=20 lower bound")
present("06-agent-systems.tex", "$131{,}072$", "n=20 upper bound")
claim("n=20 upper end is 2^17 = 131072", 2 ** (20 - math.floor(math.log2(11))) == 131072)
for frag, label in [("$16.5$--$17.0$", "n=20 bit range"),
                    ("$45.3$--$46.0$", "n=50 bit range"),
                    ("$1800$", "Bittensor commit-reveal interval")]:
    present("06-agent-systems.tex", frag, label)
claim("n=20 bits: log2 of the bracket is 16.54 to 17.00",
      abs(math.log2(lo20) - 16.54) < 5e-3 and abs(math.log2(131072) - 17.0) < 1e-9)
lo50 = math.ceil(2 ** 51 / 52)
hi50 = 2 ** (50 - math.floor(math.log2(26)))
claim("n=50 bits: log2 of the bracket is 45.30 to 46.00",
      abs(math.log2(lo50) - 45.30) < 5e-3 and abs(math.log2(hi50) - 46.0) < 5e-3,
      f"[{math.log2(lo50):.2f}, {math.log2(hi50):.2f}]")

# ------------------------------------------------------------------- Table 3
# Parsed from the LaTeX, not restated, for the same reason as Table 1.
print("\nTable 3 (compression ratio) parsed from the LaTeX")
KFLAT = {3: (4, 4), 5: (10, 10), 7: (32, 32), 9: (97, 128)}


def bracket(n):
    if n in KFLAT:
        return KFLAT[n]
    return math.ceil(2 ** (n + 1) / (n + 2)), 2 ** (n - math.floor(math.log2(n / 2 + 1)))


t3 = re.search(r"\$C\(n\)\$\s*&(.+?)\\\\", tex("06-agent-systems.tex"))
claim("Table 3's C(n) row is present and parseable", t3 is not None)
if t3:
    cells = [c.strip() for c in t3.group(1).split("&")]
    claim("Table 3 has six C(n) cells (n = 3,5,7,9,20,50)", len(cells) == 6,
          f"parsed {cells}")
    for n, cell in zip((3, 5, 7, 9, 20, 50), cells):
        lo, hi = bracket(n)
        got = sorted((2 ** n / hi, 2 ** n / lo))
        nums = [float(x) for x in re.findall(r"[0-9]+(?:\.[0-9]+)?", cell)]
        ok = nums and all(
            any(abs(v - g) <= 0.05 * max(1.0, g) for g in got) for v in nums)
        claim(f"Table 3: C({n}) cell '{cell}' matches [{got[0]:.2f}, {got[1]:.2f}]", ok)

# ------------------------------------------------------------------- Table 4
print("\nTable 4 (mechanisms) against experiment_agents.json")
try:
    exp = json.load(open(data("experiment_agents.json")))
    base = {r["mechanism"]: r for r in exp["5"]["q0.5_eta0.0"]}
except (OSError, KeyError) as e:
    claim("experiment_agents.json is present and has the n=5 noiseless block",
          False, str(e))
    base = {}

NAME = {"prefix-4": "prefix4", "prefix-2": "prefix2", "top-2": "top2",
        "hash-10": "hash10"}
mech_rows = re.findall(
    r"^(full|count|threshold|prefix-4|prefix-2|top-2|hash-10|flat|kmedian)\s*&"
    r"\s*\$(\d+)\$\s*&\s*\$([0-9.]+)\$\s*&\s*\$([0-9.]+)\$\s*&"
    r"\s*\$([0-9.]+)\$\s*&\s*(?:\\textbf\{)?(yes|no)",
    tex("065-experiment.tex"), re.MULTILINE)
claim("Table 4 parsed all nine mechanism rows", len(mech_rows) == 9,
      f"parsed {len(mech_rows)}")
for name, K, D, D0, g, flat in mech_rows:
    key = NAME.get(name, name)
    r = base.get(key)
    if r is None:
        UNSOURCED.append(f"Table 4 row '{name}' has no artifact row")
        print(f"  [MISS] Table 4 row {name} absent from the artifact")
        continue
    ok = (int(K) == r["K"] and abs(float(D) - r["D"]) < 5e-5
          and abs(float(D0) - r["D0_unrestricted"]) < 5e-5
          and abs(float(g) - r["gamma"]) < 5e-5
          and (flat == "yes") == bool(r["flat"]))
    claim(f"Table 4 row {name} matches the artifact", ok,
          f"paper K={K} D={D} D0={D0} g={g} flat={flat}  |  artifact K={r['K']} "
          f"D={r['D']:.4f} D0={r['D0_unrestricted']:.4f} g={r['gamma']:.4f} "
          f"flat={r['flat']}")

# the two headline numbers quoted in the prose of that section
if base:
    f_, km = base.get("flat"), base.get("kmedian")
    claim("flat and kmedian really do share K and D in the artifact",
          f_ and km and f_["K"] == km["K"] and abs(f_["D"] - km["D"]) < 1e-9
          and f_["gamma"] > 0.49 and km["gamma"] < 1e-7)
    c3 = {r["mechanism"]: r for r in exp["3"]["q0.5_eta0.0"]}["count"]
    c5 = base["count"]
    claim("the aggregate margin really is 1/n at n=3 and n=5",
          abs(c3["gamma"] - 1/3) < 1e-9 and abs(c5["gamma"] - 1/5) < 1e-9,
          f"n=3 {c3['gamma']:.6f}, n=5 {c5['gamma']:.6f}")
    present("065-experiment.tex", "$1/n$", "the 1/n aggregate-margin claim")
    pre = io.open(data("PREREGISTRATION_2026-09-15.md"), encoding="utf-8").read()
    claim("the pre-registration predicted gamma(count)=1, i.e. we were wrong",
          "count}) = 1$ in" in pre,
          "the falsified prediction is still on the record in the pre-registration")


print("\nTable 5 (episode records) against experiment_episodes.json")
try:
    epi = json.load(open(data("experiment_episodes.json")))
    erows = {r["scheme"]: r for r in epi["5"]["exact"]}
except (OSError, KeyError) as e:
    claim("experiment_episodes.json present with the n=5 block", False, str(e))
    erows = {}

EPI_NAME = {"full trace": "full_trace", "one bit per agent": "per_agent_bit",
            "top-half agents only": "per_agent_coarse",
            "multiset of artifacts": "global_summary",
            "count of completions": "aggregate",
            "final output only": "final_output"}
epi_rows = re.findall(
    r"^([a-z][a-z \-]+?)\s*&\s*\$(\d+)\$\s*&\s*\$([0-9.]+)\$\s*&"
    r"\s*\$([0-9.]+)\$\s*\\\\",
    tex("065-experiment.tex"), re.MULTILINE)
epi_rows = [r for r in epi_rows if r[0].strip() in EPI_NAME]
claim("Table 5 parsed all six episode rows", len(epi_rows) == 6,
      f"parsed {[r[0].strip() for r in epi_rows]}")
for name, K, D, g in epi_rows:
    r = erows.get(EPI_NAME[name.strip()])
    if r is None:
        UNSOURCED.append(f"Table 5 row {name} has no artifact"); continue
    ok = (int(K) == r["K"] and abs(float(D) - r["D"]) < 5e-5
          and abs(float(g) - r["gamma"]) < 5e-5)
    claim(f"Table 5 row {name.strip()} matches the artifact", ok,
          f"paper K={K} D={D} g={g}  |  artifact K={r[chr(34)+chr(75)+chr(34)] if False else r['K']} "
          f"D={r['D']:.4f} g={r['gamma']:.4f}")
if erows:
    ft, pab = erows["full_trace"], erows["per_agent_bit"]
    claim("one bit per agent really does match the full trace on both axes",
          abs(ft["D"] - pab["D"]) < 1e-9 and abs(ft["gamma"] - pab["gamma"]) < 1e-9,
          f"full K={ft['K']} vs per-agent K={pab['K']}")
    gs = erows["global_summary"]
    claim("the multiset record really has a smaller margin than one bit per agent",
          gs["gamma"] < pab["gamma"] - 1e-9,
          f"{gs['gamma']:.4f} < {pab['gamma']:.4f}")
    worst = max(max(c["dD"], c["dgamma"]) for c in epi["5"]["sampled"])
    m = re.search(r"to within \$([0-9.]+)\$ at", tex("065-experiment.tex"))
    claim("the paper states a sampling bound at all", m is not None)
    if m:
        claim("the stated sampling bound is not an understatement",
              float(m.group(1)) >= worst - 1e-9,
              f"paper says {m.group(1)}, measured worst {worst:.4f}")


print("\nTable 6 (LLM episodes) against experiment_llm_scored.json")
try:
    llm = json.load(open(data("experiment_llm_scored.json")))
except OSError as e:
    claim("experiment_llm_scored.json present", False, str(e)); llm = {}
LLM_NAME = {"full trace": "full_trace", "per-agent summary": "per_agent_summary",
            "artifact multiset": "artifact_multiset",
            "global summary": "global_summary", "final output only": "final_output"}
llm_rows = re.findall(r"^([a-z][a-z -]+?)\s*&\s*\$(\d+)\$\s*&\s*\$([0-9.]+)\$\s*\\\\", tex("066-llm.tex"), re.MULTILINE)
llm_rows = [r for r in llm_rows if r[0].strip() in LLM_NAME]
claim("Table 6 parsed all five rows", len(llm_rows) == 5,
      f"parsed {[r[0].strip() for r in llm_rows]}")
for name, by, err in llm_rows:
    r = llm.get(LLM_NAME[name.strip()])
    if r is None:
        UNSOURCED.append(f"Table 6 row {name}"); continue
    ok = abs(int(by) - r["bytes"]) <= 1 and abs(float(err) - r["D_judge"]) < 5e-4
    claim(f"Table 6 row {name.strip()} matches the artifact", ok,
          f"paper {by}B/{err}  artifact {r[chr(98)+chr(121)+chr(116)+chr(101)+chr(115)]:.0f}B/{r[chr(68)+chr(95)+chr(106)+chr(117)+chr(100)+chr(103)+chr(101)]:.3f}")
gapinfo = llm.get("_attribution_gap")
if gapinfo:
    m = re.search(r"by\s+\$([0-9.]+)\$\s+bits\s+of\s+attribution\s+error", tex("066-llm.tex"))
    claim("the quoted attribution gap matches the artifact",
          m is not None and abs(float(m.group(1)) - gapinfo["difference"]) < 5e-4,
          f"paper {m.group(1) if m else None}  artifact {gapinfo[chr(100)+chr(105)+chr(102)+chr(102)+chr(101)+chr(114)+chr(101)+chr(110)+chr(99)+chr(101)]:.3f}")
    ci = re.search(r"\$\[([0-9.]+), ([0-9.]+)\]\$", tex("066-llm.tex"))
    claim("the quoted bootstrap interval matches the artifact",
          ci is not None
          and abs(float(ci.group(1)) - gapinfo["ci95"][0]) < 5e-4
          and abs(float(ci.group(2)) - gapinfo["ci95"][1]) < 5e-4,
          f"paper [{ci.group(1)}, {ci.group(2)}]" if ci else "not found")


# ------------------------------------------------- environment and check count
print("\nEnvironment and check-count consistency")
env = json.load(open(data("environment.json")))
claim("environment.json reports matches_pinned", env["matches_pinned"] is True)
for f in ("A-proofs.tex",):
    body = tex(f)
    for field in ("python_short", "numpy", "scipy"):
        v = env[field]
        claim(f"the appendix states {field} = {v}", v in body, f"{v}")

m = re.search(r"All\s*\$(\d+)\$\s*checks", tex("A-proofs.tex"))
claim("the appendix states a check count", m is not None)
if m:
    import subprocess
    r = subprocess.run([sys.executable, str(data("src/verify_all.py"))],
                       capture_output=True, text=True, cwd=str(data(".")))
    actual = r.stdout.count("[PASS]")
    claim(f"the stated count ({m.group(1)}) equals what verify_all.py emits",
          int(m.group(1)) == actual and r.returncode == 0,
          f"verify_all emitted {actual} passes, exit {r.returncode}")

# ------------------------------------------------------------------ summary
print("\n" + "=" * 62)
if UNSOURCED:
    print(f"{len(UNSOURCED)} claim(s) could not be located in the paper:")
    for u in UNSOURCED:
        print("  -", u)
if FAILS:
    print(f"{len(FAILS)} MISMATCH(ES) between paper and artifact:")
    for f in FAILS:
        print("  -", f)
    sys.exit(1)
if UNSOURCED:
    sys.exit(1)
print("EVERY AUDITED NUMBER IN THE PAPER MATCHES ITS ARTIFACT.")
sys.exit(0)
