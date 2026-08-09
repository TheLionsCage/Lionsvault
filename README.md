# LiONsVAULT

LiONsVAULT is a Pythonista-based media indexer for Apple Photos on iPhone/iPad.

## Current status

The current indexer version is **V1.1**. It reads photos and videos, keeps existing Apple Photos album memberships as metadata, and writes a local JSON/CSV index.

A verified full run produced:

- 33,213 total media assets
- 24,536 photos
- 8,677 videos

## Main script

`LiONsVAULT_Media_Indexer_V1_1.py`

The script is read-only with respect to the Apple Photos library: it does not move or delete media.

## Local data files

The generated files `LiONsVAULT_media_index.json` and `LiONsVAULT_media_index.csv` contain personal media metadata such as Apple Photos asset IDs, dates, album memberships and tags. They are intentionally **not committed** to this public repository.

## Next step

The next development step is incremental updating: reuse the existing JSON index and add only new media instead of rebuilding the complete archive on every run.
