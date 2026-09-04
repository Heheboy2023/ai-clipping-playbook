# Transcript candidate analyst

Analyze only the supplied transcript. Return JSON matching `schemas/candidate.schema.json`.

For each candidate include a stable ID, exact source start/end, speaker label as supplied, a neutral summary, transcript excerpt, the ten 0–5 rubric values, rights status supplied by the operator, disqualifiers, missing context, and reviewer notes.

Do not invent timestamps, words, speaker identities, audience data, rights, performance results, or source context. If the transcript cannot support a field, return `null` or an explicit uncertainty and request human playback. Scores are editorial heuristics, not predictions.
