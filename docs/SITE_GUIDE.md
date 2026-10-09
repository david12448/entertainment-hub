# Entertainment Hub 공개 시범 화면

현재 저장소는 **공개 UI만** 담습니다. 수집기, 원본 스냅샷, 공식 채널 확인 레지스트리, 영상 후보 큐, 키, 상세 URL 매핑은 비공개 `entertainment-data` 영역에만 보관합니다.

## 사용자 UI
- 이름/별칭 통합 검색(한글·영문), 플랫폼·장르·콘텐츠 유형을 **각각** 필터.
- 작고 단순한 카드 → 펼쳐지는 개별 작품 상세.
- 공식 원문 페이지 링크만 노출. 확인되지 않은 개별 엔딩 영상의 URL을 만들지 않음.
- 추후 엔딩/스토리 영상은 스포일러 가림을 기본 적용.
- 팬 영상/팬 공략은 공식 자료와 다른 라벨과 검수 경로.
- 현재 자료는 `data/sample-games.json`의 *시범 레코드*이며 최신 데이터베이스나 실시간 영상 목록이 아님.
- 음악·영화·드라마·애니 탭은 현재 개발 예정 표시이며 실제 기능 없음.

## 검증 출처
- Astro Bot: https://www.playstation.com/ko-kr/games/astro-bot/
- PUBG: https://www.pubg.com/ko/game-info/overview
- PAC-MAN: https://pacman.com/en/games/
- 스타크래프트와 리그 오브 레전드는 작품 분류 시범 데이터만 있으며 개별 공식 영상 미등록.

## 운영 경계
- 실제 승인되지 않은 영상/저작물 복제 금지. 게임 ROM, BIOS, 불법 복제 파일은 다루지 않음.
- 공식 영상은 원본 또는 허용된 임베드로 연결; 원본 재호스팅 금지.
- 필요한 정보만 게시. 공개 레코드의 복사를 완전히 막을 수 있다고 약속하지 않음.
- 이후 대용량 공개 전체 JSON은 서버 검색+페이지네이션+요청 제한 방식으로 전환 검토.
- `culture-events`의 공연·e스포츠·오프라인 행사와는 공식 일정만 연결하고 수집 원본은 중복 복사하지 않음.
- 모든 작업은 중앙 `project-common-rules`의 public-safe 공통 원칙을 준수.

## 로컬 프리뷰
```sh
python -m http.server 8000
```
그 다음 http://localhost:8000/ 으로 접근. `file://`로 열면 브라우저의 JSON fetch 보안 정책으로 표시되지 않을 수 있습니다.

## 검증
```sh
python -m unittest discover -s tests -v
```
