#!/usr/bin/env python3
"""Ablation 7: Leave-one-donor-out sensitivity analysis."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics, ablation_output_dir)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_07_leave_one_donor_out")
    alv_all = load_alveolar(cfg)
    donor_key = cfg["batch_correction"]["batch_key"]
    donors = alv_all.obs[donor_key].astype(str).unique().tolist()
    logger.info(f"Iterating over {len(donors)} donors")

    all_rows = []
    for i, donor in enumerate(donors):
        logger.info(f"[{i+1}/{len(donors)}] Leaving out: {donor}")
        alv = alv_all[alv_all.obs[donor_key].astype(str) != donor].copy()
        try:
            alv, trends = run_workflow(alv, cfg, logger)
            m = core_metrics(alv, cfg, trends_df=trends,
                             primary_ordering=list(cfg["gene_programs"].keys()))
        except Exception as e:
            logger.warning(f"Donor {donor} failed: {e}")
            m = {"error": str(e)}
        m["left_out_donor"] = donor
        all_rows.append(m)

    out = ablation_output_dir("07_leave_one_donor_out", cfg)
    pd.DataFrame(all_rows).to_csv(out / "loo_metrics.csv", index=False)
    logger.info(f"Done. Wrote {out/'loo_metrics.csv'}")


if __name__ == "__main__":
    main()
