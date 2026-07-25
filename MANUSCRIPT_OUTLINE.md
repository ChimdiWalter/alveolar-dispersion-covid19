# Manuscript Outline

## Epithelial Robustness Collapse in Lethal COVID-19: Trajectory Analysis of Alveolar Cell-State Failure in the Columbia/NYP Lung Atlas

---

## Title page

**Title:** Epithelial Robustness Collapse in Lethal COVID-19: Trajectory Analysis of Alveolar Cell-State Failure in the Columbia/NYP Lung Atlas

**Short title:** Alveolar Robustness Collapse in Lethal COVID-19

**Authors:** [Names and affiliations]

**Corresponding author:** [Name, email]

**Keywords:** alveolar epithelium, COVID-19, single-nucleus RNA-seq, pseudotime, trajectory inference, robustness, AT2 cells, diffuse alveolar damage

---

## Abstract (250 words max)

**Structure:** Background → Gap → Approach → Key Results → Significance

**Scaffold:**
The alveolar epithelium sustains gas exchange through the coordinated function of AT1 and AT2 cells, with AT2 cells serving as progenitors for injury repair. In lethal COVID-19, these cells face concurrent viral assault and inflammatory damage, but whether their failure proceeds as a binary event or a staged process remains unclear.

[GAP] Standard comparisons between healthy and diseased states obscure the continuous nature of cell-state change and cannot resolve the order of molecular events during alveolar collapse.

[APPROACH] We analyzed [N] alveolar epithelial cells from the Columbia/NYP COVID-19 Lung Atlas (SCP1219) using manifold construction, diffusion pseudotime, and gene program scoring to reconstruct the transcriptomic trajectory of epithelial failure. We defined robustness collapse through five convergent criteria and validated findings through ten systematic ablation analyses.

[RESULTS] COVID-19 alveolar cells were significantly displaced from and more dispersed than healthy cells on the transcriptomic manifold [effect sizes]. Pseudotime analysis revealed an ordered progression: [interferon → inflammation → repair attempt → apoptosis]. We identified a transitional population expressing KRT8/CLDN4 markers consistent with stalled AT2-to-AT1 differentiation, enriched in COVID-19 tissue. Core findings were robust across [N/10] ablations including cell-type restriction, embedding method changes, batch correction, and donor exclusion.

[SIGNIFICANCE] These results support a model of staged epithelial robustness collapse under extreme perturbation, providing a quantitative framework for understanding alveolar failure applicable beyond COVID-19 to other forms of acute lung injury.

---

## Introduction

### Paragraph 1: The alveolar epithelium and its importance
The alveolar epithelium is the functional unit of gas exchange. AT1 cells form the exchange surface; AT2 cells produce surfactant and serve as the alveolar progenitor. The AT2-to-AT1 differentiation axis is the primary repair mechanism.

### Paragraph 2: COVID-19 as an extreme perturbation
SARS-CoV-2 enters AT2 cells via ACE2. The paradox: the cells needed for repair are themselves targets. Diffuse alveolar damage, inflammatory cascades, and the accumulation of transitional epithelial cells in COVID-19 lungs.

### Paragraph 3: Limitations of standard analytical approaches
Clustering and differential expression between conditions provide averages but cannot capture the continuous, ordered nature of cell-state change. This approach misses trajectories, branching, intermediate states, and the progression from recoverable injury to irreversible failure.

### Paragraph 4: The case for trajectory and manifold analysis
Treating each cell as a position in a continuous landscape allows us to reconstruct the topology of failure. Pseudotime provides an ordering that, while not proof of temporal dynamics, tests whether the molecular evidence is consistent with a staged process.

### Paragraph 5: Study overview and aims
We analyze [N] alveolar epithelial cells from SCP1219 to (1) characterize the failure manifold, (2) reconstruct the trajectory and score gene programs along it, and (3) validate through ablation. We frame this as "robustness collapse" — connecting epithelial failure to systems-biology concepts of robustness under perturbation.

---

## Results

### Result 1: Alveolar epithelial cells from healthy and COVID-19 lungs occupy distinct regions of the transcriptomic manifold
- Manifold construction (Fig 1)
- COVID cells displaced from healthy (Fig 1a, quantified in Table 2)
- Internal structure within COVID: gradient, not island

### Result 2: COVID-19 cells are statistically displaced from homeostasis with increased dispersion
- Centroid distance analysis (Table 2)
- Levene's test for dispersion
- AT1 vs AT2 displacement comparison

### Result 3: Diffusion pseudotime reveals an ordered trajectory from homeostasis to failure
- Trajectory structure (Fig 2)
- Pseudotime density by condition (Fig 4)
- Permutation test confirms condition-pseudotime association (Table S7)

### Result 4: Gene programs activate in a staged, biologically coherent order
- Program trends along pseudotime (Fig 3)
- Ordering: interferon → NF-kB → differentiation → apoptosis
- Marker gene validation (Fig 5)

### Result 5: Transitional cells with stalled AT2-to-AT1 differentiation markers are enriched in COVID-19
- KRT8+/CLDN4+ cells at intermediate pseudotime
- Co-expression patterns
- Enrichment in COVID vs healthy

### Result 6: The failure trajectory is consistent across donors
- Donor-level pseudotime distributions (Fig 7)
- Leave-one-donor-out results

### Result 7: Core findings are robust across analytical perturbations
- Ablation summary (Fig 6)
- Program ordering preserved across cell-type subsets, embedding methods, batch correction, root cells
- Specific fragilities, if any, reported transparently

---

## Discussion

### Paragraph 1: Summary of principal findings
Restate the core finding: alveolar epithelial cells in lethal COVID-19 distribute across a continuous transcriptomic landscape consistent with staged robustness collapse.

### Paragraph 2: Biological interpretation — the staged failure model
Connect the ordered program activation to known lung injury biology. Interferon response as first defense. NF-kB as inflammatory amplification. Repair initiation (AT2-to-AT1 differentiation) as the lung's attempt to restore the epithelium. Apoptosis as the terminal outcome when repair cannot be completed.

### Paragraph 3: Transitional cells and the failure of repair
The KRT8+/CLDN4+ transitional population represents a potentially clinically significant state — cells that initiated repair but stalled. Connect to the DATP/aberrant basaloid literature. These cells may represent a window where intervention could theoretically rescue repair.

### Paragraph 4: Robustness as a framework for understanding tissue failure
Connect to systems-biology concepts. The alveolar epithelium has evolved robustness to minor perturbation (the AT2 progenitor system). COVID-19 overwhelms this robustness. The trajectory we reconstruct maps the collapse of robustness from a systems perspective.

### Paragraph 5: Relationship to published COVID-19 lung atlas studies
Compare our findings to Melms et al. (2021) and other SCP1219 analyses. What does the trajectory perspective add that cell-type composition analysis did not reveal?

### Paragraph 6: Limitations
- Cross-sectional data: pseudotime ≠ real time
- Single dataset: requires replication
- Post-mortem tissue: may not perfectly reflect ante-mortem biology
- No mild/moderate cases: cannot define the point of no return
- Apoptosis vs stress ambiguity: terminal state may be composite
- Computational inference: ablation stability is encouraging but not proof

### Paragraph 7: Future directions
- Validation in independent COVID-19 lung cohorts (Delorey et al., Wendisch et al.)
- Application of the robustness-collapse framework to other forms of DAD (bacterial pneumonia, VILI)
- Spatial transcriptomics to add anatomical context to the trajectory
- RNA velocity as orthogonal directionality evidence
- Experimental follow-up: can transitional cells be pushed toward repair completion in organoid systems?

### Paragraph 8: Conclusion
One paragraph synthesis. What this study contributes to the field. Conservative, appropriate framing.

---

## Methods

### Data source and access
SCP1219. Download method. snRNA-seq protocol (as described by original authors).

### Quality control
Thresholds. Rationale. Software versions.

### Normalization and feature selection
Total-count normalization, log1p. N HVGs. Flavor.

### Cell-type annotation and validation
Original annotations used with marker validation. Re-annotation criteria if applied.

### Batch correction
Harmony on PCA space. Batch key. Verification of correction.

### Dimensionality reduction
PCA (N components). UMAP (parameters). Diffusion map (N components). Neighbor graph (k).

### Trajectory inference
DPT. Root cell selection (healthy AT2 centroid). Branching.

### Gene program scoring
8 programs. score_genes method. Gene lists (Table S1). Control gene matching.

### Robustness metrics
Centroid distance. Dispersion (Levene's). NN mixing. Pseudotime density.

### Statistical tests
Mann-Whitney U (displacement). Levene's (dispersion). Permutation test (pseudotime enrichment). Spearman (gene trends). BH FDR correction.

### Ablation analyses
Description of all 10 ablations. Metrics compared.

### Software
Python version. Package versions. Reproducibility statement.

---

## Supplementary Materials

- Table S1–S8 (see TABLE_PLAN.md)
- Figure S1–S11 (see FIGURE_PLAN.md)
- Supplementary Note 1: Extended methods for ablation analyses
- Supplementary Note 2: Gene program curation rationale
- Data availability: SCP1219 accession
- Code availability: GitHub repository link
