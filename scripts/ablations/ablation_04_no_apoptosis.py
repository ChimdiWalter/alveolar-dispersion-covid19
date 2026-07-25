#!/usr/bin/env python3
"""Ablation 4: Remove apoptosis genes from HVG set before manifold construction.

Tests whether the trajectory is an artifact of apoptosis-driven variance.
If pseudotime ordering survives, the trajectory reflects coordinated
state change beyond dying-cell signal.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_04_no_apoptosis")
    alv = load_alveolar(cfg)
    apop = set(cfg["gene_programs"]["apoptosis"]["genes"])
    keep = [g for g in alv.var_names if g not in apop]
    logger.info(f"Removing {alv.n_vars - len(keep)} apoptosis genes before HVG")
    alv = alv[:, keep].copy()
    # Drop apoptosis program from scoring since its genes were removed.
    cfg_noapop = {**cfg, "gene_programs": {k: v for k, v in cfg["gene_programs"].items()
                                           if k != "apoptosis"}}
    alv, trends = run_workflow(alv, cfg_noapop, logger)
    m = core_metrics(alv, cfg_noapop, trends_df=trends,
                     primary_ordering=list(cfg_noapop["gene_programs"].keys()))
    save_ablation_metrics("04_no_apoptosis_genes", m, cfg)
    logger.info(f"Done: {m}")


if __name__ == "__main__":
    main()
