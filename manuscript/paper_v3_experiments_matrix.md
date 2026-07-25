# Paper v3 — Extension Experiments Matrix

## Experiment inventory

| ID | Category | Question | Required data | Can run now? | Expected impact | Reviewer value | Main risk | Manuscript location |
|----|----------|----------|---------------|-------------|-----------------|----------------|-----------|-------------------|
| D1 | Donor modeling | Donor-level primary endpoints | Primary atlas | YES | High | Essential | Low power (n=27) | Main text |
| D2 | Donor modeling | Pseudobulk expression profiles | Primary atlas | YES | Medium | High | None | Supplement |
| D3 | Donor modeling | Mixed-effects: PT ~ condition + (1\|donor) | Primary atlas | YES (needs statsmodels) | High | Essential | Small n | Main text |
| D4 | Donor modeling | Donor bootstrap CIs | Primary atlas | YES | High | Essential | None | Main text |
| D5 | Donor modeling | Study-weighted sensitivity | Replication data | YES | Medium | High | None | Supplement |
| M1 | Mechanism | Program-to-geometry linkage | Primary atlas | YES | Medium | Medium | Associative only | Main/supplement |
| M2 | Mechanism | Repair-failure axis analysis | Primary atlas | YES | Medium | Medium | Descriptive | Supplement |
| M3 | Mechanism | Branching/fate-competition | Primary atlas | YES (needs CellRank/Palantir) | Medium | Medium | May not resolve | Supplement |
| M4 | Mechanism | Geometry-informed transitional score | Primary atlas | YES | High | High | Novel, untested | Main text |
| M5 | Mechanism | Program-sequence robustness | Primary atlas | YES | Medium | High | Already partially done (Abl 8) | Supplement |
| P1 | State score | Candidate score construction | Primary atlas | YES | High | High | Novel | Main text |
| P2 | State score | Score benchmarking | Primary atlas | YES | High | High | None | Main text |
| P3 | State score | Cross-cohort transfer | Replication data | YES | Very high | Very high | May fail | Main text |
| P4 | State score | Stability audit | Primary atlas | YES | Medium | High | None | Supplement |
| G1 | Generalization | External disease-cohort replication | External data | NO (needs download) | Very high | Very high | Data access | Main text / future |
| G2 | Generalization | Multi-cohort geometric portability | External data | NO | Very high | Very high | Data access | Main text / future |
| G3 | Generalization | Cross-disease comparison | External data | NO | Very high | Very high | May not replicate | Main text / future |
| O1 | Orthogonal | Spatial localization | Spatial data | NO | Very high | Very high | Data access | Future work |
| O2 | Orthogonal | Pathology linkage | Clinical data | NO | Very high | Very high | Data access | Future work |
| O3 | Orthogonal | Histology markers | Collaboration | NO | High | High | Requires wet lab | Future work |
| O4 | Orthogonal | RNA velocity | BAM files | NO (needs BAMs) | High | High | Data access | Future work |

---

## What makes this a stronger specialized-journal paper
(achievable now with existing data)

1. Donor-level primary inference (D1, D3, D4)
2. Portable state score (P1-P3)
3. Program-to-geometry linkage (M1)
4. Repair-failure analysis (M2)
5. Ablation robustness already done

## What makes this a broad-interest journal paper
(achievable with external data download)

6. External disease-cohort replication (G1)
7. Cross-disease generalization (G3)
8. Multi-cohort portability matrix (G2)

## What would be needed for Nature-level ambition

9. Spatial transcriptomics validation (O1)
10. Pathology-linked validation (O2)
11. RNA velocity directionality (O4)
12. Functional validation in organoids (O3 / future)
13. Generalization to non-COVID injuries proven computationally (G3)
14. Mechanistic insight beyond association (requires perturbation data)

### Honest assessment
The current computational evidence alone is at **strong specialized-journal level** (Genome Biology, NAR Genomics, Bioinformatics). Adding donor-level inference and a portable state score brings it closer to **Nature Communications / Cell Reports** tier. Reaching **Nature** would require at minimum spatial validation or an independent wet-lab confirmation of the transitional-state biology, which is beyond the scope of a purely computational re-analysis.
