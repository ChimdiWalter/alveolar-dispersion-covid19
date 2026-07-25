"""
Gene program scoring and trend analysis.

Primary method: Scanpy score_genes (Tirosh et al., 2016 control-gene approach).
  - Scores each cell for each gene program relative to a background of genes
    with similar expression levels.
  - Fast, deterministic, well-validated.

Alternative: AUCell (Aibar et al., 2017).
  - Ranks-based; more robust to normalization differences.
  - Better for very large gene sets or when comparing across datasets.
  - Not used as primary because score_genes is sufficient for within-dataset
    comparisons and is native to Scanpy.
"""

import logging
from typing import Optional

logger = logging.getLogger("robustness.programs")

try:
    import scanpy as sc
    import numpy as np
    import pandas as pd
except ImportError:
    pass


def score_gene_programs(adata: "sc.AnnData", cfg: dict,
                        use_raw: bool = True) -> "sc.AnnData":
    """Score all gene programs defined in config.

    For each program, adds a column 'program_{name}' to adata.obs.

    Parameters
    ----------
    adata : AnnData
        Normalized (log-transformed). If use_raw=True, scoring uses adata.raw.
    cfg : dict
    use_raw : bool
        Whether to score on the .raw layer (all genes, not just HVGs).

    Returns
    -------
    AnnData with program scores in .obs.
    """
    programs = cfg["gene_programs"]
    for name, prog_info in programs.items():
        genes = prog_info["genes"]
        # Filter to genes present in the data
        if use_raw and adata.raw is not None:
            available = [g for g in genes if g in adata.raw.var_names]
        else:
            available = [g for g in genes if g in adata.var_names]

        missing = set(genes) - set(available)
        if missing:
            logger.warning(f"Program '{name}': {len(missing)} genes not found: {missing}")

        if len(available) < 3:
            logger.warning(f"Program '{name}': only {len(available)} genes available. "
                           "Score may be unreliable.")

        score_name = f"program_{name}"
        sc.tl.score_genes(adata, gene_list=available, score_name=score_name,
                          use_raw=use_raw)
        logger.info(f"Scored '{name}': {len(available)}/{len(genes)} genes, "
                    f"stored in obs['{score_name}']")

    return adata


def score_random_control_sets(adata: "sc.AnnData", cfg: dict,
                               reference_program: str = "apoptosis",
                               n_random: int = 100,
                               seed: int = 42) -> "pd.DataFrame":
    """Score cells with random gene sets as negative controls.

    Generates n_random gene sets of the same size as the reference program
    and scores each. Returns a DataFrame of scores for comparison.

    Parameters
    ----------
    adata : AnnData
    cfg : dict
    reference_program : str
        Name of the program whose size to match.
    n_random : int
    seed : int

    Returns
    -------
    pd.DataFrame
        Shape (n_cells, n_random) with random set scores.
    """
    prog = cfg["gene_programs"][reference_program]
    prog_size = len(prog["genes"])

    if adata.raw is not None:
        all_genes = list(adata.raw.var_names)
    else:
        all_genes = list(adata.var_names)

    rng = np.random.default_rng(seed)
    random_scores = {}

    for i in range(n_random):
        random_genes = list(rng.choice(all_genes, size=prog_size, replace=False))
        score_name = f"random_ctrl_{i}"
        sc.tl.score_genes(adata, gene_list=random_genes, score_name=score_name,
                          use_raw=True)
        random_scores[score_name] = adata.obs[score_name].values
        # Clean up obs column to avoid bloat
        del adata.obs[score_name]

    return pd.DataFrame(random_scores, index=adata.obs_names)


def program_trends_along_pseudotime(adata: "sc.AnnData",
                                     cfg: dict,
                                     n_bins: int = 50) -> "pd.DataFrame":
    """Compute smoothed gene program scores along pseudotime bins.

    Parameters
    ----------
    adata : AnnData
        Must have 'dpt_pseudotime' and program score columns in .obs.
    cfg : dict
    n_bins : int

    Returns
    -------
    pd.DataFrame
        Columns: pseudotime_bin, program_name, mean_score, sem.
    """
    pt = adata.obs["dpt_pseudotime"]
    bins = pd.cut(pt, bins=n_bins, labels=False)

    program_names = [f"program_{name}" for name in cfg["gene_programs"]]
    available = [p for p in program_names if p in adata.obs.columns]

    records = []
    for b in range(n_bins):
        mask = bins == b
        n = mask.sum()
        if n == 0:
            continue
        pt_center = pt[mask].mean()
        for prog in available:
            vals = adata.obs.loc[mask, prog]
            records.append({
                "pseudotime_bin": b,
                "pseudotime_center": pt_center,
                "program": prog.replace("program_", ""),
                "mean_score": vals.mean(),
                "sem": vals.std() / np.sqrt(n) if n > 1 else 0,
                "n_cells": n,
            })

    return pd.DataFrame(records)
