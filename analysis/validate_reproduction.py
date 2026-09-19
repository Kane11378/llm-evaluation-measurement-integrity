#!/usr/bin/env python3
"""Validate regenerated deterministic sensitivity surfaces against frozen public data.

This deliberately uses numerical tolerance rather than byte-for-byte floating-point
identity so that harmless library-version differences do not masquerade as scientific
reproducibility failures.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent.parent
FROZEN=ROOT/"figure_data"
REPRO=ROOT/"reproduced"/"figure_data"

FILES=[
    "fig2_scorer_censoring_surface.csv",
    "fig2_missingness_surface.csv",
    "fig2_retry_acceptance_surface.csv",
    "fig2_finalizer_surface.csv",
    "fig2_resource_surface.csv",
    "fig2_pseudorep_surface.csv",
    "fig2_pseudorep_validation.csv",
    "fig2_bank_completion_surface.csv",
    "fig2_extraction_zero_map_surface.csv",
    "fig2_extraction_outcome_dependent_row_loss_surface.csv",
]

ATOL=5e-7
RTOL=1e-10

for name in FILES:
    f=pd.read_csv(FROZEN/name)
    r=pd.read_csv(REPRO/name)
    if list(f.columns) != list(r.columns):
        raise SystemExit(f"{name}: column mismatch")
    if f.shape != r.shape:
        raise SystemExit(f"{name}: shape mismatch {f.shape} != {r.shape}")
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
