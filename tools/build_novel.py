"""Build a novel for the web player (portfolio block "novel") from a raw Emotions Club story.

Usage: python tools/build_novel.py <story.json> [--images DIR] [--title "Room 313"] [--genre thriller]

Images are looked up next to the JSON the way the raw folder keeps them: "scene_01_a (Room 313).webp",
"character_01_base (Room 313).webp" (the " (<title>)" suffix is optional). Output: assets/novels/<id>/ —
novel.json (screens of the story, one line each) and the webp files it uses, copied as is.
Emotion sprites character_NN_<emotion> next to _base are picked by the stage direction of a line "(shocked) …",
same rules as gamebook-editor/tools/import_emc.py. Stdlib only.
"""
import argparse
import json
import re
import shutil
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "novels"
# accent colour of the player per genre — the same as GENRES in gamebook-editor (Stasik)
GENRES = {"default": "#ffb040", "thriller": "#962836", "romance": "#d4708c", "adventure": "#60ac96",
          "horror": "#809646", "scifi": "#5aaadc"}
EMOTIONS = {
    "angry": ["furious", "angr", "cold", "sharp", "snap", "mad", "glar", "fierce", "harsh", "bitter", "curt", "frown", "jaw", "yell", "danger"],
    "happy": ["smil", "laugh", "grin", "amused", "lightly", "cheer", "warm", "relie", "genuine", "gentl"],
    "sad": ["sad", "hurt", "tear", "broken", "sorrow", "quiet", "soft", "sigh", "shaken", "weak", "fading"],
    "surprised": ["shock", "surpris", "startl", "stunned", "gasp"],
    "scared": ["scared", "afraid", "fear", "panic", "tense", "strained", "nervous", "urgent", "alert", "whisper"],
    "flirty": ["teas", "flirt", "smirk", "playful", "mock", "sly"],
    "serious": ["flat", "grim", "firm", "low", "dry", "calm", "focused"],
}


def find_image(folder, name, title):
    """scene_01_a.webp → the raw file: "scene_01_a (Room 313).webp", then .png/.jpg, then without the suffix."""
    stem = Path(name).stem
    for s in (f"{stem} ({title})", stem):
        for ext in (".webp", ".png", ".jpg"):
            p = folder / (s + ext)
            if p.exists():
                return p
    return None


def emotion_sprites(folder, image, title):
    prefix = re.sub(r"base$", "", Path(image).stem)
    out = {}
    for f in folder.iterdir():
        m = re.fullmatch(re.escape(prefix) + r"([a-z]+)(?: \((.+)\))?\.(webp|png|jpg)", f.name, re.I)
        if m and m[1].lower() != "base" and (not m[2] or m[2] == title):
            out.setdefault(m[1].lower(), f"{prefix}{m[1].lower()}.webp")
    return out


def emotion_of(text, sprites):
    m = re.match(r"\s*\(([^)]*)\)", text or "")
    if not m or not sprites:
        return None
    note = m[1].lower()
    return next((e for e in sprites if e in note or any(w in note for w in EMOTIONS.get(e, []))), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--images", help="folder with the images (default: next to the JSON)")
    ap.add_argument("--title", help="default: from the id, room_313 → Room 313")
    ap.add_argument("--genre", default="thriller", choices=GENRES)
    a = ap.parse_args()
    src = Path(a.json)
    data = json.loads(src.read_text(encoding="utf-8"))
    tale = next(iter(data["tales"].values())) if "tales" in data else data
    title = a.title or tale["id"].replace("_", " ").title()
    folder = Path(a.images) if a.images else src.parent
    out = OUT / tale["id"]
    out.mkdir(parents=True, exist_ok=True)

    used = set()

    def img(name):
        if name and find_image(folder, name, title):
            used.add(name)
            return Path(name).stem + ".webp"
        print("  ! no image", name)
        return None

    players = [c["id"] for c in tale["characters"] if c.get("type") == "player"]
    sprites = {c["id"]: emotion_sprites(folder, c["image"], title) for c in tale["characters"]}
    chars = {}
    for c in tale["characters"]:
        side = "left" if players[:1] == [c["id"]] else "right" if c["id"] in players else None
        chars[c["id"]] = {"name": c["name"], "img": img(c["image"]), "side": side,
                          "emo": {e: img(f) for e, f in sprites[c["id"]].items()}}
        if sprites[c["id"]]:
            print(f"  {c['name']}: emotions {', '.join(sorted(sprites[c['id']]))}")

    screens = {}
    for s in tale["screens"]:  # a choice has two screens with one id: "block" (wait for the partner) and "choice"
        if s["type"] == "block":
            continue
        actor = s.get("actor") or {}
        who = actor.get("playerId") or actor.get("npcId") or actor.get("characterId")
        text = re.sub(r"\s*\n\s*", " ", (s.get("content") or "").strip())
        if s["type"] == "final":  # "discuss the ending in the chat" is about the app; there is no chat here
            text = re.sub(r"\s*[^.?!]*\bin the chat\b[^.?!]*[.?!]", "", text)
        o = {"t": s["type"], "bg": img(s["image"]), "text": text, "p": s.get("progress", 0)}
        if s["type"] == "scene":
            o["title"] = s.get("title") or ""
        if s["type"] == "dialog":
            o["who"] = who
            e = emotion_of(text, sprites.get(who))
            if e:
                o["emo"] = e
        if s["type"] == "choice":
            o["by"] = s.get("availableFor")
            o["opts"] = [{"text": x["text"], "to": x["id"]} for x in s["options"]]
        elif s.get("next"):
            o["next"] = s["next"]
        screens[s["id"]] = o

    cover = find_image(folder, "cover", title)
    if cover:
        used.add("cover")
    novel = {"id": tale["id"], "title": title, "genre": a.genre.title(), "accent": GENRES[a.genre], "start": tale["firstScreenId"],
             "length": tale.get("maxBranchLength") or max(s["p"] for s in screens.values()),
             "cover": "cover.webp" if cover else None, "chars": chars, "screens": screens}
    for name in used:
        p = find_image(folder, name, title)
        if p.suffix != ".webp":
            print("  ! not webp, copied as is:", p.name)
        shutil.copyfile(p, out / (Path(name).stem + ".webp"))
    (out / "novel.json").write_text(json.dumps(novel, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    size = sum(f.stat().st_size for f in out.iterdir()) // 1024
    print(f"«{title}»: {len(screens)} screens, {len(used)} images, {size} KB → {out}")


if __name__ == "__main__":
    main()
