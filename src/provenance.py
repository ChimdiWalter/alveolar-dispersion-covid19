"""
Run provenance capture: git commit, dependency versions, config, and seed.

A committed results file is only independently verifiable if it's traceable
back to the exact code, dependency versions, and configuration that produced
it. Every pipeline invocation records a snapshot so future runs (unlike the
results already in this repo, which predate this module) carry that trail.
"""

import json
import logging
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version

logger = logging.getLogger("robustness.provenance")

# Packages whose exact version can materially affect numerical results —
# embedding/clustering/trajectory algorithms are version-sensitive
# independent of the fixed random seed.
_TRACKED_PACKAGES = [
    "numpy", "pandas", "scipy", "scikit-learn", "scanpy", "anndata",
    "leidenalg", "python-igraph", "statsmodels", "harmonypy",
    "scikit-misc", "umap-learn",
]


def _git_info() -> dict:
    from .utils import PROJECT_ROOT

    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=5, check=True,
        ).stdout.strip()
    except Exception as e:
        logger.warning(f"Could not determine git commit: {e}")
        return {"commit": None, "dirty": None}

    try:
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=5, check=True,
        ).stdout
        dirty = bool(status.strip())
    except Exception as e:
        logger.warning(f"Could not determine git working-tree status: {e}")
        dirty = None

    return {"commit": commit, "dirty": dirty}


def _package_versions() -> dict:
    versions = {}
    for pkg in _TRACKED_PACKAGES:
        try:
            versions[pkg] = version(pkg)
        except PackageNotFoundError:
            versions[pkg] = None
    return versions


def capture_provenance(cfg: dict, step: str = "all") -> dict:
    """Capture a snapshot of the environment and config used for a run.

    Parameters
    ----------
    cfg : dict
        Project config (records the random seed and dataset name).
    step : str
        Which pipeline step this snapshot corresponds to (e.g. "qc", "all").

    Returns
    -------
    dict
        JSON-serializable provenance record.
    """
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "step": step,
        "git": _git_info(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "random_seed": cfg.get("random_seed"),
        "dataset": cfg.get("project", {}).get("dataset"),
        "package_versions": _package_versions(),
    }


def save_provenance(cfg: dict, step: str = "all"):
    """Capture and save a provenance record to <results>/provenance/.

    Parameters
    ----------
    cfg : dict
    step : str

    Returns
    -------
    pathlib.Path
        Path to the saved JSON file.
    """
    from .utils import resolve_path

    record = capture_provenance(cfg, step=step)

    out_dir = resolve_path(cfg["paths"]["results"]) / "provenance"
    out_dir.mkdir(parents=True, exist_ok=True)

    stamp = record["timestamp_utc"].replace(":", "").replace("-", "").split(".")[0]
    path = out_dir / f"{step}_{stamp}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    logger.info(f"Provenance record saved -> {path}")
    return path
