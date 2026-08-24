import numpy as np
import pandas as pd
import pytest

from src.io import load_atlas, load_metadata, save_adata, save_table
from tests._scp1219_layout import write_scp1219_layout


def test_load_atlas_cached_h5ad(test_cfg, synthetic_atlas):
    raw_dir = test_cfg["paths"]["raw_data"]
    from pathlib import Path

    Path(raw_dir).mkdir(parents=True, exist_ok=True)
    synthetic_atlas.write_h5ad(Path(raw_dir) / "cached.h5ad")

    loaded = load_atlas(test_cfg)
    assert loaded.n_obs == synthetic_atlas.n_obs
    assert loaded.n_vars == synthetic_atlas.n_vars
    assert list(loaded.obs["cell_type_fine"]) == list(synthetic_atlas.obs["cell_type_fine"])


def test_load_atlas_native_scp1219_layout(test_cfg, synthetic_atlas):
    from pathlib import Path

    raw_dir = Path(test_cfg["paths"]["raw_data"])
    write_scp1219_layout(synthetic_atlas, raw_dir)

    loaded = load_atlas(test_cfg)

    assert loaded.n_obs == synthetic_atlas.n_obs
    assert loaded.n_vars == synthetic_atlas.n_vars
    assert list(loaded.var_names) == list(synthetic_atlas.var_names)
    assert list(loaded.obs_names) == list(synthetic_atlas.obs_names)

    # Counts should round-trip through the gzip mtx write/read exactly.
    orig = np.asarray(synthetic_atlas.X.todense())
    got = np.asarray(loaded.X.todense())
    np.testing.assert_allclose(orig, got)

    # Metadata (group/donor_id/cell_type_fine) must have joined onto obs.
    assert "cell_type_fine" in loaded.obs.columns
    assert "group" in loaded.obs.columns
    assert "donor_id" in loaded.obs.columns
    assert set(loaded.obs["group"].astype(str)) == {"Control", "COVID-19"}


def test_load_atlas_raises_when_nothing_found(test_cfg):
    from pathlib import Path

    Path(test_cfg["paths"]["raw_data"]).mkdir(parents=True, exist_ok=True)
    with pytest.raises(FileNotFoundError):
        load_atlas(test_cfg)


def test_load_metadata_missing_returns_empty(test_cfg):
    from pathlib import Path

    Path(test_cfg["paths"]["metadata"]).mkdir(parents=True, exist_ok=True)
    meta = load_metadata(test_cfg)
    assert meta.empty


def test_load_metadata_reads_csv(test_cfg):
    from pathlib import Path

    meta_dir = Path(test_cfg["paths"]["metadata"])
    meta_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({"id": ["a", "b"], "val": [1, 2]}).set_index("id")
    df.to_csv(meta_dir / "meta.csv")

    loaded = load_metadata(test_cfg)
    assert list(loaded.columns) == ["val"]
    assert list(loaded.index) == ["a", "b"]


def test_save_adata_and_reload(test_cfg, synthetic_atlas):
    path = save_adata(synthetic_atlas, "unit_test_adata", test_cfg)
    assert path.exists()

    import anndata as ad

    reloaded = ad.read_h5ad(path)
    assert reloaded.n_obs == synthetic_atlas.n_obs
    assert reloaded.n_vars == synthetic_atlas.n_vars


def test_save_table(test_cfg):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    path = save_table(df, "unit_test_table", cfg=test_cfg)
    assert path.exists()
    reloaded = pd.read_csv(path, index_col=0)
    assert list(reloaded["a"]) == [1, 2]
