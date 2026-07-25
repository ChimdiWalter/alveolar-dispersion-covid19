# Project: Ablation-First Trajectory Analysis of Alveolar Epithelial Robustness Collapse in Lethal COVID-19

A class-project reanalysis of the Columbia/NYP COVID-19 Lung Atlas (SCP1219, Melms 2021)
with pre-registered robustness tests, a ten-way ablation battery, and an independent
cross-cohort replication on 618 donors from cellxgene census.

**Status:** v2 revision complete. Harmony batch correction fixed, gene-program audit
done, independent replication added.

---

## TL;DR (v2)

| Criterion | Primary (SCP1219) | Replication (census, 618 donors) |
|---|---|---|
| Centroid displacement (MW) | fails (p=1.0) | fails cell-level (p=1.0) |
| Dispersion (Levene) | supported (p ≈ 0) | **supported** (p ≈ 10⁻¹³⁷) |
| Pseudotime enrichment | supported (p=0.001) | supported donor-level (p=1.98e-3) |
| Harmony-corrected shift | — | **MPD × 2.6** (0.0483 → 0.1246) |
| KRT8⁺/CLDN4⁺ DATPs | 3.1× enriched | 0.48× (retracted as portable metric) |

**Takeaways.** Robustness collapse (dispersion + donor-level pseudotime displacement)
replicates across cohorts. Directional centroid displacement and marker-threshold
DATP enrichment do not.

---

## Manuscripts and presentations

### v1 (original)
- [paper.tex](manuscript/paper.tex) — [paper.pdf](manuscript/paper.pdf)
- [presentation.tex](manuscript/presentation.tex) — [presentation.pdf](manuscript/presentation.pdf)
- [explainer.tex](manuscript/explainer.tex) — [explainer.pdf](manuscript/explainer.pdf)

### v2 (revised, with Harmony fix + replication)
- [paper_v2.tex](manuscript/paper_v2.tex) — [paper_v2.pdf](manuscript/paper_v2.pdf)
- [presentation_2.tex](manuscript/presentation_2.tex) — [presentation_2.pdf](manuscript/presentation_2.pdf)
- [explainer_2.tex](manuscript/explainer_2.tex) — [explainer_2.pdf](manuscript/explainer_2.pdf)

### Planning documents
- [project_proposal.md](project_proposal.md)
- [project_plan.md](project_plan.md) — [project_plan_summary.md](project_plan_summary.md)
- [ANALYSIS_PLAN.md](ANALYSIS_PLAN.md)
- [MANUSCRIPT_OUTLINE.md](MANUSCRIPT_OUTLINE.md)
- [FIGURE_PLAN.md](FIGURE_PLAN.md) — [TABLE_PLAN.md](TABLE_PLAN.md)
- [PROJECT_STATUS.md](PROJECT_STATUS.md) — [RUNBOOK.md](RUNBOOK.md) — [TODO.md](TODO.md)

---

## Figures

| # | File | What it shows |
|---|---|---|
| 1a | [fig1a_condition.pdf](results/figures/fig1a_condition.pdf) / [.png](results/figures/fig1a_condition.png) | UMAP colored by condition (COVID / Healthy) |
| 1b | [fig1b_celltype.pdf](results/figures/fig1b_celltype.pdf) / [.png](results/figures/fig1b_celltype.png) | UMAP colored by cell type (AT1 / AT2 / ECM-high) |
| 2  | [fig2_pseudotime.pdf](results/figures/fig2_pseudotime.pdf) / [.png](results/figures/fig2_pseudotime.png) | UMAP colored by diffusion pseudotime |
| 3  | [fig3_program_dynamics.pdf](results/figures/fig3_program_dynamics.pdf) / [.png](results/figures/fig3_program_dynamics.png) | 8 gene-program scores vs pseudotime |
| 4  | [fig4_pseudotime_density.pdf](results/figures/fig4_pseudotime_density.pdf) / [.png](results/figures/fig4_pseudotime_density.png) | Pseudotime density, COVID vs Healthy |
| 5  | [fig5_marker_trends.pdf](results/figures/fig5_marker_trends.pdf) / [.png](results/figures/fig5_marker_trends.png) | Canonical marker expression along pseudotime |
| 5b | [fig5b_displacement.pdf](results/figures/fig5b_displacement.pdf) / [.png](results/figures/fig5b_displacement.png) | Within-group distance to centroid (dispersion) |
| 7  | [fig7_donor_consistency.pdf](results/figures/fig7_donor_consistency.pdf) / [.png](results/figures/fig7_donor_consistency.png) | LOO donor consistency of pseudotime shift |

---

## Tables

### Main tables
- [table2_robustness_metrics.csv](results/tables/table2_robustness_metrics.csv) — 3 pre-registered criteria outcomes
- [table3_composite_evidence.csv](results/tables/table3_composite_evidence.csv) — composite assessment
- [pseudotime_by_condition.csv](results/tables/pseudotime_by_condition.csv) — per-condition pseudotime summary

### Supplementary
- [tableS2_qc_prefilter.csv](results/tables/tableS2_qc_prefilter.csv) / [tableS2_qc_postfilter.csv](results/tables/tableS2_qc_postfilter.csv) — QC metrics
- [tableS3_marker_validation.csv](results/tables/tableS3_marker_validation.csv) — marker specificity
- [tableS5_donor_statistics.csv](results/tables/tableS5_donor_statistics.csv) — per-donor cell counts and LOO
- [tableS6_ablation_summary.csv](results/ablations/tableS6_ablation_summary.csv) — full ablation battery
- [tableS8_program_trends.csv](results/tables/tableS8_program_trends.csv) — program ordering along pseudotime

---

## Ablations (results/ablations/)

| # | Variant | Metrics |
|---|---|---|
| 01 | [AT2-only](results/ablations/01_at2_only/) | restrict to AT2 cells |
| 02 | [diffmap](results/ablations/02_embedding_diffmap/) / [umap](results/ablations/02_embedding_umap/) | embedding swap |
| 03 | [corrected](results/ablations/03_batch_corrected/) / [uncorrected](results/ablations/03_batch_uncorrected/) | Harmony on/off (**v2: now functional**) |
| 04 | [no-apoptosis-genes](results/ablations/04_no_apoptosis_genes/) | program leakage check |
| 05 | [AT2-centroid](results/ablations/05_root_healthy_AT2_centroid/) / [AT1-centroid](results/ablations/05_root_healthy_AT1_centroid/) / [random-healthy](results/ablations/05_root_random_healthy/) / [COVID-extreme](results/ablations/05_root_covid_extreme/) | root sensitivity |
| 06 | [broader-epithelial](results/ablations/06_broader_epithelial/) | airway inclusion (shift abolished) |
| 07 | [LOO](results/ablations/07_leave_one_donor_out/) | leave-one-donor-out, 27 iters |
| 08 | [curated-only](results/ablations/08_alt_programs_curated_only/) / [MSigDB-only](results/ablations/08_alt_programs_msigdb_only/) | gene-list sensitivity |
| 09 | [Palantir](results/ablations/09_palantir/) | alt trajectory algorithm |
| 10 | [permutation-controls](results/ablations/10_permutation_controls/) | 1000 label shuffles |

Summary CSV: [tableS6_ablation_summary.csv](results/ablations/tableS6_ablation_summary.csv)

---

## Replication cohort (v2, new)

- Scripts: [scripts/replication/fetch_replication.py](scripts/replication/fetch_replication.py), [scripts/replication/analyze_replication.py](scripts/replication/analyze_replication.py)
- Data (not tracked): `data/replication/replication_alveolar.h5ad` — 921,510 × 84, 35 datasets, 618 donors, Melms excluded
- Results: [replication_metrics.json](results/replication/replication_metrics.json), [replication_obs.parquet](results/replication/replication_obs.parquet)

Headline: n=89,736 cells post-cap (4,441 COVID / 85,295 normal; 43 COVID donors / 575 normal donors). Dispersion Levene stat 626, p≈10⁻¹³⁷; donor-level MW p=1.98e-3.

---

## Source code layout

- [src/io.py](src/io.py) — data loading
- [src/qc.py](src/qc.py) — QC filters
- [src/embedding.py](src/embedding.py) — PCA/UMAP/diffmap/Harmony (**v2: Harmony orientation fix, lines 196–199**)
- [src/trajectory.py](src/trajectory.py) — diffusion pseudotime
- [src/programs.py](src/programs.py) — gene-program scoring
- [src/annotation.py](src/annotation.py) — cell-type annotation
- [src/stats.py](src/stats.py) — pre-registered tests
- [src/plots.py](src/plots.py) — figure code
- [src/utils.py](src/utils.py) — misc utilities

Pipeline drivers:
- [scripts/run_pipeline.py](scripts/run_pipeline.py) — primary end-to-end
- [scripts/ablations/run_all_ablations.py](scripts/ablations/run_all_ablations.py) — ablation battery
- [scripts/download_data.py](scripts/download_data.py)
- [Snakefile](Snakefile) / [Makefile](Makefile)

Configuration:
- [config.yaml](config.yaml) — pipeline parameters, gene programs, QC thresholds
- [requirements.txt](requirements.txt)

---

## How to reproduce

```bash
# primary pipeline
python scripts/run_pipeline.py

# ablations (10-way)
python scripts/ablations/run_all_ablations.py

# v2 replication
python scripts/replication/fetch_replication.py     # downloads from cellxgene census
python scripts/replication/analyze_replication.py   # runs Levene, MW, chi-square

# build papers
cd manuscript
pdflatex paper_v2.tex && pdflatex paper_v2.tex
pdflatex presentation_2.tex
pdflatex explainer_2.tex && pdflatex explainer_2.tex
```

Environment: Python 3.12.3, scanpy 1.12.1, anndata 0.12.10, harmonypy 0.2.0
(PyTorch backend), palantir 1.4.4. Seed 42 throughout.
