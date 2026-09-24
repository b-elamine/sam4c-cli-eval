# CVE / threat corpus and coverage numbers

Grounded in recognized sources so selection is systematic, not cherry-picked:
- CWE weakness classes,
- MITRE ATT&CK for Containers / Cloud,
- CIS Kubernetes and cloud Benchmarks,
- OWASP Kubernetes / Cloud-Native Top 10,
- concrete CVE instances from NVD (filter: cloud / k8s / container by CWE).

Organized **by weakness class** (the level our checks operate at). Each class lists representative
CVEs / incidents / benchmark controls, the architectural weakness, our check, and the outcome.
The chain is CVE -> CWE -> our check; one check covers many CVEs of the same class.

> Caveat: exact CVE ids and incident details are from memory and MUST be verified against NVD and
> primary reports before the paper. Entries marked "(pattern)" are recognized misconfiguration
> patterns (CIS/ATT&CK/incidents) rather than a single CVE. Mapping is a judgment - use a second rater.

Outcome: **prevented** (a check flags it, runnable case exists) / **gap** (architectural but the
check/property is not built) / **out-of-scope** (code/runtime/library, not a design weakness).

---

## In-scope, PREVENTED by design

### Class P1 - Missing authentication on an exposed surface (CWE-306). Check: missing-auth. Case c3.
- Tesla Kubernetes dashboard, internet-exposed, no auth, cryptojacking (2018)
- Kubernetes Dashboard exposed without auth (pattern, multiple incidents)
- Docker Engine API on tcp/2375 with no TLS/auth, cryptojacking campaigns (pattern)
- etcd exposed on :2379 without auth (pattern; CIS K8s control)
- Kubelet API :10250 / read-only :10255 unauthenticated (pattern)
- Exposed CI servers (Jenkins) with no auth (pattern)
- CVE-2018-1002105 (K8s API server, unauth request reaches backends)

### Class P2 - Stateful datastore exposed to the external sphere (CWE-668/200). Check: exposed-data. Case c4.
- MongoDB ransacking, tens of thousands no-auth internet-exposed (2017)
- Exposed Elasticsearch / Kibana clusters leaking data (pattern)
- Redis bound to a public interface, default no-auth (pattern)
- CouchDB / Cassandra / Hadoop HDFS exposed (pattern)
- Public S3 buckets (Accenture, Verizon, Booz Allen and many others) (pattern, CWE-668)
- Public Azure Blob / GCS buckets (pattern)
- RDS / managed DB made publicly accessible (pattern; CIS control)

### Class P3 - Accidental external exposure / over-broad network (CWE-668). Check: accidental-exposure. Case c5.
- Security group / firewall rule 0.0.0.0/0 on an internal resource (CIS control)
- Memcached UDP reachable from the internet, amplification DDoS (2018)
- Internal service inadvertently behind a public ingress / LoadBalancer / NodePort (pattern)
- Missing Kubernetes NetworkPolicy (default allow-all) (CIS control)

### Class P4 - No isolation between tiers (CWE-668/284). Check: Isolation. Case c2.
- Flat network: a sensitive DB reachable from the frontend / DMZ (pattern)
- Missing NetworkPolicy enabling lateral movement after a pod compromise (ATT&CK: Lateral Movement)
- Shared connector between trust zones that a rule requires isolated (design)

### Class P5 - Resource exhaustion / DoS / EDoS (CWE-400). Check: Availability. Case c1.
- HTTP/2 flood family (CVE-2019-9512 Ping Flood, CVE-2019-9514 Reset Flood, CVE-2019-9518)
- CVE-2019-11253 (Kubernetes API "YAML bomb" / billion-laughs DoS)
- Single-replica service with no PodDisruptionBudget -> outage on node loss (CIS control)
- Autoscaling / EDoS billing exhaustion (pattern)

### Class P6 - Broken access control: access without authentication (CWE-862). Check: authz-without-authn. Case c6.
- Resource reachable/usable with no authentication in front of it (pattern)
- Anonymous access enabled (e.g. anonymous-auth, system:anonymous bindings) (CIS control)
- Default service-account token mounted and usable (CIS control)

### Class P7 - Contradictory / inconsistent policy (consistency). Check: Isolation-vs-communication. Case c7.
- Declaring Isolation and a communication requirement over the same pair (design error)

---

## In-scope, GAP (architectural, but the check/property is not built yet)

### Class G1 - Over-permissive / least-privilege IAM (CWE-269). Needs least-privilege modeling.
- Capital One 2019 (over-permissive IAM role reached via SSRF; the SSRF itself is out-of-scope)
- IAM wildcard policies ("Action: *", "Resource: *") (CIS control)
- Over-privileged Kubernetes service accounts / cluster-admin bindings (CIS control)

### Class G2 - Improper authorization scope (CWE-863). Needs finer-grained RBAC-scope modeling.
- CVE-2019-11247 (namespaced resource served at cluster scope)
- Privilege escalation through over-broad RBAC verbs (pattern)

### Class G3 - Channel confidentiality / integrity (CWE-319/300). Needs model-level Confidentiality.
- CVE-2020-8554 (K8s external-IP / LoadBalancer MITM)
- Missing TLS on service-to-service or ingress traffic (CIS control)
- etcd peer/client traffic unencrypted (CIS control)

### Class G4 - Secrets management (CWE-312/798). Needs a secrets-hygiene check.
- Hardcoded credentials in ConfigMaps / env vars (pattern)
- Secrets committed to git / images (pattern)
- Kubernetes Secrets unencrypted at rest (CIS control)

### Class G5 - Data residency / privacy (privacy / compliance). Needs the DataResidency property.
- Data stored or processed in a disallowed region (GDPR) (pattern)
- Cross-border data transfer constraints (pattern)

### Class G6 - Supply chain / image integrity (CWE-1357/1395). Needs ImageIntegrity (delegates to a scanner).
- Unpinned / :latest images (CIS control)
- Vulnerable base image / known-vulnerable dependency (pattern; e.g. shipping a Log4Shell jar)
- Unsigned or typosquatted images (pattern)

---

## Out-of-scope (code / runtime / library; define the threat-model boundary)

### Class O1 - Container-runtime and kernel escapes
- CVE-2019-5736 (runc host-binary overwrite escape)
- CVE-2022-0847 (Dirty Pipe), CVE-2022-0185 (kernel) - host kernel escapes

### Class O2 - Vulnerable libraries / application code
- CVE-2021-44228 (Log4Shell), CVE-2014-0160 (Heartbleed), Shellshock - code/library flaws

### Class O3 - Runtime file/volume handling
- CVE-2021-25741 (kubelet symlink hostPath), CVE-2017-1002101 (subpath) - runtime defects

---

## Numbers (provisional, pending NVD verification)

- Weakness classes: **13 in-scope** (P1-P7 prevented, G1-G6 gap) + **3 out-of-scope** (O1-O3) = 16.
- Representative CVEs / incidents / benchmark controls: **~45** across these classes.
- **Coverage of in-scope classes: 7 of 13 prevented by design (54%)**, each with a runnable
  vuln+fixed case (c1-c7); 6 are gaps with identified properties to add.
- By representative-instance count, the prevented classes (P1-P7) cover the large majority of the
  documented cloud *misconfiguration* instances in the corpus; the gaps cluster in
  least-privilege, channel encryption, secrets, residency, and supply chain.

Two ways to report N, both honest:
- **by class:** "13 in-scope weakness classes; 7 prevented by design, 6 future work; 3 out of scope."
- **by instance:** "~45 documented CVEs/incidents/controls; the prevented classes account for the
  majority of the misconfiguration instances."

Headline (count-based, no fake accuracy):
> "We assemble a corpus from CWE, the CIS Kubernetes Benchmark, MITRE ATT&CK for Containers, and
> NVD, spanning 13 in-scope architectural weakness classes (about 45 documented CVEs/incidents/
> controls). The model prevents 7 classes by design, each demonstrated by a design it flags and a
> corrected design it clears; the remaining 6 are future work, and code-level vulnerability classes
> are out of scope, defining the boundary of a design-level approach."

## To do before the paper
- Verify every CVE id / CWE / control against NVD, CIS, ATT&CK, and primary incident reports.
- Fix and state the selection protocol (which CWE ids, which CIS section, which ATT&CK matrix,
  which NVD window) so selection is reproducible.
- Second-rater classification on a sample; report inter-rater agreement.
- Optionally implement DataResidency or model-level Confidentiality to move a gap class to prevented.
