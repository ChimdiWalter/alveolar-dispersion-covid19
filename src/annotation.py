"""
Cell-type annotation validation and re-annotation.

Primary method: Canonical marker gene scoring + Leiden re-clustering of the
epithelial subset with manual label assignment based on marker expression.

Why this approach:
  - The SCP1219 atlas ships with author-provided annotations. We trust but
    verify: marker gene dotplots and score distributions confirm or refute
    existing labels before any downstream analysis.
  - Automated annotation tools (CellTypist, scType) are alternatives but
    introduce their own reference biases. Manual marker-based validation
    is more transparent and appropriate for a focused epithelial study.
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.annotation")

try:
    import scanpy as sc
    import pandas as pd
    import numpy as np
except ImportError:
    pass


def validate_markers(adata: "sc.AnnData", markers: dict,
                     annotation_col: str = "cell_type") -> "pd.DataFrame":
    """Check whether annotated cell types express expected marker genes.

    Parameters
    ----------
    adata : AnnData
        Annotated and normalized.
    markers : dict
        {cell_type: [gene1, gene2, ...]} from config.
    annotation_col : str
        Column in adata.obs containing cell type labels.

    Returns
    -------
    pd.DataFrame
        Mean expression of each marker gene per annotated cell type.
    """
    records = []
    for ct, genes in markers.items():
        present_genes = [g for g in genes if g in adata.var_names]
        missing = set(genes) - set(present_genes)
        if missing:
            logger.warning(f"Markers not found in var_names for {ct}: {missing}")
        for g in present_genes:
            for label in adata.obs[annotation_col].unique():
                mask = (adata.obs[annotation_col] == label).values
                n_cells = int(mask.sum())
                if n_cells == 0:
                    continue
                sub_X = adata[mask, g].X
                try:
                    mean_expr = float(sub_X.mean())
                except (ZeroDivisionError, ValueError):
                    mean_expr = 0.0
                try:
                    pct_expressing = float((sub_X > 0).mean())
                except (ZeroDivisionError, ValueError):
                    pct_expressing = 0.0
                records.append({
                    "expected_type": ct,
                    "marker": g,
                    "annotated_type": label,
                    "mean_expression": mean_expr,
                    "pct_expressing": pct_expressing,
                })
    return pd.DataFrame(records)


def subset_alveolar(adata: "sc.AnnData", cfg: dict,
                    annotation_col: Optional[str] = None) -> "sc.AnnData":
    """Subset to alveolar epithelial cells (AT1, AT2, Transitional).

    Parameters
    ----------
    adata : AnnData
    cfg : dict
        Project config with cell_types.primary_focus list.
    annotation_col : str, optional
        Override for annotation column name.

    Returns
    -------
    AnnData
        Subset containing only alveolar epithelial cells.
    """
    col = annotation_col or cfg["cell_types"]["annotation_column"]
    target_types = cfg["cell_types"]["primary_focus"]
    mask = adata.obs[col].isin(target_types)
    n_selected = mask.sum()
    logger.info(f"Subsetting to {target_types}: {n_selected}/{adata.n_obs} cells")
    return adata[mask].copy()


def recluster_epithelial(adata: "sc.AnnData", resolution: float = 0.5,
                         n_pcs: int = 30) -> "sc.AnnData":
    """Re-cluster the epithelial subset for independent annotation.

    Use this if the original annotations appear noisy or inconsistent
    with marker expression.

    Parameters
    ----------
    adata : AnnData
        Normalized, HVG-selected epithelial subset.
    resolution : float
        Leiden clustering resolution.
    n_pcs : int
        Number of PCs for neighbor graph.

    Returns
    -------
    AnnData with 'leiden_epi' column in .obs.
    """
    sc.pp.pca(adata, n_comps=n_pcs)
    sc.pp.neighbors(adata, n_pcs=n_pcs)
    sc.tl.leiden(adata, resolution=resolution, key_added="leiden_epi")
    logger.info(f"Re-clustered into {adata.obs['leiden_epi'].nunique()} clusters "
                f"at resolution {resolution}")
    return adata
