# TODO — Project Task List

## Dispersion, Not Displacement: Loss of Alveolar Epithelial State Coherence in Lethal COVID-19

**Last updated: 2026-08-25 (critical-review revision)**

This revision corrects the prior version's stale completion status: nearly
everything below marked complete had, in fact, already been done — it just
wasn't checked off. It also replaces the old "Optional / ambitious" list with a
feasibility-ordered set of concrete follow-ups identified by a closer,
evidence-based review of the manuscript and its underlying results. See
`PROJECT_STATUS.md`'s "Phase 11: Critical Review and Journal-Tier Correction"
section for the full evidence trail behind every claim here — this file stays a
task list, not a report.

---

## Paper v3 — Essential before submission

- [x] Run `src/donor_models.py` → `donor_summary()` on primary atlas — `results/v3/donor_summary.csv`
- [x] Run `src/donor_models.py` → `donor_level_test()` for pseudotime, dispersion, frac_transitional — `results/v3/donor_level_tests.json`
- [x] Run `src/donor_models.py` → `donor_bootstrap_ci()` for pseudotime shift and dispersion ratio — `results/v3/donor_bootstrap_ci.json`
- [x] Run `src/donor_models.py` → `mixed_effects_pseudotime()` — `results/v3/mixed_effects.json`
- [x] Run `src/donor_models.py` → `donor_dispersion_comparison()` for per-donor dispersion — `results/v3/donor_dispersion*.{json,csv}`
- [x] Update paper_v3.tex with computed donor-level results — every number in `manuscript/paper_v3.tex` matches `results/v3/` (verified line-by-line, e.g. OLS coefficient +0.043/p=0.013/R²=0.22 at line 199, mixed-effects at line 284)
- [x] Generate Figure 1: competing-models conceptual schematic — present as inline TikZ in `paper_v3.tex` (not a separate image file; functional but a hand-drawn schematic, see Priority 3 below for a polish note)
- [x] Generate Figure 3: dispersion centerpiece with donor-level and replication panels — `results/figures/fig3_dispersion_centerpiece.{pdf,png}`
- [x] Generate Figure 4: donor-aware pseudotime with Harmony comparison — `results/figures/fig4_donor_pseudotime.{pdf,png}`
- [x] Generate Figure 7: replication summary with portability matrix — `results/figures/fig7_replication_summary.{pdf,png}`
- [x] Compile paper_v3.tex and verify it renders correctly — `manuscript/paper_v3.pdf` exists (2.1MB, figure-heavy, not a near-empty stub)

## Paper v3 — High-value next

- [x] Run `src/state_score.py` → `score_all()` and `benchmark_scores()` on primary atlas — `results/v3/state_scores.csv`, `state_score_benchmarks.csv`
- [x] Test state scores on replication cohort for cross-cohort transfer — `results/v3/replication_state_benchmarks.csv` (all p < 10⁻³⁰⁰ for condition separation, per paper_v3.tex Future Directions)
- [x] Run `src/mechanism.py` → `program_geometry_linkage()` on primary atlas — `results/v3/program_geometry_linkage.csv`
- [x] Run `src/mechanism.py` → `fan_out_contribution()` to identify dispersion-driving programs — `results/v3/fan_out_contribution.csv` (see caveat under Priority 3: this regression has no p-values or cross-validation in the saved file — treat its ranking as suggestive, not confirmed)
- [x] Run `src/mechanism.py` → `repair_stall_analysis()` for repair-failure axis — `results/v3/repair_stall.json`
- [x] Generate all v3 supplementary figures (S1-S13) — all present as PDF+PNG pairs in `results/figures/`
- [x] Write supplementary methods for new donor-level analyses — covered in `manuscript/paper_v3.tex`'s abridged Methods section (donor-level OLS, bootstrap, mixed-effects all described)

## Paper v3 — Prioritized follow-ups (feasibility-ordered, 2026-08-25)

Replaces the old "Optional / ambitious" list. Ordered by what's actually
achievable next, not by scientific importance alone. Full specs for each are in
`ANALYSIS_PLAN.md`'s new "Follow-up" section (same `Field | Value` / "Failure
mode" format Chimdi used for the original experiment specs).

**Priority 1 — no external gate, code + public API only:**
- [ ] Expand the replication cohort's gene panel beyond the current 84-gene
      shortlist (or go full-transcriptome) via `cellxgene_census`, then
      re-run a genuine manifold/DPT replication instead of the program-score
      surrogate. This is uniquely low-blocker: `scripts/replication/fetch_replication.py`
      already fetches this cohort programmatically from the public
      `cellxgene_census` API — no portal login required, unlike SCP1219. Only
      `gene_shortlist`/`var_value_filter` (lines 31–43) need loosening and
      `scripts/replication/analyze_replication.py` needs re-running. See
      ANALYSIS_PLAN.md Follow-up 1 / RUNBOOK.md Step 13.

**Priority 2 — needs real primary SCP1219 data (blocked on manual portal download):**
- [ ] Fix `centroid_distance()`'s `rep_key` wiring so `displacement_effect_size`
      is actually recomputed per ablation instead of silently reusing the
      cached primary-run value (`r = 0.1407`) across ablations 02, 03, 05, 08,
      and 09 — then re-run all 10 ablations. See ANALYSIS_PLAN.md Follow-up 2 /
      RUNBOOK.md Step 14.

**Priority 3 — writing/analysis, no new data needed:**
- [ ] Disclose ablation 1's (AT2-only) displacement-sign flip
      (`r = +0.14 → -0.29`) in the manuscript — currently unmentioned. See
      ANALYSIS_PLAN.md Follow-up 3 / RUNBOOK.md Step 15.
- [ ] Revision pass on Results/Discussion prose: the same bolded-topic-sentence
      pattern ("X was supported." / "Robust findings." / "Portable.") repeats
      15+ times, and Discussion largely re-narrates Results in the same order
      rather than synthesizing — worth tightening.
- [ ] Add significance testing/cross-validation to the mechanism regression
      (`results/v3/fan_out_contribution.csv`), or soften its manuscript
      language further given the underlying analysis has no p-values or CV.
      See ANALYSIS_PLAN.md Follow-up 4 / RUNBOOK.md Step 16.
- [ ] Fill in real author names/affiliations (`manuscript/paper_v3.tex:22` is
      still a placeholder).
- [ ] Optional: polish Figure 1's hand-drawn TikZ schematic into a proper
      illustration.

**Priority 4 — genuinely blocked on new data or collaboration (unchanged):**
- [ ] Download Delorey 2021 or Adams 2020 for cross-disease generalization (G1-G3)
- [ ] Run `src/generalization.py` on external datasets
- [ ] Investigate RNA velocity feasibility (requires BAM files)
- [ ] Build classifier-based transitional-state transfer (replaces marker thresholds)
- [ ] Spatial transcriptomics / pathology linkage (needs a new collaboration)

---

## Immediate (before any analysis on a fresh clone)

The analysis below has already been run once, on a machine that had the real
SCP1219 data — that's what `results/` reflects. These steps are what a *new*
environment (a fresh clone, or the reproducibility harness)
needs before it can re-run anything for real.

- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Download SCP1219 dataset from Single Cell Portal → `data/raw/` (run `python scripts/download_data.py --verify` to confirm)
- [ ] Download metadata files → `metadata/`
- [ ] Open `notebooks/01_data_inspection.ipynb` and update `config.yaml` with verified column names
- [ ] Verify literature citations in `docs/LITERATURE_REVIEW.md` (DOIs, exact author lists)

## Automation entry points (created)

- `make pipeline` — full primary analysis
- `make ablations` — all 10 ablation experiments
- `snakemake -j4` — DAG-driven reproducible build
- `notebooks/01_data_inspection.ipynb` — inspect columns/donors/markers
- `notebooks/02_qc_and_subset.ipynb` — QC thresholds and alveolar subset
- `notebooks/03_trajectory_exploration.ipynb` — interactive pseudotime/program exploration

## Phase 1: Data loading and QC (Week 1) — complete (see results/tables/tableS2_qc_*)

- [x] Load atlas and print shape, columns, dtypes
- [x] Identify correct condition column, cell-type column, donor column
- [x] Update config.yaml with verified column names
- [x] Compute and inspect QC metric distributions
- [x] Set dataset-specific QC thresholds (adjust defaults if needed)
- [x] Apply QC filters
- [x] Save QC summary table (Table S2)

## Phase 2: Annotation and subsetting (Week 1–2) — complete

- [x] Validate cell-type annotations with marker genes
- [x] Save marker validation table (Table S3)
- [x] Decide whether re-annotation is needed
- [x] Subset to alveolar epithelial cells (AT1, AT2, Transitional)
- [x] Generate cohort summary table (Table 1)
- [x] Save validated alveolar subset

## Phase 3: Embedding and manifold (Week 2) — complete

- [x] Normalize and select HVGs
- [x] Run PCA; inspect variance explained (Figure S4)
- [x] Assess batch/donor effects on PCA
- [x] Apply Harmony if needed
- [x] Build neighbor graph
- [x] Compute UMAP (Figure 1)
- [x] Compute diffusion map (Figure S5)
- [x] Generate batch assessment figure (Figure S3)
- [x] Save embedded alveolar object

## Phase 4: Trajectory and gene programs (Week 3) — complete

- [x] Select root cell (healthy AT2 centroid)
- [x] Run diffusion pseudotime
- [x] Generate pseudotime UMAP (Figure 2)
- [x] Compute pseudotime density by condition (Figure 4)
- [x] Score all 8 gene programs
- [x] Generate gene program dynamics plot (Figure 3)
- [x] Generate marker gene trends (Figure 5)
- [x] Compute pseudotime by donor (Figure 7)
- [x] Identify transitional cell population
- [x] Save pseudotime-scored object

## Phase 5: Statistical analysis (Week 3) — complete

- [x] Compute centroid distance and run displacement test
- [x] Run dispersion test (Levene's)
- [x] Compute NN condition mixing
- [x] Run permutation test for pseudotime enrichment
- [x] Compute gene-level pseudotime trends (Table S4)
- [x] Compute robustness composite score (Table 3)
- [x] Save all statistics tables (Table 2, Table 3)

## Phase 6: Ablations (Week 4) — complete, but see Priority 2 above (displacement metric not re-tested by 5/10 ablations)

- [x] Ablation 1: AT2-only
- [x] Ablation 2: Embedding comparison (UMAP vs diffmap)
- [x] Ablation 3: With/without batch correction
- [x] Ablation 4: Remove apoptosis genes
- [x] Ablation 5: Root cell sensitivity (4 roots)
- [x] Ablation 6: Broader epithelial context
- [x] Ablation 7: Leave-one-donor-out
- [x] Ablation 8: Alternative gene program definitions
- [x] Ablation 9: Palantir trajectory
- [x] Ablation 10: Permutation and random gene-set controls
- [x] Generate ablation summary figure (Figure 6)
- [x] Save ablation summary table (Table S6)

## Phase 7: Figures and tables (Week 5) — complete

- [x] Generate all main figures (1–7) at publication quality
- [x] Generate all supplementary figures (S1–S13)
- [x] Generate all main tables (1–3)
- [x] Generate all supplementary tables (S1–S8)
- [x] Write figure legends

## Phase 8: Writing (Weeks 5–6) — complete, but see Priority 3 above (prose revision recommended)

- [x] Draft Methods section
- [x] Draft Results section
- [x] Draft Introduction
- [x] Draft Discussion
- [x] Draft Abstract
- [x] Draft Supplementary Notes
- [ ] Internal review and revision — this critical review is a first pass; see Priority 3

## Phase 9: Finalization (Week 6)

- [x] Clean and document all code — all 68 public functions and classes across `src/` carry docstrings (verified by AST scan), and the synthetic-data test suite, CI, pinned deps and provenance tracking cover every `src/` module
- [ ] Verify reproducibility (re-run from clean state) — blocked on real SCP1219 data access; the reproducibility harness makes the *code* verifiable without real data, but a real-data re-run is still needed to confirm the numbers themselves
- [ ] Prepare oral presentation slides
- [ ] Final review of all deliverables
- [ ] Submit — blocked on author names/affiliations (Priority 3) and a final decision on target journal (see PROJECT_STATUS.md Phase 11)
