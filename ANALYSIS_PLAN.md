# Analysis Plan — Manuscript-Grade Study Design

## Dispersion, Not Displacement: Loss of Alveolar Epithelial State Coherence in Lethal COVID-19

**Paper v3 revision: 2026-04-30**

---

## 1. Refined Aims

### Aim 1 (Primary): Test competing geometric models of epithelial injury

**Objective:** Distinguish between coherent centroid displacement (all cells shift toward one damaged state) and dispersion-dominated fan-out (cells scatter heterogeneously) in lethal COVID-19 alveolar epithelium. The primary inferential unit is the **donor**, not the cell.

**Primary analyses:**
- Dispersion: within-group variance comparison (Levene's test) — **primary metric**
- Centroid distance: COVID vs healthy distance to healthy centroid (Mann-Whitney U) — **pre-registered, expected negative**
- Donor-level pseudotime: per-donor median pseudotime comparison
- Donor-level bootstrap CIs for pseudotime shift and dispersion ratio
- Nearest-neighbor condition mixing score

**Donor-aware analyses (essential for paper_v3):**
- Donor-level summary table: median pseudotime, IQR, dispersion, frac_transitional, program scores per donor (`src/donor_models.py`)
- Donor-level Mann-Whitney for all key metrics
- Donor-level bootstrap CIs (10,000 resamples of donors, not cells) for pseudotime shift and dispersion ratio
- OLS or mixed-effects model: median_pseudotime ~ is_covid (donor-level)
- Per-donor dispersion comparison (median distance to own-group centroid)

**Secondary analyses:**
- AT1-specific and AT2-specific displacement (do they differ?)
- Donor-stratified displacement (is the effect consistent?)

### Aim 2 (Primary): Reconstruct the failure trajectory and characterize gene program dynamics

**Objective:** Test whether alveolar cells distribute along a continuous pseudotime trajectory with ordered activation of stress, repair, and apoptosis programs.

**Primary analyses:**
- Diffusion pseudotime (DPT) rooted in healthy AT2 centroid
- Gene program scoring (8 programs) along pseudotime
- Pseudotime density comparison: COVID vs healthy (permutation test)
- Program activation ordering: test whether interferon peaks before inflammation, inflammation before repair, repair before apoptosis

**Secondary analyses:**
- Branching analysis: does the trajectory bifurcate (repair vs death)?
- Individual marker gene trends along pseudotime (Spearman correlation)
- Differential expression analysis along pseudotime (GAM-based)

### Aim 3 (Sensitivity): Ablation and robustness validation

**Objective:** Determine which findings survive systematic perturbation of analytical choices.

**Primary analyses:**
- 10 ablation experiments (see Section 6)
- Leave-one-donor-out stability assessment

**Secondary analyses:**
- Random gene-set controls for program scoring
- UMAP random-seed stability
- Comparison to published findings on SCP1219

---

## 2. Operational Definitions

### Homeostasis
Operationally defined as the transcriptomic state of alveolar epithelial cells from healthy donors. Identified as cells with:
- Condition label = "Healthy"
- High expression of canonical identity markers (SFTPC for AT2, AGER for AT1)
- Low expression of stress/apoptosis programs
- Located in the dense core of the healthy cell distribution in PCA space

### Robustness loss
Defined by convergence of five criteria (all must be assessed; no single criterion is sufficient):

| # | Criterion | Metric | Test |
|---|-----------|--------|------|
| 1 | Displacement from homeostasis | Distance to healthy centroid | Mann-Whitney U, COVID > Healthy |
| 2 | Increased dispersion | Within-group variance | Levene's test |
| 3 | Loss of identity markers | SFTPC, AGER decline along pseudotime | Spearman rho < 0, p < 0.05 |
| 4 | Ordered program activation | Interferon peak < inflammation peak < repair peak < apoptosis peak | Peak position comparison |
| 5 | Stalled differentiation | KRT8/CLDN4 elevated at intermediate pseudotime in COVID cells | Enrichment test at intermediate bins |

### Transitional / failed-repair state
Cells meeting ALL of the following:
- Pseudotime in the middle tertile (33rd–66th percentile)
- KRT8 expression > median AND/OR CLDN4 expression > median
- AT2 identity score declining but not zero
- AT1 identity score partially activated but not at healthy AT1 levels
- Predominantly from COVID donors

### Apoptosis-associated terminal state
Cells meeting:
- Pseudotime in the top decile (>90th percentile)
- Apoptosis program score > 75th percentile
- AT2 and AT1 identity scores in bottom quartile
- Stress program scores elevated

---

## 3. Statistical Analysis Plan

### 3.1 Sample size and power
The dataset contains ~20,000+ alveolar epithelial cells. For the primary displacement test (Mann-Whitney U comparing ~15,000 COVID vs ~5,000 healthy cells), statistical power is effectively 1.0 for any biologically meaningful effect. The concern is not statistical power but rather whether observed effects are biologically meaningful and robust to analytical variation (hence the extensive ablation plan).

**Emphasis:** We focus on effect sizes, not just p-values. With N > 20,000, trivially small effects will be statistically significant. We will report:
- Effect size (rank-biserial r for Mann-Whitney U)
- Cohen's d for mean differences
- Confidence intervals for all point estimates
- Visualization of distributions, not just summary statistics

### 3.2 Multiple testing
- Gene-level pseudotime trend tests: Benjamini-Hochberg FDR correction at α = 0.05
- Program-level tests: 8 programs tested; Bonferroni correction applied (effective α = 0.00625)
- Ablation comparisons: not multiplicity-corrected (each is an independent sensitivity check, not a hypothesis test)

### 3.3 Primary statistical tests

| Analysis | Test | Null hypothesis | Alternative | Correction |
|----------|------|-----------------|-------------|------------|
| Displacement | Mann-Whitney U | COVID distance = Healthy distance | COVID > Healthy | None (single primary test) |
| Dispersion | Levene's test | Var(COVID) = Var(Healthy) | Var(COVID) > Var(Healthy) | None |
| Pseudotime enrichment | Permutation test (N=1000) | Condition labels independent of pseudotime | COVID enriched at high pseudotime | None |
| Gene trend | Spearman correlation | No monotonic trend along pseudotime | Trend exists | BH FDR |
| Program ordering | Peak pseudotime comparison | Random ordering | Interferon < inflammation < repair < apoptosis | Descriptive |
| Donor consistency | Kruskal-Wallis | All donors same pseudotime distribution | Variation exists | By condition |

### 3.4 Sensitivity analysis framework
Each ablation produces a "core metric" that is compared to the primary analysis. Core metrics:
1. Median pseudotime difference (COVID - Healthy)
2. Program ordering (rank correlation of peak positions with expected ordering)
3. Displacement effect size (rank-biserial r)

An ablation "passes" if the core metric retains the same sign and the same qualitative conclusion. Quantitative differences are expected and reported.

---

## 4. Primary vs Secondary vs Sensitivity Analyses

### Primary (publication-critical)
These are the analyses that directly test the central hypothesis. If these fail, the paper does not exist.

1. Alveolar epithelial manifold construction and condition comparison
2. Pseudotime trajectory reconstruction
3. Gene program scoring and ordering along pseudotime
4. Displacement and dispersion quantification
5. Transitional state characterization

### Secondary (strengthening but not required)
These add depth but the paper stands without them.

6. AT1 vs AT2 separate trajectory analysis
7. Branching/fate analysis
8. Differential expression along pseudotime
9. Comparison to published findings

### Sensitivity (Aim 3 — validation)
These determine the confidence level of the primary findings.

10. All 10 ablation experiments
11. Permutation controls
12. Random gene-set controls
13. Leave-one-donor-out
14. UMAP stability

---

## 5. Experiment Specifications

### Experiment 1: Alveolar epithelial subset validation

| Field | Value |
|-------|-------|
| Purpose | Confirm cell identity before any trajectory analysis |
| Input | Full atlas (116,313 cells) with metadata |
| Method | Subset AT1/AT2/transitional by annotation; validate with marker dotplots |
| Primary output | `data/processed/alveolar_validated.h5ad` |
| Plots | Marker gene dotplot, UMAP of epithelial subset |
| Tables | Table S1: marker validation matrix |
| Code module | `src/annotation.py` → `validate_markers()`, `subset_alveolar()` |
| Failure mode | Annotations do not match markers → must re-cluster and re-annotate |

### Experiment 2: Manifold construction and condition comparison

| Field | Value |
|-------|-------|
| Purpose | Build the transcriptomic landscape; compare healthy vs COVID spatial distributions |
| Input | Validated alveolar cells |
| Method | PCA → neighbors → UMAP + diffusion map |
| Primary output | `data/processed/alveolar_embedded.h5ad` |
| Plots | Fig 1 (UMAP by condition + cell type), UMAP by donor |
| Tables | Table 1: cohort summary (cells per donor, per condition) |
| Code module | `src/embedding.py` |
| Failure mode | Manifold organizes by donor instead of biology → apply Harmony |

### Experiment 3: Pseudotime trajectory reconstruction

| Field | Value |
|-------|-------|
| Purpose | Infer continuous ordering from homeostasis to failure |
| Input | Embedded alveolar cells with diffusion map |
| Method | DPT rooted in healthy AT2 centroid |
| Primary output | `data/processed/alveolar_pseudotime.h5ad` |
| Plots | Fig 2 (UMAP colored by pseudotime), Fig 4 (pseudotime density by condition) |
| Tables | Pseudotime summary by condition, pseudotime summary by donor |
| Code module | `src/trajectory.py` |
| Failure mode | No continuous trajectory → fall back to cluster-based analysis |

### Experiment 4: Gene program dynamics

| Field | Value |
|-------|-------|
| Purpose | Test whether programs activate in a staged, biologically coherent order |
| Input | Pseudotime-ordered cells; 8 gene programs from config |
| Method | score_genes per program; plot trends along pseudotime |
| Primary output | Program scores in adata.obs; trend DataFrame |
| Plots | Fig 3 (program trends), Fig 5 (marker gene trends) |
| Tables | Table S2: gene program definitions; trend statistics table |
| Code module | `src/programs.py` |
| Failure mode | Programs activate simultaneously → process is catastrophic, not staged |

### Experiment 5: Displacement and dispersion quantification

| Field | Value |
|-------|-------|
| Purpose | Statistical evidence for robustness loss |
| Input | Embedded cells with condition labels |
| Method | Centroid distance + Mann-Whitney U; Levene's test; NN mixing |
| Primary output | Displacement test results; dispersion test results |
| Plots | Displacement boxplot; NN mixing histogram |
| Tables | Main Table 2: robustness metrics summary |
| Code module | `src/stats.py` |
| Failure mode | Non-significant → the claim of displacement is not supported |

### Experiment 6: Transitional state characterization

| Field | Value |
|-------|-------|
| Purpose | Identify cells with evidence of stalled AT2-to-AT1 differentiation |
| Input | Pseudotime-ordered cells with program scores |
| Method | Identify cells at intermediate pseudotime with high KRT8/CLDN4 and partial AT1 markers |
| Primary output | Transitional cell subset; characterization table |
| Plots | Marker co-expression scatter; pseudotime location of transitional cells |
| Tables | Transitional cell marker profile |
| Code module | `src/annotation.py` + `src/programs.py` |
| Failure mode | No clear transitional population → repair may not be attempted or detectable |

### Experiment 7: Donor-level consistency

| Field | Value |
|-------|-------|
| Purpose | Confirm findings are not driven by one outlier donor |
| Input | Pseudotime values + donor IDs |
| Method | Pseudotime distributions per donor; leave-one-donor-out |
| Primary output | Per-donor pseudotime summary |
| Plots | Fig 7 (donor pseudotime boxplots) |
| Tables | Table S4: donor statistics |
| Code module | `src/trajectory.py` → `pseudotime_by_donor()` |
| Failure mode | One donor drives everything → investigate quality; report with caution |

### Experiment 8: Differential expression along progression

| Field | Value |
|-------|-------|
| Purpose | Identify individual genes with significant pseudotime trends |
| Input | Pseudotime-ordered cells |
| Method | Spearman correlation of each gene with pseudotime; BH FDR correction |
| Primary output | Table of significant trend genes |
| Plots | Heatmap of top trend genes |
| Tables | Table S3: top pseudotime trend genes |
| Code module | `src/stats.py` → `test_gene_trend()` |
| Failure mode | Very few significant genes → trajectory may lack molecular specificity |

### Experiment 9: Branching/fate analysis (secondary)

| Field | Value |
|-------|-------|
| Purpose | Test whether the trajectory bifurcates into repair vs death |
| Input | Pseudotime-ordered cells with diffusion map |
| Method | DPT branch detection; or Palantir fate probabilities |
| Primary output | Branch assignments; fate probability per cell |
| Plots | UMAP with branches colored; fate probability along pseudotime |
| Code module | `src/trajectory.py` |
| Failure mode | No clear branching → trajectory is linear (still informative) |

### Experiment 10: Robustness composite score

| Field | Value |
|-------|-------|
| Purpose | Summarize convergent evidence for robustness collapse |
| Input | Results of displacement, dispersion, and permutation tests |
| Method | Count significant criteria; classify as strong/moderate/weak/unsupported |
| Primary output | Composite score dict |
| Tables | Main Table 3: robustness evidence summary |
| Code module | `src/stats.py` → `robustness_composite_score()` |

---

## 6. Ablation and Sensitivity Specifications

### Ablation 1: AT2 cells only

| Field | Value |
|-------|-------|
| What changes | Remove AT1 and transitional cells; analyze AT2 only |
| Why it matters | Tests whether trajectory reflects within-cell-type injury, not AT1/AT2 composition |
| Compare | Median pseudotime diff, program ordering rank correlation, displacement effect size |
| Strengthens if | Trajectory and ordering preserved in AT2-only |
| Weakens if | Trajectory disappears → was driven by cell-type proportions |
| Output files | `results/intermediate/ablation_01_at2only.h5ad`, `results/tables/ablation_01_metrics.csv` |

### Ablation 2: PCA/UMAP vs diffusion-based embedding

| Field | Value |
|-------|-------|
| What changes | Replace diffusion map embedding with PCA-based UMAP for trajectory |
| Why it matters | Tests embedding-method dependence |
| Compare | Qualitative trajectory structure; program ordering |
| Strengthens if | Same broad structure under both methods |
| Weakens if | Trajectory only appears with one method |
| Output files | `results/intermediate/ablation_02_embedding.h5ad`, `results/tables/ablation_02_metrics.csv` |

### Ablation 3: With vs without batch correction

| Field | Value |
|-------|-------|
| What changes | Run full analysis without Harmony correction |
| Why it matters | Tests whether trajectory is biology or batch artifact |
| Compare | Core metrics with and without correction |
| Strengthens if | Trajectory present in both |
| Weakens if | Trajectory only appears with correction (possible artifact) or only without correction (correction too aggressive) |
| Output files | `results/intermediate/ablation_03_nobatch.h5ad`, `results/tables/ablation_03_metrics.csv` |

### Ablation 4: Remove apoptosis genes

| Field | Value |
|-------|-------|
| What changes | Exclude apoptosis program genes from HVG list before manifold construction |
| Why it matters | Tests whether trajectory is a death gradient or a multi-faceted process |
| Compare | Trajectory persistence; non-apoptotic program ordering |
| Strengthens if | Trajectory and non-apoptotic ordering preserved |
| Weakens if | Trajectory collapses → was just alive-to-dead |
| Output files | `results/intermediate/ablation_04_noapoptosis.h5ad`, `results/tables/ablation_04_metrics.csv` |

### Ablation 5: Root cell sensitivity

| Field | Value |
|-------|-------|
| What changes | Use 4 different root cells for pseudotime |
| Why it matters | Tests starting-point dependence |
| Compare | Program ordering across root choices |
| Strengthens if | Ordering preserved regardless of root (within healthy cells) |
| Weakens if | Ordering changes with root → trajectory structure is fragile |
| Output files | `results/tables/ablation_05_root_comparison.csv` |

### Ablation 6: Broader epithelial context

| Field | Value |
|-------|-------|
| What changes | Include airway epithelial cells (club, ciliated, basal) |
| Why it matters | Tests whether alveolar trajectory is specific or a generic epithelial response |
| Compare | Whether alveolar trajectory persists as distinct feature |
| Strengthens if | Alveolar trajectory visible as distinct branch |
| Weakens if | Trajectory subsumed into broader epithelial manifold |
| Output files | `results/intermediate/ablation_06_broaderepi.h5ad`, `results/tables/ablation_06_metrics.csv` |

### Ablation 7: Leave-one-donor-out

| Field | Value |
|-------|-------|
| What changes | Exclude one donor at a time; rerun trajectory |
| Why it matters | Tests donor-level robustness |
| Compare | Core metrics across all N-1 iterations |
| Strengthens if | All iterations give qualitatively same result |
| Weakens if | One donor drives the finding |
| Output files | `results/tables/ablation_07_lodo_summary.csv` |

### Ablation 8: Alternative gene program definitions

| Field | Value |
|-------|-------|
| What changes | Use MSigDB-only gene sets vs curated-only gene sets |
| Why it matters | Tests whether findings depend on specific gene set curation |
| Compare | Program ordering with alternative definitions |
| Strengthens if | Ordering preserved across gene set definitions |
| Weakens if | Ordering depends on specific gene choices |
| Output files | `results/tables/ablation_08_altprograms.csv` |

### Ablation 9: Alternative trajectory algorithm (Palantir)

| Field | Value |
|-------|-------|
| What changes | Replace DPT with Palantir for trajectory inference |
| Why it matters | Tests trajectory-method dependence |
| Compare | Pseudotime ordering; program dynamics |
| Strengthens if | Both methods produce consistent ordering |
| Weakens if | Methods disagree substantially |
| Output files | `results/intermediate/ablation_09_palantir.h5ad`, `results/tables/ablation_09_metrics.csv` |

### Ablation 10: Permutation and random controls

| Field | Value |
|-------|-------|
| What changes | Shuffle condition labels (1000×); score random gene sets (100×) |
| Why it matters | Establishes null distributions for all primary findings |
| Compare | Observed statistics vs null distributions |
| Strengthens if | Observed far exceeds null |
| Weakens if | Observed within null range → finding is noise |
| Output files | `results/tables/ablation_10_permutation.csv`, `results/tables/ablation_10_random_genesets.csv` |

---

## 7. Threat-to-Validity Assessment

### Internal validity threats

| Threat | Severity | Mitigation |
|--------|----------|------------|
| **Cross-sectional design** | Fundamental | Cannot prove temporal dynamics. All findings framed as "consistent with" staged process. Pseudotime is an ordering inference, not a time measurement. |
| **Donor confounding** | High | Batch correction (Harmony); leave-one-donor-out analysis; donor-stratified reporting |
| **Annotation error** | High | Marker gene validation before any analysis; re-annotation if needed |
| **Embedding artifacts** | Moderate | Compare UMAP vs diffusion maps; test UMAP seed stability; avoid quantitative analysis on UMAP coordinates |
| **Pseudotime root sensitivity** | Moderate | Test 4 different root cells; report whether ordering is stable |
| **Batch-correction artifacts** | Moderate | Compare with and without correction; avoid over-correction |
| **Ambient RNA contamination** | Moderate | Check for unexpected marker expression in wrong cell types; healthy cells scoring high on injury programs |
| **Apoptotic cell dropout** | Moderate | snRNA-seq captures nuclei from dead cells better than scRNA-seq; the most apoptotic cells may still be underrepresented |
| **Gene set arbitrariness** | Moderate | Test alternative gene set definitions; random gene set controls |
| **Multiple testing** | Low | BH FDR correction; Bonferroni for program-level tests; emphasis on effect sizes |

### External validity threats

| Threat | Severity | Note |
|--------|----------|------|
| **Single dataset** | High | All findings are specific to SCP1219 until replicated in independent cohorts |
| **Lethal COVID-19 only** | High | No mild/moderate cases for comparison; cannot determine if findings are specific to lethal disease or general to COVID |
| **Unknown disease duration** | Moderate | Time from infection to death varies; "pseudotime" within the tissue may not align with clinical timeline |
| **Post-mortem artifacts** | Low-Moderate | Tissue collected post-mortem; gene expression may not fully reflect ante-mortem biology |
| **Generalizability to other injuries** | Speculative | Claims about "robustness collapse" as a general principle require validation in other DAD contexts |

### What this study cannot claim
1. That individual cells traverse the inferred pseudotime trajectory
2. That the observed gene program ordering reflects real temporal dynamics
3. Causality between any molecular program and cell fate
4. That findings generalize beyond lethal COVID-19
5. Therapeutic targets or intervention points (without experimental validation)

### What this study can claim (paper_v3 revision)
1. That COVID-19 alveolar cells show dispersion-dominated loss of state coherence, not coherent centroid displacement
2. That within-group dispersion is the most portable cross-cohort signature of alveolar injury
3. That a donor-aware pseudotime shift exists and is amplified by batch correction
4. That a KRT8+/CLDN4+ transitional population is enriched in the primary atlas (but not portable under marker thresholds)
5. That identity-program decline with pseudotime is stable; fine injury-program ordering is hypothesis-generating
6. That these findings are robust to ablation, cross-method validation (Palantir), and independent replication

---

## 8. Paper v3 Extension Analyses

### 8.1 Donor-aware inference (Essential)
- Module: `src/donor_models.py`
- Analyses: donor_summary, donor_level_test, donor_bootstrap_ci, donor_dispersion_comparison, mixed_effects_pseudotime, pseudobulk_expression
- Status: Code implemented, not yet run on data

### 8.2 Portable state score (High value)
- Module: `src/state_score.py`
- Analyses: at2_identity_score, at1_identity_score, transitional_score, injury_composite_score, coherence_loss_score, repair_failure_score, benchmark_scores
- Status: Code implemented, not yet run

### 8.3 Mechanistic linkage (Medium value)
- Module: `src/mechanism.py`
- Analyses: program_geometry_linkage, repair_stall_analysis, local_heterogeneity, fan_out_contribution
- Status: Code implemented, not yet run

### 8.4 Cross-disease generalization (Ambitious / future)
- Module: `src/generalization.py`
- Plan: `docs/GENERALIZATION_PLAN.md`
- Status: Code scaffold implemented; external data not downloaded

### 8.5 Orthogonal validation (Future work)
- Plan: `docs/ORTHOGONAL_VALIDATION_PLAN.md`
- Status: Plan only; requires spatial, pathology, or RNA velocity data
