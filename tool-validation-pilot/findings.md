# CVE-robustness pilot — findings

**Last verified: 2026-07-30** by re-running `bash private/cve-pilot/run.sh` against the current
build (`target/sam4c-cli.jar`), after the Deployable/Host/Colocation/Implementation architecture
metamodel port. All 7 cases still discriminate (vuln flagged, fixed clean).

---

## 1. What this pilot is (and is not)

**What it is:** a *discrimination test*. For each of 7 architectural weakness classes, we model a
**vulnerable** design and a **fixed** design, run the tool on each, and check that the tool flags
the vulnerable one and stays silent on the fixed one. If a check cannot tell a bad design from a
good one, it is worthless — this is the minimum bar, and all 7 pass it.

**What it is NOT:** a coverage measurement. It does not say *how much* of the threat space the tool
covers. That question (how many CWE-1008 weaknesses are addressed) is answered separately in
`cwe1008-triage.md` / `methodology.md`, and the honest number there is ~12 of ~45 design-level
weaknesses. Do not read "all 7 prevented" as "prevents everything" — it means "on these 7 classes,
the checks fire correctly."

**Threat model:** model-level detection of *architectural / configuration* weaknesses. Code bugs
(injection, memory safety, crypto implementation) are out of scope by design.

**Wording discipline:** the checks emit *semantic warnings*. They are non-blocking unless `--strict`
is passed. So the precise claim is "**flagged** at design time," and "**prevented** only under
`--strict`" (which makes a flagged design exit non-zero and write no output). Avoid saying
"prevented by design" unqualified — it overclaims.

---

## 2. How a case is built

Each case folder holds two model pairs:

```
cN-cweXXX-name/
  vuln.arch.yaml   vuln.secdsl     # the weak design
  fixed.arch.yaml  fixed.secdsl    # the corrected design
```

- `*.arch.yaml` — the architecture (components, exposure, ports, connectors, links).
- `*.secdsl`   — the security requirements (`#attribute`, `#context`, `#property` directives).

Run one variant:
```
java -jar target/sam4c-cli.jar  cN/vuln.arch.yaml  cN/vuln.secdsl
```
`run.sh` runs all 14 variants and classifies each by grepping the output:
`Conformance violations` → FLAGGED (conformance); a line starting `  ! ` → FLAGGED (semantic);
`Error:` → ERROR (broken test); otherwise → clean.

Important: in every case the vulnerable model is a **valid, conformant** model. The problem is never
a malformed model — it is a well-formed model whose *design* is insecure. So every flag below comes
from the **semantic** layer, never the conformance layer.

---

## 3. Results — verified 2026-06-25

| Case | CWE | Check (code) | vuln | fixed |
|------|-----|--------------|------|-------|
| c1 | CWE-400 DoS / EDoS | Availability satisfiability (`SemanticValidator:122-143`) | FLAGGED | clean |
| c2 | CWE-668 missing isolation | Isolation path (`:45-51`) | FLAGGED | clean |
| c3 | CWE-306 missing authentication | missing-auth (`:53-66`) | FLAGGED | clean |
| c4 | CWE-200 / 668 exposed data | exposed-data (`:79-86`) | FLAGGED | clean |
| c5 | CWE-668 accidental exposure | accidental-exposure (`:88-96`) | FLAGGED | clean |
| c6 | CWE-862 broken access control | authz-without-authn (`:98-105`) | FLAGGED | clean |
| c7 | policy contradiction | isolation-vs-communication (`:107-120`) | FLAGGED | clean |

### Exact warnings produced on the vulnerable models (real output)

- **c1** (two warnings — both halves of the high-availability requirement fail):
  - `Availability=high but 'API' has 1 copy (needs >= 2) -- single point of failure, requirement not satisfied`
  - `Availability=high but 'API' is not spread across zones (...) -- a whole-zone outage would take it down`
- **c2**: `Isolation violated: a network path exists via connector 'shared' between the two sides -- they are not isolated`
- **c3**: `'AdminAPI' is exposed (exposure: external) but no Authentication rule guards it -- unauthenticated entry point`
- **c4** (two warnings — see note below):
  - `'DB' is exposed (exposure: external) but no Authentication rule guards it -- unauthenticated entry point`
  - `Data store 'DB' faces the external sphere -- a stateful store should not be directly exposed`
- **c5**: `'Svc' is declared exposure=internal but is wired to an external connector -- unintended exposure`
- **c6**: `Authorization grants access to 'DB' but no Authentication rule guards it -- access without authentication`
- **c7**: `Isolation requires no path between two sides that Confidentiality connects -- contradictory policy`

**On c4's double warning:** checks are *global* — they all run on every model — so one design can
trip several, each a legitimate true positive. An externally-exposed data store is both an exposed
store (c4) and an unauthenticated entry point (c3). This is correct behaviour, not a bug. For a
clean one-concern-per-row demo, either scope each case to a single concern or report the secondary
finding explicitly (as done here).

---

## 4. What each case demonstrates, and where the fix lives

A useful lens: **where does the fix go — the architecture or the security model?**

- **c1 — Availability.** secdsl identical in vuln/fixed (`Availability(backendCtx, high)`). The fix
  is purely architectural: `replicas: 1` → `replicas: 3` plus `spread: zone`. Shows a declared
  requirement being *enforced*, not just recorded.
- **c2 — Isolation.** secdsl identical (`Isolation(dbCtx, frontendCtx)`). The fix is topological:
  one shared connector → two separate connectors, so no path exists. The merge computes the path;
  the check reads it.
- **c3 — Missing auth.** *By-default* check: fires with no security rule at all. Fix adds an
  `Authentication` rule (and an IdP component) so the exposed workload is guarded.
- **c4 — Exposed data.** *By-default*. Fix flips the data store `exposure: external` → `internal`.
- **c5 — Accidental exposure.** *By-default*. Fix flips the connector `external: true` → `false`,
  matching the workload's declared internal exposure.
- **c6 — Authz without authn.** Requirement-driven (needs an `Authorization` rule). Fix adds an
  `Authentication ... -> dbCtx` so the granted resource is guarded.
- **c7 — Contradiction.** Same arch in both; the fix is in the security model — remove the
  `Confidentiality` rule that contradicts the `Isolation` over the same pair.

Two structural observations worth debating:
- **Three of seven checks (c3, c4, c5) are "secure by default"** — they need no security policy and
  fire from the architecture alone. Strength (security for free) or a blurring of what counts as a
  *security* property? Open question.
- **Two checks (c2, c6) are mostly readers** of what `ModelMerger` already computed (resolved paths,
  resolved contexts). The detection logic is thin; the merge does the heavy lifting.

---

## 5. Status of the checks (all implemented and verified)

In `SemanticValidator.validate(...)` (one method, sequential blocks). All reason only over types,
declared enums, references, resolved structure, and cross-rule relationships — never over free-form
attribute values, so no domain knowledge is baked in:

- coverage emptiness — a rule/context that matches nothing (generic sanity check)
- c1 Availability — medium needs ≥2 effective replicas; high also needs `spread: zone`
- c2 Isolation — a non-empty resolved path between the two sides is a violation
- c3 missing-auth — a workload `exposure: external` with no `Authentication` targeting it
- c4 exposed-data — a `Data` component facing the external sphere (external exposure or connector)
- c5 accidental-exposure — a workload `exposure != external` wired to an `external` connector
- c6 authz-without-authn — an `Authorization` resource that no `Authentication` guards
- c7 isolation-vs-communication — `Isolation` and a `Confidentiality`/`Integrity`/`Authentication`
  rule over the same pair

In `Main`: `--strict` → any warning or unresolved reference returns exit 1 and writes nothing
(detection becomes prevention).

> History: c1 was the first satisfiability check; c2 and c3 were originally identified as gaps in an
> earlier pass and have since been implemented (this demonstrated the "test → find gap → close →
> re-test" loop). c4–c7 followed. All are now in the build above.

---

## 6. Known limitations of this pilot (the honest list)

1. **Verdicts are decided by grepping human-readable output**, not a structured exit code or JSON.
   Rename a message string in the Java and the classifier silently misreads it. More robust: a
   `--format json` mode, or rely on the `--strict` exit code.
2. **No `expected` assertions.** `run.sh` prints verdicts but does not check them against a stored
   expectation, so it is a demo, not a regression test. Adding a per-case `expected` (vuln→flagged,
   fixed→clean) turns it into one.
3. **Seven hand-built cases is a demonstration, not a corpus.** The systematic coverage question is
   in `cwe1008-triage.md`; see also the evaluation-method discussion (CWE coverage is likely the
   wrong instrument for a design-level tool — `../related-work.md` and the cloudcom-paper memo).
4. **"Discrimination" ≠ "no false positives/negatives at scale."** Each case shows the check
   separates one bad design from one good one; it does not bound precision/recall over many designs.

---

## 7. Next (the actually-remaining work)

1. Add `expected` to each case and make `run.sh` assert it → a real regression test. (Items
   "close c2" and "implement c3" from the old plan are **done**.)
2. Decide the evaluation framing for the paper: the CWE-1008 coverage % is likely the wrong
   instrument — prefer case study + level-matched expressiveness (see the cloudcom-paper memo).
3. Optionally grow the corpus only if it serves the chosen framing; do not scale CWE coverage for
   its own sake.
