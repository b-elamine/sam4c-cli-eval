# Results

2026-09-20 | tool `sam4c-cli` | test status: **28 / 28 pass** (`python3 private/run-all-tests.py`)

**45 findings on 7 real systems, 39 confirmed in the systems' own source. 12 of 12 mutation pairs detected, 11 of 11 checks tested.**

## 1. Setup

| | |
|---|---|
| Subjects | 7 public systems: 4 Kubernetes (Online Boutique, Bank of Anthos, Sock Shop, TeaStore), 3 Compose (OpenTelemetry Demo, Hotel Reservation, Social Network) |
| Ground truth | the systems' own deployment files (2026-07-31 versions) and service source code |
| Models | one architecture file + one rule file per system, every unit of the deployment files modeled |
| Rules | one rubric for all: the session or account store is reachable from the entry only through its own domain (multi-hop `Isolation` with `via`); `Availability medium` on the user-facing path; `Confidentiality` where the call graph carries payment or ledger data; `Authentication` and `Authorization` only where the system has them |
| Checks | 11 (3 always-on, 8 rule-dependent) |
| Baseline | none: no tool checks the design model before generation |
| Timing | median of 10 runs after 2 warm-up runs, JVM start-up included |

## 2. The 7 systems

| System | Format | Domain | Units | App | Data | Ext | Conn | Links | Rules | Findings | ms | MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BoA bank-of-anthos | K8s | banking | 9 | 7 | 2 | 1 | 13 | 25 | 5 | **5** | 340 | 96 |
| HR hotel-reservation | Compose | hospitality | 24 | 12 | 12 | 1 | 42 | 83 | 3 | **5** | 360 | 103 |
| OB online-boutique | K8s | e-commerce | 12 | 11 | 1 | 1 | 17 | 33 | 4 | **4** | 340 | 101 |
| OTel opentelemetry-demo | Compose | e-commerce | 20 | 18 | 2 | 1 | 49 | 97 | 4 | **5** | 335 | 102 |
| SN social-network | Compose | social | 27 | 14 | 13 | 2 | 48 | 94 | 3 | **15** | 340 | 104 |
| SS sock-shop | K8s | e-commerce | 14 | 9 | 5 | 1 | 16 | 31 | 4 | **8** | 330 | 101 |
| TS teastore | K8s | e-commerce | 7 | 6 | 1 | 1 | 14 | 27 | 3 | **3** | 325 | 95 |
| **Total** | 4 K8s / 3 Compose | 4 domains | **113** | 77 | 36 | 8 | 199 | 390 | **26** | **45** | | |

## 3. Findings per check and system

`–` = check not applicable (system has no rule of that type). `·` = checked, nothing found (this does not prove nothing is there).

| Check | CWE | BoA | HR | OB | OTel | SN | SS | TS | **Total** | Systems |
|---|---|---|---|---|---|---|---|---|---|---|
| Unauthenticated entry | CWE-306 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | **8** | 7/7 |
| Exposed data store | CWE-668 | · | · | · | · | · | · | · | **0** | 0/7 |
| Unintended exposure | CWE-668 | · | · | · | · | · | · | · | **0** | 0/7 |
| Isolation violated | CWE-923 | · | · | · | · | 1 | 1 | · | **2** | 2/7 |
| Plaintext channel | CWE-319 | 3 | – | 1 | 1 | – | 1 | – | **6** | 4/4 |
| Authentication bypass | CWE-306 | · | – | – | – | – | – | 1 | **1** | 1/2 |
| Insufficient replicas | none | 1 | 4 | 2 | 3 | 12 | 5 | 1 | **28** | 7/7 |
| No zone spread | none | – | – | – | – | – | – | – | **0** | 0/0 |
| Contradictory policy | none | · | · | · | · | · | · | · | **0** | 0/7 |
| Access w/o authn | CWE-306 | · | – | – | – | – | – | – | **0** | 0/1 |
| Vacuous resolution | none | · | · | · | · | · | · | · | **0** | 0/7 |
| **Total** | | **5** | **5** | **4** | **5** | **15** | **8** | **3** | **45** | |

## 4. Are the findings true? (each checked against the source)

C = confirmed | P = partial (exposure true, the app has a login on some routes) | D = by design (real path the app needs) | A = model artifact (true in the model, not in the app)

| Check | Total | C | P | D | A | Precision C | Precision C+P+D |
|---|---|---|---|---|---|---|---|
| Unauthenticated entry | 8 | 3 | 4 | 0 | 1 | 38% | 88% |
| Isolation violated | 2 | 1 | 0 | 1 | 0 | 50% | 100% |
| Plaintext channel | 6 | 6 | 0 | 0 | 0 | 100% | 100% |
| Authentication bypass | 1 | 1 | 0 | 0 | 0 | 100% | 100% |
| Insufficient replicas | 28 | 28 | 0 | 0 | 0 | 100% | 100% |
| **All** | **45** | **39** | 4 | 1 | 1 | **87%** | **98%** |

Every finding with its `path:line` evidence: `findings-explained.md`.

## 5. Mutation pilot (each pair differs by one architectural fact)

| Pair | Fault | Intended check | Vulnerable | Fixed |
|---|---|---|---|---|
| c1 | one replica, one zone | replicas, zone spread | flagged (2) | clean |
| c2 | shared connector between isolated sides | isolation | flagged (1) | clean |
| c3 | external component, no authentication | unauthenticated entry | flagged (1) | clean |
| c4 | data store exposed externally | exposed data store | flagged (2) | clean |
| c5 | declared internal, wired external | unintended exposure | flagged (1) | clean |
| c6 | authorization on an unauthenticated resource | access without authn | flagged (1) | clean |
| c7 | isolation and confidentiality on the same pair | contradictory policy | flagged (1) | clean |
| c8 | path that bypasses the approved mediator | isolation (via) | flagged (1) | clean |
| c9 | target does not verify the token, path bypasses the authenticator | authentication bypass | flagged (1) | clean |
| c10 | http on a confidential channel | plaintext channel | flagged (1) | clean |
| c11 | multi-hop path through an exposed unauthenticated component | isolation (weak-hop chain) | flagged (2) | clean |
| c12 | context that matches no component | vacuous resolution | flagged (2) | clean |
| **Result** | | **11 / 11 checks** | **12/12 flagged** | **12/12 clean** |

## 6. Models checked against the repos

| System | Units in repo = modeled | Edges: deployment file / service code / config | Corrected in the models |
|---|---|---|---|
| BoA | 9 | 11 / 1 / 0 = 12 | +1 unit, +1 edge, 2 persistence flags, credentials |
| HR | 24 | 22 / 9 / 10 = 41 | +9 units, +10 edges |
| OB | 12 | 16 / 0 / 0 = 16 | +1 unit, 1 port |
| OTel | 20 | 48 / 0 / 0 = 48 | +5 units, 1 persistence flag |
| SN | 27 | 13 / 27 / 6 = 46 | +8 units, 6 flags, -5 / +14 edges, 1 port |
| SS | 14 | 2 / 13 / 0 = 15 | 4 flags, -1 / +3 edges |
| TS | 7 | 6 / 7 / 0 = 13 | 1 flag, +3 edges |
| **Total** | **113** | **118 / 57 / 16 = 191** | 24 units, 14 flags, 6 edges removed, 31 added, 2 ports |

## 7. Reproduce

This file lived inside the sam4c-cli repo originally; the commands below are
from that context. From this evaluation folder, use
`python3 scripts/reproduce.py <path-to-jar>` instead (see the top-level
README.md).

```
mvn -q -DskipTests package                       # build, from the sam4c-cli repo
python3 private/run-all-tests.py                # 28 tests, from the sam4c-cli repo
java -jar target/sam4c-cli.jar --validate private/case-study/<system>.arch.yaml private/case-study/<system>.secdsl
```

## 8. Limits

- Findings were checked by the author, not an independent labeller. Recall on real systems is not measured.
- Multi-hop `Isolation` with `via` is used on all 7 real systems (2 findings, 5 silent). Weak-hop chaining (no `via`) is tested by the pilot only.
- `Availability medium` everywhere, so zone spread is exercised by the pilot only.