# Evaluation infrastructure can distort behavioral effects in language-model experiments

[![reproducibility](https://github.com/Kane11378/llm-evaluation-measurement-integrity/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/Kane11378/llm-evaluation-measurement-integrity/actions/workflows/reproducibility.yml)

Public reproducibility package accompanying the manuscript by **Kang Wang**.

This repository contains the intentionally released scientific materials needed to audit and reproduce the manuscript's analytic, deterministic-synthetic and frozen empirical results. It is **not** a mirror of the author's private Pharos research repository.

## Scientific scope

The manuscript does **not** report a confirmed general provenance bias.

Its empirical record contains:
- a corrected N=28 confirmatory non-detection;
- an exploratory depth pattern;
- a wholly fresh prospective N=124 test that did not confirm the pre-specified positive depth contrast.

The general contribution is a measurement and identification framework showing, under explicit assumptions, how observation, scoring, replacement, post-processing, resource truncation, extraction and dependence can change an apparent behavioral contrast or its uncertainty.

## Evidence classes

The public package separates four evidence classes:

1. **Exact analytic results** — algebraic consequences of stated measurement models.
2. **Deterministic synthetic surfaces** — parameter-sensitivity geometry; not estimates of historical OMI bias.
3. **Validation simulations** — deterministic finite-sample checks used only where stated.
4. **Frozen empirical OMI results** — preserved experimental records and derived statistics.

Synthetic parameter values must not be interpreted as empirical estimates of OMI integrity hazards, ICCs or resource-demand distributions.

## Repository structure

- `analysis/` — deterministic sensitivity and figure-generation code.
- `figure_data/` — frozen CSV/JSON inputs for manuscript figures.
- `figures/` — frozen vector figures; PDF/PNG upload formats will be added at release freeze.
- `protocol/` — identification, measurement and reproducibility documentation.
- `empirical/` — shareable frozen empirical derived artifacts and custody documentation.
- `manifests/` — cryptographic identities and release manifests.

## Reproduction

The released analysis and figure code makes **no model/provider calls**.

Independent empirical recomputation:

```bash
python analysis/recompute_n28.py
python analysis/recompute_n124.py
```

The N=28 command reads only the public instance-level effects plus their provenance manifest and reproduces N, mean, SD, SE, t statistic, two-sided p value and 95% t confidence interval. The N=124 command independently recomputes the prospectively frozen depth confirmation. Deterministic sensitivity and figure reproduction remain covered by the repository workflow.

Detailed environment and reproduction commands are frozen with the versioned release.

## Data integrity

The corrected N=28 release includes all 28 frozen instance-level effects needed for independent statistical recomputation and a provenance manifest binding them to the canonical corrected derived-ledger SHA-256 `8ce6a19f9e62fd29ecef0ff1ec62708690c1e462c0d75b69dfc7ad1c846382c1`. That ledger was reconstructed deterministically from preserved raw custody under the unchanged frozen oracle, scorer and analyzer; no behavioral replay occurred.

Raw provider transport/account metadata is not required for the reported N=28 statistics and is not published here. The public instance-level release is therefore a scientific derived-data artifact, not a raw-provider dump. Other empirical artifacts are accompanied by the corresponding custody or cryptographic documentation.

## Generative-AI disclosure

OpenAI ChatGPT was used for English-language editing and to assist with drafting and checking scripts used for experimental execution, deterministic analysis and figure generation. The human author independently determined the scientific questions, experimental design, execution decisions, statistical interpretation and final manuscript content, verified the adopted scripts and outputs, and takes full responsibility for the scientific results and integrity of the work. ChatGPT is not an author.

## Author

**Kang Wang**  
College of Finance and Economics, Taiyuan University of Technology  
Taiyuan 030024, Shanxi, China  
ORCID: 0009-0006-7727-1214

## Citation

A versioned Zenodo DOI will be added to the v1.0.0 release metadata.

## Private research repository

The broader Pharos research-management repository remains private and is not required to reproduce the manuscript claims.
