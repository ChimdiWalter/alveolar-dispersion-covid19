import copy
import importlib.util

import numpy as np
import pytest

from src.embedding import (
    normalize_and_select_hvg,
    run_pca,
    run_neighbors,
    run_umap,
    run_diffmap,
    run_harmony,
)

HARMONYPY_AVAILABLE = importlib.util.find_spec("harmonypy") is not None


def test_normalize_and_select_hvg(synthetic_atlas, test_cfg):
    adata = synthetic_atlas.copy()
    n_genes_before = adata.n_vars
    out = normalize_and_select_hvg(adata, test_cfg)
    assert out.raw is not None
    assert out.raw.n_vars == n_genes_before
    assert out.n_vars <= test_cfg["feature_selection"]["n_top_genes"]
    assert out.n_vars > 0
    assert not np.isnan(out.X.toarray()).any()


def test_run_pca(synthetic_atlas, test_cfg):
    adata = normalize_and_select_hvg(synthetic_atlas.copy(), test_cfg)
    out = run_pca(adata, test_cfg)
    assert "X_pca" in out.obsm
    assert out.obsm["X_pca"].shape == (out.n_obs, test_cfg["dimred"]["n_pcs"])
    assert not np.isnan(out.obsm["X_pca"]).any()


def test_run_neighbors_and_umap_and_diffmap(synthetic_atlas, test_cfg):
    adata = normalize_and_select_hvg(synthetic_atlas.copy(), test_cfg)
    adata = run_pca(adata, test_cfg)
    adata = run_neighbors(adata, test_cfg)
    assert "connectivities" in adata.obsp

    adata = run_umap(adata, test_cfg)
    assert "X_umap" in adata.obsm
    assert adata.obsm["X_umap"].shape == (adata.n_obs, 2)

    adata = run_diffmap(adata, test_cfg)
    assert "X_diffmap" in adata.obsm
    assert adata.obsm["X_diffmap"].shape[0] == adata.n_obs


@pytest.mark.skipif(
    not HARMONYPY_AVAILABLE,
    reason=(
        "harmonypy not installed in this environment (e.g. no C++ build "
        "toolchain for its CMake-based build, as on this Windows test "
        "machine); Harmony batch correction is not covered by this test run."
    ),
)
def test_run_harmony(synthetic_atlas, test_cfg):
    cfg = copy.deepcopy(test_cfg)
    cfg["batch_correction"]["method"] = "harmony"

    adata = normalize_and_select_hvg(synthetic_atlas.copy(), cfg)
    adata = run_pca(adata, cfg)
    out = run_harmony(adata, cfg)

    assert "X_pca_harmony" in out.obsm
    assert out.obsm["X_pca_harmony"].shape == out.obsm["X_pca"].shape
    assert not np.isnan(out.obsm["X_pca_harmony"]).any()
