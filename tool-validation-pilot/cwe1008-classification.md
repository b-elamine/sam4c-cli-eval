# CWE-1008 (Architectural Concepts) classification - fill manually

Source of truth: MITRE CWE-1008 view (https://cwe.mitre.org/data/definitions/1008.html).

## Structure (three levels)
A tactic does NOT hold CVEs. It expands into a sub-list of **member weaknesses**, and CVEs
("Observed Examples") attach to each member weakness:

```
Tactic (category)            e.g. Authenticate Actors
  -> member weakness (CWE)   e.g. CWE-306 Missing Authentication, CWE-258 Empty Password,
                                  CWE-798 Hard-coded Credentials, CWE-521 Weak Password Reqs ...
       -> Observed Examples  real CVEs listed on that member-weakness page
```

So the UNIT you classify is the **member weakness** (one row each); the tactic is just the group
label (it repeats); the CVE column holds that member weakness's own Observed Examples. One tactic
yields several rows, and they can have DIFFERENT verdicts (some covered, some gap, some
out-of-scope) - that finer grain is what makes the result honest. The rows in the table below are
one-per-tactic starters only; replace them with one row per member weakness.

## How to fill each column
- **Tactic**: the CWE-1008 category name (e.g. Authenticate Actors, Limit Access, Encrypt Data...).
- **CWE**: the member weakness id (e.g. CWE-306).
- **Name**: its short name.
- **Scope**: `in` if it is a design/architecture-level weakness; `out` if it is code / app / runtime
  level (state why in Name or a note). Use the SAME principle every time (decide once).
- **Check**: which of our checks addresses it - one of:
  missing-auth, exposed-data, accidental-exposure, Isolation, Availability, authz-without-authn,
  Isolation-vs-communication  -  or `-` if none yet.
- **Test**: the runnable demo case (c1..c7) if covered, else `-`.
- **Verdict**: `covered` (in-scope + a check + a passing test) / `gap` (in-scope, no check yet) /
  `out-of-scope` (Scope = out).
- **Observed CVEs**: a few real CVEs from that CWE page's "Observed Examples" (optional, for grounding).

Keep one weakness per row. Do not skip the `out` ones - listing them is the anti-cherry-pick proof.

## Table (fill: one row per MEMBER WEAKNESS, grouped by tactic)

The two example rows below show the pattern (one tactic, several member weaknesses, mixed
verdicts). Delete them and fill from MITRE; do not leave one-row-per-tactic.

| Tactic | CWE | Name | Scope | Check | Test | Verdict | Observed CVEs |
|--------|-----|------|-------|-------|------|---------|---------------|
| Authenticate Actors | CWE-306 | Missing Authentication for Critical Function | in | missing-auth | c3 | covered | (fill) |
| Authenticate Actors | CWE-798 | Use of Hard-coded Credentials | in | - | - | gap (secrets) | (fill) |
| ... | ... | ... | ... | ... | ... | ... | ... |

For reference, the member weaknesses our checks already cover (slot each under its tactic):
- CWE-306 Missing Authentication -> missing-auth -> c3
- CWE-862 Missing Authorization -> authz-without-authn -> c6
- CWE-668 Exposure of Resource to Wrong Sphere -> Isolation (c2) and exposed-data/accidental-exposure (c4/c5)
- CWE-319 Cleartext Transmission -> gap (Encrypt Data tactic)
- CWE-924 Improper Enforcement of Message Integrity -> gap (Verify Message Integrity tactic)
- CWE-400 Uncontrolled Resource Consumption -> Availability -> c1 (verify it appears in the 1008 view; if not, cite from its own view and note that)

## When done
Save this file and tell me, or paste the table in chat. I will:
- compute the numbers (in-scope total, covered, gap, out-of-scope; coverage %),
- build the evaluation table for the paper,
- flag any row whose Verdict is inconsistent with Scope/Check/Test.
