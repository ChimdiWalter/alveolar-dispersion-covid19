"""
Portable transitional-state scoring.

Replaces hard KRT8/CLDN4 marker thresholds with more portable,
continuous, and biologically interpretable state scores.
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.state_score")

try:
    import numpy as np
    import pandas as pd
except ImportError:
    pass


def at2_identity_score(adata, cfg: dict) -> np.ndarray:
    """AT2 identity score from curated markers."""
    genes = cfg["gene_programs"]["AT2_identity"]["genes"]
    return _mean_expression(adata, genes)


def at1_identity_score(adata, cfg: dict) -> np.ndarray:
    """AT1 identity score from curated markers."""
    genes = cfg["gene_programs"]["AT1_identity"]["genes"]
    return _mean_expression(adata, genes)


def transitional_score(adata, cfg: dict) -> np.ndarray:
    """Continuous transitional-state score.

    Captures cells in the transitional zone between AT2 and AT1 identity:
    - elevated KRT8, CLDN4, SFN (transitional markers)
    - declining AT2 identity
    - partial AT1 activation

    This is more portable than a hard two-marker threshold because it
    uses multiple genes and produces a continuous value.
    """
    trans_genes = cfg["gene_programs"]["AT2_to_AT1_differentiation"]["genes"]
    return _mean_expression(adata, trans_genes)


def injury_composite_score(adata, cfg: dict) -> np.ndarray:
    """Composite injury score from non-homeostatic programs.

    Mean of per-cell scores across:
    interferon, NF-kB, oxidative stress, apoptosis, senescence,
    AT2-to-AT1 differentiation.
    """
    injury_programs = [
        "interferon_response",
        "nfkb_inflammatory",
        "oxidative_stress",
        "apoptosis",
        "senescence",
        "AT2_to_AT1_differentiation",
    ]
    cols = []
    for p in injury_programs:
        if f"score_{p}" in adata.obs.columns:
            cols.append(f"score_{p}")
        elif f"program_{p}" in adata.obs.columns:
            cols.append(f"program_{p}")
    if not cols:
        logger.warning("No injury program scores found in adata.obs")
        return np.full(adata.n_obs, np.nan)
    return adata.obs[cols].mean(axis=1).values


def coherence_loss_score(adata, cfg: dict, rep_key: str = "X_pca") -> np.ndarray:
    """Per-cell coherence-loss score.

    Defined as the Euclidean distance from each cell to the centroid of
    healthy cells in the representation space. Higher values indicate
    greater departure from the homeostatic state.

    This is a continuous, geometry-based score that does not depend on
    marker thresholds or cell-type annotations.
    """
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    rep = adata.obsm[rep_key]

    healthy_mask = adata.obs[condition_col].values == healthy_label
    centroid = rep[healthy_mask].mean(axis=0)
    return np.linalg.norm(rep - centroid, axis=1)


def repair_failure_score(adata, cfg: dict) -> np.ndarray:
    """Repair-failure score: high transitional signal with declining identity.

    Captures cells that have initiated the AT2-to-AT1 repair program
    but show identity loss. Computed as:

        repair_failure = transitional_score - 0.5 * (AT2_identity + AT1_identity)

    Positive values indicate cells with strong transitional signal
    relative to their residual identity.
    """
    trans = transitional_score(adata, cfg)
    at2 = at2_identity_score(adata, cfg)
    at1 = at1_identity_score(adata, cfg)
    return trans - 0.5 * (at2 + at1)


def score_all(adata, cfg: dict, rep_key: str = "X_pca") -> "pd.DataFrame":
    """Compute all state scores and return as a DataFrame.

    Adds scores to adata.obs as side effect.
    """
    scores = {
        "at2_identity": at2_identity_score(adata, cfg),
        "at1_identity": at1_identity_score(adata, cfg),
        "transitional": transitional_score(adata, cfg),
        "injury_composite": injury_composite_score(adata, cfg),
        "coherence_loss": coherence_loss_score(adata, cfg, rep_key),
        "repair_failure": repair_failure_score(adata, cfg),
    }

    for name, vals in scores.items():
        adata.obs[f"state_{name}"] = vals

    return pd.DataFrame(scores, index=adata.obs_names)


def benchmark_scores(
    adata,
    cfg: dict,
    score_df: "pd.DataFrame",
    rep_key: str = "X_pca",
) -> "pd.DataFrame":
    """Benchmark state scores against known labels and pseudotime.

    For each score, compute:
    - Spearman correlation with pseudotime
    - Mann-Whitney U between conditions
    - AUC for separating transitional from non-transitional cells
    """
    from scipy import stats as sp_stats

    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    covid_label = cfg["conditions"]["covid_label"]
    ct_col = cfg["cell_types"]["annotation_column"]

    results = []
    for col in score_df.columns:
        vals = score_df[col].values
        rec = {"score": col}

        if "dpt_pseudotime" in adata.obs.columns:
            pt = adata.obs["dpt_pseudotime"].values
            mask = ~(np.isnan(vals) | np.isnan(pt))
            if mask.sum() > 10:
                rho, p = sp_stats.spearmanr(vals[mask], pt[mask])
                rec["pseudotime_spearman_rho"] = float(rho)
                rec["pseudotime_spearman_p"] = float(p)

        h_vals = vals[adata.obs[condition_col].values == healthy_label]
        c_vals = vals[adata.obs[condition_col].values == covid_label]
        h_vals = h_vals[~np.isnan(h_vals)]
        c_vals = c_vals[~np.isnan(c_vals)]
        if len(h_vals) > 5 and len(c_vals) > 5:
            U, p = sp_stats.mannwhitneyu(c_vals, h_vals, alternative="two-sided")
            rec["condition_mw_p"] = float(p)
            rec["covid_median"] = float(np.median(c_vals))
            rec["healthy_median"] = float(np.median(h_vals))

        if ct_col in adata.obs.columns:
            is_trans = adata.obs[ct_col].isin(
                ["ECM-high epithelial", "Transitional"]
            ).values
            if is_trans.sum() > 10 and (~is_trans).sum() > 10:
                from sklearn.metrics import roc_auc_score

                mask = ~np.isnan(vals)
                try:
                    auc = roc_auc_score(is_trans[mask], vals[mask])
                    rec["transitional_auc"] = float(auc)
                except Exception:
                    pass

        results.append(rec)

    return pd.DataFrame(results)


def _mean_expression(adata, genes: list) -> np.ndarray:
    """Mean expression of available genes from the raw matrix."""
    if adata.raw is not None:
        available = [g for g in genes if g in adata.raw.var_names]
        if not available:
            return np.full(adata.n_obs, np.nan)
        X = adata.raw[:, available].X
    else:
        available = [g for g in genes if g in adata.var_names]
        if not available:
            return np.full(adata.n_obs, np.nan)
        X = adata[:, available].X
    if hasattr(X, "toarray"):
        X = X.toarray()
    return np.asarray(X).mean(axis=1).flatten()
