# Changelog

Audit trail of substantive project-status and documentation changes. Each entry
cites the evidence behind it — file paths, and how the claim was verified — so
status claims here can be independently checked, not just trusted.

---

## 2026-08-25 — Manuscript-status critical review (`pierce/manuscript-status-review`)

A closer, evidence-based read of `manuscript/paper_v3.tex` against real
comparable published work, plus a direct audit of the ablations and replication
pipeline code (not a self-reported status check). Documentation-only — no code
or manuscript numbers changed on this branch.

- **Journal-tier assessment corrected.** `PROJECT_STATUS.md`'s "Current paper
  level assessment" previously stated Nature Communications was "achievable
  with donor-level inference and portable state score." Corrected to label Nat
  Comms an uncertain stretch goal, and the specialized-journal tier (Genome
  Biology, NAR Genomics and Bioinformatics, Communications Biology, iScience,
  Am J Respir Cell Mol Biol) as the actual target. Evidence: direct comparison
  to Watson et al. 2023 (*Am J Respir Cell Mol Biol*, PMC10704119), a closely
  comparable COVID-19 alveolar-epithelial reanalysis that included functional
  (lentiviral) and protein-level (IHC) validation `paper_v3` lacks; and
  "Assessment of dispersion metrics..." (PLOS Comp Bio, biorxiv
  10.1101/2025.05.19.654854), confirming dispersion metrics are established
  methodology, not a novel framework. See `PROJECT_STATUS.md` Phase 11.

- **Ablation coverage gap found.** `displacement_effect_size` is frozen at the
  primary run's cached value across 5 of 10 ablations because
  `centroid_distance()` (`src/stats.py`) defaults to `rep_key="X_pca"` and is
  never passed the ablation's actual embedding. Verified by direct read of
  `results/ablations/{02,03,05,08,09}_*/metrics.json` (identical
  `r = 0.1407` across all five) and `src/stats.py`'s `centroid_distance()`
  signature. Also found: ablation 1 (AT2-only) flips the displacement sign
  (`r = +0.14 → -0.29`, `results/ablations/01_at2_only/metrics.json`), not
  disclosed in `paper_v3.tex`. Not fixed on this branch (decision: document
  only — code fix deferred since re-validating it needs real SCP1219 data,
  which isn't available locally). Tracked as `ANALYSIS_PLAN.md` §9 Follow-up 2
  (and the AT2-only flip as Follow-up 3).

- **Mechanism-regression caveat documented.** `results/v3/fan_out_contribution.csv`
  (the senescence/oxidative-stress/inflammatory "driver" coefficients cited in
  `paper_v3.tex` line 277) is an unregularized OLS with no p-values or
  cross-validation columns in the file itself — verified by reading the CSV
  directly. The manuscript's existing hedge (R²=0.11) is appropriate but
  doesn't fully convey this to a reader who doesn't check the raw file. Tracked
  as `ANALYSIS_PLAN.md` §9 Follow-up 4.

- **84-gene replication panel: identified as a low-blocker next step, not a
  hard limitation.** Read `scripts/replication/fetch_replication.py` lines
  31–43: the panel is the union of `config.yaml`'s gene-program genes plus a
  fixed marker list, restricted only "to keep the download compact (<1 GB)"
  (verbatim code comment) — not a `cellxgene_census` API constraint. The census
  has 921,510 raw alveolar cells available (per
  `scripts/replication/analyze_replication.py`'s docstring) before the
  84-gene/200-cells-per-donor subsampling that produced the paper's reported
  89,736-cell figure. Expanding the panel is a code-only change with no
  portal-gated manual step, unlike the primary SCP1219 cohort. Tracked as
  `ANALYSIS_PLAN.md` §9 Follow-up 1 — the single most actionable next
  validation step identified this session.

- **`TODO.md` rewritten** to check off genuinely completed items (donor-level
  inference, bootstrap CIs, mixed-effects, state scores, mechanism linkage,
  figures/tables — all verified present in `results/v3/` and `results/figures/`
  during an earlier session's audit, 2026-08-22) and replace the stale
  "Optional/ambitious" section with a feasibility-ordered list reflecting this
  session's findings.

- **`ANALYSIS_PLAN.md` §9 added** — four pre-registered follow-up test cases in
  the document's own `Field | Value` / "Failure mode" convention (§5): gene-panel
  expansion, ablation displacement-metric fix + re-run, ablation-1 sign-flip
  disclosure, mechanism-regression validation.

- **`docs/GENERALIZATION_PLAN.md` and `docs/ORTHOGONAL_VALIDATION_PLAN.md`**
  given dated status headers confirming their self-reported status is accurate
  (generalization: code scaffolded in `src/generalization.py`, never run against
  real data; orthogonal validation: planning-only, Palantir trajectory ablation
  — `results/ablations/09_palantir/`— is the one already-complete exception).

### Follow-on, same day: re-templated to Chimdi's exact conventions, made executable

The first pass above documented findings but used the wrong template for half of
them and left nothing runnable. Corrected:

- **`ANALYSIS_PLAN.md` §9 re-templated.** Follow-ups 2 and 3 are ablation-grid
  work, not experiment specs — converted to the §6 *Ablation* field set (What
  changes / Why it matters / Compare / Strengthens if / Weakens if / Output
  files) instead of the §5 *Experiment* fields they'd been given. Follow-ups 1
  and 4 stay as experiments but are now completed to the full §5 field set
  (Input, Primary output, Plots, Tables, Code module added — previously only
  Purpose/Method/Failure mode).
- **`ANALYSIS_PLAN.md` §7 (Threat-to-Validity) extended** with four rows this
  review surfaced: ablation coverage gap and cell-type composition sensitivity
  and unvalidated mechanism regression (internal validity); replication
  gene-panel restriction (external validity). Item 6 of "What this study can
  claim" caveated — displacement robustness is only genuinely re-tested by half
  the ablation grid, not all of it as originally stated.
- **`ANALYSIS_PLAN.md` §8 status bullets refreshed.** 8.1–8.3 said "Code
  implemented, not yet run"; all three have been run — now point at their real
  `results/v3/` outputs instead.
- **`RUNBOOK.md` given Steps 13–16**, one per follow-up, with real runnable
  code and Checkpoints/Troubleshooting rows — the follow-ups are now
  executable procedures, not just specifications. Also fixed `RUNBOOK.md`'s
  stale Prerequisites block, which hardcoded the original author's personal
  environment (`~/.venvs/lesegenv`, `/deltos/e/lesion_phes/...`).
- **`TABLE_PLAN.md` / `FIGURE_PLAN.md`** register the new expected outputs:
  an expanded-panel replication table, and a note that Figure 6 / Table S6's
  displacement column is currently constant by construction (the ablation
  coverage gap above) and will change once Follow-up 2 runs.
- **`PROJECT_STATUS.md` / `TODO.md` cross-references added**, pointing each
  `ANALYSIS_PLAN.md` §9 Follow-up at its new `RUNBOOK.md` step (1→13, 2→14,
  3→15, 4→16) so a reader lands on the executable procedure, not just the spec.
- **`RUNBOOK.md` checkpoint 8 corrected — it asserted the opposite of the
  paper's central finding.** It read "Displacement test significant with
  reasonable effect size," but a *non-significant* displacement test
  (`p = 1.0`, `r = 0.14` opposite to the hypothesized direction) alongside
  *significant* dispersion is the correct, expected result — that contrast is
  precisely what discriminates the dispersion model from coherent displacement
  (`paper_v3.tex`, Results §"Two competing models"). As written, anyone
  following the runbook would have read the study's key result as a pipeline
  failure. Corrected, with an explanatory note added beneath the Checkpoints
  table. This is a leftover from the pre-v3 "robustness collapse" framing,
  when displacement *was* the hypothesis.

---

## 2026-08-24 — Reproducibility harness (`pierce/repro-harness`, commit `4e86330`)

Prior work on a separate branch, not part of this branch's diff — listed here
for a complete audit trail. Pushed to `piercetaylor/alveolar-dispersion-covid19`;
CI verified green on GitHub Actions (53 passed, 0 skipped, including Harmony
batch correction, which Linux CI can build but this Windows dev machine cannot).

- Added a synthetic-data pytest suite (`tests/`, 12 files) — a deterministic
  fixture built from `config.yaml`'s own gene lists, plus an end-to-end smoke
  test of the real `scripts/run_pipeline.py` step functions.
- Added `.github/workflows/tests.yml` (GitHub Actions CI).
- Fixed two real bugs the test suite surfaced:
  - `src/qc.py` read `qc.get("max_pct_mt")`, a key that never matched
    `config.yaml`'s `max_pct_mito` — the mitochondrial-fraction QC filter had
    silently never applied on any prior run. (Verified to have zero effect on
    the currently-committed primary-cohort results: max `pct_counts_mt` in
    that data was 7.02%, under the 20% threshold either way — see
    `results/tables/tableS2_qc_{prefilter,postfilter}.csv`, byte-identical.)
  - `config.yaml`'s `feature_selection.method: "seurat_v3"` requires
    `scikit-misc`, never listed in `requirements.txt` — added.
- Added `requirements.lock.txt` (pinned dependency snapshot) and fixed
  `Makefile`'s hardcoded personal venv path (`~/.venvs/lesegenv` →
  project-local `.venv`, all targets routed through the venv's interpreter).
- Added `src/provenance.py` — every `scripts/run_pipeline.py` run now stamps a
  JSON snapshot (git commit, package versions, seed, platform) to
  `results/provenance/`. Added `results/PROVENANCE_NOTE.md` disclaiming that
  results already committed to the repo predate this system and have no
  retroactive provenance trail.
