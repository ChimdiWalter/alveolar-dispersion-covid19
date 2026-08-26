# Orthogonal Validation Plan

> **Status (as of 2026-08-25):** All planned orthogonal validation analyses below
> (spatial transcriptomics, pathology linkage, RNA velocity, histology) remain
> **not started** — no relevant data exists in the repo. One exception: ablation 9
> (Palantir, an alternative trajectory algorithm) is complete
> (`results/ablations/09_palantir/metrics.csv`/`.json` have real computed values)
> and is orthogonal-validation-*adjacent*, but it belongs to the ablations suite —
> a different, already-completed robustness check — not to O1–O4 below, which
> remain entirely unimplemented.

## Goal
Strengthen the manuscript with validation axes beyond the primary snRNA-seq trajectory analysis.

---

## Current status
No spatial transcriptomics, histology, or pathology data are currently in the repository. All orthogonal validation analyses below are planned, not implemented.

## Validation axes

### O1: Spatial localization of transitional states
**Question:** Do KRT8+/CLDN4+ transitional cells localize to regions of active alveolar damage?

**Required data:**
- Spatial transcriptomics (Visium, MERFISH, or similar) of COVID-19 lung sections
- Ideally from the same cohort (SCP1219) or a compatible lethal-COVID autopsy set

**Analysis plan:**
1. Map transitional-state score onto spatial coordinates
2. Test whether high-transitional-score spots co-localize with:
   - Low AT2 identity regions
   - High injury-composite regions
   - Proximity to immune cell infiltrates
3. Compute spatial autocorrelation (Moran's I) for the transitional score

**Expected output:**
- Spatial map with transitional-state score overlay
- Co-localization statistics
- Comparison to random spatial distribution

### O2: Pathology-linked validation
**Question:** Does donor-level transcriptomic dispersion correlate with pathology severity?

**Required data:**
- DAD (diffuse alveolar damage) grade or score per donor
- Histological assessment (edema, hyaline membranes, fibrosis stage)
- Clinical metadata (days on ventilator, viral load)

**Analysis plan:**
1. Correlate donor-level dispersion with DAD grade (Spearman)
2. Test whether high-dispersion donors have more severe pathology
3. Use pathology severity as an external validation of the transcriptomic geometry

**Expected output:**
- Scatter: donor-level dispersion vs pathology score
- Correlation coefficient and CI

### O3: Histology-aligned marker plausibility
**Question:** Are the marker predictions from the transcriptomic analysis consistent with protein-level expression patterns?

**What a histology collaborator would need:**
- Sections from the same or similar COVID-19 autopsy lungs
- Immunohistochemistry for: KRT8, CLDN4, SFTPC, AGER, CASP3, ISG15
- Expected pattern:
  - KRT8+/CLDN4+ cells at intermediate positions between intact alveoli and damaged regions
  - SFTPC+ cells in intact alveolar regions
  - AGER+ cells lining intact alveolar surfaces
  - CASP3+ cells in damaged/terminal regions

**This does not require computational implementation** — it requires a pathology collaboration.

### O4: RNA velocity
**Question:** Does RNA velocity support the same directionality as diffusion pseudotime?

**Required:**
- Spliced/unspliced count matrices (available if BAM files are accessible)
- scVelo or velocyto analysis

**Analysis plan:**
1. Compute RNA velocity on the same alveolar subset
2. Test whether velocity vectors point in the same direction as increasing pseudotime
3. Report velocity consistency as direction-independent evidence

**Status:** Not implemented. Requires access to raw BAM files from SCP1219.

## Priority ranking

| Validation | Feasibility | Reviewer impact | Priority |
|-----------|-------------|-----------------|----------|
| O4: RNA velocity | Medium (needs BAMs) | High | 1 |
| O2: Pathology linkage | Low (needs clinical data) | Very high | 2 |
| O1: Spatial localization | Low (needs spatial data) | Very high | 3 |
| O3: Histology markers | Low (needs collaboration) | High | 4 |

## For the current manuscript
None of these analyses are available for paper_v3. They are listed as future directions. If any become available before submission, they would substantially strengthen the paper.
