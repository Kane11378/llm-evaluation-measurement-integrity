# Pre-release reproducibility audit

## Fixed-bank completion surface repair — 2026-09-19

During public CI validation, 13 of 2,091 rows in the deterministic fixed-bank completion surface were found to contain a scientific-notation serialization defect in the `full_bank_probability` field.

The exact model is:

`P(full)=(1-h)^B`.

The affected rows stored probabilities of order `10^-1` where the paired coordinates and `stop_probability` field implied the correct values were of order `10^-10`.

The entire surface was mechanically regenerated from the exact analytic identity rather than manually editing individual rows.

This pre-release repair changed:
- the derived deterministic Figure 2g surface input;
- the rendered Figure 2g panel.

It did **not** change:
- any language-model response;
- any N=28 or N=124 empirical endpoint;
- any confidence interval or p value;
- any analytic identity;
- the manuscript's qualitative fixed-bank conclusion.

The defect was discovered before external submission by independent regeneration in the public reproducibility CI. Git history retains the original pre-repair blob.
