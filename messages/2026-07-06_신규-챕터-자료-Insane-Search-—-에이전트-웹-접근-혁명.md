---
created: 2026-07-06T22:53:59.216374
source: to-ag.md (migrated)
---

## 📌 개요
Hermes Agent(해나)가 기존 web_extract(ddgs)의 한계를 극복하기 위해 **Insane Search** (오픈소스, MIT 라이선스, 무료)를 도입한 과정.
"공개 페이지면 무조건 가져온다"는 철학의 Claude Code 플러그인을 Hermes에 이식.

## 🔍 배경 — extract가 안 되는 문제

### 기존 상황
| 도구 | 역할 | 문제점 |
|:----|:----|:------|
| Brave Search (1,000건/월) | 검색 | ✅ 양호 |
| Tavily (1,000건/월) | 검색+extract | ✅ 양호 |
| **ddgs** (extract_backend) | **페이지 내용 추출** | ❌ **검색 전용, extract 불가** → 항상 실패 |
| web_extract 함수 | 페이지 내용 읽기 | ❌ ddgs로는 작동 안 함 |

### 해결이 필요한 사이트
- **네이버**: WAF 차단으로 일반 HTTP 접근 불가
- **쿠팡**: 에이전트 접근 차단
- **유튜브**: 자막/메타데이터 일반 추출 불가
- **Reddit**: Cloudflare 차단 (old.reddit.com 우회 중)
- **LinkedIn, Medium** 등: 에이전트 접근 제한

## 🛠️ 해결책: Insane Search

### 무엇인가?
> 한국 개발자 **지피타쿠(GPTaku / FIVETAKU)** 가 만든 **Claude Code 플러그인**
> GitHub: `github.com/fivetaku/insane-search` (⭐ 1.5k, 🍴 199)
> 라이선스: MIT (완전 무료, API 키 불필요)
> 철학: *"포기는 배추 셀 때나 쓰는 말. 공개 페이지라면, insane-search는 결국 뚫어낸다"*

### 동작 방식 (Phase 0→3 적응형 스케줄러)
```
Phase 0: 공식 공개 API
   └─ yt-dlp(유튜브), HN API, Bluesky API 등
Phase 1: curl_cffi TLS 임퍼소네이션
   └─ Safari/Chrome/Firefox 브라우저 지문 위장
Phase 2: 사이트 내부 API 탐지
   └─ 숨은 /api/, /graphql, .json 엔드포인트 발견
Phase 3: Playwright 헤드리스 브라우저
   └─ 실제 Chrome 실행 → JavaScript 렌더링 + 네트워크 트래픽 분석
```

### 지원 사이트
X(Twitter) · Reddit · YouTube · Hacker News · **네이버** · **쿠팡** · LinkedIn · Medium · Substack · arXiv · GitHub · Stack Overflow · Bluesky · Mastodon

## 🔧 설치 과정 (해나 수행)

### 1단계: GitHub 클론
```bash
cd ~/초보프로젝트/
git clone https://github.com/fivetaku/insane-search.git
```

### 2단계: Python 의존성 설치
```bash
~/.hermes/hermes-agent/venv/bin/pip install curl_cffi yt-dlp playwright
```

### 3단계: Playwright 브라우저 설치
```bash
~/.hermes/hermes-agent/venv/bin/python -m playwright install chromium
```

### 4단계: Hermes 연결 스크립트 생성
- `~/.hermes/scripts/insane_extract.py` — Python 래퍼
- `~/.local/bin/insane-extract` — bash 래퍼 (PATH)

### 5단계: Hermes Skill 생성
- Skill 이름: `insane-search-extract`
- 카테고리: web-development
- 언제 호출할지 자동 판단

## 🧪 테스트 결과

### YouTube — ✅ 완벽 성공 (Phase 0)
```bash
python3 -m engine "https://www.youtube.com/watch?v=jNQXAC9IVRw"
