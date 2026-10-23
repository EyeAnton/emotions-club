"""Build a novel for the web player (portfolio block "novel") from a raw Emotions Club story.

Usage: python tools/build_novel.py <story.json> [--images DIR] [--title "Room 313"] [--genre thriller] [--id room_313]
All the novels at once — tools/build_library.py (it calls build() below).

Images are looked up next to the JSON the way the raw folder keeps them: "scene_01_a (Room 313).webp",
"character_01_base (Room 313).webp" (with strict=False also without the " (<title>)" suffix). Output:
assets/novels/<id>/ — novel.json (screens of the story, one line each) and the images it uses, copied as is.
Gaps in the raw images are closed: a missing background → another one of the same scene (scene_05_b → scene_05_*),
else the background of the previous screen, else the first one found; a missing character → img null (the player
leaves them off the stage); no cover → the first background.
Emotion sprites character_NN_<emotion> next to _base are picked by the stage direction of a line "(shocked) …",
same rules as gamebook-editor/tools/import_emc.py. Stdlib only.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "novels"
HEAVY = 300 * 1024  # a background heavier than this (some raw webp are lossless, ~1.2 MB) becomes a JPEG
SIPS = shutil.which("sips")  # macOS; elsewhere heavy backgrounds are copied as is
# accent colour of the player per genre — the same as GENRES in gamebook-editor (Stasik)
GENRES = {"default": "#ffb040", "thriller": "#962836", "romance": "#d4708c", "adventure": "#60ac96",
          "horror": "#809646", "scifi": "#5aaadc", "fantasy": "#8a6cd8", "mystery": "#5a78b4", "comedy": "#e0a040"}
EMOTIONS = {
    "angry": ["furious", "angr", "cold", "sharp", "snap", "mad", "glar", "fierce", "harsh", "bitter", "curt", "frown", "jaw", "yell", "danger"],
    "happy": ["smil", "laugh", "grin", "amused", "lightly", "cheer", "warm", "relie", "genuine", "gentl"],
    "sad": ["sad", "hurt", "tear", "broken", "sorrow", "quiet", "soft", "sigh", "shaken", "weak", "fading"],
    "surprised": ["shock", "surpris", "startl", "stunned", "gasp"],
    "scared": ["scared", "afraid", "fear", "panic", "tense", "strained", "nervous", "urgent", "alert", "whisper"],
    "flirty": ["teas", "flirt", "smirk", "playful", "mock", "sly"],
    "serious": ["flat", "grim", "firm", "low", "dry", "calm", "focused"],
}


def find_image(folder, name, title, strict=False):
    """scene_01_a.webp → the raw file: "scene_01_a (Room 313).webp", then .png/.jpg; without the suffix unless strict."""
    stem = Path(name).stem
    for s in (f"{stem} ({title})",) + (() if strict else (stem,)):
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


def options(s):
    """Options of a choice: a list "options" or flat fields option-0-id / option-0-text / option-0-price."""
    if s.get("options"):
        return s["options"]
    return [{"id": s[f"option-{i}-id"], "text": s.get(f"option-{i}-text") or ""} for i in range(9) if s.get(f"option-{i}-id")]


def build(json_path, images_dir=None, title=None, genre="thriller", id=None, strict=False, display=None):
    """One novel → assets/novels/<id>/. title — as in the raw file names, display — as shown (default: title). Returns a summary: id, title, screens, choices, endings, words, cover, fallbacks."""
    src = Path(json_path)
    data = json.loads(src.read_text(encoding="utf-8"))
    tale = next(iter(data["tales"].values())) if "tales" in data else data
    title = title or tale["id"].replace("_", " ").title()
    nid = id or tale["id"]
    folder = Path(images_dir) if images_dir else src.parent
    out = OUT / nid
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    key = re.sub(r"[^a-z]", "", genre.lower())
    files, fallbacks = {}, []  # output name → raw file

    def put(p, stem=None, flat=True):
        """flat — a background (no transparency): a heavy one is re-encoded to JPEG on copy"""
        stem = stem or Path(p.name).stem.replace(f" ({title})", "")
        name = stem + (".jpg" if flat and SIPS and p.stat().st_size > HEAVY else p.suffix)
        files[name] = p
        return name

    def img(name, flat=True):
        p = name and find_image(folder, name, title, strict)
        return put(p, Path(name).stem, flat) if p else None

    # every background of this story in the raw folder, for the fallbacks
    bgs = sorted(f for f in folder.iterdir() if f.name.endswith(f" ({title}){f.suffix}") and re.match(r"(scene|cutscene)", f.name)
                 and f.suffix in (".webp", ".png", ".jpg"))
    rank = {".webp": 0, ".png": 1, ".jpg": 2}
    bgs = sorted({f.name[:-len(f" ({title}){f.suffix}")]: f
                  for f in sorted(bgs, key=lambda f: -rank[f.suffix])}.items())  # stem → file, webp wins
    last = None

    resolved = {}

    def bg(name):
        nonlocal last
        if name in resolved:
            got = resolved[name]
            last = got or last
            return got
        got = img(name)
        if not got:
            stem = Path(name or "").stem
            m = re.match(r"(scene_\d+)", stem)
            same = [f for st, f in bgs if m and st.startswith(m[1] + "_")]
            if same:
                got = put(same[0])
            elif last:
                got = last
            elif bgs:
                got = put(bgs[0][1])
            fallbacks.append(f"{name} → {got}")
        resolved[name] = got
        last = got or last
        return got

    players = [c["id"] for c in tale["characters"] if c.get("type") == "player"]
    sprites = {c["id"]: emotion_sprites(folder, c["image"], title) for c in tale["characters"]}
    chars = {}
    for c in tale["characters"]:
        side = "left" if players[:1] == [c["id"]] else "right" if c["id"] in players else None
        im = img(c["image"], flat=False)
        if not im:
            fallbacks.append(f"{c['image']} ({c['name']}) → null")
        chars[c["id"]] = {"name": c["name"], "img": im, "side": side,
                          "emo": {e: img(f, flat=False) for e, f in sprites[c["id"]].items()}}

    screens = {}
    for s in tale["screens"]:  # a choice has two screens with one id: "block" (wait for the partner) and "choice"
        if s["type"] == "block":
            continue
        actor = s.get("actor") or {}
        who = actor.get("playerId") or actor.get("npcId") or actor.get("characterId")
        text = re.sub(r"\s*\n\s*", " ", re.sub(r"</?\w+>", "", s.get("content") or "").strip())
        if s["type"] == "final":  # "discuss the ending in the chat" is about the app; there is no chat here
            text = re.sub(r"\s*[^.?!]*\bin the chat\b[^.?!]*[.?!]", "", text)
        o = {"t": s["type"], "bg": bg(s.get("image")), "text": text, "p": s.get("progress", 0)}
        if s["type"] == "scene":
            o["title"] = s.get("title") or ""
        if s["type"] == "dialog":
            o["who"] = who
            e = emotion_of(text, sprites.get(who))
            if e:
                o["emo"] = e
        if s["type"] == "choice":
            o["by"] = s.get("availableFor")
            o["opts"] = [{"text": x["text"], "to": x["id"]} for x in options(s)]
        elif s.get("next"):
            o["next"] = s["next"]
        screens[s["id"]] = o

    cover = find_image(folder, "cover", title, strict)
    if cover:
        cover = put(cover, "cover")
    else:
        first = next((s["bg"] for s in screens.values() if s["bg"]), None)
        cover = put(files[first], "cover") if first else None
        fallbacks.append(f"cover → {first}")
    for name, p in files.items():
        if name.endswith(".jpg") and p.suffix != ".jpg" or (p.suffix == ".jpg" and p.stat().st_size > HEAVY and SIPS):
            subprocess.run([SIPS, "-Z", "900", "-s", "format", "jpeg", "-s", "formatOptions", "66", str(p),
                            "--out", str(out / name)], check=True, capture_output=True)
        else:
            shutil.copyfile(p, out / name)
    start = tale["firstScreenId"]
    novel = {"id": nid, "title": display or title, "genre": genre.title() if genre.islower() else genre,
             "accent": GENRES.get(key, GENRES["default"]), "start": start,
             "length": tale.get("maxBranchLength") or max(s["p"] for s in screens.values()),
             "cover": cover, "chars": chars, "screens": screens}
    (out / "novel.json").write_text(json.dumps(novel, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # words of one playthrough on average: every option equally likely
    memo = {}

    def words(k, seen=()):
        if k in memo:
            return memo[k]
        s = screens.get(k)
        if not s or k in seen:
            return 0
        nx = [o["to"] for o in s.get("opts", [])] or ([s["next"]] if s.get("next") else [])
        w = len(s["text"].split()) + (sum(words(n, seen + (k,)) for n in nx) / len(nx) if nx else 0)
        memo[k] = w
        return w

    import sys
    sys.setrecursionlimit(max(10000, len(screens) * 4))
    size = sum(f.stat().st_size for f in out.iterdir()) // 1024
    summary = {"id": nid, "title": display or title, "screens": len(screens), "images": len(files), "kb": size, "cover": cover,
               "choices": sum(s["t"] == "choice" for s in screens.values()),
               "endings": sum(not s.get("next") and not s.get("opts") for s in screens.values()),
               "words": round(words(start)), "fallbacks": fallbacks}
    print(f"«{title}»: {len(screens)} screens, {len(files)} images, {size} KB → {out}"
          + "".join(f"\n  fallback {f}" for f in fallbacks))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--images", help="folder with the images (default: next to the JSON)")
    ap.add_argument("--title", help="default: from the id, room_313 → Room 313")
    ap.add_argument("--genre", default="thriller", choices=GENRES)
    ap.add_argument("--id", help="folder and id of the novel (default: the id in the JSON)")
    a = ap.parse_args()
    build(a.json, a.images, a.title, a.genre, a.id)


if __name__ == "__main__":
    main()
