import photos
import console
import json
import csv
import os
from datetime import datetime

# ============================================================
# LiONsVAULT MEDIA INDEXER V1.2
# Pythonista / Apple Fotos
#
# Neu in V1.2:
# - lädt vorhandenen JSON-Index, falls vorhanden
# - überspringt bereits bekannte Asset-IDs
# - analysiert nur neue Medien
# - ergänzt neue Medien im bestehenden Index
# - CSV wird aus dem aktualisierten Gesamtindex neu erzeugt
#
# Sicherheit:
# - verändert keine Medien
# - löscht nichts
# - verschiebt nichts
# ============================================================

LAST_MONTHS = None
MAX_ASSETS = None
OUTPUT_JSON = "LiONsVAULT_media_index.json"
OUTPUT_CSV = "LiONsVAULT_media_index.csv"

PROJECT_ALBUM_RULES = {
    "lions cage": ["project:lionscage"],
    "lionscage": ["project:lionscage"],
    "musikvideos": ["project:lionscage", "use:musicvideo"],
    "dj": ["project:lionscage", "content:dj"],
    "club": ["project:lionscage", "content:club"],
    "live videos": ["project:lionscage", "content:live"],
    "remix": ["project:lionscage", "content:remix"],
    "spotify canvas": ["project:lionscage", "use:canvas"],
    "lionstech": ["project:lionstech"],
    "business": ["area:business"],
    "privat": ["area:private"],
    "urlaub": ["area:private", "content:travel"],
    "creator": ["area:creator"],
    "mc5": ["project:mc5"],
    "instagram": ["platform:instagram"],
    "tiktok": ["platform:tiktok"],
    "capcut": ["editor:capcut"],
    "filmora": ["editor:filmora"],
    "tempo": ["editor:tempo"],
}

STATUS_ALBUM_RULES = {
    "ohne wasserzeichen": ["quality:no_watermark"],
    "wasserzeichen": ["quality:watermark"],
    "watermark": ["quality:watermark"],
    "clean": ["quality:clean"],
    "reine videos": ["quality:clean"],
    "ui": ["quality:ui"],
    "screen": ["source:screen"],
    "prüfen": ["status:review"],
    "pruefen": ["status:review"],
}


def iso_date(value):
    if not value:
        return None
    try:
        return value.isoformat()
    except Exception:
        return str(value)


def add_tag(tags, value):
    if value and value not in tags:
        tags.append(value)


def add_tags(tags, values):
    for value in values:
        add_tag(tags, value)


def orientation_tag(width, height):
    if not width or not height:
        return "orientation:unknown"
    ratio = width / float(height)
    if 0.95 <= ratio <= 1.05:
        return "orientation:square"
    return "orientation:portrait" if height > width else "orientation:landscape"


def aspect_ratio_tag(width, height):
    if not width or not height:
        return None
    ratio = width / float(height)
    known = [(9/16,"format:9x16"),(16/9,"format:16x9"),(1.0,"format:1x1"),(4/5,"format:4x5"),(3/4,"format:3x4"),(4/3,"format:4x3")]
    best_ratio, best_tag = min(known, key=lambda item: abs(ratio-item[0]))
    return best_tag if abs(ratio-best_ratio) <= 0.04 else "format:other"


def duration_tags(duration):
    duration = float(duration or 0)
    tags = []
    if duration < 5:
        tags.append("duration:under5")
    elif duration <= 20:
        tags.append("duration:5-20")
    elif duration <= 60:
        tags.append("duration:21-60")
    elif duration <= 90:
        tags.append("duration:61-90")
    else:
        tags.append("duration:over90")
    if duration <= 60:
        tags.append("use:shortform_candidate")
    return tags


def resolution_tags(width, height):
    if not width or not height:
        return []
    long_side = max(width, height)
    short_side = min(width, height)
    if long_side >= 3840 or short_side >= 2160:
        return ["resolution:4k_or_higher"]
    if long_side >= 1920 or short_side >= 1080:
        return ["resolution:hd"]
    return ["resolution:below_hd"]


def asset_identifier(asset):
    try:
        return str(asset.local_id)
    except Exception:
        return str(asset)


def asset_media_type(asset):
    try:
        media_type = str(asset.media_type).lower().strip()
        if media_type == "video":
            return "video"
        if media_type == "image":
            return "photo"
    except Exception:
        pass
    return "video" if float(getattr(asset, "duration", 0) or 0) > 0 else "photo"


def asset_subtypes(asset):
    try:
        return [str(x) for x in (asset.media_subtypes or [])]
    except Exception:
        return []


def subtype_tags(subtypes):
    tags = []
    for subtype in subtypes:
        value = subtype.lower()
        if "screenshot" in value:
            add_tag(tags, "source:screenshot")
        if "screen" in value and "record" in value:
            add_tag(tags, "source:screenrecording")
        if "hdr" in value:
            add_tag(tags, "media:hdr")
        if "panorama" in value:
            add_tag(tags, "media:panorama")
    return tags


def asset_is_favorite(asset):
    try:
        return bool(asset.favorite)
    except Exception:
        return False


def album_rule_tags(album_names):
    tags = []
    for album_name in album_names:
        normalized = album_name.lower().strip()
        if "ohne wasserzeichen" in normalized:
            add_tag(tags, "quality:no_watermark")
        else:
            for needle, rule_tags in STATUS_ALBUM_RULES.items():
                if needle == "ohne wasserzeichen":
                    continue
                if needle in normalized:
                    add_tags(tags, rule_tags)
        for needle, rule_tags in PROJECT_ALBUM_RULES.items():
            if needle in normalized:
                add_tags(tags, rule_tags)
    return tags


def get_album_memberships():
    memberships = {}
    console.show_activity("Album-Zugehörigkeiten werden gelesen ...")
    try:
        albums = photos.get_albums()
        for album in albums:
            title = str(album.title or "Unbenannt")
            try:
                assets = album.assets
            except Exception:
                assets = []
            for asset in assets:
                aid = asset_identifier(asset)
                memberships.setdefault(aid, [])
                if title not in memberships[aid]:
                    memberships[aid].append(title)
    finally:
        console.hide_activity()
    return memberships


def date_allowed(asset):
    if LAST_MONTHS is None:
        return True
    creation_date = getattr(asset, "creation_date", None)
    if not creation_date:
        return False
    days = int(LAST_MONTHS * 30.4375)
    return (datetime.now() - creation_date).days <= days


def build_tags(asset, album_names):
    tags = []
    media_type = asset_media_type(asset)
    add_tag(tags, "type:" + media_type)
    width = int(getattr(asset, "pixel_width", 0) or 0)
    height = int(getattr(asset, "pixel_height", 0) or 0)
    add_tag(tags, orientation_tag(width, height))
    add_tag(tags, aspect_ratio_tag(width, height))
    add_tags(tags, resolution_tags(width, height))
    add_tags(tags, subtype_tags(asset_subtypes(asset)))
    if media_type == "video":
        add_tags(tags, duration_tags(getattr(asset, "duration", 0)))
    if asset_is_favorite(asset):
        add_tag(tags, "status:favorite")
    add_tags(tags, album_rule_tags(album_names))
    if media_type == "video" and "orientation:portrait" in tags and "resolution:below_hd" not in tags and "quality:watermark" not in tags and "quality:ui" not in tags and "source:screenrecording" not in tags:
        add_tag(tags, "use:vertical_candidate")
    return sorted(tags)


def load_existing_index():
    if not os.path.exists(OUTPUT_JSON):
        print("Kein bestehender JSON-Index gefunden.")
        print("Es wird ein vollständiger Erstindex erstellt.\n")
        return []
    try:
        with open(OUTPUT_JSON, "r", encoding="utf-8") as file:
            records = json.load(file)
        if not isinstance(records, list):
            raise ValueError("Die JSON-Datei enthält keinen gültigen LiONsVAULT-Index.")
        print(f"Bestehender Index geladen: {len(records)} Medien")
        return records
    except Exception as error:
        raise RuntimeError(f"Bestehender JSON-Index konnte nicht gelesen werden: {error}")


def load_all_assets():
    console.show_activity("Fotos und Videos werden eingelesen ...")
    try:
        images = photos.get_assets(media_type="image", include_hidden=False)
        videos = photos.get_assets(media_type="video", include_hidden=False)
    finally:
        console.hide_activity()
    print(f"Fotos in Apple Fotos:  {len(images)}")
    print(f"Videos in Apple Fotos: {len(videos)}")
    return images + videos


def build_record(asset, memberships):
    aid = asset_identifier(asset)
    album_names = memberships.get(aid, [])
    media_type = asset_media_type(asset)
    width = int(getattr(asset, "pixel_width", 0) or 0)
    height = int(getattr(asset, "pixel_height", 0) or 0)
    duration = float(getattr(asset, "duration", 0) or 0)
    return {
        "asset_id": aid,
        "type": media_type,
        "media_subtypes": asset_subtypes(asset),
        "creation_date": iso_date(getattr(asset, "creation_date", None)),
        "width": width,
        "height": height,
        "duration_seconds": round(duration, 2) if media_type == "video" else None,
        "favorite": asset_is_favorite(asset),
        "albums": album_names,
        "tags": build_tags(asset, album_names),
    }


def update_index():
    console.clear()
    print("LiONsVAULT MEDIA INDEXER V1.2")
    print("=" * 50)
    print("Update-Modus – keine Medien werden verändert.\n")
    existing_records = load_existing_index()
    known_ids = {record.get("asset_id") for record in existing_records if record.get("asset_id")}
    memberships = get_album_memberships()
    assets = load_all_assets()
    if MAX_ASSETS is not None:
        assets = assets[:MAX_ASSETS]
    new_records = []
    skipped_known = 0
    total = len(assets)
    for asset in assets:
        if not date_allowed(asset):
            continue
        aid = asset_identifier(asset)
        if aid in known_ids:
            skipped_known += 1
            continue
        new_records.append(build_record(asset, memberships))
        if len(new_records) % 100 == 0:
            print(f"{len(new_records)} neue Medien analysiert ...")
    updated_records = existing_records + new_records
    print("\n" + "=" * 50)
    print("UPDATE FERTIG")
    print("=" * 50)
    print(f"Apple Fotos gesamt:        {total}")
    print(f"Bereits bekannt:           {skipped_known}")
    print(f"Neu hinzugefügt:           {len(new_records)}")
    print(f"LiONsVAULT Index gesamt:   {len(updated_records)}")
    return updated_records, len(new_records)


def save_json(records):
    with open(OUTPUT_JSON, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def save_csv(records):
    fields = ["asset_id", "type", "media_subtypes", "creation_date", "width", "height", "duration_seconds", "favorite", "albums", "tags"]
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["media_subtypes"] = " | ".join(record.get("media_subtypes", []))
            row["albums"] = " | ".join(record.get("albums", []))
            row["tags"] = " | ".join(record.get("tags", []))
            writer.writerow(row)


def print_summary(records, new_count):
    photos_count = sum(1 for record in records if record.get("type") == "photo")
    videos_count = sum(1 for record in records if record.get("type") == "video")
    print("\nGesamtbestand:")
    print(f"Fotos:   {photos_count}")
    print(f"Videos:  {videos_count}")
    print(f"Neu:     {new_count}")
    print("\nDateien:")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_CSV}")


def main():
    records, new_count = update_index()
    save_json(records)
    save_csv(records)
    print_summary(records, new_count)
    if new_count == 0:
        message = "Der LiONsVAULT-Index ist aktuell.\n\nEs wurden keine neuen Medien gefunden."
    else:
        message = f"{new_count} neue Medien wurden ergänzt.\n\nGesamt im Index: {len(records)}"
    console.alert("LiONsVAULT Update fertig", message, "OK", hide_cancel_button=True)


if __name__ == "__main__":
    try:
        main()
    except PermissionError:
        console.alert("Kein Zugriff", "Bitte erlaube Pythonista vollständigen Zugriff auf deine Fotos.", "OK", hide_cancel_button=True)
    except Exception as error:
        console.hide_activity()
        console.alert("Fehler", str(error), "OK", hide_cancel_button=True)
        raise
