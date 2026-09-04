# Strong-Moment Scoring Prompt

## Outcome

Score editorial candidates consistently while treating the score as a review
aid—not a virality model.

## Replace these placeholders

- `[AUDIENCE_AND_OBJECTIVE]`
- `[RUBRIC_WEIGHTS]`
- `[CANDIDATE_RECORDS]`
- `[SOURCE_CONTEXT]`

## Prompt

```text
Evaluate [CANDIDATE_RECORDS] for [AUDIENCE_AND_OBJECTIVE] using
[RUBRIC_WEIGHTS]. Use [SOURCE_CONTEXT] as the only evidence.

Score clarity, standalone value, audience fit, tension, emotion, surprise,
utility, payoff, source integrity, and visual viability from 0 to 5. Quote the
specific evidence for each score. Mark rights, privacy, sensitive context,
missing payoff, misleading implication, and poor audio/visual evidence as
disqualifiers. Never convert the score into a view, retention, revenue, or
virality prediction.

Return one structured row per candidate and a separate uncertainty note.
```

## Expected output and verification

Transfer the numeric fields into `templates/moment-scorecard.csv`, run
`clipkit candidates score`, and compare the ranking with a human score. Record
every override and its reason.

## Limitations

Weights are editorial heuristics. They need calibration for the audience and do
not prove cause or predict platform performance.

