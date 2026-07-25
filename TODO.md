# TODO — Project Task List

## Dispersion, Not Displacement: Loss of Alveolar Epithelial State Coherence in Lethal COVID-19

**Last updated: 2026-04-30 (paper_v3 revision)**

---

## Paper v3 — Essential before submission

- [ ] Run `src/donor_models.py` → `donor_summary()` on primary atlas
- [ ] Run `src/donor_models.py` → `donor_level_test()` for pseudotime, dispersion, frac_transitional
- [ ] Run `src/donor_models.py` → `donor_bootstrap_ci()` for pseudotime shift and dispersion ratio
- [ ] Run `src/donor_models.py` → `mixed_effects_pseudotime()` (install statsmodels if needed)
- [ ] Run `src/donor_models.py` → `donor_dispersion_comparison()` for per-donor dispersion
- [ ] Update paper_v3.tex with computed donor-level results (replace TODO placeholders)
- [ ] Generate Figure 1: competing-models conceptual schematic (manual illustration)
- [ ] Generate Figure 3: dispersion centerpiece with donor-level and replication panels
- [ ] Generate Figure 4: donor-aware pseudotime with Harmony comparison
- [ ] Generate Figure 7: replication summary with portability matrix
- [ ] Compile paper_v3.tex and verify it renders correctly

## Paper v3 — High-value next

- [ ] Run `src/state_score.py` → `score_all()` and `benchmark_scores()` on primary atlas
- [ ] Test state scores on replication cohort for cross-cohort transfer
- [ ] Run `src/mechanism.py` → `program_geometry_linkage()` on primary atlas
- [ ] Run `src/mechanism.py` → `fan_out_contribution()` to identify dispersion-driving programs
- [ ] Run `src/mechanism.py` → `repair_stall_analysis()` for repair-failure axis
- [ ] Generate all v3 supplementary figures (S1-S13)
- [ ] Write supplementary methods for new donor-level analyses

## Paper v3 — Optional / ambitious

- [ ] Download Delorey 2021 or Adams 2020 for cross-disease generalization (G1-G3)
- [ ] Run `src/generalization.py` on external datasets
- [ ] Investigate RNA velocity feasibility (requires BAM files)
- [ ] Build classifier-based transitional-state transfer (replaces marker thresholds)

---

## Immediate (before any analysis)

- [ ] Install Python dependencies: `pip install -r requirements.txt` in lesegenv
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

## Phase 1: Data loading and QC (Week 1)

- [ ] Load atlas and print shape, columns, dtypes
- [ ] Identify correct condition column, cell-type column, donor column
- [ ] Update config.yaml with verified column names
- [ ] Compute and inspect QC metric distributions
- [ ] Set dataset-specific QC thresholds (adjust defaults if needed)
- [ ] Apply QC filters
- [ ] Save QC summary table (Table S2)

## Phase 2: Annotation and subsetting (Week 1–2)

- [ ] Validate cell-type annotations with marker genes
- [ ] Save marker validation table (Table S3)
- [ ] Decide whether re-annotation is needed
- [ ] Subset to alveolar epithelial cells (AT1, AT2, Transitional)
- [ ] Generate cohort summary table (Table 1)
- [ ] Save validated alveolar subset

## Phase 3: Embedding and manifold (Week 2)

- [ ] Normalize and select HVGs
- [ ] Run PCA; inspect variance explained (Figure S4)
- [ ] Assess batch/donor effects on PCA
- [ ] Apply Harmony if needed
- [ ] Build neighbor graph
- [ ] Compute UMAP (Figure 1)
- [ ] Compute diffusion map (Figure S5)
- [ ] Generate batch assessment figure (Figure S3)
- [ ] Save embedded alveolar object

## Phase 4: Trajectory and gene programs (Week 3)

- [ ] Select root cell (healthy AT2 centroid)
- [ ] Run diffusion pseudotime
- [ ] Generate pseudotime UMAP (Figure 2)
- [ ] Compute pseudotime density by condition (Figure 4)
- [ ] Score all 8 gene programs
- [ ] Generate gene program dynamics plot (Figure 3)
- [ ] Generate marker gene trends (Figure 5)
- [ ] Compute pseudotime by donor (Figure 7)
- [ ] Identify transitional cell population
- [ ] Save pseudotime-scored object

## Phase 5: Statistical analysis (Week 3)

- [ ] Compute centroid distance and run displacement test
- [ ] Run dispersion test (Levene's)
- [ ] Compute NN condition mixing
- [ ] Run permutation test for pseudotime enrichment
- [ ] Compute gene-level pseudotime trends (Table S4)
- [ ] Compute robustness composite score (Table 3)
- [ ] Save all statistics tables (Table 2, Table 3)

## Phase 6: Ablations (Week 4)

- [ ] Ablation 1: AT2-only
- [ ] Ablation 2: Embedding comparison (UMAP vs diffmap)
- [ ] Ablation 3: With/without batch correction
- [ ] Ablation 4: Remove apoptosis genes
- [ ] Ablation 5: Root cell sensitivity (4 roots)
- [ ] Ablation 6: Broader epithelial context
- [ ] Ablation 7: Leave-one-donor-out
- [ ] Ablation 8: Alternative gene program definitions
- [ ] Ablation 9: Palantir trajectory
- [ ] Ablation 10: Permutation and random gene-set controls
- [ ] Generate ablation summary figure (Figure 6)
- [ ] Save ablation summary table (Table S6)

## Phase 7: Figures and tables (Week 5)

- [ ] Generate all main figures (1–7) at publication quality
- [ ] Generate all supplementary figures (S1–S11)
- [ ] Generate all main tables (1–3)
- [ ] Generate all supplementary tables (S1–S8)
- [ ] Write figure legends

## Phase 8: Writing (Weeks 5–6)

- [ ] Draft Methods section
- [ ] Draft Results section
- [ ] Draft Introduction
- [ ] Draft Discussion
- [ ] Draft Abstract
- [ ] Draft Supplementary Notes
- [ ] Internal review and revision

## Phase 9: Finalization (Week 6)

- [ ] Clean and document all code
- [ ] Verify reproducibility (re-run from clean state)
- [ ] Prepare oral presentation slides
- [ ] Final review of all deliverables
- [ ] Submit
