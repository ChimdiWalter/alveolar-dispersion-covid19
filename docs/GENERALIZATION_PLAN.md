# Generalization Plan — Beyond COVID-19

> **Status (as of 2026-08-25):** `src/generalization.py` is a functional, non-stub
> implementation (5 real functions: `harmonize_metadata`, `subset_alveolar_generic`,
> `cross_cohort_dispersion`, `cross_cohort_donor_direction`, `portability_matrix`),
> but it has never been run against real external data — no `data/external/`
> directory, no `scripts/run_generalization.py` driver script, and no
> `results/generalization/` output exist in this repo. **Scaffolded, not run.**

## Goal
Test whether dispersion-dominated loss of alveolar epithelial state coherence generalizes beyond lethal COVID-19 to other severe lung injury contexts.

---

## Rationale
The current paper's strongest finding — increased within-group dispersion — could reflect a general property of severe alveolar injury rather than a COVID-specific phenomenon. Demonstrating generalization would substantially increase the paper's impact and make the "loss of state coherence" framework a broadly useful tool.

## Candidate external datasets

| Dataset | Disease | Modality | Approx. donors | Priority | Acquisition |
|---------|---------|----------|-----------------|----------|-------------|
| Delorey 2021 (Nature) | Lethal COVID-19 | snRNA-seq | ~15 + ctrl | Essential | GEO |
| Wendisch 2021 (Cell) | COVID-19 + fibrosis | scRNA-seq | ~20 | High | GEO |
| Adams 2020 (Sci Adv) | IPF | scRNA-seq | ~32 + 28 ctrl | High | GEO |
| Habermann 2020 (Sci Adv) | IPF | scRNA-seq | ~20 | Medium | GEO |
| HLCA core (Nat Med 2023) | Healthy reference | scRNA/snRNA | ~100+ | Medium | cellxgene |

## Experiments

### G1: External disease-cohort replication
- Download Delorey 2021 or Adams 2020
- Extract alveolar AT1/AT2 cells
- Score same 8 gene programs
- Compute within-group dispersion (Levene's test)
- Compare to primary atlas result

### G2: Multi-cohort geometric portability
- Run dispersion analysis across multiple cohorts
- Compare variance ratios
- Test whether dispersion is a more portable signal than DATP thresholds

### G3: Cross-disease comparison
- Compare COVID fan-out to IPF fan-out
- Test whether the geometry (dispersion vs displacement) differs by disease

## Implementation
- `src/generalization.py` — harmonization and cross-cohort analysis functions
- `scripts/run_generalization.py` — entry point (creates stubs if data not present)
- `results/generalization/` — output directory

## Expected figures
- Cross-cohort dispersion comparison (bar/box plot of variance ratios)
- Donor-level summary comparison across diseases
- Portability heatmap: which signatures transfer to which cohorts

## Expected tables
- Dataset metadata (donors, cells, modality, disease)
- Dispersion metrics per cohort
- Portability matrix

## Status
- `src/generalization.py`: implemented (scaffold with harmonization, dispersion, donor-direction functions)
- External data: NOT downloaded — requires manual acquisition from GEO/cellxgene
- Analyses: NOT run — awaiting data
