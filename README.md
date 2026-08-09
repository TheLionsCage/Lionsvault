# LiONsVAULT

LiONsVAULT is a Pythonista-based media indexer for Apple Photos on iPhone/iPad.

## Current status

The current indexer version is **V1.2**.

A verified full V1.1 run produced:

- 33,213 total media assets
- 24,536 photos
- 8,677 videos

## Main script

`LiONsVAULT_Media_Indexer_V1_2.py`

V1.2 reuses an existing `LiONsVAULT_media_index.json`, skips already known Apple Photos asset IDs and adds only newly saved media. The CSV is regenerated from the updated complete index.

If no JSON index exists, V1.2 automatically performs a complete first index.

The script remains read-only with respect to the Apple Photos library: it does not move or delete media.

## Local data files

The generated files `LiONsVAULT_media_index.json` and `LiONsVAULT_media_index.csv` contain personal media metadata such as Apple Photos asset IDs, dates, album memberships and tags. They are intentionally **not committed** to this public repository and are protected by `.gitignore`.

## Workflow

1. Keep `LiONsVAULT_Media_Indexer_V1_2.py` and the existing JSON index in the same Pythonista folder.
2. Run the script whenever new media should be added to LiONsVAULT.
3. Known assets are skipped.
4. New photos/videos are appended to the JSON index.
5. The CSV is refreshed automatically.

## Next step

Add content-based tagging and search without changing the existing media library.
