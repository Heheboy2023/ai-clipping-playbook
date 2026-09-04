# Caption Cleanup Without Meaning Changes

## Outcome

Correct punctuation, casing, and line breaks while preserving the spoken words.

## Replace these placeholders

- `[CAPTION_SEGMENTS]`
- `[KNOWN_NAMES_AND_TERMS]`
- `[MAX_CHARACTERS_PER_LINE]`

## Prompt

```text
Clean [CAPTION_SEGMENTS] using [KNOWN_NAMES_AND_TERMS]. Preserve every spoken
claim and timestamp. Correct obvious transcription errors only when the supplied
reference proves the correction. Improve punctuation and line breaks, with no
more than [MAX_CHARACTERS_PER_LINE] characters per line where natural.

Flag uncertain words instead of guessing. Keep speaker labels and meaningful
non-speech audio. Return the same segment IDs and timestamps.
```

## Verification

Read each caption while listening to the source and inspect the rendered frame.

