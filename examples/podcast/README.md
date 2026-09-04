# Podcast clipping example

This fixture models a creator-supplied video podcast. It cuts a reviewed moment, reframes it vertically, burns reviewed captions, and normalizes the final audio. The manifest already marks synthetic fixture rights and editorial selection as confirmed; replace both decisions when adapting it to real material.

Dry run: `clipkit run --manifest examples/podcast/job.yaml --dry-run`

Execute locally: `clipkit run --manifest examples/podcast/job.yaml`

Then watch the outputs in full before recording approval. Clipkit never publishes them.
