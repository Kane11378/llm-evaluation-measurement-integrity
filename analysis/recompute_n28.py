#!/usr/bin/env python3
"""Recompute the frozen corrected N=28 primary statistics from public instance-level data.

No provider/model calls.
"""
from pathlib import Path
import hashlib
import json
import math

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "empirical" / "corrected_n28_instance_effects.csv"
MANIFEST = ROOT / "empirical" / "corrected_n28_provenance_manifest.json"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
raw = DATA.read_bytes()
got_sha = hashlib.sha256(raw).hexdigest()
expected_sha = manifest["released_file"]["sha256"]
if got_sha != expected_sha:
    raise RuntimeError(f"N=28 public data SHA-256 mismatch: {got_sha} != {expected_sha}")

df = pd.read_csv(DATA)
required = {"instance_id", "D_overall"}
missing = required - set(df.columns)
if missing:
    raise RuntimeError(f"Missing columns: {sorted(missing)}")
if len(df) != 28:
    raise RuntimeError(f"Expected 28 independent instances, got {len(df)}")
if df["instance_id"].duplicated().any():
    raise RuntimeError("Duplicate instance_id in corrected N=28 public data")
expected_ids = [f"R4PC{i:03d}" for i in range(1, 29)]
if df["instance_id"].tolist() != expected_ids:
    raise RuntimeError("Unexpected corrected N=28 instance ordering/identity")

x = df["D_overall"].to_numpy(dtype=float)
n = len(x)
mean = x.mean()
sd = x.std(ddof=1)
se = sd / math.sqrt(n)
t_stat = mean / se
dfree = n - 1
p = 2 * stats.t.sf(abs(t_stat), dfree)
crit = stats.t.ppf(0.975, dfree)
ci = (mean - crit * se, mean + crit * se)

expected = manifest["expected_recomputation"]
checks = {
    "mean": (mean, expected["mean_LOCAL_minus_CROSS"]),
    "sd": (sd, expected["sd"]),
    "se": (se, expected["se"]),
    "t": (t_stat, expected["t"]),
    "p_two_sided": (p, expected["p_two_sided"]),
    "ci95_low": (ci[0], expected["ci95"][0]),
    "ci95_high": (ci[1], expected["ci95"][1]),
}
for name, (got, want) in checks.items():
    if not np.isclose(got, want, rtol=0.0, atol=5e-11):
        raise RuntimeError(f"{name} mismatch: {got:.15f} != {want:.15f}")

print(f"N={n}")
print(f"mean={mean:.10f}")
print(f"sd={sd:.10f}")
print(f"se={se:.10f}")
print(f"t({dfree})={t_stat:.10f}")
print(f"p_two_sided={p:.10f}")
print(f"ci95=[{ci[0]:+.10f}, {ci[1]:+.10f}]")
