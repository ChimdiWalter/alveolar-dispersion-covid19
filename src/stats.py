"""
Statistical tests and robustness metrics.

This module implements the quantitative backbone of the robustness-collapse
analysis: displacement metrics, dispersion tests, pseudotime enrichment,
permutation controls, and trend analysis.
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.stats")

try:
    import numpy as np
    import pandas as pd
    from scipy import stats as sp_stats
    from scipy.spatial.distance import cdist
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Displacement and dispersion metrics
# ---------------------------------------------------------------------------

def centroid_distance(adata, cfg: dict,
                     rep_key: str = "X_pca") -> "pd.DataFrame":
    """Compute per-cell distance from the healthy-cell centroid.

    Parameters
    ----------
    adata : AnnData
    cfg : dict
    rep_key : str
        Obsm key for the representation space.

    Returns
    -------
    pd.DataFrame with columns [cell, condition, distance_to_healthy_centroid].
    """
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    rep = adata.obsm[rep_key]

    healthy_mask = adata.obs[condition_col].values == healthy_label
    centroid = rep[healthy_mask].mean(axis=0)
    dists = np.linalg.norm(rep - centroid, axis=1)

    df = pd.DataFrame({
        "cell": adata.obs_names,
        "condition": adata.obs[condition_col].values,
        "distance_to_healthy_centroid": dists,
    })
    return df


def displacement_test(dist_df: "pd.DataFrame",
                      healthy_label: str = "Healthy",
                      covid_label: str = "COVID-19") -> dict:
    """Mann-Whitney U test comparing distances between conditions.

    Returns
    -------
    dict with U statistic, p-value, effect size (rank-biserial r), and
    group summaries.
    """
    d_h = dist_df.loc[dist_df["condition"] == healthy_label, "distance_to_healthy_centroid"]
    d_c = dist_df.loc[dist_df["condition"] == covid_label, "distance_to_healthy_centroid"]

    U, p = sp_stats.mannwhitneyu(d_c, d_h, alternative="greater")
    # Rank-biserial correlation as effect size
    n1, n2 = len(d_c), len(d_h)
    r = 1 - (2 * U) / (n1 * n2)

    return {
        "test": "Mann-Whitney U (COVID > Healthy)",
        "U": U,
        "p_value": p,
        "effect_size_r": r,
        "covid_mean": d_c.mean(),
        "covid_median": d_c.median(),
        "healthy_mean": d_h.mean(),
        "healthy_median": d_h.median(),
        "n_covid": n1,
        "n_healthy": n2,
    }


def dispersion_test(adata, cfg: dict,
                    rep_key: str = "X_pca") -> dict:
    """Levene's test for equality of variances between conditions.

    Tests whether COVID cells are more dispersed (higher variance in
    embedding space) than healthy cells.

    Returns
    -------
    dict with test statistic, p-value, and group variances.
    """
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    covid_label = cfg["conditions"]["covid_label"]
    rep = adata.obsm[rep_key]

    healthy_mask = adata.obs[condition_col].values == healthy_label
    covid_mask = adata.obs[condition_col].values == covid_label

    # Compute per-cell distance from own group centroid
    h_centroid = rep[healthy_mask].mean(axis=0)
    c_centroid = rep[covid_mask].mean(axis=0)
    d_h = np.linalg.norm(rep[healthy_mask] - h_centroid, axis=1)
    d_c = np.linalg.norm(rep[covid_mask] - c_centroid, axis=1)

    stat, p = sp_stats.levene(d_h, d_c, center="median")

    return {
        "test": "Levene's test (dispersion)",
        "statistic": stat,
        "p_value": p,
        "healthy_variance": d_h.var(),
        "covid_variance": d_c.var(),
        "healthy_mean_dispersion": d_h.mean(),
        "covid_mean_dispersion": d_c.mean(),
    }


def nn_condition_mixing(adata, cfg: dict) -> "pd.DataFrame":
    """Compute nearest-neighbor condition mixing score per cell.

    For each cell, what fraction of its k nearest neighbors share the
    same condition label?

    Returns
    -------
    pd.DataFrame with columns [cell, condition, same_condition_fraction].
    """
    condition_col = cfg["conditions"]["condition_column"]
    conditions = adata.obs[condition_col].values

    # Get neighbor indices from the connectivities graph
    from scipy.sparse import issparse
    conn = adata.obsp["connectivities"]
    if issparse(conn):
        conn = conn.tocsr()

    scores = []
    for i in range(adata.n_obs):
        neighbors = conn[i].nonzero()[1]
        if len(neighbors) == 0:
            scores.append(np.nan)
            continue
        same = (conditions[neighbors] == conditions[i]).mean()
        scores.append(same)

    return pd.DataFrame({
        "cell": adata.obs_names,
        "condition": conditions,
        "same_condition_fraction": scores,
    })


# ---------------------------------------------------------------------------
# Permutation tests
# ---------------------------------------------------------------------------

def permutation_test_pseudotime(adata, cfg: dict,
                                 n_perm: int = 1000,
                                 seed: int = 42) -> dict:
    """Permutation test for condition-pseudotime association.

    Shuffles condition labels and recomputes the difference in median
    pseudotime between conditions. Compares the observed difference to
    the null distribution.

    Returns
    -------
    dict with observed_diff, p_value, null_mean, null_std.
    """
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    covid_label = cfg["conditions"]["covid_label"]

    pt = adata.obs["dpt_pseudotime"].values
    conditions = adata.obs[condition_col].values

    # Observed difference
    obs_diff = np.median(pt[conditions == covid_label]) - np.median(pt[conditions == healthy_label])

    # Permutation null
    rng = np.random.default_rng(seed)
    null_diffs = np.empty(n_perm)
    for i in range(n_perm):
        shuffled = rng.permutation(conditions)
        null_diffs[i] = (np.median(pt[shuffled == covid_label]) -
                         np.median(pt[shuffled == healthy_label]))

    p_value = (np.sum(null_diffs >= obs_diff) + 1) / (n_perm + 1)

    return {
        "test": "permutation (median pseudotime difference)",
        "observed_diff": obs_diff,
        "p_value": p_value,
        "null_mean": null_diffs.mean(),
        "null_std": null_diffs.std(),
        "n_permutations": n_perm,
    }


# ---------------------------------------------------------------------------
# Pseudotime trend testing
# ---------------------------------------------------------------------------

def test_gene_trend(adata, gene: str, n_bins: int = 50) -> dict:
    """Test whether a gene's expression varies significantly along pseudotime.

    Uses Spearman correlation as a simple, non-parametric trend test.

    Parameters
    ----------
    adata : AnnData
    gene : str
    n_bins : int

    Returns
    -------
    dict with rho, p_value, direction.
    """
    pt = adata.obs["dpt_pseudotime"].values

    if adata.raw is not None and gene in adata.raw.var_names:
        expr = np.asarray(adata.raw[:, gene].X.todense()).flatten()
    elif gene in adata.var_names:
        expr = np.asarray(adata[:, gene].X.todense()).flatten()
    else:
        return {"gene": gene, "error": "not found"}

    rho, p = sp_stats.spearmanr(pt, expr)
    return {
        "gene": gene,
        "spearman_rho": rho,
        "p_value": p,
        "direction": "increasing" if rho > 0 else "decreasing",
    }


def robustness_composite_score(displacement_result: dict,
                                dispersion_result: dict,
                                permutation_result: dict) -> dict:
    """Compute a summary robustness-collapse confidence score.

    Combines three independent lines of evidence:
    1. Displacement significance
    2. Dispersion difference significance
    3. Pseudotime enrichment significance

    Returns
    -------
    dict with individual p-values and a combined assessment.
    """
    criteria = {
        "displacement_p": displacement_result["p_value"],
        "dispersion_p": dispersion_result["p_value"],
        "pseudotime_perm_p": permutation_result["p_value"],
    }

    n_significant = sum(1 for p in criteria.values() if p < 0.05)

    return {
        **criteria,
        "n_significant_of_3": n_significant,
        "assessment": (
            "strong" if n_significant == 3 else
            "moderate" if n_significant == 2 else
            "weak" if n_significant == 1 else
            "not supported"
        ),
    }
