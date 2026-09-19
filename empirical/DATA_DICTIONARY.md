# Public empirical data dictionary

## empirical/corrected_n28_instance_effects.csv

One row per independent instance in the corrected N=28 confirmatory overall analysis.

Columns:

- `instance_id`: frozen synthetic instance identifier.
- `D_overall`: frozen instance-level LOCAL-minus-CROSS effect, defined as the mean of the six matched seam-level exact-correctness differences for that instance.

The independent inferential N is 28, not the 336 individual API calls. These 28 effects are the complete instance-level vector frozen in the corrected analysis; they are sufficient to recompute the reported mean, SD, SE, t statistic, two-sided p value and 95% t confidence interval.

Run:

```bash
python analysis/recompute_n28.py
```

The recomputation script first verifies the CSV SHA-256 against `corrected_n28_provenance_manifest.json`, then recomputes the frozen statistics.

## empirical/corrected_n28_provenance_manifest.json

Public custody/provenance record for the corrected N=28 instance-level release.

It records the canonical corrected 336-row derived-ledger SHA-256:

`8ce6a19f9e62fd29ecef0ff1ec62708690c1e462c0d75b69dfc7ad1c846382c1`

The corrected ledger was reconstructed deterministically from 336 preserved raw responses under the unchanged frozen oracle, scorer and analyzer. No behavioral replay, row replacement or endpoint change occurred. Raw provider transport/account metadata is not required for statistical recomputation and is not published in this public package.

## empirical/corrected_n28_result.json

Frozen scalar summary of the corrected first confirmatory overall analysis.

It is redundant with, and can be independently checked against, `corrected_n28_instance_effects.csv`.

## empirical/fresh_n124_instance_effects.csv

One row per independent fresh instance in the prospectively frozen N=124 confirmation.

Columns:

- `instance_id`: synthetic instance identifier.
- `relabel`: prospectively balanced nuisance relabel assignment (0/1).
- `D_S`: mean of the two matched LOCAL-minus-CROSS correctness differences at stage S.
- `D_T`: mean of the two matched LOCAL-minus-CROSS correctness differences at stage T.
- `D_U`: mean of the two matched LOCAL-minus-CROSS correctness differences at stage U.
- `L_primary`: frozen primary instance score, `(D_U-D_S)/2`.

Each node-level correctness value is binary, so stage averages occur in increments of 0.5 and the primary occurs in increments of 0.25.

The independent inferential N is 124, not the 1,488 individual API calls.

Run:

```bash
python analysis/recompute_n124.py
```

to reproduce the reported N=124 primary mean, SD, SE, t statistic, two-sided p value and 95% t confidence interval.

## empirical/fresh_n124_result.json

Frozen scalar summary for the fresh prospective N=124 confirmation.

It is redundant with, and can be independently checked against, `fresh_n124_instance_effects.csv`.
