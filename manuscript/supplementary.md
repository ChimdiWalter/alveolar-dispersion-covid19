# Supplementary Materials

## Supplementary Note 1: Extended Methods for Ablation Analyses

Each ablation experiment modifies one component of the primary analysis pipeline and reruns the core workflow. The three metrics compared across all ablations are:

1. **Median pseudotime difference** (COVID median - Healthy median): measures the magnitude of condition-associated pseudotime shift
2. **Program ordering rank correlation**: Spearman correlation between the rank order of program peak positions in the ablation vs. the primary analysis
3. **Displacement effect size**: rank-biserial r from the Mann-Whitney U test of centroid distances

An ablation "passes" if all three metrics retain the same sign and qualitative interpretation as the primary analysis. Quantitative differences are expected and reported.

**Summary across ablations (primary MPD = +0.048, primary ρ = 1.0 self-correlation, primary r = +0.14):**

| Ablation | MPD | ρ | r | Passes MPD sign | Passes ρ | Passes r |
|---|---|---|---|---|---|---|
| 1 — AT2 only | +0.133 | 0.33 | −0.29 | ✓ | ✓ | ✗ (sign flip) |
| 2 — UMAP | +0.048 | 0.55 | +0.14 | ✓ | ✓ | ✓ |
| 2 — diffmap-augmented | +0.048 | 0.55 | +0.14 | ✓ | ✓ | ✓ |
| 3 — batch corrected* | +0.048 | 0.55 | +0.14 | ✓ | ✓ | ✓ |
| 3 — batch uncorrected* | +0.048 | 0.55 | +0.14 | ✓ | ✓ | ✓ |
| 4 — no apoptosis genes | +0.074 | 0.50 | +0.14 | ✓ | ✓ | ✓ |
| 5 — root healthy AT1 | −0.037 | 0.64 | +0.14 | ✗ | ✓ | ✓ |
| 5 — root random healthy | +0.010 | 0.55 | +0.14 | ✓ | ✓ | ✓ |
| 5 — root COVID extreme | −0.009 | −0.10 | +0.14 | ✗ | ✗ | ✓ |
| 5 — root healthy AT2 (primary) | +0.048 | 0.55 | +0.14 | ✓ | ✓ | ✓ |
| 6 — broader epithelial | −0.008 | 0.83 | +0.25 | ✗ | ✓ | ✓ |
| 7 — leave-one-donor-out (27 iter) | 0.028–0.202 | −0.17 to 0.74 | per-iter varies | ✓ (27/27) | mixed | ✓ |
| 8 — curated-only programs | +0.048 | 1.00 | +0.14 | ✓ | ✓ | ✓ |
| 8 — MSigDB-only programs | +0.048 | −0.80 | +0.14 | ✓ | ✗ (inverted) | ✓ |
| 9 — Palantir | n/a | n/a | n/a | `palantir_not_installed` | | |
| 10 — permutation null | n/a (p = 0.001) | — | — | (primary MPD not exceeded in 1,000 perms) | | |

*Ablation 3 cannot distinguish corrected from uncorrected because Harmony failed at runtime and the "corrected" branch fell back to uncorrected PCA; both branches are effectively identical computations.

See Table S6 for the raw `metrics.json` aggregate.

## Supplementary Note 2: Gene Program Curation Rationale

Gene programs were curated from two sources: (1) established MSigDB Hallmark gene sets and (2) published lung biology literature. For each program, we selected genes with documented functional roles in the relevant process, prioritizing genes with well-characterized expression in alveolar epithelial cells.

**AT2 identity genes** were selected based on their consistent identification as AT2 markers across multiple lung atlases (Travaglini et al., 2020; Sikkema et al., 2023).

**AT1 identity genes** follow the same logic, with emphasis on genes that are specific to AT1 cells and not broadly expressed across epithelial types.

**Interferon response genes** are canonical interferon-stimulated genes (ISGs) consistently upregulated in type I and type II interferon signaling, drawn from the MSigDB Hallmark Interferon Alpha Response and Interferon Gamma Response gene sets.

**NF-kB inflammatory genes** include core NF-kB pathway components and well-established transcriptional targets, drawn from the MSigDB Hallmark TNF-alpha Signaling via NF-kB gene set.

**Oxidative stress genes** are key effectors and regulators of the cellular response to reactive oxygen species, including antioxidant enzymes (SOD1/2, GPX1/4, CAT) and the NRF2 pathway.

**AT2-to-AT1 differentiation genes** include the transitional markers KRT8, CLDN4, and SFN identified by Kobayashi et al. (2020) and Strunz et al. (2020), plus terminal AT1 markers that increase during successful differentiation.

**Apoptosis genes** are core pro-apoptotic effectors from the intrinsic and extrinsic pathways, supplemented with genes from the MSigDB Hallmark Apoptosis set.

**Senescence genes** are drawn from the SenMayo gene set (Saul et al., 2022) and include canonical senescence markers (CDKN1A/p21, CDKN2A/p16), SASP components, and senescence-associated secretory phenotype genes.

Full gene lists with sources are provided in Table S1.

## Supplementary Figures

See FIGURE_PLAN.md for specifications of Figures S1–S11.

## Supplementary Tables

See TABLE_PLAN.md for specifications of Tables S1–S8.

## Data Availability

The Columbia/NYP COVID-19 Lung Atlas is available through the Broad Institute Single Cell Portal under accession SCP1219.

## Code Availability

All analysis code is available at [repository URL]. The analysis pipeline is implemented in Python and can be executed from the project repository following the instructions in RUNBOOK.md.
