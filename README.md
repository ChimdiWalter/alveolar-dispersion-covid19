# Dispersion, Not Displacement: Loss of Alveolar Epithelial State Coherence in Lethal COVID-19

Pierce Taylor, Chimdi Walter Ndubuisi, and Toni Kazic

Trajectory analysis of alveolar cell-state failure in the Columbia/NYP Lung Atlas (SCP1219).

## Overview

This project tests two competing geometric models of alveolar epithelial injury in lethal COVID-19: coherent displacement (all cells shift toward a single damaged state) versus heterogeneous dispersion (cells fan outward across multiple injury states). Using 22,128 alveolar epithelial cells from the Columbia/NYP COVID-19 Lung Atlas (SCP1219; 7 healthy donors, 20 COVID-19 donors), we score eight gene programs along diffusion pseudotime and evaluate robustness through ten pre-specified ablation analyses, Harmony batch correction, an orthogonal trajectory algorithm (Palantir), and independent replication on 89,736 cells from 618 donors across 35 datasets.

**Key findings:**

- Coherent centroid displacement was not supported (one-sided Mann-Whitney p = 1.0)
- Within-group dispersion was strongly supported (variance ratio 2.3; Levene p < 10^-30) and replicated cross-cohort (variance ratio 1.65; p ~ 10^-137)
- COVID-19 cells were enriched at higher pseudotime (permutation p = 0.001; median difference +0.048), preserved in 27/27 leave-one-donor-out iterations and amplified 2.6-fold under Harmony batch correction
- A KRT8+/CLDN4+ transitional population was enriched 3.1-fold in the primary atlas but did not transfer cross-cohort under marker-threshold definitions

## Repository structure

```
.
├── config.yaml                 # Centralized project configuration
├── requirements.txt            # Python dependencies
├── Makefile                    # Convenience targets
├── Snakefile                   # Snakemake workflow DAG
│
├── src/                        # Core analysis library
│   ├── io.py                   # Data loading and saving
│   ├── qc.py                   # Quality control
│   ├── annotation.py           # Cell-type annotation and validation
│   ├── embedding.py            # PCA, UMAP, diffusion map, Harmony
│   ├── trajectory.py           # Pseudotime inference (DPT, Palantir)
│   ├── programs.py             # Gene program scoring
│   ├── stats.py                # Statistical tests and metrics
│   ├── plots.py                # Publication-quality figures
│   ├── donor_models.py         # Donor-level inference
│   ├── state_score.py          # Portable transitional-state scoring
│   ├── mechanism.py            # Program-to-geometry linkage
│   └── generalization.py       # Cross-disease generalization
│
├── scripts/                    # Pipeline entry points
│   ├── run_pipeline.py         # End-to-end pipeline runner
│   ├── download_data.py        # Data acquisition
│   ├── run_v3_analyses.py      # v3 replication analyses
│   └── generate_v3_figures.py  # v3 figure generation
│
├── notebooks/                  # Jupyter analysis notebooks
│   ├── 01_data_inspection.ipynb
│   ├── 02_qc_and_subset.ipynb
│   └── 03_trajectory_exploration.ipynb
│
├── manuscript/                 # Reports and presentations
│   ├── presentation_report.org # Full presentation report (org-mode)
│   ├── paper_v3.tex            # LaTeX manuscript (v3 dispersion framing)
│   ├── paper.tex               # LaTeX manuscript (v1)
│   └── ...                     # Presentations and explainers
│
├── results/
│   ├── figures/                # Generated figures
│   └── tables/                 # Generated tables
│
├── metadata/                   # Gene program definitions
├── docs/                       # Literature review, validation plans
└── data/                       # Raw and processed data (not committed)
```

## Dataset

**Columbia University / NYP COVID-19 Lung Atlas (SCP1219)**

- Assay: single-nucleus RNA-seq
- Total cells: 116,313
- Alveolar subset: 22,128 cells (9,608 AT1; 11,341 AT2; 1,179 ECM-high transitional)
- Donors: 27 (7 healthy controls, 20 COVID-19)
- Source: [Single Cell Portal SCP1219](https://singlecell.broadinstitute.org/single_cell/study/SCP1219)
- Reference: Melms et al. (2021) Nature 595:114-119

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Download data (place SCP1219 files in data/raw/)
python scripts/download_data.py

# Run the full pipeline
python scripts/run_pipeline.py

# Or use Make
make pipeline

# Or use Snakemake
snakemake -j4
```

## Computational stack

Python 3.12+ with scanpy 1.12, anndata, numpy, scipy, pandas, harmonypy, palantir, matplotlib, statsmodels. Full list in `requirements.txt`.

## Study design documents

| Document | Purpose |
|----------|---------|
| [ANALYSIS_PLAN.md](ANALYSIS_PLAN.md) | Full study design with statistical plan |
| [FIGURE_PLAN.md](FIGURE_PLAN.md) | Figure specifications |
| [TABLE_PLAN.md](TABLE_PLAN.md) | Table specifications |
| [MANUSCRIPT_OUTLINE.md](MANUSCRIPT_OUTLINE.md) | Manuscript skeleton |
| [RUNBOOK.md](RUNBOOK.md) | Step-by-step execution guide |
| [project_proposal.md](project_proposal.md) | Original project proposal |

## References

1. Melms JC et al. (2021). A molecular single-cell lung atlas of lethal COVID-19. Nature 595:114-119.
2. Kobayashi Y et al. (2020). Persistence of a regeneration-associated, transitional alveolar epithelial cell state in pulmonary fibrosis. Nature Cell Biology 22:934-946.
3. Strunz M et al. (2020). Alveolar regeneration through a Krt8+ transitional stem cell state that persists in human lung fibrosis. Nature Communications 11:3559.
4. Haghverdi L et al. (2016). Diffusion pseudotime robustly reconstructs lineage branching. Nature Methods 13:845-848.
5. Setty M et al. (2019). Characterization of cell fate probabilities in single-cell data with Palantir. Nature Biotechnology 37:451-460.
