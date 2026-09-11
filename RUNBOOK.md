# Runbook — Step-by-Step Execution Guide

## Epithelial Robustness Collapse in Lethal COVID-19

---

## Prerequisites

### 1. Environment setup
```bash
python3 -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```
**Note:** the reproducibility harness adds `make install` / `make test` targets
that wrap this, plus a pinned `requirements.lock.txt` snapshot of exact working
versions — prefer those over the raw `pip install` above. The paths above
replace the original author's machine-specific `~/.venvs/lesegenv` /
`/deltos/e/lesion_phes/...` setup, which will not exist on any other machine.

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

## Post-Hoc Validation Steps (2026-08-25)

Executable procedures for the four follow-ups specified in `ANALYSIS_PLAN.md` §9.
None of these have been run yet — see each step's **Check** for the falsifiable
outcome that determines whether it succeeded.

### Step 13: Expanded-panel replication re-fetch (ANALYSIS_PLAN.md §9 Follow-up 1)

**No SCP1219 portal access needed** — unlike every other step in this runbook,
`cellxgene_census` is a public, no-login API. This is why it's the highest-priority
follow-up: it's the only one not gated on manual data acquisition.

`scripts/replication/fetch_replication.py`'s `gene_shortlist` (lines 31–43) is
currently `program_genes | marker_extras` — restricted purely "to keep the download
compact (<1 GB)" per the code's own comment, not an API limitation. Loosen it:

```python
# In scripts/replication/fetch_replication.py, replace the gene_shortlist block
# (lines 31-43) with a larger set. Two options, in order of increasing scope:

# Option A — expanded HVG-driven panel (recommended first pass):
#   Query a broader set (e.g. 2,000-3,000 genes) rather than the current ~84.
#   Combine the existing program_genes | marker_extras with a scanpy HVG selection
#   run once on a small pilot query, or simply widen marker_extras substantially.

# Option B — full transcriptome (drop the gene filter entirely):
#   Remove the var_value_filter argument to cc.get_anndata() so all genes are
#   returned. Expect the download to be far larger than 1GB across 921,510 raw
#   alveolar cells (per analyze_replication.py's docstring) — start with Option A
#   unless you have the disk/memory budget for a full-transcriptome pull.
```

```bash
python3 scripts/replication/fetch_replication.py
python3 scripts/replication/analyze_replication.py
```

**Check:** the expanded cohort supports a genuine manifold/DPT reconstruction (not
just the current program-score-composite surrogate), and dispersion + donor-level
pseudotime direction still replicate under that reconstruction — not just under the
composite score. If they don't, that weakens the "most portable finding" claim and
the 84-gene composite approach itself needs scrutiny (see §9 Follow-up 1's Failure
mode in `ANALYSIS_PLAN.md`).
**Also tune if needed:** the per-donor subsampling cap (currently 200 cells/donor,
`analyze_replication.py`) is a second knob if the expanded download is too large.
**Output:** `data/replication/replication_alveolar.h5ad` (larger), `results/replication/` (updated).

### Step 14: Re-run the ablation grid with per-ablation displacement (ANALYSIS_PLAN.md §9 Follow-up 2)

**Gated on real SCP1219 data in `data/raw/`** (see Prerequisites §3) — unlike Step 13.

`centroid_distance()` (`src/stats.py`) defaults to `rep_key="X_pca"` and is never
passed the ablation's actual embedding, so `displacement_effect_size` is silently
frozen at the primary run's cached value (`r = 0.1407`) across ablations 02
(embedding), 03 (batch-correction), 05 (root-strategy), 08 (gene-program), and 09
(Palantir) in `results/tables/tableS6_ablation_summary.csv`.

```python
# Fix the call sites in the ablation runner so each ablation passes its own
# embedding to centroid_distance(), e.g.:
#   Ablation 03 (batch-corrected variant): centroid_distance(alv, cfg, rep_key="X_pca_harmony")
#   Ablation 02 (UMAP variant):            centroid_distance(alv, cfg, rep_key="X_umap")
#   Ablation 05 (each root variant):       recompute on that variant's own X_pca/X_diffmap
#   Ablation 08 (alt gene programs):       recompute on that variant's own re-embedded X_pca
#   Ablation 09 (Palantir):                recompute displacement on the Palantir-consistent embedding
```

```bash
python3 scripts/ablations/run_all_ablations.py
```

**Check:** `displacement_effect_size` now VARIES across ablations 02/03/05/08/09
instead of being a constant `0.1407` in `results/tables/tableS6_ablation_summary.csv`.
If any ablation's recomputed value becomes significant in the hypothesized direction
(COVID > Healthy), `paper_v3.tex` line 222's "never significant... across all
ablations" claim needs revision.
**Output:** `results/tables/tableS6_ablation_summary.csv` (corrected), `results/ablations/*/metrics.{csv,json}` (re-run).

### Step 15: Investigate ablation 1's displacement sign flip (ANALYSIS_PLAN.md §9 Follow-up 3)

`results/ablations/01_at2_only/metrics.json` shows displacement flips sign entirely
under AT2-only restriction (`r = +0.14` primary → `r ≈ -0.29` AT2-only) — not
mentioned anywhere in `paper_v3.tex`'s ablation robustness discussion.

```python
from src.stats import centroid_distance
import anndata as ad

alv = ad.read_h5ad("data/processed/alveolar_embedded.h5ad")  # or ablation 1's own embedding
at1 = alv[alv.obs["cell_type_fine"] == "AT1"]
at2 = alv[alv.obs["cell_type_fine"] == "AT2"]
# Compare distance-to-healthy-centroid distributions between AT1 and AT2 directly
# to see whether AT1 cells are systematically driving the primary-cohort
# displacement signal that AT2-only restriction removes.
```

**Check:** either a mechanistic explanation for the AT1/AT2 asymmetry emerges, or
it's determined to be a data artifact — and `paper_v3.tex` is updated either way
(currently silent on this ablation's displacement result).
**Output:** an explanatory note added to `paper_v3.tex`'s ablation-robustness
discussion, or a documented artifact determination in `ANALYSIS_PLAN.md`.

### Step 16: Validate the mechanism regression (ANALYSIS_PLAN.md §9 Follow-up 4)

`results/v3/fan_out_contribution.csv` (senescence coeff 6.83, oxidative_stress 3.83,
nfkb_inflammatory 1.95) is an unregularized OLS with no p-values or cross-validation
in the underlying file.

```python
# In src/mechanism.py's fan_out_contribution():
#   1. Add permutation-based p-values: shuffle the target (distance-to-healthy-
#      centroid) N times, refit, and compare each coefficient's magnitude to its
#      null distribution.
#   2. Add cross-validated R^2 (e.g. k-fold) instead of reporting only in-sample R^2.
```

```bash
python3 -c "
from src.mechanism import fan_out_contribution
from src.utils import load_config
import anndata as ad
cfg = load_config()
alv = ad.read_h5ad('data/processed/alveolar_programs.h5ad')
fan_out_contribution(alv, cfg)  # after adding permutation p-values + CV R^2
"
```

**Check:** senescence/oxidative-stress/NF-κB coefficients survive permutation
testing and cross-validated R² is meaningfully above zero. If not, the Discussion's
"Mechanistic decomposition" paragraph (`paper_v3.tex` line 277) needs substantial
caveating or removal rather than presentation as a partial-but-real finding.
**Output:** `results/v3/fan_out_contribution.csv` (with p-value/CV columns added).

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
| 8 | Statistics | Dispersion (Levene) significant, variance ratio ≈2.3; displacement (Mann–Whitney) **not** significant — see note below |
| 9 | Figures | All 7 main figures generated |
| 11 | Ablations | ≥7/10 ablations consistent with primary findings |
| 13 | Expanded-panel replication | Genuine manifold/DPT reconstruction succeeds on expanded cohort; dispersion + donor-level direction still replicate |
| 14 | Ablation displacement recomputed | `displacement_effect_size` differs across ablations 02/03/05/08/09 — no longer a constant `0.1407` |
| 15 | AT2-only sign flip investigated | Explanation or artifact determination documented; `paper_v3.tex` updated |
| 16 | Mechanism regression validated | Coefficients survive permutation testing; cross-validated R² reported (not just in-sample) |

**Note on checkpoint 8 (corrected 2026-08-25):** this row previously read
"Displacement test significant with reasonable effect size," which inverts the
study's actual central finding. A *non-significant* displacement test
(`p = 1.0`, rank-biserial `r = 0.14` opposite to the hypothesized direction)
alongside *significant* dispersion is the expected and correct result — it is
what discriminates the dispersion model from the coherent-displacement model
(`paper_v3.tex`, Results §"Two competing models"). Do not treat a null
displacement result here as a pipeline failure.

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
| `cellxgene_census` fetch too slow / exceeds disk or memory (Step 13) | Expanded/full-transcriptome gene panel across 921,510 raw alveolar cells is much larger than the original 84-gene, <1GB pull | Start with an expanded HVG-driven panel (Option A) rather than full transcriptome (Option B); tighten the per-donor cell cap in `analyze_replication.py` |
| `FileNotFoundError` on Steps 14–15 | `data/raw/` still empty — real SCP1219 data was never downloaded to this environment | Download SCP1219 per Prerequisites §3 first; these two steps cannot run on synthetic data |
| `harmonypy` fails to build (`CMake Error`, `nmake` not found) | No C++ build toolchain on this machine (a real issue hit on Windows dev machines) | Skip Harmony locally; it builds fine on Linux (confirmed on GitHub Actions CI) — run Harmony-dependent steps there instead |
| Out-of-memory building the diffusion map on an expanded-panel replication cohort (Step 13) | Full/expanded-panel h5ad too large to hold densely in memory for DPT | Keep the matrix sparse through preprocessing; subsample donors further; or run on a machine with more RAM |
