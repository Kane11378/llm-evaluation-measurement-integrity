# Public empirical data dictionary

## empirical/fresh_n124_instance_effects.csv

One row per independent fresh instance in the prospectively frozen N=124 confirmation.

Columns:

- `instance_id`: synthetic instance identifier.
- `relabel`: prospectively balanced nuisance relabel assignment (0/1).
- `D_S`: mean of the two matched LOCAL−CROSS correctness differences at stage S.
- `D_T`: mean of the two matched LOCAL−CROSS correctness differences at stage T.
- `D_U`: mean of the two matched LOCAL−CROSS correctness differences at stage U.
- `L_primary`: frozen primary instance score, `(D_U-D_S)/2`.

Each node-level correctness value is binary, so stage averages occur in increments of 0.5 and the primary occurs in increments of 0.25.

The independent inferential N is 124, not the 1,488 individual API calls.

Run:

```bash
python analysis/recompute_n124.py
```

to reproduce the reported N=124 primary mean, SD, SE, t statistic, two-sided p value and 95% t confidence interval.

## empirical/corrected_n28_result.json

Frozen summary of the corrected first confirmatory overall analysis.

The underlying corrected derived ledger has canonical SHA-256:

`8ce6a19f9e62fd29ecef0ff1ec62708690c1e462c0d75b69dfc7ad1c846382c1`

The public-release decision for additional row-level N=28 source material is handled separately from the summary because the original correction was reconstructed from preserved raw-response custody artifacts.

## empirical/fresh_n124_result.json

Frozen scalar summary for the fresh prospective N=124 confirmation.

It is redundant with, and can be independently checked against, `fresh_n124_instance_effects.csv`.
