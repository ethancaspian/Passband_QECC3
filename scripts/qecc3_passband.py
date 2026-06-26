#!/usr/bin/env python3
"""Core utilities for passband-controlled QEC figure reproduction."""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class PassbandThresholds:
    eta_threshold: float = 0.95
    p2q_threshold: float = 0.001
    leakage_threshold: float = 0.05
    confidence_multiplier: float = 1.0

def collectivity_fraction(T2_single_a: float, T2_single_b: float, T2_encoded: float) -> float:
    """Compute eta = 1 - gamma_encoded/(gamma_a + gamma_b)."""
    if T2_single_a <= 0 or T2_single_b <= 0 or T2_encoded <= 0:
        raise ValueError("All T2 values must be positive.")
    gamma_a = 1.0 / T2_single_a
    gamma_b = 1.0 / T2_single_b
    gamma_encoded = 1.0 / T2_encoded
    return 1.0 - gamma_encoded / (gamma_a + gamma_b)

def qcmr_db(eta: float, eps: float = 1e-12) -> float:
    """Rate-domain qCMR = 10 log10(eta/(1-eta)) in dB, clipped for reporting."""
    eta_clipped = min(max(eta, eps), 1.0 - eps)
    return 10.0 * math.log10(eta_clipped / (1.0 - eta_clipped))

def qnf_from_log_model(eta: float, p2q: float) -> float:
    """
    Manuscript-level passband map model used for the plotted contour.
    Replace this function with exported circuit-level simulation data if available.
    """
    if p2q <= 0:
        raise ValueError("p2q must be positive.")
    log10_qnf = 18.0 * (0.95 - eta) + 0.75 * math.log10(p2q / 0.001)
    return 10.0 ** log10_qnf

Decision = Literal["ENGAGE_DFS", "BYPASS_DFS", "REFRESH_BLOCK"]

def passband_decision(
    eta: float,
    sigma_eta: float,
    p2q: float,
    dfs_exit_fraction: float,
    thresholds: PassbandThresholds = PassbandThresholds(),
) -> Decision:
    """Three-gate DFS passband decision."""
    if eta <= 0:
        return "BYPASS_DFS"
    lower_eta = eta - thresholds.confidence_multiplier * sigma_eta
    if lower_eta < thresholds.eta_threshold:
        return "BYPASS_DFS"
    if p2q > thresholds.p2q_threshold:
        return "BYPASS_DFS"
    if dfs_exit_fraction > thresholds.leakage_threshold:
        return "REFRESH_BLOCK"
    return "ENGAGE_DFS"
