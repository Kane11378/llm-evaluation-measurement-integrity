#!/usr/bin/env python3
"""Validate regenerated deterministic sensitivity surfaces against frozen public data.

Frozen and regenerated rows are aligned by scientific design coordinates before
comparison. Numerical tolerance is intentionally far below manuscript precision,
while avoiding false failures from harmless library-version floating-point changes.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent.parent
FROZEN=ROOT/"figure_data"
REPRO=ROOT/"reproduced"/"figure_data"

KEYS={
    "fig2_scorer_censoring_surface.csv":
        ["treatment_correct_retention","treatment_incorrect_retention"],
    "fig2_missingness_surface.csv":
        ["treatment_observation_intercept","treatment_observation_slope_on_difficulty"],
    "fig2_retry_acceptance_surface.csv":
        ["treatment_pass_if_correct","treatment_pass_if_incorrect"],
    "fig2_finalizer_surface.csv":
        ["treatment_sensitivity","treatment_false_positive_probability"],
    "fig2_resource_surface.csv":
        ["output_cap","treatment_log_demand_shift"],
    "fig2_pseudorep_surface.csv":
        ["calls_per_instance_K","icc_rho"],
    "fig2_pseudorep_validation.csv":
        ["K","rho"],
    "fig2_bank_completion_surface.csv":
        ["bank_size_B","per_call_hazard_h"],
    "fig2_extraction_zero_map_surface.csv":
        ["control_extraction_success_random_within_arm","treatment_extraction_success_random_within_arm"],
    "fig2_extraction_outcome_dependent_row_loss_surface.csv":
        ["treatment_correct_extraction_retention","treatment_incorrect_extraction_retention"],
}

ATOL=1e-5
RTOL=1e-10

for name, keys in KEYS.items():
    f=pd.read_csv(FROZEN/name)
    r=pd.read_csv(REPRO/name)
    if list(f.columns) != list(r.columns):
        raise SystemExit(f"{name}: column mismatch")
    if f.shape != r.shape:
        raise SystemExit(f"{name}: shape mismatch {f.shape} != {r.shape}")

    # Row order is not scientific content. Align by the frozen design coordinates.
    f=f.sort_values(keys).reset_index(drop=True)
    r=r.sort_values(keys).reset_index(drop=True)

    for col in f.columns:
        if pd.api.types.is_numeric_dtype(f[col]) and pd.api.types.is_numeric_dtype(r[col]):
            a=f[col].to_numpy(dtype=float)
            b=r[col].to_numpy(dtype=float)
            if not np.allclose(a,b,rtol=RTOL,atol=ATOL,equal_nan=True):
                diff=np.nanmax(np.abs(a-b))
                raise SystemExit(f"{name}:{col}: numerical mismatch max_abs={diff}")
        else:
            if not f[col].fillna("").astype(str).equals(r[col].fillna("").astype(str)):
                raise SystemExit(f"{name}:{col}: categorical/string mismatch")
    print(f"PASS {name}: {len(f)} rows")

print(f"ALL SURFACES PASS within atol={ATOL:g}, rtol={RTOL:g}")
