# Methodology

How this was built, short version. `scripts/reproduce.py` re-derives the
numbers below from the inputs, so this is enforced, not just written down.

## Goal

Do design-time checks find real, source-confirmed weaknesses in real
cloud-native systems, on their default config, no synthetic examples?

## Systems

7 public repos, chosen for domain spread (e-commerce, banking, observability,
hospitality, social) and platform spread (4 Kubernetes, 3 Compose). All
public source, so every finding can be checked against a line of code.
No production/proprietary systems, nothing modified to add a known CVE.

## Modeling: git to `.arch.yaml` + `.secdsl`

Manual, same 10 steps for all 7. Steps 9-10 are judgment calls, the rest is
a direct read of the repo.

| Step | Read from git | Goes into the model |
|---|---|---|
| 1 | the one deployment file the repo actually ships | one `Architecture` |
| 2 | nothing (manifest never says which machine runs a pod) | one `Worker` host, everything `deployedOn` it |
| 3 | every Deployment/StatefulSet/Compose service | one `Deployable`: `Data` if the image is a known DB/cache/broker, else `App` |
| 4 | `Service.type` / Compose `ports:` | `external` only for the real public entry, else `internal` |
| 5 | `containerPort`, known protocol of the image | one `Port`, number + protocol |
| 6 | env vars/ConfigMaps/`depends_on`, then source code if the manifest is silent | one `Connector` + 2 `Link`s per call |
| 7 | `image:` | one `Implementation` |
| 8 | volumes | `persistent: true` only if the volume outlives the pod |
| 9 | the author, reading the system | `Domain`/`DataClass` tags — first judgment call |
| 10 | the author, one rubric for all 7 | the `.secdsl` rules |

Why this shape, briefly: one ground-truth file only (no merging branches or
hand-picked subsets); no invented host topology since the manifest doesn't
have one; App/Data decided by image, not name, since names lie; exposure
defaults to internal unless the manifest says otherwise; source code is a
fallback only for edges the manifest doesn't state, never for anything else;
persistence means "survives losing the pod," not "is technically a DB
image." Steps 9-10 are the one place judgment enters, and that's the point
of naming them explicitly instead of pretending the whole thing is
mechanical.

## Rules: one rubric, applied to all 7

- Isolation: session/account store reachable from the entry only through its
  own service (multi-hop `via`)
- Availability: medium on the user-facing path (>=2 copies)
- Confidentiality: on any path carrying payment/ledger data
- Authentication: only where the system actually has a real auth service

6 rule types exist (+ Integrity, Authorization); those two aren't exercised
on the 7 real systems yet.

## Model verification

Every model re-checked against the cloned repo before trusting a finding:
24 missing units added, 14 wrong persistence flags fixed, 6 fake edges
removed, 31 real edges added, 2 port numbers corrected. None of this changed
a finding. Full counts: `FINDINGS.md` section 3.

Still a judgment call, not a read: which Compose host-port services count as
`external`, the `Domain`/`DataClass` tags, and the rubric itself.

## Finding verification

Every finding checked against the repo, `path:line` evidence in
`FINDINGS.md`. Four verdicts:
- **Confirmed** — true in the repo, no caveat
- **Partial** — exposure real, app has login on some routes
- **Model artifact** — true in the model, not a real weakness (login built
  into the app that the model can't express)
- **By design** — a real, intended path the rubric flags anyway

45 findings: 39 Confirmed, 4 Partial, 1 By design, 1 Model artifact. One
labeller (the author), no second opinion yet.

## What this doesn't measure

- Recall — only precision is checked, not what the tool misses
- Independent labelling — one person, no inter-rater check
- A baseline — no comparison against Checkov/KICS/etc. yet
- Scale beyond 7 — all hand-built, no automatic importer yet
- Zone spread — `Availability` is medium everywhere, not exercised anywhere here
- No synthetic examples — an earlier mutation-pair pilot was dropped; every
  number here is from a real, unmodified system

## Reproduce

```
cat tool/README.md                                    # build the tool
python3 scripts/reproduce.py /path/to/sam4c-cli.jar    # re-check everything
```
