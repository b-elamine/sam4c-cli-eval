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

## Modeling: from git to the two model files

Each system gets 2 files, built by hand, same way every time: `.arch.yaml`
(what the system looks like) and `.secdsl` (what it must satisfy).

**Building `.arch.yaml`** -- mechanical, read straight from the one
deployment file the repo actually ships:

1. **Every workload becomes a component.** Every Kubernetes
   `Deployment`/`StatefulSet`, or every Compose `service:` entry, becomes
   one component. A known database/cache/broker image (Postgres, Redis,
   RabbitMQ...) is tagged `Data`, everything else `App`.
2. **Is it reachable from outside?** `Service.type: LoadBalancer`/`NodePort`
   (Kubernetes) or a published host port (Compose) -> `external`. Anything
   else -> `internal`.
3. **Port and protocol.** The container port is a fact in the file; the
   protocol is inferred from what the image is known to speak (Postgres ->
   `tcp`, an HTTP service -> `http`).
4. **Who calls whom.** An env var or ConfigMap naming another service, or a
   Compose `depends_on`, becomes one connection. Only if the manifest says
   nothing about a call does the process fall back to reading that
   service's own source code.
5. **What image runs.** The `image:` field, copied as-is.
6. **Does the data survive a restart?** A PVC, `volumeClaimTemplate`,
   `hostPath`, or named Compose volume -> persistent. `emptyDir`, no
   volume, or an init-script-only mount -> not persistent.
7. **Where does it run.** The manifest never says which machine a pod ends
   up on, so every component is placed on one made-up placeholder host,
   the same one for the whole system.

**Building `.secdsl`** -- the only 2 steps that are judgment, not a read:

8. Tag each component with its business role (`Domain`) and, for stores,
   what kind of data it holds (`DataClass`). Nothing in a manifest says
   "this is the payment path" -- a person reads the system and decides.
9. Apply one fixed rubric (next section) to every system, using those tags,
   to write the actual rules.

Why it's built this way: one file only, never a merge of branches or a
hand-picked subset; no invented host layout, since the manifest has none;
Data vs App is decided by the image, not the name, since names lie; source
code is a fallback for calls only, never for anything else. Steps 8-9 are
named explicitly as judgment so the process isn't mistaken for fully
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
- **Confirmed** -- true in the repo, no caveat
- **Partial** -- exposure real, app has login on some routes
- **Model artifact** -- true in the model, not a real weakness (login built
  into the app that the model can't express)
- **By design** -- a real, intended path the rubric flags anyway

45 findings: 39 Confirmed, 4 Partial, 1 By design, 1 Model artifact. One
labeller (the author), no second opinion yet.

## What this doesn't measure

- Recall -- only precision is checked, not what the tool misses
- Independent labelling -- one person, no inter-rater check
- A baseline -- no comparison against Checkov/KICS/etc. yet
- Scale beyond 7 -- all hand-built, no automatic importer yet
- Zone spread -- `Availability` is medium everywhere, not exercised anywhere here
- No synthetic examples -- an earlier mutation-pair pilot was dropped; every
  number here is from a real, unmodified system

## Reproduce

```
cat tool/README.md                                    # build the tool
python3 scripts/reproduce.py /path/to/sam4c-cli.jar    # re-check everything
```
