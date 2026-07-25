# Runbook — Step-by-Step Execution Guide

## Epithelial Robustness Collapse in Lethal COVID-19

---

## Prerequisites

### 1. Environment setup
```bash
source ~/.venvs/lesegenv/bin/activate
cd /deltos/e/lesion_phes/code/python/pipeline/sb_class_project
pip install -r requirements.txt
```

### 2. Verify installation
```bash
python3 -c "import scanpy; import anndata; import pandas; import matplotlib; print('All core packages OK')"
```

### 3. Download data
Download the SCP1219 dataset from the Broad Institute Single Cell Portal:
- URL: https://singlecell.broadinstitute.org/single_cell/study/SCP1219
- Place files in `data/raw/`
- Expected: either a single `.h5ad` file or 10X-format files (matrix.mtx.gz, barcodes.tsv.gz, features.tsv.gz)
- Also download any available metadata files → place in `metadata/`

**Note:** SCP1219 may require authentication or a Terra account. Check the portal for access instructions.

---

## Execution Steps

### Step 0: Validate setup
```bash
python3 -c "
from src.utils import load_config, ensure_dirs
cfg = load_config()
ensure_dirs(cfg)
print('Config loaded. Directories OK.')
print(f'Raw data path: {cfg[\"paths\"][\"raw_data\"]}')
"
```

### Step 1: Load and inspect data
```bash
python3 scripts/run_pipeline.py --step load_and_inspect
```
**Or interactively:**
```python
from src.io import load_atlas, load_metadata
from src.utils import load_config
cfg = load_config()
adata = load_atlas(cfg)
print(adata)
print(adata.obs.columns.tolist())
print(adata.obs.head())
```
**Check:** How many cells? How many genes? What columns are in .obs? What are the condition labels? What are the cell-type annotations called?

**CRITICAL:** After inspection, update `config.yaml` with the correct column names:
- `conditions.condition_column`
- `conditions.healthy_label`
- `conditions.covid_label`
- `cell_types.annotation_column`
- `batch_correction.batch_key`

### Step 2: Quality control
```python
from src.qc import compute_qc_metrics, apply_qc_filters, qc_summary
adata = compute_qc_metrics(adata)
print(qc_summary(adata))
# Inspect distributions before setting thresholds
# Adjust config.yaml QC thresholds if needed based on distributions
adata = apply_qc_filters(adata, cfg)
```
**Output:** QC summary table → `results/tables/tableS2_qc_summary.csv`

### Step 3: Normalize and select HVGs
```python
from src.embedding import normalize_and_select_hvg
adata = normalize_and_select_hvg(adata, cfg)
```

### Step 4: Subset alveolar epithelial cells
```python
from src.annotation import subset_alveolar, validate_markers
marker_df = validate_markers(adata, cfg["markers"], cfg["cell_types"]["annotation_column"])
# Inspect marker_df — do labels match markers?
marker_df.to_csv("results/tables/tableS3_marker_validation.csv")

alv = subset_alveolar(adata, cfg)
```

### Step 5: Batch assessment and correction
```python
from src.embedding import run_pca, run_neighbors, run_umap, run_harmony
alv = run_pca(alv, cfg)
alv = run_neighbors(alv, cfg)
alv = run_umap(alv, cfg)
# Visualize by donor — is there batch stratification?

# If batch correction needed:
alv = run_harmony(alv, cfg)
alv = run_neighbors(alv, cfg, use_rep="X_pca_harmony")
alv = run_umap(alv, cfg)
```

### Step 6: Diffusion map and trajectory
```python
from src.embedding import run_diffmap
from src.trajectory import run_dpt, pseudotime_density_by_condition, pseudotime_by_donor

alv = run_diffmap(alv, cfg)
alv = run_dpt(alv, cfg)

pt_density = pseudotime_density_by_condition(alv, cfg)
pt_donor = pseudotime_by_donor(alv, cfg)
```

### Step 7: Gene program scoring
```python
from src.programs import score_gene_programs, program_trends_along_pseudotime
alv = score_gene_programs(alv, cfg)
trends = program_trends_along_pseudotime(alv, cfg)
```

### Step 8: Statistical tests
```python
from src.stats import (centroid_distance, displacement_test, dispersion_test,
                       nn_condition_mixing, permutation_test_pseudotime,
                       robustness_composite_score)

dist_df = centroid_distance(alv, cfg)
disp_result = displacement_test(dist_df, cfg["conditions"]["healthy_label"],
                                 cfg["conditions"]["covid_label"])
var_result = dispersion_test(alv, cfg)
perm_result = permutation_test_pseudotime(alv, cfg)
composite = robustness_composite_score(disp_result, var_result, perm_result)
```

### Step 9: Generate figures
```python
from src.plots import *
fig1a, _ = plot_umap_condition(alv, cfg)
save_fig(fig1a, "fig1a_condition")

fig1b, _ = plot_umap_celltype(alv, cfg)
save_fig(fig1b, "fig1b_celltype")

fig2, _ = plot_umap_pseudotime(alv)
save_fig(fig2, "fig2_pseudotime")

fig3, _ = plot_program_trends(trends)
save_fig(fig3, "fig3_program_dynamics")

fig4, _ = plot_pseudotime_density(alv, cfg)
save_fig(fig4, "fig4_pseudotime_density")

fig5, _ = plot_marker_genes_pseudotime(alv, ["SFTPC", "AGER", "KRT8", "ISG15", "CASP3", "BAX"])
save_fig(fig5, "fig5_marker_trends")

fig7, _ = plot_donor_pseudotime(pt_donor)
save_fig(fig7, "fig7_donor_consistency")
```

### Step 10: Save processed data
```python
from src.io import save_adata
save_adata(alv, "alveolar_final", cfg)
```

### Step 11: Run ablations
Repeat Steps 4–8 with modifications per ablation specification (see ANALYSIS_PLAN.md Section 6). Save each ablation's metrics to `results/tables/ablation_XX_metrics.csv`.

### Step 12: Generate ablation summary figure
Compile ablation results into Figure 6.

---

## Checkpoints

| Step | Checkpoint | What to verify |
|------|-----------|----------------|
| 1 | Data loaded | Cell count matches expectation (~116K total) |
| 2 | QC complete | Reasonable cell retention (>80%) |
| 4 | Alveolar subset | ~20K+ cells, markers validate correctly |
| 5 | Batch assessment | Donors not dominating UMAP structure |
| 6 | Pseudotime | Healthy cells at low PT, COVID at high PT |
| 7 | Programs scored | All 8 programs scored with >50% gene coverage |
| 8 | Statistics | Displacement test significant with reasonable effect size |
| 9 | Figures | All 7 main figures generated |
| 11 | Ablations | ≥7/10 ablations consistent with primary findings |

---

## Troubleshooting

| Problem | Likely cause | Solution |
|---------|-------------|----------|
| `FileNotFoundError` on load | Data not downloaded | Download SCP1219 → `data/raw/` |
| `KeyError` on column access | Wrong column name in config | Inspect `adata.obs.columns` and update config.yaml |
| UMAP shows donor-dominated structure | Batch effects | Apply Harmony; verify correction |
| Pseudotime looks random | Weak trajectory signal | Check graph connectivity; consider cluster-based analysis instead |
| Program scores all near zero | Gene names don't match | Check gene symbol format (HGNC vs Ensembl) |
| Memory error on full atlas | Dataset too large | Work on alveolar subset only; or increase available RAM |
