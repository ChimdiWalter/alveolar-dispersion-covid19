from pathlib import Path

import pytest

from src.utils import load_config, ensure_dirs, resolve_path, PROJECT_ROOT


def test_load_config_default():
    cfg = load_config()
    assert cfg["project"]["dataset"] == "SCP1219"
    assert cfg["conditions"]["condition_column"] == "group"
    assert cfg["random_seed"] == 42


def test_load_config_explicit_path():
    cfg = load_config(PROJECT_ROOT / "config.yaml")
    assert cfg["cell_types"]["annotation_column"] == "cell_type_fine"


def test_load_config_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "does_not_exist.yaml")


def test_resolve_path_relative():
    p = resolve_path("data/raw")
    assert p == PROJECT_ROOT / "data" / "raw"


def test_ensure_dirs_creates_output_dirs(tmp_path):
    cfg = {
        "paths": {
            "results": str(tmp_path / "results"),
            "figures": str(tmp_path / "results" / "figures"),
            "tables": str(tmp_path / "results" / "tables"),
            "intermediate": str(tmp_path / "results" / "intermediate"),
            "processed_data": str(tmp_path / "data" / "processed"),
            "logs": str(tmp_path / "logs"),
        }
    }
    ensure_dirs(cfg)
    for key in ("results", "figures", "tables", "intermediate", "processed_data", "logs"):
        assert Path(cfg["paths"][key]).is_dir()
