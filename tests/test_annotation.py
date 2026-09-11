from src.annotation import validate_markers, subset_alveolar


def test_validate_markers_returns_expected_columns(synthetic_atlas, real_cfg):
    df = validate_markers(
        synthetic_atlas, real_cfg["markers"], real_cfg["cell_types"]["annotation_column"]
    )
    assert set(df.columns) == {
        "expected_type",
        "marker",
        "annotated_type",
        "mean_expression",
        "pct_expressing",
    }
    assert len(df) > 0
    # AT2 markers should score higher in AT2 cells than any other type.
    at2_rows = df[(df["expected_type"] == "AT2") & (df["marker"] == "SFTPC")]
    at2_in_at2 = at2_rows.loc[at2_rows["annotated_type"] == "AT2", "mean_expression"].iloc[0]
    at2_in_at1 = at2_rows.loc[at2_rows["annotated_type"] == "AT1", "mean_expression"].iloc[0]
    assert at2_in_at2 > at2_in_at1


def test_validate_markers_handles_missing_genes(synthetic_atlas, real_cfg):
    markers = {"fake_type": ["NOT_A_REAL_GENE"]}
    df = validate_markers(synthetic_atlas, markers, real_cfg["cell_types"]["annotation_column"])
    assert df.empty


def test_subset_alveolar_selects_only_primary_focus_types(synthetic_atlas, real_cfg):
    subset = subset_alveolar(synthetic_atlas, real_cfg)
    target_types = set(real_cfg["cell_types"]["primary_focus"])
    assert set(subset.obs["cell_type_fine"].unique()) <= target_types
    expected_n = synthetic_atlas.obs["cell_type_fine"].isin(target_types).sum()
    assert subset.n_obs == expected_n
