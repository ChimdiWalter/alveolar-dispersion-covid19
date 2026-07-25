#!/bin/bash
set -u
cd /deltos/e/lesion_phes/code/python/pipeline/sb_class_project
source /home/cnptp/.venvs/lesegenv/bin/activate
for a in ablation_02_embedding ablation_03_batch ablation_04_no_apoptosis ablation_06_broader_epithelial ablation_10_permutation_controls; do
  echo "=== $a $(date) ==="
  python scripts/ablations/$a.py 2>&1 | tail -15
  echo "EXIT=$?"
done
echo "=== aggregate $(date) ==="
python - <<'PY'
from pathlib import Path
import json, pandas as pd
R = Path("results/ablations")
rows=[]
for p in R.rglob("metrics.json"):
    try:
        d = json.loads(p.read_text())
        d["ablation"] = p.parent.name
        rows.append(d)
    except Exception as e:
        print(f"Skip {p}: {e}")
df = pd.DataFrame(rows)
df.to_csv(R/"tableS6_ablation_summary.csv", index=False)
print(df.to_string(index=False))
PY
echo "=== DONE $(date) ==="
