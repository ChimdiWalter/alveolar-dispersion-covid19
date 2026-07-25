#!/usr/bin/env python3
"""Ablation 2: UMAP-based vs diffusion-map-based neighbor graph for pseudotime."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_02_embedding")
    results = {}
    for method in ("umap", "diffmap"):
        logger.info(f"Variant: {method}")
        alv = load_alveolar(cfg)
        # Toggle by overriding which representation feeds DPT neighbors
        cfg_v = {**cfg, "dimred": {**cfg["dimred"], "primary_rep": method}}
        alv, trends = run_workflow(alv, cfg_v, logger)
        m = core_metrics(alv, cfg_v, trends_df=trends,
                         primary_ordering=list(cfg["gene_programs"].keys()))
        m["variant"] = method
        results[method] = m
    for k, v in results.items():
        save_ablation_metrics(f"02_embedding_{k}", v, cfg)
    logger.info(f"Done. Variants: {list(results.keys())}")


if __name__ == "__main__":
    main()
