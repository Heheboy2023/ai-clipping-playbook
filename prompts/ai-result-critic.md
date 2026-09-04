# AI Clipping Result Critic

## Outcome

Classify every automated action as accept, correct, replace, or reject.

## Replace these placeholders

- `[SOURCE_RECORD]`
- `[AI_CANDIDATE]`
- `[CORRECTION_LOG]`
- `[ACCEPTANCE_CRITERIA]`

## Prompt

```text
Review [AI_CANDIDATE] against [SOURCE_RECORD], [CORRECTION_LOG], and
[ACCEPTANCE_CRITERIA]. Check boundaries, meaning, speaker, crop, captions,
visual obstruction, audio artifacts, music rights notes, export settings, and
missing context. For each field, return accept, correct, replace, or reject with
source-grounded evidence. Do not estimate time saved or expected performance.
```

## Verification

The result is an exception queue, not approval. A human must inspect and play the
complete export.

