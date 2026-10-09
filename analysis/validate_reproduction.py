#!/usr/bin/env python3
"""Validate regenerated deterministic sensitivity surfaces against frozen public data.

Frozen and regenerated rows are aligned by scientific design coordinates before
comparison. Numerical tolerance is intentionally far below manuscript precision,
while avoiding false failures from harmless library-version floating-point changes.
"""
from pathlib import Path
import json
import re
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

    if name == "fig2_bank_completion_surface.csv":
        # This panel has an exact analytic target. Validate each file against the
        # identity rather than relying on floating-coordinate row alignment.
        for label, d in (("frozen",f),("reproduced",r)):
            B=d["bank_size_B"].to_numpy(dtype=float)
            h=d["per_call_hazard_h"].to_numpy(dtype=float)
            p=d["full_bank_probability"].to_numpy(dtype=float)
            stop=d["stop_probability"].to_numpy(dtype=float)
            expected=np.power(1.0-h,B)
            if not np.allclose(p,expected,rtol=1e-12,atol=1e-12):
                raise SystemExit(f"{name}:{label}: P(full) identity failure")
            if not np.allclose(stop,1.0-expected,rtol=1e-12,atol=1e-12):
                raise SystemExit(f"{name}:{label}: stop-probability identity failure")
        if set(f["bank_size_B"]) != set(r["bank_size_B"]):
            raise SystemExit(f"{name}: bank-size coordinate mismatch")
        if not np.allclose(sorted(f["per_call_hazard_h"].unique()),
                           sorted(r["per_call_hazard_h"].unique()),
                           rtol=1e-12,atol=1e-15):
            raise SystemExit(f"{name}: hazard coordinate mismatch")
        print(f"PASS {name}: {len(f)} rows; analytic identity verified")
        continue

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

# Static tables carry scientific claims and public source references. Check both;
# Figure 1's source column is a graph coordinate rather than a file citation.
STATIC_FILES = {
    "fig1_pipeline_nodes.csv": ([], []),
    "fig1_pipeline_edges.csv": ([], []),
    "fig3_empirical_ladder.csv": (["order"], []),
    "fig4_effect_estimates.csv": (["estimate"], []),
    "table1_protocol.csv": (["threat"], []),
}
STATIC_ATOL = 5e-11
for name, (identity_columns, provenance_columns) in STATIC_FILES.items():
    f = pd.read_csv(FROZEN / name)
    r = pd.read_csv(REPRO / name)
    if list(f.columns) != list(r.columns) or f.shape != r.shape:
        raise SystemExit(f"{name}: static table schema/shape mismatch")
    if identity_columns:
        if f.duplicated(identity_columns).any() or r.duplicated(identity_columns).any():
            raise SystemExit(f"{name}: duplicate static scientific identity")
    # Keep frozen row order: Figure 4's plotted labels depend on that order.
    for col in f.columns:
        if col in provenance_columns:
            continue
        if pd.api.types.is_numeric_dtype(f[col]) and pd.api.types.is_numeric_dtype(r[col]):
            if not np.allclose(f[col].to_numpy(dtype=float), r[col].to_numpy(dtype=float),
                               rtol=0.0, atol=STATIC_ATOL, equal_nan=True):
                raise SystemExit(f"{name}:{col}: static scientific numeric mismatch")
        elif not f[col].fillna("").astype(str).equals(r[col].fillna("").astype(str)):
            raise SystemExit(f"{name}:{col}: static scientific text/order mismatch")
    print(f"PASS {name}: {len(f)} frozen scientific rows")

    if name in ("fig3_empirical_ladder.csv", "fig4_effect_estimates.csv", "table1_protocol.csv"):
        for reference in f["source"]:
            for citation in reference.split("; "):
                relative, _, anchor = citation.partition("#")
                path = (ROOT / relative).resolve()
                if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
                    raise SystemExit(f"{name}: missing or nonpublic source reference {citation}")
                if anchor:
                    headings = re.findall(r"^#{1,6}\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
                    slugs = [re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-") for h in headings]
                    if anchor not in slugs:
                        raise SystemExit(f"{name}: missing public source anchor {citation}")

print("PASS synchronized, resolvable public source references")

packages = []
results = []
for label, directory, result_path in (
    ("frozen", FROZEN, ROOT / "analysis" / "SENSITIVITY_SURFACE_RESULTS.json"),
    ("reproduced", REPRO, ROOT / "reproduced" / "SENSITIVITY_SURFACE_RESULTS_REPRODUCED.json"),
):
    package = json.loads((directory / "figure_data_package.json").read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    if package["surface_results"] != result:
        raise SystemExit(f"{label}: figure package does not contain its corresponding surface result")
    if package["schema"] != "public_sensitivity_surface_figure_data":
        raise SystemExit(f"{label}: unexpected public figure package schema")
    if package["generated_by"] != "analysis/sensitivity_surface_framework.py":
        raise SystemExit(f"{label}: figure package generator path mismatch")
    if result["analysis"] != "synthetic_sensitivity_surfaces":
        raise SystemExit(f"{label}: unexpected sensitivity analysis label")
    for path in package["empirical_files"] + package["figure1_files"]:
        if not (ROOT / path).is_file():
            raise SystemExit(f"{label}: figure package references missing public file {path}")
    packages.append(package)
    results.append(result)

for key in ("schema", "version", "generated_by", "empirical_files", "figure1_files"):
    if packages[0][key] != packages[1][key]:
        raise SystemExit(f"figure package metadata mismatch: {key}")
for key in ("analysis", "version", "seed", "behavioral_provider_calls", "scientific_spend"):
    if results[0][key] != results[1][key]:
        raise SystemExit(f"surface result metadata mismatch: {key}")
print("PASS synchronized public figure package and analysis metadata")
print(f"ALL REPRODUCTION CHECKS PASS; surfaces atol={ATOL:g}, rtol={RTOL:g}; static science atol={STATIC_ATOL:g}")
