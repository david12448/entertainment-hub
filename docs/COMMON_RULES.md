# Common project rules

Version: 1.0 (2026-10-09)

## 1. Protect project assets
- Keep collectors, raw snapshots, source registries, parser details, credentials, and internal mappings in private storage.
- Public interfaces expose only necessary normalized results. Avoid publishing bulk internal datasets, hidden source maps, and operational endpoints.
- Apply pagination, access controls, and proportionate rate limits where appropriate. Never rely on JavaScript obfuscation or hiding URLs as a security boundary.
- Do not embed secrets or private internal instructions in public repositories. Assume public data can be copied; focus on reducing mass extraction and protecting proprietary implementation.
- Keep official attribution and user-accessible original-source navigation where required; do not bypass access controls or licenses.

## 2. Learn from mistakes
- Document reproducible problems, impact, cause (or uncertainty), attempted fixes, verified resolution, regression test, and prevention in `docs/TROUBLESHOOTING.md` per project.
- Do not invent historical incidents. Mark unverified explanations as hypotheses.
- Generalize cross-project lessons into this central repository without copying secrets or proprietary source details.

## 3. Change safety
- Preserve existing files and working behavior. Use dedicated branches and pull requests; do not auto-merge.
- Review the diff, run available checks, and keep project-specific instructions separate from centrally managed guidance.
- No progress notifications or scheduled monitoring should be added by default.


## 4. Unattended operation
- Follow [central autonomous-work policy](https://github.com/david12448/project-common-rules/blob/main/AUTONOMOUS_WORK_POLICY.md) for user-away execution, manual approval boundaries, and 04:00–12:00 KST quiet hours.
- A GitHub Markdown policy does not independently schedule a ChatGPT task or override GitHub/ChatGPT native push-notification settings.
