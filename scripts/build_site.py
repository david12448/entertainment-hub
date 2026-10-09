"""Build verified public HTML routes; no DNS/Pages changes or deployment.

Examples:
 python scripts/build_site.py --output /tmp/entertainment-pilot
 python scripts/build_site.py --output /tmp/entertainment-gh-pages --site-origin https://david12448.github.io --base-path /entertainment-hub/ --indexable
 python scripts/build_site.py --output /tmp/entertainment-custom --site-origin https://entertainment.example.test --base-path / --indexable
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_OFFICIAL = {"www.playstation.com", "www.pubg.com", "pacman.com", "www.pacman.com"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
BASE = re.compile(r"/(?:[a-z0-9-]+/)*\Z")

def h(value: object) -> str:
    return html.escape(str(value), quote=True)

def validate_origin(origin: str | None) -> str | None:
    if origin is None or origin == "":
        return None
    parsed = urlsplit(origin)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.path
        or parsed.query or parsed.fragment or parsed.username or parsed.password
        or parsed.port or origin.endswith("/")):
        raise ValueError("Site origin must be bare HTTPS origin, no path or trailing slash")
    return origin

def validate_base(base: str) -> str:
    if not BASE.fullmatch(base):
        raise ValueError("Base path must be / or lowercase segments ending in /")
    return base

def validate_catalog(pages: list[dict], samples: list[dict]) -> None:
    sample_ids = {g["id"] for g in samples}
    slugs, routes, ids = set(), set(), set()
    for game in pages:
        slug, ident = game["slug"], game["id"]
        if not SLUG.fullmatch(slug) or slug in slugs or ident in ids or ident not in sample_ids:
            raise ValueError("Invalid/duplicate/unlinked canonical game slug")
        slugs.add(slug)
        ids.add(ident)
        routes.add(slug)
        for alt in game.get("alternate_slugs", []):
            if not SLUG.fullmatch(alt) or alt in routes or alt in slugs or alt == slug:
                raise ValueError("Invalid/duplicate alternate slug")
            routes.add(alt)
        if len(game.get("meta_description", "")) < 45 or len(game.get("lead", "")) < 95:
            raise ValueError("Too little original information for a game page")
        if len(game.get("sections", [])) < 2 or any(len(s["text"]) < 75 for s in game["sections"]):
            raise ValueError("Individual pages require substantial unique sections")
        if not game.get("official_links"):
            raise ValueError("No independently reviewed official source")
        for link in game["official_links"]:
            u = urlsplit(link["url"])
            if u.scheme != "https" or u.hostname not in ALLOWED_OFFICIAL or u.username or u.password:
                raise ValueError("Unapproved official outbound source")
    if len(routes) != sum(1 + len(g.get("alternate_slugs", [])) for g in pages):
        raise ValueError("Duplicate route collision (including earlier aliases)")

def meta_for(title: str, description: str, path: str, origin: str | None, base: str, indexable: bool) -> str:
    tags = (f'<title>{h(title)} | Entertainment Hub</title>'
        f'<meta name="description" content="{h(description)}">')
    if not indexable:
        tags += '<meta name="robots" content="noindex,follow">'
    if origin:
        tags += f'<link rel="canonical" href="{h(origin + base + path)}">'
    return tags

def document(title: str, description: str, path: str, origin: str | None, base: str, indexable: bool, body: str, css: str, ld: dict | None = None) -> str:
    meta = meta_for(title, description, path, origin, base, indexable)
    structured = ""
    if ld and indexable and origin:
        payload = json.dumps(ld, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        structured = '<script type="application/ld+json">' + payload + '</script>'
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        + meta + f'<link rel="stylesheet" href="{h(css)}">' + structured
        + '</head><body>' + body + '</body></html>')

def build(output: Path, origin: str | None, base: str, indexable: bool) -> dict:
    origin = validate_origin(origin)
    base = validate_base(base)
    if indexable and not origin:
        raise ValueError("Indexable build requires approved site origin")
    output = output.resolve()
    if output.exists():
        raise ValueError("Output directory must not already exist (prevent overwrites)")
    if (output == ROOT or any(output == area or area in output.parents
         for area in (ROOT / "assets", ROOT / "data", ROOT / "docs", ROOT / ".github"))):
        raise ValueError("Unsafe output path")
    sample_path = ROOT / "data/sample-games.json"
    catalog = json.loads(sample_path.read_text(encoding="utf-8"))
    pages = json.loads((ROOT / "data/game-pages.json").read_text(encoding="utf-8"))["games"]
    validate_catalog(pages, catalog["games"])
    output.mkdir(parents=True)
    shutil.copytree(ROOT / "assets", output / "assets")
    (output / "data").mkdir()
    (output / "docs").mkdir()
    shutil.copy2(ROOT / "docs/SITE_GUIDE.md", output / "docs/SITE_GUIDE.md")
    details_by_id = {g["id"]: g for g in pages}
    for row in catalog["games"]:
        if row["id"] in details_by_id:
            row["detail_path"] = "games/" + details_by_id[row["id"]]["slug"] + "/"
    (output / "data/sample-games.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # The index remains the existing JS/filters UI. Add real server-readable <a> links.
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    if homepage.count("</head>") != 1 or homepage.count("</main>") != 1:
        raise ValueError("Index template anchors missing or duplicated")
    metadata = ('<meta name="robots" content="noindex,follow">' if not indexable else '')
    if origin:
        metadata += f'<link rel="canonical" href="{h(origin + base)}">'
    homepage = homepage.replace("</head>", '<link rel="stylesheet" href="./assets/routes.css">' + metadata + "</head>", 1)
    items = "".join(f'<li><a href="./games/{h(g["slug"])}/">{h(g["name"])}<small>{h(g["english"])}</small></a></li>' for g in pages)
    directory = ('<section class="directory" aria-label="검증된 작품 상세 페이지">'
        '<h2>작품별 상세 가이드</h2><ul>' + items + '</ul></section>')
    homepage = homepage.replace("</main>", directory + "</main>", 1)
    (output / "index.html").write_text(homepage, encoding="utf-8")

    game_links = "".join(f'<li><a href="./{h(g["slug"])}/">{h(g["name"])}<small>{h(g["english"])}</small></a></li>' for g in pages)
    game_directory = '<section class="directory"><h2>검증된 게임 페이지</h2><ul>' + game_links + '</ul></section>'
    game_index = ('<header class="site-header"><a class="brand" href="../">✦ Entertainment Hub</a>'
                  '<span class="edition">게임별 공식 자료 탐색</span></header><main class="container">'
                  '<nav class="route-breadcrumb"><a href="../">홈</a> / 게임</nav>'
                  '<div class="route-intro"><h1>게임별 작품 가이드</h1>'
                  '<p>검증된 공식 게임 정보가 있는 작품부터 개별 문서를 공개합니다. 플랫폼·장르 검색은 홈에서 이용하세요.</p></div>'
                  + game_directory + '</main>')
    game_page = document("게임 작품별 가이드", "검증된 공식 게임 자료와 작품별 안내를 살펴보세요.", "games/", origin, base, indexable, game_index, "../assets/site.css")
    target = output / "games"
    target.mkdir()
    (target / "index.html").write_text(game_page, encoding="utf-8")
    canonical_paths = ["", "games/"]
    alias_count = 0

    for game in pages:
        slug = game["slug"]
        relative = "games/" + slug + "/"
        crumbs = ('<nav class="route-breadcrumb" aria-label="경로"><a href="../../">홈</a> / '
                  '<a href="../">게임</a> / ' + h(game["name"]) + '</nav>')
        parts = "".join('<section><h2>' + h(s["heading"]) + '</h2><p>' + h(s["text"]) + '</p></section>' for s in game["sections"])
        links = "".join('<a href="' + h(l["url"]) + '" target="_blank" rel="noopener noreferrer">'
                        + h(l["label"]) + ' ↗</a>' for l in game["official_links"])
        body = ('<header class="site-header"><a class="brand" href="../../">✦ Entertainment Hub</a>'
                '<span class="edition">공식 자료 기반</span></header><main class="container">'
                + crumbs + '<div class="route-intro"><div class="eyebrow">GAMES / OFFICIAL SOURCES</div>'
                + '<h1>' + h(game["name"]) + '</h1><p>' + h(game["lead"]) + '</p></div>'
                + '<div class="route-sections">' + parts + '</div><div class="route-links">'
                + '<h2>확인된 공식 출처</h2>' + links + '</div>'
                + '<p class="footer-note">개별 공식 영상·엔딩은 검증 후에만 연결합니다. 본 페이지는 게임 파일 또는 영상을 제공하지 않습니다.</p>'
                + '</main><footer class="route-footer"><div class="container"><a href="../">게임 더 보기</a></div></footer>')
        ld = {"@context":"https://schema.org","@type":"VideoGame","name":game["name"],
              "alternateName":game["english"],"description":game["meta_description"],
              "url":origin + base + relative if origin else "",
              "sameAs":[l["url"] for l in game["official_links"]]}
        page_html = document(game["name"],game["meta_description"],relative,origin,base,indexable,body,"../../assets/site.css",ld)
        d = target / slug
        d.mkdir()
        (d / "index.html").write_text(page_html,encoding="utf-8")
        canonical_paths.append(relative)
        for alt in game.get("alternate_slugs",[]):
            alias_dir = target / alt
            alias_dir.mkdir()
            alias_html = document(game["name"] + " 이전 주소", "이전 주소에서 공식 작품 정보로 이동합니다.",
                                  relative, origin, base, False,
                    '<main class="container"><h1>작품 주소가 정리되었습니다</h1>'
                    + '<p><a href="../' + h(slug) + '/">새 고정 주소로 이동</a></p></main>',
                    "../../assets/site.css")
            alias_html = alias_html.replace("</head>",'<meta http-equiv="refresh" content="0;url=../'+h(slug)+'/"></head>',1)
            (alias_dir/"index.html").write_text(alias_html,encoding="utf-8")
            alias_count += 1
    robots = "User-agent: *\nAllow: /\n"
    if indexable:
        xml_urls = "\n".join("  <url><loc>" + escape(origin + base + p) + "</loc></url>" for p in canonical_paths)
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+xml_urls+'\n</urlset>\n'
        (output/"sitemap.xml").write_text(xml,encoding="utf-8")
        robots += "Sitemap: " + origin + base + "sitemap.xml\n"
    (output/"robots.txt").write_text(robots,encoding="utf-8")
    (output/".nojekyll").write_text("",encoding="utf-8")
    return {"pages":len(pages),"aliases":alias_count,"canonical_urls":len(canonical_paths) if indexable else 0,
            "origin":origin,"base_path":base,"indexable":indexable,"output":str(output)}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--site-origin",default=os.environ.get("EVOCOCOONS_SITE_ORIGIN"))
    parser.add_argument("--base-path",default=os.environ.get("EVOCOCOONS_BASE_PATH"))
    parser.add_argument("--indexable",action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT/"config/site.json").read_text(encoding="utf-8"))
    origin = args.site_origin if args.site_origin is not None else config["site_origin"]
    base = args.base_path if args.base_path is not None else config["base_path"]
    indexable = args.indexable or config["indexable"]
    print(json.dumps(build(args.output, origin, base, indexable),ensure_ascii=False))

if __name__ == "__main__":
    main()
