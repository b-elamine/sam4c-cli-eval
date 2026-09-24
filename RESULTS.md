# Results

Tool version: `tool/README.md`. Test status: **15 / 15 pass** (`python3 scripts/reproduce.py <path-to-jar>`)

**45 findings on 7 real systems, 39 confirmed in the systems' own source, none injected.**

## 1. Setup

| | |
|---|---|
| Subjects | 7 public systems: 4 Kubernetes (Online Boutique, Bank of Anthos, Sock Shop, TeaStore), 3 Compose (OpenTelemetry Demo, Hotel Reservation, Social Network) |
| Ground truth | the systems' own deployment files + service source code |
| Models | 1 arch file + 1 rule file per system, every unit modeled |
| Rules | one rubric for all 7, see `METHODOLOGY.md` |
| Checks | 11 (3 always-on, 8 rule-dependent) |
| Baseline | none yet |
| Timing | median of 10 runs, 2 warm-ups, JVM start-up included |

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

"All" row, how it's computed (pooled, not an average of the 5 rows above):
```
Precision C     = (3+1+6+1+28) / (8+2+6+1+28) = 39/45 = 87%
Precision C+P+D = (7+2+6+1+28) / (8+2+6+1+28) = 44/45 = 98%
```
For comparison, simple average of the 5 per-check % (38,50,100,100,100)/5 = 78% --
lower, because "Insufficient replicas" alone is 28/45 findings and pulls the
pooled number up.

Every finding with its `path:line` evidence: `FINDINGS.md`.

## 5. Reproduce

```
cat tool/README.md                                       # build the tool at the pinned commit
python3 scripts/reproduce.py /path/to/sam4c-cli.jar       # 15 checks, from this folder's root
```

Limits: see `METHODOLOGY.md`.