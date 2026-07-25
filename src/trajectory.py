"""
Trajectory inference and pseudotime analysis.

Primary method: Scanpy diffusion pseudotime (DPT).
  - Operates on the diffusion map representation.
  - Root cell is chosen as the cell nearest to the centroid of healthy AT2
    cells in diffusion-component space.
  - Biologically appropriate because DPT models progression as a diffusion
    process on the cell graph, naturally handling continuous transitions
    and branching.

Alternative: Palantir (Setty et al., 2019).
  - Uses diffusion maps + multiscale space + Markov chain.
  - Better at detecting terminal states and fate probabilities.
  - More computationally expensive; recommended as ablation (Ablation 9).

Alternative: Monocle 3 (R-based).
  - Principal-graph approach. Not used because the pipeline is Python-first.
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.trajectory")

try:
    import scanpy as sc
    import numpy as np
    import pandas as pd
except ImportError:
    pass


def find_root_cell(adata: "sc.AnnData", cfg: dict,
                   strategy: Optional[str] = None) -> int:
    """Identify the root cell for pseudotime computation.

    Parameters
    ----------
    adata : AnnData
        Must have diffusion map or PCA computed.
    cfg : dict
    strategy : str, optional
        Override root strategy. Options:
        - 'healthy_AT2_centroid' (default): cell nearest to centroid of healthy AT2
        - 'healthy_AT1_centroid': cell nearest to centroid of healthy AT1
        - 'random_healthy': random healthy cell
        - 'covid_extreme': cell farthest from healthy centroid

    Returns
    -------
    int
        Index (iloc position) of the root cell.
    """
    strategy = strategy or cfg["trajectory"]["root_strategy"]
    condition_col = cfg["conditions"]["condition_column"]
    healthy_label = cfg["conditions"]["healthy_label"]
    annot_col = cfg["cell_types"]["annotation_column"]

    # Choose representation
    if "X_diffmap" in adata.obsm:
        rep = adata.obsm["X_diffmap"]
    else:
        rep = adata.obsm["X_pca"]

    if strategy == "healthy_AT2_centroid":
        mask = (adata.obs[condition_col] == healthy_label) & (adata.obs[annot_col] == "AT2")
        centroid = rep[mask.values].mean(axis=0)
        dists = np.linalg.norm(rep - centroid, axis=1)
        root = int(np.argmin(dists))

    elif strategy == "healthy_AT1_centroid":
        mask = (adata.obs[condition_col] == healthy_label) & (adata.obs[annot_col] == "AT1")
        centroid = rep[mask.values].mean(axis=0)
        dists = np.linalg.norm(rep - centroid, axis=1)
        root = int(np.argmin(dists))

    elif strategy == "random_healthy":
        rng = np.random.default_rng(cfg.get("random_seed", 42))
        healthy_idx = np.where(adata.obs[condition_col].values == healthy_label)[0]
        root = int(rng.choice(healthy_idx))

    elif strategy == "covid_extreme":
        healthy_mask = adata.obs[condition_col].values == healthy_label
        healthy_centroid = rep[healthy_mask].mean(axis=0)
        dists = np.linalg.norm(rep - healthy_centroid, axis=1)
        root = int(np.argmax(dists))

    else:
        raise ValueError(f"Unknown root strategy: {strategy}")

    logger.info(f"Root cell selected (strategy={strategy}): index {root}, "
                f"barcode {adata.obs_names[root]}")
    return root


def run_dpt(adata: "sc.AnnData", cfg: dict,
            root: Optional[int] = None) -> "sc.AnnData":
    """Compute diffusion pseudotime.

    Parameters
    ----------
    adata : AnnData
        Must have diffusion map and neighbor graph.
    cfg : dict
    root : int, optional
        Root cell index. Auto-detected if None.

    Returns
    -------
    AnnData with .obs['dpt_pseudotime'] and .uns['iroot'].
    """
    if root is None:
        root = find_root_cell(adata, cfg)

    adata.uns["iroot"] = root
    sc.tl.dpt(adata)
    logger.info(f"DPT computed. Pseudotime range: "
                f"{adata.obs['dpt_pseudotime'].min():.3f} – "
                f"{adata.obs['dpt_pseudotime'].max():.3f}")
    return adata


def pseudotime_density_by_condition(adata: "sc.AnnData",
                                     cfg: dict) -> "pd.DataFrame":
    """Compute pseudotime distribution statistics per condition.

    Returns
    -------
    pd.DataFrame with mean, median, std, skew per condition.
    """
    condition_col = cfg["conditions"]["condition_column"]
    records = []
    for cond in adata.obs[condition_col].unique():
        vals = adata.obs.loc[adata.obs[condition_col] == cond, "dpt_pseudotime"]
        records.append({
            "condition": cond,
            "n_cells": len(vals),
            "mean_pseudotime": vals.mean(),
            "median_pseudotime": vals.median(),
            "std_pseudotime": vals.std(),
            "skew": vals.skew(),
        })
    return pd.DataFrame(records)


def pseudotime_by_donor(adata: "sc.AnnData", cfg: dict) -> "pd.DataFrame":
    """Compute pseudotime summary statistics per donor.

    Returns
    -------
    pd.DataFrame with one row per donor.
    """
    condition_col = cfg["conditions"]["condition_column"]
    donor_col = cfg["batch_correction"]["batch_key"]
    records = []
    for donor in adata.obs[donor_col].unique():
        mask = adata.obs[donor_col] == donor
        vals = adata.obs.loc[mask, "dpt_pseudotime"]
        cond = adata.obs.loc[mask, condition_col].iloc[0]
        records.append({
            "donor": donor,
            "condition": cond,
            "n_cells": len(vals),
            "mean_pseudotime": vals.mean(),
            "median_pseudotime": vals.median(),
            "std_pseudotime": vals.std(),
        })
    return pd.DataFrame(records)
