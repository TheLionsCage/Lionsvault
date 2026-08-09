# LiONsVAULT

LiONsVAULT is a Pythonista-based media indexer for Apple Photos on iPhone/iPad.

## Current development status

Current validated development version: **V2.2**.

Latest validation run:

- Index total: 33,216 media records
- Batch processed: 500/500
- Problem assets: 0
- Analysis version: `analysis:vision_v7`

## V2.2 changes

- Topic keywords match as complete words/phrases instead of arbitrary substrings.
- Prevents false topic matches such as `ki` inside OCR noise.
- `content:data_screen` is narrowly defined as charts, graphs, statistics, budgets, KPIs, financial/numeric data, spreadsheets and analytics views.
- A vehicle dashboard alone does not create `content:data_screen`.
- OCR filtering targets useful text, quote/topic content, TikTok/Instagram/LiONsCAGE watermark markers and relevant UI signals.
- OCR storage remains intentionally limited to reduce noise.
- Per-asset diagnostics and local problem-asset skip handling remain active.

## Core capabilities

- incremental JSON updates for newly saved media
- Apple Photos album memberships as metadata
- source tagging from app-created albums such as CapCut, TikTok, Instagram, WhatsApp, Filmora and Tempo
- Live Photo and animated-media tagging
- local Apple Vision OCR and visual classification
- quote/text candidate recognition
- topic tagging for personal development, relationships, business, marketing, AI, music, techno, gaming and related themes
- visual content tagging for reusable archive motifs
- batch-based analysis for large Apple Photos libraries

## Data safety

The Apple Photos library remains read-only. LiONsVAULT does not move or delete media.

Generated `LiONsVAULT_media_index.json`, `LiONsVAULT_media_index.csv` and local problem-asset data can contain private Apple Photos identifiers, dates, album memberships and recognized text. These files must remain excluded from the public repository.

## Tag model

- `topic:` semantic theme
- `content:` visible/content motif
- `source:` origin or media subtype
- `project:` reliable project context
- `quality:` usability, watermark or UI signal
- `analysis:` analysis/version state

## Current workflow

1. Keep the current script and persistent JSON index in the same Pythonista folder.
2. Run analysis in controlled batches.
3. Existing analyzed records are retained according to the current analysis version.
4. JSON is the persistent archive index; CSV is the review/export format.
5. Problem assets are logged locally instead of blocking the complete archive run.

## Validation status

V2.2 completed a 500-asset validation batch successfully with zero problem assets. The current next step is continued archive processing with the validated V2.2 logic.
