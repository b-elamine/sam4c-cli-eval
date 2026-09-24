# Evaluation: 7 real cloud-native systems

7 real apps, modeled by hand, checked with the tool, every finding checked
against the real source. Standalone, separate from the tool repo and the paper.

## Run it

```
cat tool/README.md
python3 scripts/reproduce.py /path/to/sam4c-cli.jar
```
`15/15 checks passed` if it's all good.

## What's here

- `METHODOLOGY.md` -- how it was built
- `RESULTS.md` -- the numbers
- `FINDINGS.md` -- all 45 findings, evidence + verdict
- `model-inventory.md` -- every component
- `real-systems/inputs/` -- the models, manifests, evidence (tool input)
- `real-systems/outputs/` -- the tool's raw findings
- `tool/README.md` -- pinned tool version
- `scripts/reproduce.py` -- the only script, redoes everything

## Numbers

45 findings, 7 systems, 39 confirmed in source. Not here yet: baseline,
second labeller, recall -- see `METHODOLOGY.md`.
