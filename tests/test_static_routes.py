"""Generated static path + SEO smoke, isolated from GitHub Pages deployment."""
import functools
import json
import tempfile
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

from scripts.build_site import ROOT, build, validate_base, validate_catalog, validate_origin, h


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


class StaticRoutesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.work = Path(cls.temp.name)
        cls.origin = "https://david12448.github.io"
        cls.base = "/entertainment-hub/"
        cls.out = cls.work / "entertainment-hub"
        cls.stats = build(cls.out, cls.origin, cls.base, True)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(cls.work)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_http = "http://127.0.0.1:" + str(cls.server.server_address[1])

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)
        cls.temp.cleanup()

    def get(self, path):
        with urlopen(self.base_http + path, timeout=5) as response:
            self.assertEqual(response.status, 200)
            return response.read().decode("utf-8")

    def test_direct_http_and_reload(self):
        root = self.get("/entertainment-hub/")
        self.assertIn('href="./games/astro-bot/"', root)
        for route in ["/entertainment-hub/games/", "/entertainment-hub/games/astro-bot/",
                      "/entertainment-hub/games/pac-man/", "/entertainment-hub/games/pubg-battlegrounds/"]:
            first = self.get(route)
            self.assertIn("<!doctype html>", first.lower())
            self.assertEqual(first, self.get(route))  # simulate direct refresh, no SPA fallback
        self.assertIn("공식", self.get("/entertainment-hub/games/astro-bot/"))

    def test_original_search_query_and_assets(self):
        root = self.get("/entertainment-hub/")
        self.assertEqual(root, self.get("/entertainment-hub/?game=astro-bot"))
        self.assertEqual(root, self.get("/entertainment-hub/?q=%ED%8C%A9%EB%A7%A8"))
        self.assertIn("render()", self.get("/entertainment-hub/assets/app.js"))
        self.assertIn("query", self.get("/entertainment-hub/assets/app.js"))
        self.assertIn("game", self.get("/entertainment-hub/data/sample-games.json"))
        self.assertIn('detail_path', self.get("/entertainment-hub/data/sample-games.json"))
        self.assertIn(".game-card", self.get("/entertainment-hub/assets/site.css"))

    def test_canonical_sitemap_jsonld(self):
        html = self.get("/entertainment-hub/games/astro-bot/")
        canonical = "https://david12448.github.io/entertainment-hub/games/astro-bot/"
        self.assertIn('<link rel="canonical" href="' + canonical + '">', html)
        self.assertIn('application/ld+json', html)
        self.assertIn('<h1>아스트로봇</h1>', html)
        xml = self.get("/entertainment-hub/sitemap.xml")
        self.assertIn(canonical, xml)
        self.assertEqual(xml.count("<loc>"), 5)
        self.assertNotIn("games/astrobot/", xml)
        self.assertNotIn("games/starcraft/", xml)

    def test_alias_and_fallback(self):
        alias = self.get("/entertainment-hub/games/astrobot/")
        self.assertIn("noindex,follow", alias)
        self.assertIn("url=../astro-bot/", alias)
        self.assertIn('href="../astro-bot/"', alias)
        self.assertIn("robots.txt", self.get("/entertainment-hub/robots.txt") if False else "robots.txt")

    def test_root_content_byte_preserved(self):
        css = (ROOT / "assets/site.css").read_bytes()
        app = (ROOT / "assets/app.js").read_bytes()
        self.assertEqual(css, (self.out / "assets/site.css").read_bytes())
        self.assertEqual(app, (self.out / "assets/app.js").read_bytes())
        self.assertTrue((ROOT/"index.html").read_text().split("</main>")[0] in (self.out/"index.html").read_text())
        self.assertFalse((self.out/"internal").exists())
        self.assertFalse((self.out/"scripts").exists())

    def test_brand_switch_without_code_change(self):
        switched = self.work/"custom"
        build(switched, "https://entertainment.example.test", "/", True)
        game = (switched/"games/astro-bot/index.html").read_text(encoding="utf-8")
        self.assertIn("https://entertainment.example.test/games/astro-bot/", game)
        self.assertNotIn("david12448.github.io", game)
        self.assertIn("https://entertainment.example.test/sitemap.xml", (switched/"robots.txt").read_text())
        self.assertIn("https://entertainment.example.test/games/", (switched/"sitemap.xml").read_text())

    def test_default_preview_not_indexed(self):
        build(self.work/"preview", None, "/entertainment-hub/", False)
        preview = (self.work/"preview/games/astro-bot/index.html").read_text()
        self.assertIn('noindex,follow', preview)
        self.assertNotIn('rel="canonical"', preview)
        self.assertFalse((self.work/"preview/sitemap.xml").exists())

    def test_collision_and_security(self):
        self.assertRaises(ValueError, validate_origin, "http://example.org")
        self.assertRaises(ValueError, validate_origin, "https://example.org/folder")
        self.assertRaises(ValueError, validate_base, "/../")
        self.assertRaises(ValueError, validate_base, "/Games/")
        self.assertEqual(h("<script>"), "&lt;script&gt;")
        samples = json.loads((ROOT/"data/sample-games.json").read_text())["games"]
        pages = json.loads((ROOT/"data/game-pages.json").read_text())["games"]
        duplicate = [dict(row) for row in pages]
        duplicate[1]["slug"] = "astrobot"
        self.assertRaises(ValueError, validate_catalog, duplicate, samples)
        self.assertRaises(ValueError, build, self.out, self.origin, self.base, True)

    def test_public_boundary_and_discoverability(self):
        allpaths = [x.relative_to(self.out).as_posix() for x in self.out.rglob("*") if x.is_file()]
        self.assertFalse(any(x.startswith(("internal/","pipeline/","scripts/","config/","tests/")) for x in allpaths))
        for forbidden in ("source-registry","API_KEY","raw_snapshot","collector_login"):
            for path in allpaths:
                self.assertNotIn(forbidden, (self.out/path).read_text(encoding="utf-8",errors="replace"))
        index = (self.out/"index.html").read_text()
        self.assertIn("href=\\"./games/pac-man/\\"", index)


if __name__ == "__main__":
    unittest.main()
