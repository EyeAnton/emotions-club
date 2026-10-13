"""Build web assets for the case page from the raw portfolio folder.

Usage: python tools/build_assets.py [SRC_DIR]
Default SRC_DIR is the Yandex.Disk portfolio folder. Needs ffmpeg (FFMPEG env var or on PATH).
Files Yandex.Disk is still downloading can't be read yet; they are retried until they open.
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else
           r"C:\Users\lerit\Yandex.Disk\Портфолио_SDG\2026\Portfolio\Emotions Club")
OUT = Path(__file__).resolve().parent.parent / "assets"
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or \
    r"C:\Users\lerit\AppData\Local\Screenforge\app-0.1.0\resources\ffmpeg\win32-x64\ffmpeg.exe"

STORY = "Room 313"
STORY_SCENES = ["01_a", "01_b", "02_a", "02_b", "02_c", "03_a", "04_a", "04_b", "04_c", "04_d", "04_e",
                "05_a", "06_a", "06_b"]
# novels whose covers go into the library grid (title in the raw file name -> slug)
COVERS = ["Room 313", "Ghost in 4b", "The Cursed Crown", "Song of the Sea Court", "Daughter of the Flame",
          "Moonlight Heist", "The Witch Next Door", "Hotel Mix Up", "Crimson Masquerade", "The Thirst Pact",
          "Raiders of the Forgotten Star", "The Island Escape", "Treasure Of Two", "The archivist`s code",
          "Threads of the Moon", "Talk on the Plane", "Stuck in the Elevator", "The Double Life",
          "New Year with the Ex", "Echoes of Peru", "The Enchanted Stranger", "Resort Fling",
          "Midnight Pitch for Two", "Morning in Paris", "Rival`s Touch", "Share the Bed-", "Private Lesson"]
# casts shown side by side: several characters per novel, one style
CASTS = ["The Cursed Crown", "Song of the Sea Court", "Daughter of the Flame", "The Thirst Pact"]
VIDEOCOVERS = ["Ghost in 4b", "Moonlight Heist", "The Cursed Crown", "The Witch Next Door",
               "Treasure Of Two", "The Double Life", "Hotel Mix Up"]
PROMOS = {"promo_1": "1_v1 (9x16).mp4", "promo_2": "2_v1_female (9x16).mp4", "promo_3": "3_v1 (9x16).mp4"}


def slug(title):
    return "".join(c if c.isalnum() else "_" for c in title.lower()).strip("_").replace("__", "_")


def readable(p, tries=int(os.environ.get("WAIT_TRIES", "1"))):
    for _ in range(tries):
        try:
            with open(p, "rb") as f:
                f.read(16)
            return True
        except OSError:
            time.sleep(10) if tries > 1 else None
    return False


def ff(src, dst, *args):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size > 0:
        return
    if not readable(src):
        print("SKIP (still syncing):", src.name)
        return
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), *args, str(dst)], check=True)
    print("ok", dst.relative_to(OUT), f"{dst.stat().st_size // 1024} KB")


def webp(src, dst, width, q=78):
    ff(src, dst, "-vf", f"scale='min({width},iw)':-2", "-c:v", "libwebp", "-quality", str(q), "-frames:v", "1")


def main():
    s = slug(STORY)
    for sc in STORY_SCENES:
        webp(SRC / f"scene_{sc} ({STORY}).jpg", OUT / "story" / f"scene_{sc}.webp", 960)
    for i in range(1, 5):
        webp(SRC / f"character_{i:02d}_base ({STORY}).png", OUT / "story" / f"character_{i:02d}.webp", 720, 82)
    webp(SRC / f"cover ({STORY}).jpg", OUT / "story" / "cover.webp", 1024, 82)
    webp(SRC / f"cutscene ({STORY}).jpg", OUT / "story" / "cutscene.webp", 1024, 82)

    for t in COVERS:
        webp(SRC / f"cover ({t}).jpg", OUT / "covers" / f"{slug(t)}.webp", 480)

    for t in CASTS:
        for i in range(1, 8):
            p = SRC / f"character_{i:02d}_base ({t}).png"
            if p.exists():
                webp(p, OUT / "casts" / slug(t) / f"character_{i:02d}.webp", 420, 80)

    for t in VIDEOCOVERS:
        src = SRC / f"videocover ({t}).mp4"
        dst = OUT / "videocovers" / f"{slug(t)}.mp4"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() and readable(src):
            shutil.copyfile(src, dst)  # already web-sized: 1040x400, 5 s, ~0.7 MB
            print("ok", dst.relative_to(OUT))
        ff(src, OUT / "videocovers" / f"{slug(t)}.webp", "-vf", "scale=1040:-2", "-frames:v", "1",
           "-c:v", "libwebp", "-quality", "75")

    for name, f in PROMOS.items():
        ff(SRC / f, OUT / "promo" / f"{name}.mp4", "-vf", "scale=540:-2,fps=30", "-an",
           "-c:v", "libopenh264", "-b:v", "1300k", "-pix_fmt", "yuv420p", "-movflags", "+faststart")
        ff(SRC / f, OUT / "promo" / f"{name}.webp", "-ss", "2", "-vf", "scale=540:-2", "-frames:v", "1",
           "-c:v", "libwebp", "-quality", "75")


if __name__ == "__main__":
    main()
