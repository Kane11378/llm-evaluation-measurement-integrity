# When Evaluation Changes the Effect: A Measurement-Integrity Framework for Language-Model Experiments

[![reproducibility](https://github.com/Kane11378/llm-evaluation-measurement-integrity/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/Kane11378/llm-evaluation-measurement-integrity/actions/workflows/reproducibility.yml)

Public reproducibility package accompanying the manuscript by **Kang Wang**.

This branch prepares **v1.1.0, an unreleased archival candidate**. The reviewed new archive is intended to become the manuscript's preferred reproducibility version after publication. No release date or new version DOI has been assigned. The historical v1.0.0 archive remains available below.

This repository contains the public scientific materials needed to audit and reproduce the manuscript's analytic, deterministic-synthetic and frozen empirical results.

## Scientific scope

The manuscript does **not** report a confirmed general provenance bias.

The audited contextual-provenance empirical study contains:
- a corrected N=28 confirmatory non-detection;
- an exploratory depth pattern;
- a wholly fresh prospective N=124 test that did not confirm the pre-specified positive depth contrast.

The general contribution is a measurement and identification framework showing, under explicit assumptions, how observation, scoring, replacement, post-processing, resource truncation, extraction and dependence can change an apparent behavioral contrast or its uncertainty.

## Evidence classes

The public package separates four evidence classes:

1. **Exact analytic results** — algebraic consequences of stated measurement models.
2. **Deterministic synthetic surfaces** — parameter-sensitivity geometry; not estimates of historical measurement bias in the empirical case.
3. **Validation simulations** — deterministic finite-sample checks used only where stated.
4. **Frozen empirical results** — released instance-level effects, scalar summaries and documented custody identities.

Synthetic parameter values must not be interpreted as empirical estimates of integrity hazards, ICCs or resource-demand distributions.

## Repository structure

- `analysis/` — deterministic sensitivity, empirical recomputation and figure-generation code.
- `figure_data/` — frozen CSV/JSON inputs for manuscript figures.
- `figures/` — frozen SVG, PDF and 300-dpi PNG figure files plus their SHA-256 manifest.
- `protocol/` — identification, measurement and reproducibility documentation.
- `empirical/` — shareable frozen empirical derived artifacts and custody/provenance documentation.

## Reproduction

The released analysis and figure code makes **no model/provider calls**.

Independent empirical recomputation:

```bash
python analysis/recompute_n28.py
python analysis/recompute_n124.py
```

The N=28 command reads only the public instance-level effects plus their provenance manifest and reproduces N, mean, SD, SE, t statistic, two-sided p value and 95% t confidence interval. The N=124 command independently recomputes the prospectively frozen depth confirmation. Deterministic sensitivity and figure reproduction are checked by the repository workflow.

A pinned Python environment is provided in `requirements.txt` and `environment.yml`.

Regenerate and validate the deterministic sensitivity surfaces with:

```bash
python analysis/sensitivity_surface_framework.py
python analysis/validate_reproduction.py
```

The figure renderer is `analysis/reproduce_figures.py`. Run it in a separate working copy: it writes new exports to `figures/`. The reproducibility workflow retains the original publication files, renders separate outputs, then restores and verifies the original files against their manifest. Successful rendering does not imply that regenerated files have the same byte identity as the archived figures.

The archived figures are reproducibility exports from the public figure data. Figure 3 presents the same numerical and scientific evidence as the manuscript's presentation figure, with a different table layout and some wording differences. Archival and journal artwork are distinct assets; regenerating the archive figures does not replace the manuscript figure.

The N=28 data and publication figure manifest use exact byte hashes. Preserve the repository's declared line endings when checking out files, including on Windows.

## Data integrity

The corrected N=28 release includes all 28 frozen instance-level effects needed for independent statistical recomputation and a provenance manifest binding them to the canonical corrected derived-ledger SHA-256 `8ce6a19f9e62fd29ecef0ff1ec62708690c1e462c0d75b69dfc7ad1c846382c1`. That ledger was reconstructed deterministically from preserved raw custody under the unchanged frozen oracle, scorer and analyzer; no behavioral replay occurred.

Raw provider transport/account metadata are not required for the reported N=28 statistics and are not published. The public instance-level release is therefore a scientific derived-data artifact, not a raw-provider dump.

The [public evidence-availability matrix](protocol/evidence_provenance.md#public-evidence-availability) distinguishes independently recomputable results from author-reported history and underlying records held by the author.

## Licenses

| Content | License or rights boundary |
|---|---|
| Original software source and executable figure-generation code | [MIT](LICENSE) |
| Author-owned original derived scientific datasets and tables | [CC BY 4.0](LICENSE-DATA.md) |
| Author-owned original documentation and research figure content | [CC BY 4.0](LICENSE-DATA.md) |
| Third-party components, provider-owned material, unpublished custody artifacts and material with unresolved rights | Excluded from the author's grant; retain applicable separate terms. DejaVu figure font notices are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). |

The [data, figure and documentation license](LICENSE-DATA.md) defines the grant and attribution requirements. A public provenance summary or hash does not release or license the underlying author-held records. Historical archival versions retain their existing identities and license notices.

## Author

**Kang Wang**  
College of Finance and Economics, Taiyuan University of Technology  
Taiyuan 030024, Shanxi, China  
ORCID: 0009-0006-7727-1214

The associated manuscript contains the authoritative research-process and manuscript-preparation AI declarations. ChatGPT 5.6 Sol (OpenAI) assisted with code, technical documentation, workflow and repository preparation, and manuscript organization, language refinement and editorial review. The author independently verified the scientific decisions and adopted material and takes responsibility for the work.

## Citation

The prospective citation metadata in [CITATION.cff](CITATION.cff) describe **v1.1.0 (unreleased)**. For work using this candidate, identify the exact Git commit and its unreleased status. After the new archive is published and verified, cite its actual version-specific DOI and the associated manuscript.

Historical archive: **v1.0.0**, [DOI 10.5281/zenodo.22846957](https://doi.org/10.5281/zenodo.22846957). This DOI identifies only the original archived snapshot. It does not identify the current candidate or a future replacement archive.

[RELEASE_NOTES.md](RELEASE_NOTES.md) describes the prospective version. [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) lists the remaining publication gates. GitHub-Zenodo archiving uses [.zenodo.json](.zenodo.json); its version and component-license description must remain consistent with the citation file when release publication is authorized.
