"""
Mechanistic analysis: linking geometry to biological programs.

This module tests which biological programs best explain the
geometric structure of the fan-out (dispersion, pseudotime position,
transitional-state occupancy).
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.mechanism")

try:
    import numpy as np
    import pandas as pd
    from scipy import stats as sp_stats
except ImportError:
    pass


def program_geometry_linkage(
    adata, cfg: dict, rep_key: str = "X_pca"
) -> "pd.DataFrame":
    """Test which programs correlate with geometric properties.

    For each program score, compute:
    - Spearman rho with distance from healthy centroid
    - Spearman rho with pseudotime
    - Spearman rho with local dispersion (distance to k-NN centroid)
    """
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    rep = adata.obsm[rep_key]

    healthy_mask = adata.obs[condition_col].values == healthy_label
    h_centroid = rep[healthy_mask].mean(axis=0)
    dist_to_healthy = np.linalg.norm(rep - h_centroid, axis=1)

    prog_cols = [c for c in adata.obs.columns if c.startswith("score_") or c.startswith("program_")]
    results = []

    for col in prog_cols:
        prog_name = col.replace("score_", "").replace("program_", "")
        vals = adata.obs[col].values
        mask = ~np.isnan(vals)

        rec = {"program": prog_name}

        rho, p = sp_stats.spearmanr(vals[mask], dist_to_healthy[mask])
        rec["rho_dist_to_healthy"] = float(rho)
        rec["p_dist_to_healthy"] = float(p)

        if "dpt_pseudotime" in adata.obs.columns:
            pt = adata.obs["dpt_pseudotime"].values
            pt_mask = mask & ~np.isnan(pt)
            rho_pt, p_pt = sp_stats.spearmanr(vals[pt_mask], pt[pt_mask])
            rec["rho_pseudotime"] = float(rho_pt)
            rec["p_pseudotime"] = float(p_pt)

        results.append(rec)

    return pd.DataFrame(results)


def repair_stall_analysis(adata, cfg: dict) -> dict:
    """Test whether repair-associated programs rise and stall.

    Compares the ratio of differentiation-program score to
    apoptosis-program score at different pseudotime bins.

    If repair stalls, we expect the differentiation/apoptosis ratio
    to decline at late pseudotime in COVID cells.
    """
    if "dpt_pseudotime" not in adata.obs.columns:
        return {"error": "pseudotime not computed"}

    diff_col = next((c for c in adata.obs.columns if c.endswith("AT2_to_AT1_differentiation")), None)
    apop_col = next((c for c in adata.obs.columns if c.endswith("apoptosis") and ("score" in c or "program" in c)), None)
    if diff_col is None or apop_col is None:
        return {"error": "required program scores not found"}

    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    covid_label = cfg["conditions"]["covid_label"]

    pt = adata.obs["dpt_pseudotime"].values
    diff_score = adata.obs[diff_col].values
    apop_score = adata.obs[apop_col].values
    conditions = adata.obs[condition_col].values

    n_bins = 10
    bin_edges = np.linspace(0, 1, n_bins + 1)
    records = []

    for i in range(n_bins):
        lo, hi = bin_edges[i], bin_edges[i + 1]
        bin_mask = (pt >= lo) & (pt < hi)

        for cond_label in [healthy_label, covid_label]:
            mask = bin_mask & (conditions == cond_label)
            n = mask.sum()
            if n < 5:
                continue
            mean_diff = float(np.nanmean(diff_score[mask]))
            mean_apop = float(np.nanmean(apop_score[mask]))
            ratio = mean_diff / (mean_apop + 1e-6)
            records.append({
                "bin": i,
                "pt_lo": float(lo),
                "pt_hi": float(hi),
                "condition": cond_label,
                "n_cells": int(n),
                "mean_differentiation": mean_diff,
                "mean_apoptosis": mean_apop,
                "diff_apop_ratio": ratio,
            })

    return {"bins": records}


def local_heterogeneity(
    adata, cfg: dict, rep_key: str = "X_pca", k: int = 30
) -> np.ndarray:
    """Compute per-cell local heterogeneity score.

    For each cell, compute the variance of program scores among
    its k nearest neighbors. High values indicate cells in regions
    of high transcriptomic heterogeneity (part of the fan-out).
    """
    from scipy.sparse import issparse

    conn = adata.obsp.get("connectivities", None)
    if conn is None:
        logger.warning("No connectivities found; run sc.pp.neighbors first")
        return np.full(adata.n_obs, np.nan)

    prog_cols = [c for c in adata.obs.columns if c.startswith("score_") or c.startswith("program_")]
    if not prog_cols:
        return np.full(adata.n_obs, np.nan)

    prog_mat = adata.obs[prog_cols].values
    if issparse(conn):
        conn = conn.tocsr()

    het_scores = np.empty(adata.n_obs)
    for i in range(adata.n_obs):
        neighbors = conn[i].nonzero()[1]
        if len(neighbors) < 3:
            het_scores[i] = np.nan
            continue
        neighbor_progs = prog_mat[neighbors]
        het_scores[i] = float(np.var(neighbor_progs))

    return het_scores


def fan_out_contribution(
    adata, cfg: dict, rep_key: str = "X_pca"
) -> "pd.DataFrame":
    """Decompose the fan-out: which programs explain distance from healthy centroid?

    Uses a simple linear regression of distance-to-healthy-centroid
    on program scores to identify which programs contribute most
    to the dispersion pattern.
    """
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    rep = adata.obsm[rep_key]

    healthy_mask = adata.obs[condition_col].values == healthy_label
    h_centroid = rep[healthy_mask].mean(axis=0)
    dists = np.linalg.norm(rep - h_centroid, axis=1)

    prog_cols = [c for c in adata.obs.columns if c.startswith("score_") or c.startswith("program_")]
    if not prog_cols:
        return pd.DataFrame()

    X = adata.obs[prog_cols].values
    mask = ~np.any(np.isnan(X), axis=1)

    from sklearn.linear_model import LinearRegression

    lr = LinearRegression()
    lr.fit(X[mask], dists[mask])

    results = []
    for i, col in enumerate(prog_cols):
        prog_name = col.replace("score_", "").replace("program_", "")
        results.append({
            "program": prog_name,
            "coefficient": float(lr.coef_[i]),
            "abs_coefficient": float(abs(lr.coef_[i])),
        })

    df = pd.DataFrame(results).sort_values("abs_coefficient", ascending=False)
    df.attrs["r_squared"] = float(lr.score(X[mask], dists[mask]))
    return df
