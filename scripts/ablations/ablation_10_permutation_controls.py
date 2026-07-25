#!/usr/bin/env python3
"""Ablation 10: Permutation and random-gene-set null controls.

(A) Shuffle condition labels N times and recompute median pseudotime difference
    → empirical null distribution of the condition effect.
(B) Sample random gene sets matched to apoptosis-program size and score pseudotime
    correlations → null distribution for program-level activity.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, ablation_output_dir, resolve_path)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_10_permutation_controls")
    import anndata as ad
    alv = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "alveolar_programs.h5ad")

    from src.stats import permutation_test_pseudotime
    from src.programs import score_random_control_sets

    # (A) permutation test for condition vs pseudotime
    perm = permutation_test_pseudotime(alv, cfg,
                                       n_perm=cfg["statistics"]["permutation_n"])
    logger.info(f"Permutation test: {perm}")

    # (B) random gene-set controls
    target_size = len(cfg["gene_programs"]["apoptosis"]["genes"])
    random_scores = score_random_control_sets(
        alv, cfg,
        reference_program="apoptosis",
        n_random=cfg["statistics"]["random_geneset_n"],
    )
    real_rhos = {p: float(alv.obs[f"{p}_score"].corr(alv.obs["dpt_pseudotime"], method="spearman"))
                 for p in cfg["gene_programs"].keys()
                 if f"{p}_score" in alv.obs.columns}

    out = ablation_output_dir("10_permutation_controls", cfg)
    pd.DataFrame([perm]).to_csv(out / "perm_condition.csv", index=False)
    pd.DataFrame(random_scores).to_csv(out / "random_geneset_rhos.csv", index=False)
    pd.DataFrame([real_rhos]).to_csv(out / "real_program_rhos.csv", index=False)
    logger.info(f"Done. Outputs in {out}")


if __name__ == "__main__":
    main()
