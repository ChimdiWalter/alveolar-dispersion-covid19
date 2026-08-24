import copy
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import load_config  # noqa: E402
from tests._synthetic import make_synthetic_atlas  # noqa: E402


@pytest.fixture
def real_cfg():
    """The actual project config.yaml, unmodified."""
    return load_config()


@pytest.fixture
def test_cfg(tmp_path, real_cfg):
    """A scaled-down copy of the real config for fast tests on synthetic data.

    Only overrides what's needed for speed/size and to route all outputs
    into a pytest tmp_path so tests never touch the repo's real data/results
    directories. Everything else (column names, labels, gene programs,
    markers) is the real schema.
    """
    cfg = copy.deepcopy(real_cfg)

    cfg["feature_selection"]["n_top_genes"] = 60
    cfg["dimred"]["n_pcs"] = 10
    cfg["dimred"]["n_neighbors"] = 30
    cfg["dimred"]["diffmap"]["n_comps"] = 10
    cfg["statistics"]["permutation_n"] = 200

    # harmonypy isn't installable on this machine (no C++ toolchain); tests
    # that specifically exercise run_harmony override this back to "harmony".
    cfg["batch_correction"]["method"] = "none"

    cfg["paths"] = {
        "raw_data": str(tmp_path / "data" / "raw"),
        "processed_data": str(tmp_path / "data" / "processed"),
        "metadata": str(tmp_path / "metadata"),
        "results": str(tmp_path / "results"),
        "figures": str(tmp_path / "results" / "figures"),
        "tables": str(tmp_path / "results" / "tables"),
        "intermediate": str(tmp_path / "results" / "intermediate"),
        "manuscript_figures": str(tmp_path / "manuscript_figures"),
        "logs": str(tmp_path / "logs"),
    }
    return cfg


@pytest.fixture
def synthetic_atlas(real_cfg):
    """A small, deterministic AnnData mimicking the SCP1219 schema."""
    return make_synthetic_atlas(seed=42, cfg=real_cfg)
