# Methodology

How this evaluation was designed and run, in enough detail to redo it. Every
step below is also enforced by `scripts/reproduce.py`, which regenerates the
finding counts from the inputs and checks them against `RESULTS.md`.

## 1. Goal

Check whether design-time architecture/security checks find real, source-
confirmed weaknesses in real cloud-native systems, running against their
public default configuration, with no synthetic examples and no injected
faults.

## 2. System selection

Seven public, actively used reference/demo cloud-native applications, chosen
for:
- **Domain spread**: e-commerce (Online Boutique, Sock Shop, TeaStore),
  banking (Bank of Anthos), observability (OpenTelemetry Demo), hospitality
  (Hotel Reservation), social networking (Social Network).
- **Platform spread**: 4 on Kubernetes, 3 on Docker Compose.
- **Public, inspectable source**: every system's deployment manifest and
  service source code is public, so every finding can be checked against a
  line of code, not just trusted.
- **No cherry-picking on findings**: systems were modeled from their
  deployment file before any check was run against them.

No production or proprietary systems, no systems modified to contain a known
CVE for this evaluation (that is a separate, smaller pilot, see section 6).

## 3. Modeling protocol: from git to the two model files

Each system becomes one `.arch.yaml` (architecture) and one `.secdsl`
(security rules), built with the same ten steps for all seven systems. This
is a manual process; step 9 and part of step 10 are judgment calls, everything
else is a direct read of the repo.

| Step | Source in git | What it becomes in the model |
|---|---|---|
| 1 | One ground-truth deployment file per system (the Kubernetes manifest or `docker-compose.yml` actually shipped in the repo) | one `Architecture` named after the system |
| 2 | Nothing — manifests do not say which machine runs a pod | one `Worker` host (the cluster or compose host); every deployable's `deployedOn` points at it |
| 3 | Every Kubernetes Deployment/StatefulSet, every Compose service | one `Deployable` each: `Data` if the image is a database, cache or broker (mongo, postgres, mariadb, redis, memcached, rabbitmq), else `App` |
| 4 | Kubernetes `Service.type` (LoadBalancer/NodePort), Compose `ports:` | `exposure: external` only for the system's intended public entry point; everything else `internal` (Compose dev-UI host-port mappings, e.g. jaeger, consul, flagd-ui, stay `internal`, noted in the model header) |
| 5 | `containerPort`, Compose `ports`, the known protocol of the image | one `Port` per endpoint, with number and protocol (`http`, `grpc`, `tcp` for databases/Thrift, `udp` for the jaeger agent) |
| 6 | Env vars/ConfigMaps naming another service, Compose `depends_on`, then the service source code where the manifest is silent | one `Connector` per directed call, one outbound `Link` on the caller, one inbound `Link` on the callee |
| 7 | `image:` | one `Implementation` per deployable |
| 8 | Volumes | `persistent: true` only if the data volume outlives the pod (PVC, `volumeClaimTemplate`, `hostPath`, named Compose volume); `emptyDir`, no volume, or an init-script-only mount is not persistent |
| 9 | The author, reading the system | `Domain` attribute (business role) and `DataClass` on sensitive stores — the first judgment call |
| 10 | The author, one rubric applied identically to all 7 (see section 4) | the `.secdsl` rule set |

Full worked example (Online Boutique `frontend`): the Service
`frontend-external` is `type: LoadBalancer`, so `exposure: external`; the
Deployment's `containerPort: 8080` becomes port `http_in`; env vars like
`PRODUCT_CATALOG_SERVICE_ADDR` become one connector each; no `replicas:`
field, so the tool counts one copy by Kubernetes' own default.

## 4. Rule authoring: one rubric, applied to all 7

The same policy template is instantiated per system, using each system's own
`Domain`/`DataClass` tags (step 9 above) as the attribute vocabulary — no
component is ever named directly in a rule:

- **Isolation**: the session or account store must be reachable from the
  public entry only through its own owning service (the multi-hop `via`
  form).
- **Availability**: `medium` on every component on the user-facing path (at
  least 2 copies).
- **Confidentiality**: on every path the call graph shows carrying payment or
  ledger data.
- **Authentication**: only on systems that actually have a real
  authentication service, targeting the components that must sit behind it.

Six rule types exist in the DSL (Confidentiality, Integrity, Isolation,
Authentication, Authorization, Availability); Integrity and Authorization are
not exercised on the 7 real systems in this run (open item, see section 7).

## 5. Model verification: is each model actually right?

Before any finding is trusted, every model was independently re-checked
against the cloned repo it came from:

- **Units**: every Deployment/StatefulSet/Compose service in the manifest
  must appear in the model, and nothing else. First-pass models had 24
  missing units; all added.
- **Persistence flags**: every `persistent: true`/`false` was checked against
  the actual volume declaration. 14 were wrong and fixed.
- **Edges**: every connector was checked against an env var, ConfigMap,
  `depends_on`, or a direct read of the service source code when the
  manifest was silent. 6 edges that did not exist in code were removed, 31
  real edges that were missing were added.
- **Exposure and ports**: the intended public entry point and its port
  numbers were checked against the `Service`/`ports:` declarations. 2 port
  numbers were corrected to match the real container port.

None of these corrections changed a finding (the errors were in unrelated
parts of the model). Full per-system counts and the exact list of
corrections are in `FINDINGS.md`, section 3.

What stays a judgment call, not a read: which host-port services on the 3
Compose systems count as `external` (Compose maps dev-tool ports too), the
`Domain`/`DataClass` tags, and the rubric itself.

## 6. Finding verification: is each finding true?

Every finding the tool produced was checked against the cloned repo, one
`path:line` citation per finding, recorded in `FINDINGS.md`. Four verdicts:

- **Confirmed**: the fact is true in the repo, no caveat.
- **Partial**: the exposure is real, but the app has a login on some routes
  (the tool's unauthenticated-entry check cannot see login logic built into
  the entry point itself, since it has no rule to attach to).
- **Model artifact**: true in the model, not a real weakness (one case:
  Bank of Anthos's frontend does redirect to a login page in application
  code, which the model has no way to express).
- **By design**: a real, intended path that the rubric flags because the
  rubric's mediator list does not include it (Sock Shop's front-end
  legitimately talks to its own session store).

Result: 45 findings, 39 Confirmed, 4 Partial, 1 By design, 1 Model artifact.
The labelling was done by one person (the tool's author) reading the source;
there is no second, independent labeller yet (see section 7).

## 7. Tool validation: the mutation pilot

Separately from the 7 real systems, `tool-validation-pilot/` holds 12
hand-built vulnerable/fixed model pairs, one per check family, each pair
differing by exactly one fact (`c1`..`c12`, see
`tool-validation-pilot/methodology.md`). Each pair checks that the tool
fires on the fault and stays silent on the fix. This is a sanity check on
the tool's mechanics, not part of the real-system evidence, and is kept in
a separate folder so the two are never mixed in a results table.

## 8. What this evaluation does not measure (state plainly)

- **Recall.** Only precision is measured (of what the tool reports, how much
  is true). Nothing here measures what the tool misses.
- **Independent labelling.** One person checked all 45 findings; no
  inter-rater agreement is computed.
- **A baseline.** No comparison against an existing config scanner
  (Checkov, KICS, kube-linter, etc.) is included in this folder yet.
- **Scale beyond 7.** All 7 models are hand-built; nothing here validates an
  automatic importer at larger scale.
- **Zone spread.** `Availability` is `medium` everywhere, so the
  zone-spread half of the Availability check is exercised by the pilot only,
  not by any of the 7 real systems.

## 9. Reproducing this evaluation

See `README.md` for the exact commands. In short: build the tool at the
pinned commit (`tool/README.md`), then run
`python3 scripts/reproduce.py <path-to-jar>` from this folder's root. It
re-derives every finding count in `RESULTS.md` from `real-systems/inputs/`
and re-checks all 12 pilot pairs, and exits non-zero if anything drifts.
