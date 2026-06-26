#!/usr/bin/env python3
"""Generate manuscript figures for Passband-Controlled Quantum Error Correction."""
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.ticker import LogFormatterMathtext
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({"font.size": 9, "axes.linewidth": 0.8, "pdf.fonttype": 42, "ps.fonttype": 42})

def savefig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight")
    plt.close()

def fig1_signal_chain() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    def box(x, y, w, h, text):
        ax.add_patch(Rectangle((x, y), w, h, fill=False, linewidth=1.0))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center")
    def arrow(start, end, text=None):
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=10, linewidth=1.0))
        if text:
            mx, my = (start[0]+end[0])/2, (start[1]+end[1])/2
            ax.text(mx, my + 0.15, text, ha="center", va="bottom", fontsize=8)
    xs = [0.7, 3.0, 5.3, 7.6]
    labels = ["DFS input\nfilter", "Stabilizer\nlayer", "Decoder\nrouting", "Algorithm\nlayer"]
    metrics = ["qCMR,\nη, p₂q", "QNF$_{DFS}$", "QNF$_{stab}$", "$W_A,\\Delta_i$"]
    for x, lab, met in zip(xs, labels, metrics):
        box(x, 4.5, 1.55, 0.75, lab); box(x, 3.35, 1.55, 0.55, met)
        arrow((x + 0.775, 4.5), (x + 0.775, 3.9))
    for i in range(3):
        arrow((xs[i]+1.55, 4.875), (xs[i+1], 4.875))
    box(2.35, 1.9, 5.3, 0.8, "Passband controller\nengage / bypass / refresh / reweight / reroute")
    arrow((5.0, 3.35), (5.0, 2.7), "measured passband")
    ax.plot([2.35, 0.35, 0.35, 0.7], [2.3, 2.3, 4.875, 4.875], color="black", linewidth=1.0)
    ax.add_patch(FancyArrowPatch((0.35, 4.875), (0.7, 4.875), arrowstyle="->", mutation_scale=10, linewidth=1.0))
    ax.text(0.55, 3.0, "bypass", fontsize=8)
    ax.plot([7.65, 9.65, 9.65, 9.15], [2.3, 2.3, 4.875, 4.875], color="black", linewidth=1.0)
    ax.add_patch(FancyArrowPatch((9.65, 4.875), (9.15, 4.875), arrowstyle="->", mutation_scale=10, linewidth=1.0))
    ax.text(8.95, 3.0, "configure\nstack", fontsize=8, ha="center")
    box(1.0, 0.55, 2.1, 0.6, "Declared\nresource model")
    box(6.9, 0.55, 2.1, 0.6, "Matched-resource\nbaseline")
    arrow((3.1, 0.85), (6.9, 0.85)); arrow((7.95, 1.15), (6.0, 1.9))
    ax.set_title("Matched-resource QEC signal chain", fontsize=11)
    savefig("fig1_signal_chain")

def fig2_eta_threshold() -> None:
    df = pd.read_csv(DATA / "fig2_eta_threshold_curves.csv")
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(df["eta"], df["p_L_dfs_layer"], "-", color="black", label="dual-rail DFS layer")
    ax.plot(df["eta"], df["p_L_matched_d5"], "--", color="black", label="matched d=5 baseline")
    ax.plot(df["eta"], df["p_L_matched_d3"], "-.", color="black", label="matched d=3 baseline")
    ax.axvline(0.95, color="black", linestyle=":", linewidth=1.0)
    ax.text(0.952, 2.0e-3, "$\\eta$ threshold\n$\\approx 0.95$", fontsize=8)
    ax.set_yscale("log"); ax.set_xlim(0.50, 1.00); ax.set_ylim(1e-4, 1.1e-2)
    ax.set_xlabel("collectivity fraction $\\eta$"); ax.set_ylabel("logical error rate $p_L$")
    ax.text(0.72, 2.2e-4, "BYPASS"); ax.text(0.955, 2.2e-4, "ENGAGE")
    ax.legend(frameon=False, fontsize=8); savefig("fig2_eta_threshold")

def fig3_advantage_panels() -> None:
    df_a = pd.read_csv(DATA / "fig3a_advantage_vs_eta.csv")
    df_b = pd.read_csv(DATA / "fig3b_advantage_vs_p2q.csv")
    fig, axes = plt.subplots(2, 1, figsize=(6.3, 6.2))
    ax = axes[0]
    ax.plot(df_a["eta"], df_a.iloc[:, 1], color="black")
    ax.axhline(1.0, color="black", linestyle="--"); ax.axvline(0.95, color="black", linestyle=":")
    ax.set_xlim(0.70, 1.00); ax.set_ylim(0.0, 1.35)
    ax.set_xlabel("collectivity fraction $\\eta$ at $p_{2q}=0.005$")
    ax.set_ylabel("advantage ratio\n$p_L$(baseline)/$p_L$(layer)")
    ax.text(0.705, 1.08, "break-even", fontsize=8); ax.text(0.82, 0.20, "BYPASS region")
    ax.text(0.95, 0.55, "high gate error\nprevents advantage", fontsize=8)
    ax = axes[1]
    ax.plot(df_b["p2q"], df_b.iloc[:, 1], color="black")
    ax.axhline(1.0, color="black", linestyle="--"); ax.axvline(0.001, color="black", linestyle=":")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(1e-4, 1e-2); ax.set_ylim(0.08, 10)
    ax.set_xlabel("two-qubit gate error $p_{2q}$ at $\\eta=0.99$")
    ax.set_ylabel("advantage ratio\n$p_L$(baseline)/$p_L$(layer)")
    ax.text(1.12e-3, 0.11, "$p_{2q}$ threshold\n$\\approx 0.001$", fontsize=8)
    ax.text(1.6e-4, 2.5, "ENGAGE"); ax.text(3.0e-3, 0.22, "BYPASS")
    savefig("fig3_advantage_panels")

def fig4_hahn_echo() -> None:
    df = pd.read_csv(DATA / "fig4_echo_curves_pair_149_150_processed.csv")
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(df["tau_us"], df["single_rail_echo_a"], "-", color="black", label="single-rail echo a")
    ax.plot(df["tau_us"], df["single_rail_echo_b"], "--", color="black", label="single-rail echo b")
    ax.plot(df["tau_us"], df["encoded_dfs_echo"], "-.", color="black", label="encoded DFS echo")
    ax.plot(df["tau_us"], df["dfs_exit_fraction"], ":", color="black", linewidth=1.8, label="DFS-exit fraction")
    ax.set_xlim(0, 150); ax.set_ylim(0, 1.05)
    ax.set_xlabel("delay time $\\tau$ ($\\mu$s)"); ax.set_ylabel("normalized probability / fraction")
    ax.legend(frameon=False, fontsize=8); savefig("fig4_hahn_echo")

def fig5_eta_bars() -> None:
    df = pd.read_csv(DATA / "eta_table_ibm_kingston.csv")
    fig, ax = plt.subplots(figsize=(5.8, 3.8)); x = np.arange(len(df))
    ax.bar(x, df["eta"], width=0.55, facecolor="white", edgecolor="black", linewidth=1.2)
    ax.errorbar(x, df["eta"], yerr=df["sigma_eta"], fmt="none", color="black", capsize=3)
    ax.axhline(0.95, color="black", linestyle="--")
    ax.text(len(df)-0.55, 0.91, "DFS passband $\\eta\\geq 0.95$", fontsize=8, ha="right", bbox=dict(facecolor="white", edgecolor="none", pad=1))
    ax.set_xticks(x); ax.set_xticklabels(df["pair"], fontsize=8)
    ax.set_ylim(0, 1.05); ax.set_xlabel("qubit pair"); ax.set_ylabel("collectivity fraction $\\eta$")
    ax.text(0.1, 0.82, "All measured pairs\noutside passband", fontsize=8); savefig("fig5_eta_bars")

def fig6_qnf_map() -> None:
    eta = np.linspace(0.80, 0.999, 260); p2q = np.logspace(-4, -2, 260)
    E, P = np.meshgrid(eta, p2q)
    qnf = 10 ** (18.0 * (0.95 - E) + 0.75 * np.log10(P / 0.001))
    fig, ax = plt.subplots(figsize=(6.2, 4.5))
    ax.contourf(E, P, qnf, levels=[1e-6, 1.0, 1e6], colors=["white", "white"], hatches=["", "/"])
    contour = ax.contour(E, P, qnf, levels=[1.0], colors="black", linewidths=1.4)
    labels = ax.clabel(contour, fmt={1.0: "QNF = 1"}, fontsize=8, inline=True)
    for label in labels:
        label.set_bbox(dict(facecolor="white", edgecolor="none", pad=1))
    ax.axvline(0.95, color="black", linestyle=":"); ax.axhline(0.001, color="black", linestyle=":")
    ax.annotate("Heron r2 range\n$\\eta\\approx0.42$--$0.70$\noutside plotted range", xy=(0.802, 0.0020), xytext=(0.815, 4.5e-4), arrowprops=dict(arrowstyle="->", linewidth=0.8), fontsize=8)
    ax.plot([0.99], [0.0040], marker="o", color="black", markersize=4)
    ax.annotate("ion-trap-like\ngate-limited", xy=(0.99, 0.0040), xytext=(0.945, 0.0068), arrowprops=dict(arrowstyle="->", linewidth=0.8), fontsize=8)
    ax.plot([0.975], [0.00055], marker="o", color="black", markersize=4)
    ax.annotate("target\npassband", xy=(0.975, 0.00055), xytext=(0.93, 1.6e-4), arrowprops=dict(arrowstyle="->", linewidth=0.8), fontsize=8)
    ax.text(0.968, 2.8e-4, "ENGAGE\nQNF < 1", ha="center", fontsize=9)
    ax.text(0.84, 8.2e-3, "BYPASS\nQNF $\\geq$ 1", ha="center", va="center", fontsize=9, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.set_yscale("log"); ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.set_xlim(0.80, 1.00); ax.set_ylim(1e-4, 1e-2)
    ax.set_xlabel("collectivity fraction $\\eta$"); ax.set_ylabel("two-qubit gate error $p_{2q}$")
    savefig("fig6_qnf_map")

def main() -> None:
    fig1_signal_chain(); fig2_eta_threshold(); fig3_advantage_panels()
    fig4_hahn_echo(); fig5_eta_bars(); fig6_qnf_map()
    print(f"Figures written to {OUT}")

if __name__ == "__main__":
    main()
