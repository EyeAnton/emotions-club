"""Build every Emotions Club novel for the portfolio player and the library it opens with.

Usage: python3 tools/build_library.py [RAW_DIR]   (default: ~/Downloads/Portfolio/Emotions Club)

Each novel → assets/novels/<id>/ (tools/build_novel.py build(), images looked up strictly by the " (<title>)" suffix),
plus thumb.jpg — the cover at 360px (sips, macOS). assets/novels/library.json lists them for the player: the free ones
first (they can be played), then the premium ones (a badge for now) from the shortest. minutes — an average
playthrough at 200 words a minute.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_novel import OUT, build  # noqa: E402

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "Downloads" / "Portfolio" / "Emotions Club")
FREE = ["room_313", "talk_on_the_plane", "stuck_in_the_elevator", "moonlight_heist"]
# id (= the raw JSON name): title in the raw image names, title on the site, genre
NOVELS = {
    "crimson_masquerade": ("Crimson Masquerade", "Crimson Masquerade", "Horror"),
    "cursed_crown": ("The Cursed Crown", "The Cursed Crown", "Fantasy"),
    "daughter_of_the_flame": ("Daughter of the Flame", "Daughter of the Flame", "Fantasy"),
    "echoes_of_peru": ("Echoes of Peru", "Echoes of Peru", "Adventure"),
    "hotel_mixup": ("Hotel Mix Up", "Hotel Mix-Up", "Romance"),
    "midnight_pact": ("Midnight Pact", "Midnight Pact", "Comedy"),
    "midnight_pitch_for_two": ("Midnight Pitch for Two", "Midnight Pitch for Two", "Romance"),
    "moonlight_heist": ("Moonlight Heist", "Moonlight Heist", "Adventure"),
    "new_year_with_the_ex": ("New Year with the Ex", "New Year with the Ex", "Comedy"),
    "private_lesson": ("Private Lesson", "Private Lesson", "Romance"),
    "raiders_of_the_forgotten_star": ("Raiders of the Forgotten Star", "Raiders of the Forgotten Star", "Sci-Fi"),
    "resort_fling": ("Resort Fling", "Resort Fling", "Romance"),
    "room_313": ("Room 313", "Room 313", "Thriller"),
    "share_the_bed": ("Share the Bed?", "Share the Bed?", "Romance"),
    "song_of_the_sea_court": ("Song of the Sea Court", "Song of the Sea Court", "Fantasy"),
    "stuck_in_the_elevator": ("Stuck in the Elevator", "Stuck in the Elevator", "Comedy"),
    "talk_on_the_plane": ("Talk on the Plane", "Talk on the Plane", "Romance"),
    "the_archivists_code": ("The archivist`s code", "The Archivist's Code", "Thriller"),
    "the_double_life": ("The Double Life", "The Double Life", "Thriller"),
    "the_enchanted_stranger": ("The Enchanted Stranger", "The Enchanted Stranger", "Fantasy"),
    "the_ghost_in_4b": ("Ghost in 4b", "The Ghost in 4B", "Mystery"),
    "the_island_escape": ("The Island Escape", "The Island Escape", "Adventure"),
    "the_night_that_lingers": ("The Night That Lingers", "The Night That Lingers", "Romance"),
    "the_rivals_touch": ("Rival`s Touch", "Rival's Touch", "Romance"),
    "the_thirst_pact": ("The Thirst Pact", "The Thirst Pact", "Fantasy"),
    "the_witch_next_door": ("The Witch Next Door", "The Witch Next Door", "Mystery"),
    "threads_of_the_moon": ("Threads of the Moon", "Threads of the Moon", "Fantasy"),
    "treasure_of_two": ("Treasure Of Two", "Treasure of Two", "Adventure"),
}


def main():
    items = []
    for nid, (title, display, genre) in NOVELS.items():
        s = build(RAW / f"{nid}.json", RAW, title, genre, id=nid, strict=True, display=display)
        d = OUT / nid
        subprocess.run(["sips", "-Z", "360", "-s", "format", "jpeg", "-s", "formatOptions", "78",
                        str(d / s["cover"]), "--out", str(d / "thumb.jpg")], check=True, capture_output=True)
        items.append({"id": nid, "title": display, "genre": genre, "free": nid in FREE,
                      "src": f"{nid}/novel.json", "cover": f"{nid}/{s['cover']}", "thumb": f"{nid}/thumb.jpg",
                      "minutes": max(1, round(s["words"] / 200)), "choices": s["choices"], "endings": s["endings"],
                      "_words": s["words"]})
    items.sort(key=lambda x: (FREE.index(x["id"]) if x["free"] else len(FREE), x["_words"]))
    for x in items:
        del x["_words"]
    (OUT / "library.json").write_text(json.dumps({"novels": items}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"library.json: {len(items)} novels, {sum(x['free'] for x in items)} free")


if __name__ == "__main__":
    main()
