# Transcription setup

Clipkit supports the local `whisper` CLI from [OpenAI Whisper](https://github.com/openai/whisper). FFmpeg must already work.

```bash
python -m pip install -e ".[transcription]"
whisper --help
clipkit transcribe --input work/authorized-source.wav --output work/transcript --model tiny.en --language en
clipkit validate-transcript --manifest work/transcript/transcript.json
```

The output folder contains a normalized `transcript.json` and `transcript.srt`. Choose a model based on available memory, language, desired accuracy, and time; `tiny.en` is a quick English smoke-test model, not a quality recommendation.

The model may mishear names, numbers, accents, overlap, music, jargon, or low-quality speech. It does not reliably establish real speaker identity. Review the transcript against the audio, reconcile labels with `templates/speaker-map.csv`, and never silently “clean up” meaning.

Model downloads can require network access and disk space on first use. The core render workflow does not require Whisper or an API key.
