#!/usr/bin/env python3
"""One-command regression: python3 private/run-all-tests.py   (from the repo root, jar built)"""
import subprocess, sys, os, re, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JAR = ROOT + "/target/sam4c-cli.jar"
PAT = [("unauthenticated entry", "is exposed (exposure: external) but no"), ("exposed data store", "Data store '"),
       ("unintended exposure", "is declared exposure="), ("isolation violated", "Isolation violated:"),
       ("plaintext channel", "requires a protected channel"), ("authentication bypass", "Authentication requires access from"),
       ("insufficient replicas", "requirement not satisfied"), ("no zone spread", "would take it down"),
       ("contradictory policy", "Isolation requires no path between two sides"), ("access without authn", "Authorization grants access to"),
       ("vacuous resolution", "matches no components")]

def run(arch, rules):
    out = subprocess.run(["java", "-jar", JAR, "--validate", arch, rules], capture_output=True, text=True, cwd=ROOT).stdout
    warns = [l.strip()[2:] for l in out.splitlines() if l.startswith("  !")]
    c = collections.Counter()
    for w in warns:
        for n, p in PAT:
            if p in w: c[n] += 1; break
    return ("Conformance OK" in out), warns, c

# real systems: expected findings per check (regression baseline)
SYSTEMS = {
 "bank-of-anthos":     {"unauthenticated entry": 1, "plaintext channel": 3, "insufficient replicas": 1},
 "hotel-reservation":  {"unauthenticated entry": 1, "insufficient replicas": 4},
 "online-boutique":    {"unauthenticated entry": 1, "plaintext channel": 1, "insufficient replicas": 2},
 "opentelemetry-demo": {"unauthenticated entry": 1, "plaintext channel": 1, "insufficient replicas": 3},
 "social-network":     {"unauthenticated entry": 2, "isolation violated": 1, "insufficient replicas": 12},
 "sock-shop":          {"unauthenticated entry": 1, "isolation violated": 1, "plaintext channel": 1, "insufficient replicas": 5},
 "teastore":           {"unauthenticated entry": 1, "authentication bypass": 1, "insufficient replicas": 1},
}
# pilot: check each vulnerable variant must raise (and nothing else), fixed must be silent
PILOT = {
 "c1-cwe400-availability": {"insufficient replicas", "no zone spread"}, "c2-cwe668-isolation": {"isolation violated"},
 "c3-cwe306-missing-auth": {"unauthenticated entry"}, "c4-cwe200-exposed-data": {"unauthenticated entry", "exposed data store"},
 "c5-cwe668-accidental": {"unintended exposure"}, "c6-cwe862-authz-noauthn": {"access without authn"},
 "c7-contradiction-iso-conf": {"contradictory policy"}, "c8-multihop-mediator": {"isolation violated"},
 "c9-cwe306-token-at-target": {"authentication bypass"}, "c10-cwe319-plaintext": {"plaintext channel"},
 "c11-cwe923-weakhop-chain": {"isolation violated", "unauthenticated entry"}, "c12-vacuous-resolution": {"vacuous resolution"},
}
fail = 0; n = 0
def check(ok, label):
    global fail, n
    n += 1; fail += 0 if ok else 1
    print(("PASS  " if ok else "FAIL  ") + label)

print("== real systems (conformance + expected findings)")
tot = 0
for s, exp in SYSTEMS.items():
    ok, warns, c = run(f"private/case-study/{s}.arch.yaml", f"private/case-study/{s}.secdsl"); tot += len(warns)
    check(ok, f"{s}: conformance")
    check(dict(c) == exp and sum(exp.values()) == len(warns), f"{s}: {len(warns)} findings {dict(c)}")
check(tot == 45, f"total findings = {tot} (expected 45)")
print("== mutation pilot (vulnerable raises exactly the intended check, fixed is silent)")
covered = set()
for p, want in PILOT.items():
    okv, wv, cv = run(f"private/cve-pilot/{p}/vuln.arch.yaml", f"private/cve-pilot/{p}/vuln.secdsl")
    okf, wf, cf = run(f"private/cve-pilot/{p}/fixed.arch.yaml", f"private/cve-pilot/{p}/fixed.secdsl")
    check(okv and okf and set(cv) == want and len(wf) == 0, f"{p}: vulnerable {sorted(cv)} / fixed {len(wf)} findings")
    covered |= set(cv)
check(len(covered) == 11, f"checks exercised by the pilot: {len(covered)}/11")
print(f"\n{n - fail}/{n} tests passed")
sys.exit(1 if fail else 0)
