#!/usr/bin/env python3
"""Ablation 9: Palantir as an alternative trajectory algorithm."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar,
                    core_metrics, save_ablation_metrics)


def main():
    cfg = load_config()
    logger = setup_logging("ablation_09_palantir")
    try:
        import palantir  # noqa: F401
    except ImportError:
        logger.error("palantir not installed. Skipping ablation 9.")
        save_ablation_metrics("09_palantir", {"error": "palantir_not_installed"}, cfg)
        return

    from src.embedding import normalize_and_select_hvg, run_pca, run_neighbors, run_diffmap
    from src.programs import score_gene_programs, program_trends_along_pseudotime
    from src.trajectory import find_root_cell
    import palantir
    import pandas as pd

    alv = load_alveolar(cfg)
    alv = normalize_and_select_hvg(alv, cfg)
    alv = run_pca(alv, cfg)
    alv = run_neighbors(alv, cfg)
    alv = run_diffmap(alv, cfg)

    root_idx = find_root_cell(alv, cfg, strategy=cfg["trajectory"]["root_strategy"])
    dm_res = palantir.utils.run_diffusion_maps(
        pd.DataFrame(alv.obsm["X_pca"][:, :cfg["dimred"]["n_pcs"]],
                     index=alv.obs_names))
    ms_data = palantir.utils.determine_multiscale_space(dm_res)
    pr = palantir.core.run_palantir(
        ms_data, alv.obs_names[root_idx],
        num_waypoints=cfg["trajectory"]["palantir"]["n_waypoints"])
    alv.obs["palantir_pseudotime"] = pr.pseudotime.values
    alv.obs["dpt_pseudotime"] = alv.obs["palantir_pseudotime"]  # alias for downstream
    alv = score_gene_programs(alv, cfg)
    trends = program_trends_along_pseudotime(alv, cfg)
    m = core_metrics(alv, cfg, trends_df=trends,
                     primary_ordering=list(cfg["gene_programs"].keys()))
    save_ablation_metrics("09_palantir", m, cfg)
    logger.info(f"Done: {m}")


if __name__ == "__main__":
    main()
