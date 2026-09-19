# v1.0.0-nmi-submission

Reproducibility release accompanying the manuscript:

**Evaluation infrastructure can distort behavioral effects in language-model experiments**

Author: **Kang Wang**  
ORCID: 0009-0006-7727-1214

## Scientific contents

This release contains:
- exact analytic measurement results;
- deterministic sensitivity-surface code and frozen figure data;
- CI-validated Figure 1–4 source and rendered files;
- corrected N=28 confirmatory result summary;
- fresh N=124 full instance-level primary/stage data;
- one-command N=124 confirmatory recomputation;
- identification and reproducibility protocols;
- claim-boundary documentation;
- cryptographic figure manifest.

## Frozen empirical interpretation

Corrected overall N=28:
- estimate +0.04167
- 95% CI [-0.03821,+0.12155]
- p=.29398
- non-detection, not equivalence.

Fresh prospective N=124 depth primary:
- estimate +0.016129
- 95% CI [-0.035417,+0.067675]
- t(123)=0.6194
- p=.536815
- pre-specified positive depth contrast not confirmed.

## Reproducibility

The public GitHub Actions workflow:
- recomputes the N=124 primary;
- regenerates deterministic sensitivity surfaces;
- validates regenerated surfaces against frozen data/analytic identities;
- renders SVG/PDF/300-dpi PNG figures;
- freezes figure hashes.

No provider/model calls are required to reproduce the analytic/synthetic figures or frozen N=124 statistics.

## Scope

This release is a sanitized scientific reproducibility package. The broader private Pharos research-management repository is not part of the release and is not required to reproduce the manuscript claims.
