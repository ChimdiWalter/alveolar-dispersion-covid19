# Project Plan Summary: Alveolar Epithelial Robustness Under Lethal COVID-19

---

## Title

*Mapping the Loss of Alveolar Epithelial Robustness in Lethal COVID-19: A Transcriptomic Trajectory Analysis of Cell-State Exhaustion and Failed Repair*

---

## Project Overview

This project uses the Columbia/NYP COVID-19 Lung Atlas (SCP1219) --- a single-nucleus RNA-seq dataset of 116,313 human lung cells from healthy donors and patients who died of COVID-19 --- to investigate how alveolar epithelial cells progressively lose their identity and function under extreme viral injury. Rather than simply comparing "healthy" vs. "COVID" cells, we construct a continuous transcriptomic landscape and trace plausible paths from homeostasis through stress, failed repair, and apoptosis.

---

## Central Hypothesis

Alveolar epithelial cells in lethal COVID-19 distribute across a continuous landscape reflecting progressive loss of homeostatic identity, activation and failure of repair programs, and convergence toward apoptosis --- a process we term *epithelial robustness collapse*.

**Supporting sub-hypotheses:**
1. Healthy alveolar cells occupy a compact region of the transcriptomic manifold; COVID cells are dispersed away from it along injury-associated axes.
2. Pseudotime rooted in healthy cells reveals an ordered progression: interferon response, inflammatory stress, attempted repair, then apoptosis.
3. AT1 and AT2 cells may follow partially distinct failure trajectories, with AT2 cells showing evidence of stalled differentiation toward AT1 fate.

---

## Three Specific Aims

**Aim 1 --- Characterize the alveolar epithelial landscape.**
Subset AT1, AT2, and transitional cells. Build a low-dimensional manifold via PCA/UMAP/diffusion maps. Quantify whether COVID cells are displaced from and more dispersed than healthy cells.

**Aim 2 --- Reconstruct the failure trajectory and score gene programs.**
Apply pseudotime inference (diffusion pseudotime or Palantir) rooted in healthy cells. Score each cell for interferon, inflammation, oxidative stress, AT2-to-AT1 differentiation, and apoptosis programs. Determine whether these programs activate in a biologically coherent order.

**Aim 3 --- Validate through ablation and sensitivity analyses.**
Systematically vary analytical choices (cell-type subsets, embedding methods, batch correction, gene sets, root cells, donor inclusion) to test whether biological conclusions are robust or fragile.

---

## Dataset and Study Design

| Feature | Detail |
|---------|--------|
| Dataset | SCP1219 --- Columbia/NYP COVID-19 Lung Atlas |
| Assay | Single-nucleus RNA-seq |
| Total cells | 116,313 |
| Healthy controls | 36,677 cells |
| Lethal COVID-19 | 79,636 cells |
| Focus population | ~20,000+ alveolar epithelial cells (AT1, AT2, transitional) |
| Study type | Cross-sectional with pseudo-dynamic inference |

Healthy cells serve as the reference anchor defining normal alveolar identity. COVID cells are examined relative to this anchor. Evidence for robustness collapse requires convergence of: (1) displacement from homeostasis, (2) increased dispersion, (3) loss of identity markers, (4) ordered program activation, and (5) stalled differentiation.

---

## Analysis Pipeline (Summary)

1. **QC** --- Filter low-quality nuclei by gene counts, total RNA, and mitochondrial fraction
2. **Normalization** --- Scale counts and log-transform
3. **Feature selection** --- Identify 2,000--3,000 highly variable genes
4. **Cell-type subsetting** --- Extract AT1, AT2, transitional cells; validate with canonical markers
5. **Batch correction** --- Assess and correct donor/batch effects (Harmony or scVI) if needed
6. **Dimensionality reduction** --- PCA (30--50 components), UMAP, diffusion maps
7. **Trajectory inference** --- Diffusion pseudotime or Palantir, rooted in healthy AT2 cells
8. **Gene program scoring** --- Score cells for 8 curated programs (AT1/AT2 identity, interferon, NF-kB, oxidative stress, AT2-to-AT1 differentiation, apoptosis, senescence)
9. **Robustness metrics** --- Centroid distance, dispersion, condition mixing, pseudotime density

---

## Seven Main Experiments

| # | Experiment | Key Question |
|---|-----------|-------------|
| 1 | Alveolar population identification | Are AT1/AT2/transitional cells cleanly identifiable? |
| 2 | Manifold construction and condition comparison | Do COVID cells spread away from the healthy region? |
| 3 | Pseudotime trajectory reconstruction | Is there a continuous path from homeostasis to apoptosis? |
| 4 | Gene program scoring along pseudotime | Do stress, repair, and apoptosis programs activate in order? |
| 5 | Homeostatic displacement quantification | Are COVID cells statistically farther from and more dispersed than healthy cells? |
| 6 | Transitional/failed-repair state identification | Do stalled AT2-to-AT1 cells exist in the COVID group? |
| 7 | Donor-level consistency | Are findings consistent across all donors? |

---

## Seven Ablation and Sensitivity Analyses

| # | Ablation | Tests Whether... |
|---|---------|-----------------|
| 1 | AT2 only vs. AT1+AT2 | Trajectory reflects within-cell-type injury, not AT1/AT2 differences |
| 2 | PCA/UMAP vs. diffusion maps | Results are independent of embedding method |
| 3 | With vs. without batch correction | Findings reflect biology, not batch artifacts |
| 4 | With vs. without apoptosis genes | Trajectory captures multi-faceted failure, not just a death gradient |
| 5 | Different pseudotime root cells | Ordering is robust to starting-point choice |
| 6 | Alveolar only vs. broader epithelium | Alveolar trajectory is specific, not a general epithelial signal |
| 7 | Leave-one-donor-out | No single donor drives the results |

---

## Controls and Validation

- **Biological:** Marker gene validation for all cell types; benchmarking against known AT2-to-AT1 differentiation biology; sanity checks on program scores
- **Analytical:** Permutation tests for pseudotime-condition association; random gene set controls; UMAP stability across random seeds; comparison to published findings on the same dataset

---

## Expected Results

- Healthy alveolar cells form a compact, coherent cluster
- COVID cells disperse outward along stress/injury/apoptosis axes
- Pseudotime reveals an ordered cascade: interferon, then inflammation, then repair attempt, then apoptosis
- Transitional cells (stalled AT2-to-AT1 differentiation) are enriched in COVID
- Core findings survive most ablations

---

## Key Pitfalls and Mitigations

| Pitfall | Mitigation |
|---------|-----------|
| Noisy cell-type annotations | Validate with markers; re-annotate if needed |
| Donor effects dominating manifold | Batch correction + leave-one-donor-out |
| Weak trajectory signal | Check graph connectivity; fall back to cluster-based analysis |
| Over-interpretation of pseudotime | Frame as "consistent with," not proof; cross-reference known biology |
| Apoptosis vs. general stress overlap | Multiple gene sets; acknowledge if inseparable |
| Cross-sectional limitation | Explicit language throughout; no causal claims |

---

## Suggested Figures

1. **UMAP manifold** colored by condition and cell type
2. **Pseudotime trajectory** overlaid on manifold
3. **Gene program dynamics** along pseudotime (multi-panel heatmap/ribbon)
4. **Pseudotime density** --- healthy vs. COVID distributions
5. **Key marker genes** along pseudotime (*SFTPC*, *AGER*, *KRT8*, *ISG15*, *CASP3*)
6. **Ablation summary panel** --- core finding across all ablations
7. **Donor-level consistency** --- pseudotime distributions per donor

---

## Timeline (6 Weeks)

| Week | Focus |
|------|-------|
| 1 | Data download, QC, normalization, annotation validation |
| 2 | Alveolar subsetting, batch correction, manifold construction |
| 3 | Trajectory inference, gene program scoring, robustness metrics |
| 4 | Ablation and sensitivity analyses, permutation controls |
| 5 | Figure generation, results and methods writing |
| 6 | Report completion, presentation prep, notebook cleanup |

---

## Deliverables

- Final written report (15--25 pages)
- 5--7 publication-quality figures
- Supplementary tables (gene programs, QC metrics, DE genes, donor statistics)
- Documented analysis notebook/pipeline (Python, runnable from `lesegenv`)
- Oral presentation (15--20 minutes)

---

## One-Paragraph Summary

This project uses single-nucleus RNA-seq data from the Columbia/NYP COVID-19 Lung Atlas to investigate how alveolar epithelial cells lose their functional identity and robustness under lethal SARS-CoV-2 infection. We construct a continuous transcriptomic landscape of alveolar cell states and use trajectory inference to ask whether cells move through an ordered progression from homeostasis through interferon activation, inflammatory stress, attempted but failed repair, and ultimately apoptosis. Gene program scoring along this trajectory reconstructs the molecular sequence of alveolar failure, while systematic ablation analyses test whether the biological conclusions are robust. The result is a rigorous, biology-centered map of how the alveolar epithelial system collapses under extreme perturbation.

---

*Summarized from the full project plan. See `project_plan.md` for complete details.*
