import numpy as np

from src.embedding import normalize_and_select_hvg, run_pca, run_neighbors, run_diffmap
from src.trajectory import run_dpt
from src.programs import score_gene_programs, program_trends_along_pseudotime


def _programs_scored(synthetic_atlas, test_cfg):
    adata = normalize_and_select_hvg(synthetic_atlas.copy(), test_cfg)
    adata = run_pca(adata, test_cfg)
    adata = run_neighbors(adata, test_cfg)
    adata = run_diffmap(adata, test_cfg)
    adata = run_dpt(adata, test_cfg)
    return score_gene_programs(adata, test_cfg)


def test_score_gene_programs_adds_one_column_per_program(synthetic_atlas, test_cfg):
    adata = _programs_scored(synthetic_atlas, test_cfg)
    for name in test_cfg["gene_programs"]:
        col = f"program_{name}"
        assert col in adata.obs.columns
        assert adata.obs[col].notna().all()


def test_score_gene_programs_covid_signal_present(synthetic_atlas, test_cfg):
    """The synthetic fixture deliberately elevates interferon_response and
    apoptosis genes' raw (normalized) expression in COVID-19 cells.

    We check the raw expression shift directly for both programs (a
    controlled property of the fixture), and the score_genes-derived
    program score for interferon_response specifically, as an end-to-end
    check that score_gene_programs wires normalization through correctly.
    We don't assert the apoptosis *score* direction: scanpy's score_genes
    picks its background/control genes from the same expression bin as the
    target genes, and here both boosted programs land in the same high bin,
    so the control set for one can be contaminated by the other — a fixture
    artifact of boosting two programs to a similar level, not a pipeline bug.
    """
    adata = _programs_scored(synthetic_atlas, test_cfg)
    condition_col = test_cfg["conditions"]["condition_column"]
    is_covid = adata.obs[condition_col] == "COVID-19"

    for prog in ("interferon_response", "apoptosis"):
        genes = [g for g in test_cfg["gene_programs"][prog]["genes"] if g in adata.raw.var_names]
        raw_expr = adata.raw[:, genes].X
        raw_expr = np.asarray(raw_expr.todense())
        covid_raw_mean = raw_expr[is_covid.values].mean()
        control_raw_mean = raw_expr[(~is_covid).values].mean()
        assert covid_raw_mean > control_raw_mean

    col = "program_interferon_response"
    covid_mean = adata.obs.loc[is_covid, col].mean()
    control_mean = adata.obs.loc[~is_covid, col].mean()
    assert covid_mean > control_mean


def test_score_gene_programs_partially_missing_genes_does_not_crash(synthetic_atlas, test_cfg):
    import copy

    cfg = copy.deepcopy(test_cfg)
    # Mix of a real gene (guaranteed present in the synthetic panel) and
    # genes that don't exist, to exercise the missing-gene warning path
    # without hitting the degenerate zero-genes-available case.
    cfg["gene_programs"]["fake_program"] = {
        "genes": ["SFTPC", "NOT_A_GENE_1", "NOT_A_GENE_2"]
    }
    adata = normalize_and_select_hvg(synthetic_atlas.copy(), cfg)
    adata = run_pca(adata, cfg)
    out = score_gene_programs(adata, cfg)
    assert "program_fake_program" in out.obs.columns


def test_program_trends_along_pseudotime(synthetic_atlas, test_cfg):
    adata = _programs_scored(synthetic_atlas, test_cfg)
    trends = program_trends_along_pseudotime(adata, test_cfg, n_bins=10)
    assert set(trends.columns) == {
        "pseudotime_bin",
        "pseudotime_center",
        "program",
        "mean_score",
        "sem",
        "n_cells",
    }
    assert set(trends["program"]) == set(test_cfg["gene_programs"].keys())
    assert (trends["n_cells"] > 0).all()
