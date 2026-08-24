"""
End-to-end smoke test: runs scripts/run_pipeline.py's real step functions,
in sequence, on the synthetic atlas — the actual reproducibility harness
this test suite exists to provide. Never touches the repo's real
data/results directories (test_cfg routes everything into tmp_path).

Harmony batch correction is not exercised (harmonypy isn't installable on
this Windows test machine without a C++ toolchain) — test_cfg sets
batch_correction.method to "none" so step_embed takes the uncorrected path.
The figures step is not exercised (matplotlib isn't installed here).
"""

import logging

from scripts.run_pipeline import (
    step_qc,
    step_subset,
    step_embed,
    step_trajectory,
    step_programs,
    step_stats,
)

_logger = logging.getLogger("test.pipeline_smoke")


def test_full_pipeline_runs_end_to_end_on_synthetic_atlas(synthetic_atlas, test_cfg):
    adata = step_qc(synthetic_atlas.copy(), test_cfg, _logger)
    assert adata.n_obs > 0
    assert "pct_counts_mt" in adata.obs.columns

    alv = step_subset(adata, test_cfg, _logger)
    assert alv.n_obs > 0
    target_types = set(test_cfg["cell_types"]["primary_focus"])
    assert set(alv.obs["cell_type_fine"].unique()) <= target_types

    alv = step_embed(alv, test_cfg, _logger)
    assert "X_pca" in alv.obsm
    assert "X_umap" in alv.obsm
    assert "X_diffmap" in alv.obsm
    assert "X_pca_harmony" not in alv.obsm  # harmony disabled in test_cfg

    alv = step_trajectory(alv, test_cfg, _logger)
    assert "dpt_pseudotime" in alv.obs.columns

    alv, trends = step_programs(alv, test_cfg, _logger)
    for name in test_cfg["gene_programs"]:
        assert f"program_{name}" in alv.obs.columns
    assert len(trends) > 0

    disp_result, var_result, perm_result, composite = step_stats(alv, test_cfg, _logger)
    assert "p_value" in disp_result
    assert "p_value" in var_result
    assert "p_value" in perm_result
    assert composite["assessment"] in ("strong", "moderate", "weak", "not supported")

    # Output tables should actually have been written to tmp_path, not the
    # real repo results/ directory.
    from pathlib import Path

    tables_dir = Path(test_cfg["paths"]["tables"])
    assert (tables_dir / "table2_robustness_metrics.csv").exists()
    assert (tables_dir / "table3_composite_evidence.csv").exists()
    assert (tables_dir / "tableS3_marker_validation.csv").exists()
