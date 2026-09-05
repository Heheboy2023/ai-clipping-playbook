# Transcript Candidate Analyst

## Outcome

Return a source-grounded candidate list from a supplied transcript without
inventing words, timestamps, speakers, facts, or performance predictions.

## Replace these placeholders

- `[AUDIENCE]`
- `[PAGE_OBJECTIVE]`
- `[MAX_CANDIDATES]`
- `[TRANSCRIPT]`

## Prompt

```text
You are reviewing a transcript for [AUDIENCE]. The page objective is
[PAGE_OBJECTIVE]. Identify at most [MAX_CANDIDATES] candidate moments.

Use only [TRANSCRIPT]. Do not infer words that are absent. For each candidate,
return candidate_id, start, end, speakers, a one-sentence summary, the exact
supporting transcript excerpt, required preceding context, payoff, uncertainty,
and rejection risks. Timestamps must come from the supplied transcript. If a
moment lacks context, a payoff, or reliable timing, reject it rather than repair
it from memory.

For a beginner reading the result, use a short table and include the exact first
and last words to search for. Use supplied time markers as search ranges; do not
invent precise cut times inside a paragraph. Do not predict views.

If I explicitly ask for machine-readable output, return JSON matching the
attached schemas/candidate.schema.json. Use numeric elapsed seconds for start
and end, and include source_excerpt and uncertainty. Do not claim the file
matches a schema that you have not received.
```

## Expected output and verification

Validate the JSON, locate every excerpt in the transcript, then listen from at
least 3 seconds before the proposed start through 3 seconds after the proposed
end. Correct words, speakers, timing, and context before approval.

## Limitations

Transcript analysis cannot establish rights, identity, truth, sensitive context,
or likely performance. A human must review the source media.
