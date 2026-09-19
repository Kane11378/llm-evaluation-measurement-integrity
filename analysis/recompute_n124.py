#!/usr/bin/env python3
"""Recompute the frozen fresh N=124 confirmatory statistics from public instance-level data.

No provider/model calls.
"""
from pathlib import Path
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "empirical" / "fresh_n124_instance_effects.csv"

df = pd.read_csv(DATA)

required = {"instance_id","relabel","D_S","D_T","D_U","L_primary"}
missing = required - set(df.columns)
if missing:
    raise RuntimeError(f"Missing columns: {sorted(missing)}")
if len(df) != 124:
    raise RuntimeError(f"Expected 124 independent instances, got {len(df)}")

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
