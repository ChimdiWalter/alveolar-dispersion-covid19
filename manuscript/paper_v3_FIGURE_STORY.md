# Paper v3 — Figure Story

## Narrative logic

The figure sequence tells a story of model discrimination:
1. Set up the competing models (displacement vs fan-out)
2. Show the manifold
3. Present the strongest evidence (dispersion)
4. Show the trajectory shift with donor awareness
5. Show the transitional compartment (supportive, not headline)
6. Demonstrate robustness
7. Demonstrate replication

Each figure should be readable independently — a reviewer skimming figures should understand the entire paper.

---

## Main Figures

### Figure 1: Conceptual schematic — two competing models of epithelial injury
**Biological claim:** Injury could produce either coherent displacement (all cells shift together toward a single damaged state) or heterogeneous fan-out (cells scatter across multiple injury states). These predict different geometric signatures that are empirically distinguishable.

**Panels:**
- (a) Schematic: healthy compact cluster → coherent displacement model (shifted cluster, same shape)
- (b) Schematic: healthy compact cluster → fan-out/dispersion model (expanded cloud, same center, broader tail)
- (c) Predicted outcomes table: displacement test (positive vs null), dispersion test (null vs positive), pseudotime enrichment (positive vs positive)

**Statistical annotation:** None (conceptual figure)

**Message:** The paper explicitly tests these two models. The data will distinguish them.

**Placement:** Main text, first figure.

---

### Figure 2: The alveolar epithelial manifold
**Biological claim:** Alveolar epithelial cells from healthy and COVID-19 lungs occupy a shared transcriptomic landscape, but COVID-19 cells visibly occupy a broader region.

**Panels:**
- (a) UMAP colored by condition (Healthy blue, COVID-19 red)
- (b) UMAP colored by fine cell type (AT1, AT2, ECM-high transitional)
- (c) UMAP colored by donor (shows batch structure)
- (d) UMAP after Harmony correction colored by condition (shows that integration does not eliminate the spread)

**Statistical annotation:** n per condition and cell type in panel labels.

**Message:** COVID-19 cells are not shifted as a block — they fan out. Harmony correction does not remove this pattern.

**Placement:** Main text.

---

### Figure 3: Dispersion — the centerpiece
**Biological claim:** COVID-19 alveolar cells show markedly greater within-group dispersion in transcriptomic space than healthy cells. This is the strongest and most replicable finding.

**Panels:**
- (a) Violin/box plot: Euclidean distance to own-group centroid in PCA space, by condition. Annotated with Levene's statistic, p-value, and variance ratio.
- (b) Box plot: distance to healthy centroid, by condition. Annotated with Mann-Whitney U, p = 1.0 (displacement fails). COVID median LOWER than healthy median — annotate this.
- (c) Donor-level dispersion: per-donor median distance to group centroid, colored by condition. Each dot = one donor.
- (d) Replication dispersion: same metric in the independent cohort (89,736 cells, 618 donors). Variance ratio 1.65, Levene p ~ 10^-137.

**Statistical annotation:**
- Panel a: Levene stat = 276.5, p < 10^-30, variance ratio 2.3
- Panel b: MW U p = 1.0, rank-biserial r = 0.14 (opposite direction)
- Panel c: donor-level comparison
- Panel d: replication Levene p ~ 10^-137

**Message:** Dispersion, not displacement. This is the primary result and it replicates.

**Placement:** Main text, centerpiece figure.

---

### Figure 4: Donor-aware pseudotime shift
**Biological claim:** COVID-19 cells are enriched at higher pseudotime positions along an injury-associated axis, and this shift is a donor-level property preserved under batch correction.

**Panels:**
- (a) Pseudotime density by condition (overlapping histograms)
- (b) Per-donor median pseudotime, bar chart colored by condition
- (c) Pseudotime shift under Harmony correction (+0.125, 2.6x amplification)
- (d) Donor-level pseudotime in the replication cohort (injury composite median by donor, 43 COVID vs 575 control donors, MW p = 0.002)

**Statistical annotation:**
- Panel a: permutation p = 0.001, MPD = +0.048
- Panel b: donor-level visualization
- Panel c: Harmony MPD = +0.125
- Panel d: donor-level replication p = 0.002

**Message:** The trajectory shift is modest but robust: all 27 LODO iterations preserve direction, Harmony amplifies it, and donor-level replication confirms it.

**Placement:** Main text.

---

### Figure 5: Transitional compartment enrichment
**Biological claim:** A KRT8+/CLDN4+ transitional population accumulates in COVID-19 alveolar epithelium, consistent with stalled AT2-to-AT1 repair. This is a primary-atlas observation, not a portable threshold-based signature.

**Panels:**
- (a) UMAP highlighting ECM-high/transitional cells by condition
- (b) Stacked bar: fraction of ECM-high in each condition (8.5% vs 2.7%)
- (c) Marker expression: KRT8, CLDN4, SFTPC, AGER across cell types (dotplot or violin)
- (d) Pseudotime distribution of transitional cells vs AT1 and AT2

**Statistical annotation:**
- Panel b: 3.1-fold enrichment, chi-squared p < 10^-30
- Panel d: transitional cells concentrated at intermediate pseudotime

**Message:** Transitional cells accumulate in COVID-19, consistent with repair failure. But this finding is atlas-annotation-dependent and does not transfer cross-cohort under simple marker thresholds.

**Placement:** Main text.

---

### Figure 6: Ablation robustness matrix
**Biological claim:** The pseudotime shift is robust across all tested perturbations; dispersion is always supported; fine program ordering is fragile.

**Panels:**
- (a) Heatmap or forest plot: MPD across all 10 ablations + primary
- (b) Program-ordering rank correlation (rho) across ablations
- (c) Displacement effect size (r) across ablations — shows it never supports displacement
- (d) Leave-one-donor-out MPD range (all 27 positive)

**Statistical annotation:**
- Each cell annotated with metric value
- Green/red coloring for pass/fail
- Key fragilities highlighted: MSigDB inversion (rho = -0.80), broader epithelial (MPD collapses)

**Message:** The pseudotime shift and dispersion are robust; fine program ordering and specific transitional markers are method- or gene-list-sensitive.

**Placement:** Main text.

---

### Figure 7: Replication summary
**Biological claim:** Geometric signatures (dispersion, donor-level direction) are portable across 35 independent datasets. Annotation-dependent signatures (DATP thresholds, fine program ordering) are not.

**Panels:**
- (a) Replication dispersion: violin of injury composite by condition, 89,736 cells
- (b) Donor-level replication: box plot of donor-level injury composite medians, 43 COVID vs 575 control
- (c) Per-program cell-level replication: heatmap of p-values (IFN and AT1 replicate; NF-kB, apoptosis, etc. do not)
- (d) Portability summary matrix: rows = findings, columns = [primary, replication, portable?]

**Statistical annotation:**
- Panel a: Levene p ~ 10^-137, variance ratio 1.65
- Panel b: donor-level MW p = 0.002
- Panel c: per-program p-values
- Panel d: yes/no portability for each finding

**Message:** The right question is not "does everything replicate?" but "which findings are geometric (and portable) versus annotation-dependent (and atlas-specific)?"

**Placement:** Main text.

---

## Supplementary Figures

### Figure S1: QC metric distributions
Pre/post filtering n_genes, total_counts, pct_mito.

### Figure S2: Marker gene validation dotplot
Canonical markers across annotated cell types.

### Figure S3: Batch effect assessment
UMAP by donor before and after Harmony.

### Figure S4: PCA variance explained
Scree plot.

### Figure S5: Diffusion map embedding
DC1-DC3 colored by condition and pseudotime.

### Figure S6: Gene program dynamics along pseudotime
8-program score trajectories (20 bins). This was main Figure 3 in v2; in v3 it moves to supplement because fine ordering is fragile.

### Figure S7: Marker gene expression along pseudotime
SFTPC, AGER, KRT8, ISG15, CASP3, BAX individual trends.

### Figure S8: Permutation null distribution
Null histogram with observed value marked.

### Figure S9: Random gene set controls
Random gene-set scores vs real program scores.

### Figure S10: UMAP random-seed stability
Multiple UMAP seeds showing consistent structure.

### Figure S11: Leave-one-donor-out detail
Per-donor ablation metrics.

### Figure S12: Palantir pseudotime comparison
Palantir vs DPT pseudotime colored on UMAP; MPD comparison.

### Figure S13: Transitional cell characterization
KRT8 vs SFTPC and KRT8 vs AGER co-expression at intermediate pseudotime.

---

## Key changes from v2 figure plan

| Change | Rationale |
|--------|-----------|
| New Figure 1 (conceptual schematic) | Sets up model discrimination explicitly |
| Dispersion promoted to Figure 3 (centerpiece) | Strongest finding first |
| Gene program dynamics moved to supplement | Fine ordering is fragile |
| Harmony-corrected UMAP added to Figure 2 | Shows batch correction does not remove fan-out |
| Donor-level panels added throughout | Donor is the correct inferential unit |
| Replication given its own figure (Fig 7) | Cross-cohort evidence is major |
| Portability matrix added | Makes the portable-vs-fragile distinction visual |
