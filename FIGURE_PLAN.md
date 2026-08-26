# Figure Plan

## Dispersion, Not Displacement: Loss of Alveolar Epithelial State Coherence in Lethal COVID-19

**Paper v3 revision: 2026-04-30**

See also: `manuscript/paper_v3_FIGURE_STORY.md` for the full narrative logic.

---

## Main Figures (paper_v3 order)

### Figure 1: Conceptual schematic — two competing models of epithelial injury
**Panels:** (a) Coherent displacement model: healthy cluster → shifted cluster. (b) Dispersion/fan-out model: healthy cluster → expanded cloud. (c) Predicted outcomes table for displacement vs dispersion tests.
**Caption concept:** Two geometric models of epithelial injury make distinct, testable predictions. Under coherent displacement, all cells shift toward one damaged state. Under dispersion, cells fan outward into heterogeneous injury states. These models predict opposite outcomes for centroid-displacement and variance tests.
**Code module:** Manual illustration (Illustrator / Inkscape)
**Output:** `results/figures/fig1_schematic.pdf`

### Figure 2: The alveolar epithelial manifold
**Panels:** (a) UMAP colored by condition (Healthy blue, COVID-19 red). (b) UMAP colored by cell type (AT1, AT2, Transitional). (c) UMAP colored by donor. (d) UMAP after Harmony correction colored by condition.
**Caption concept:** COVID-19 cells visibly occupy a broader region of the manifold than healthy cells. Harmony correction reduces donor structure but preserves the spread pattern.
**Code module:** `src/plots.py` → `plot_umap_condition()`, `plot_umap_celltype()`
**Output:** `results/figures/fig2_manifold.pdf`

### Figure 3: Dispersion — the centerpiece
**Panels:** (a) Violin/box: distance to own-group centroid by condition (Levene's test). (b) Box: distance to healthy centroid by condition (MW p=1.0, displacement fails). (c) Donor-level: per-donor median dispersion by condition. (d) Replication: dispersion in independent cohort (89,736 cells, Levene p~10^-137).
**Caption concept:** COVID-19 alveolar cells show markedly increased within-group dispersion (2.3-fold variance ratio), while centroid displacement fails. Dispersion replicates cross-cohort (1.65-fold). This is the primary and most portable finding.
**Statistical annotation:** Levene stat, p-value, variance ratio; MW U p=1.0 for displacement.
**Code module:** `src/plots.py` (new function needed)
**Output:** `results/figures/fig3_dispersion.pdf`

### Figure 4: Donor-aware pseudotime shift
**Panels:** (a) Pseudotime density by condition. (b) Per-donor median pseudotime bars. (c) Pseudotime shift under Harmony (MPD +0.125). (d) Donor-level replication (MW p=0.002).
**Caption concept:** COVID-19 cells are enriched at higher pseudotime. The shift is preserved in all 27 LODO iterations, amplified 2.6x by Harmony, and replicates at the donor-pseudobulk level.
**Code module:** `src/plots.py` → `plot_pseudotime_density()`, `plot_donor_pseudotime()`
**Output:** `results/figures/fig4_donor_pseudotime.pdf`

### Figure 5: Transitional compartment enrichment
**Panels:** (a) UMAP highlighting transitional cells. (b) Stacked bar: fraction by condition. (c) Marker violin: KRT8, CLDN4, SFTPC, AGER. (d) Pseudotime distribution of transitional cells.
**Caption concept:** A KRT8+/CLDN4+ transitional population accumulates in COVID-19 (3.1-fold), consistent with stalled repair. This is a primary-atlas observation; marker-threshold portability fails cross-cohort.
**Code module:** `src/plots.py`
**Output:** `results/figures/fig5_transitional.pdf`

### Figure 6: Ablation robustness matrix
**Panels:** (a) Heatmap: MPD across ablations. (b) Program-ordering rho. (c) Displacement r (never significant). (d) LODO range.
**Caption concept:** The pseudotime shift and dispersion are robust across all perturbations that preserve the alveolar compartment. Fine program ordering is sensitive to gene-list choice.
**Code module:** Custom notebook function
**Output:** `results/figures/fig6_ablation.pdf`
**Known limitation (2026-08-25):** panel (c)'s displacement-r column is currently constant by construction across ablations 02/03/05/08/09 (see Table S6's matching note) — not yet an informative robustness result. Becomes meaningful after ANALYSIS_PLAN.md §9 Follow-up 2 / RUNBOOK.md Step 14.

### Figure 7: Replication summary
**Panels:** (a) Replication dispersion violin. (b) Donor-level injury composite. (c) Per-program replication heatmap. (d) Portability matrix: rows=findings, columns=[primary, replication, portable?].
**Caption concept:** Geometric signatures (dispersion, donor-level direction) are portable; annotation-dependent signatures (DATP threshold, specific program peaks) are not.
**Code module:** Custom notebook function
**Output:** `results/figures/fig7_replication.pdf`
**Planned extension (2026-08-25):** once ANALYSIS_PLAN.md §9 Follow-up 1 / RUNBOOK.md Step 13 (expanded-panel replication, Table S9) runs, panel (d)'s portability matrix should distinguish "replicated under 84-gene panel" from "replicated under expanded/full-transcriptome panel" — the current single-column matrix can't make that distinction.

---

## Supplementary Figures

### Figure S1: QC metric distributions
Pre- and post-filtering distributions of n_genes, total_counts, pct_mito.
**Output:** `results/figures/figS1_qc.pdf`

### Figure S2: Marker gene validation dotplot
Dotplot of canonical markers across annotated cell types.
**Output:** `results/figures/figS2_markers.pdf`

### Figure S3: Batch effect assessment
UMAP colored by donor/batch before and after Harmony correction.
**Output:** `results/figures/figS3_batch.pdf`

### Figure S4: PCA variance explained
Scree plot and cumulative variance explained.
**Output:** `results/figures/figS4_pca.pdf`

### Figure S5: Diffusion map embedding
Diffusion components 1-3 colored by condition and pseudotime.
**Output:** `results/figures/figS5_diffmap.pdf`

### Figure S6: Permutation test null distribution
Histogram of null pseudotime differences (1000 permutations) with observed value marked.
**Output:** `results/figures/figS6_permutation.pdf`

### Figure S7: Random gene set control comparison
Distribution of random gene-set pseudotime correlations vs real program correlations.
**Output:** `results/figures/figS7_random_controls.pdf`

### Figure S8: UMAP stability across random seeds
Multiple UMAP embeddings with different random seeds showing consistent large-scale structure.
**Output:** `results/figures/figS8_umap_stability.pdf`

### Figure S9: Leave-one-donor-out ablation details
Per-donor ablation showing trajectory metrics with each donor excluded.
**Output:** `results/figures/figS9_lodo.pdf`

### Figure S10: Transitional cell characterization
Co-expression plots of KRT8 vs SFTPC and KRT8 vs AGER in intermediate-pseudotime cells.
**Output:** `results/figures/figS10_transitional.pdf`

### Figure S11: Robustness composite evidence summary
Visual summary of the 3 pre-registered criteria and model-discrimination outcome.
**Output:** `results/figures/figS11_composite.pdf`

### Figure S12: Palantir pseudotime comparison
Palantir vs DPT pseudotime on UMAP; MPD comparison; program ordering rho.
**Output:** `results/figures/figS12_palantir.pdf`

### Figure S13: Transitional cell characterization
KRT8 vs SFTPC and KRT8 vs AGER co-expression at intermediate pseudotime.
**Output:** `results/figures/figS13_transitional_detail.pdf`

---

## Key changes from v2 figure plan

| Change | Rationale |
|--------|-----------|
| New Figure 1 (conceptual schematic) | Sets up model discrimination before showing any data |
| Dispersion promoted to Figure 3 (centerpiece) | Strongest and most portable finding |
| Gene program dynamics moved to Figure S6 | Fine ordering is fragile; identity-first pattern is described in text |
| Donor-level panels added to Figures 3, 4, 7 | Donor is the correct inferential unit |
| Harmony comparison added to Figures 2d and 4c | Batch correction strengthens signal |
| Replication gets its own main figure (Fig 7) | Cross-cohort evidence is a major pillar |
| Portability matrix added to Figure 7d | Visual summary of what replicates and what does not |
