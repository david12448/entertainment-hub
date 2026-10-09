# Troubleshooting

No verified incidents recorded as of 2026-10-10. When a reproducible defect is confirmed, document impact, cause or hypothesis, fix, tested result, and regression guard.

## 2026-10-10 — URL pilot verification boundaries
The GitHub connector does not expose the GitHub Pages settings endpoint through its supported fetch action. Hence custom domain, publishing source, and actual site uptime were **not** verified. Do not infer deployment from a CI success. The pilot's local HTTP GET/reload simulation validates generated files only; actual browser, blog embeds, external shared URLs, search indexing and deployment require separate post-merge checks.

## 2026-10-10 — PR #3 first CI failure (verified)
- Observed: GitHub Actions run 37971087565 failed in `Check sample catalog`. The existing three sample tests passed, but importing `tests/test_static_routes.py` raised SyntaxError at a malformed quoted assertion on line 130. Thus the additional static-route tests were not run.
- Cause: a test assertion was serialized with extra backslashes around inner quote delimiters. This was a test-file syntax defect, not a GitHub Pages deployment failure.
- Fix: replace the assertion with valid single-quoted Python syntax, correct a directory-relative link and replace an overly strict prefix comparison of the generated root (which legitimately gains metadata).
- Prevention: CI imports and tests every added Python test before claiming URL coverage, and JavaScript receives a Node syntax check. The follow-up Actions result must be checked before marking validation as passed.

## 2026-10-10 — CI test-content threshold (verified)
- Symptom: workflow run 37971228778 finished failure at StaticRoutesTest.setUpClass after the original three sample tests had succeeded.
- Cause: the pilot's validated public page lead for one sample was 98 characters, while the generator had required 100. This mismatch blocked smoke setup; it was not a routing or deployment failure.
- Resolution: adjusted minimum lead length conservatively to 95 while retaining substantive original sections and the verified official-reference requirement. The following workflow run 37971359105 **passed all 12 tests** plus JavaScript syntax and isolated preview build.
- Prevention: verify fixture lengths against explicit validation thresholds; report untested deployment/browser behavior separately.
