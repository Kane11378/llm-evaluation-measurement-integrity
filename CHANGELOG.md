# Changelog

## Version 1.1.0

- Clarified component licensing: original software remains MIT;
  author-owned original derived data, research figure content and documentation
  are CC BY 4.0. Third-party font notices and excluded rights are recorded separately.
- Synchronized Figure 3's scientific descriptions across its data, generator and
  SVG/PDF/PNG exports and clarified Table 1 examples. Scientific values and
  plotting parameters are preserved. The figure manifest identifies each export's
  exact bytes and build provenance.
- Added a public evidence-availability matrix separating recomputable derived
  statistics from author-held original custody evidence.
- Documented the relationship between repository figure reproductions and
  manuscript presentation artwork in `protocol/figure_presentation.md`.

The figure-data schema uses `K6_scale_marker` and `B1488_scale_marker`.
Their Boolean values and synthetic scale-marker interpretation are unchanged.
Sensitivity result metadata uses `analysis` in place of `task`, and the two
scale-note fields use `scale_note`. The generator path names the script included
in this repository. Consumers of earlier schemas should map the earlier names
to these fields explicitly.

Reproduction validation checks the frozen N=124 primary statistics, scientific
row identities and static figure/table data in addition to the sensitivity
surfaces. Declared line endings preserve exact N=28 and publication-figure
identities on Windows. Empirical rows, canonical ledger identity, scientific
values, seeds and Figure 1/2/4 export bytes are preserved. The historical v1.0.0
snapshot and its identifier remain separate from version 1.1.0.

## Fixed-bank completion surface repair — 2026-09-19

During public CI validation, 13 of 2,091 rows in the deterministic fixed-bank completion surface were found to contain a scientific-notation serialization defect in the `full_bank_probability` field.

The exact model is:

`P(full)=(1-h)^B`.

The affected rows stored probabilities of order `10^-1` where the paired coordinates and `stop_probability` field implied the correct values were of order `10^-10`.

The entire surface was mechanically regenerated from the exact analytic identity rather than manually editing individual rows.

The repair changed:

- the derived deterministic Figure 2g surface input;
- the rendered Figure 2g panel.

It did **not** change:

- any language-model response;
- any N=28 or N=124 empirical endpoint;
- any confidence interval or p value;
- any analytic identity;
- the manuscript's qualitative fixed-bank conclusion.

The defect was discovered by independent regeneration in the public reproducibility CI. Git history retains the original pre-repair blob.
