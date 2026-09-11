import json

from src.provenance import capture_provenance, save_provenance


def test_capture_provenance_structure(test_cfg):
    record = capture_provenance(test_cfg, step="test")

    assert record["step"] == "test"
    assert record["random_seed"] == test_cfg["random_seed"]
    assert record["dataset"] == test_cfg["project"]["dataset"]

    assert "commit" in record["git"]
    commit = record["git"]["commit"]
    # Either a real 40-char SHA (when run inside the git repo) or None
    # (git unavailable) — never a truncated/garbled value.
    assert commit is None or len(commit) == 40

    versions = record["package_versions"]
    assert "scanpy" in versions
    assert versions["scanpy"] is not None
    assert "numpy" in versions
    assert versions["numpy"] is not None


def test_capture_provenance_missing_package_is_none(test_cfg):
    record = capture_provenance(test_cfg, step="test")
    # harmonypy is not installed in this test environment (see
    # tests/test_embedding.py); confirm the missing-package path returns
    # None rather than raising or omitting the key entirely.
    assert "harmonypy" in record["package_versions"]
    assert record["package_versions"]["harmonypy"] is None or isinstance(
        record["package_versions"]["harmonypy"], str
    )


def test_save_provenance_writes_json(test_cfg):
    path = save_provenance(test_cfg, step="test")

    assert path.exists()
    assert path.parent.name == "provenance"

    data = json.loads(path.read_text())
    assert data["step"] == "test"
    assert data["random_seed"] == test_cfg["random_seed"]
