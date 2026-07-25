#!/usr/bin/env python3
"""Fetch an independent COVID-19 lung AT1/AT2 replication cohort from the
cellxgene census (HLCA extended + Krasnow COVID infection), strictly excluding
the Melms (SCP1219) dataset that the primary analysis uses.

Rationale:
  * Delorey (GSE171524) and Wendisch (PRJNA705687) are not on cellxgene census
    and a raw GEO download is expensive; the HLCA extended is a harmonized
    multi-study atlas that contains COVID-19 lung nuclei from independent
    upstream studies (Bharat, Delorey-integrated portions, Melms-integrated,
    etc.). We drop the Melms contribution so replication is genuinely out-of-
    sample.
  * We restrict var-axis to the gene-program genes plus canonical markers to
    keep the download compact (<1 GB).
"""
import sys
import logging
from pathlib import Path
import yaml
import anndata as ad
import cellxgene_census as cc

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("replication.fetch")

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())

MELMS_DATASET_ID = "d8da613f-e681-4c69-b463-e94f5e66847f"

# --- Gene shortlist ---------------------------------------------------------
program_genes = set()
for spec in CFG["gene_programs"].values():
    program_genes.update(spec["genes"])
marker_extras = {
    "SFTPC", "SFTPA1", "SFTPB", "ABCA3",       # AT2
    "AGER", "HOPX", "PDPN", "CAV1", "RTKN2",   # AT1
    "KRT8", "KRT18", "CLDN4", "SFN", "LGALS3", # transitional / DATP
    "MKI67", "TOP2A",                           # proliferation
    "ACE2", "TMPRSS2",                          # SARS-CoV-2 entry
}
gene_shortlist = sorted(program_genes | marker_extras)
log.info("gene shortlist: %d genes", len(gene_shortlist))

# --- Cell query: AT1/AT2 + DATP-adjacent, lung, human ----------------------
CT = (
    "cell_type == 'pulmonary alveolar type 1 cell' or "
    "cell_type == 'pulmonary alveolar type 2 cell'"
)
DISEASES = ["COVID-19", "normal"]

OUT = ROOT / "data/replication/replication_alveolar.h5ad"
OUT.parent.mkdir(parents=True, exist_ok=True)

pieces = []
with cc.open_soma(census_version="2025-11-08") as census:
    for dz in DISEASES:
        flt = (
            f"tissue_general == 'lung' and disease == '{dz}' and "
            f"dataset_id != '{MELMS_DATASET_ID}' and ({CT})"
        )
        log.info("fetching disease=%s ...", dz)
        a = cc.get_anndata(
            census,
            organism="Homo sapiens",
            obs_value_filter=flt,
            var_value_filter="feature_name in " + repr(gene_shortlist),
            column_names={
                "obs": [
                    "soma_joinid", "dataset_id", "donor_id", "cell_type",
                    "disease", "tissue", "sex", "self_reported_ethnicity",
                    "assay", "development_stage",
                ],
                "var": ["feature_name"],
            },
        )
        # Use gene symbol as var_names for convenience
        a.var_names = a.var["feature_name"].astype(str).values
        a.obs["condition"] = dz
        log.info("  %s: %d cells, %d genes", dz, a.n_obs, a.n_vars)
        pieces.append(a)

adata = ad.concat(pieces, axis=0, merge="same", uns_merge="same")
adata.obs_names_make_unique()
log.info("concatenated: %s", adata.shape)
log.info("datasets represented: %d", adata.obs["dataset_id"].nunique())
log.info("donors represented: %d", adata.obs["donor_id"].nunique())
log.info("writing %s", OUT)
adata.write_h5ad(OUT, compression="gzip")
log.info("done")
