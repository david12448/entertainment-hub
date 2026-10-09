# entertainment-hub

## 게임 검색과 URL 파일럿 (브랜치 PR, 미배포)
기존 게임 검색 UI의 고정 주소 생성 실험을 `feature/static-pretty-url-pilot` 브랜치에서 검토합니다.
- `scripts/build_site.py`: 공식 출처가 있는 게임만 `games/<slug>/index.html` 생성
- `data/game-pages.json`: 개별 페이지용 검토된 공개 설명(시범 3건)
- `config/site.json`: 루트 도메인 미확정; origin=null, GitHub Pages 테스트 prefix, 색인 보류
- `docs/URL_SUBDOMAIN_PLAN.md`: URL/SEO/기존 링크/배포·DNS 지침
- `tests/test_static_routes.py`: 두 도메인 설정, 직접 GET·재요청, sitemap·canonical 검증

실제 DNS·Custom Domain 변경, 공개 배포, 자동 PR 병합은 하지 않습니다.
