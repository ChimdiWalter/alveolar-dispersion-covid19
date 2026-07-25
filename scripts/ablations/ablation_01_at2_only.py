#!/usr/bin/env python3
"""Ablation 1: AT2 cells only (excludes AT1 and transitional)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_01_at2_only")
    alv = load_alveolar(cfg)

    col = cfg["cell_types"]["annotation_column"]
    mask = alv.obs[col].astype(str).str.contains("AT2", case=False, na=False)
    alv = alv[mask].copy()
    logger.info(f"AT2-only subset: {alv.n_obs} cells")

    alv, trends = run_workflow(alv, cfg, logger)
    metrics = core_metrics(alv, cfg, trends_df=trends,
                           primary_ordering=list(cfg["gene_programs"].keys()))
    metrics["n_cells"] = int(alv.n_obs)
    out = save_ablation_metrics("01_at2_only", metrics, cfg)
    trends.to_csv(out / "program_trends.csv", index=False)
    logger.info(f"Done. Metrics: {metrics}")


if __name__ == "__main__":
    main()
