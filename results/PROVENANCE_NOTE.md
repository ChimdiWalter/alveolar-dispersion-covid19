# Provenance note

The files elsewhere in `results/` as of the repository's initial commit
predate this project's provenance-tracking system (added 2026-08-24) and
were computed on an environment whose exact package versions and git commit
were not independently recorded at the time. `config.yaml` specifies
`random_seed: 42`, and `src/embedding.py` / `src/trajectory.py` /
`src/stats.py` all consume it, but no per-run snapshot exists confirming
which dependency versions produced the numbers currently committed here.

From this point forward, every `python scripts/run_pipeline.py` invocation
writes a JSON snapshot to `results/provenance/<step>_<timestamp>.json` (see
`src/provenance.py`) recording the git commit (and whether the working tree
was dirty), Python version, platform, the config's random seed, and the
installed versions of every package whose exact version can materially
affect the pipeline's numerical output (scanpy, anndata, leidenalg,
harmonypy, etc. — see `src/provenance.py`'s `_TRACKED_PACKAGES`).

Re-running the pipeline on real data will produce a verifiable provenance
trail going forward; the results already committed here do not have one
retroactively, and this note exists so that gap is documented rather than
silently assumed away.
