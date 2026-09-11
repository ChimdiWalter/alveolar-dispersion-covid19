import pytest

from src.embedding import normalize_and_select_hvg, run_pca, run_neighbors, run_diffmap
from src.trajectory import (
    find_root_cell,
    run_dpt,
    pseudotime_density_by_condition,
    pseudotime_by_donor,
)


@pytest.fixture
def embedded(synthetic_atlas, test_cfg):
    adata = normalize_and_select_hvg(synthetic_atlas.copy(), test_cfg)
    adata = run_pca(adata, test_cfg)
    adata = run_neighbors(adata, test_cfg)
    adata = run_diffmap(adata, test_cfg)
    return adata


@pytest.mark.parametrize(
    "strategy", ["healthy_AT2_centroid", "healthy_AT1_centroid", "random_healthy", "covid_extreme"]
)
def test_find_root_cell_all_strategies_return_valid_index(embedded, test_cfg, strategy):
    root = find_root_cell(embedded, test_cfg, strategy=strategy)
    assert isinstance(root, int)
    assert 0 <= root < embedded.n_obs


def test_find_root_cell_healthy_strategies_pick_a_healthy_cell(embedded, test_cfg):
    healthy_label = test_cfg["conditions"]["healthy_label"]
    condition_col = test_cfg["conditions"]["condition_column"]
    root = find_root_cell(embedded, test_cfg, strategy="healthy_AT2_centroid")
    assert embedded.obs[condition_col].iloc[root] == healthy_label


def test_find_root_cell_unknown_strategy_raises(embedded, test_cfg):
    with pytest.raises(ValueError):
        find_root_cell(embedded, test_cfg, strategy="not_a_real_strategy")


def test_run_dpt_adds_pseudotime(embedded, test_cfg):
    out = run_dpt(embedded, test_cfg)
    assert "dpt_pseudotime" in out.obs.columns
    assert "iroot" in out.uns
    assert out.obs["dpt_pseudotime"].notna().all()
    assert (out.obs["dpt_pseudotime"] >= 0).all()


def test_pseudotime_density_by_condition(embedded, test_cfg):
    out = run_dpt(embedded, test_cfg)
    density = pseudotime_density_by_condition(out, test_cfg)
    assert set(density["condition"]) == {"Control", "COVID-19"}
    assert (density["n_cells"] > 0).all()
    for col in ("mean_pseudotime", "median_pseudotime", "std_pseudotime"):
        assert col in density.columns


def test_pseudotime_by_donor(embedded, test_cfg):
    out = run_dpt(embedded, test_cfg)
    donor_df = pseudotime_by_donor(out, test_cfg)
    assert len(donor_df) == out.obs["donor_id"].nunique()
    assert set(donor_df["condition"]) <= {"Control", "COVID-19"}
