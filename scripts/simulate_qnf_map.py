#!/usr/bin/env python3
"""Export a QNF passband map grid from the manuscript-level model."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

def main():
    eta = np.linspace(0.80, 0.999, 260)
    p2q = np.logspace(-4, -2, 260)
    rows = []
    for e in eta:
        for p in p2q:
            qnf = 10 ** (18.0 * (0.95 - e) + 0.75 * np.log10(p / 0.001))
            rows.append({"eta": e, "p2q": p, "qnf": qnf, "region": "ENGAGE" if qnf < 1 else "BYPASS"})
    path = OUT / "fig6_qnf_map_grid.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Wrote {path}")

if __name__ == "__main__":
    main()
