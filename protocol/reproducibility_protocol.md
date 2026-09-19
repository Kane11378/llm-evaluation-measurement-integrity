# Reproducibility protocol for fixed-bank language-model experiments

This protocol is tied to a first-planned-attempt estimand. It is not a universal rule for every deployed language-model system.

## Before exposure

Freeze:
- treatment definition;
- task/oracle and computational-necessity checks;
- instance bank;
- order/balance rules;
- model/settings/resource envelope;
- scorer and integrity ontology;
- primary estimand;
- multiplicity;
- continuation/stopping rules;
- independent inferential unit.

## During execution

- verify request identity before send;
- persist raw response bytes before parsing;
- classify completed/readable nonexact outputs as behavioral errors;
- classify true noncompletion/resource/transport/custody events as integrity failures;
- for a strict first-attempt confirmatory bank, do not retry, replace or impute after an integrity failure.

## After execution

- derive ledger fields deterministically;
- reopen raw responses in a second-pass reconciliation;
- verify completion, visible output, score and relevant metadata against the derived ledger;
- perform inference at the independent design unit;
- preserve non-detections and integrity failures as outcomes rather than repairing them into favorable evidence.

## Exploratory-to-confirmatory transition

Outcome-informed patterns may motivate a new hypothesis only on a wholly fresh, prospectively frozen bank.

## Important limitation

Fixed-bank stopping prevents silent selected continuation within an exposed bank. It does **not** prove that full-bank completion is missing-at-random across hypothetical repetitions.

A retrying production system can be a legitimate scientific target, but then the retry policy itself must be prospectively specified and the estimand changes to the policy-level output.
