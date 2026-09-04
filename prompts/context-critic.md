# Context-Preservation Critic

## Outcome

Detect candidate clips that become misleading when removed from their source.

## Replace these placeholders

- `[CANDIDATE]`
- `[PRECEDING_CONTEXT]`
- `[FOLLOWING_CONTEXT]`
- `[FACT_NOTES]`

## Prompt

```text
Audit [CANDIDATE] against [PRECEDING_CONTEXT], [FOLLOWING_CONTEXT], and
[FACT_NOTES]. Identify changed meaning, missing qualification, speaker-reference
errors, unresolved pronouns, sarcasm, hypothetical language, interrupted ideas,
or a payoff that occurs outside the proposed end.

Return: release, repair, or reject; the smallest defensible boundary change; any
text that must be corrected; and every uncertainty. Do not add facts or claim
that the clip is legally usable.
```

## Verification

Listen across the full context window and compare the final cut with the source.

