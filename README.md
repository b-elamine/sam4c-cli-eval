# SAM4C-derived tool: evaluation on 7 real cloud-native systems

This folder is a standalone, reproducible record of one evaluation: modeling
7 real open-source cloud applications, running the tool's checks against
them, and verifying every finding against the systems' own source code.

It is separate from the tool's source repo and from the paper repo on
purpose, so it can be shared, archived, or made public on its own.

## Quickstart

```
# 1. build the tool at the pinned commit
cat tool/README.md

# 2. reproduce every number in RESULTS.md
python3 scripts/reproduce.py /path/to/sam4c-cli.jar
```

Expect `28/28 checks passed`.

## Where everything is

| Path | What it is |
|---|---|
| `README.md` | this page |
| `METHODOLOGY.md` | how the systems were picked, modeled, verified, and how findings were checked — detailed enough to redo |
| `RESULTS.md` | every summary table: systems, findings per check, verdicts, model-check counts |
| `FINDINGS.md` | all 45 findings, one row each, with the `path:line` evidence in the real repo and a verdict |
| `model-inventory.md` | every modeled component, one row each |
| `real-systems/inputs/` | the 7 `.arch.yaml` + `.secdsl` model pairs (the tool's input) |
| `real-systems/inputs/manifests/` | the ground-truth deployment file each model was built from, vendored verbatim at its real repo path |
| `real-systems/inputs/evidence/` | the service source files cited as finding evidence, vendored verbatim at their real repo path |
| `real-systems/outputs/` | the tool's raw JSON output per system (the tool's output) |
| `tool-validation-pilot/` | 12 hand-built vulnerable/fixed pairs used to sanity-check the tool's mechanics, kept separate from the real-system results |
| `eval-tables/` | the same results as paper-ready LaTeX tables (tex/pdf/png) |
| `tool/README.md` | the exact tool commit this evaluation was run against, and how to build it |
| `scripts/reproduce.py` | one command that rebuilds every number in `RESULTS.md` from the inputs |
| `scripts/run-all-tests.py` | the original regression runner, kept for reference (assumes the sam4c-cli repo layout; `reproduce.py` is the version to use here) |

## Headline numbers

| | |
|---|---|
| Systems modeled | 7 (113 deployables, 199 connectors, 390 links, 26 rules) |
| Findings | 45, on real default configurations, none injected |
| Confirmed in source | 39 of 45 (87%); 44 of 45 (98%) are real facts about the design |
| Mutation pilot | 12 of 12 flagged, 12 of 12 clean, all 11 checks covered |
| Reproduce check | 28 of 28 pass (`scripts/reproduce.py`) |

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

## What this is not

This folder does not include a baseline comparison against existing
scanners, an independent second labeller, or a measurement of recall. These
are stated as open items in `METHODOLOGY.md`, section 8, not hidden.

## Provenance

Built from `sam4c-cli` at commit `9850fbd564c0e9db9504627f53f99ce12268a978`
(`git@github.com:b-elamine/S4CLI.git`). All 7 repos were cloned and checked
out at the commit recorded per-system in `FINDINGS.md`, section 1.
