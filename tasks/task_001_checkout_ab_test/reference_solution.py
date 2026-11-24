"""Reference solution for task_001. Writes/prints the verifiable answers."""
import json, math, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
df = pd.read_csv(HERE / "data" / "checkout_experiment.csv")

def rate(d, arm):
    s = d[d.arm == arm]
    return s.converted.mean()

# Q1: naive (raw file, no cleaning)
raw_ctrl, raw_var = rate(df, "control"), rate(df, "variant")

# Cleaning: drop internal QA accounts, then exact duplicate users
clean = df[df.is_internal == 0].drop_duplicates(subset="user_id")
clean_ctrl, clean_var = rate(clean, "control"), rate(clean, "variant")

# Q3: per-device lift (absolute, percentage points) + two-proportion z-test
def ztest(d):
    c, v = d[d.arm == "control"].converted, d[d.arm == "variant"].converted
    p1, p2, n1, n2 = c.mean(), v.mean(), len(c), len(v)
    pp = (c.sum() + v.sum()) / (n1 + n2)
    z = (p2 - p1) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    pval = math.erfc(abs(z) / math.sqrt(2))
    return p2 - p1, pval

seg = {dev: ztest(clean[clean.device == dev]) for dev in ["desktop", "mobile"]}

# Q4: mix-standardised lift using the pooled (both arms) device mix
mix = clean.device.value_counts(normalize=True)
std_ctrl = sum(mix[d] * clean[(clean.arm == "control") & (clean.device == d)].converted.mean() for d in mix.index)
std_var = sum(mix[d] * clean[(clean.arm == "variant") & (clean.device == d)].converted.mean() for d in mix.index)

# Stratified significance: weighted sum of per-device differences, variance from each stratum
var_std = 0.0
for d in mix.index:
    c = clean[(clean.arm == "control") & (clean.device == d)].converted
    v = clean[(clean.arm == "variant") & (clean.device == d)].converted
    var_std += mix[d] ** 2 * (c.var(ddof=1) / len(c) + v.var(ddof=1) / len(v))
z_std = (std_var - std_ctrl) / math.sqrt(var_std)
p_std = math.erfc(abs(z_std) / math.sqrt(2))

answers = {
    "q1_raw_conversion_control": round(raw_ctrl, 4),
    "q1_raw_conversion_variant": round(raw_var, 4),
    "q2_clean_rows": int(len(clean)),
    "q2_clean_conversion_control": round(clean_ctrl, 4),
    "q2_clean_conversion_variant": round(clean_var, 4),
    "q2_clean_naive_lift_pp": round((clean_var - clean_ctrl) * 100, 2),
    "q3_desktop_lift_pp": round(seg["desktop"][0] * 100, 2),
    "q3_mobile_lift_pp": round(seg["mobile"][0] * 100, 2),
    "q3_desktop_significant_5pct": bool(seg["desktop"][1] < 0.05),
    "q3_mobile_significant_5pct": bool(seg["mobile"][1] < 0.05),
    "q4_standardised_lift_pp": round((std_var - std_ctrl) * 100, 2),
    "q4_standardised_significant_5pct": bool(p_std < 0.05),
    "q5_recommendation": "ship_variant",
}

if __name__ == "__main__":
    out = json.dumps(answers, indent=2)
    print(out)
    if "--write" in sys.argv:
        (HERE / "answer.json").write_text(out + "\n")
