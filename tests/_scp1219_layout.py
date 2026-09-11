"""
Write an AnnData to disk in the native SCP1219 file layout that
src/io.py::_load_scp1219 expects, so that loader can be exercised without
a real download.
"""

import gzip
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.io as sio
import scipy.sparse as sp
import anndata as ad


def write_scp1219_layout(adata: "ad.AnnData", out_dir: Path) -> None:
    """Write `adata` (cells x genes) as SCP1219-formatted raw files into out_dir.

    Files written:
      - gene_sorted-lung_expression_data.mtx.gz  (genes x cells, per SCP convention)
      - lung_cellNames.csv                       (one barcode per line, no header)
      - lung_geneNames_upload.csv                (one gene per line, no header)
      - lung_metaData.txt                        (TSV, row 2 is a "TYPE" row per SCP convention)
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # SCP convention stores the matrix as genes x cells.
    mat = sp.coo_matrix(adata.X).T
    with gzip.open(out_dir / "gene_sorted-lung_expression_data.mtx.gz", "wb") as fh:
        sio.mmwrite(fh, mat)

    pd.Series(adata.obs_names).to_csv(
        out_dir / "lung_cellNames.csv", header=False, index=False
    )
    pd.Series(adata.var_names).to_csv(
        out_dir / "lung_geneNames_upload.csv", header=False, index=False
    )

    meta = adata.obs.copy()
    meta.index.name = "NAME"
    type_row = pd.DataFrame(
        [["TYPE"] + ["group" for _ in meta.columns]], columns=["NAME"] + list(meta.columns)
    )

    meta_path = out_dir / "lung_metaData.txt"
    with open(meta_path, "w", newline="") as fh:
        header = "\t".join(["NAME"] + list(meta.columns)) + "\n"
        fh.write(header)
        fh.write("\t".join(type_row.iloc[0].astype(str)) + "\n")
        meta.to_csv(fh, sep="\t", header=False)
