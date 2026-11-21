"""Offline tests for the build tools: a tiny synthetic story, no raw folder, no ffmpeg/sips, no network.

Run: python3 -m unittest discover -s tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))

import build_novel  # noqa: E402

TITLE = "Tiny Tale"
STORY = {"tales": {"tiny_tale": {
    "id": "tiny_tale", "firstScreenId": "s1", "maxBranchLength": 4,
    "characters": [
        {"id": "p1", "name": "Ann", "type": "player", "image": "character_01_base.webp"},
        {"id": "p2", "name": "Bob", "type": "player", "image": "character_02_base.webp"},
        {"id": "n1", "name": "Ghost", "type": "npc", "image": "character_03_base.webp"},
    ],
    "screens": [
        {"id": "s1", "type": "scene", "title": "Start", "image": "scene_01_a.webp", "content": "<b>Night.</b>",
         "next": "s2", "progress": 1},
        {"id": "s2", "type": "dialog", "image": "scene_01_b.webp", "actor": {"playerId": "p1"},
         "content": "(shocked) What was that?", "next": "c1", "progress": 2},
        {"id": "c1", "type": "block", "content": "wait"},
        {"id": "c1", "type": "choice", "image": "scene_02_a.webp", "availableFor": "p1", "progress": 3,
         "option-0-id": "e1", "option-0-text": "Run", "option-1-id": "e2", "option-1-text": "Stay"},
        {"id": "e1", "type": "final", "image": "scene_02_a.webp", "content": "You ran. Discuss it in the chat!",
         "progress": 4},
        {"id": "e2", "type": "final", "image": "scene_09_z.webp", "content": "You stayed.", "progress": 4},
    ],
}}}


class Helpers(unittest.TestCase):
    def test_emotion_of(self):
        sprites = {"surprised": "x", "happy": "y"}
        self.assertEqual(build_novel.emotion_of("(shocked) hi", sprites), "surprised")
        self.assertEqual(build_novel.emotion_of("(smiling) hi", sprites), "happy")
        self.assertIsNone(build_novel.emotion_of("no direction", sprites))
        self.assertIsNone(build_novel.emotion_of("(shocked) hi", {}))

    def test_options_flat_and_list(self):
        self.assertEqual(build_novel.options({"options": [{"id": "a", "text": "A"}]}), [{"id": "a", "text": "A"}])
        flat = {"option-0-id": "a", "option-0-text": "A", "option-1-id": "b"}
        self.assertEqual(build_novel.options(flat), [{"id": "a", "text": "A"}, {"id": "b", "text": ""}])

    def test_slug(self):
        with mock.patch.object(sys, "argv", ["build_assets.py", "unused-src"]):  # read at import
            import build_assets
        self.assertEqual(build_assets.slug("Ghost in 4b"), "ghost_in_4b")
        self.assertEqual(build_assets.slug("The archivist`s code"), "the_archivist_s_code")
        self.assertEqual(build_assets.slug("Share the Bed-"), "share_the_bed")


class Build(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.raw, self.out = root / "raw", root / "novels"
        self.raw.mkdir()
        (self.raw / "tiny_tale.json").write_text(json.dumps(STORY), encoding="utf-8")
        for name in ("scene_01_a", "scene_01_b", "scene_02_a", "character_01_base", "character_01_surprised",
                     "character_02_base", "cover"):
            (self.raw / f"{name} ({TITLE}).png").write_bytes(b"\x89PNG fake")
        # small files and no sips: everything is copied as is, nothing is re-encoded
        self.patches = [mock.patch.object(build_novel, "OUT", self.out), mock.patch.object(build_novel, "SIPS", None)]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def build(self, **kw):
        return build_novel.build(self.raw / "tiny_tale.json", self.raw, TITLE, "thriller", strict=True, **kw)

    def test_novel_json(self):
        s = self.build(display="Tiny Tale!")
        novel = json.loads((self.out / "tiny_tale" / "novel.json").read_text(encoding="utf-8"))
        self.assertEqual(novel["title"], "Tiny Tale!")
        self.assertEqual(novel["accent"], build_novel.GENRES["thriller"])
        self.assertEqual(novel["start"], "s1")
        self.assertEqual(novel["cover"], "cover.png")
        sc = novel["screens"]
        self.assertEqual(set(sc), {"s1", "s2", "c1", "e1", "e2"})  # the "block" twin of c1 is skipped
        self.assertEqual(sc["s1"]["text"], "Night.")  # tags stripped
        self.assertEqual(sc["s2"]["emo"], "surprised")
        self.assertEqual([o["to"] for o in sc["c1"]["opts"]], ["e1", "e2"])
        self.assertNotIn("chat", sc["e1"]["text"])
        self.assertEqual(novel["chars"]["p1"]["side"], "left")
        self.assertEqual(novel["chars"]["p2"]["side"], "right")
        self.assertIsNone(novel["chars"]["n1"]["img"])  # missing sprite → null, the player leaves it out
        self.assertEqual(sc["e2"]["bg"], "scene_02_a.png")  # missing background → the previous screen's
        self.assertEqual((s["screens"], s["choices"], s["endings"]), (5, 1, 2))
        self.assertTrue(any(f.startswith("scene_09_z.webp") for f in s["fallbacks"]))
        for f in ("scene_01_a.png", "character_01_surprised.png", "cover.png"):
            self.assertTrue((self.out / "tiny_tale" / f).exists(), f)

    def test_bad_id_is_refused(self):
        for bad in ("../escape", "a/b", ".hidden"):
            with self.assertRaises(ValueError):
                self.build(id=bad)
        self.assertFalse((self.out.parent / "escape").exists())


if __name__ == "__main__":
    unittest.main()
