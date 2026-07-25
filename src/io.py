"""
Data loading, saving, and path management.
"""

from pathlib import Path
import logging

logger = logging.getLogger("robustness.io")

try:
    import anndata as ad
    import scanpy as sc
    import pandas as pd
except ImportError as e:
    logger.warning(f"Optional dependency not installed: {e}")

from .utils import load_config, resolve_path, PROJECT_ROOT


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_atlas(cfg: dict | None = None) -> "ad.AnnData":
    """Load the full SCP1219 atlas from the raw data directory.

    Supports:
      - Cached h5ad: data/raw/*.h5ad (preferred — written on first load)
      - SCP1219 native layout (Melms et al. 2021):
          gene_sorted-lung_expression_data.mtx.gz  (genes x cells)
          lung_cellNames.csv                       (one barcode per line)
          lung_geneNames_upload.csv                (one gene per line)
          lung_metaData.txt                        (TSV with SCP TYPE header row)
      - Generic 10X mtx/h5

    Parameters
    ----------
    cfg : dict, optional
        Project config. Loaded from config.yaml if None.

    Returns
    -------
    anndata.AnnData
        The full, unprocessed atlas with metadata attached to .obs.
    """
    if cfg is None:
        cfg = load_config()
    raw_dir = resolve_path(cfg["paths"]["raw_data"])

    # Cached h5ad first (fastest)
    h5ad_files = list(raw_dir.glob("*.h5ad"))
    if h5ad_files:
        path = h5ad_files[0]
        logger.info(f"Loading cached h5ad: {path}")
        return ad.read_h5ad(path)

    # SCP1219 native layout
    scp_mtx = raw_dir / "gene_sorted-lung_expression_data.mtx.gz"
    if scp_mtx.exists():
        return _load_scp1219(raw_dir)

    # Generic 10X mtx
    mtx_files = list(raw_dir.glob("*.mtx*"))
    if mtx_files:
        logger.info(f"Loading 10X mtx from: {raw_dir}")
        return sc.read_10x_mtx(raw_dir, var_names="gene_symbols")

    # 10X HDF5
    h5_files = list(raw_dir.glob("*.h5"))
    if h5_files:
        path = h5_files[0]
        logger.info(f"Loading 10X h5: {path}")
        return sc.read_10x_h5(path)

    raise FileNotFoundError(
        f"No recognized data files in {raw_dir}. "
        "Place SCP1219 data (gene_sorted-lung_expression_data.mtx.gz + "
        "lung_cellNames.csv + lung_geneNames_upload.csv + lung_metaData.txt) "
        "or a cached .h5ad in data/raw/"
    )


def _load_scp1219(raw_dir: Path) -> "ad.AnnData":
    """Load SCP1219 native file layout into AnnData (cells x genes)."""
    import gzip
    import numpy as np
    import pandas as pd
    import scipy.io as sio
    import scipy.sparse as sp

    mtx_path = raw_dir / "gene_sorted-lung_expression_data.mtx.gz"
    cells_path = raw_dir / "lung_cellNames.csv"
    genes_path = raw_dir / "lung_geneNames_upload.csv"
    meta_path = raw_dir / "lung_metaData.txt"

    logger.info(f"Loading SCP1219 MTX: {mtx_path}")
    with gzip.open(mtx_path, "rb") as fh:
        mat = sio.mmread(fh)           # COO, genes x cells per SCP convention
    mat = sp.csr_matrix(mat)

    cells = pd.read_csv(cells_path, header=None)[0].astype(str).tolist()
    genes = pd.read_csv(genes_path, header=None)[0].astype(str).tolist()

    # Orient as cells x genes
    if mat.shape == (len(genes), len(cells)):
        mat = mat.T.tocsr()
    elif mat.shape != (len(cells), len(genes)):
        raise ValueError(
            f"Matrix shape {mat.shape} matches neither "
            f"(genes={len(genes)}, cells={len(cells)}) nor its transpose."
        )

    adata = ad.AnnData(X=mat)
    adata.obs_names = cells
    adata.var_names = genes
    adata.var_names_make_unique()

    # Metadata: SCP convention has a TYPE row (row 2) after the header
    logger.info(f"Loading SCP1219 metadata: {meta_path}")
    meta = pd.read_csv(meta_path, sep="\t", skiprows=[1], index_col=0)
    # Align to obs order (some cells may lack metadata; left-join preserves obs)
    meta = meta.reindex(adata.obs_names)
    missing = meta.isna().all(axis=1).sum()
    if missing:
        logger.warning(f"{missing} cells have no metadata entry")
    adata.obs = adata.obs.join(meta)

    logger.info(
        f"SCP1219 loaded: {adata.n_obs} cells x {adata.n_vars} genes; "
        f"obs columns: {list(adata.obs.columns)[:8]}..."
    )
    return adata


def load_metadata(cfg: dict | None = None) -> "pd.DataFrame":
    """Load cell-level metadata from the metadata directory.

    Parameters
    ----------
    cfg : dict, optional
        Project config.

    Returns
    -------
    pd.DataFrame
    """
    if cfg is None:
        cfg = load_config()
    meta_dir = resolve_path(cfg["paths"]["metadata"])
    csv_files = list(meta_dir.glob("*.csv")) + list(meta_dir.glob("*.tsv"))
    if not csv_files:
        logger.warning("No metadata CSV/TSV found in metadata/. "
                       "Metadata may be embedded in the h5ad.")
        return pd.DataFrame()
    path = csv_files[0]
    sep = "\t" if path.suffix == ".tsv" else ","
    logger.info(f"Loading metadata: {path}")
    return pd.read_csv(path, sep=sep, index_col=0)


# ---------------------------------------------------------------------------
# Saving
# ---------------------------------------------------------------------------

def save_adata(adata: "ad.AnnData", name: str, cfg: dict | None = None) -> Path:
    """Save an AnnData object to the processed data directory.

    Parameters
    ----------
    adata : anndata.AnnData
    name : str
        Filename stem (e.g., "alveolar_qc"). Extension .h5ad added automatically.
    cfg : dict, optional

    Returns
    -------
    Path to saved file.
    """
    if cfg is None:
        cfg = load_config()
    out_dir = resolve_path(cfg["paths"]["processed_data"])
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.h5ad"
    logger.info(f"Saving AnnData → {path}")
    adata.write_h5ad(path)
    return path


def save_table(df: "pd.DataFrame", name: str, subdir: str = "tables",
               cfg: dict | None = None) -> Path:
    """Save a DataFrame as CSV to results/tables/.

    Parameters
    ----------
    df : pd.DataFrame
    name : str
        Filename stem.
    subdir : str
        Subdirectory under results/.
    cfg : dict, optional

    Returns
    -------
    Path to saved file.
    """
    if cfg is None:
        cfg = load_config()
    out_dir = resolve_path(cfg["paths"][subdir]) if subdir in cfg.get("paths", {}) else resolve_path(f"results/{subdir}")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.csv"
    logger.info(f"Saving table → {path}")
    df.to_csv(path)
    return path
