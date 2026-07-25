"""
Donor-level inference and modeling.

This module makes the donor — not the cell — the primary inferential unit.
It computes donor-level summaries, pseudobulk profiles, bootstrap confidence
intervals, and mixed-effects model scaffolds.
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.donor_models")

try:
    import numpy as np
    import pandas as pd
    from scipy import stats as sp_stats
except ImportError:
    pass


def donor_summary(adata, cfg: dict) -> "pd.DataFrame":
    """Compute per-donor summary statistics for all key quantities.

    Returns a DataFrame with one row per donor containing:
    - median_pseudotime, iqr_pseudotime
    - dispersion (median distance to own-group centroid in PCA)
    - frac_transitional (fraction of ECM-high / transitional cells)
    - program scores (median per donor for each program)
    """
    condition_col = cfg["conditions"]["condition_column"]
    donor_col = cfg["batch_correction"]["batch_key"]
    ct_col = cfg["cell_types"]["annotation_column"]
    transitional_labels = {"ECM-high epithelial", "Transitional"}

    records = []
    rep = adata.obsm.get("X_pca", None)

    for donor, idx in adata.obs.groupby(donor_col, observed=True).groups.items():
        sub = adata[idx]
        obs = sub.obs
        n_cells = len(idx)
        condition = obs[condition_col].iloc[0]

        rec = {
            "donor_id": donor,
            "condition": condition,
            "n_cells": n_cells,
        }

        if "dpt_pseudotime" in obs.columns:
            pt = obs["dpt_pseudotime"].values
            rec["median_pseudotime"] = float(np.nanmedian(pt))
            rec["mean_pseudotime"] = float(np.nanmean(pt))
            rec["iqr_pseudotime"] = float(
                np.nanpercentile(pt, 75) - np.nanpercentile(pt, 25)
            )

        if rep is not None:
            donor_rep = rep[np.isin(adata.obs_names, idx)]
            centroid = donor_rep.mean(axis=0)
            dists = np.linalg.norm(donor_rep - centroid, axis=1)
            rec["within_donor_dispersion"] = float(dists.var())
            rec["median_dist_to_donor_centroid"] = float(np.median(dists))

        ct_values = obs[ct_col].values if ct_col in obs.columns else []
        n_trans = sum(1 for v in ct_values if v in transitional_labels)
        rec["frac_transitional"] = n_trans / n_cells if n_cells > 0 else 0.0

        for prog_col in obs.columns:
            if prog_col.startswith("score_") or prog_col.startswith("program_"):
                prog_name = prog_col.replace("score_", "").replace("program_", "")
                vals = obs[prog_col].values
                rec[f"median_{prog_name}"] = float(np.nanmedian(vals))

        records.append(rec)

    return pd.DataFrame(records)


def donor_level_test(
    donor_df: "pd.DataFrame",
    metric: str,
    healthy_label: str = "Control",
    covid_label: str = "COVID-19",
) -> dict:
    """Two-sample Mann-Whitney U test at the donor level.

    Parameters
    ----------
    donor_df : pd.DataFrame
        Output of donor_summary().
    metric : str
        Column name to compare between conditions.
    """
    h = donor_df.loc[donor_df["condition"] == healthy_label, metric].dropna()
    c = donor_df.loc[donor_df["condition"] == covid_label, metric].dropna()

    if len(h) < 2 or len(c) < 2:
        return {"metric": metric, "error": "too few donors"}

    U, p_two = sp_stats.mannwhitneyu(c, h, alternative="two-sided")
    _, p_greater = sp_stats.mannwhitneyu(c, h, alternative="greater")

    n1, n2 = len(c), len(h)
    r = 1 - (2 * U) / (n1 * n2)

    return {
        "metric": metric,
        "n_covid": n1,
        "n_healthy": n2,
        "covid_median": float(c.median()),
        "healthy_median": float(h.median()),
        "U": float(U),
        "p_two_sided": float(p_two),
        "p_one_sided_greater": float(p_greater),
        "rank_biserial_r": float(r),
    }


def donor_bootstrap_ci(
    donor_df: "pd.DataFrame",
    metric: str,
    healthy_label: str = "Control",
    covid_label: str = "COVID-19",
    n_boot: int = 10000,
    ci: float = 0.95,
    seed: int = 42,
) -> dict:
    """Bootstrap CI for the difference in donor-level medians.

    Resamples donors (not cells) with replacement.
    """
    rng = np.random.default_rng(seed)
    h = donor_df.loc[donor_df["condition"] == healthy_label, metric].dropna().values
    c = donor_df.loc[donor_df["condition"] == covid_label, metric].dropna().values

    obs_diff = float(np.median(c) - np.median(h))
    boot_diffs = np.empty(n_boot)

    for i in range(n_boot):
        h_boot = rng.choice(h, size=len(h), replace=True)
        c_boot = rng.choice(c, size=len(c), replace=True)
        boot_diffs[i] = np.median(c_boot) - np.median(h_boot)

    alpha = (1 - ci) / 2
    lo = float(np.percentile(boot_diffs, 100 * alpha))
    hi = float(np.percentile(boot_diffs, 100 * (1 - alpha)))

    return {
        "metric": metric,
        "observed_diff": obs_diff,
        "ci_lower": lo,
        "ci_upper": hi,
        "ci_level": ci,
        "n_bootstrap": n_boot,
        "boot_mean": float(boot_diffs.mean()),
        "boot_std": float(boot_diffs.std()),
    }


def donor_dispersion_comparison(
    adata, cfg: dict, rep_key: str = "X_pca"
) -> dict:
    """Compare within-group dispersion at the donor level.

    For each donor, compute median distance to that donor's centroid.
    Then compare the distribution of donor-level dispersions between conditions.
    """
    condition_col = cfg["conditions"]["condition_column"]
    donor_col = cfg["batch_correction"]["batch_key"]
    healthy_label = cfg["conditions"]["healthy_label"]
    covid_label = cfg["conditions"]["covid_label"]
    rep = adata.obsm[rep_key]

    donor_dispersions = []
    for donor, idx in adata.obs.groupby(donor_col, observed=True).groups.items():
        donor_rep = rep[np.isin(adata.obs_names, idx)]
        if len(donor_rep) < 5:
            continue
        centroid = donor_rep.mean(axis=0)
        dists = np.linalg.norm(donor_rep - centroid, axis=1)
        condition = adata.obs.loc[idx[0], condition_col]
        donor_dispersions.append({
            "donor_id": donor,
            "condition": condition,
            "median_dispersion": float(np.median(dists)),
            "variance_dispersion": float(dists.var()),
            "n_cells": len(donor_rep),
        })

    df = pd.DataFrame(donor_dispersions)
    h_disp = df.loc[df["condition"] == healthy_label, "median_dispersion"].values
    c_disp = df.loc[df["condition"] == covid_label, "median_dispersion"].values

    if len(h_disp) < 2 or len(c_disp) < 2:
        return {"error": "too few donors for comparison"}

    U, p = sp_stats.mannwhitneyu(c_disp, h_disp, alternative="greater")
    lev_stat, lev_p = sp_stats.levene(c_disp, h_disp, center="median")

    return {
        "n_covid_donors": len(c_disp),
        "n_healthy_donors": len(h_disp),
        "covid_median_dispersion": float(np.median(c_disp)),
        "healthy_median_dispersion": float(np.median(h_disp)),
        "mannwhitney_p": float(p),
        "levene_stat": float(lev_stat),
        "levene_p": float(lev_p),
        "donor_dispersion_df": df,
    }


def pseudobulk_expression(
    adata, cfg: dict, layer: Optional[str] = None
) -> "pd.DataFrame":
    """Compute donor-level pseudobulk expression profiles.

    Returns a DataFrame with donors as rows and genes as columns,
    where each value is the mean log-normalized expression across
    all cells from that donor.
    """
    donor_col = cfg["batch_correction"]["batch_key"]
    condition_col = cfg["conditions"]["condition_column"]

    records = []
    for donor, idx in adata.obs.groupby(donor_col, observed=True).groups.items():
        sub = adata[idx]
        if layer and layer in sub.layers:
            X = sub.layers[layer]
        elif sub.raw is not None:
            X = sub.raw[idx].X
        else:
            X = sub.X

        if hasattr(X, "toarray"):
            X = X.toarray()
        mean_expr = np.asarray(X).mean(axis=0).flatten()

        rec = {
            "donor_id": donor,
            "condition": sub.obs[condition_col].iloc[0],
            "n_cells": len(idx),
        }
        for i, gene in enumerate(
            sub.raw.var_names if sub.raw is not None else sub.var_names
        ):
            rec[gene] = float(mean_expr[i])
        records.append(rec)

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Mixed-effects model scaffold
# ---------------------------------------------------------------------------

def mixed_effects_pseudotime(donor_df: "pd.DataFrame") -> dict:
    """Scaffold for a mixed-effects model: pseudotime ~ condition + (1|donor).

    This function checks whether statsmodels is available and runs a
    linear mixed-effects model if so. Otherwise it returns a stub.

    NOTE: This is a donor-level model, so the random effect is not
    strictly necessary (each donor has one observation). For cell-level
    mixed models, use the cell-level data directly.
    """
    try:
        import statsmodels.formula.api as smf
    except ImportError:
        return {
            "model": "mixed_effects_pseudotime",
            "status": "statsmodels not installed",
            "instruction": "pip install statsmodels; then re-run",
        }

    if "median_pseudotime" not in donor_df.columns:
        return {"error": "median_pseudotime not in donor_df"}

    df = donor_df[["donor_id", "condition", "median_pseudotime"]].dropna()
    df["is_covid"] = (df["condition"] != "Control").astype(int)

    try:
        model = smf.ols("median_pseudotime ~ is_covid", data=df).fit()
        return {
            "model": "OLS (donor-level, no random effect needed for n=27)",
            "coefficient_is_covid": float(model.params["is_covid"]),
            "p_value_is_covid": float(model.pvalues["is_covid"]),
            "ci_lower": float(model.conf_int().loc["is_covid", 0]),
            "ci_upper": float(model.conf_int().loc["is_covid", 1]),
            "r_squared": float(model.rsquared),
            "n_obs": int(model.nobs),
        }
    except Exception as e:
        return {"model": "OLS", "error": str(e)}
