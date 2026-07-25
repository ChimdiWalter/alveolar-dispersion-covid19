#!/usr/bin/env python3
"""
End-to-end pipeline runner for the Alveolar Robustness Collapse project.

Usage:
    python scripts/run_pipeline.py                  # Run all steps
    python scripts/run_pipeline.py --step qc        # Run a specific step
    python scripts/run_pipeline.py --step trajectory --skip-if-exists

Steps:
    load_and_inspect  — Load atlas, print summary, save metadata report
    qc                — Quality control filtering
    subset            — Subset to alveolar epithelial cells + validate
    embed             — Normalize, HVG, PCA, batch correction, UMAP, diffmap
    trajectory        — Diffusion pseudotime
    programs          — Gene program scoring
    stats             — Robustness metrics and statistical tests
    figures           — Generate all main figures
    ablations         — Run all ablation experiments
    all               — Run everything in sequence
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import load_config, setup_logging, ensure_dirs


def parse_args():
    parser = argparse.ArgumentParser(description="Alveolar Robustness Collapse Pipeline")
    parser.add_argument("--step", default="all",
                        choices=["load_and_inspect", "qc", "subset", "embed",
                                 "trajectory", "programs", "stats", "figures",
                                 "ablations", "all"],
                        help="Pipeline step to run")
    parser.add_argument("--config", default=None, help="Path to config.yaml")
    parser.add_argument("--skip-if-exists", action="store_true",
                        help="Skip steps whose output files already exist")
    return parser.parse_args()


def step_load_and_inspect(cfg, logger):
    """Load the atlas and inspect its structure."""
    from src.io import load_atlas, load_metadata, save_table
    import pandas as pd

    logger.info("=" * 60)
    logger.info("STEP: Load and inspect data")
    logger.info("=" * 60)

    adata = load_atlas(cfg)
    logger.info(f"Atlas loaded: {adata.n_obs} cells × {adata.n_vars} genes")
    logger.info(f"Obs columns: {adata.obs.columns.tolist()}")
    logger.info(f"Obs dtypes:\n{adata.obs.dtypes}")

    # Print value counts for likely categorical columns
    for col in adata.obs.columns:
        if adata.obs[col].dtype == "object" or adata.obs[col].dtype.name == "category":
            vc = adata.obs[col].value_counts()
            if len(vc) < 50:
                logger.info(f"\n{col}:\n{vc}")

    # Try loading separate metadata
    meta = load_metadata(cfg)
    if not meta.empty:
        logger.info(f"Separate metadata loaded: {meta.shape}")

    return adata


def step_qc(adata, cfg, logger):
    """Run quality control."""
    from src.qc import compute_qc_metrics, apply_qc_filters, qc_summary
    from src.io import save_table

    logger.info("=" * 60)
    logger.info("STEP: Quality control")
    logger.info("=" * 60)

    adata = compute_qc_metrics(adata)
    summary = qc_summary(adata)
    logger.info(f"Pre-filter QC summary:\n{summary}")
    save_table(summary, "tableS2_qc_prefilter", cfg=cfg)

    adata = apply_qc_filters(adata, cfg)
    summary_post = qc_summary(adata)
    logger.info(f"Post-filter QC summary:\n{summary_post}")
    save_table(summary_post, "tableS2_qc_postfilter", cfg=cfg)

    return adata


def step_subset(adata, cfg, logger):
    """Subset to alveolar epithelial cells and validate annotations."""
    from src.annotation import validate_markers, subset_alveolar
    from src.io import save_table, save_adata

    logger.info("=" * 60)
    logger.info("STEP: Subset alveolar epithelial cells")
    logger.info("=" * 60)

    marker_df = validate_markers(adata, cfg["markers"],
                                  cfg["cell_types"]["annotation_column"])
    save_table(marker_df, "tableS3_marker_validation", cfg=cfg)
    logger.info("Marker validation table saved")

    alv = subset_alveolar(adata, cfg)
    logger.info(f"Alveolar subset: {alv.n_obs} cells")

    save_adata(alv, "alveolar_validated", cfg)
    return alv


def step_embed(alv, cfg, logger):
    """Normalize, HVG, PCA, batch correction, UMAP, diffusion map."""
    from src.embedding import (normalize_and_select_hvg, run_pca,
                                run_neighbors, run_umap, run_diffmap, run_harmony)
    from src.io import save_adata

    logger.info("=" * 60)
    logger.info("STEP: Embedding and manifold construction")
    logger.info("=" * 60)

    alv = normalize_and_select_hvg(alv, cfg)
    alv = run_pca(alv, cfg)

    # Batch correction if configured
    if cfg["batch_correction"].get("method") == "harmony":
        try:
            alv = run_harmony(alv, cfg)
            alv = run_neighbors(alv, cfg, use_rep="X_pca_harmony")
            logger.info("Using Harmony-corrected PCA for neighbors")
        except Exception as e:
            logger.warning(f"Harmony failed: {e}. Using uncorrected PCA.")
            alv = run_neighbors(alv, cfg)
    else:
        alv = run_neighbors(alv, cfg)

    alv = run_umap(alv, cfg)
    alv = run_diffmap(alv, cfg)

    save_adata(alv, "alveolar_embedded", cfg)
    return alv


def step_trajectory(alv, cfg, logger):
    """Run diffusion pseudotime."""
    from src.trajectory import run_dpt, pseudotime_density_by_condition, pseudotime_by_donor
    from src.io import save_adata, save_table

    logger.info("=" * 60)
    logger.info("STEP: Trajectory inference")
    logger.info("=" * 60)

    alv = run_dpt(alv, cfg)

    pt_density = pseudotime_density_by_condition(alv, cfg)
    logger.info(f"Pseudotime density:\n{pt_density}")
    save_table(pt_density, "pseudotime_by_condition", cfg=cfg)

    pt_donor = pseudotime_by_donor(alv, cfg)
    save_table(pt_donor, "tableS5_donor_statistics", cfg=cfg)

    save_adata(alv, "alveolar_pseudotime", cfg)
    return alv


def step_programs(alv, cfg, logger):
    """Score gene programs."""
    from src.programs import score_gene_programs, program_trends_along_pseudotime
    from src.io import save_adata, save_table

    logger.info("=" * 60)
    logger.info("STEP: Gene program scoring")
    logger.info("=" * 60)

    alv = score_gene_programs(alv, cfg)

    trends = program_trends_along_pseudotime(alv, cfg)
    save_table(trends, "tableS8_program_trends", cfg=cfg)

    save_adata(alv, "alveolar_programs", cfg)
    return alv, trends


def step_stats(alv, cfg, logger):
    """Run statistical tests."""
    from src.stats import (centroid_distance, displacement_test,
                           dispersion_test, permutation_test_pseudotime,
                           robustness_composite_score)
    from src.io import save_table
    import pandas as pd

    logger.info("=" * 60)
    logger.info("STEP: Statistical analysis")
    logger.info("=" * 60)

    dist_df = centroid_distance(alv, cfg)
    disp_result = displacement_test(dist_df,
                                     cfg["conditions"]["healthy_label"],
                                     cfg["conditions"]["covid_label"])
    logger.info(f"Displacement test: {disp_result}")

    var_result = dispersion_test(alv, cfg)
    logger.info(f"Dispersion test: {var_result}")

    perm_result = permutation_test_pseudotime(alv, cfg,
                                               n_perm=cfg["statistics"]["permutation_n"])
    logger.info(f"Permutation test: {perm_result}")

    composite = robustness_composite_score(disp_result, var_result, perm_result)
    logger.info(f"Composite robustness score: {composite}")

    # Save results
    metrics = pd.DataFrame([disp_result, var_result, perm_result])
    save_table(metrics, "table2_robustness_metrics", cfg=cfg)
    save_table(pd.DataFrame([composite]), "table3_composite_evidence", cfg=cfg)

    return disp_result, var_result, perm_result, composite


def step_figures(alv, cfg, trends, logger):
    """Generate all main figures."""
    from src.plots import (plot_umap_condition, plot_umap_celltype,
                           plot_umap_pseudotime, plot_pseudotime_density,
                           plot_program_trends, plot_marker_genes_pseudotime,
                           plot_displacement_boxplot, plot_donor_pseudotime,
                           save_fig)
    from src.stats import centroid_distance
    from src.trajectory import pseudotime_by_donor

    logger.info("=" * 60)
    logger.info("STEP: Figure generation")
    logger.info("=" * 60)

    fig, _ = plot_umap_condition(alv, cfg)
    save_fig(fig, "fig1a_condition", cfg["paths"]["figures"])

    fig, _ = plot_umap_celltype(alv, cfg)
    save_fig(fig, "fig1b_celltype", cfg["paths"]["figures"])

    fig, _ = plot_umap_pseudotime(alv)
    save_fig(fig, "fig2_pseudotime", cfg["paths"]["figures"])

    if trends is not None:
        fig, _ = plot_program_trends(trends)
        save_fig(fig, "fig3_program_dynamics", cfg["paths"]["figures"])

    fig, _ = plot_pseudotime_density(alv, cfg)
    save_fig(fig, "fig4_pseudotime_density", cfg["paths"]["figures"])

    fig, _ = plot_marker_genes_pseudotime(
        alv, ["SFTPC", "AGER", "KRT8", "ISG15", "CASP3", "BAX"])
    save_fig(fig, "fig5_marker_trends", cfg["paths"]["figures"])

    dist_df = centroid_distance(alv, cfg)
    fig, _ = plot_displacement_boxplot(dist_df)
    save_fig(fig, "fig5b_displacement", cfg["paths"]["figures"])

    pt_donor = pseudotime_by_donor(alv, cfg)
    fig, _ = plot_donor_pseudotime(pt_donor)
    save_fig(fig, "fig7_donor_consistency", cfg["paths"]["figures"])

    logger.info("All main figures generated")


def main():
    args = parse_args()
    cfg = load_config(args.config)
    logger = setup_logging("pipeline")
    ensure_dirs(cfg)

    logger.info("Alveolar Robustness Collapse Pipeline")
    logger.info(f"Step: {args.step}")
    logger.info(f"Config: {args.config or 'config.yaml (default)'}")

    if args.step in ("load_and_inspect", "all"):
        adata = step_load_and_inspect(cfg, logger)
        if args.step == "load_and_inspect":
            return

    if args.step in ("qc", "all"):
        if args.step == "qc":
            from src.io import load_atlas
            adata = load_atlas(cfg)
        adata = step_qc(adata, cfg, logger)
        if args.step == "qc":
            return

    if args.step in ("subset", "all"):
        if args.step == "subset":
            import anndata as ad
            from src.utils import resolve_path
            adata = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "atlas_qc.h5ad")
        alv = step_subset(adata, cfg, logger)
        if args.step == "subset":
            return

    if args.step in ("embed", "all"):
        if args.step == "embed":
            import anndata as ad
            from src.utils import resolve_path
            alv = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "alveolar_validated.h5ad")
        alv = step_embed(alv, cfg, logger)
        if args.step == "embed":
            return

    if args.step in ("trajectory", "all"):
        if args.step == "trajectory":
            import anndata as ad
            from src.utils import resolve_path
            alv = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "alveolar_embedded.h5ad")
        alv = step_trajectory(alv, cfg, logger)
        if args.step == "trajectory":
            return

    if args.step in ("programs", "all"):
        if args.step == "programs":
            import anndata as ad
            from src.utils import resolve_path
            alv = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "alveolar_pseudotime.h5ad")
        alv, trends = step_programs(alv, cfg, logger)
        if args.step == "programs":
            return

    if args.step in ("stats", "all"):
        if args.step == "stats":
            import anndata as ad
            from src.utils import resolve_path
            alv = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "alveolar_programs.h5ad")
        step_stats(alv, cfg, logger)
        if args.step == "stats":
            return

    if args.step in ("figures", "all"):
        if args.step == "figures":
            import anndata as ad
            from src.utils import resolve_path
            alv = ad.read_h5ad(resolve_path(cfg["paths"]["processed_data"]) / "alveolar_programs.h5ad")
            trends = None  # Will need to reload
        step_figures(alv, cfg, trends if 'trends' in dir() else None, logger)

    logger.info("=" * 60)
    logger.info("Pipeline complete.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
