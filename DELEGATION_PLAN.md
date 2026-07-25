asles

### ROLE A — Computational Lead (you)
**Owns:** primary pipeline, existing codebase, integration, final manuscript assembly
**Skills needed:** Python, scanpy, single-cell analysis, statistics

### ROLE B — Computational Scientist #2
**Owns:** independent replication cohorts (Delorey + Adams)
**Skills needed:** Python, scanpy/anndata, GEO data download, basic single-cell pipeline
**Deliverables are self-contained:** download data, run existing pipeline, return metrics JSON

### ROLE C — Computational Scientist #3
**Owns:** cross-species (Strunz mouse) + RNA velocity
**Skills needed:** Python, scVelo, ortholog mapping, mouse scRNA-seq
**Deliverables are self-contained:** different species = no merge conflicts

### ROLE D — Biologist #1 (lung biology / pathology focus)
**Owns:** biological interpretation, gene program validation, clinical context, spatial data search
**Skills needed:** lung biology, alveolar cell biology, literature expertise, writing

### ROLE E — Biologist #2 (writing / figures / review)
**Owns:** manuscript writing (Intro, Discussion), figure design, journal formatting, bibliography
**Skills needed:** scientific writing, figure layout, LaTeX or Word, literature synthesis

---

## Phase 1: Parallel Foundation (Weeks 1-2)

All five roles work simultaneously. No dependencies between roles in this phase.

### ROLE A — Computational Lead (you)
| Task | Deliverable | Time | Deadline |
|------|-------------|------|----------|
| Implement cell-level mixed-effects models | `results/v3/mixed_effects_cell_level.json` | 4-6h | Day 3 |
| `pseudotime ~ condition + (1\|donor_id)` using statsmodels MixedLM | p-value, coefficient, ICC | | |
| `dispersion ~ condition + (1\|donor_id)` | Same format | | |
| Train transitional-state classifier (logistic regression, 84 genes) | `results/v3/classifier_transfer.json` + AUC curves | 4-6h | Day 5 |
| Apply classifier to cellxgene replication cohort | Cross-cohort AUC, precision-recall | | |
| Update `src/donor_models.py` with MixedLM function | Committed code | | Day 3 |

**Handoff to Role B:** Provide `config.yaml`, `src/` modules, `scripts/run_pipeline.py` with instructions.
**Handoff to Role C:** Provide `config.yaml`, 8 gene program definitions, expected output format.

### ROLE B — Computational Scientist #2
| Task | Deliverable | Time | Deadline |
|------|-------------|------|----------|
| Download Delorey 2021 from GEO (GSE171524) | `data/external/delorey/` h5ad file | 3-4h | Day 4 |
| QC + subset to alveolar AT1/AT2/transitional | `data/external/delorey/alveolar.h5ad` | 2-3h | Day 5 |
| Downloada Adams 2020 IPF from GEO (GSE136831) | `data/external/adams/` h5ad file | 3-4h | Day 4 |
| QC + subset to alveolar AT1/AT2 | `data/external/adams/alveolar.h5ad` | 2-3h | Day 5 |

**Instructions for Role B:**
```
# For each dataset:
1. Download raw count matrix from GEO
2. Load into anndata
3. Identify the cell-type annotation column
4. Subset to AT1/AT2/transitional cells (look for labels like:
   "AT1", "AT2", "alveolar type 1", "alveolar type 2",
   "KRT8+", "transitional", "aberrant basaloid")
5. Add harmonized columns:
   - adata.obs["condition_harmonized"] = "Disease" or "Control"
   - adata.obs["donor_id_harmonized"] = "<dataset>_" + donor_id
6. Save as .h5ad with gzip compression
7. Report: n_cells per condition, n_donors per condition, 
   available genes overlap with our 84-gene panel
```

### ROLE C — Computational Scientist #3
| Task | Deliverable | Time | Deadline |
|------|-------------|------|----------|
| Download Strunz 2020 from GEO (GSE141259) | `data/external/strunz/` h5ad file | 3-4h | Day 4 |
| Build mouse→human ortholog mapping table | `metadata/mouse_human_orthologs.csv` | 2-3h | Day 5 |
| QC + subset to alveolar epithelial | `data/external/strunz/alveolar.h5ad` | 2-3h | Day 6 |
| Check SCP1219 for BAM/loom files (RNA velocity) | Report: available or not | 1h | Day 3 |

**Instructions for ortholog mapping:**
```
# Use biomart or NCBI homologene:
import pybiomart
# Map: Sftpc→SFTPC, Krt8→KRT8, Ager→AGER, Hopx→HOPX, etc.
# Most AT1/AT2/stress genes have 1:1 orthologs
# Output: CSV with columns [mouse_gene, human_gene, confidence]
# Flag any program genes that lack 1:1 orthologs
```

### ROLE D — Biologist #1
| Task | Deliverable | Time | Deadline |
|------|-------------|------|----------|
| Validate 8 gene programs against current literature | `docs/GENE_PROGRAM_VALIDATION.md` | 6-8h | Day 7 |
| Search for publicly available spatial transcriptomics COVID lung data | `docs/SPATIAL_DATA_SEARCH.md` | 4h | Day 5 |
| Mine SCP1219 metadata for clinical variables (ventilator days, viral load, DAD grade) | Report: what's available | 2h | Day 3 |
| Review Strunz 2020 paper for lineage tracing details relevant to our framework | 1-page summary | 2h | Day 5 |
| Identify which transitional-cell markers are validated at protein level (IHC/IF) | Table of marker validation status | 3h | Day 7 |

**Gene program validation checklist:**
```
For each of the 8 programs (AT2_identity, AT1_identity, interferon_response,
nfkb_inflammatory, oxidative_stress, AT2_to_AT1_differentiation, apoptosis,
senescence):

1. Are all genes still considered canonical members? (check 2024-2025 reviews)
2. Are any important genes MISSING that recent literature added?
3. Are any genes controversial or context-dependent?
4. What is the overlap with MSigDB Hallmark sets? (we already know this
   matters — Ablation 8 showed MSigDB inverts ordering)
5. Would a reviewer with lung biology expertise challenge any gene choice?

Deliver as a table:
| Program | Gene | Status | Evidence | Notes |
```

### ROLE E — Biologist #2 (Writing)
| Task | Deliverable | Time | Deadline |
|------|-------------|------|----------|
| Draft expanded Introduction (biological context for Nature audience) | `manuscript/intro_nature_draft.md` | 8h | Day 7 |
| Draft Discussion section: cross-disease generalization framing | `manuscript/discussion_nature_draft.md` | 8h | Day 10 |
| Build proper .bib bibliography from current hand-written references | `manuscript/references.bib` | 3h | Day 5 |
| Design figure layout for 7 main figures + 10 Extended Data | `manuscript/FIGURE_LAYOUT_NATURE.md` | 4h | Day 7 |

**Writing brief for Nature audience:**
```
Key framing shifts from paper_v3:
- Lead with the QUESTION (how does the alveolar epithelium fail?) not the method
- "Loss of state coherence" is the concept; ablation-first framework is how you prove it
- The negative result (centroid displacement fails) must be in paragraph 1 of Results
- Cross-disease generalization (IPF, mouse bleomycin) is what makes this not
  "just a COVID paper"
- The DATP retraction becomes a positive story: "we discovered that marker 
  thresholds don't transfer, but geometric signatures do"
- Word limit: ~3000 words main text (Nature), unlimited Methods
```

---

## Phase 2: Pipeline Runs (Weeks 2-3)

Dependencies from Phase 1 must be complete before these start.

### ROLE A — Computational Lead
| Task | Depends on | Deliverable | Time | Deadline |
|------|-----------|-------------|------|----------|
| Run full pipeline on Delorey data | Role B Delorey h5ad | `results/delorey/` full 3-test battery | 6-8h | Day 14 |
| Run full pipeline on Adams IPF data | Role B Adams h5ad | `results/adams/` full 3-test battery | 6-8h | Day 16 |
| Run ablation grid on Delorey | Delorey pipeline complete | `results/delorey/ablations/` | 4-6h | Day 17 |
| Build cross-cohort portability table | All pipelines complete | `results/portability_matrix.csv` | 2h | Day 18 |

### ROLE B — Computational Scientist #2
| Task | Depends on | Deliverable | Time | Deadline |
|------|-----------|-------------|------|----------|
| Score 8 gene programs on Delorey | Delorey alveolar.h5ad ready | Program scores in .obs | 2h | Day 8 |
| Score 8 gene programs on Adams | Adams alveolar.h5ad ready | Program scores in .obs | 2h | Day 8 |
| Run donor-level summary on both | Programs scored | `donor_summary.csv` per dataset | 2h | Day 9 |
| Donor-level MW + bootstrap CIs on both | Donor summary ready | `donor_level_tests.json` per dataset | 2h | Day 10 |

### ROLE C — Computational Scientist #3
| Task | Depends on | Deliverable | Time | Deadline |
|------|-----------|-------------|------|----------|
| Run full pipeline on Strunz mouse (per timepoint) | Strunz h5ad + orthologs ready | `results/strunz/` metrics per timepoint | 8-10h | Day 14 |
| Dispersion vs real time plot | Pipeline complete | `results/strunz/dispersion_vs_time.pdf` | 2h | Day 15 |
| Pseudotime shift vs real time plot | Pipeline complete | `results/strunz/pseudotime_vs_time.pdf` | 2h | Day 15 |
| Lineage-trace validation (if available) | Strunz data inspected | `results/strunz/lineage_validation.json` | 4h | Day 17 |
| RNA velocity on SCP1219 (if BAMs found) | BAM availability confirmed | `results/velocity/` | 6-8h | Day 17 |

### ROLE D — Biologist #1
| Task | Depends on | Deliverable | Time | Deadline |
|------|-----------|-------------|------|----------|
| Interpret Delorey dispersion results in clinical context | Delorey results ready | 1-page clinical interpretation | 3h | Day 16 |
| Interpret Adams IPF results: COVID vs fibrosis biology | Adams results ready | 1-page interpretation | 3h | Day 18 |
| Interpret Strunz time-series: what timepoints correspond to what biology | Strunz results ready | Timeline annotation figure | 4h | Day 18 |
| Write Methods: biological rationale for gene program choices | Gene validation done | Methods paragraph | 3h | Day 14 |

### ROLE E — Biologist #2 (Writing)
| Task | Depends on | Deliverable | Time | Deadline |
|------|-----------|-------------|------|----------|
| Draft Results: cross-disease comparison section | Delorey + Adams results | Results paragraphs | 6h | Day 19 |
| Draft Results: cross-species section | Strunz results | Results paragraphs | 4h | Day 20 |
| Design Figure 8: cross-cohort portability heatmap | Portability matrix | Figure sketch | 3h | Day 20 |
| Begin Extended Data figure assembly | All supplementary figures | ED Figures 1-10 | 6h | Day 21 |

---

## Phase 3: Integration + Manuscript Assembly (Weeks 3-4)

### ROLE A — Computational Lead
| Task | Deliverable | Deadline |
|------|-------------|----------|
| Integrate all results into unified paper_v4.tex | Complete manuscript LaTeX | Day 24 |
| Build final portability table (Table 2: 5 cohorts x 6 findings) | Table in paper | Day 22 |
| Generate all publication-quality figures | `results/figures/` PDFs | Day 23 |
| Run final reproducibility check (seed 42, all pipelines) | `logs/final_reproducibility.log` | Day 25 |

### ALL ROLES — Joint
| Task | Deliverable | Deadline |
|------|-------------|----------|
| Internal manuscript review (everyone reads full draft) | Comments | Day 26 |
| Address internal review comments | Revised draft | Day 28 |
| Final proofread + figure polish | Submission-ready PDF | Day 30 |

---

## Deliverable Format Standards

Everyone must use these formats so integration is seamless:

### Data files
```
# AnnData objects must have:
adata.obs["condition_harmonized"]  # "Disease" or "Control"
adata.obs["donor_id_harmonized"]   # "<dataset>_<original_donor_id>"
adata.obs["dataset_source"]        # e.g., "delorey_2021", "adams_2020"
# Program scores: adata.obs["score_<program_name>"]
# Save as: .h5ad with compression="gzip"
```

### Results JSON
```json
{
  "dataset": "delorey_2021",
  "n_cells": 12345,
  "n_donors_disease": 15,
  "n_donors_control": 10,
  "displacement": {"U": ..., "p": ..., "r": ...},
  "dispersion": {"levene_stat": ..., "levene_p": ..., "variance_ratio": ...},
  "pseudotime": {"observed_diff": ..., "perm_p": ..., "loo_direction": "X/X"},
  "donor_level": {"mw_p": ..., "bootstrap_ci": [..., ...]}
}
```

### Figures
```
- Vector format: PDF (for paper) + PNG 300dpi (for review)
- Color scheme: blue=healthy/control, red=COVID/disease, orange=IPF, green=mouse
- Font: 8pt minimum for Nature
- Panel labels: lowercase bold (a, b, c, d)
- Save to: results/figures/<dataset>/
```

---

## Communication Protocol

- **Weekly sync:** 30-min meeting, each role reports: done / blocked / next
- **Shared folder:** All deliverables go to `results/<dataset>/` or `manuscript/drafts/`
- **Blocking issues:** Flag within 24h on group chat, don't wait for weekly sync
- **Code review:** Role A reviews all computational code before integration

---

## Timeline Summary

```
Week 1  [May 7-14]   All roles in parallel: data download, mixed-effects,
                      gene validation, writing drafts, ortholog mapping
Week 2  [May 14-21]  Pipeline runs on 3 external datasets + RNA velocity
Week 3  [May 21-28]  Integration, cross-cohort table, manuscript assembly
Week 4  [May 28-Jun 4] Internal review, revision, submission prep
        [Jun 4]      TARGET: submission-ready manuscript
```

---

## Authorship Note

Suggested contribution mapping (CRediT taxonomy):
- **Role A:** Conceptualization, Methodology, Software, Formal Analysis, Writing-Original Draft
- **Role B:** Data Curation, Formal Analysis (Delorey + Adams replication)
- **Role C:** Data Curation, Formal Analysis (Strunz cross-species + velocity)
- **Role D:** Investigation, Validation, Writing-Review & Editing (biological interpretation)
- **Role E:** Visualization, Writing-Original Draft, Writing-Review & Editing
