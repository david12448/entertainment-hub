# Entertainment Hub work handoff (2026-10-10)

## Current verified project state
- `entertainment-hub`: Public, GitHub repo has_pages=false. Main still initial README as inspected, proposed game discovery UI PR #1, OST planning PR #2 and stacked static URL PR #3.
- `entertainment-data`: Private, repo has_pages=false; game ingestion foundation PR #1, OST taxonomy PR #2. No verified publisher-channel API data published.
- `project-common-rules`: central standard proposal PR #3, not merged. Common rules merged main v1.0 remain authoritative.
- `culture-events`: its URL pilot is separate and not overwritten.

## Implementation and verified checks
- Keep current search/filter/JS card prototype from game UI PR #1 (base of URL PR). URL PR #3 adds domain-neutral build plus 3 substantial official-source pages and 2 example aliases. No actual domain, DNS, Pages, or redirect service configured.
- Current static paths in generated output: /, /games/, /games/astro-bot/, /games/pubg-battlegrounds/, /games/pac-man/. Canonical host and base path are build settings, not code constants.
- Tests: GitHub Actions run 37971359105 SUCCESS; 12 unit/integration tests, JS syntax check, public boundary check and isolated preview build.
- Local server repeated GET tests passed for /entertainment-hub/ project-prefix paths; this is not external production reachability.
- Existing query root remains 200 in test, JS can preselect ?game, ?slug, ?id, ?q, but real browser query behavior is untested.
- New domain switch in tests changes canonical+sitemap to an alternative test host; default non-indexable build emits neither sitemap nor canonical. Full technical details: docs/URL_SUBDOMAIN_PLAN.md.

## Next work / approval boundary
1. Review stacked PR chain; do not merge PR #3 before deciding whether to merge parent game UI PR #1. OST PR #2 remains independent.
2. Browser/manual QA at generated route paths; iframe and Blogger/Tistory compatibility require actual external URL inventory.
3. Once brand and origin are explicitly approved, implement reviewed Pages build/deploy workflow and confirm repository Settings > Pages; build with origin/base path. Do not create a CNAME or change DNS without separate approval.
4. Validate real HTTP response and reload, full mobile/desktop navigation, canonical/sitemap, verification in search webmaster tools. Review scale and Cloudflare alternative later.
5. Keep collectors and approved source registry private; only validated public fields may be exported. Never fabricate videos, scenes or downloads.

No reminder/scheduled progress notifications, automatic PR merging, or changes to currently working other projects were made.
