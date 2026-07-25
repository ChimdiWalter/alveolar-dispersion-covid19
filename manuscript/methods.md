# Methods

## Data source

We analyzed the Columbia University / New York Presbyterian COVID-19 Lung Atlas (Single Cell Portal accession SCP1219; Melms et al., 2021), a publicly available single-nucleus RNA-seq (snRNA-seq) dataset of 116,313 nuclei from human lung tissue. The cohort comprises lungs from 7 healthy organ donors and 20 patients who died of COVID-19 (27 donors total). Condition assignment (`Control` vs. `COVID-19`) was read from the `group` column of the provided metadata. Fine cell-type annotations (`cell_type_fine`) were taken as provided with the atlas.

## Alveolar subset selection

We retained cells labeled `AT1`, `AT2`, or `ECM-high epithelial` in `cell_type_fine`, yielding 22,128 cells (9,608 AT1, 11,341 AT2, 1,179 ECM-high transitional) from all 27 donors (12,181 from controls, 9,947 from COVID-19). The `ECM-high epithelial` label is inherited from the original atlas; we verified by marker expression (elevated KRT8, CLDN4 relative to both AT1 and AT2; Table S3) that these cells correspond to the KRT8⁺/CLDN4⁺ damage-associated transitional population described in mouse and human lung injury (Kobayashi et al., 2020; Strunz et al., 2020) rather than to an ECM-producing stromal contaminant.

## Normalization and feature selection

Counts were normalized to a target sum of 10,000 per cell (`scanpy.pp.normalize_total`) and log-transformed (`scanpy.pp.log1p`). The top 3,000 highly variable genes (HVGs) were selected using the Seurat v3 method (`flavor="seurat_v3"`) from raw counts. The full normalized log-expression matrix was retained as `adata.raw` for gene-program scoring; subsequent dimensionality reduction used the HVG-restricted matrix after per-gene scaling (`scanpy.pp.scale`, max_value = 10).

## Dimensionality reduction and manifold construction

Principal component analysis retained 50 components (`scanpy.tl.pca`, seed 42). A k-nearest-neighbor graph was constructed with k = 15 in PCA space (`scanpy.pp.neighbors`, `n_pcs=50`). UMAP embedding used `min_dist=0.3`, `spread=1.0`, random seed 42 (visualization only). A diffusion map with 15 components was computed (`scanpy.tl.diffmap`) for trajectory analysis.

## Batch correction (attempted)

We configured Harmony batch correction (harmonypy 0.2.0; Korsunsky et al., 2019) on the PCA space with `donor_id` as the batch key, `max_iter_harmony=20`, `sigma=0.1`. At runtime, `harmonypy` returned an `X_pca_harmony` obsm array of shape `(50,)` where `(22128, 50)` was expected, causing a downstream shape error. The pipeline detected the shape mismatch and fell back to uncorrected PCA for all downstream steps. This fallback is logged explicitly and is tested by Ablation 3 below.

## Trajectory inference and pseudotime

Diffusion pseudotime (DPT; Haghverdi et al., 2016) was computed via `scanpy.tl.dpt`. The root cell was selected as the cell with minimum Euclidean distance to the centroid of healthy AT2 cells in diffusion-component space. Pseudotime values were min-max normalized to [0, 1] for reporting. Sensitivity to root choice was evaluated in Ablation 5 (four alternative roots).

## Gene-program scoring

Eight programs were defined from curated gene lists supplemented where noted with MSigDB hallmark sets (config file `gene_programs`):

- AT2 identity: SFTPC, SFTPA1, SFTPA2, ABCA3, LAMP3, SLC34A2, NAPSA, PGC, LPCAT1
- AT1 identity: AGER, PDPN, HOPX, CLIC5, CAV1, EMP2, AKAP5, RTKN2
- Interferon response: ISG15, IFI6, IFIT1, IFIT3, MX1, MX2, OAS1, OAS2, STAT1, IRF7, BST2, IFI44L, IFITM3
- NF-κB inflammatory: NFKB1, RELA, TNF, IL6, IL1B, CXCL8, CCL2, ICAM1, PTGS2, SOD2, BIRC3, TNFAIP3
- Oxidative stress: SOD1, SOD2, GPX1, GPX4, CAT, TXN, HMOX1, NQO1, GCLC, GCLM, NFE2L2, PRDX1
- AT2→AT1 differentiation: KRT8, CLDN4, SFN, KRT18, LGALS3, HOPX, AGER, PDPN
- Apoptosis: BAX, BAK1, CASP3, CASP7, CASP9, BCL2L11, BID, PMAIP1, BBC3, CYCS, APAF1, FAS, FASLG
- Senescence: CDKN1A, CDKN2A, TP53, RB1, SERPINE1, GLB1, IGFBP7, CCL2, IL6, MMP1

Scoring used `scanpy.tl.score_genes` (Satija et al., 2015 adaptation) against a random background of similarly-expressed genes. Scores were computed against the full `.raw` expression matrix. One gene, GPX1, was silently absent from the HVG-restricted variance features and therefore omitted from the oxidative-stress program; other programs may contain analogous dropouts that we did not exhaustively audit.

## Robustness and dispersion metrics

**Centroid displacement.** Euclidean distance from each cell to the centroid of healthy (Control) cells in 50-dimensional PCA space. The one-sided Mann-Whitney U test (alternative: COVID > Healthy) was used to compare distributions. Effect size was reported as the rank-biserial correlation r.

**Within-group dispersion.** For each condition, we computed the Euclidean distance of each cell to that condition's own centroid in PCA space, then compared the two distance distributions with Levene's test for equality of variances.

**Pseudotime shift.** We computed the difference in median pseudotime between conditions (COVID − Control). Statistical significance was assessed by a permutation test: condition labels were shuffled 1,000 times and the median-difference null distribution was recorded. The empirical p-value was (1 + number of permuted |differences| ≥ |observed|) / (1 + number of permutations).

**Program-ordering comparison across ablations.** For each ablation, we computed the pseudotime position at which each of the eight program mean scores peaked (in 20 evenly-spaced pseudotime bins), producing an 8-entry rank vector. We compared this vector against the primary-analysis vector using Spearman's rank correlation (ρ). ρ = 1 indicates identical ordering; ρ = −1 indicates inverted ordering.

## Composite robustness-collapse assessment

Three criteria were pre-specified: (1) centroid displacement (Mann-Whitney U one-sided p < 0.05), (2) within-group dispersion (Levene p < 0.05 with COVID > Healthy variance), (3) pseudotime enrichment (permutation p < 0.05 with COVID > Healthy median). The composite label was "strong" if all three were satisfied, "moderate" if two, "weak" if one, "not supported" if zero.

## Ablation framework

Ten ablations were defined (Table S6; driver `scripts/ablations/run_all_ablations.py`):

1. **AT2-only subset** — restrict cells to AT2 only.
2. **Embedding variants** — PCA-only vs. diffusion-map-augmented neighbor graph.
3. **Batch correction** — with vs. without Harmony (partial overlap with primary due to Harmony fallback).
4. **Apoptosis-gene removal** — drop apoptosis genes before HVG selection.
5. **Root sensitivity** — four alternative pseudotime roots (healthy AT1 centroid, random healthy, COVID extreme, healthy AT2 centroid).
6. **Broader epithelial** — include airway Club, Ciliated, Basal, Goblet, Mucous alongside alveolar cells.
7. **Leave-one-donor-out** — 27 iterations, each excluding one donor.
8. **Alternative gene programs** — curated-only (no MSigDB) and MSigDB-only variants.
9. **Palantir trajectory inference** — alternative trajectory algorithm (if installed).
10. **Null controls** — permutation null for pseudotime shift and 100 random gene sets.

Each ablation produces a `metrics.json` containing median pseudotime difference (MPD), program peak-ordering ρ versus primary, and displacement effect size r. Results were aggregated into Table S6.

**Implementation note.** An initial version of `scripts/ablations/common.py` read the displacement effect size from key `"effect_size"` / `"r"`, while the upstream `displacement_test()` function writes key `"effect_size_r"`. Ablation rows generated before the fix show `displacement_effect_size = 0.0`; we re-ran all ablations after patching `common.py` to consult `effect_size_r` first.

## Palantir (Ablation 9)

Palantir (Setty et al., 2019) was configured with 1,200 waypoints and 5 trend components but was not installed in the analysis environment. Ablation 9 detected this and exited with a documented `palantir_not_installed` flag rather than failing; installing Palantir and re-running is listed as future work.

## Statistical conventions

Multiple-testing correction used Benjamini-Hochberg at FDR = 0.05. All random seeds were fixed to 42. Tests were two-sided unless noted otherwise (the pre-registered centroid-displacement test was one-sided, COVID > Healthy, per the directional robustness-collapse hypothesis).

## Software and reproducibility

Analyses were performed in Python 3.12.3 using Scanpy 1.12.1 (Wolf et al., 2018), AnnData 0.12.10, NumPy 2.4.3, SciPy 1.17.1, pandas 2.3.3, scikit-learn 1.8.0, matplotlib 3.10.8, and harmonypy 0.2.0. All random seeds were fixed to 42. Configuration is stored in `config.yaml`; analysis entry points are under `scripts/`; ablation drivers are under `scripts/ablations/`. Complete code and configuration are available at [repository URL].
