# Version 1.1.0

Reproducibility package accompanying the manuscript:

**When Evaluation Changes the Effect: A Measurement-Integrity Framework for Language-Model Experiments**

Author: **Kang Wang**  
ORCID: 0009-0006-7727-1214

## Changes from the historical archive

- Updated the manuscript title, public source references and evidence-availability documentation.
- Clarified Figure 3 and protocol-table descriptions, preserving all scientific values and plotting parameters.
- Clarified the distinction between independently recomputable public derived results and historical custody records held by the author.
- Strengthened validation of the frozen N=124 inputs and deterministic reproduction sources.
- Declared stable line endings for byte-sensitive data and figure files.
- Documented original software under MIT, author-owned original derived scientific data, research figure content and documentation under CC BY 4.0, and separate third-party terms.
- Distinguished version 1.1.0 metadata from the historical archive's identifier.

## Scientific contents and interpretation

The package includes exact analytic measurement results, deterministic sensitivity surfaces, Figure 1–4 source data and SVG/PDF/300-dpi PNG exports, independent empirical recomputation, identification and reproducibility protocols, and file-integrity manifests.

The frozen empirical interpretations are preserved:

| Analysis | Estimate | 95% confidence interval | Two-sided p value | Interpretation |
|---|---:|---|---:|---|
| Corrected overall N=28 | +0.04167 | [-0.03821, +0.12155] | .29398 | Non-detection; not equivalence |
| Fresh prospective N=124 depth primary | +0.016129 | [-0.035417, +0.067675] | .536815 | Pre-specified positive depth contrast not confirmed |

The fresh N=124 test remains t(123)=0.6194. Deterministic sensitivity parameter values remain illustrative model inputs, not estimates of historical empirical bias.

The repository exports include code-defined schematics and views of frozen scientific data. Figures 1, 3 and 4 use different layouts from the manuscript's presentation artwork while preserving scientific content and source boundaries. Their rendered bytes need not match the manuscript figures. The public figure manifest identifies the exact repository exports. [Figure presentation and source notes](protocol/figure_presentation.md) record the sources and caption correspondence for these assets.

## Reproduction and integrity

The native reproducibility workflow recomputes N=28 and N=124, regenerates and validates all deterministic sensitivity data, renders Figure 1–4, and verifies the frozen publication files. The complete public file inventory is recorded in `ARCHIVE_MANIFEST.json`; `analysis/verify_archive.py` verifies its file identities.

No provider/model calls are required to reproduce the public analytic, deterministic-synthetic or frozen empirical results. Numeric recomputation does not independently establish historical raw-response custody.

## Historical version

The original **v1.0.0** tag and [version DOI 10.5281/zenodo.22846957](https://doi.org/10.5281/zenodo.22846957) identify the original historical snapshot. That archived snapshot remains separate from version 1.1.0.
