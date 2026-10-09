import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

class SampleCatalogTests(unittest.TestCase):
    def test_data_contract_and_rights(self):
        data = json.loads((ROOT / "data/sample-games.json").read_text(encoding="utf-8"))
        self.assertEqual(data["dataset"], "ui-sample-not-live")
        seen = set()
        for game in data["games"]:
            self.assertNotIn(game["id"], seen)
            seen.add(game["id"])
            self.assertTrue(game["platforms"])
            self.assertTrue(game["genres"])
            for material in game["materials"]:
                u = urlparse(material["url"])
                self.assertEqual(u.scheme, "https")
                self.assertIn(u.hostname, {"www.playstation.com", "www.pubg.com", "pacman.com", "www.pacman.com"})
                self.assertIn("spoiler", material)
        self.assertGreaterEqual(len(seen), 5)

    def test_no_sensitive_internal_fields(self):
        raw = (ROOT / "data/sample-games.json").read_text(encoding="utf-8")
        for term in ['"source_id"', '"collector"', '"raw_snapshot"', '"api_key"', '"channel_registry"']:
            self.assertNotIn(term, raw)

    def test_no_fake_video_urls(self):
        data = json.loads((ROOT / "data/sample-games.json").read_text(encoding="utf-8"))
        for game in data["games"]:
            self.assertFalse(any("youtube.com/watch" in m["url"] for m in game["materials"]))


if __name__ == "__main__":
    unittest.main()
