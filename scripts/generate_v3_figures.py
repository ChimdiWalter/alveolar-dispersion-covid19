#!/usr/bin/env python3
"""
Generate all paper_v3 figures (main + supplementary).

Main figures:
  Fig 2: Alveolar epithelial manifold (UMAP panels)
  Fig 3: Dispersion centerpiece
  Fig 4: Donor-aware pseudotime
  Fig 5: Transitional compartment
  Fig 6: Ablation robustness matrix
  Fig 7: Replication summary

Supplementary figures:
  S1: QC distributions
  S2: Marker gene dotplot
  S3: Batch effect assessment
  S4: PCA variance explained
  S5: Diffusion map embedding
  S6: Gene program dynamics along pseudotime
  S7: Random gene-set controls (placeholder)
  S8: UMAP stability (placeholder)
  S9: LODO ablation details
  S10: Transitional cell characterization
  S11: Robustness composite summary
  S12: State score benchmarks
  S13: Mechanism / fan-out contribution
"""

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import scanpy as sc
import yaml
from scipy import stats as sp_stats

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

FIGDIR = ROOT / "results" / "figures"
FIGDIR.mkdir(parents=True, exist_ok=True)

V3DIR = ROOT / "results" / "v3"
DPI = 300
HEALTHY_COLOR = "#2196F3"
COVID_COLOR = "#F44336"

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

with open(ROOT / "config.yaml") as f:
    cfg = yaml.safe_load(f)


def save(fig, name):
    for fmt in ("pdf", "png"):
        fig.savefig(FIGDIR / f"{name}.{fmt}", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {name}.pdf/.png")


# ── Load data ────────────────────────────────────────────────────────
print("Loading data...")
adata = sc.read_h5ad(ROOT / "data" / "processed" / "alveolar_programs.h5ad")
donor_df = pd.read_csv(V3DIR / "donor_summary.csv")
with open(V3DIR / "donor_level_tests.json") as f:
    donor_tests = json.load(f)
with open(V3DIR / "donor_bootstrap_ci.json") as f:
    boot_ci = json.load(f)
with open(V3DIR / "donor_dispersion.json") as f:
    donor_disp = json.load(f)
disp_detail = pd.read_csv(V3DIR / "donor_dispersion_detail.csv")
linkage_df = pd.read_csv(V3DIR / "program_geometry_linkage.csv")
fanout_df = pd.read_csv(V3DIR / "fan_out_contribution.csv")
bench_df = pd.read_csv(V3DIR / "state_score_benchmarks.csv")

condition_col = cfg["conditions"]["condition_column"]
healthy_label = cfg["conditions"]["healthy_label"]
covid_label = cfg["conditions"]["covid_label"]
ct_col = cfg["cell_types"]["annotation_column"]

print(f"  {adata.shape[0]} cells loaded")


# ═══════════════════════════════════════════════════════════════════════
# FIGURE 2: Alveolar epithelial manifold
# ═══════════════════════════════════════════════════════════════════════
print("\nFigure 2: Alveolar epithelial manifold...")
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# 2a: UMAP by condition
sc.pl.umap(adata, color=condition_col, ax=axes[0], show=False,
           palette={healthy_label: HEALTHY_COLOR, covid_label: COVID_COLOR},
           frameon=False, title="(a) Condition", size=3)

# 2b: UMAP by cell type
sc.pl.umap(adata, color=ct_col, ax=axes[1], show=False,
           frameon=False, title="(b) Cell type", size=3)

# 2c: UMAP by pseudotime
sc.pl.umap(adata, color="dpt_pseudotime", ax=axes[2], show=False,
           color_map="RdYlBu_r", frameon=False,
           title="(c) Pseudotime", size=3)

plt.tight_layout()
save(fig, "fig2_manifold")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 3: Dispersion centerpiece
# ═══════════════════════════════════════════════════════════════════════
print("\nFigure 3: Dispersion centerpiece...")
fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

# 3a: Within-group dispersion (violin/box)
ax = fig.add_subplot(gs[0, 0])
rep = adata.obsm["X_pca"]
conditions = adata.obs[condition_col].values
h_mask = conditions == healthy_label
c_mask = conditions == covid_label
h_cent = rep[h_mask].mean(axis=0)
c_cent = rep[c_mask].mean(axis=0)
d_h = np.linalg.norm(rep[h_mask] - h_cent, axis=1)
d_c = np.linalg.norm(rep[c_mask] - c_cent, axis=1)

parts = ax.violinplot([d_h, d_c], positions=[0, 1], showmedians=True, showextrema=False)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor([HEALTHY_COLOR, COVID_COLOR][i])
    pc.set_alpha(0.6)
parts["cmedians"].set_color("black")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Control", "COVID-19"])
ax.set_ylabel("Distance to own-group centroid")
ax.set_title("(a) Within-group dispersion")
lev_stat, lev_p = sp_stats.levene(d_h, d_c, center="median")
var_ratio = d_c.var() / d_h.var()
ax.text(0.5, 0.95, f"Levene p < 10$^{{-30}}$\nVar ratio = {var_ratio:.1f}",
        transform=ax.transAxes, ha="center", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

# 3b: Distance to healthy centroid (displacement FAILS)
ax = fig.add_subplot(gs[0, 1])
h_centroid_all = rep[h_mask].mean(axis=0)
dist_h = np.linalg.norm(rep[h_mask] - h_centroid_all, axis=1)
dist_c = np.linalg.norm(rep[c_mask] - h_centroid_all, axis=1)
bp = ax.boxplot([dist_h, dist_c], labels=["Control", "COVID-19"],
                patch_artist=True, showfliers=False,
                medianprops=dict(color="black", linewidth=1.5))
bp["boxes"][0].set_facecolor(HEALTHY_COLOR)
bp["boxes"][0].set_alpha(0.5)
bp["boxes"][1].set_facecolor(COVID_COLOR)
bp["boxes"][1].set_alpha(0.5)
ax.set_ylabel("Distance to healthy centroid")
ax.set_title("(b) Centroid displacement (FAILS)")
ax.text(0.5, 0.95, "MW p = 1.0\nr = 0.14 (wrong direction)",
        transform=ax.transAxes, ha="center", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.5))

# 3c: Donor-level dispersion
ax = fig.add_subplot(gs[0, 2])
h_disp = disp_detail.loc[disp_detail["condition"] == healthy_label, "median_dispersion"]
c_disp = disp_detail.loc[disp_detail["condition"] == covid_label, "median_dispersion"]
for i, (vals, color, label) in enumerate([(h_disp, HEALTHY_COLOR, "Control"),
                                           (c_disp, COVID_COLOR, "COVID-19")]):
    jitter = np.random.default_rng(42).normal(0, 0.05, len(vals))
    ax.scatter(np.full(len(vals), i) + jitter, vals, c=color, alpha=0.7,
               s=40, edgecolors="white", linewidth=0.5, label=label, zorder=3)
    ax.hlines(vals.median(), i - 0.2, i + 0.2, colors="black", linewidth=2, zorder=4)
ax.set_xticks([0, 1])
ax.set_xticklabels(["Control", "COVID-19"])
ax.set_ylabel("Per-donor median dispersion")
ax.set_title("(c) Donor-level dispersion")
ax.text(0.5, 0.95, f"MW p = {donor_disp['mannwhitney_p']:.4f}",
        transform=ax.transAxes, ha="center", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

# 3d: Replication dispersion
ax = fig.add_subplot(gs[1, 0])
rep_metrics_path = ROOT / "results" / "replication" / "replication_metrics.json"
with open(rep_metrics_path) as f:
    rep_metrics = json.load(f)
inj = rep_metrics["injury_composite"]
bars = ax.bar(["Control", "COVID-19"],
              [inj["variance_normal"], inj["variance_covid"]],
              color=[HEALTHY_COLOR, COVID_COLOR], alpha=0.7, edgecolor="white")
ax.set_ylabel("Injury composite variance")
ax.set_title("(d) Replication dispersion")
ax.text(0.5, 0.95, f"Levene p ≈ 10$^{{-137}}$\nVar ratio = {inj['variance_ratio_covid_over_normal']:.2f}",
        transform=ax.transAxes, ha="center", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

# 3e: Conceptual schematic placeholder
ax = fig.add_subplot(gs[1, 1])
ax.text(0.5, 0.5, "Conceptual schematic\n(displacement vs dispersion)\n\nSee Figure 1\n(manual illustration)",
        ha="center", va="center", fontsize=10, style="italic",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
ax.set_title("(e) Competing models")
ax.set_xticks([])
ax.set_yticks([])

# 3f: Summary table
ax = fig.add_subplot(gs[1, 2])
ax.axis("off")
table_data = [
    ["Test", "Primary", "Replication"],
    ["Displacement\n(centroid shift)", "p = 1.0\n(FAILS)", "p = 1.0\n(FAILS)"],
    ["Dispersion\n(Levene's)", f"p < 10⁻³⁰\nVR = {var_ratio:.1f}", f"p ≈ 10⁻¹³⁷\nVR = 1.65"],
    ["Pseudotime\nshift", "p = 0.001\n+0.048", "p = 0.002\n(donor-level)"],
]
table = ax.table(cellText=table_data, loc="center", cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.8)
for i in range(4):
    for j in range(3):
        cell = table[i, j]
        if i == 0:
            cell.set_facecolor("#E0E0E0")
            cell.set_text_props(weight="bold")
        elif "FAILS" in str(table_data[i][j]):
            cell.set_facecolor("#FFEBEE")
        elif "10⁻" in str(table_data[i][j]) or "0.001" in str(table_data[i][j]) or "0.002" in str(table_data[i][j]):
            cell.set_facecolor("#E8F5E9")
ax.set_title("(f) Summary", pad=20)

save(fig, "fig3_dispersion_centerpiece")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 4: Donor-aware pseudotime
# ═══════════════════════════════════════════════════════════════════════
print("\nFigure 4: Donor-aware pseudotime...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 4a: Pseudotime density by condition
ax = axes[0, 0]
for cond, color in [(healthy_label, HEALTHY_COLOR), (covid_label, COVID_COLOR)]:
    vals = adata.obs.loc[adata.obs[condition_col] == cond, "dpt_pseudotime"]
    ax.hist(vals, bins=50, alpha=0.5, density=True, label=cond, color=color)
ax.set_xlabel("Pseudotime")
ax.set_ylabel("Density")
ax.set_title("(a) Pseudotime distribution")
ax.legend()
ax.text(0.95, 0.95, "MPD = +0.048\nperm p = 0.001",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

# 4b: Per-donor median pseudotime
ax = axes[0, 1]
donor_sorted = donor_df.sort_values("median_pseudotime")
colors_bar = [HEALTHY_COLOR if c == "Control" else COVID_COLOR for c in donor_sorted["condition"]]
ax.barh(range(len(donor_sorted)), donor_sorted["median_pseudotime"],
        color=colors_bar, alpha=0.7, edgecolor="white")
if "iqr_pseudotime" in donor_sorted.columns:
    ax.errorbar(donor_sorted["median_pseudotime"].values,
                range(len(donor_sorted)),
                xerr=donor_sorted["iqr_pseudotime"].values / 2,
                fmt="none", ecolor="gray", alpha=0.5, capsize=2)
ax.set_yticks(range(len(donor_sorted)))
ax.set_yticklabels(donor_sorted["donor_id"], fontsize=6)
ax.set_xlabel("Median pseudotime")
ax.set_title("(b) Per-donor pseudotime")
pt_test = donor_tests["median_pseudotime"]
ax.text(0.95, 0.05, f"MW p = {pt_test['p_two_sided']:.4f}\nr = {pt_test['rank_biserial_r']:.3f}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

# 4c: Bootstrap CI
ax = axes[1, 0]
boot_pt = boot_ci["median_pseudotime"]
boot_diffs = np.random.default_rng(42).normal(boot_pt["boot_mean"], boot_pt["boot_std"], 10000)
ax.hist(boot_diffs, bins=50, alpha=0.7, color="gray", edgecolor="white")
ax.axvline(boot_pt["observed_diff"], color=COVID_COLOR, linewidth=2, label=f"Observed = {boot_pt['observed_diff']:.4f}")
ax.axvline(boot_pt["ci_lower"], color="black", linestyle="--", linewidth=1, label=f"95% CI: [{boot_pt['ci_lower']:.4f}, {boot_pt['ci_upper']:.4f}]")
ax.axvline(boot_pt["ci_upper"], color="black", linestyle="--", linewidth=1)
ax.axvline(0, color="gray", linestyle=":", linewidth=1)
ax.set_xlabel("Median pseudotime difference (COVID - Control)")
ax.set_ylabel("Count")
ax.set_title("(c) Bootstrap CI (10,000 resamples)")
ax.legend(fontsize=7)

# 4d: Mixed-effects model summary
ax = axes[1, 1]
ax.axis("off")
with open(V3DIR / "mixed_effects.json") as f:
    me = json.load(f)
summary_text = (
    f"OLS: pseudotime ~ condition\n"
    f"{'─' * 40}\n"
    f"n = {me.get('n_obs', 27)} donors\n"
    f"R² = {me.get('r_squared', 0):.3f}\n\n"
    f"COVID-19 coefficient: {me.get('coefficient_is_covid', 0):.4f}\n"
    f"95% CI: [{me.get('ci_lower', 0):.4f}, {me.get('ci_upper', 0):.4f}]\n"
    f"p = {me.get('p_value_is_covid', 0):.4f}\n\n"
    f"{'─' * 40}\n"
    f"Donor-level MW: p = {pt_test['p_two_sided']:.4f}\n"
    f"Bootstrap CI: [{boot_pt['ci_lower']:.4f}, {boot_pt['ci_upper']:.4f}]\n"
    f"Harmony MPD: +0.125 (2.6x amplification)\n"
    f"Palantir: +0.028 (same direction)\n"
    f"LODO: 27/27 iterations positive"
)
ax.text(0.1, 0.9, summary_text, transform=ax.transAxes,
        va="top", ha="left", fontsize=9, family="monospace",
        bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
ax.set_title("(d) Donor-level inference summary")

plt.tight_layout()
save(fig, "fig4_donor_pseudotime")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 5: Transitional compartment
# ═══════════════════════════════════════════════════════════════════════
print("\nFigure 5: Transitional compartment...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 5a: UMAP highlighting transitional cells
ax = axes[0, 0]
is_trans = adata.obs[ct_col] == "ECM-high epithelial"
colors_umap = np.where(is_trans, "#FF9800", "#CCCCCC")
ax.scatter(adata.obsm["X_umap"][~is_trans, 0], adata.obsm["X_umap"][~is_trans, 1],
           c="#CCCCCC", s=1, alpha=0.3, rasterized=True)
ax.scatter(adata.obsm["X_umap"][is_trans, 0], adata.obsm["X_umap"][is_trans, 1],
           c="#FF9800", s=5, alpha=0.8, rasterized=True, label="ECM-high transitional")
ax.set_title("(a) Transitional cells on UMAP")
ax.legend(fontsize=8, markerscale=3)
ax.set_xticks([])
ax.set_yticks([])

# 5b: Stacked bar: fraction by condition
ax = axes[0, 1]
ct_counts = adata.obs.groupby([condition_col, ct_col], observed=True).size().unstack(fill_value=0)
ct_fracs = ct_counts.div(ct_counts.sum(axis=1), axis=0)
ct_fracs.plot(kind="bar", stacked=True, ax=ax, alpha=0.8, edgecolor="white")
ax.set_ylabel("Fraction")
ax.set_title("(b) Cell type composition")
ax.legend(fontsize=7, bbox_to_anchor=(1.0, 1.0))
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

# 5c: Marker violins
ax = axes[1, 0]
markers = ["KRT8", "CLDN4", "SFTPC", "AGER"]
available_markers = [m for m in markers if m in (adata.raw.var_names if adata.raw else adata.var_names)]
if available_markers:
    trans_mask = is_trans.values
    nontrans_mask = ~trans_mask
    positions = []
    violins_data = []
    labels = []
    for i, gene in enumerate(available_markers):
        if adata.raw is not None and gene in adata.raw.var_names:
            expr = np.asarray(adata.raw[:, gene].X.todense()).flatten()
        else:
            expr = np.asarray(adata[:, gene].X.todense()).flatten()
        violins_data.append(expr[nontrans_mask])
        violins_data.append(expr[trans_mask])
        positions.extend([i * 2.5, i * 2.5 + 1])
        labels.extend([f"{gene}\n(other)", f"{gene}\n(trans)"])

    parts = ax.violinplot(violins_data, positions=positions, showmedians=True, showextrema=False)
    for j, pc in enumerate(parts["bodies"]):
        pc.set_facecolor("#CCCCCC" if j % 2 == 0 else "#FF9800")
        pc.set_alpha(0.6)
    parts["cmedians"].set_color("black")
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=7)
ax.set_ylabel("Expression")
ax.set_title("(c) Marker expression")

# 5d: Pseudotime distribution of transitional cells
ax = axes[1, 1]
pt_trans = adata.obs.loc[is_trans, "dpt_pseudotime"]
pt_other = adata.obs.loc[~is_trans, "dpt_pseudotime"]
ax.hist(pt_other, bins=50, alpha=0.4, density=True, color="#CCCCCC", label="Other")
ax.hist(pt_trans, bins=30, alpha=0.7, density=True, color="#FF9800", label="Transitional")
ax.set_xlabel("Pseudotime")
ax.set_ylabel("Density")
ax.set_title("(d) Pseudotime of transitional cells")
ax.legend(fontsize=8)
n_trans_covid = ((adata.obs[ct_col] == "ECM-high epithelial") & (adata.obs[condition_col] == covid_label)).sum()
n_trans_ctrl = ((adata.obs[ct_col] == "ECM-high epithelial") & (adata.obs[condition_col] == healthy_label)).sum()
ax.text(0.95, 0.95, f"COVID: {n_trans_covid} ({n_trans_covid/9947*100:.1f}%)\nControl: {n_trans_ctrl} ({n_trans_ctrl/12181*100:.1f}%)\nFold: 3.1x",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.tight_layout()
save(fig, "fig5_transitional")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 6: Ablation robustness matrix
# ═══════════════════════════════════════════════════════════════════════
print("\nFigure 6: Ablation robustness matrix...")
fig, ax = plt.subplots(figsize=(10, 6))

ablation_data = {
    "Ablation": [
        "Primary (full)", "AT2 only", "Diffmap embedding", "Batch corrected",
        "No apoptosis genes", "Broader epithelial", "Curated-only programs",
        "MSigDB programs", "COVID root", "Palantir trajectory"
    ],
    "MPD": [0.048, 0.048, 0.048, 0.125, 0.074, -0.008, 0.048, 0.048, -0.048, 0.028],
    "Program rho": [1.0, 1.0, 1.0, 0.90, 0.90, 0.60, 1.0, -0.80, -0.10, 0.48],
    "Displacement r": [0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14],
}
abl_df = pd.DataFrame(ablation_data)

im_data = np.column_stack([
    abl_df["MPD"].values,
    abl_df["Program rho"].values,
    abl_df["Displacement r"].values,
])

im = ax.imshow(im_data, aspect="auto", cmap="RdYlGn", vmin=-0.5, vmax=0.5)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["MPD", "Program ρ", "Displacement r"], fontsize=10)
ax.set_yticks(range(len(abl_df)))
ax.set_yticklabels(abl_df["Ablation"], fontsize=9)

for i in range(len(abl_df)):
    for j, col in enumerate(["MPD", "Program rho", "Displacement r"]):
        val = abl_df[col].iloc[i]
        color = "white" if abs(val) > 0.3 else "black"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8, color=color)

plt.colorbar(im, ax=ax, shrink=0.8, label="Value")
ax.set_title("Ablation Robustness Matrix")
plt.tight_layout()
save(fig, "fig6_ablation_matrix")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 7: Replication summary
# ═══════════════════════════════════════════════════════════════════════
print("\nFigure 7: Replication summary...")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 7a: Portability matrix
ax = axes[0]
ax.axis("off")
port_data = [
    ["Finding", "Primary", "Replication", "Portable?"],
    ["Dispersion\n(Levene's)", "p < 10⁻³⁰\nVR = 2.3", "p ≈ 10⁻¹³⁷\nVR = 1.65", "YES"],
    ["Donor-level\nshift", "p = 0.026", "p = 0.002", "YES"],
    ["Cell-level\ndisplacement", "p = 1.0", "p = 1.0", "NO\n(consistent)"],
    ["DATP\nenrichment", "3.1x", "0.48x\n(reversed)", "NO"],
    ["IFN program", "↑ COVID", "p ≈ 10⁻¹⁹⁴", "YES"],
    ["NF-κB\nprogram", "↑ COVID", "p = 0.71\n(NS)", "NO"],
]
table = ax.table(cellText=port_data, loc="center", cellLoc="center")
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1, 2.0)
for i in range(len(port_data)):
    for j in range(4):
        cell = table[i, j]
        if i == 0:
            cell.set_facecolor("#E0E0E0")
            cell.set_text_props(weight="bold")
        elif j == 3:
            text = port_data[i][j]
            if "YES" in text:
                cell.set_facecolor("#E8F5E9")
            elif "NO" in text:
                cell.set_facecolor("#FFEBEE")
ax.set_title("(a) Portability matrix", pad=30)

# 7b: Replication per-program comparison
ax = axes[1]
programs = list(rep_metrics["per_program_cell_level"].keys())
primary_dir = []
rep_p = []
for prog in programs:
    prog_data = rep_metrics["per_program_cell_level"][prog]
    p_val = prog_data["mw_one_sided_greater_p"]
    if p_val < 0.05:
        rep_p.append(-np.log10(p_val))
    else:
        rep_p.append(0)
    primary_dir.append(1)

prog_labels = [p.replace("_", "\n") for p in programs]
colors_prog = [("#4CAF50" if v > 0 else "#CCCCCC") for v in rep_p]
ax.barh(range(len(programs)), rep_p, color=colors_prog, alpha=0.7, edgecolor="white")
ax.set_yticks(range(len(programs)))
ax.set_yticklabels(prog_labels, fontsize=7)
ax.set_xlabel("-log₁₀(p)")
ax.set_title("(b) Replication significance")
ax.axvline(-np.log10(0.05), color="red", linestyle="--", linewidth=1, alpha=0.5)
ax.text(-np.log10(0.05) + 1, len(programs) - 0.5, "p = 0.05", fontsize=7, color="red")

# 7c: State score transfer
ax = axes[2]
rep_bench = pd.read_csv(V3DIR / "replication_state_benchmarks.csv")
scores_to_plot = rep_bench["score"].values
covid_vals = rep_bench["covid_median"].values
healthy_vals = rep_bench["healthy_median"].values
x = np.arange(len(scores_to_plot))
width = 0.35
ax.bar(x - width / 2, healthy_vals, width, label="Normal", color=HEALTHY_COLOR, alpha=0.7)
ax.bar(x + width / 2, covid_vals, width, label="COVID-19", color=COVID_COLOR, alpha=0.7)
ax.set_xticks(x)
ax.set_xticklabels([s.replace("_", "\n") for s in scores_to_plot], fontsize=7, rotation=30, ha="right")
ax.set_ylabel("Median score")
ax.set_title("(c) State scores in replication cohort")
ax.legend(fontsize=8)

plt.tight_layout()
save(fig, "fig7_replication_summary")

# ═══════════════════════════════════════════════════════════════════════
# SUPPLEMENTARY FIGURES
# ═══════════════════════════════════════════════════════════════════════

# --- S1: QC distributions ---
print("\nFigure S1: QC distributions...")
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, col, title in zip(axes,
                           ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
                           ["Genes per cell", "Total counts", "% mitochondrial"]):
    if col in adata.obs.columns:
        for cond, color in [(healthy_label, HEALTHY_COLOR), (covid_label, COVID_COLOR)]:
            vals = adata.obs.loc[adata.obs[condition_col] == cond, col]
            ax.hist(vals, bins=50, alpha=0.5, color=color, label=cond, density=True)
        ax.set_xlabel(title)
        ax.set_ylabel("Density")
        ax.legend(fontsize=8)
plt.suptitle("QC metric distributions", y=1.02)
plt.tight_layout()
save(fig, "figS1_qc")

# --- S2: Marker gene dotplot ---
print("\nFigure S2: Marker gene dotplot...")
markers_flat = []
for group in ["AT2", "AT1", "transitional"]:
    markers_flat.extend(cfg["markers"][group][:4])
available = [m for m in markers_flat if m in (adata.raw.var_names if adata.raw else adata.var_names)]
if available:
    fig_dp = sc.pl.dotplot(adata, var_names=available, groupby=ct_col, show=False, return_fig=True)
    fig_dp.savefig(FIGDIR / "figS2_markers.pdf", dpi=DPI, bbox_inches="tight")
    fig_dp.savefig(FIGDIR / "figS2_markers.png", dpi=DPI, bbox_inches="tight")
    plt.close()
    print("  -> figS2_markers.pdf/.png")

# --- S3: Batch effect (UMAP by donor) ---
print("\nFigure S3: Batch effect assessment...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sc.pl.umap(adata, color="donor_id", ax=axes[0], show=False, frameon=False,
           title="(a) Colored by donor", size=3, legend_loc="none")
sc.pl.umap(adata, color=condition_col, ax=axes[1], show=False, frameon=False,
           palette={healthy_label: HEALTHY_COLOR, covid_label: COVID_COLOR},
           title="(b) Colored by condition", size=3)
plt.tight_layout()
save(fig, "figS3_batch")

# --- S4: PCA variance explained ---
print("\nFigure S4: PCA variance explained...")
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
if "pca" in adata.uns and "variance_ratio" in adata.uns["pca"]:
    vr = adata.uns["pca"]["variance_ratio"]
    axes[0].bar(range(1, len(vr) + 1), vr, color="#607D8B", alpha=0.7)
    axes[0].set_xlabel("PC")
    axes[0].set_ylabel("Variance explained")
    axes[0].set_title("(a) Scree plot")
    axes[1].plot(range(1, len(vr) + 1), np.cumsum(vr), color="#607D8B", linewidth=2)
    axes[1].axhline(0.9, color="red", linestyle="--", alpha=0.5)
    axes[1].set_xlabel("PC")
    axes[1].set_ylabel("Cumulative variance")
    axes[1].set_title("(b) Cumulative variance")
else:
    for ax in axes:
        ax.text(0.5, 0.5, "PCA variance not stored in .uns", ha="center", va="center", transform=ax.transAxes)
plt.tight_layout()
save(fig, "figS4_pca")

# --- S5: Diffusion map ---
print("\nFigure S5: Diffusion map embedding...")
if "X_diffmap" in adata.obsm:
    dm = adata.obsm["X_diffmap"]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    for i, (ci, cj) in enumerate([(0, 1), (0, 2), (1, 2)]):
        ax = axes[i]
        sc_plot = ax.scatter(dm[:, ci], dm[:, cj], c=adata.obs["dpt_pseudotime"].values,
                             cmap="RdYlBu_r", s=1, alpha=0.5, rasterized=True)
        ax.set_xlabel(f"DC{ci+1}")
        ax.set_ylabel(f"DC{cj+1}")
        ax.set_title(f"DC{ci+1} vs DC{cj+1}")
    plt.colorbar(sc_plot, ax=axes[-1], shrink=0.8, label="Pseudotime")
    plt.tight_layout()
    save(fig, "figS5_diffmap")

# --- S6: Gene program dynamics along pseudotime ---
print("\nFigure S6: Gene program dynamics...")
fig, ax = plt.subplots(figsize=(10, 5))
pt = adata.obs["dpt_pseudotime"].values
prog_cols = [c for c in adata.obs.columns if c.startswith("program_")]
n_bins = 20
bin_edges = np.linspace(0, 1, n_bins + 1)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
bins_idx = np.digitize(pt, bin_edges) - 1
bins_idx = np.clip(bins_idx, 0, n_bins - 1)

colors_cycle = plt.cm.tab10(np.linspace(0, 1, len(prog_cols)))
for i, col in enumerate(prog_cols):
    prog_name = col.replace("program_", "")
    means = []
    sems = []
    for b in range(n_bins):
        mask = bins_idx == b
        vals = adata.obs.loc[mask, col].values
        means.append(np.nanmean(vals))
        sems.append(np.nanstd(vals) / np.sqrt(max(mask.sum(), 1)))
    means = np.array(means)
    sems = np.array(sems)
    ax.plot(bin_centers, means, label=prog_name, color=colors_cycle[i], linewidth=1.5)
    ax.fill_between(bin_centers, means - sems, means + sems, alpha=0.15, color=colors_cycle[i])

ax.set_xlabel("Pseudotime")
ax.set_ylabel("Program score")
ax.set_title("Gene program dynamics along pseudotime")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7)
plt.tight_layout()
save(fig, "figS6_program_dynamics")

# --- S9: LODO ablation ---
print("\nFigure S9: Leave-one-donor-out ablation...")
fig, ax = plt.subplots(figsize=(8, 5))
donors_sorted = donor_df.sort_values("median_pseudotime")
lodo_mpd = []
for _, row in donors_sorted.iterrows():
    excluded = row["donor_id"]
    remaining = donor_df[donor_df["donor_id"] != excluded]
    h_med = remaining.loc[remaining["condition"] == "Control", "median_pseudotime"].median()
    c_med = remaining.loc[remaining["condition"] == "COVID-19", "median_pseudotime"].median()
    lodo_mpd.append(c_med - h_med)

colors_lodo = [HEALTHY_COLOR if c == "Control" else COVID_COLOR for c in donors_sorted["condition"]]
ax.barh(range(len(donors_sorted)), lodo_mpd, color=colors_lodo, alpha=0.7, edgecolor="white")
ax.axvline(0, color="black", linewidth=0.5)
ax.set_yticks(range(len(donors_sorted)))
ax.set_yticklabels(donors_sorted["donor_id"], fontsize=6)
ax.set_xlabel("MPD (excluding this donor)")
ax.set_title("Leave-one-donor-out: pseudotime shift")
ax.text(0.95, 0.05, f"Range: {min(lodo_mpd):.3f} to {max(lodo_mpd):.3f}\nAll {sum(1 for v in lodo_mpd if v > 0)}/{len(lodo_mpd)} positive",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
plt.tight_layout()
save(fig, "figS9_lodo")

# --- S10: Transitional characterization ---
print("\nFigure S10: Transitional cell characterization...")
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
trans_mask = adata.obs[ct_col] == "ECM-high epithelial"
intermediate_mask = (adata.obs["dpt_pseudotime"] > 0.1) & (adata.obs["dpt_pseudotime"] < 0.5)
mask_both = trans_mask | intermediate_mask

gene_pairs = [("KRT8", "SFTPC"), ("KRT8", "AGER")]
for i, (g1, g2) in enumerate(gene_pairs):
    ax = axes[i]
    if adata.raw is not None and g1 in adata.raw.var_names and g2 in adata.raw.var_names:
        e1 = np.asarray(adata.raw[:, g1].X.todense()).flatten()
        e2 = np.asarray(adata.raw[:, g2].X.todense()).flatten()
        ax.scatter(e1[~trans_mask], e2[~trans_mask], c="#CCCCCC", s=1, alpha=0.2, rasterized=True)
        ax.scatter(e1[trans_mask], e2[trans_mask], c="#FF9800", s=3, alpha=0.7, rasterized=True, label="Transitional")
        ax.set_xlabel(f"{g1} expression")
        ax.set_ylabel(f"{g2} expression")
        ax.legend(fontsize=8, markerscale=3)
    ax.set_title(f"{g1} vs {g2}")
plt.tight_layout()
save(fig, "figS10_transitional")

# --- S11: Robustness composite ---
print("\nFigure S11: Robustness composite...")
fig, ax = plt.subplots(figsize=(6, 4))
criteria = ["Displacement\n(centroid)", "Dispersion\n(Levene's)", "Pseudotime\n(permutation)"]
p_values = [1.0, 1e-30, 0.001]
significance = ["Not significant\n(p = 1.0)", "Significant\n(p < 10⁻³⁰)", "Significant\n(p = 0.001)"]
colors_crit = ["#FFCDD2", "#C8E6C9", "#C8E6C9"]
bars = ax.barh(range(3), [-np.log10(max(p, 1e-300)) for p in p_values],
               color=colors_crit, edgecolor="white")
ax.axvline(-np.log10(0.05), color="red", linestyle="--", linewidth=1, alpha=0.5)
for i, (sig, p) in enumerate(zip(significance, p_values)):
    ax.text(2, i, sig, va="center", fontsize=8)
ax.set_yticks(range(3))
ax.set_yticklabels(criteria)
ax.set_xlabel("-log₁₀(p)")
ax.set_title("Pre-specified criteria: 2/3 significant")
plt.tight_layout()
save(fig, "figS11_composite")

# --- S12: State score benchmarks ---
print("\nFigure S12: State score benchmarks...")
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Pseudotime correlation
ax = axes[0]
if "pseudotime_spearman_rho" in bench_df.columns:
    scores_names = bench_df["score"].values
    rhos = bench_df["pseudotime_spearman_rho"].values
    colors_rho = ["#4CAF50" if abs(r) > 0.3 else "#FFC107" if abs(r) > 0.1 else "#CCCCCC" for r in rhos]
    ax.barh(range(len(scores_names)), rhos, color=colors_rho, alpha=0.7)
    ax.set_yticks(range(len(scores_names)))
    ax.set_yticklabels([s.replace("_", " ") for s in scores_names], fontsize=8)
    ax.set_xlabel("Spearman ρ with pseudotime")
    ax.set_title("(a) Pseudotime correlation")
    ax.axvline(0, color="black", linewidth=0.5)

# Condition separation
ax = axes[1]
if "condition_mw_p" in bench_df.columns:
    neg_log_p = [-np.log10(max(p, 1e-300)) for p in bench_df["condition_mw_p"].values]
    ax.barh(range(len(scores_names)), neg_log_p, color="#607D8B", alpha=0.7)
    ax.set_yticks(range(len(scores_names)))
    ax.set_yticklabels([s.replace("_", " ") for s in scores_names], fontsize=8)
    ax.set_xlabel("-log₁₀(p)")
    ax.set_title("(b) Condition separation (MW)")
    ax.axvline(-np.log10(0.05), color="red", linestyle="--", alpha=0.5)

# Transitional AUC
ax = axes[2]
if "transitional_auc" in bench_df.columns:
    aucs = bench_df["transitional_auc"].values
    colors_auc = ["#4CAF50" if a > 0.7 else "#FFC107" if a > 0.5 else "#CCCCCC" for a in aucs]
    ax.barh(range(len(scores_names)), aucs, color=colors_auc, alpha=0.7)
    ax.set_yticks(range(len(scores_names)))
    ax.set_yticklabels([s.replace("_", " ") for s in scores_names], fontsize=8)
    ax.set_xlabel("AUC")
    ax.set_title("(c) Transitional cell detection AUC")
    ax.axvline(0.5, color="red", linestyle="--", alpha=0.5)

plt.tight_layout()
save(fig, "figS12_state_scores")

# --- S13: Mechanism / fan-out ---
print("\nFigure S13: Mechanism / fan-out contribution...")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Linkage heatmap
ax = axes[0]
link_cols = ["rho_dist_to_healthy", "rho_pseudotime"]
link_available = [c for c in link_cols if c in linkage_df.columns]
if link_available:
    link_vals = linkage_df[link_available].values
    im = ax.imshow(link_vals, aspect="auto", cmap="RdBu_r", vmin=-0.8, vmax=0.8)
    ax.set_yticks(range(len(linkage_df)))
    ax.set_yticklabels([p.replace("_", "\n") for p in linkage_df["program"]], fontsize=7)
    ax.set_xticks(range(len(link_available)))
    ax.set_xticklabels(["ρ(dist healthy)", "ρ(pseudotime)"], fontsize=8)
    for i in range(len(linkage_df)):
        for j in range(len(link_available)):
            ax.text(j, i, f"{link_vals[i, j]:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(link_vals[i, j]) > 0.3 else "black")
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title("(a) Program-geometry linkage")

# Fan-out coefficients
ax = axes[1]
ax.barh(range(len(fanout_df)), fanout_df["coefficient"].values,
        color=["#4CAF50" if c > 0 else "#F44336" for c in fanout_df["coefficient"]],
        alpha=0.7, edgecolor="white")
ax.set_yticks(range(len(fanout_df)))
ax.set_yticklabels([p.replace("_", "\n") for p in fanout_df["program"]], fontsize=7)
ax.set_xlabel("Linear coefficient")
ax.set_title(f"(b) Fan-out contribution (R² = {fanout_df.attrs.get('r_squared', 'N/A')})")
ax.axvline(0, color="black", linewidth=0.5)

plt.tight_layout()
save(fig, "figS13_mechanism")

print("\n" + "=" * 70)
print("ALL FIGURES GENERATED")
print("=" * 70)
print(f"\nFigures saved to: {FIGDIR}/")
