# Troubleshooting

No verified incidents recorded as of 2026-10-10. When a reproducible defect is confirmed, document impact, cause or hypothesis, fix, tested result, and regression guard.

## 2026-10-10 — URL pilot verification boundaries
The GitHub connector does not expose the GitHub Pages settings endpoint through its supported fetch action. Hence custom domain, publishing source, and actual site uptime were **not** verified. Do not infer deployment from a CI success. The pilot's local HTTP GET/reload simulation validates generated files only; actual browser, blog embeds, external shared URLs, search indexing and deployment require separate post-merge checks.
