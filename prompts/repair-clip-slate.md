# Repair a proposed clip slate

Attach the proposed slate and its source transcript. This prompt helps review
text; it is not proof that the assistant has watched media you did not supply.

```text
Review this proposed clip slate against the supplied transcript.

For each row:
1. Quote the short source phrase that supports the takeaway.
2. Mark claims that go beyond the source.
3. Identify any duplicate idea in another row.
4. List footage or audio that still needs human checking.
5. Suggest keep, merge, revise, or drop.

Do not add earnings, view predictions, or missing dialogue.
Do not treat transcript times as final media cut points.
If a visual cannot be checked from the supplied material, say so.
Return the smallest repaired slate that preserves distinct value.
```

Check quoted support yourself. Resolve media-only questions against the actual
recording before turning the repaired slate into production jobs.
