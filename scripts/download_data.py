#!/usr/bin/env python3
"""
Download helper for SCP1219 (Columbia/NYP COVID-19 Lung Atlas).

The Broad Single Cell Portal requires authentication (Google account + Terra
credentials) to download data programmatically. This script does not bypass
that — it prints the exact steps needed and verifies the expected files once
they arrive in data/raw/.

Options:
    1. Portal UI  : https://singlecell.broadinstitute.org/single_cell/study/SCP1219
                    Click "Download" → select the .h5ad or matrix bundle.
    2. scp-cli    : pip install scp-tools && scp auth login; scp download SCP1219
    3. Alternative mirrors: see PROJECT_STATUS.md for cached copies if approved.

After download, run:
    python scripts/download_data.py --verify
"""

import argparse
import hashlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"

EXPECTED = [
    # (filename glob, minimum size in MB, description)
    ("gene_sorted-lung_expression_data.mtx.gz", 500, "SCP1219 expression matrix (genes x cells)"),
    ("lung_cellNames.csv", 1, "Cell barcodes"),
    ("lung_geneNames_upload.csv", 0.1, "Gene names"),
    ("lung_metaData.txt", 1, "Cell metadata (condition/cell_type/donor)"),
    ("lung_clusterfile.txt", 1, "Published UMAP coordinates"),
]


def verify():
    RAW.mkdir(parents=True, exist_ok=True)
    found = []
    for pattern, min_mb, desc in EXPECTED:
        matches = list(RAW.glob(pattern))
        for m in matches:
            size_mb = m.stat().st_size / 1e6
            status = "OK " if size_mb >= min_mb else "SMALL"
            found.append((status, m.name, f"{size_mb:.1f} MB", desc))
    if not found:
        print(f"No data files found in {RAW}")
        print("Download SCP1219 from the portal and place files in data/raw/")
        return 1
    print(f"{'Status':<6} {'File':<50} {'Size':<12} {'Purpose'}")
    print("-" * 100)
    for row in found:
        print(f"{row[0]:<6} {row[1]:<50} {row[2]:<12} {row[3]}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verify", action="store_true", help="Check data/raw/ contents")
    args = p.parse_args()
    if args.verify:
        sys.exit(verify())
    else:
        print(__doc__)
        print(f"\nPlace downloaded files into: {RAW}")


if __name__ == "__main__":
    main()
