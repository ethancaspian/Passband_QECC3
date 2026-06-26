# Passband-Controlled Quantum Error Correction — Reproducibility Repository

This repository supports the manuscript:

**Passband-Controlled Quantum Error Correction**  
Ethan A. Caspian, Independent Researcher  
Related patent disclosure: **U.S. Patent Application No. 19/717,655**,  
“Matched-Filter Control of Quantum Error Correction Layers Based on Measured Hardware Passbands.”

## Repository purpose

This is a curated reproducibility package. It contains:

- processed values used in the manuscript figures and tables,
- scripts to regenerate the main figures,
- simulation/plotting parameters for the QNF passband maps,
- helper routines for eta/qCMR calculation and echo-curve fitting,
- a clean paper-facing data availability statement.

It intentionally does **not** include private notebooks, USPTO materials, IDS trackers, raw cloud-account exports,
API tokens, or unfiled continuation ideas.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_figures.py
```

Outputs will be written to `figures/`.

## Data provenance and scope

The public CSV/JSON files in `data/processed/` are processed figure/table inputs corresponding to the manuscript.
Raw hardware execution records and additional calibration metadata are **not included** in this public package.
They may be provided by the author upon reasonable request, subject to hardware-provider terms, privacy review,
and removal of account/device metadata not needed for scientific reproduction.

The generated figures are intended to reproduce the manuscript-level plotted results and schematic passband maps.
Before journal submission, verify and, where available, replace processed curve files with final exported datasets
from the exact submitted manuscript.

## Main scientific quantities

- `eta = 1 - gamma_encoded/(gamma_a + gamma_b)`
- `qCMR = 10 log10(eta/(1-eta))`
- `QNF = p_L(with layer) / p_L(matched baseline)`

The layer is engaged when `QNF < 1` under the declared resource model and bypassed otherwise.

## Patent notice

See `NOTICE.md`. This repository is provided for research reproducibility only and should not be interpreted
as a grant of patent rights or a legal opinion.

## Contact

Ethan A. Caspian  
ORCID: https://orcid.org/0009-0008-7340-028X  
Website: https://www.earthurcaspian.com
