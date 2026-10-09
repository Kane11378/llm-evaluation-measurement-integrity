# v1.1.0 — unreleased archival candidate

Prospective reproducibility version accompanying the manuscript:

**When Evaluation Changes the Effect: A Measurement-Integrity Framework for Language-Model Experiments**

Author: **Kang Wang**  
ORCID: 0009-0006-7727-1214

The version number is proposed for the next archive. No release date or new version-specific DOI has been assigned. Publication remains subject to independent review and the author's approval of the exact public contents.

## Changes from the historical archive

- Updated the manuscript title, public source references and evidence-availability documentation.
- Replaced internal display labels in Figure 3 and protocol examples with scientific descriptions, preserving all scientific values and plotting parameters.
- Clarified the distinction between independently recomputable public derived results and historical custody records held by the author.
- Strengthened validation of the frozen N=124 inputs and deterministic reproduction sources.
- Declared stable line endings for byte-sensitive data and figure files.
- Documented original software under MIT, author-owned original derived scientific data, research figure content and documentation under CC BY 4.0, and separate third-party terms.
- Prepared current version metadata without reusing the historical archive's DOI as a new archive identity.

## Scientific contents and interpretation

The candidate includes exact analytic measurement results, deterministic sensitivity surfaces, Figure 1–4 source data and SVG/PDF/300-dpi PNG exports, independent empirical recomputation, identification and reproducibility protocols, and file-integrity manifests.

The frozen empirical interpretations are preserved:

| Analysis | Estimate | 95% confidence interval | Two-sided p value | Interpretation |
|---|---:|---|---:|---|
| Corrected overall N=28 | +0.04167 | [-0.03821, +0.12155] | .29398 | Non-detection; not equivalence |
| Fresh prospective N=124 depth primary | +0.016129 | [-0.035417, +0.067675] | .536815 | Pre-specified positive depth contrast not confirmed |

The fresh N=124 test remains t(123)=0.6194. Deterministic sensitivity parameter values remain illustrative model inputs, not estimates of historical empirical bias.

Figure 3's public exports use the repository's data-driven layout. Journal presentation artwork may use a different layout while representing the same scientific evidence. The public figure manifest identifies the exact archived exports and distinguishes original figure builds from the Figure 3 label migration. Layout or byte differences must be reviewed without replacing scientific data or accepted presentation artwork merely to obtain matching hashes.

## Reproduction and integrity

The native reproducibility workflow recomputes N=28 and N=124, regenerates and validates all deterministic sensitivity data, renders Figure 1–4, and verifies the frozen publication files. The complete public file inventory is recorded in `ARCHIVE_MANIFEST.json`; `analysis/verify_archive.py` verifies its file identities.

No provider/model calls are required to reproduce the public analytic, deterministic-synthetic or frozen empirical results. Numeric recomputation does not independently establish historical raw-response custody.

## Historical version

The original **v1.0.0** tag and [version DOI 10.5281/zenodo.22846957](https://doi.org/10.5281/zenodo.22846957) retain their historical meaning. The candidate does not edit, delete or replace that archived snapshot. After verification and publication, the new archive's actual version-specific DOI should become the manuscript's preferred reference for these revised public files.

Remaining gates are listed in [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md).
