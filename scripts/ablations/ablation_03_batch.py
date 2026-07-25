#!/usr/bin/env python3
"""Ablation 3: With vs without Harmony batch correction."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_03_batch")
    for corrected in (True, False):
        logger.info(f"Variant: batch_correct={corrected}")
        alv = load_alveolar(cfg)
        alv, trends = run_workflow(alv, cfg, logger, batch_correct=corrected)
        m = core_metrics(alv, cfg, trends_df=trends,
                         primary_ordering=list(cfg["gene_programs"].keys()))
        m["batch_correct"] = corrected
        save_ablation_metrics(f"03_batch_{'corrected' if corrected else 'uncorrected'}",
                              m, cfg)


if __name__ == "__main__":
    main()
