#!/usr/bin/env python3
"""Ablation 5: Sensitivity to pseudotime root-cell choice."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_05_root")
    roots = cfg["trajectory"]["alternative_roots"] + [cfg["trajectory"]["root_strategy"]]
    for root in roots:
        logger.info(f"Root strategy: {root}")
        alv = load_alveolar(cfg)
        alv, trends = run_workflow(alv, cfg, logger, root_strategy=root)
        m = core_metrics(alv, cfg, trends_df=trends,
                         primary_ordering=list(cfg["gene_programs"].keys()))
        m["root_strategy"] = root
        save_ablation_metrics(f"05_root_{root}", m, cfg)


if __name__ == "__main__":
    main()
