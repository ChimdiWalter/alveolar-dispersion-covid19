"""Shared helpers for ablation experiments.

Each ablation:
  1. Loads the validated alveolar subset (or full atlas where required)
  2. Modifies one component of the primary workflow
  3. Reruns embed → trajectory → programs → stats
  4. Writes metrics to results/ablations/{ablation_name}/metrics.csv
  5. Compares the three core metrics (median pseudotime diff, program ordering
     rank correlation, displacement effect size) against the primary analysis
"""

from pathlib import Path
import sys
import json
import logging
import pandas as pd
from scipy.stats import spearmanr

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import load_config, setup_logging, resolve_path  # noqa: E402


def ablation_output_dir(name, cfg=None):
    cfg = cfg or load_config()
    out = resolve_path(cfg["paths"]["results"]) / "ablations" / name
    out.mkdir(parents=True, exist_ok=True)
    return out


def load_alveolar(cfg):
    """Load the validated alveolar subset (output of step_subset)."""
    import anndata as ad
    path = resolve_path(cfg["paths"]["processed_data"]) / "alveolar_validated.h5ad"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python scripts/run_pipeline.py --step subset` first."
        )
    return ad.read_h5ad(path)


def core_metrics(alv, cfg, trends_df=None, primary_ordering=None):
    """Compute the 3 comparison metrics for an ablation run."""
    from src.trajectory import pseudotime_density_by_condition
    from src.stats import centroid_distance, displacement_test

    pt = pseudotime_density_by_condition(alv, cfg)
    healthy_med = pt.loc[pt["condition"] == cfg["conditions"]["healthy_label"], "median_pseudotime"].iloc[0]
    covid_med = pt.loc[pt["condition"] == cfg["conditions"]["covid_label"], "median_pseudotime"].iloc[0]
    median_diff = covid_med - healthy_med

    dist = centroid_distance(alv, cfg)
    disp = displacement_test(dist, cfg["conditions"]["healthy_label"],
                             cfg["conditions"]["covid_label"])

    ordering_corr = None
    if trends_df is not None and primary_ordering is not None:
        # rank correlation of program peak pseudotime ordering
        # Compute peak (pseudotime_center at argmax of mean_score) per program.
        peaks = (trends_df.sort_values("mean_score", ascending=False)
                 .groupby("program", as_index=False).first()
                 .sort_values("pseudotime_center"))
        order = peaks["program"].tolist()
        common = [p for p in primary_ordering if p in order]
        if len(common) >= 3:
            rank_here = [order.index(p) for p in common]
            rank_primary = [primary_ordering.index(p) for p in common]
            rho, _ = spearmanr(rank_here, rank_primary)
            ordering_corr = float(rho)

    return {
        "median_pseudotime_diff": float(median_diff),
        "displacement_effect_size": float(disp.get("effect_size_r",
                                         disp.get("effect_size", disp.get("r", 0.0)))),
        "program_ordering_rho": ordering_corr,
    }


def save_ablation_metrics(name, metrics, cfg=None):
    out = ablation_output_dir(name, cfg)
    pd.DataFrame([metrics]).to_csv(out / "metrics.csv", index=False)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return out


def run_workflow(alv, cfg, logger=None, batch_correct=True, root_strategy=None):
    """Run embed → trajectory → programs on an AnnData object and return metrics-ready state."""
    from src.embedding import (normalize_and_select_hvg, run_pca, run_neighbors,
                                run_umap, run_diffmap, run_harmony)
    from src.trajectory import run_dpt
    from src.programs import score_gene_programs, program_trends_along_pseudotime

    alv = normalize_and_select_hvg(alv, cfg)
    alv = run_pca(alv, cfg)

    if batch_correct and cfg["batch_correction"].get("method") == "harmony":
        try:
            alv = run_harmony(alv, cfg)
            alv = run_neighbors(alv, cfg, use_rep="X_pca_harmony")
        except Exception as e:
            if logger:
                logger.warning(f"Harmony failed: {e}; falling back to uncorrected PCA.")
            alv = run_neighbors(alv, cfg)
    else:
        alv = run_neighbors(alv, cfg)

    alv = run_umap(alv, cfg)
    alv = run_diffmap(alv, cfg)
    if root_strategy is not None:
        cfg = {**cfg, "trajectory": {**cfg["trajectory"], "root_strategy": root_strategy}}
    alv = run_dpt(alv, cfg)
    alv = score_gene_programs(alv, cfg)
    trends = program_trends_along_pseudotime(alv, cfg)
    return alv, trends
