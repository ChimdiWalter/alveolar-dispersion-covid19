#!/usr/bin/env python3
"""Ablation 6: Include airway epithelial populations (Club, Ciliated, Basal).

Tests whether the failure trajectory is specific to the alveolar compartment
or shared with airway epithelial injury states.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, run_workflow,
                    core_metrics, save_ablation_metrics, resolve_path)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_06_broader_epithelial")
    # Reload raw atlas, re-run QC, then subset to broader epithelial types.
    # (The main pipeline does not persist the full post-QC atlas.)
    from src.io import load_atlas
    from src.qc import compute_qc_metrics, apply_qc_filters
    atlas = load_atlas(cfg)
    atlas = compute_qc_metrics(atlas)
    atlas = apply_qc_filters(atlas, cfg)
    col = cfg["cell_types"]["annotation_column"]
    keep = cfg["cell_types"]["broader_epithelial"]
    mask = atlas.obs[col].astype(str).isin(keep)
    alv = atlas[mask].copy()
    logger.info(f"Broader epithelial subset: {alv.n_obs} cells ({keep})")
    alv, trends = run_workflow(alv, cfg, logger)
    m = core_metrics(alv, cfg, trends_df=trends,
                     primary_ordering=list(cfg["gene_programs"].keys()))
    save_ablation_metrics("06_broader_epithelial", m, cfg)


if __name__ == "__main__":
    main()
