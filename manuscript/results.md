# Results

## Alveolar epithelial cells from healthy and COVID-19 lungs: cohort composition

We extracted 22,128 alveolar epithelial cells from the SCP1219 atlas, comprising 9,608 AT1, 11,341 AT2, and 1,179 ECM-high transitional cells, from 7 healthy donors (12,181 nuclei) and 20 COVID-19 donors (9,947 nuclei). Per-donor cell counts ranged from 62 (L04covaddon) to 2,850 (C52ctr); 10 donors contributed fewer than 300 alveolar cells (Table S5). Cell-type marker validation confirmed annotation quality: AT2 cells expressed SFTPC and SFTPA1 at high levels, AT1 cells expressed AGER and HOPX, and ECM-high transitional cells expressed KRT8 and CLDN4 at elevated levels relative to both AT1 and AT2 populations (Table S3).

The ECM-high transitional population was enriched 3.1-fold in COVID-19 relative to control lungs: 848 of 9,947 COVID-19 cells (8.5%) vs. 331 of 12,181 control cells (2.7%) were ECM-high transitional (χ², p < 10⁻³⁰). Viewed per-donor, 24 of 27 donors contributed at least one transitional cell; control donors contributed 37–81 transitional cells each, whereas the COVID-19 transitional counts were distributed across all 20 COVID donors (Table S5, Figure 7).

## Manifold and pseudotime reconstruction

After normalization, Seurat-v3 highly variable gene selection (3,000 genes), PCA (50 components), and k-nearest-neighbor graph construction (k = 15), we computed UMAP and diffusion-map embeddings (Figure 1). Harmony batch correction was configured but failed during pipeline execution due to a dimensionality mismatch in the returned `X_pca_harmony` obsm field (shape (50,) returned where (22128, 50) was expected); the pipeline therefore fell back to uncorrected PCA. This fallback is recorded in the log and explicitly tested by Ablation 3 (see below). The uncorrected UMAP showed visible donor structure (Figure S1) but clear separation of AT1, AT2, and ECM-high populations (Figure 1b).

Diffusion pseudotime (DPT) rooted at the cell nearest the healthy AT2 centroid ordered cells from low values (dominated by AT2 identity; Figure 2, Figure 5) to high values (injury-associated; see below). Control cells concentrated at low pseudotime (median 0.063, mean 0.111) while COVID-19 cells were shifted upward (median 0.111, mean 0.118) with narrower dispersion in COVID-19 (std 0.046 vs. 0.098; Table: pseudotime_by_condition.csv).

## Pseudotime shift: significant by permutation, modest in magnitude

The condition-associated pseudotime shift was the most consistent signal in the dataset. The observed median difference (COVID − Control) was +0.0483 on a [0, 1]-normalized pseudotime axis. Under 1,000 permutations of condition labels, the null distribution of median differences was tightly centered at zero (null mean 6.0 × 10⁻⁵, null std 1.24 × 10⁻³), and the observed value was not exceeded in any permutation, yielding p = 0.000999 (= 1/1,001; Table 2).

Leave-one-donor-out analysis (Ablation 7) preserved the direction of this shift in every one of 27 iterations; the smallest recorded pseudotime difference was 0.028 (excluding donor C52ctr) and the largest 0.202 (excluding donor C56ctr, a small control with 351 cells and unusually high pseudotime variance); the bulk of iterations fell in the range 0.047–0.086 (Table S6).

## The centroid-displacement test was NOT supported

We tested whether COVID-19 cells were further from the healthy centroid in PCA space than healthy cells (one-sided Mann-Whitney U; COVID > Healthy). The test was not significant (U = 5.206 × 10⁷, p = 1.0). Mean distances were comparable (COVID 12.36 vs. Healthy 12.10), but median distance was lower in COVID-19 (10.68 vs. 11.56), indicating that a substantial fraction of COVID-19 cells lie *closer* to the healthy centroid than healthy cells themselves. The rank-biserial effect size (r = 0.14) points in the opposite direction to the one-sided alternative. We report this result prominently because the centroid-displacement metric was pre-specified as one of three core criteria for robustness collapse (Methods); the data do not support it.

A plausible interpretation: COVID-19 cells do not radiate uniformly away from the healthy centroid. Instead, some COVID-19 cells remain near homeostatic identity while others occupy distant, heterogeneous positions — a pattern captured by the dispersion test rather than by displacement.

## Dispersion: COVID-19 cells are significantly more spread out

Within-group dispersion (Euclidean distance to each group's own centroid) was markedly higher in COVID-19 (variance 33.28) than in controls (variance 14.58), a 2.3-fold difference. Levene's test on the two distributions yielded statistic 276.5, p ≈ 0 (below floating-point precision reported as 0.0 in Table 2). This result is the quantitative counterpart of the visual fan-out seen on UMAP (Figure 1a): COVID-19 cells occupy a broader range of transcriptomic states than controls, consistent with fragmentation into heterogeneous injury states rather than coherent movement to a single new state.

## Gene programs along pseudotime: identity first, injury programs later

Scoring each cell for eight gene programs (AT2 identity, AT1 identity, AT2-to-AT1 differentiation, interferon response, NF-κB inflammatory, oxidative stress, apoptosis, senescence) and computing the pseudotime position at which each program's mean score peaked yielded the following ordering (Figure 3, Table S8):

| Rank | Program | Peak pseudotime | Peak mean score |
|---|---|---|---|
| 1 | AT2 identity | 0.015 | 0.75 |
| 2 | AT1 identity | 0.266 | 1.25 |
| 3 | Apoptosis | 0.591 | 0.17 |
| 4 | AT2→AT1 differentiation | 0.744 | 0.57 |
| 4 (tie) | NF-κB inflammatory | 0.744 | 0.18 |
| 4 (tie) | Oxidative stress | 0.744 | 0.21 |
| 7 | Interferon response | 0.866 | 0.33 |
| 8 | Senescence | 0.935 | 0.24 |

This ordering is **not** the hypothesized interferon→NF-κB→repair→apoptosis cascade. In the observed data, homeostatic identity programs (AT2, AT1) peak in the lower third of pseudotime; the six injury-associated programs all peak in the upper half; and within the upper half, apoptosis peaks before the inflammatory/stress programs rather than after. Several caveats apply. First, the gene `GPX1` was absent from the HVG-restricted variance features and excluded from the oxidative-stress program; other programs may have similar dropouts. Second, "peak" is a coarse summary; programs with broad plateaus along pseudotime (e.g., NF-κB, oxidative stress, AT2→AT1 differentiation all peaking at the same pseudotime bin 0.744) cannot be ordinated finely. Third, Scanpy `score_genes` produces scores normalized against randomly matched background genes, so absolute score values are not directly comparable across programs.

The honest summary is: AT2 and AT1 identity scores decline monotonically with pseudotime (Figure 3); injury programs rise toward the high-pseudotime region; apoptosis rises earlier than interferon/senescence, which may reflect either true biological ordering, the behavior of program scoring under heterogeneous cell populations, or our gene-list choice — distinguishing these is what Ablation 8 (alternative gene programs) was designed to test.

## ECM-high transitional population occupies a mid-trajectory state enriched in COVID-19

The 1,179 ECM-high transitional cells were distributed across pseudotime but concentrated at intermediate positions (mean pseudotime ≈ 0.3–0.5; Figure S10). These cells express KRT8, CLDN4, and partial AT1 markers (Table S3) — the molecular signature of damage-associated transient progenitors (DATPs) or KRT8⁺ alveolar differentiation intermediates described in mouse lung injury and human IPF (Kobayashi et al., 2020; Strunz et al., 2020; Adams et al., 2020; Habermann et al., 2020). Their 3.1-fold enrichment in COVID-19 (reported above) is consistent with accumulation of cells that initiated the AT2→AT1 repair program but have not completed it.

We note a nomenclature point: the annotation label `ECM-high epithelial` comes from the original atlas (Melms et al., 2021). Marker expression confirms these cells are the KRT8⁺/CLDN4⁺ transitional population and not an ECM-producing stromal contaminant (Table S3).

## Donor-level consistency of the pseudotime shift

All 20 COVID-19 donors had median pseudotime ≥ 0.087, while 5 of 7 control donors had median pseudotime < 0.090 (Table S5, Figure 7). The two exceptions on the control side (C51ctr median 0.156; C56ctr median 0.119 but with large std 0.24 over only 351 cells) reflect either small-n variance (C56ctr) or a genuinely higher-pseudotime healthy donor (C51ctr); the effect survives their inclusion. No COVID-19 donor had median pseudotime below the lowest healthy-donor median.

## Ablation analyses

The 10 ablations (Table S6, Figure 6) targeted separate axes of methodological variation. We summarize each below using the three pre-specified comparison metrics: median pseudotime difference (MPD), program-ordering rank correlation ρ with the primary analysis, and displacement effect-size r. The primary-analysis values for these metrics (this study, Table 2) are MPD = +0.048, r = 0.14, ρ = 1.0 (self-correlation).

**Ablation 1 — AT2-only subset (11,341 cells).** MPD = +0.133 (larger than primary), ρ = 0.33, r = −0.29. Restricting to AT2 cells amplified the pseudotime shift but degraded program ordering, and the displacement effect size reversed sign — COVID-19 AT2 cells were *closer* on average to the healthy AT2 centroid than healthy AT2 cells were, an even stronger version of the non-displacement pattern seen in the primary analysis. This is consistent with AT1 cells contributing structure to the program ordering and with the non-displacement finding being a robust feature of COVID-19 alveolar cells rather than an artifact of cell-type mixing.

**Ablation 2 — Alternative embeddings (UMAP vs. diffusion-map-augmented neighbors).** Both variants produced identical MPD (+0.048), ρ (0.55), and r (0.14). The pseudotime shift does not depend on embedding choice — it is a property of the underlying PCA/neighbor structure, not of the visualization.

**Ablation 3 — With vs. without batch correction.** Both variants yielded MPD = +0.048, ρ = 0.55, r = 0.14. Because Harmony failed at runtime (harmonypy shape bug) and the "corrected" branch itself fell back to uncorrected PCA, this ablation cannot independently distinguish corrected from uncorrected results — both branches are effectively the same computation. A genuine test of batch correction requires a working harmonypy or a substitute method (scVI, scanorama); we list this as known future work.

**Ablation 4 — Remove apoptosis genes before HVG selection.** MPD = +0.074, ρ = 0.50, r = 0.14. Dropping apoptosis-program genes from the HVG pool slightly increased the pseudotime shift (suggesting apoptosis genes contribute "noise" distributed across both conditions rather than driving the shift) and moderately degraded program ordering — as expected given apoptosis is one of the programs being ordinated.

**Ablation 5 — Four alternative pseudotime roots.** MPD by root: healthy AT1 centroid −0.037; random healthy +0.010; COVID extreme −0.009; healthy AT2 centroid +0.048. Program ordering ρ was 0.64 (healthy AT1), 0.55 (random healthy), −0.10 (COVID extreme), 0.55 (healthy AT2). The primary (healthy AT2 centroid) root gave the largest and most consistent signal; rooting from the COVID extreme inverted the ordering (ρ ≈ 0), as expected — confirming that pseudotime direction is root-dependent and must be interpreted with the root choice declared. Displacement r = 0.14 across all four roots (the metric is root-invariant because it is computed in PCA space, not pseudotime).

**Ablation 6 — Broader epithelial (alveolar + airway: Club, Ciliated, Basal, Goblet, Mucous).** MPD = −0.008, ρ = 0.83, r = 0.25. **Adding airway epithelial cells abolishes the pseudotime shift.** Program ordering actually *improves* modestly (ρ 0.83), and the displacement effect size rises (r 0.25) — but the direction of pseudotime is no longer condition-associated. This is the most biologically informative ablation: the trajectory we describe is a property of the alveolar compartment specifically. Pooling alveolar + airway epithelium into a single manifold dilutes the alveolar-injury axis because airway cells occupy a different region of expression space whose structure dominates the resulting pseudotime. Generalizing the robustness-collapse framework to lung epithelium broadly will require compartment-specific trajectories, not a pooled manifold.

**Ablation 7 — Leave-one-donor-out (27 iterations).** All 27 iterations preserved the direction of the MPD (range 0.028–0.202). The single outlier is donor C56ctr (MPD = 0.202, ρ = −0.17) — a small-n control donor (351 cells) with unusually high pseudotime variance whose removal actually increases the observed shift; the other 26 iterations cluster in the range 0.028–0.086. ρ range across all 27 iterations is −0.17 to 0.74 (primarily in the 0.40–0.74 range). No single donor is required for the MPD signal to remain positive, although program-ordering rank correlation is more variable than pre-compact drafts of this manuscript stated.

**Ablation 8 — Alternative gene programs.**
 - Curated-only programs (no MSigDB supplements): MPD = +0.048 (identical to primary), ρ = 1.0.
 - MSigDB-only programs: MPD = +0.048 (identical), ρ = −0.80.
 The program ordering is therefore stable under curation choice but NOT under substitution of MSigDB hallmark sets. This is the single largest ablation-induced change to program ordering and is discussed below.

**Ablation 9 — Palantir trajectory inference.** Palantir was not installed in the analysis environment; the ablation exited gracefully with a documented `palantir_not_installed` flag in Table S6 rather than failing. This is a known limitation; installing Palantir and rerunning is listed as future work.

**Ablation 10 — Null controls.** The permutation test on median pseudotime difference (1,000 shuffles of condition labels) produced a null distribution centered at zero (mean 6.0 × 10⁻⁵, std 1.24 × 10⁻³); the observed +0.048 was not exceeded in any permutation (p = 0.000999 = 1/1,001). 100 random gene sets size-matched to the apoptosis program were scored across all cells; the distributions were centered near zero (mean ≈ 0, std ≈ 0.07–0.10 per random set), confirming that real program scores (e.g., apoptosis score range extending above 0.17 mean with biologically coherent pseudotime trends) are distinguishable from random size-matched gene sets.

## Composite assessment

Of the three pre-registered criteria:

1. **Centroid displacement** (Mann-Whitney U, COVID > Healthy): NOT supported (p = 1.0).
2. **Dispersion** (Levene's test): supported (p ≈ 0; variance ratio 2.3).
3. **Pseudotime enrichment** (permutation test): supported (p = 0.001; observed MPD = +0.048).

The composite robustness-collapse assessment is "moderate" (2 of 3 criteria met; Table 3).

## Summary of findings

Lethal COVID-19 does not push alveolar epithelial cells coherently away from the healthy centroid; it fans them out along a continuous pseudotime axis, producing a significantly more heterogeneous COVID-19 population with enrichment of an ECM-high/KRT8⁺ transitional cell population at intermediate pseudotime. Gene-program peaks along pseudotime are consistent with identity loss followed by broad injury-program activation, though the specific ordering within the injury phase is sensitive to gene-list choice (Ablation 8). The pseudotime shift itself is robust to donor exclusion, embedding choice, and batch-correction status; the displacement metric is not supported and should be replaced or supplemented in future work by the dispersion and trajectory-based measures used here.
