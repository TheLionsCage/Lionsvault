# LiONsVAULT

LiONsVAULT is a Pythonista-based media indexer for Apple Photos on iPhone/iPad.

## Current development status

The current development line is **V1.7**.

Verified archive baseline:

- 33,213 total media assets
- 24,536 photos
- 8,677 videos

## What V1.7 adds

- incremental JSON updates for newly saved media
- Apple Photos album memberships as metadata
- source tagging from app-created albums such as CapCut, TikTok, Instagram, WhatsApp, Filmora and Tempo
- Live Photo and animated-media tagging
- local Apple Vision OCR for screenshots, text images and quote candidates
- topic tagging for success, motivation, discipline, love, heartbreak, business, marketing, AI, music, techno, gaming and related themes
- visual content tagging for cars, night drives, streets, rain, clubs, stages, travel, hotels, nature, people and other reusable content motifs
- batch-based content analysis so the archive can be processed progressively

## Data safety

The Apple Photos library remains read-only. LiONsVAULT does not move or delete media.

Generated files such as `LiONsVAULT_media_index.json` and `LiONsVAULT_media_index.csv` contain private Apple Photos asset IDs, dates, album memberships and recognized text. These files are intentionally excluded from the public repository via `.gitignore`.

## Tag model

LiONsVAULT separates tags into clear layers:

- `topic:` meaning/theme, e.g. `topic:success`, `topic:heartbreak`, `topic:ai`
- `content:` visible motif, e.g. `content:car`, `content:rain`, `content:stage`
- `source:` origin/format, e.g. `source:capcut`, `source:livephoto`, `source:screenshot`
- `project:` known project context, e.g. `project:lionscage`
- `quality:` usability signals such as watermark/UI status

## Current workflow

1. Keep the current LiONsVAULT script and the existing JSON index in the same Pythonista folder.
2. Run the indexer to add newly saved media.
3. Run content analysis in batches.
4. The JSON remains the persistent archive index.
5. CSV is regenerated as a convenient review/export format.

## Next development step

Validate V1.7 content tagging on real archive batches, then add search/output workflows for practical content production.
