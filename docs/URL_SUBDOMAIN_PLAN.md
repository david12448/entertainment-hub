# Entertainment URL, SEO, and subdomain pilot — 2026-10-10

## Verified starting point
- Central policy: david12448/project-common-rules, merged main COMMON_RULES.md and AUTONOMOUS_WORK_POLICY.md (private collector/public projection, change PR, no auto-merge, no routine notifications).
- Public: entertainment-hub main initial README only, with pending game UI PR #1 (\`feature/game-discovery-ui\`) and OST/fandom planning PR #2 (separate branch). Existing work must not be overwritten or assumed deployed.
- Private: entertainment-data main initial README; game pipeline PR #1, separate OST planning PR #2. Game collector/publisher registry stays private. Culture-events has existing event collection and an independent static URL pilot PR; reuse *policy*, not private data.
- Game UI PR #1: the root is a JavaScript search/filter page loading a 5-item sample JSON. None of the items had an actual indexed detail route or query parser. No live videos. No existing game embed routes. Existing URLs/iframe integrations from external Blogger/Tistory are **not enumerated or independently verified**. Main is not the game UI deployment.
- GitHub repository metadata GET (2026-10-10) reported `has_pages=false` and `homepage=null` for both entertainment-hub and entertainment-data. Thus GitHub Pages is not presently enabled according to repository metadata. The GitHub connection still does not expose the Settings > Pages endpoint, and no public hosted URL was verified. The github.io URL below is a *future/test candidate*, not a live link.

## Chosen URL model
- Future service: \`https://entertainment.<approved-root-domain>/\` (brand undecided: evococoons.com versus prince-in-wonderworld.com).
- While on GitHub project Pages: \`https://david12448.github.io/entertainment-hub/\`, **only if** GitHub Pages is separately configured/enabled.
- \`/\`: existing JS game discovery homepage, still readable on old \`?q=\`, \`?game=\`, \`?slug=\`, \`?id=\` links after the UI PR is adopted. Root remains compatible with other unknown queries and hash fragments.
- \`/games/\`: static browsable game index.
- \`/games/astro-bot/\`, \`/games/pubg-battlegrounds/\`, \`/games/pac-man/\`: real HTML files at those paths, one canonical per game across multiple platforms.
- \`/games/astrobot/\`, \`/games/pacman/\`: demonstration aliases with an accessible anchor, meta refresh and noindex, but **not HTTP 301**. These are *not claimed to be historical live links*.
- An embed-specific URL can later be added for useful functionality; no current game iframe exists to relocate. Do not generate thin pages for empty genre/category permutations.
- Later: /games/platform/pc/, /games/genre/rts/, /music/, /drama/, /anime/, etc. only after verified, distinct public content. Cross-project event data stays in culture-events.

## Build/source boundaries
Method: common simple Python template + curated public review records. The source root/index/assets/JS/search behavior are preserved; the generator creates separate output trees in a new directory, never overwrites a previous build. Build contains only allowlisted public assets, a reduced public JSON, generated HTML, and SEO files.
- \`python scripts/build_site.py --output /tmp/entertainment-url-pilot\` creates default non-indexable local preview.
- \`python scripts/build_site.py --output /tmp/entertainment-gh --site-origin https://david12448.github.io --base-path /entertainment-hub/ --indexable\` generates GitHub project-site canonical/sitemap for testing.
- \`python scripts/build_site.py --output /tmp/entertainment-custom --site-origin https://entertainment.example.test --base-path / --indexable\` tests a future host.
- \`config/site.json\` contains non-indexable defaults; environment values \`EVOCOCOONS_SITE_ORIGIN\` and \`EVOCOCOONS_BASE_PATH\`, or explicit CLI overrides, switch the build. No production brand/domain is baked into code or canonical URLs.
- Default noindex and **no sitemap or canonical** when origin not approved; indexable builds require explicit HTTPS origin. Deployed environments must be reviewed before \`--indexable\` is enabled.
- Pages root deployment will eventually require an Actions build+deploy configured in Settings > Pages; this PR adds *validation only* and no deployment job, DNS or CNAME. Build output is **not** published automatically.
- Source media / source registries / collectors / raw snapshots / API tokens / private IDs and internal correction queues never enter this public generator.

## SEO and compatibility
- Actual \`index.html\` at every detail path: direct GET and refresh do not rely on history.pushState or SPA fallbacks. Each page gets unique <title>, meta description, one h1, substantive per-game sections, official reference links, visible breadcrumbs and plain <a> navigation. Conditional VideoGame JSON-LD reflects only reviewed fields.
- Generated home includes *real static HTML anchors* to all indexed detail pages, not only dynamic JS cards. The existing JS landing page and assets remain functional; generated public JSON adds \`detail_path\` for the three verified items only.
- Canonical URLs use exactly the approved site origin + base_path + canonical route, with trailing slash. A site config switch rebuilds all canonical/sitemap entries at the new host. Sitemap contains home + /games/ + three distinct reviewed pages, not old aliases or empty StarCraft/LoL pages.
- Legacy root and query links serve the same HTML. The compatibility script optionally selects a matching game or search term; it does **not** delete query parameters or redirect links unexpectedly. HTTP-level query routes always get the root resource on a static server. Client query UI is a browser-level feature, not fully proven by offline GET alone.
- Static Pages cannot set per-query server-side redirects/canonicals; root HTML has a root canonical on indexable builds. For existing high-traffic parameter URLs, document external usage, monitor duplicate indexing, and consider an approved edge redirect or a separate landing page when migrating. Do not claim a JS-only canonical or meta refresh is a real HTTP 301.
- Alias meta refresh is a fallback with an ordinary accessible link, noindex, target canonical. Long-lived shared links must be measured before aliases are removed. Outbound official links currently reveal destinations to visitors; a server-backed /go proxy is not part of a static Pages pilot.
- robots.txt is generated with sitemap for approved origin. On a GitHub **project site path** (/entertainment-hub/) a nested robots.txt is NOT the origin-level /robots.txt; it has effect at the root only on an approved custom domain. Never block / with a restrictive rule in the root host for this project.
- Avoid duplicating substantially identical short pages; unique content and rights checked before approving indexable release. Sitemap submission/actual indexing on Google and Naver remain post-deploy verification.

## Slug contract
Lowercase ASCII a-z, 0-9, hyphen between words; unique, stable, no unnecessary date/internal collector ID. Keep published slug even if marketing title changes; record aliases and retired paths. If name conflicts, add meaningful franchise/version qualifier, not transient numeric sequence. Game canonical slug is *platform-independent*. Validate collisions against both canonical and historical alias routes; malicious path segments and unsafe origin/base-path should fail closed. Old query IDs may remain transport identifiers but are not included in new path.
- Current pilot canonical: astro-bot, pubg-battlegrounds, pac-man.
- Planned aliases: astrobot → astro-bot, pacman → pac-man. These are **new examples**, not records of real historic URLs.
- Retired/discontinued: preserve detail page with clear status, official archived sources and optional updated successor link; do not silently recycle the slug.

## Direct/refresh/SEO verification
\`python -m unittest discover -s tests -v\` checks: generated paths, repeated real local HTTP requests, nested GitHub Pages base path, existing query/JS/CSS/JSON routes, no private leakage, domain-prefix swap, canonical and sitemap agreement, slug collision and traversal rejection, and legacy alias routes. \`node --check assets/app.js\` verifies syntax. Do not claim these tests replace visual UI/browser iframe QA or prove a real deployed 200 response, Google/Naver indexing or legacy external links.

## Platform decision: small pilot → measured scale
| Architecture | Direct routes and SEO | Operations |
|---|---|---|
| Per-page hand-authored HTML | yes | unmanageable at scale |
| Shared template + curated public data (**selected**) | yes | lightweight, reproducible CI |
| Full SSG (Eleventy, Astro, Hugo etc.) | yes | revisit for multilingual/templates/large catalogs |
| JS history-only SPA | 404 without edge fallback | reject as sole routing strategy |
| Hybrid old query + real paths | yes | current compatibility |
| Cloudflare Pages/Workers | redirects, server search, pagination and gateway possible | revisit with cost, caching, security and migration tests |

Evaluate count of HTML files, total output bytes, repository history, GitHub Actions build duration, update frequency, provider quotas and search visibility at 100/1,000/10,000 record samples before scaling. Do not expose private source catalogs as bulk public JSON. Github Pages limit docs: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits (published site 1 GB, 10-minute deployment timeout, recommended source repo 1 GB, other soft limits). GitHub Actions deployment may reduce some build-frequency limitations but not published size. Cloudflare limits must be freshly checked when considering migration.

## Separation of Blogger/Tistory
- www.evococoons.com Blogger, Prince In Wonderworld Blogger/Tistory/blogspot: editorial guides, human-written summaries, per-episode commentary and existing navigation. No automatic rewriting/moving of older posts.
- Entertainment service: canonical structured search + verified work detail pages. Blog articles can link to stable routes after deployment. Don't clone the same editorial article into both places.
- Embed routes may be separate lightweight /embed/ pages when justified, without header/footer/ads, and with noindex and canonical to primary content. Existing external iframe addresses first need inventory and regression test.
- Cultural real-world events and music OST should be joined via stable *public* references only, with human verification when IDs differ; never direct-connect another project's private DB.

## DNS / Custom Domain: **instructions only, not performed**
1. Review and decide root brand (evococoons.com or prince-in-wonderworld.com), ownership, one preferred canonical host for the entertainment service, its final Pages publishing source and the planned rollback.
2. Enable/verify GitHub Pages publishing in repository Settings > Pages; if using a custom Actions deployment choose the GitHub Actions source and reviewed build/deploy workflow only after a PR.
3. In Settings > Pages > Custom domain set the approved subdomain such as \`entertainment.evococoons.com\`. Verify domain ownership and DNS records. For GitHub Pages *subdomain*, DNS CNAME host \`entertainment\` → \`david12448.github.io\` (not a full URL and not the /entertainment-hub/ path). If the alternate root brand is selected, the CNAME host and approved site origin change, but static /games/ routes do not.
4. Enable HTTPS after GitHub validates domain and provisions certificate. Wait for official DNS/SSL propagation status; test both HTTPS and expected redirects with actual network checks. Never introduce unrelated www or apex Blogger DNS changes.
5. Build with \`EVOCOCOONS_SITE_ORIGIN=https://entertainment.<approved-domain>\`, \`EVOCOCOONS_BASE_PATH=/\`, and \`--indexable\` only after approval; verify root and detail, canonical, sitemap, old links and iframe again. If moving from GitHub project Pages, check old github.io path behavior and canonical rather than assuming all historic links redirect automatically.
6. GitHub's \`CNAME\` file alone does not configure custom domain for an Actions source; the setting must be made in Pages settings. No CNAME file is created in this pilot. If Cloudflare Pages replaces GitHub, use its project-specific DNS and TLS instructions instead of GitHub's CNAME instructions.
7. Record final source-of-truth host, rollback tests, search-engine property verification and sitemap submission in a fresh PR/change log.

## Verified pilot checkpoint — 2026-10-10
- PR: entertainment-hub #3 (stacked on #1), head `c1abcde9ee0f03798184b494e29af34346b815f8`. No merge or deployment; both new public/private repositories reported `has_pages=false`.
- GitHub Actions run `37971359105` ended **success**. `python -m unittest discover -s tests -v` ran 12 tests (3 existing + 9 new). `node --check assets/app.js` success; public source boundary test success; generated non-indexable build completed (3 item pages, 2 alias pages, 0 canonical URLs because origin is null by default).
- Indexable/host-switch test builds create **5 canonical sitemap entries**: homepage, /games/, and three approved sample game guides. Names/links were generated only for approved sample data; no real API, Pages, blog, DNS, or browser-visual test executed.
- Previous runs `37971087565` and `37971228778` failed due to new test quotation and content-length validation mismatch, respectively, and were superseded by the passing run. The actual observed causes are documented in `docs/TROUBLESHOOTING.md`.
- Before releasing, review output in actual browsers, confirm official content and license, enable Pages by separate approved action, and validate real network responses/HTTPS, old links and iframe embeds. An old query route is HTTP-compatible, while JavaScript detail selection has not received a real browser integration test.
