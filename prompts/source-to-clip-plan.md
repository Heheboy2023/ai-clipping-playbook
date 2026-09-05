# One source to a clip plan

Use after checking the transcript and defining the audience. This creates a slate, not rendered videos.

```text
Build a clip plan from this transcript.

Audience: [AUDIENCE]
Page promise: [WHAT PEOPLE COME HERE FOR]
Topic buckets: [THREE SIMPLE TOPICS]
Transcript: [TEXT OR ATTACHED FILENAME]

Find up to six distinct ideas. For each, give a clip ID, source search range,
exact opening and ending words, one-sentence takeaway, moment type, topic
bucket, setup needed, picture or sound to check, and how it differs from
the others. Do not invent dialogue, footage, or exact times inside paragraphs.
Return fewer than six when the source is thin.

Suggest three to edit first. Explain the order and flag missing media.
```

Save checked results in `templates/candidate-slate.csv`. It is an editorial planning table, not automatically a machine-ready batch manifest. Use `examples/clip-room/transcript.txt` only as the fictional text exercise it is labeled as.
