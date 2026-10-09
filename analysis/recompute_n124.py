#!/usr/bin/env python3
"""Recompute the frozen fresh N=124 confirmatory statistics from public instance-level data.

No provider/model calls.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "empirical" / "fresh_n124_instance_effects.csv"
RESULT = ROOT / "empirical" / "fresh_n124_result.json"

expected = json.loads(RESULT.read_text(encoding="utf-8"))
df = pd.read_csv(DATA)

required = {"instance_id","relabel","D_S","D_T","D_U","L_primary"}
missing = required - set(df.columns)
if missing:
    raise RuntimeError(f"Missing columns: {sorted(missing)}")
if len(df) != 124:
    raise RuntimeError(f"Expected 124 independent instances, got {len(df)}")
if expected["independent_instances"] != len(df):
    raise RuntimeError("Instance count does not match the frozen N=124 result")
if df["instance_id"].duplicated().any():
    raise RuntimeError("Duplicate instance_id in fresh N=124 public data")
expected_ids = [f"R4N124{i:03d}" for i in range(1, 125)]
if df["instance_id"].tolist() != expected_ids:
    raise RuntimeError("Unexpected fresh N=124 instance ordering/identity")

numeric_columns = ["relabel", "D_S", "D_T", "D_U", "L_primary"]
if not np.isfinite(df[numeric_columns].to_numpy(dtype=float)).all():
    raise RuntimeError("Non-finite value in fresh N=124 public data")
if not df["relabel"].isin([0, 1]).all():
    raise RuntimeError("N=124 relabel assignments must be 0 or 1")
if (df["relabel"] == 0).sum() != 62 or (df["relabel"] == 1).sum() != 62:
    raise RuntimeError("N=124 relabel assignments must remain balanced 62/62")
stage_values = df[["D_S", "D_T", "D_U"]].to_numpy(dtype=float)
if not ((stage_values >= -1) & (stage_values <= 1)).all():
    raise RuntimeError("N=124 stage effects must lie within [-1, 1]")
if not np.equal(stage_values * 2, np.round(stage_values * 2)).all():
    raise RuntimeError("N=124 stage effects must lie on half steps")
primary_values = df["L_primary"].to_numpy(dtype=float)
if not np.equal(primary_values * 4, np.round(primary_values * 4)).all():
    raise RuntimeError("N=124 primary scores must lie on quarter steps")

recalc = (df["D_U"] - df["D_S"]) / 2.0
if not (recalc == df["L_primary"]).all():
    raise RuntimeError("L_primary does not equal (D_U-D_S)/2 for every row")

x = df["L_primary"].to_numpy()
n = len(x)
mean = x.mean()
sd = x.std(ddof=1)
se = sd / n**0.5
t_stat = mean / se
dfree = n - 1
p = 2 * stats.t.sf(abs(t_stat), dfree)
crit = stats.t.ppf(0.975, dfree)
ci = (mean - crit * se, mean + crit * se)

if expected["primary"] != "L_i=(D_i_U-D_i_S)/2":
    raise RuntimeError("Unexpected frozen N=124 primary definition")
checks = {
    "mean": (mean, expected["estimate"]),
    "sd": (sd, expected["sd"]),
    "se": (se, expected["se"]),
    "t": (t_stat, expected["t"]),
    "df": (dfree, expected["df"]),
    "p_two_sided": (p, expected["p_two_sided"]),
    "ci95_low": (ci[0], expected["ci95"][0]),
    "ci95_high": (ci[1], expected["ci95"][1]),
}
for name, (got, want) in checks.items():
    if not np.isclose(got, want, rtol=0.0, atol=5e-11):
        raise RuntimeError(f"{name} mismatch: {got:.15f} != {want:.15f}")

print(f"N={n}")
print(f"mean={mean:.15f}")
print(f"sd={sd:.15f}")
print(f"se={se:.15f}")
print(f"t({dfree})={t_stat:.15f}")
print(f"p_two_sided={p:.15f}")
print(f"ci95=[{ci[0]:.15f}, {ci[1]:.15f}]")

for stage in ("S","T","U"):
    y=df[f"D_{stage}"].to_numpy()
    m=y.mean()
    s=y.std(ddof=1)
    ss=s/n**0.5
    tt=0.0 if ss == 0 else m/ss
    pp=1.0 if ss == 0 else 2*stats.t.sf(abs(tt),dfree)
    print(f"Delta_{stage}: mean={m:.15f}, raw_p={pp:.15f}")
