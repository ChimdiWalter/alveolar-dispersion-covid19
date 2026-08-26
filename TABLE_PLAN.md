# Table Plan

## Epithelial Robustness Collapse in Lethal COVID-19

---

## Main Tables

### Table 1: Dataset and cohort summary
**Contents:** Donors per condition, cells per condition, cells per cell type, cells per donor, clinical metadata available.
**Source:** Metadata inspection after data loading.
**Code:** `src/io.py` → `load_metadata()`; custom summary in notebook.
**Output:** `results/tables/table1_cohort_summary.csv`

### Table 2: Robustness metrics summary
**Contents:** Centroid distance (healthy vs COVID means, Mann-Whitney U, p-value, effect size r), dispersion (Levene's test), NN mixing scores, pseudotime enrichment (permutation p-value). Reported for all alveolar, AT1-only, and AT2-only.
**Source:** Experiment 5 outputs.
**Code:** `src/stats.py`
**Output:** `results/tables/table2_robustness_metrics.csv`

### Table 3: Robustness collapse evidence summary
**Contents:** Five convergent criteria, whether each is met, the associated p-value/effect size, and the overall assessment (strong/moderate/weak).
**Source:** `src/stats.py` → `robustness_composite_score()`
**Code:** Custom assembly in notebook.
**Output:** `results/tables/table3_composite_evidence.csv`

---

## Supplementary Tables

### Table S1: Gene program definitions
**Contents:** Program name, genes in program, source/reference, number of genes found in dataset.
**Source:** `config.yaml` gene_programs section.
**Output:** `results/tables/tableS1_gene_programs.csv`

### Table S2: QC metrics and filtering thresholds
**Contents:** Thresholds applied, cells before/after filtering, per-condition breakdown.
**Source:** `src/qc.py` → `qc_summary()`
**Output:** `results/tables/tableS2_qc_summary.csv`

### Table S3: Marker gene validation matrix
**Contents:** Mean expression and percent expressing for each canonical marker in each annotated cell type.
**Source:** `src/annotation.py` → `validate_markers()`
**Output:** `results/tables/tableS3_marker_validation.csv`

### Table S4: Top pseudotime-trending genes
**Contents:** Gene, Spearman rho, p-value (raw and FDR-adjusted), direction.
**Source:** `src/stats.py` → `test_gene_trend()` applied to all genes.
**Output:** `results/tables/tableS4_pseudotime_trends.csv`

### Table S5: Donor-level statistics
**Contents:** Donor ID, condition, n_cells, mean/median pseudotime, displacement from centroid.
**Source:** `src/trajectory.py` → `pseudotime_by_donor()`
**Output:** `results/tables/tableS5_donor_statistics.csv`

### Table S6: Ablation outcome summary
**Contents:** Ablation name, core metric (primary analysis), core metric (ablation), qualitative assessment (consistent/inconsistent), interpretation.
**Source:** Ablation experiments in notebook.
**Output:** `results/tables/tableS6_ablation_summary.csv`
**Known limitation (2026-08-25):** the `displacement_effect_size` column is currently constant (r=0.1407) across ablations 02/03/05/08/09 by construction, not by finding — `centroid_distance()` defaults to `rep_key="X_pca"` and is never passed each ablation's actual embedding. Will change once ANALYSIS_PLAN.md §9 Follow-up 2 / RUNBOOK.md Step 14 is run.

### Table S7: Permutation test details
**Contents:** Observed median pseudotime difference, null mean, null std, p-value, number of permutations.
**Source:** `src/stats.py` → `permutation_test_pseudotime()`
**Output:** `results/tables/tableS7_permutation.csv`

### Table S8: Program peak pseudotime positions
**Contents:** Program name, pseudotime bin of peak score, mean peak score, onset pseudotime (when score first exceeds baseline + 1 SD).
**Source:** `src/programs.py` → `program_trends_along_pseudotime()`
**Output:** `results/tables/tableS8_program_peaks.csv`

### Table S9: Replication under an expanded gene panel (2026-08-25)
**Contents:** Dispersion (Levene statistic/p-value/variance ratio), donor-level direction test, and DATP marker-threshold enrichment recomputed on an expanded/full-transcriptome replication cohort, reported side-by-side against the current 84-gene-panel values (Levene p≈10⁻¹³⁷, variance ratio 1.65, donor-level p=0.002, DATP fold enrichment 0.48×) so portability under panel expansion is directly readable.
**Source:** ANALYSIS_PLAN.md §9 Follow-up 1; RUNBOOK.md Step 13.
**Code:** `scripts/replication/fetch_replication.py` (expanded `gene_shortlist`), `scripts/replication/analyze_replication.py`
**Output:** `results/tables/tableS9_replication_expanded_panel.csv`
