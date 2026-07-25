#!/usr/bin/env python3
"""Driver: run all 10 ablations sequentially and aggregate metrics."""
import subprocess
import sys
from pathlib import Path
import pandas as pd
import json

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent
RESULTS = PROJECT_ROOT / "results" / "ablations"

ABLATIONS = [
    "ablation_01_at2_only.py",
    "ablation_02_embedding.py",
    "ablation_03_batch.py",
    "ablation_04_no_apoptosis.py",
    "ablation_05_root.py",
    "ablation_06_broader_epithelial.py",
    "ablation_07_leave_one_donor_out.py",
    "ablation_08_alt_programs.py",
    "ablation_09_palantir.py",
    "ablation_10_permutation_controls.py",
]


def main():
    failed = []
    for s in ABLATIONS:
        print(f"\n{'='*70}\nRunning {s}\n{'='*70}")
        rc = subprocess.call([sys.executable, str(HERE / s)])
        if rc != 0:
            failed.append(s)

    # Aggregate all metrics.json files
    rows = []
    for p in RESULTS.rglob("metrics.json"):
        try:
            d = json.loads(p.read_text())
            d["ablation"] = p.parent.name
            rows.append(d)
        except Exception as e:
            print(f"Skip {p}: {e}")
    if rows:
        df = pd.DataFrame(rows)
        out = RESULTS / "tableS6_ablation_summary.csv"
        df.to_csv(out, index=False)
        print(f"\nWrote aggregated summary: {out}")
        print(df.to_string(index=False))

    if failed:
        print(f"\nFailed ablations: {failed}")
        sys.exit(1)


if __name__ == "__main__":
    main()
