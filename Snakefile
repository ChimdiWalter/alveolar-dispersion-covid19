# Snakemake workflow for alveolar robustness collapse pipeline
# Usage:
#   snakemake -j4                   # run everything with 4 cores
#   snakemake -j4 all_ablations     # run ablations only
#   snakemake -n                    # dry-run (show DAG)

import os
from pathlib import Path

configfile: "config.yaml"

PROCESSED = Path(config["paths"]["processed_data"])
RESULTS   = Path(config["paths"]["results"])
TABLES    = Path(config["paths"]["tables"])
FIGURES   = Path(config["paths"]["figures"])
ABL_DIR   = RESULTS / "ablations"

ABLATIONS = [
    "01_at2_only", "02_embedding_umap", "02_embedding_diffmap",
    "03_batch_corrected", "03_batch_uncorrected",
    "04_no_apoptosis_genes",
    "05_root_healthy_AT2_centroid", "05_root_healthy_AT1_centroid",
    "05_root_random_healthy", "05_root_covid_extreme",
    "06_broader_epithelial", "07_leave_one_donor_out",
    "08_alt_programs_msigdb_only", "08_alt_programs_curated_only",
    "09_palantir", "10_permutation_controls",
]

rule all:
    input:
        PROCESSED / "alveolar_programs.h5ad",
        RESULTS / "table2_robustness_metrics.csv",
        FIGURES / "fig1a_condition.png",
        FIGURES / "fig2_pseudotime.png",
        FIGURES / "fig3_program_dynamics.png",
        ABL_DIR / "tableS6_ablation_summary.csv",

rule qc:
    input: "config.yaml"
    output: PROCESSED / "atlas_qc.h5ad"
    shell: "python scripts/run_pipeline.py --step qc"

rule subset:
    input: PROCESSED / "atlas_qc.h5ad"
    output: PROCESSED / "alveolar_validated.h5ad"
    shell: "python scripts/run_pipeline.py --step subset"

rule embed:
    input: PROCESSED / "alveolar_validated.h5ad"
    output: PROCESSED / "alveolar_embedded.h5ad"
    shell: "python scripts/run_pipeline.py --step embed"

rule trajectory:
    input: PROCESSED / "alveolar_embedded.h5ad"
    output: PROCESSED / "alveolar_pseudotime.h5ad"
    shell: "python scripts/run_pipeline.py --step trajectory"

rule programs:
    input: PROCESSED / "alveolar_pseudotime.h5ad"
    output: PROCESSED / "alveolar_programs.h5ad"
    shell: "python scripts/run_pipeline.py --step programs"

rule stats:
    input: PROCESSED / "alveolar_programs.h5ad"
    output: RESULTS / "table2_robustness_metrics.csv"
    shell: "python scripts/run_pipeline.py --step stats"

rule figures:
    input: PROCESSED / "alveolar_programs.h5ad"
    output:
        FIGURES / "fig1a_condition.png",
        FIGURES / "fig2_pseudotime.png",
        FIGURES / "fig3_program_dynamics.png",
    shell: "python scripts/run_pipeline.py --step figures"

rule ablation:
    input: PROCESSED / "alveolar_validated.h5ad"
    output: ABL_DIR / "{ablation}" / "metrics.json"
    params:
        script = lambda w: f"scripts/ablations/ablation_{w.ablation.split('_')[0]}_{'_'.join(w.ablation.split('_')[1:]) or 'all'}.py"
    shell: "python {params.script}"

rule all_ablations:
    input: expand(ABL_DIR / "{abl}" / "metrics.json", abl=ABLATIONS)
    output: ABL_DIR / "tableS6_ablation_summary.csv"
    shell: "python scripts/ablations/run_all_ablations.py"
