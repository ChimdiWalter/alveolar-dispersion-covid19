"""
Cross-disease generalization framework.

Tests whether dispersion-dominated loss of state coherence generalizes
beyond lethal COVID-19 to other forms of severe lung injury (ARDS,
bacterial pneumonia, IPF, etc.).
"""

import logging
from typing import Optional, List

logger = logging.getLogger("robustness.generalization")

try:
    import numpy as np
    import pandas as pd
    from scipy import stats as sp_stats
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Metadata harmonization
# ---------------------------------------------------------------------------

def harmonize_metadata(
    adata,
    condition_col: str,
    disease_label: str,
    healthy_label: str,
    donor_col: str,
    celltype_col: str,
    dataset_name: str,
) -> None:
    """Harmonize external dataset metadata to match primary pipeline columns.

    Adds standardized columns to adata.obs in place:
    - 'condition_harmonized': 'Disease' or 'Control'
    - 'donor_id_harmonized': unique donor identifier
    - 'dataset_source': dataset name for cross-cohort tracking
    """
    adata.obs["condition_harmonized"] = "Control"
    disease_mask = adata.obs[condition_col] == disease_label
    adata.obs.loc[disease_mask, "condition_harmonized"] = "Disease"

    healthy_mask = adata.obs[condition_col] == healthy_label
    adata.obs.loc[healthy_mask, "condition_harmonized"] = "Control"

    adata.obs["donor_id_harmonized"] = (
        dataset_name + "_" + adata.obs[donor_col].astype(str)
    )
    adata.obs["dataset_source"] = dataset_name
    adata.obs["celltype_harmonized"] = adata.obs[celltype_col].astype(str)


def subset_alveolar_generic(
    adata,
    celltype_col: str = "celltype_harmonized",
    at1_labels: Optional[List[str]] = None,
    at2_labels: Optional[List[str]] = None,
    transitional_labels: Optional[List[str]] = None,
):
    """Subset to alveolar epithelial cells using flexible label matching.

    Falls back to regex matching on common patterns if explicit labels
    are not provided.
    """
    if at1_labels is None:
        at1_labels = ["AT1", "alveolar type 1", "pulmonary alveolar type 1 cell"]
    if at2_labels is None:
        at2_labels = ["AT2", "alveolar type 2", "pulmonary alveolar type 2 cell"]
    if transitional_labels is None:
        transitional_labels = [
            "ECM-high epithelial", "Transitional", "KRT8+ transitional",
            "aberrant basaloid", "DATP",
        ]

    all_labels = at1_labels + at2_labels + transitional_labels
    mask = adata.obs[celltype_col].isin(all_labels)

    if mask.sum() == 0:
        logger.warning("No alveolar cells found with provided labels. "
                       "Available: %s", adata.obs[celltype_col].unique()[:20])
    return adata[mask].copy()


# ---------------------------------------------------------------------------
# Cross-cohort analysis
# ---------------------------------------------------------------------------

def cross_cohort_dispersion(
    adata, condition_col: str = "condition_harmonized",
    rep_key: str = "X_pca",
) -> dict:
    """Run the primary dispersion analysis on a harmonized external dataset.

    Returns the same metrics as the primary analysis for comparison:
    - Within-group variance by condition
    - Levene's test
    - Variance ratio
    """
    rep = adata.obsm.get(rep_key, None)
    if rep is None:
        return {"error": f"representation {rep_key} not found in obsm"}

    conditions = adata.obs[condition_col].values
    disease_mask = conditions == "Disease"
    control_mask = conditions == "Control"

    if disease_mask.sum() < 10 or control_mask.sum() < 10:
        return {"error": "too few cells in one condition"}

    d_centroid = rep[disease_mask].mean(axis=0)
    c_centroid = rep[control_mask].mean(axis=0)
    d_dists = np.linalg.norm(rep[disease_mask] - d_centroid, axis=1)
    c_dists = np.linalg.norm(rep[control_mask] - c_centroid, axis=1)

    stat, p = sp_stats.levene(d_dists, c_dists, center="median")
    var_ratio = float(np.var(d_dists, ddof=1) / np.var(c_dists, ddof=1))

    return {
        "n_disease": int(disease_mask.sum()),
        "n_control": int(control_mask.sum()),
        "disease_variance": float(np.var(d_dists, ddof=1)),
        "control_variance": float(np.var(c_dists, ddof=1)),
        "variance_ratio": var_ratio,
        "levene_stat": float(stat),
        "levene_p": float(p),
    }


def cross_cohort_donor_direction(
    adata,
    score_col: str = "injury_composite",
    condition_col: str = "condition_harmonized",
    donor_col: str = "donor_id_harmonized",
) -> dict:
    """Donor-level Mann-Whitney on injury composite in external dataset."""
    donor_med = (
        adata.obs.groupby([donor_col, condition_col], observed=True)[score_col]
        .median()
        .reset_index()
    )
    dc = donor_med.loc[donor_med[condition_col] == "Disease", score_col].values
    dn = donor_med.loc[donor_med[condition_col] == "Control", score_col].values

    if len(dc) < 3 or len(dn) < 3:
        return {"error": "too few donors"}

    U, p = sp_stats.mannwhitneyu(dc, dn, alternative="greater")
    return {
        "n_disease_donors": len(dc),
        "n_control_donors": len(dn),
        "disease_median": float(np.median(dc)),
        "control_median": float(np.median(dn)),
        "mannwhitney_p": float(p),
    }


def portability_matrix(
    primary_results: dict,
    replication_results: dict,
    external_results: Optional[dict] = None,
) -> "pd.DataFrame":
    """Build a portability matrix comparing findings across cohorts.

    Each row is a finding; columns are cohorts; cells are
    'supported', 'not supported', or 'not tested'.
    """
    findings = [
        "dispersion",
        "pseudotime_shift_cell_level",
        "pseudotime_shift_donor_level",
        "datp_enrichment",
        "program_ordering",
        "centroid_displacement",
    ]

    rows = []
    for f in findings:
        row = {"finding": f}
        row["primary"] = primary_results.get(f, "not tested")
        row["replication"] = replication_results.get(f, "not tested")
        if external_results:
            row["external"] = external_results.get(f, "not tested")
        rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Candidate external datasets
# ---------------------------------------------------------------------------

CANDIDATE_DATASETS = {
    "delorey_2021": {
        "description": "COVID-19 tissue atlases (Nature 2021)",
        "disease": "lethal COVID-19",
        "modality": "snRNA-seq",
        "source": "GEO/SRA",
        "n_donors_approx": "~15 COVID + controls",
        "alveolar_relevance": "high — autopsy lung tissue",
        "acquisition": "download from GEO; reprocess from raw counts",
        "priority": "essential",
    },
    "wendisch_2021": {
        "description": "COVID-19 lung fibrosis (Cell 2021)",
        "disease": "lethal COVID-19 + fibrosis",
        "modality": "scRNA-seq",
        "source": "GEO",
        "n_donors_approx": "~20",
        "alveolar_relevance": "high",
        "acquisition": "download from GEO",
        "priority": "high",
    },
    "adams_2020": {
        "description": "IPF lung atlas (Science Advances 2020)",
        "disease": "idiopathic pulmonary fibrosis",
        "modality": "scRNA-seq",
        "source": "GEO",
        "n_donors_approx": "~32 IPF + 28 control",
        "alveolar_relevance": "high — tests generalization beyond COVID",
        "acquisition": "download from GEO",
        "priority": "high — key for generalization claim",
    },
    "habermann_2020": {
        "description": "IPF lung fibrosis (Science Advances 2020)",
        "disease": "IPF",
        "modality": "scRNA-seq",
        "source": "GEO",
        "n_donors_approx": "~20",
        "alveolar_relevance": "high — aberrant basaloid cells",
        "acquisition": "download from GEO",
        "priority": "medium",
    },
    "hlca_core": {
        "description": "Human Lung Cell Atlas core (Nature Medicine 2023)",
        "disease": "healthy reference",
        "modality": "scRNA-seq + snRNA-seq",
        "source": "cellxgene",
        "n_donors_approx": "~100+",
        "alveolar_relevance": "high — healthy baseline for dispersion",
        "acquisition": "cellxgene census API",
        "priority": "medium",
    },
}
