"""
Dimensionality reduction, manifold construction, and batch correction.

Primary methods:
  - PCA → nearest-neighbor graph → UMAP (standard visualization)
  - Diffusion maps (continuous-transition-preserving embedding)
  - Harmony for batch correction (lightweight, fast, no GPU required)

Why these choices:
  - PCA/UMAP is the community standard and makes results comparable to
    published COVID-19 lung atlas studies.
  - Diffusion maps are specifically suited for trajectory analysis because
    they model data as a random walk on a graph, naturally capturing
    continuous transitions (Haghverdi et al., 2016).
  - Harmony is preferred over scVI for the primary analysis because it is
    deterministic, fast, and well-validated for donor/batch integration in
    lung atlases. scVI is available as an ablation alternative.

Alternatives:
  - scVI (deep generative model) — better for very large batch effects but
    introduces stochasticity and requires GPU for speed.
  - BBKNN — batch-balanced k-nearest neighbors; lighter-weight but less
    widely used.
  - scanorama — good for integration of separate datasets; less relevant
    here (single atlas).
"""

import logging

logger = logging.getLogger("robustness.embedding")

try:
    import scanpy as sc
    import numpy as np
except ImportError:
    pass


def normalize_and_select_hvg(adata: "sc.AnnData", cfg: dict) -> "sc.AnnData":
    """Normalize, log-transform, and select highly variable genes.

    Parameters
    ----------
    adata : AnnData
        QC-filtered, raw counts.
    cfg : dict
        Project config.

    Returns
    -------
    AnnData with .raw set to full normalized data, filtered to HVGs.
    """
    norm_cfg = cfg["normalization"]
    fs_cfg = cfg["feature_selection"]

    # Normalize
    sc.pp.normalize_total(adata, target_sum=norm_cfg["target_sum"])
    if norm_cfg["log_transform"]:
        sc.pp.log1p(adata)

    # Store full normalized data before HVG subsetting
    adata.raw = adata

    # HVG selection
    sc.pp.highly_variable_genes(
        adata,
        n_top_genes=fs_cfg["n_top_genes"],
        flavor=fs_cfg["method"],
        batch_key=fs_cfg.get("batch_key"),
    )
    n_hvg = adata.var["highly_variable"].sum()
    logger.info(f"Selected {n_hvg} highly variable genes")

    adata = adata[:, adata.var["highly_variable"]].copy()
    return adata


def run_pca(adata: "sc.AnnData", cfg: dict) -> "sc.AnnData":
    """Run PCA with optional scaling.

    Parameters
    ----------
    adata : AnnData
        Normalized, HVG-filtered.
    cfg : dict

    Returns
    -------
    AnnData with PCA in .obsm['X_pca'].
    """
    n_pcs = cfg["dimred"]["n_pcs"]
    sc.pp.scale(adata, max_value=10)
    sc.tl.pca(adata, n_comps=n_pcs, svd_solver="arpack")
    logger.info(f"PCA computed: {n_pcs} components, "
                f"variance explained = {adata.uns['pca']['variance_ratio'][:5].sum():.2%} (top 5)")
    return adata


def run_neighbors(adata: "sc.AnnData", cfg: dict,
                  use_rep: str = "X_pca") -> "sc.AnnData":
    """Build nearest-neighbor graph.

    Parameters
    ----------
    adata : AnnData
    cfg : dict
    use_rep : str
        Representation to use. 'X_pca' (default) or 'X_pca_harmony'.

    Returns
    -------
    AnnData with neighbor graph.
    """
    n_neighbors = cfg["dimred"]["n_neighbors"]
    n_pcs = cfg["dimred"]["n_pcs"]
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=n_pcs, use_rep=use_rep)
    logger.info(f"Neighbor graph built: k={n_neighbors}, rep={use_rep}")
    return adata


def run_umap(adata: "sc.AnnData", cfg: dict) -> "sc.AnnData":
    """Compute UMAP embedding.

    Parameters
    ----------
    adata : AnnData
        Must have neighbor graph computed.
    cfg : dict

    Returns
    -------
    AnnData with .obsm['X_umap'].
    """
    umap_cfg = cfg["dimred"]["umap"]
    sc.tl.umap(adata, min_dist=umap_cfg["min_dist"], spread=umap_cfg["spread"],
               random_state=umap_cfg["random_state"])
    logger.info("UMAP embedding computed")
    return adata


def run_diffmap(adata: "sc.AnnData", cfg: dict) -> "sc.AnnData":
    """Compute diffusion map embedding.

    Diffusion maps are preferred for trajectory analysis because they
    model transitions as a diffusion process on the cell-cell graph,
    preserving continuous gradients between states.

    Parameters
    ----------
    adata : AnnData
        Must have neighbor graph computed.
    cfg : dict

    Returns
    -------
    AnnData with .obsm['X_diffmap'].
    """
    n_comps = cfg["dimred"]["diffmap"]["n_comps"]
    sc.tl.diffmap(adata, n_comps=n_comps)
    logger.info(f"Diffusion map computed: {n_comps} components")
    return adata


def run_harmony(adata: "sc.AnnData", cfg: dict) -> "sc.AnnData":
    """Apply Harmony batch correction on PCA space.

    Parameters
    ----------
    adata : AnnData
        Must have PCA computed.
    cfg : dict

    Returns
    -------
    AnnData with .obsm['X_pca_harmony'].
    """
    try:
        import harmonypy
    except ImportError:
        logger.error("harmonypy not installed. Run: pip install harmonypy")
        raise

    batch_key = cfg["batch_correction"]["batch_key"]
    harmony_cfg = cfg["batch_correction"]["harmony"]

    ho = harmonypy.run_harmony(
        adata.obsm["X_pca"],
        adata.obs,
        batch_key,
        max_iter_harmony=harmony_cfg["max_iter_harmony"],
        sigma=harmony_cfg["sigma"],
    )
    # harmonypy >= 0.2 (PyTorch backend) returns Z_corr as (cells, PCs).
    # Older releases returned (PCs, cells) which required a transpose; we now
    # detect orientation by matching the n_obs axis, so either layout works.
    Z = ho.Z_corr
    if Z.shape[0] != adata.n_obs and Z.shape[1] == adata.n_obs:
        Z = Z.T
    adata.obsm["X_pca_harmony"] = Z
    logger.info(f"Harmony batch correction applied on key '{batch_key}'")
    return adata
