#!/usr/bin/env python3
"""
Reproduce every number in RESULTS.md from scratch.

Usage:
    python3 scripts/reproduce.py /path/to/sam4c-cli.jar

Or set SAM4C_JAR:
    SAM4C_JAR=/path/to/sam4c-cli.jar python3 scripts/reproduce.py

The jar must be built from sam4c-cli at commit 9850fbd564c0e9db9504627f53f99ce12268a978
(see tool/README.md for build instructions). Run from the repo root of this
evaluation folder (sam4c-evaluation/), or the paths below will not resolve.
"""
import subprocess, sys, os, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JAR = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SAM4C_JAR")
if not JAR or not os.path.isfile(JAR):
    print("Give the built sam4c-cli.jar as an argument, or set SAM4C_JAR.")
    print("See tool/README.md for how to build it.")
    sys.exit(2)

PAT = [
    ("unauthenticated entry", "is exposed (exposure: external) but no"),
    ("exposed data store", "Data store '"),
    ("unintended exposure", "is declared exposure="),
    ("isolation violated", "Isolation violated:"),
    ("plaintext channel", "requires a protected channel"),
    ("authentication bypass", "Authentication requires access from"),
    ("insufficient replicas", "requirement not satisfied"),
    ("no zone spread", "would take it down"),
    ("contradictory policy", "Isolation requires no path between two sides"),
    ("access without authn", "Authorization grants access to"),
    ("vacuous resolution", "matches no components"),
]


def run(arch, rules):
    out = subprocess.run(
        ["java", "-jar", JAR, "--validate", arch, rules],
        capture_output=True, text=True,
    ).stdout
    warns = [l.strip()[2:] for l in out.splitlines() if l.startswith("  !")]
    c = collections.Counter()
    for w in warns:
        for name, needle in PAT:
            if needle in w:
                c[name] += 1
                break
    return ("Conformance OK" in out), warns, c


# The expected findings per check, one real system at a time. This is not a
# comparison against another tool (no such baseline exists yet, see
# METHODOLOGY.md section 8) -- it's the already-verified output from
# FINDINGS.md, copied here so a future run can be checked against it and any
# drift is caught, not missed.
SYSTEMS = {
    "bank-of-anthos":     {"unauthenticated entry": 1, "plaintext channel": 3, "insufficient replicas": 1},
    "hotel-reservation":  {"unauthenticated entry": 1, "insufficient replicas": 4},
    "online-boutique":    {"unauthenticated entry": 1, "plaintext channel": 1, "insufficient replicas": 2},
    "opentelemetry-demo": {"unauthenticated entry": 1, "plaintext channel": 1, "insufficient replicas": 3},
    "social-network":     {"unauthenticated entry": 2, "isolation violated": 1, "insufficient replicas": 12},
    "sock-shop":          {"unauthenticated entry": 1, "isolation violated": 1, "plaintext channel": 1, "insufficient replicas": 5},
    "teastore":           {"unauthenticated entry": 1, "authentication bypass": 1, "insufficient replicas": 1},
}

fail = 0
n = 0


def check(ok, label):
    global fail, n
    n += 1
    fail += 0 if ok else 1
    print(("PASS  " if ok else "FAIL  ") + label)


print("== real systems (conformance + expected findings, matches RESULTS.md) ==")
tot = 0
for s, exp in SYSTEMS.items():
    arch = f"{ROOT}/real-systems/inputs/{s}.arch.yaml"
    rules = f"{ROOT}/real-systems/inputs/{s}.secdsl"
    ok, warns, c = run(arch, rules)
    tot += len(warns)
    check(ok, f"{s}: conformance")
    check(dict(c) == exp and sum(exp.values()) == len(warns), f"{s}: {len(warns)} findings {dict(c)}")

    # rewrite real-systems/outputs/<system>.txt every run, so it can never
    # drift from what the tool actually reports right now
    out_path = f"{ROOT}/real-systems/outputs/{s}.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(f"  ! {w}" for w in warns) + ("\n" if warns else ""))

check(tot == 45, f"total findings = {tot} (expected 45)")

print(f"\n{n - fail}/{n} checks passed")
sys.exit(1 if fail else 0)
