import numpy as np
import pandas as pd
import anndata as ad
import pytest

from src.stats import (
    centroid_distance,
    displacement_test,
    dispersion_test,
    permutation_test_pseudotime,
    robustness_composite_score,
)

_COND_CFG = {
    "conditions": {
        "condition_column": "group",
        "healthy_label": "Control",
        "covid_label": "COVID-19",
    }
}


def _make_adata_with_rep(rep, conditions, extra_obs=None):
    n = rep.shape[0]
    obs = pd.DataFrame({"group": conditions}, index=[f"c{i}" for i in range(n)])
    if extra_obs:
        for k, v in extra_obs.items():
            obs[k] = v
    a = ad.AnnData(X=np.zeros((n, 1), dtype=np.float32), obs=obs)
    a.obsm["X_pca"] = rep
    return a


def test_centroid_distance_healthy_centroid_is_zero_for_itself():
    rng = np.random.default_rng(0)
    healthy = rng.normal(0, 0.1, size=(20, 3))
    covid = rng.normal(5, 0.1, size=(20, 3))
    rep = np.vstack([healthy, covid])
    conditions = ["Control"] * 20 + ["COVID-19"] * 20
    adata = _make_adata_with_rep(rep, conditions)

    df = centroid_distance(adata, _COND_CFG)
    assert set(df.columns) == {"cell", "condition", "distance_to_healthy_centroid"}
    covid_dist = df.loc[df["condition"] == "COVID-19", "distance_to_healthy_centroid"].mean()
    healthy_dist = df.loc[df["condition"] == "Control", "distance_to_healthy_centroid"].mean()
    assert covid_dist > healthy_dist


def test_displacement_test_detects_clear_signal():
    dist_df = pd.DataFrame({
        "condition": ["Control"] * 30 + ["COVID-19"] * 30,
        "distance_to_healthy_centroid": np.concatenate([
            np.full(30, 1.0), np.full(30, 10.0)
        ]),
    })
    result = displacement_test(dist_df, healthy_label="Control", covid_label="COVID-19")
    assert result["p_value"] < 0.001
    assert result["covid_mean"] > result["healthy_mean"]


def test_displacement_test_no_signal_when_identical():
    rng = np.random.default_rng(1)
    vals = rng.normal(5, 1, size=60)
    dist_df = pd.DataFrame({
        "condition": ["Control"] * 30 + ["COVID-19"] * 30,
        "distance_to_healthy_centroid": vals,
    })
    result = displacement_test(dist_df, healthy_label="Control", covid_label="COVID-19")
    assert result["p_value"] > 0.05


def test_dispersion_test_detects_clear_variance_difference():
    rng = np.random.default_rng(2)
    healthy = rng.normal(0, 0.2, size=(100, 3))
    covid = rng.normal(0, 3.0, size=(100, 3))
    rep = np.vstack([healthy, covid])
    conditions = ["Control"] * 100 + ["COVID-19"] * 100
    adata = _make_adata_with_rep(rep, conditions)

    result = dispersion_test(adata, _COND_CFG)
    assert result["p_value"] < 0.001
    assert result["covid_variance"] > result["healthy_variance"]


def test_dispersion_test_no_signal_when_equal_variance():
    rng = np.random.default_rng(3)
    healthy = rng.normal(0, 1.0, size=(100, 3))
    covid = rng.normal(0, 1.0, size=(100, 3))
    rep = np.vstack([healthy, covid])
    conditions = ["Control"] * 100 + ["COVID-19"] * 100
    adata = _make_adata_with_rep(rep, conditions)

    result = dispersion_test(adata, _COND_CFG)
    assert result["p_value"] > 0.05


def test_permutation_test_pseudotime_is_deterministic_given_seed():
    rng = np.random.default_rng(4)
    n = 40
    conditions = ["Control"] * (n // 2) + ["COVID-19"] * (n // 2)
    pt = rng.uniform(0, 1, size=n)
    adata = _make_adata_with_rep(
        np.zeros((n, 1)), conditions, extra_obs={"dpt_pseudotime": pt}
    )

    r1 = permutation_test_pseudotime(adata, _COND_CFG, n_perm=200, seed=42)
    r2 = permutation_test_pseudotime(adata, _COND_CFG, n_perm=200, seed=42)
    assert r1 == r2


def test_permutation_test_pseudotime_detects_clear_signal():
    # Continuous, non-tied values so the true Control/COVID-19 split is the
    # (near-)unique extreme separation among all possible relabelings —
    # with only two distinct values (a tie-heavy fixture), many random
    # relabelings can reproduce the same extreme median split by chance,
    # which was found to make this assertion flaky.
    rng = np.random.default_rng(7)
    n = 60
    conditions = ["Control"] * 30 + ["COVID-19"] * 30
    pt = np.concatenate([
        rng.normal(0.2, 0.05, size=30),
        rng.normal(0.8, 0.05, size=30),
    ])
    adata = _make_adata_with_rep(
        np.zeros((n, 1)), conditions, extra_obs={"dpt_pseudotime": pt}
    )
    result = permutation_test_pseudotime(adata, _COND_CFG, n_perm=500, seed=42)
    assert result["p_value"] < 0.01
    assert result["observed_diff"] > 0


@pytest.mark.parametrize(
    "p_values,expected",
    [
        ((0.001, 0.001, 0.001), "strong"),
        ((0.001, 0.001, 0.5), "moderate"),
        ((0.001, 0.5, 0.5), "weak"),
        ((0.5, 0.5, 0.5), "not supported"),
    ],
)
def test_robustness_composite_score_bucketing(p_values, expected):
    disp, disp2, perm = p_values
    result = robustness_composite_score(
        {"p_value": disp}, {"p_value": disp2}, {"p_value": perm}
    )
    assert result["assessment"] == expected
    assert result["n_significant_of_3"] == sum(1 for p in p_values if p < 0.05)
