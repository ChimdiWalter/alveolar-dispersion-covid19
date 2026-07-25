# Project Status — Epithelial Robustness Collapse

**Last updated:** 2026-04-13

---

## Phase 1: Project Audit and Synthesis — COMPLETE

### Current state
Three markdown documents exist (project_plan.md, project_plan_summary.md, project_proposal.md). All are well-written, biologically grounded, and internally consistent. No code, no data, no directory structure existed before this session.

### Strongest unifying title
*Epithelial Robustness Collapse in Lethal COVID-19: Trajectory Analysis of Alveolar Cell-State Failure in the Columbia/NYP Lung Atlas*

### Refined central hypothesis
Alveolar epithelial cells in lethal COVID-19 do not undergo a binary healthy-to-damaged transition but instead distribute across a continuous transcriptomic manifold reflecting staged robustness collapse — progressive loss of homeostatic identity, ordered activation then failure of repair programs, and convergence toward apoptotic terminal states — with AT2 cells showing distinctive evidence of stalled differentiation.

### Main biological claims to test
1. COVID alveolar cells are displaced from and more dispersed than healthy cells on the transcriptomic manifold
2. Pseudotime ordering reveals a staged cascade: interferon → inflammation → repair attempt → apoptosis
3. Transitional/failed-repair cells (KRT8+/CLDN4+) are enriched in COVID and occupy intermediate pseudotime
4. AT1 and AT2 follow partially distinct failure trajectories
5. These findings are robust across ablations of method, gene sets, donors, and cell composition

### Strengths
- Excellent biological framing with clear hypothesis structure
- Strong ablation/sensitivity plan (7 ablations, expanded to 10)
- Honest about cross-sectional limitations throughout
- Biology-first language makes it accessible
- Operational definition of robustness collapse (5 convergent criteria)

### Weaknesses / Gaps identified
- No code existed — everything was conceptual
- No requirements.txt or environment specification
- venv (lesegenv) lacks critical packages (scanpy, anndata, pandas, matplotlib, seaborn, statsmodels, harmonypy)
- No statistical analysis plan with power/effect-size considerations
- No formal threat-to-validity section
- Literature citations referenced conceptually but none formally cited
- No config-driven workflow — parameters scattered in prose
- Gene program definitions listed but not operationalized
- No manuscript structure

### Risks
- The venv lacks critical packages — must install before execution
- SCP1219 data must be downloaded manually
- Donor count and batch structure unknown until metadata inspection
- Cross-sectional design fundamentally limits causal claims

---

## Phase 2: Literature Grounding — COMPLETE

See `docs/LITERATURE_REVIEW.md` for the full literature scaffold with annotated bibliography and positioning statement.

## Phase 3: Research Design Refinement — COMPLETE

See `ANALYSIS_PLAN.md` for the manuscript-grade study design with statistical analysis plan and threat-to-validity section.

## Phase 4: Repository Structure — COMPLETE

### Files created
- `.gitignore`
- `config.yaml` — centralized project configuration
- `requirements.txt` — Python dependencies
- `src/__init__.py`, `src/utils.py`, `src/io.py`, `src/qc.py`
- `src/annotation.py`, `src/embedding.py`, `src/trajectory.py`
- `src/programs.py`, `src/stats.py`, `src/plots.py`
- `README.md`
- `ANALYSIS_PLAN.md`
- `FIGURE_PLAN.md`
- `TABLE_PLAN.md`
- `MANUSCRIPT_OUTLINE.md`
- `RUNBOOK.md`
- `TODO.md`
- `docs/LITERATURE_REVIEW.md`
- `scripts/run_pipeline.py`
- `notebooks/` — placeholder for analysis notebooks

### Directories created
```
data/raw/
data/processed/
metadata/
notebooks/
scripts/
src/
results/figures/
results/tables/
results/intermediate/
manuscript/figures/
manuscript/tables/
docs/
env/
logs/
```

## Phase 5: Data Handling Code — COMPLETE

All src/ modules contain functional code with docstrings:
- `io.py` — load/save h5ad, metadata, tables
- `qc.py` — QC metrics, filtering, summary
- `annotation.py` — marker validation, subsetting, re-clustering
- `embedding.py` — normalization, HVG, PCA, UMAP, diffusion map, Harmony
- `trajectory.py` — root finding, DPT, pseudotime statistics
- `programs.py` — gene program scoring, random controls, trends
- `stats.py` — displacement, dispersion, NN mixing, permutation tests, trend tests
- `plots.py` — all 7+ main figure types

## Phase 6–7: Experiments and Ablations — COMPLETE

See `ANALYSIS_PLAN.md` for full experiment and ablation specifications.
See `RUNBOOK.md` for execution instructions.

## Phase 8: Figure and Table Plan — COMPLETE

See `FIGURE_PLAN.md` and `TABLE_PLAN.md`.

## Phase 9: Manuscript Scaffold — COMPLETE

See `MANUSCRIPT_OUTLINE.md` and `manuscript/` directory.

---

## What requires actual execution

1. **Install dependencies**: `pip install -r requirements.txt` in lesegenv
2. **Download SCP1219 data**: manual download from Single Cell Portal
3. **Run the pipeline**: `python scripts/run_pipeline.py`
4. **Generate all figures and tables**
5. **Write manuscript prose**

## Phase 10: Paper v3 Reframing — COMPLETE (2026-04-30)

### Major changes
- **Title:** "Dispersion, not displacement: loss of alveolar epithelial state coherence in lethal COVID-19"
- **Central framing:** dispersion-dominated loss of state coherence (not "robustness collapse")
- **Donor as primary inferential unit** throughout
- **Harmony-corrected analysis** promoted to co-primary
- **Results reordered** to lead with strongest finding (dispersion)
- **Competing-model framing** added (displacement vs fan-out)
- **Negative result (centroid failure)** reframed as model-discriminating positive finding

### New files created
- `manuscript/paper_v3.tex` — full rewritten LaTeX manuscript
- `manuscript/paper_v3_TITLE_OPTIONS.md`
- `manuscript/paper_v3_ABSTRACT_OPTIONS.md`
- `manuscript/paper_v3_FIGURE_STORY.md`
- `manuscript/paper_v3_REVIEWER_RISKS.md`
- `manuscript/paper_v3_RESULTS_REWRITE_NOTES.md`
- `manuscript/paper_v3_CHANGELOG.md`
- `manuscript/paper_v3_experiments_matrix.md`
- `manuscript/paper_v3_priority_roadmap.md`
- `src/donor_models.py` — donor-level inference module
- `src/state_score.py` — portable transitional-state scoring
- `src/mechanism.py` — program-to-geometry linkage
- `src/generalization.py` — cross-disease generalization scaffold
- `docs/GENERALIZATION_PLAN.md`
- `docs/ORTHOGONAL_VALIDATION_PLAN.md`

### Current paper level assessment
- **Class project:** exceeded
- **Workshop / poster:** exceeded
- **Strong specialized journal (Genome Biology, NAR Genomics):** YES — current level
- **Nature Communications / Cell Reports:** achievable with donor-level inference and portable state score
- **Nature:** requires spatial validation, pathology linkage, or functional validation

---

## Priority order for execution (v3)
1. Run donor-level inference (src/donor_models.py) — **essential before submission**
2. Run portable state score benchmarking (src/state_score.py) — high value
3. Run program-to-geometry linkage (src/mechanism.py) — strengthens novelty
4. Generate all v3 figures — required for submission
5. Update paper_v3.tex with computed results — required
6. Download external datasets for generalization (future)
7. Orthogonal validation (future — requires spatial / pathology data)
