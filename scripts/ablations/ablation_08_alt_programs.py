#!/usr/bin/env python3
"""Ablation 8: Alternative gene program definitions.

Compares MSigDB-only programs vs curated-only programs vs the primary
(merged) definitions. Tests whether ordering is driven by any one source.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (load_config, setup_logging, load_alveolar, run_workflow,
                    core_metrics, save_ablation_metrics)


# Hand-picked MSigDB-only subsets (no curated additions)
MSIGDB_ONLY = {
    "interferon_response": ["ISG15", "IFI6", "IFIT1", "MX1", "OAS1", "STAT1"],
    "nfkb_inflammatory": ["NFKB1", "RELA", "TNF", "IL6", "CXCL8", "ICAM1"],
    "oxidative_stress": ["SOD1", "SOD2", "GPX1", "CAT", "TXN", "PRDX1"],
    "apoptosis": ["BAX", "CASP3", "CASP9", "BCL2L11", "CYCS", "FAS"],
}

# Curated-only (lung-biology-specific) subsets
CURATED_ONLY = {
    "AT2_identity": ["SFTPC", "SFTPA1", "ABCA3", "LAMP3", "SLC34A2"],
    "AT1_identity": ["AGER", "PDPN", "HOPX", "CLIC5", "AKAP5"],
    "AT2_to_AT1_differentiation": ["KRT8", "CLDN4", "SFN", "KRT18", "LGALS3"],
}


def main():
    cfg = load_config()
    logger = setup_logging("ablation_08_alt_programs")

    for variant_name, program_dict in (("msigdb_only", MSIGDB_ONLY),
                                        ("curated_only", CURATED_ONLY)):
        logger.info(f"Variant: {variant_name}")
        cfg_v = {**cfg, "gene_programs": {
            k: {"genes": v, "source": variant_name}
            for k, v in program_dict.items()
        }}
        alv = load_alveolar(cfg_v)
        alv, trends = run_workflow(alv, cfg_v, logger)
        m = core_metrics(alv, cfg_v, trends_df=trends,
                         primary_ordering=list(cfg["gene_programs"].keys()))
        m["variant"] = variant_name
        save_ablation_metrics(f"08_alt_programs_{variant_name}", m, cfg)


if __name__ == "__main__":
    main()
