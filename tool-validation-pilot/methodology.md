# Evaluation methodology (CWE-1008 coverage) - documented procedure

Goal: a reproducible procedure so every IN/OUT and covered/gap verdict in the triage is
*derivable*, not asserted. Two raters apply it; disagreements resolved conservatively (toward OUT
for scope, toward gap for coverage) and recorded.

## 1. Source and denominator
We use CWE-1008 (Architectural Concepts), a platform-independent MITRE taxonomy. We classify
**every** member weakness of **every** category (the complete set), so selection is not ours.
Unit of classification = the **member weakness** (one per row), grouped by its tactic. Concrete
CVEs come from each weakness's MITRE "Observed Examples" (grounding/prevalence, not chosen by us).

## 2. Scope decision: IN vs OUT

**Definition.** A weakness is **IN** iff it is a property of the deployment architecture/configuration
that (a) the architecture metamodel can **represent**, and (b) can be **remedied by changing the
deployment model** (arch.yaml / secdsl), without editing any component's source code. Otherwise OUT.

**Procedure per weakness (record which step decided it):**
1. **Modes of Introduction** (from the CWE page): if it lists *Architecture and Design* or
   *Operation/Configuration* -> IN-candidate; if only *Implementation* -> OUT-candidate.
2. **Fix test**: to remove the weakness, do you change the deployment model or change code inside a
   component? model -> IN; code -> OUT.
3. **Representability**: can the metamodel express the relevant fact (exposure, connector, link,
   deployedOn, a required security property, scale/spread, a secret reference, an image reference,
   a placement/zone)? If not representable -> OUT.
4. If 1-3 conflict -> `(review)`, decide with the second rater, default OUT, record the reason.

**Scope-reason codes** (record one per row):
- IN: `design-introduced`, `topology`, `access-policy`, `exposure`, `secret-ref`,
  `encryption-config`, `resource-limit`, `placement`.
- OUT: `impl-code`, `crypto-impl`, `input/injection`, `session/app`, `runtime/kernel`,
  `auth-mechanism-logic`, `audit-not-modeled`, `not-representable`.

## 3. Coverage decision: covered vs gap  (only for IN weaknesses)

**Definition.** A weakness is **covered** iff there exists an implemented check whose **trigger
condition is satisfied by some faithful architecture that exhibits this weakness class**, and a
vuln/fixed model demonstrates the tool flags the vulnerable design and clears the fixed one.
Otherwise it is a **gap** (IN + representable, but no implemented check detects it); name the
property that would close it.

**The 7 implemented checks and their exact trigger conditions** (coverage is decided against these):
- c1 Availability: an `Availability` target workload lacks effective `replicas >= 2`, or (high) lacks `spread: zone`.
- c2 Isolation: an `Isolation` rule's two sides share a resolved connector path.
- c3 missing-auth: a workload with `exposure: external` has no `Authentication` targeting it.
- c4 exposed-data: a `Data` component is `exposure: external` or attached to an `external` connector.
- c5 accidental-exposure: a workload with `exposure != external` is attached to an `external` connector.
- c6 authz-without-authn: an `Authorization` rule's resource has no `Authentication` guarding it.
- c7 iso-vs-comm: an `Isolation` and a `Confidentiality`/`Integrity`/`Authentication` rule cover the same pair.

**Procedure per IN weakness:**
1. State the **model fact** that expresses the weakness (e.g. CWE-319 -> "data flows over a
   connector with no encryption requirement enforced").
2. Does any check's trigger condition (above) fire on an architecture with that fact? 
   - **yes** -> `covered`; cite the check (cX) and the demonstrating case.
   - **no** -> `gap`; name the missing property/check (e.g. Confidentiality).
3. **No "partial".** If a check fires on a faithful instantiation of the weakness class, it is
   covered; if the weakness's defining cases are not what any check detects, it is a gap. Borderline
   -> gap, with a note. (This replaces the earlier vague `covered~`.)

**Coverage-reason** (record one per IN row):
- covered: "check cX fires on <fact>" (+ case).
- gap: "representable as <fact>; no check fires; needs <property>" (e.g. needs Confidentiality,
  Integrity, Secrets, least-privilege Authorization, finer-grained Authorization, Audit).

## 4. Why most IN weaknesses are gaps (the honest consequence)
The 7 checks detect a small fixed set of facts (exposure, isolation path, missing/absent auth/authz,
resource redundancy, policy contradiction). Any IN weakness whose defining fact is **outside** that
set has no firing check and is a gap: encryption (319, 311-314), integrity (353, 924, 494), secrets
(258/259/260/798/321...), least-privilege (266/269/272/732...), finer-grained authz (863), audit.
These name the future-work properties, in priority order.

## 5. Recording (so each row is auditable)
Each triage row carries: Scope (IN/OUT) + scope-reason code; Verdict (covered cX / gap+needed-property
/ out-reason). Anyone can re-derive the verdict from the CWE's Modes of Introduction + the fix test
(scope) and the 7 trigger conditions (coverage).

## 6. Threats to validity
- The mapping is a human judgment -> two raters, report inter-rater agreement, list disagreements.
- "covered" is demonstrated by *representative* models, not exhaustive per-CVE -> we test one
  faithful model per covered class; CVE Observed Examples show the class is real and common.
- Scope boundary is principled (design vs code) and pre-stated, not adjusted to results; OUT is
  never used for "we miss it" (that is a gap).
