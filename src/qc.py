"""
Quality control filtering for snRNA-seq data.

Primary method: Scanpy-based thresholding on gene counts, total counts,
and mitochondrial fraction.

Alternatives considered:
  - scDblFinder (R) or Scrublet (Python) for doublet detection
  - SoupX or CellBender for ambient RNA removal
  These are recommended as secondary steps but not included in the primary
  pipeline because the SCP1219 atlas was likely already QC-filtered by
  the original authors. We apply our own filters as a safety net and to
  ensure reproducibility.
"""

import logging

logger = logging.getLogger("robustness.qc")

try:
    import scanpy as sc
    import numpy as np
    import pandas as pd
except ImportError:
    pass


def compute_qc_metrics(adata: "sc.AnnData") -> "sc.AnnData":
    """Annotate cells with QC metrics (in-place).

    Adds to adata.obs:
      - n_genes_by_counts
      - total_counts
      - pct_counts_mt

    Parameters
    ----------
    adata : AnnData

    Returns
    -------
    AnnData (same object, modified in place)
    """
    # Identify mitochondrial genes
    adata.var["mt"] = adata.var_names.str.startswith("MT-")
    sc.pp.calculate_qc_metrics(
        adata, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True
    )
    logger.info(
        f"QC metrics computed: {adata.n_obs} cells, "
        f"{adata.var['mt'].sum()} MT genes identified"
    )
    return adata


def apply_qc_filters(adata: "sc.AnnData", cfg: dict) -> "sc.AnnData":
    """Filter cells and genes based on QC thresholds from config.

    Parameters
    ----------
    adata : AnnData
        Must have QC metrics computed (call compute_qc_metrics first).
    cfg : dict
        Project configuration with qc section.

    Returns
    -------
    AnnData
        Filtered copy.
    """
    qc = cfg["qc"]
    n_before = adata.n_obs

    # Cell filters
    sc.pp.filter_cells(adata, min_genes=qc["min_genes_per_cell"])
    if qc.get("max_genes_per_cell"):
        adata = adata[adata.obs["n_genes_by_counts"] < qc["max_genes_per_cell"]].copy()
    if qc.get("max_total_counts"):
        adata = adata[adata.obs["total_counts"] < qc["max_total_counts"]].copy()
    if qc.get("max_pct_mt"):
        adata = adata[adata.obs["pct_counts_mt"] < qc["max_pct_mt"]].copy()

    # Gene filters
    sc.pp.filter_genes(adata, min_cells=qc.get("min_cells_per_gene", 10))

    n_after = adata.n_obs
    logger.info(f"QC filtering: {n_before} → {n_after} cells "
                f"({n_before - n_after} removed)")
    return adata


def qc_summary(adata: "sc.AnnData") -> "pd.DataFrame":
    """Generate a summary table of QC statistics.

    Returns
    -------
    pd.DataFrame with rows for each metric and columns [mean, median, min, max].
    """
    metrics = ["n_genes_by_counts", "total_counts", "pct_counts_mt"]
    rows = []
    for m in metrics:
        vals = adata.obs[m]
        rows.append({
            "metric": m,
            "mean": vals.mean(),
            "median": vals.median(),
            "min": vals.min(),
            "max": vals.max(),
            "std": vals.std(),
        })
    return pd.DataFrame(rows).set_index("metric")
