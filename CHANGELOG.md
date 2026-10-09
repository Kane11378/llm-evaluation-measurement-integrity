# Pre-release reproducibility audit

## Unreleased publication preparation

- Finalized author-approved component licensing: original software remains MIT;
  author-owned original derived data, research figure content and documentation
  are CC BY 4.0. Third-party font notices and excluded rights are recorded separately.
- Synchronized Figure 3's ordinary display label across its data, generator and
  SVG/PDF/PNG exports; removed internal instrument/bank labels from Table 1
  examples. Scientific values and plotting parameters are preserved. The
  manifest distinguishes the original build from the local Figure 3 migration.
- Added a public evidence-availability matrix separating recomputable derived
  statistics from author-held original custody evidence.
- Consolidated the README's assistance note under author information; the
  manuscript remains authoritative for formal AI declarations.

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

## Unreleased publication cleanup

The manuscript association and repository AI-use summary are aligned with the current manuscript and its formal declarations. Private operational source references are replaced by public provenance summaries, with the original references retained separately. The empirical rows, canonical ledger identity, scientific values, seeds and Figure 1/2/4 files are unchanged. Figure 3 has the separately documented display-label migration.

The figure-data schema uses the publication-facing fields `K6_scale_marker` and `B1488_scale_marker`, replacing the earlier project-prefixed field names. Their Boolean values and the synthetic scale-marker interpretation are unchanged. Sensitivity result metadata uses `analysis` in place of `task`, and the two scale-note fields use `scale_note`. The generator path now names the script included in this repository. Consumers of earlier schemas should map the prior names to these fields explicitly.

Reproduction validation now checks the frozen N=124 primary statistics, scientific row identities and static figure/table data in addition to the sensitivity surfaces. Declared line endings preserve the exact N=28 and publication-figure identities on Windows. These changes do not revise v1.0.0 or assign its DOI to a later snapshot.
