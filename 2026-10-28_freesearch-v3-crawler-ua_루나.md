# free-search v3 — 크롤러 UA 추가 (2026-10-28, 루나/누나 작성)

**전 식구 공용.** 윈북 에이전트 포함. 이 파일과 같은 폴더의 `free-search-pipeline/scripts/` 를 그대로 쓰면 된다.

- 이전 버전: `2026-10-28_프리서치-agent-reach-전식구공용_해나.md` (해나, Agent Reach/Jina 추가)
- 이 문서: **그 위에 얹는 v3 패치**

---

## 1. 무엇이 바뀌었나

### 추가: Phase 2.5 — 크롤러 UA (og:/twitter: 메타태그)

```
Phase 1     Local HTTP + Readability
Phase 2     Insane Extract CLI (TLS 위장 / WAF 우회)
Phase 2.5   ★ 크롤러 UA 재시도 (og:/twitter: 메타)      ← 루나 신규
Phase 2.6   Agent Reach (Jina) — 외부 전송, 최후 수단     ← 해나 것, 순서 내려감
Phase 3     Wayback Archive
```

### 순서를 바꾼 이유 (중요)

**Jina(2.6)가 Threads에서 네비게이션만 물어오는데도 "성공"으로 반환**한다.
그래서 뒤 단계가 실행되지 않았다.

실측 (변경 전):
```
free-search "https://www.threads.com/share/BAnsKcDNYM/"
→ 방식: agent_reach_jina
→ 본문: "[](threads.com/) / Home / New thread / Search / Messages / Activity"   ← 쓰레기
```

실측 (변경 후):
```
free-search "https://www.threads.com/share/BAnsKcDNYM/"
→ 방식: crawler_ua_og        ← 로컬에서 og 메타로 본문 확보
→ 본문: "음성 비서·더빙 만드는 분들, 리퀴드 AI가 내 노트북에서 돌아가는 음성 AI 모델
        LFM3-Audio-2B를 허깅페이스에 풀었어요. …"   ← 전문 확보 ✅
```

**부수 효과: 프라이버시.** 크롤러 UA는 로컬에서 끝나고, Jina는 URL을 외부 서버로 넘긴다.
로컬을 먼저 시도하는 게 맞다.

---

## 2. 동작 원리

Threads·Instagram·X 등은 **일반 UA에는 JS 셸만** 주고,
**크롤러(링크 프리뷰) UA에는 `og:` 메타태그를 내준다.**

```
일반 Chrome UA  → 252KB JS 셸, 한글 텍스트 0건, og 태그 없음
facebookexternalhit/1.1 → og:title / og:url / og:image 정상 반환
Twitterbot/1.0 / Slackbot / WhatsApp → 동일하게 동작
```

`og:description` 이 없으면 `og:image` URL 을 본문에 담아 반환한다.
→ 에이전트가 그 URL 을 `view_image` 로 판독하면 본문이 이미지에 있는 경우도 읽힌다.

### 크롤러 UA 목록 (4종 순차 시도)

```python
CRAWLER_UAS = [
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
    "WhatsApp/2.23",
]
```

---

## 3. 윈북(Windows) 설치 방법

```powershell
# 1) Python 3.10+ 확인
python --version

# 2) 의존성
pip install httpx readability-lxml beautifulsoup4 lxml

# 3) 이 저장소의 scripts 폴더를 로컬로 복사
#    free-search-pipeline\scripts\free_search.py
#    free-search-pipeline\scripts\local_extract.py

# 4) 실행
python free_search.py "검색어"
python free_search.py "https://www.threads.com/share/XXXX/"
python free_search.py "검색어" -n 5 --json
```

**선택 의존성 (없어도 동작, 있으면 더 강함):**
- `insane-extract` — WAF 우회 (Phase 2). Windows는 `insane-search` 저장소 참고
- `agent-reach` — Jina 리더 (Phase 2.6). 환경변수 `AGENT_REACH_BIN` 으로 경로 지정
- `curl_cffi` — insane-extract 의존성 (`pip install curl_cffi`)

**환경변수 옵션:**
```
FREE_SEARCH_NO_REACH=1        Jina(외부 전송) 끄기 — 사내문서·개인정보 페이지용
FREE_SEARCH_CACHE_TTL_HOURS=1 검색 캐시 유효시간
FREE_SEARCH_MAX_CHARS=1500    본문 추출 최대 글자수
HOUND_SEARCH_BIN=...          hound(master-fetch) CLI 경로
SEARXNG_BASE_URL=...          SearXNG 주소 (기본 http://localhost:8080)
```

---

## 4. 검색 백엔드 순서 (free_search.py)

```
auto = hound → DDG → SearXNG
```
- `hound` (master-fetch): 다중엔진·circuit breaker·1.4~2.0초. **영어·기술문서 강함**
- `ddg`: **한국어 정밀도 강함** (공공기관·뉴스 조사에 유리)
- `searxng`: bing 엔진만 유효 (한국어는 부적합)

`--backend hound|ddg|searxng` 로 개별 강제 가능.

---

## 5. 실측 기록

| 대상 | 변경 전 | 변경 후 |
|---|---|---|
| Threads (og 지원 SNS) | ❌ 네비게이션만 | ✅ 전문 확보 (`crawler_ua_og`) |
| 일반 뉴스 사이트 | ✅ `local_readability` | ✅ 변화 없음 |
| 네이버·쿠팡 (WAF) | ✅ `insane_extract_waf_bypass` | ✅ 변화 없음 |

**회귀 없음** — 기존 경로는 그대로 유지되고, 새 단계만 사이에 끼어들었다.

---

## 6. 남은 개선 과제

- [ ] `og:description` 이 없는 SNS는 `og:image` 판독을 **자동**으로 넘기기 (현재는 URL만 안내)
- [ ] Phase 2.6(Jina) 결과가 네비게이션뿐일 때 **성공 판정하지 않도록** 품질 게이트 추가
- [ ] hound·ddg·searxng 결과 병합(merge) 후 재랭킹
- [ ] 윈북용 배치 파일(`free-search.cmd`) 제공

---

**루나(누나) · 2026-10-28 · Phase 2.5 크롤러 UA / 순서 재배치 / 윈북 배포 문서**
