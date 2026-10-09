# Figure sources and presentation

The archive contains reproducible views of the scientific constructions and source data used in the paper. Its figures use the layouts in [the public renderer](../analysis/reproduce_figures.py). The paper uses separate presentation layouts for Figures 1, 3 and 4. Shared scientific content does not imply identical graphics, panel placement or file bytes.

## Figure 1: identification and measurement

Figure 1 is a schematic with four panels defined explicitly in the renderer: matched provenance-role reassignment, computational necessity, the measurement chain, and identification versus detection. The labels `z=0` and `z=1` and the swapped provenance roles are design illustrations, not estimated effects. The [pipeline nodes](../figure_data/fig1_pipeline_nodes.csv) and [edges](../figure_data/fig1_pipeline_edges.csv) document the measurement relationships; the renderer defines their displayed arrangement in code rather than reading those CSVs as layout instructions.

The scientific construction keeps task-relevant information and operating conditions fixed, compares otherwise matched worlds to establish task-level necessity, retains completed/readable nonexact outputs as errors, and distinguishes absent or unreadable planned observations from behavioral errors. Identification and statistical detection remain separate. The paper presents the same four constructions in a compact layout with explicit directional arrows and mathematical labels. Neither view establishes an internal neural mechanism. The [identification framework](identification_framework.md) and [reproducibility protocol](reproducibility_protocol.md) define these boundaries.

## Figure 3: historical failures and prospective safeguards

Figure 3 is rendered directly from the seven rows in [the empirical ladder](../figure_data/fig3_empirical_ladder.csv). The archive presents the stages from top to bottom; the paper arranges them as numbered cards with arrows denoting chronological order. The failures, safeguards, reported counts and statistical results agree across the two layouts. The paper's instructions for reading its card sequence apply to that layout.

Both views preserve the historical exclusion boundaries: earlier measurement repairs do not create confirmation; the interrupted sample has no confirmatory prefix and is not replayed or resumed; resource qualification is nonconfirmatory; and the wholly fresh N=124 primary did not confirm the positive depth contrast. The sequence represents measurement hardening, not accumulation of positive evidence.

The [public evidence-availability document](evidence_provenance.md) distinguishes statistical results recomputable from released derived data from author-reported historical events. Original raw responses, transport fields, qualification records and custody/adjudication records are author-held and are not included here. Rendering a source row does not independently verify those historical records.

## Figure 4: estimates and inference boundaries

Both layouts plot the same nine estimates in [the frozen effect table](../figure_data/fig4_effect_estimates.csv), with only the two confidence intervals already supplied for the corrected N=28 overall primary and the fresh N=124 depth primary. The archive uses a single forest plot. The paper groups the same rows into four panels: corrected overall primary, first-sample exploratory stages and post-hoc slope, fresh depth primary, and fresh stage secondaries. Numerical labels in the paper use documented display rounding of the same stored values.

The corrected overall result is a non-detection, not equivalence. First-sample stage effects and the post-hoc depth slope remain exploratory; no stage secondary passes the prespecified Holm-adjusted .05 threshold. The fresh positive depth contrast was not confirmed, its primary gate is closed, and its stage secondaries support no stage-specific confirmatory claim. Point-only rows receive no newly calculated confidence intervals. See the [claim boundaries](claim_boundaries.md), [corrected result](../empirical/corrected_n28_result.json) and [fresh result](../empirical/fresh_n124_result.json).

Frozen figures are identified by [the figure manifest](../figures/FINAL_FIGURE_SHA256_MANIFEST.json). Regeneration can produce different file bytes across rendering environments while retaining these constructions, values and inference boundaries. It does not recreate the paper's separate presentation assets or replay historical model behavior.
