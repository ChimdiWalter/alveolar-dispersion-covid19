# Paper v3 — Abstract Options

## Version 1: Specialized computational biology journal
(Target: Genome Biology, Bioinformatics, NAR Genomics)

The alveolar epithelium repairs itself through AT2-to-AT1 differentiation, a process overwhelmed in lethal COVID-19. Whether injury disrupts alveolar cell states through coherent displacement toward a single damaged phenotype or through heterogeneous dispersion across multiple injury states has not been tested at single-cell resolution with systematic robustness validation.

We analyzed 22,128 alveolar epithelial cells (AT1, AT2, and KRT8+/CLDN4+ transitional) from the Columbia/NYP COVID-19 Lung Atlas (SCP1219; 7 healthy donors, 20 COVID-19 donors). After constructing a transcriptomic manifold and computing diffusion pseudotime rooted in healthy AT2 identity, we tested three pre-registered geometric criteria: centroid displacement, within-group dispersion, and pseudotime enrichment. We evaluated robustness through ten ablation analyses, an orthogonal trajectory algorithm (Palantir), Harmony donor-aware batch correction, and independent replication on 89,736 alveolar cells from 618 donors across 35 datasets.

Centroid displacement was not supported (one-sided Mann-Whitney p = 1.0). Within-group dispersion was strongly supported (variance ratio 2.3; Levene p < 10^-30) and replicated cross-cohort (variance ratio 1.65; p ~ 10^-137). COVID-19 cells were enriched at higher pseudotime (median difference +0.048; permutation p = 0.001), a signal preserved in all 27 leave-one-donor-out iterations, amplified 2.6-fold by Harmony batch correction, and confirmed by Palantir (shift +0.028, same direction). Donor-level pseudobulk analysis replicated the direction in the independent cohort (p = 0.002, 43 vs 575 donors). A KRT8+/CLDN4+ transitional population was enriched 3.1-fold in COVID-19 in the primary atlas but did not transfer cross-cohort under marker-threshold definitions. Fine-grained injury-program ordering was sensitive to gene-list choice and is reported as hypothesis-generating.

These results support a dispersion-dominated model of alveolar epithelial injury in which lethal COVID-19 fans cells outward across heterogeneous injury states rather than displacing them coherently. Dispersion and donor-level trajectory direction are the most portable signatures; threshold-based transitional-state calls and fine program ordering are atlas-specific. We recommend dispersion and trajectory-based metrics over centroid displacement for detecting epithelial state-coherence loss.

---

## Version 2: Broader-interest journal
(Target: Nature Communications, Cell Reports, eLife)

The lung's gas-exchange surface is maintained by AT2 progenitor cells that differentiate into AT1 cells after injury. In lethal COVID-19, this regenerative system faces simultaneous viral assault and inflammatory damage, but whether the resulting epithelial failure takes the form of a coherent shift toward one damaged state or a heterogeneous dispersion across many injury states has not been resolved.

We tested these competing models using 22,128 alveolar epithelial cells from the Columbia/NYP COVID-19 Lung Atlas (7 healthy donors, 20 COVID-19 donors), with ten systematic ablation analyses and independent replication across 618 donors from 35 datasets. COVID-19 alveolar cells were not coherently displaced from the healthy centroid (Mann-Whitney p = 1.0), but showed markedly increased within-group dispersion (2.3-fold variance ratio; Levene p < 10^-30), a signature that replicated strongly cross-cohort. COVID-19 cells were also shifted toward higher injury-associated pseudotime, a signal amplified by donor-aware batch correction and confirmed by an orthogonal trajectory algorithm. A KRT8+/CLDN4+ transitional population accumulated in the primary atlas but did not transfer as a portable threshold-based signature.

These findings establish dispersion-dominated loss of epithelial state coherence, rather than coherent displacement, as the primary geometric signature of alveolar injury in lethal COVID-19. The dispersion signal is the most robust and portable finding, surviving ablation, cross-method validation, and independent replication, while centroid displacement, fine program ordering, and marker-threshold transitional-state definitions are fragile or atlas-specific.

---

## Version 3: Most defensible final version
(Chosen for paper_v3)

The alveolar epithelium repairs itself through AT2-to-AT1 differentiation, but this process is overwhelmed in lethal COVID-19. Two geometric models could describe the resulting injury: coherent displacement of cells toward a single damaged state, or heterogeneous dispersion across multiple injury states. We tested these models using 22,128 alveolar epithelial cells from the Columbia/NYP COVID-19 Lung Atlas (SCP1219; 7 healthy donors, 20 COVID-19 donors), scoring eight gene programs along diffusion pseudotime and evaluating robustness through ten pre-specified ablation analyses, Harmony batch correction, an orthogonal trajectory algorithm (Palantir), and independent replication on 89,736 cells from 618 donors across 35 datasets.

Coherent centroid displacement was not supported (one-sided Mann-Whitney p = 1.0; rank-biserial r = 0.14 opposite to the hypothesized direction). Within-group dispersion was strongly supported (variance ratio 2.3; Levene p < 10^-30) and replicated decisively cross-cohort (variance ratio 1.65; p ~ 10^-137). COVID-19 cells were enriched at higher pseudotime (permutation p = 0.001; median difference +0.048 on a [0,1] axis), a signal preserved in 27/27 leave-one-donor-out iterations, amplified 2.6-fold under Harmony batch correction, confirmed at reduced magnitude by Palantir (+0.028), and replicated at the donor-pseudobulk level in the independent cohort (p = 0.002). A KRT8+/CLDN4+ transitional population was enriched 3.1-fold in the primary atlas but did not transfer cross-cohort under marker-threshold definitions. The fine-grained ordering of injury programs along pseudotime was sensitive to gene-list composition and is treated as hypothesis-generating.

These results support a model in which lethal COVID-19 produces dispersion-dominated loss of alveolar epithelial state coherence rather than a coherent directional shift. The geometric signatures — within-group dispersion and donor-level trajectory direction — are the most portable findings across cohorts and methods, while annotation-dependent and threshold-based measures are atlas-specific.

---

## Final choice

**Version 3** is the final abstract for paper_v3.

**Rationale:**
- Tightest structure: problem → competing models → approach → results → interpretation
- Leads with the negative result (centroid failure) to immediately distinguish models
- Reports exact statistics for all key findings
- Clearly labels fragile findings as fragile
- Does not overclaim transitional-state portability
- Distinguishes portable from atlas-specific findings in the final sentence
- A skeptical reviewer can assess the entire paper's claim structure from this abstract alone
