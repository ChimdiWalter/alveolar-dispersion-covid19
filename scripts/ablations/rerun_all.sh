#!/bin/bash
# Re-run every ablation with the displacement_effect_size fix applied
# (common.py now reads key "effect_size_r"). Uses venv python directly.
set -u
cd /deltos/e/lesion_phes/code/python/pipeline/sb_class_project
PY=/home/cnptp/.venvs/lesegenv/bin/python
for a in \
  ablation_01_at2_only \
  ablation_02_embedding \
  ablation_03_batch \
  ablation_04_no_apoptosis \
  ablation_05_root \
  ablation_06_broader_epithelial \
  ablation_07_leave_one_donor_out \
  ablation_08_alt_programs \
  ablation_09_palantir \
  ablation_10_permutation_controls; do
  echo "=== $a $(date) ==="
  $PY scripts/ablations/$a.py 2>&1 | tail -20
  echo "EXIT=${PIPESTATUS[0]}"
done
echo "=== aggregate $(date) ==="
$PY - <<'PY'
from pathlib import Path
import json, pandas as pd
R = Path("results/ablations")
rows=[]
for p in sorted(R.rglob("metrics.json")):
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
