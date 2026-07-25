"""
Publication-quality figure generation.

All plotting functions produce matplotlib figures that can be saved at
300 DPI for manuscript submission. Functions return (fig, ax) tuples for
further customization.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("robustness.plots")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError:
    pass

# Manuscript-quality defaults
FIGSIZE_SINGLE = (4, 4)
FIGSIZE_WIDE = (8, 4)
FIGSIZE_MULTI = (12, 8)
DPI = 300
FONT_SIZE = 10

plt.rcParams.update({
    "font.size": FONT_SIZE,
    "axes.titlesize": FONT_SIZE + 1,
    "axes.labelsize": FONT_SIZE,
    "xtick.labelsize": FONT_SIZE - 1,
    "ytick.labelsize": FONT_SIZE - 1,
    "legend.fontsize": FONT_SIZE - 1,
    "figure.dpi": DPI,
    "savefig.dpi": DPI,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,  # editable text in PDFs
    "ps.fonttype": 42,
})


def save_fig(fig, name: str, output_dir: str = "results/figures",
             formats: tuple = ("pdf", "png")) -> None:
    """Save a figure in multiple formats."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        path = out / f"{name}.{fmt}"
        fig.savefig(path, dpi=DPI, bbox_inches="tight")
        logger.info(f"Figure saved: {path}")


def plot_umap_condition(adata, cfg: dict, ax=None):
    """UMAP colored by condition (healthy vs COVID).

    Corresponds to Figure 1a.
    """
    import scanpy as sc
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    else:
        fig = ax.figure
    condition_col = cfg["conditions"]["condition_column"]
    healthy = cfg["conditions"]["healthy_label"]
    covid = cfg["conditions"]["covid_label"]
    sc.pl.umap(adata, color=condition_col, ax=ax, show=False,
               palette={healthy: "#2196F3", covid: "#F44336"},
               frameon=False, title="Condition")
    return fig, ax


def plot_umap_celltype(adata, cfg: dict, ax=None):
    """UMAP colored by cell type (AT1, AT2, Transitional).

    Corresponds to Figure 1b.
    """
    import scanpy as sc
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    else:
        fig = ax.figure
    annot_col = cfg["cell_types"]["annotation_column"]
    sc.pl.umap(adata, color=annot_col, ax=ax, show=False,
               frameon=False, title="Cell type")
    return fig, ax


def plot_umap_pseudotime(adata, ax=None):
    """UMAP colored by diffusion pseudotime.

    Corresponds to Figure 2.
    """
    import scanpy as sc
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    else:
        fig = ax.figure
    sc.pl.umap(adata, color="dpt_pseudotime", ax=ax, show=False,
               color_map="RdYlBu_r", frameon=False,
               title="Pseudotime")
    return fig, ax


def plot_pseudotime_density(adata, cfg: dict, ax=None):
    """Density/histogram of pseudotime by condition.

    Corresponds to Figure 4.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    else:
        fig = ax.figure

    condition_col = cfg["conditions"]["condition_column"]
    for cond, color in [(cfg["conditions"]["healthy_label"], "#2196F3"),
                        (cfg["conditions"]["covid_label"], "#F44336")]:
        vals = adata.obs.loc[adata.obs[condition_col] == cond, "dpt_pseudotime"]
        ax.hist(vals, bins=50, alpha=0.5, density=True, label=cond, color=color)

    ax.set_xlabel("Pseudotime")
    ax.set_ylabel("Density")
    ax.set_title("Pseudotime distribution by condition")
    ax.legend()
    return fig, ax


def plot_program_trends(trend_df: "pd.DataFrame", ax=None):
    """Gene program scores along pseudotime (smoothed lines).

    Corresponds to Figure 3.

    Parameters
    ----------
    trend_df : pd.DataFrame
        Output of programs.program_trends_along_pseudotime().
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    else:
        fig = ax.figure

    programs = trend_df["program"].unique()
    for prog in programs:
        sub = trend_df[trend_df["program"] == prog].sort_values("pseudotime_center")
        ax.plot(sub["pseudotime_center"], sub["mean_score"], label=prog, linewidth=1.5)
        ax.fill_between(sub["pseudotime_center"],
                        sub["mean_score"] - sub["sem"],
                        sub["mean_score"] + sub["sem"], alpha=0.15)

    ax.set_xlabel("Pseudotime")
    ax.set_ylabel("Program score")
    ax.set_title("Gene program dynamics along pseudotime")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    return fig, ax


def plot_marker_genes_pseudotime(adata, genes: list, ax=None):
    """Individual marker gene expression along pseudotime.

    Corresponds to Figure 5.
    """
    n_genes = len(genes)
    if ax is None:
        fig, axes = plt.subplots(1, n_genes, figsize=(3 * n_genes, 3))
    else:
        fig = ax.figure
        axes = [ax]

    if n_genes == 1:
        axes = [axes]

    pt = adata.obs["dpt_pseudotime"].values
    for i, gene in enumerate(genes):
        if adata.raw is not None and gene in adata.raw.var_names:
            expr = np.asarray(adata.raw[:, gene].X.todense()).flatten()
        elif gene in adata.var_names:
            expr = np.asarray(adata[:, gene].X.todense()).flatten()
        else:
            continue

        ax_i = axes[i]
        # Bin and average for cleaner visualization
        bins = pd.cut(pt, bins=50, labels=False)
        binned = pd.DataFrame({"pt": pt, "expr": expr, "bin": bins})
        means = binned.groupby("bin").agg(pt_mean=("pt", "mean"),
                                          expr_mean=("expr", "mean")).dropna()
        ax_i.plot(means["pt_mean"], means["expr_mean"], linewidth=1.5)
        ax_i.set_title(gene, fontstyle="italic")
        ax_i.set_xlabel("Pseudotime")
        ax_i.set_ylabel("Expression")

    plt.tight_layout()
    return fig, axes


def plot_displacement_boxplot(dist_df: "pd.DataFrame", ax=None):
    """Boxplot of distance to healthy centroid by condition.

    Corresponds to part of Figure 5 / supplementary.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    else:
        fig = ax.figure

    conditions = dist_df["condition"].unique()
    data = [dist_df.loc[dist_df["condition"] == c, "distance_to_healthy_centroid"].values
            for c in conditions]
    bp = ax.boxplot(data, labels=conditions, patch_artist=True, showfliers=False)
    colors = ["#2196F3", "#F44336"]
    for patch, color in zip(bp["boxes"], colors[:len(conditions)]):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    ax.set_ylabel("Distance to healthy centroid")
    ax.set_title("Homeostatic displacement")
    return fig, ax


def plot_donor_pseudotime(donor_df: "pd.DataFrame", ax=None):
    """Pseudotime distributions per donor, colored by condition.

    Corresponds to Figure 7.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
    else:
        fig = ax.figure

    # Sort by median pseudotime
    donor_df = donor_df.sort_values("median_pseudotime")
    colors = {"Control": "#2196F3", "Healthy": "#2196F3", "COVID-19": "#F44336"}
    bar_colors = [colors.get(c, "#999999") for c in donor_df["condition"]]

    ax.barh(range(len(donor_df)), donor_df["median_pseudotime"],
            xerr=donor_df["std_pseudotime"], color=bar_colors, alpha=0.7,
            edgecolor="white")
    ax.set_yticks(range(len(donor_df)))
    ax.set_yticklabels(donor_df["donor"], fontsize=7)
    ax.set_xlabel("Median pseudotime")
    ax.set_title("Pseudotime by donor")
    return fig, ax
