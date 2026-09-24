# Evaluation: 7 real cloud-native systems

Modeled 7 real open-source apps, ran the tool's checks, verified every
finding against the systems' own source. Standalone folder, separate from
the tool repo and the paper, so it can be shared on its own.

## Run it

```
cat tool/README.md                                     # build the tool
python3 scripts/reproduce.py /path/to/sam4c-cli.jar     # re-check everything
```
Expect `15/15 checks passed`.

## Where everything is

| Path | What it is |
|---|---|
| `METHODOLOGY.md` | how systems were picked, modeled, verified |
| `RESULTS.md` | summary tables |
| `FINDINGS.md` | all 45 findings, one row each, `path:line` evidence + verdict |
| `model-inventory.md` | every modeled component |
| `real-systems/inputs/` | the 7 `.arch.yaml` + `.secdsl` pairs (tool input) |
| `real-systems/inputs/manifests/` | ground-truth deployment files, real repo paths |
| `real-systems/inputs/evidence/` | source files cited as finding evidence, real repo paths |
| `real-systems/outputs/` | the tool's raw JSON output per system |
| `eval-tables/` | same results as LaTeX tables, static export |
| `tool/README.md` | pinned tool commit + build steps |
| `scripts/reproduce.py` | the only script, rebuilds every number above |

## Headline numbers

| | |
|---|---|
| Systems modeled | 7 (113 deployables, 199 connectors, 390 links, 26 rules) |
| Findings | 45, real default configs, none injected |
| Confirmed in source | 39 of 45 (87%); 44 of 45 (98%) are real facts |
| Reproduce check | 15 of 15 pass |

## The 7 systems

| System | Domain | Platform |
|---|---|---|
| Online Boutique | e-commerce | Kubernetes |
| Bank of Anthos | banking | Kubernetes |
| Sock Shop | e-commerce | Kubernetes |
| TeaStore | e-commerce | Kubernetes |
| OpenTelemetry Demo | observability | Kubernetes |
| Hotel Reservation | hospitality | Docker Compose |
| Social Network | social | Docker Compose |

## Not here yet

Baseline comparison, second labeller, recall. See `METHODOLOGY.md`.

## Provenance

`sam4c-cli` at `9850fbd564c0e9db9504627f53f99ce12268a978`
(`git@github.com:b-elamine/S4CLI.git`). Per-system repo/commit: `FINDINGS.md` section 1.
