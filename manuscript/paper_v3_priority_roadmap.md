# Paper v3 — Priority Roadmap

## Execution order for maximum impact

### Phase 1: Essential now (before any submission)

| Priority | Task | Module | Time estimate |
|----------|------|--------|--------------|
| 1 | Donor-level summary table | `src/donor_models.py` → `donor_summary()` | 1 hour |
| 2 | Donor-level bootstrap CIs for pseudotime shift and dispersion ratio | `src/donor_models.py` → `donor_bootstrap_ci()` | 1 hour |
| 3 | Donor-level Mann-Whitney for all key metrics | `src/donor_models.py` → `donor_level_test()` | 1 hour |
| 4 | Mixed-effects model (or simple OLS at donor level) | `src/donor_models.py` → `mixed_effects_pseudotime()` | 1 hour |
| 5 | Per-donor dispersion comparison | `src/donor_models.py` → `donor_dispersion_comparison()` | 1 hour |
| 6 | Update paper_v3.tex with computed donor-level results | Manual | 2 hours |

### Phase 2: High-value next (strengthens journal readiness)

| Priority | Task | Module | Time estimate |
|----------|------|--------|--------------|
| 7 | Portable state score: construct and benchmark | `src/state_score.py` → `score_all()`, `benchmark_scores()` | 3 hours |
| 8 | Cross-cohort state-score transfer test | `src/state_score.py` + replication data | 2 hours |
| 9 | Program-to-geometry linkage | `src/mechanism.py` → `program_geometry_linkage()` | 2 hours |
| 10 | Fan-out decomposition | `src/mechanism.py` → `fan_out_contribution()` | 1 hour |
| 11 | Repair-stall analysis | `src/mechanism.py` → `repair_stall_analysis()` | 1 hour |
| 12 | Generate all v3 figures (update plotting code) | `src/plots.py` | 4 hours |

### Phase 3: Optional but valuable

| Priority | Task | Module | Time estimate |
|----------|------|--------|--------------|
| 13 | Pseudobulk expression profiles | `src/donor_models.py` → `pseudobulk_expression()` | 2 hours |
| 14 | Local heterogeneity scores | `src/mechanism.py` → `local_heterogeneity()` | 1 hour |
| 15 | Program-sequence robustness (extended Ablation 8) | `scripts/ablations/` | 3 hours |
| 16 | Figure 1 conceptual schematic (manual illustration) | Manual / Illustrator | 3 hours |

### Phase 4: Ambitious / future work (requires external data)

| Priority | Task | Requirement |
|----------|------|-------------|
| 17 | Download and process Delorey 2021 or Adams 2020 | GEO access, compute |
| 18 | Run generalization experiments G1-G3 | External data |
| 19 | RNA velocity analysis | BAM files from SCP1219 |
| 20 | Spatial transcriptomics | New data acquisition |
| 21 | Pathology linkage | Clinical metadata / collaboration |

---

## Key strategic questions

### 1. Which additions most improve novelty without new wet-lab data?
- **Portable state score** (P1-P3): a continuous, donor-aware, cross-cohort-transferable transitional-state metric is genuinely novel and directly addresses the DATP portability failure
- **Program-to-geometry linkage** (M1): connects the geometric finding to biological programs

### 2. Which additions most improve reviewer confidence?
- **Donor-level inference** (D1-D4): essential — without this, a statistical reviewer will reject
- **Bootstrap CIs** (D4): provides uncertainty quantification that is currently missing
- **Mixed-effects model** (D3): formal treatment of the nested structure

### 3. Which additions are most realistic in the next stage?
- Everything in Phase 1 and Phase 2 can be done with existing data and code
- Phase 1 is ~6 hours of work; Phase 2 is ~13 hours

### 4. Which additions require external collaborations or datasets?
- G1-G3: external scRNA-seq datasets (downloadable from GEO)
- O1: spatial transcriptomics (requires data generation or collaboration)
- O2: pathology metadata (requires clinical collaboration)
- O3: histology validation (requires pathology collaboration)
