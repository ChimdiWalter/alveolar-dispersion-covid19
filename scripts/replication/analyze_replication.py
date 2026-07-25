#!/usr/bin/env python3
"""Replication analysis on HLCA-extended COVID-19 lung AT1/AT2 cells
(Melms/SCP1219 excluded).

Tests three pre-registered claims from the primary analysis:
  1. Dispersion: COVID AT1/AT2 cells show greater within-group spread than
     healthy along a composite injury-program axis (Levene's test).
  2. Pseudotime shift (surrogate): COVID AT1/AT2 cells are shifted toward
     an injury-program composite (one-sided Mann-Whitney).
  3. DATP (KRT8+/CLDN4+) enrichment: fraction of AT2 cells co-expressing
     KRT8+CLDN4 above thresholds is higher in COVID (chi-square).

Notes:
  * Replication cohort has 921,510 alveolar cells (56k COVID / 866k normal)
    from 35 datasets / 618 donors on cellxgene census, Melms (SCP1219)
    dataset_id removed.
  * Only a curated 84-gene panel was downloaded to keep size tractable; this
    suffices for program scoring + marker-based DATP assay but is too narrow
    for building a new manifold/DPT. Full-transcriptome DPT replication is
    reported as a remaining limitation.
  * Because the replication set is extremely imbalanced (~15:1 normal:COVID)
    and contains many studies with different protocols, we subsample normals
    per donor (cap 200 cells/donor) to reduce a few-dataset artifacts, and
    report donor-level pseudobulk medians as a secondary confirmatory test.
"""
import json
import logging
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
import scipy.stats as st
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("replication.analyze")

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
RNG = np.random.default_rng(42)

OUT = ROOT / "results/replication"
OUT.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# Load
# -------------------------------------------------------------------------
adata = ad.read_h5ad(ROOT / "data/replication/replication_alveolar.h5ad")
log.info("loaded replication: %s", adata.shape)

# Normalize per-cell (some datasets already normalized, but safe to redo on
# counts — check: values are floats or ints)
Xmax = adata.X.max() if hasattr(adata.X, "max") else 0
log.info("X max value: %s", Xmax)

# Census returns raw counts. Normalize consistently with primary pipeline.
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

# -------------------------------------------------------------------------
# Per-donor cap: ≤200 cells per donor to reduce dataset-dominance
# -------------------------------------------------------------------------
keep = []
for (donor, cond), idx in adata.obs.groupby(["donor_id", "condition"], observed=True).groups.items():
    idx = np.array(idx)
    if len(idx) > 200:
        idx = RNG.choice(idx, 200, replace=False)
    keep.extend(idx.tolist())
adata = adata[keep].copy()
log.info("after per-donor cap: %s  (COVID=%d, normal=%d)",
         adata.shape,
         (adata.obs["condition"] == "COVID-19").sum(),
         (adata.obs["condition"] == "normal").sum())

# -------------------------------------------------------------------------
# Score gene programs (scanpy score_genes) against .raw when available
# -------------------------------------------------------------------------
adata.raw = adata  # .raw = log-normalized 84 genes
programs = CFG["gene_programs"]
injury_programs = ["interferon_response", "nfkb_inflammatory", "oxidative_stress",
                   "apoptosis", "senescence", "AT2_to_AT1_differentiation"]
healthy_programs = ["AT2_identity", "AT1_identity"]

for name, spec in programs.items():
    available = [g for g in spec["genes"] if g in adata.var_names]
    if len(available) < 2:
        log.warning("program %s skipped (only %d genes available)", name, len(available))
        adata.obs[f"score_{name}"] = np.nan
        continue
    sc.tl.score_genes(adata, gene_list=available, score_name=f"score_{name}",
                      use_raw=True, random_state=42)

# Composite injury axis = mean of injury program scores
inj_cols = [f"score_{p}" for p in injury_programs if f"score_{p}" in adata.obs.columns]
adata.obs["injury_composite"] = adata.obs[inj_cols].mean(axis=1)

# -------------------------------------------------------------------------
# Test 1 — Dispersion (Levene) on injury composite
# -------------------------------------------------------------------------
covid = adata.obs.loc[adata.obs["condition"] == "COVID-19", "injury_composite"].values
normal = adata.obs.loc[adata.obs["condition"] == "normal", "injury_composite"].values
lev_stat, lev_p = st.levene(covid, normal, center="median")
var_ratio = np.var(covid, ddof=1) / np.var(normal, ddof=1)

# -------------------------------------------------------------------------
# Test 2 — One-sided Mann-Whitney (COVID > normal on injury composite)
# -------------------------------------------------------------------------
u_stat, mw_p = st.mannwhitneyu(covid, normal, alternative="greater")
# rank-biserial effect size
n1, n2 = len(covid), len(normal)
rbc = 1 - 2 * u_stat / (n1 * n2)   # conventional sign convention
med_covid = float(np.median(covid))
med_normal = float(np.median(normal))

# Donor-level pseudobulk (robust to per-cell / per-dataset structure)
donor_med = adata.obs.groupby(["donor_id", "condition"], observed=True)["injury_composite"].median().reset_index()
dc = donor_med.loc[donor_med["condition"] == "COVID-19", "injury_composite"]
dn = donor_med.loc[donor_med["condition"] == "normal", "injury_composite"]
du_stat, du_p = st.mannwhitneyu(dc, dn, alternative="greater")

# -------------------------------------------------------------------------
# Test 3 — DATP (KRT8+/CLDN4+) enrichment (chi-square, cell-level)
# -------------------------------------------------------------------------
if "KRT8" in adata.var_names and "CLDN4" in adata.var_names:
    # threshold at log-normalized > 0 for both markers
    krt8 = adata[:, "KRT8"].X.toarray().ravel() if hasattr(adata[:, "KRT8"].X, "toarray") else np.asarray(adata[:, "KRT8"].X).ravel()
    cldn4 = adata[:, "CLDN4"].X.toarray().ravel() if hasattr(adata[:, "CLDN4"].X, "toarray") else np.asarray(adata[:, "CLDN4"].X).ravel()
    datp = (krt8 > 0) & (cldn4 > 0)
    adata.obs["datp_positive"] = datp
    tab = pd.crosstab(adata.obs["condition"], adata.obs["datp_positive"])
    chi2, chi_p, _, _ = st.chi2_contingency(tab.values)
    covid_frac = adata.obs.loc[adata.obs["condition"] == "COVID-19", "datp_positive"].mean()
    normal_frac = adata.obs.loc[adata.obs["condition"] == "normal", "datp_positive"].mean()
    fold = covid_frac / normal_frac if normal_frac > 0 else float("inf")
else:
    chi_p, covid_frac, normal_frac, fold = None, None, None, None

# -------------------------------------------------------------------------
# Write results
# -------------------------------------------------------------------------
results = {
    "n_cells_total": int(adata.n_obs),
    "n_cells_covid": int(n1),
    "n_cells_normal": int(n2),
    "n_donors": int(adata.obs["donor_id"].nunique()),
    "n_donors_covid": int(adata.obs.loc[adata.obs["condition"] == "COVID-19", "donor_id"].nunique()),
    "n_donors_normal": int(adata.obs.loc[adata.obs["condition"] == "normal", "donor_id"].nunique()),
    "n_datasets": int(adata.obs["dataset_id"].nunique()),
    "injury_composite": {
        "covid_median": med_covid,
        "normal_median": med_normal,
        "difference_median": med_covid - med_normal,
        "variance_covid": float(np.var(covid, ddof=1)),
        "variance_normal": float(np.var(normal, ddof=1)),
        "variance_ratio_covid_over_normal": float(var_ratio),
        "levene_stat": float(lev_stat),
        "levene_p": float(lev_p),
        "mannwhitney_u_one_sided_p": float(mw_p),
        "rank_biserial_r": float(rbc),
        "donor_level_n_covid": int(len(dc)),
        "donor_level_n_normal": int(len(dn)),
        "donor_level_mannwhitney_p": float(du_p),
    },
    "datp": {
        "covid_fraction": float(covid_frac) if covid_frac is not None else None,
        "normal_fraction": float(normal_frac) if normal_frac is not None else None,
        "fold_enrichment": float(fold) if fold is not None else None,
        "chi2_p": float(chi_p) if chi_p is not None else None,
    },
    "per_program_cell_level": {},
}
for p in programs:
    col = f"score_{p}"
    if col not in adata.obs.columns or adata.obs[col].isna().all():
        continue
    cc = adata.obs.loc[adata.obs["condition"] == "COVID-19", col].values
    cn = adata.obs.loc[adata.obs["condition"] == "normal", col].values
    u, pu = st.mannwhitneyu(cc, cn, alternative="greater")
    results["per_program_cell_level"][p] = {
        "median_covid": float(np.nanmedian(cc)),
        "median_normal": float(np.nanmedian(cn)),
        "mw_one_sided_greater_p": float(pu),
    }

(OUT / "replication_metrics.json").write_text(json.dumps(results, indent=2))
log.info("wrote %s", OUT / "replication_metrics.json")

# Save compact obs for plotting
adata.obs.to_parquet(OUT / "replication_obs.parquet")
log.info("wrote %s", OUT / "replication_obs.parquet")

# Print headline
print("\n=== Replication Headline ===")
print(f"Cells: {n1:,} COVID / {n2:,} normal, {results['n_donors']} donors, {results['n_datasets']} datasets")
print(f"Injury composite — median COVID={med_covid:+.4f}, median normal={med_normal:+.4f}, diff={med_covid-med_normal:+.4f}")
print(f"Dispersion Levene: stat={lev_stat:.2f}  p={lev_p:.3e}  var ratio={var_ratio:.2f}")
print(f"One-sided MW (COVID>normal): p={mw_p:.3e}  rank-biserial r={rbc:.3f}")
print(f"Donor-level MW: p={du_p:.3e}  (n={len(dc)} COVID donors, {len(dn)} normal donors)")
if chi_p is not None:
    print(f"DATP (KRT8+/CLDN4+) fraction: COVID={covid_frac*100:.2f}%  normal={normal_frac*100:.2f}%  fold={fold:.2f}x  chi2 p={chi_p:.3e}")
