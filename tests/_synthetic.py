"""
Synthetic AnnData builder used by the test suite.

Produces a small, fully deterministic dataset that mimics the *schema* of the
real SCP1219 alveolar atlas (obs columns, gene panel, condition/donor
structure) without containing or requiring any real data. This lets the
pipeline be smoke-tested end-to-end without the (large, auth-gated) SCP1219
download.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import anndata as ad
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Donor layout: (donor_id, condition, n_cells). Uneven donor sizes and an
# imbalanced donor count per condition mirror the real cohort structure
# (7 healthy vs 20 COVID-19 donors in SCP1219) at a much smaller scale.
_DONOR_LAYOUT = [
    ("D01", "Control", 28),
    ("D02", "Control", 35),
    ("D03", "Control", 22),
    ("D04", "Control", 31),
    ("D05", "COVID-19", 30),
    ("D06", "COVID-19", 45),
    ("D07", "COVID-19", 26),
    ("D08", "COVID-19", 38),
    ("D09", "COVID-19", 33),
]

_CELL_TYPES = ["AT2", "AT1", "ECM-high epithelial"]

_MT_GENES = ["MT-CO1", "MT-ND1", "MT-CYB", "MT-ATP6", "MT-ND2"]

N_FILLER_GENES = 220


def config_marker_and_program_genes(cfg: dict | None = None) -> list[str]:
    """Union of every gene referenced in config.yaml's markers/gene_programs sections."""
    if cfg is None:
        with open(PROJECT_ROOT / "config.yaml") as f:
            cfg = yaml.safe_load(f)
    genes = set()
    for gene_list in cfg["markers"].values():
        genes.update(gene_list)
    for prog in cfg["gene_programs"].values():
        genes.update(prog["genes"])
    return sorted(genes)


def _cell_type_marker_map(cfg: dict) -> dict[str, list[str]]:
    """Map each synthetic cell type to the marker genes that should be elevated in it."""
    return {
        "AT2": cfg["markers"]["AT2"],
        "AT1": cfg["markers"]["AT1"],
        "ECM-high epithelial": cfg["markers"]["transitional"],
    }


def make_synthetic_atlas(seed: int = 42, cfg: dict | None = None) -> "ad.AnnData":
    """Build a small, deterministic synthetic alveolar atlas.

    Schema mirrors config.yaml: obs columns `cell_type_fine` (AT1/AT2/
    ECM-high epithelial), `group` (Control/COVID-19), `donor_id`. Gene panel
    is the union of all marker + gene-program genes plus a handful of MT-
    genes and filler genes so QC/HVG selection has real room to operate.

    Counts are simulated with a Poisson model: baseline expression for all
    genes, an elevated rate for each cell type's marker genes in that cell
    type, and a seeded COVID-vs-Control shift (higher interferon_response /
    apoptosis program expression, and higher per-cell variance) so
    downstream statistical tests have real, non-degenerate signal to detect.
    This is a fixture property for testing, not a biological claim.

    Returns
    -------
    anndata.AnnData (cells x genes), raw integer counts in .X
    """
    if cfg is None:
        with open(PROJECT_ROOT / "config.yaml") as f:
            cfg = yaml.safe_load(f)

    rng = np.random.default_rng(seed)

    marker_genes = config_marker_and_program_genes(cfg)
    filler_genes = [f"GENE{i:04d}" for i in range(N_FILLER_GENES)]
    genes = marker_genes + _MT_GENES + filler_genes
    n_genes = len(genes)
    gene_index = {g: i for i, g in enumerate(genes)}

    ct_markers = _cell_type_marker_map(cfg)
    interferon_genes = cfg["gene_programs"]["interferon_response"]["genes"]
    apoptosis_genes = cfg["gene_programs"]["apoptosis"]["genes"]
    covid_shift_genes = [g for g in (interferon_genes + apoptosis_genes) if g in gene_index]

    # Build per-cell metadata
    donor_ids, conditions, cell_types = [], [], []
    for donor_id, condition, n_cells in _DONOR_LAYOUT:
        donor_ids.extend([donor_id] * n_cells)
        conditions.extend([condition] * n_cells)
        # Roughly even split across the three cell types within a donor.
        cts = rng.choice(_CELL_TYPES, size=n_cells, replace=True)
        cell_types.extend(cts.tolist())

    n_cells_total = len(donor_ids)

    # Baseline expression: modest for marker/program genes, low for filler
    # and MT genes (so MT never dominates library size by default).
    baseline = np.full(n_genes, 1.5)
    for g in marker_genes:
        baseline[gene_index[g]] = 3.0
    for g in _MT_GENES:
        baseline[gene_index[g]] = 2.0

    # Per-cell multiplicative "activity" factor: COVID-19 cells get a wider
    # spread than Control, which is what drives real dispersion signal
    # (Levene's test on the embedding) rather than just a mean shift.
    activity = np.empty(n_cells_total)
    is_covid = np.array([c == "COVID-19" for c in conditions])
    activity[~is_covid] = rng.normal(1.0, 0.12, size=(~is_covid).sum())
    activity[is_covid] = rng.normal(1.0, 0.45, size=is_covid.sum())
    activity = np.clip(activity, 0.15, None)

    lam = np.tile(baseline, (n_cells_total, 1)) * activity[:, None]

    # Elevate each cell's own cell-type marker genes.
    for i, ct in enumerate(cell_types):
        for g in ct_markers[ct]:
            lam[i, gene_index[g]] += 12.0

    # COVID-vs-Control shift on interferon/apoptosis program genes.
    for i in range(n_cells_total):
        if is_covid[i]:
            for g in covid_shift_genes:
                lam[i, gene_index[g]] += 30.0

    counts = rng.poisson(lam).astype(np.float32)
    X = sp.csr_matrix(counts)

    obs = pd.DataFrame(
        {
            "cell_type_fine": pd.Categorical(cell_types),
            "group": pd.Categorical(conditions, categories=["Control", "COVID-19"]),
            "donor_id": pd.Categorical(donor_ids),
        },
        index=[f"cell_{i:05d}" for i in range(n_cells_total)],
    )

    adata = ad.AnnData(X=X, obs=obs)
    adata.var_names = genes
    adata.var_names_make_unique()
    return adata
