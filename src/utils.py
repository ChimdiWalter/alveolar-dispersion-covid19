"""
Shared configuration loader and utility functions.
"""

from pathlib import Path
import yaml
import logging
import sys

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config(path: str | Path | None = None) -> dict:
    """Load the project YAML configuration file.

    Parameters
    ----------
    path : str or Path, optional
        Path to config.yaml. Defaults to PROJECT_ROOT / "config.yaml".

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """
    if path is None:
        path = PROJECT_ROOT / "config.yaml"
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path) as f:
        cfg = yaml.safe_load(f)
    return cfg


def setup_logging(name: str = "robustness", level: int = logging.INFO) -> logging.Logger:
    """Create a consistently formatted logger.

    Parameters
    ----------
    name : str
        Logger name.
    level : int
        Logging level.

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter(
            "[%(asctime)s] %(name)s — %(levelname)s — %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def ensure_dirs(cfg: dict) -> None:
    """Create all output directories listed in the config if they don't exist."""
    for key in ("results", "figures", "tables", "intermediate", "processed_data", "logs"):
        p = cfg.get("paths", {}).get(key)
        if p:
            (PROJECT_ROOT / p).mkdir(parents=True, exist_ok=True)


def resolve_path(relative: str) -> Path:
    """Resolve a config-relative path to an absolute path."""
    return PROJECT_ROOT / relative
