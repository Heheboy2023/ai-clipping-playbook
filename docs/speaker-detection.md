# Speaker detection and reconciliation

The reference Whisper workflow transcribes speech but does not claim speaker diarization or identity. A token such as `SPEAKER_00` is a cluster label, not a person’s name.

For multi-speaker work:

1. Preserve multitrack audio and camera metadata when available.
2. Record known participants in `templates/speaker-roster.csv`.
3. Use voice, visual, turn-taking, and source notes to reconcile provisional labels in `templates/speaker-map.csv`.
4. Mark overlap, crosstalk, off-camera speech, uncertainty, and identity changes.
5. Check every candidate boundary and speaker-dependent crop against playback.

External diarization tools may suggest clusters, but version, model, language, channel layout, and error rates must be recorded. Human review remains required.
