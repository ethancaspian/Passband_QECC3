# Repository Manifest

## Core files

- `README.md` — repository overview and quick start.
- `NOTICE.md` — patent and scope notice.
- `LICENSE.txt` — all-rights-reserved notice.
- `CITATION.cff` — citation metadata.
- `requirements.txt` / `environment.yml` — Python dependencies.

## Scripts

- `scripts/qecc3_passband.py` — eta/qCMR/QNF/passband decision helpers.
- `scripts/generate_figures.py` — regenerates manuscript figures.
- `scripts/fit_echo_curves.py` — fits processed echo curves and computes eta/qCMR.
- `scripts/simulate_qnf_map.py` — exports a QNF map grid from the manuscript-level model.

## Processed data

- `data/processed/eta_table_ibm_kingston.csv`
- `data/processed/qnf_map_parameters.json`
- `data/processed/fig2_eta_threshold_curves.csv`
- `data/processed/fig3a_advantage_vs_eta.csv`
- `data/processed/fig3b_advantage_vs_p2q.csv`
- `data/processed/fig4_echo_curves_pair_149_150_processed.csv`

## Private/raw data

- `data/raw_private_placeholder/README.md` — reminder not to publish raw private exports without review.
