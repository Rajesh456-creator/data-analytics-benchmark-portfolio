"""Generate the synthetic dataset for task_001 (fixed seed, fully reproducible)."""
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 20260101
rng = np.random.default_rng(SEED)

# (arm, device) -> (n_users, true conversion rate)
CELLS = {
    ("control", "desktop"): (7000, 0.30),
    ("control", "mobile"):  (3000, 0.10),
    ("variant", "desktop"): (2500, 0.33),
    ("variant", "mobile"):  (7500, 0.135),
}

rows, uid = [], 1
for (arm, device), (n, p) in CELLS.items():
    conv = rng.random(n) < p
    for c in conv:
        rows.append((f"U{uid:06d}", arm, device, int(c), 0))
        uid += 1
df = pd.DataFrame(rows, columns=["user_id", "arm", "device", "converted", "is_internal"])

# Dirty data 1: internal QA accounts (always convert), 150 per arm
internal = []
for arm in ["control", "variant"]:
    for _ in range(150):
        internal.append((f"U{uid:06d}", arm, rng.choice(["desktop", "mobile"]), 1, 1))
        uid += 1
df = pd.concat([df, pd.DataFrame(internal, columns=df.columns)], ignore_index=True)

# Dirty data 2: ~3% of rows duplicated by a logging retry (exact repeats)
dups = df.sample(frac=0.03, random_state=SEED)
df = pd.concat([df, dups], ignore_index=True)

df = df.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
out = Path(__file__).resolve().parent.parent / "tasks/task_001_checkout_ab_test/data/checkout_experiment.csv"
df.to_csv(out, index=False)
print(f"wrote {len(df)} rows -> {out}")
