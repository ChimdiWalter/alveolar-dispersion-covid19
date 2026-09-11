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
**Corrected 2026-08-25 — see Phase 11 below for the evidence.** The bullets below
previously read as a checklist of upgrades; they should read as a calibrated
target, not a floor.
- **Class project:** exceeded
- **Workshop / poster:** exceeded
- **Strong specialized journal (Genome Biology, NAR Genomics and Bioinformatics,
  Communications Biology, iScience, Am J Respir Cell Mol Biol):** this is the
  paper's actual current level, and the honest primary submission target — not a
  floor already cleared.
- **Nature Communications / Cell Reports:** an uncertain **stretch goal**, not
  "achievable." Donor-level inference and the portable state score are done, but
  that alone does not close the gap to Nat Comms — see Phase 11.
- **Nature:** not realistic. Requires spatial validation, pathology linkage, or
  functional validation, none of which exist or are planned.

---

## Priority order for execution (v3)
1. Run donor-level inference (src/donor_models.py) — **essential before submission**
2. Run portable state score benchmarking (src/state_score.py) — high value
3. Run program-to-geometry linkage (src/mechanism.py) — strengthens novelty
4. Generate all v3 figures — required for submission
5. Update paper_v3.tex with computed results — required
6. Download external datasets for generalization (future)
7. Orthogonal validation (future — requires spatial / pathology data)

**Status note (2026-08-25):** items 1–5 above are done — see Phase 11.

---

## Phase 11: Critical Review and Journal-Tier Correction (2026-08-25)

A closer read of `manuscript/paper_v3.tex` against real comparable published work,
plus a direct (not self-reported) audit of the ablations and replication code,
found the journal-tier assessment above was overly optimistic and surfaced two
real gaps in the ablation grid. Nothing in this phase changes any manuscript
number or the underlying code — this is a documentation correction. Findings are
tracked as follow-up test cases in `ANALYSIS_PLAN.md` §9.

### Journal-tier reality check
- **Watson et al. (2023), *Am J Respir Cell Mol Biol*** — a closely comparable
  COVID-19 alveolar-epithelial reanalysis (167,280 cells, 6 studies pooled) —
  included lentiviral functional validation *and* IHC protein-level confirmation
  *and* bulk RNA-seq corroboration:
  [PMC10704119](https://pmc.ncbi.nlm.nih.gov/articles/PMC10704119/). `paper_v3`
  has none of that; it is purely computational reanalysis.
- **"Assessment of dispersion metrics for estimating single-cell transcriptional
  variability"** (*PLOS Computational Biology*, 2025 biorxiv preprint:
  [10.1101/2025.05.19.654854](https://www.biorxiv.org/content/10.1101/2025.05.19.654854))
  confirms dispersion/distance-to-centroid metrics are an established, actively
  studied methodology — not a framework this paper invented. `paper_v3`'s real
  contribution is the *application* to lethal COVID-19 alveolar injury plus the
  *extensive multi-cohort replication* (35 datasets, 618 donors), not a new
  statistical method.
- **Corrected verdict:** Nature is not realistic (unchanged — the original doc
  already conceded this). Nature Communications is a stretch, not an achieved
  checklist item, absent new (functional/spatial) data. The honest, defensible
  primary target is a specialized computational-biology/single-cell or pulmonary
  journal — Genome Biology, NAR Genomics and Bioinformatics, Communications
  Biology, iScience, or Am J Respir Cell Mol Biol. That is this paper's actual
  current level, and should be stated as the target, not a floor already cleared.

### Ablation grid: a real coverage gap
- `displacement_effect_size` is silently **frozen at the primary run's cached
  value** (`r = 0.1407`) across 5 of 10 ablations — embedding (#02),
  batch-correction (#03), root-strategy (#05), gene-program (#08), and Palantir
  (#09) — because `centroid_distance()` in `src/stats.py` defaults to
  `rep_key="X_pca"` and is never passed the ablation's actual embedding
  (`X_pca_harmony`, UMAP, diffmap, etc.). `paper_v3.tex` line 222 claims
  displacement was "never significant... across all ablations"; that claim is
  only genuinely re-tested by half the grid.
- **Ablation 1 (AT2-only) flips the displacement sign entirely**
  (`r = +0.14 → -0.29`, per `results/ablations/01_at2_only/metrics.json`) and is
  not mentioned anywhere in the manuscript.
- Not fixed (documentation-only per decision) — tracked as
  Follow-up 2 / `RUNBOOK.md` Step 14 (and the AT2-only sign flip as Follow-up 3
  / Step 15) in `ANALYSIS_PLAN.md` §9.

### Mechanism-regression caveat
`results/v3/fan_out_contribution.csv` (senescence coeff 6.83, oxidative_stress
3.83, nfkb_inflammatory 1.95 as top "drivers" of dispersion) is an unregularized
OLS with no p-values or cross-validation in the underlying file. `paper_v3.tex`
already hedges this appropriately (R²=0.11, "partial... interpretation," line
277), but the underlying analysis is weaker than that framing alone conveys to a
reader who doesn't check the raw file. Tracked as Follow-up 4 / `RUNBOOK.md`
Step 16 in `ANALYSIS_PLAN.md` §9.

### The 84-gene panel — the actionable good news
`scripts/replication/fetch_replication.py`'s `gene_shortlist` (lines 31–43) is
just the union of `config.yaml`'s gene-program genes plus a fixed marker list —
a pragmatic choice, not a hard data-source limitation. The code's own comment
says why: *"We restrict var-axis to the gene-program genes plus canonical markers
to keep the download compact (<1 GB)."* `cellxgene_census` is a public, no-login
API with **921,510 raw alveolar cells available** (per
`scripts/replication/analyze_replication.py`'s docstring) before the
84-gene/200-cells-per-donor subsampling that produced the paper's reported
89,736-cell figure. Expanding this — exactly what `paper_v3.tex`'s own
Limitations (line 287) and Future Directions (line 292) already call the "ideal
next step" — is achievable via a **code-only change** (loosen
`gene_shortlist`/`var_value_filter`, re-run `analyze_replication.py`), with no
manual portal-gated data acquisition, unlike the primary SCP1219 cohort. This is
the single best, most concrete, lowest-blocker next validation step available.
Tracked as Follow-up 1 / `RUNBOOK.md` Step 13 in `ANALYSIS_PLAN.md` §9.

### Manuscript prose
`paper_v3.tex`'s Results and Discussion sections repeat the same bolded-topic-
sentence pattern roughly 15+ times ("X was supported.", "Robust findings.",
"Portable.", "Not portable.", etc.), and the Discussion largely re-narrates each
Results subsection in the same order with the same numbers rather than
synthesizing at a higher level. Worth a revision pass; not executed on this
branch.
