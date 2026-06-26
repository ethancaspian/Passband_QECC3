#!/usr/bin/env python3
"""Fit processed echo curves and compute eta/qCMR."""
from __future__ import annotations
from pathlib import Path
import math
import pandas as pd
from scipy.optimize import curve_fit
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"

def exp_decay(t, A, T2, C):
    return A * np.exp(-t / T2) + C

def fit_t2(t, y):
    p0 = [max(y) - min(y), 75.0, min(y)]
    popt, pcov = curve_fit(exp_decay, t, y, p0=p0, maxfev=10000)
    return popt[1]

def qcmr_db(eta):
    eta = min(max(float(eta), 1e-12), 1 - 1e-12)
    return 10 * math.log10(eta / (1 - eta))

def main():
    df = pd.read_csv(DATA / "fig4_echo_curves_pair_149_150_processed.csv")
    t = df["tau_us"].values
    T2a = fit_t2(t, df["single_rail_echo_a"].values)
    T2b = fit_t2(t, df["single_rail_echo_b"].values)
    T2e = fit_t2(t, df["encoded_dfs_echo"].values)
    eta = 1 - (1/T2e) / ((1/T2a) + (1/T2b))
    print(f"T2_single_a = {T2a:.3f} us")
    print(f"T2_single_b = {T2b:.3f} us")
    print(f"T2_encoded  = {T2e:.3f} us")
    print(f"eta         = {eta:.4f}")
    print(f"qCMR        = {qcmr_db(eta):.2f} dB")

if __name__ == "__main__":
    main()
