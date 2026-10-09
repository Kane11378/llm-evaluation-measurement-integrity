# Prospective v1.1.0 archive checklist

**Status: unreleased.** This checklist prepares the next reproducibility archive. It does not authorize a merge, tag, GitHub Release or Zenodo publication. The author must approve the exact final public contents after independent review.

## Public contents and scientific review

- [ ] Freeze the reviewed public Git commit and identify the exact proposed version.
- [ ] Confirm the archive contains only the approved public software, dependency specifications, derived scientific data, protocols, research figures, citation metadata, license notices and release documentation.
- [ ] Inspect every public file, including visible figure text, SVG comments, embedded images and PDF/PNG metadata, for personal paths, internal engineering labels, conversation residue and unintended production annotations.
- [ ] Compare both empirical instance-level datasets and frozen scalar results with their accepted scientific baseline; preserve all observations, ordering, estimates, confidence intervals and p values.
- [ ] Reconcile Figure 3's public figure data, caption and exports with the final journal presentation figure. Record which artwork is archived. Preserve the same evidence, source boundaries and negative results; presentation differences alone do not authorize changes to scientific content.
- [ ] Verify the scoped MIT software grant, CC BY 4.0 author-owned original data/figure/documentation grant and third-party notices.

## Reproduction and file identities

- [ ] Run the repository's native reproducibility workflow on the exact public candidate commit, in its pinned dependency environment.
- [ ] Confirm independent N=28 and N=124 recomputation, every deterministic sensitivity surface and analytic identity, all frozen table/source checks and Figure 1–4 rendering pass without provider/model calls.
- [ ] Run `python analysis/verify_archive.py` against the frozen public tree before generators write new outputs. Verify every listed file's SHA-256 and byte count and the exact inventory. The manifest excludes itself to avoid a recursive checksum.
- [ ] Verify all 12 frozen Figure 1–4 exports against `figures/FINAL_FIGURE_SHA256_MANIFEST.json`, including byte counts and SHA-256. Preserve publication files separately from regenerated outputs.
- [ ] Confirm corrected-N=28 data hashes and the retained scientific custody identifiers. Distinguish verified file identity and recomputation from author-reported historical custody.
- [ ] Rebuild the complete public manifest after any accepted file change, then repeat the affected validation and outward-facing inspection.

## Metadata and publication gate

- [ ] Obtain independent acceptance of the complete public candidate and final figure selection, followed by author approval to merge and publish.
- [ ] Confirm the final version number and real publication date. Synchronize README, release notes, `CITATION.cff` and `.zenodo.json`; replace the prospective/unreleased wording only when publication is authorized.
- [ ] Check both citation and Zenodo metadata. Zenodo's GitHub integration prioritizes `.zenodo.json` when both metadata files exist, so both must have accurate titles, authors, versions and component-license descriptions. See [Zenodo metadata guidance](https://help.zenodo.org/docs/github/describe-software/zenodo-json/).
- [ ] Review the release automation explicitly before enabling publication. Preserve the historical v1.0.0 tag, archived bytes and original version DOI.
- [ ] Use a new archival version for the changed files; verify the integration or new-version deposit will archive exactly the approved public bytes. See [Zenodo version guidance](https://help.zenodo.org/docs/deposit/manage-versions/).
- [ ] Record a new version-specific DOI only after it is actually allocated and verified; confirm its relationship to the archive series. Never use the old version DOI as the identity of new files.
- [ ] Download and verify the final archived file inventory and checksums against the approved release contents. Record the real release commit and archive URL.
- [ ] Synchronize signed manuscript, signed Supplement, availability statements and other current-version citations with the verified new archive. Keep identifying repository/DOI references out of blinded submission variants and preserve authoritative formal AI declarations.

The historical [v1.0.0 DOI](https://doi.org/10.5281/zenodo.22846957) remains a reference to the original snapshot. The planned v1.1.0 candidate has no assigned archive DOI or release date.
