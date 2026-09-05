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

This is the advanced ten-criterion worksheet. Chapter 4's simpler five-point
sheet is `templates/moment-finder.csv`; it is not input for this command.

Copy the scorecard to your work folder before filling it in. Enter `start` and
`end` as seconds from the beginning of the source, not timecode strings. Keep
the exact column names. Add a real summary and scores from 0 to 5. Set
`rights_clear` to `true` only when your source use is settled; otherwise the
tool leaves that row out of the eligible ranking. Use `disqualifier` for a
specific reason a clip cannot work, such as a missing payoff.

This runnable example scores the untouched template. Its placeholder is
correctly excluded from the eligible list:

```bash
clipkit candidates score --input templates/moment-scorecard.csv --output work/scoring/template-result.csv
```

For your filled copy, replace the input path with its location. The default
equal weights produce a total from 0 to 50, not a percentage and not a view
forecast. Compare the order with your own judgment and note why you disagree.

## Limitations

Weights are editorial heuristics. They need calibration for the audience and do
not prove cause or predict platform performance.
