#!/usr/bin/env python3
"""
Run all paper_v3 analyses: donor-level inference, state scores, mechanism.

Outputs:
  results/v3/donor_summary.csv
  results/v3/donor_level_tests.json
  results/v3/donor_bootstrap_ci.json
  results/v3/mixed_effects.json
  results/v3/donor_dispersion.json
  results/v3/state_scores.csv
  results/v3/state_score_benchmarks.csv
  results/v3/program_geometry_linkage.csv
  results/v3/fan_out_contribution.csv
  results/v3/repair_stall.json
  results/v3/replication_state_scores.csv
  results/v3/replication_state_benchmarks.csv
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from donor_models import (
    donor_bootstrap_ci,
    donor_dispersion_comparison,
    donor_level_test,
    donor_summary,
    mixed_effects_pseudotime,
)
from mechanism import (
    fan_out_contribution,
    program_geometry_linkage,
    repair_stall_analysis,
)
from state_score import benchmark_scores, score_all

OUT = ROOT / "results" / "v3"
OUT.mkdir(parents=True, exist_ok=True)

with open(ROOT / "config.yaml") as f:
    cfg = yaml.safe_load(f)


def save_json(obj, name):
    with open(OUT / name, "w") as f:
        json.dump(obj, f, indent=2, default=str)
    print(f"  -> {OUT / name}")


# ── Load primary atlas ──────────────────────────────────────────────────
print("Loading primary atlas...")
adata = sc.read_h5ad(ROOT / "data" / "processed" / "alveolar_programs.h5ad")
print(f"  {adata.shape[0]} cells, {adata.shape[1]} genes, {adata.obs['donor_id'].nunique()} donors")

# ═══════════════════════════════════════════════════════════════════════
# 1. DONOR-LEVEL ANALYSES
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("1. DONOR-LEVEL ANALYSES")
print("=" * 70)

# 1a. Donor summary
print("\n1a. Computing donor summary...")
donor_df = donor_summary(adata, cfg)
donor_df.to_csv(OUT / "donor_summary.csv", index=False)
print(f"  -> {OUT / 'donor_summary.csv'}")
print(f"  {len(donor_df)} donors: {(donor_df['condition']=='Control').sum()} Control, {(donor_df['condition']=='COVID-19').sum()} COVID-19")
print(f"  Median pseudotime — Control: {donor_df.loc[donor_df['condition']=='Control', 'median_pseudotime'].median():.4f}, COVID-19: {donor_df.loc[donor_df['condition']=='COVID-19', 'median_pseudotime'].median():.4f}")

# 1b. Donor-level tests
print("\n1b. Running donor-level tests...")
test_metrics = ["median_pseudotime", "within_donor_dispersion", "frac_transitional",
                "median_dist_to_donor_centroid", "iqr_pseudotime"]
tests = {}
for metric in test_metrics:
    if metric in donor_df.columns:
        result = donor_level_test(donor_df, metric)
        tests[metric] = result
        p = result.get("p_two_sided", result.get("error", "N/A"))
        print(f"  {metric}: p={p}, COVID median={result.get('covid_median', 'N/A'):.4f}, Healthy median={result.get('healthy_median', 'N/A'):.4f}")
save_json(tests, "donor_level_tests.json")

# 1c. Bootstrap CIs
print("\n1c. Computing bootstrap CIs (10,000 resamples)...")
boot_metrics = ["median_pseudotime", "within_donor_dispersion", "frac_transitional"]
boot_results = {}
for metric in boot_metrics:
    if metric in donor_df.columns:
        result = donor_bootstrap_ci(donor_df, metric, n_boot=10000)
        boot_results[metric] = result
        print(f"  {metric}: diff={result['observed_diff']:.4f}, 95% CI=[{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]")
save_json(boot_results, "donor_bootstrap_ci.json")

# 1d. Mixed-effects model
print("\n1d. Running mixed-effects model (OLS)...")
me_result = mixed_effects_pseudotime(donor_df)
print(f"  coefficient={me_result.get('coefficient_is_covid', 'N/A')}, p={me_result.get('p_value_is_covid', 'N/A')}")
print(f"  CI=[{me_result.get('ci_lower', 'N/A')}, {me_result.get('ci_upper', 'N/A')}], R²={me_result.get('r_squared', 'N/A')}")
save_json(me_result, "mixed_effects.json")

# 1e. Donor-level dispersion comparison
print("\n1e. Running donor-level dispersion comparison...")
disp_result = donor_dispersion_comparison(adata, cfg)
disp_for_json = {k: v for k, v in disp_result.items() if k != "donor_dispersion_df"}
if "donor_dispersion_df" in disp_result:
    disp_result["donor_dispersion_df"].to_csv(OUT / "donor_dispersion_detail.csv", index=False)
    print(f"  -> {OUT / 'donor_dispersion_detail.csv'}")
print(f"  COVID median dispersion: {disp_for_json.get('covid_median_dispersion', 'N/A'):.4f}")
print(f"  Healthy median dispersion: {disp_for_json.get('healthy_median_dispersion', 'N/A'):.4f}")
print(f"  MW p={disp_for_json.get('mannwhitney_p', 'N/A')}, Levene p={disp_for_json.get('levene_p', 'N/A')}")
save_json(disp_for_json, "donor_dispersion.json")

# ═══════════════════════════════════════════════════════════════════════
# 2. STATE SCORES
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("2. STATE SCORES")
print("=" * 70)

print("\n2a. Computing all state scores...")
score_df = score_all(adata, cfg)
score_df.to_csv(OUT / "state_scores.csv")
print(f"  -> {OUT / 'state_scores.csv'}")
for col in score_df.columns:
    print(f"  {col}: mean={score_df[col].mean():.4f}, std={score_df[col].std():.4f}")

print("\n2b. Benchmarking state scores...")
bench_df = benchmark_scores(adata, cfg, score_df)
bench_df.to_csv(OUT / "state_score_benchmarks.csv", index=False)
print(f"  -> {OUT / 'state_score_benchmarks.csv'}")
print(bench_df.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════
# 3. MECHANISTIC ANALYSES
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("3. MECHANISTIC ANALYSES")
print("=" * 70)

print("\n3a. Program-geometry linkage...")
linkage_df = program_geometry_linkage(adata, cfg)
linkage_df.to_csv(OUT / "program_geometry_linkage.csv", index=False)
print(f"  -> {OUT / 'program_geometry_linkage.csv'}")
print(linkage_df.to_string(index=False))

print("\n3b. Fan-out contribution (linear regression)...")
fanout_df = fan_out_contribution(adata, cfg)
fanout_df.to_csv(OUT / "fan_out_contribution.csv", index=False)
print(f"  -> {OUT / 'fan_out_contribution.csv'}")
print(f"  R² = {fanout_df.attrs.get('r_squared', 'N/A'):.4f}")
print(fanout_df.to_string(index=False))

print("\n3c. Repair-stall analysis...")
stall_result = repair_stall_analysis(adata, cfg)
save_json(stall_result, "repair_stall.json")
if "bins" in stall_result:
    stall_df = pd.DataFrame(stall_result["bins"])
    print(f"  {len(stall_df)} bin-condition entries")
    for cond in ["Control", "COVID-19"]:
        sub = stall_df[stall_df["condition"] == cond]
        if len(sub) > 0:
            print(f"  {cond} diff/apop ratio range: {sub['diff_apop_ratio'].min():.2f} - {sub['diff_apop_ratio'].max():.2f}")

# ═══════════════════════════════════════════════════════════════════════
# 4. REPLICATION COHORT STATE SCORES
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("4. REPLICATION COHORT STATE SCORES")
print("=" * 70)

rep_path = ROOT / "data" / "replication" / "replication_alveolar.h5ad"
if rep_path.exists():
    print("Loading replication cohort...")
    rep_adata = sc.read_h5ad(rep_path)
    print(f"  {rep_adata.shape[0]} cells, {rep_adata.shape[1]} genes")

    rep_cfg = dict(cfg)
    rep_cfg["conditions"] = {
        "condition_column": "condition",
        "healthy_label": "normal",
        "covid_label": "COVID-19",
    }
    rep_cfg["cell_types"] = dict(cfg["cell_types"])
    rep_cfg["cell_types"]["annotation_column"] = "cell_type"
    rep_cfg["batch_correction"] = dict(cfg["batch_correction"])

    # Score available programs on replication data
    # Need PCA for coherence_loss_score
    print("  Computing PCA on replication cohort...")
    rep_adata_proc = rep_adata.copy()
    sc.pp.normalize_total(rep_adata_proc, target_sum=1e4)
    sc.pp.log1p(rep_adata_proc)
    sc.pp.scale(rep_adata_proc, max_value=10)
    sc.tl.pca(rep_adata_proc, n_comps=min(50, rep_adata_proc.shape[1] - 1), random_state=42)

    # Score programs on replication cohort using its 84-gene panel
    for prog_name, prog_info in cfg["gene_programs"].items():
        available = [g for g in prog_info["genes"] if g in rep_adata_proc.var_names]
        if len(available) >= 2:
            sc.tl.score_genes(rep_adata_proc, available, score_name=f"program_{prog_name}")

    print("  Computing state scores on replication cohort...")
    try:
        rep_score_df = score_all(rep_adata_proc, rep_cfg)
        rep_score_df.to_csv(OUT / "replication_state_scores.csv")
        print(f"  -> {OUT / 'replication_state_scores.csv'}")

        rep_bench_df = benchmark_scores(rep_adata_proc, rep_cfg, rep_score_df)
        rep_bench_df.to_csv(OUT / "replication_state_benchmarks.csv", index=False)
        print(f"  -> {OUT / 'replication_state_benchmarks.csv'}")
        print(rep_bench_df.to_string(index=False))
    except Exception as e:
        print(f"  WARNING: State scoring on replication cohort failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("  Replication cohort not found, skipping.")

print("\n" + "=" * 70)
print("ALL ANALYSES COMPLETE")
print("=" * 70)
print(f"\nAll results saved to: {OUT}/")
