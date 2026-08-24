import numpy as np
import pandas as pd
import anndata as ad
import scipy.sparse as sp

from src.qc import compute_qc_metrics, apply_qc_filters, qc_summary


def _tiny_adata(counts, gene_names, cell_names=None):
    if cell_names is None:
        cell_names = [f"cell{i}" for i in range(counts.shape[0])]
    a = ad.AnnData(X=sp.csr_matrix(np.asarray(counts, dtype=np.float32)))
    a.obs_names = cell_names
    a.var_names = gene_names
    return a


def test_compute_qc_metrics_adds_expected_columns(synthetic_atlas):
    adata = synthetic_atlas.copy()
    compute_qc_metrics(adata)
    for col in ("n_genes_by_counts", "total_counts", "pct_counts_mt"):
        assert col in adata.obs.columns
    assert (adata.obs["total_counts"] >= 0).all()
    assert adata.obs["pct_counts_mt"].between(0, 100).all()


def test_apply_qc_filters_removes_low_gene_cells():
    genes = ["A", "B", "C", "D", "MT-1"]
    # 3 well-expressed cells, 2 near-empty cells.
    counts = np.array([
        [10, 10, 10, 10, 1],
        [8, 9, 7, 6, 1],
        [12, 5, 6, 9, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
    ])
    adata = _tiny_adata(counts, genes)
    cfg = {"qc": {"min_genes_per_cell": 3, "min_cells_per_gene": 1}}
    compute_qc_metrics(adata)
    filtered = apply_qc_filters(adata, cfg)
    assert filtered.n_obs == 3
    assert set(filtered.obs_names) == {"cell0", "cell1", "cell2"}


def test_apply_qc_filters_removes_high_mito_cells():
    """Regression test: config key is `max_pct_mito` (config.yaml), not
    `max_pct_mt`. src/qc.py previously read the wrong key (`max_pct_mt`),
    so this filter silently never applied. This test fails until qc.py
    reads `max_pct_mito`.
    """
    genes = ["A", "B", "C", "D", "MT-1", "MT-2"]
    # Low-MT cells: ~5% of counts from MT genes.
    # High-MT cells: ~40% of counts from MT genes (above a 20% threshold).
    counts = np.array([
        [24, 24, 24, 23, 3, 2],   # ~5% MT
        [23, 24, 24, 24, 2, 3],   # ~5% MT
        [24, 23, 24, 24, 3, 2],   # ~5% MT
        [15, 15, 15, 15, 20, 20],  # ~40% MT
        [14, 15, 16, 15, 20, 20],  # ~40% MT
        [15, 15, 15, 15, 20, 20],  # ~40% MT
    ])
    adata = _tiny_adata(counts, genes)
    cfg = {"qc": {"min_genes_per_cell": 1, "min_cells_per_gene": 1, "max_pct_mito": 20.0}}
    compute_qc_metrics(adata)

    high_mito_cells = adata.obs_names[adata.obs["pct_counts_mt"] > 20.0]
    assert len(high_mito_cells) == 3, "fixture sanity check: expected 3 high-MT cells"

    filtered = apply_qc_filters(adata, cfg)
    assert filtered.n_obs == 3
    assert set(filtered.obs_names) == {"cell0", "cell1", "cell2"}
    assert (filtered.obs["pct_counts_mt"] <= 20.0).all()


def test_apply_qc_filters_removes_high_total_count_outliers():
    genes = [f"G{i}" for i in range(10)] + ["MT-1"]
    rng = np.random.default_rng(0)
    normal_cells = rng.integers(1, 20, size=(4, 11))
    outlier_cell = np.full((1, 11), 5000)
    counts = np.vstack([normal_cells, outlier_cell])
    adata = _tiny_adata(counts, genes)
    cfg = {
        "qc": {
            "min_genes_per_cell": 1,
            "min_cells_per_gene": 1,
            "max_total_counts": 1000,
        }
    }
    compute_qc_metrics(adata)
    filtered = apply_qc_filters(adata, cfg)
    assert filtered.n_obs == 4
    assert "cell4" not in filtered.obs_names


def test_apply_qc_filters_removes_high_gene_count_outliers():
    # 3 cells express only a handful of genes; 1 outlier expresses all of
    # them (above max_genes_per_cell).
    genes = [f"G{i}" for i in range(20)] + ["MT-1"]
    counts = np.zeros((4, 21))
    counts[0, :4] = 5
    counts[1, :5] = 5
    counts[2, :3] = 5
    counts[3, :] = 5  # expresses all 21 genes
    adata = _tiny_adata(counts, genes)
    cfg = {
        "qc": {
            "min_genes_per_cell": 1,
            "min_cells_per_gene": 1,
            "max_genes_per_cell": 10,
        }
    }
    compute_qc_metrics(adata)
    filtered = apply_qc_filters(adata, cfg)
    assert filtered.n_obs == 3
    assert "cell3" not in filtered.obs_names


def test_qc_summary_shape(synthetic_atlas):
    adata = synthetic_atlas.copy()
    compute_qc_metrics(adata)
    summary = qc_summary(adata)
    assert list(summary.index) == ["n_genes_by_counts", "total_counts", "pct_counts_mt"]
    for col in ("mean", "median", "min", "max", "std"):
        assert col in summary.columns
