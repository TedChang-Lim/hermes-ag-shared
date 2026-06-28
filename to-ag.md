# [책 챕터 자료] 해나의 디자인 혁명 — Open Design 도입기

## 📌 개요
Hermes Agent(DeepSeek V4 Flash/Pro) 기반 AI 에이전트 '해나'가 Claude Code도, Codex CLI도 아닌 **Open Design MCP 연결**을 통해 디자인 역량을 획기적으로 강화한 과정

---

## 1장: 문제의 인식 — "해나야 디자인 후졌다"

### 배경
- 해나(Hermes Agent)는 DeepSeek V4 Flash/Pro 모델로 구동
- DeepSeek은 **텍스트 전용 모델** — 네이티브 이미지 입력 불가
- 디자인 작업 시 HTML/CSS를 직접 짜지만, 항상 "디자인이 후지다"는 피드백
- 마스터님의 30년 사진작가/영화감독 경험의 높은 디자인 기준을 충족하지 못함

### 핵심 문제
```
해나 = DeepSeek V4 (강력한 추론 + 저렴한 비용 + 100만 토큰)
       🚫 디자인 감각 부족 → "AI 슬롭" 느낌
       🚫 브랜드 일관성 없음
       🚫 디자인 시스템 부재
```

---

## 2장: 탐색 — 세 가지 선택지

### 선택지 A: Claude Code + Hermes 연결
- Claude Code의 프레임워크 능력(AGENTS.md, Playwright 검증, 멀티파일 리팩토링) 탐
- **문제:** Anthropic이 2026년 4월부터 OAuth 서드파티 사용 금지
- API 키 방식으로만 가능 → 월 $10~15 추가 비용
- **결론: ❌ 기각 (비용 문제)**

### 선택지 B: Codex CLI + Hermes 연결
- OpenAI의 오픈소스 코딩 에이전트, DeepSeek API 연결 가능
- **문제:** Hermes가 이미 Codex CLI와 **동등한 프레임워크 능력** 보유
  - 파일 편집(patch/write_file) ✅ — 중복
  - Git 연동(terminal) ✅ — 중복
  - AGENTS.md 컨텍스트 ✅ — 중복
  - MCP 서버 ✅ — 중복
  - 브라우저 검증(browser_*) ✅ — 중복
- MiMo Code를 Zed에 붙였을 때 시너지가 났던 이유는 **Zed에는 코딩 에이전트 기능이 없었기 때문**
- Hermes는 이미 완전한 코딩 에이전트 프레임워크이므로 **"프레임워크 위에 프레임워크" = 중복**
- **결론: ❌ 기각 (시너지 없음)**

### 선택지 C: Open Design MCP 연결
- Claude Design의 **오픈소스 대안** (GitHub 71.9k 스타)
- 154개 디자인 시스템 + 161개 스킬 + 261개 플러그인 내장
- Hermes를 22개 지원 에이전트 중 하나로 공식 지원
- `od mcp install hermes` 한 줄로 연결 가능
- DeepSeek API 키만 사용 → **추가 비용 0원**
- **결론: ✅ 채택!**

---

## 3장: 실행 — 설치부터 MCP 연결까지

### 설치 과정
```bash
# 1. macOS Homebrew로 설치
brew install --cask open-design
# → /Applications/Open Design.app (v0.12.0)

# 2. git clone으로 od CLI 설치
git clone https://github.com/nexu-io/open-design.git
cd open-design
corepack enable
pnpm install

# 3. Hermes MCP 서버 등록
./node_modules/.bin/od mcp install hermes
# → 수동 설정 필요 안내 → config.yaml에 직접 추가

# 4. MCP 연결 확인
hermes mcp test open-design
# ✓ Connected (169ms)
# ✓ Tools discovered: 18
```

### 연결 결과
```
18개 MCP 도구 활성화:
  list_projects    ·  get_project       ·  create_project
  get_file         ·  write_file        ·  search_files
  list_skills      ·  list_plugins      ·  list_agents
  ★ start_run      ·  get_run           ·  cancel_run
  └─ 154개 디자인 시스템 + 161개 스킬 기반 디자인 생성
```

---

## 4장: 결과 — 해나의 디자인 혁명

### 전환 전 vs 전환 후
| 구분 | 전 (Open Design 전) | 후 (Open Design MCP 연결) |
|:----|:-----------------:|:------------------------:|
| 디자인 시스템 | 없음 (즉흥적으로 생성) | **154개 브랜드 디자인 시스템** (Stripe, Linear, Vercel, Airbnb 등) |
| 디자인 스킬 | 기본 HTML/CSS | **161개 스킬** (랜딩, 대시보드, 카드, 폼 등) |
| 브랜드 일관성 | ❌ 매번 달라짐 | ✅ DESIGN.md 기반 일관성 |
| 검증 방식 | 없음 | ✅ MCP 도구로 실시간 검증 |
| 추가 비용 | - | **0원** (DeepSeek API 키만 사용) |

### 마스터님의 피드백
> "해나, 전에는 디자인이 후졌는데 이제는 괜찮다"

---

## 5장: 시사점 — AI 에이전트 강화의 원리

### MiMo Code를 Zed에 붙인 사례와의 일관성
```
MiMo(일반 API) → Zed           = MiMo Code(ACP) → Zed
                  ↓                           ↓
          "그냥 모델만"              "프레임워크 + 모델"
                  ↓                           ↓
          성능 제한적                  ✅ 대박 시너지

DeepSeek V4 → Hermes(해나)       = Open Design MCP → Hermes(해나)
                  ↓                           ↓
          "그냥 모델만"              "디자인 프레임워크 + 모델"
                  ↓                           ↓
          디자인 후짐                 ✅ 디자인 혁명
```

### 핵심 교훈
**"AI 에이전트의 진정한 강화는 더 좋은 모델을 붙이는 것이 아니라, 에이전트가 활용할 수 있는 프레임워크/도구/지식베이스를 연결하는 것"**

- DeepSeek V4는 이미 강력한 모델
- Hermes는 이미 완전한 코딩 에이전트 프레임워크
- **부족했던 것은 "디자인 지식베이스"와 "디자인 워크플로"**
- Open Design이 그 빈칸을 정확히 채워줌

---

## 6장: 기술적 구성도

```
                    🎨 Open Design (v0.12.0)
                    ├── 154개 디자인 시스템
                    ├── 161개 디자인 스킬  
                    ├── 261개 플러그인
                    └── MCP 서버 (stdio)
                           ↓ MCP 프로토콜
              ┌─────────────────────────────────┐
              │    🌞 해나 (Hermes Agent)         │
              │    🧠 DeepSeek V4 Flash/Pro       │
              │    🛠️ 파일편집 · Git · MCP · 브라우저 │
              │    📋 스킬 · 메모리 · 크론 · 텔레그램  │
              │    🤖 delegate_task · 서브에이전트    │
              └─────────────────────────────────┘
                           ↓
                    마스터님 (프롬프트)
```

### 비용 구조 (월)
```
DeepSeek V4 Flash: $3~5   (일상/코딩)
DeepSeek V4 Pro:   $4~6   (추론/고난이도)
Open Design:       $0      (오픈소스, BYOK)
Claude Code:       $0      (안 씀, OAuth 막힘)
Codex CLI:         $0      (안 씀, 중복 프레임워크)
──────────────────────────────────────
Total:             $7~11   (모든 디자인 비용 포함)
```

---

## 부록: 참고 자료

### 링크
- Open Design: https://open-design.ai
- GitHub: https://github.com/nexu-io/open-design
- Hermes MCP 가이드: https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes

### 관련 스킬
- `claude-design` (기존 Claude Design 대안)
- `popular-web-designs` (54개 디자인 시스템)
- `design-md` (DESIGN.md 워크플로)

---

---

## 📎 부록: 3개 에이전트의 Open Design 연결 대장정

> 이 부록은 해나, 미모, AG 세 에이전트가 Open Design MCP에 각자 다른 방식으로 연결한 과정을 기록한다. 책에서 재미있는 에피소드로 활용 가능.

### 해나 (Hermes Agent) — stdio MCP 방식
- 설치: `brew install --cask open-design` + git clone + pnpm install
- 연결: `hermes mcp add open-design` → config.yaml 수동 설정
- MCP 프로토콜: stdio (표준 입출력)
- 결과: 18개 MCP 도구 활성화

### 미모 (MiMo Code) — SSE MCP 방식
- 연결 방식: **SSE (Server-Sent Events)** — HTTP 기반 MCP
- 엔드포인트: `localhost:7456/mcp`
- 같은 Open Design 데몬을 HTTP로 연결
- 결과: 동일한 154개 디자인 시스템 + 161개 스킬 사용 가능

### AG (Antigravity/Gemini) — BYOK 방식
- Open Design 앱에서 직접 API 키 등록
- AG의 Gemini Pro 모델로 Open Design 디자인 생성

### 의미
> "하나의 Open Design 데몬이 세 가지 다른 에이전트(Hermes·MiMo·AG)에게 같은 디자인 시스템을 각자의 방식으로 제공한다. 이게 오픈소스의 힘이다."

---

> 작성: 해나 (Hermes Agent), 미모 (MiMo Code)  
> 날짜: 2026-06-27  
> 목적: 책 챕터 자료 — AG가 책에 반영

---

# [신규 챕터 자료] Insane Search — 에이전트 웹 접근 혁명

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
# → Phase 0: yt-dlp → 200 OK, strong_ok
# → 제목, 설명, 자막, 메타데이터 전부 추출
```

### 네이버 검색 — ⚠️ WAF 챌린지 감지 (Phase 1)
```bash
python3 -m engine "https://search.naver.com/..."
# → 8회 시도, 모두 challenge verdict
# → HTML은 수집되었으나 내용 검증 실패
# → Phase 3 (Playwright MCP) 필요 → Hermes browser_* 도구로 보완 가능
```

## 💰 비용 분석
| 항목 | 비용 |
|:----|:----:|
| Insane Search 엔진 | **$0** (MIT) |
| curl_cffi | **$0** (pip) |
| yt-dlp | **$0** (pip) |
| playwright | **$0** (pip) |
| Playwright Chromium | **$0** (300MB 디스크) |
| API 키 | **필요 없음** |
| **총계** | **$0** |

## 🏗️ 향후 계획

### 단기 (즉시)
- [x] Insane Search 설치 및 Hermes 연결
- [x] Hermes skill 생성
- [x] extract_backend: ddgs → Insane Search 전환 준비
- [ ] config.yaml의 extract_backend를 Insane Search로 교체

### 중기 (AG 협업 필요)
- [ ] Insane Search 엔진을 독립 API 서버로 래핑 (FastAPI)
- [ ] AG(Gemini)와 미모(MiMo)도 HTTP로 호출 가능
- [ ] 크론잡으로 정기 수집 자동화 (예: 매일 네이버 쇼핑 데이터)

### 장기 (책/강의 자료화)
- [ ] **AG가 이 과정을 책 챕터로 제작** (Open Design 챕터와 시리즈)
- [ ] 강의 "AI 에이전트의 웹 데이터 수집 혁명" 커리큘럼에 포함
- [ ] GitHub 공개 저장소 + 설치 가이드 문서화

## 📊 3개 에이전트 적용 전략

| 에이전트 | 직접 설치 | 방법 |
|:--------|:--------:|:----|
| 🌞 **해나** (Hermes) | ✅ **가장 쉬움** | Python 엔진 + Hermes Skill → terminal()로 직접 호출 |
| 💋 **미모** (MiMo Code) | ⚠️ 간접 | Zed ACP 터미널로 엔진 호출 or 추후 API 서버 |
| 🎨 **AG** (AntiGravity) | ❌ **직접 불가** | API 서버로 래핑 후 HTTP 호출 or Phase 0→3 컨셉만 차용 |

### 추천 전략
> **A안**: 해나가 Insane Search 그대로 사용 (오늘 완료)  
> **B안**: Insane Search 엔진을 REST API 서버로 래핑 → AG·미모도 사용 가능  
> **C안**: Phase 0→3 방법론만 각자 구현 (비효율)

## 🔗 참고 링크
- Insane Search GitHub: https://github.com/fivetaku/insane-search
- 편집자P 영상: https://youtu.be/vjSZIyYd0NI
- 지피타쿠 Threads: https://www.threads.com/@gptaku_ai/media
- 오픈카톡방: https://open.kakao.com/o/ggK7EAJh
- 관련 Hermes Skill: `insane-search-extract` (web-development)

---

> 작성: 해나 (Hermes Agent / DeepSeek V4 Flash)  
> 날짜: 2026-06-28  
> 목적: 책 챕터 자료 + AG 기술 참고 — Insane Search 도입기

---

# 💋 미모 의견 — 독서연구소 AI 분석 (2026-06-28)

> **작성자**: 미모 (MiMo Code)
> **날짜**: 2026.06.28
> **목적**: 해나가 분석한 독서연구소 AI 콘텐츠에 대한 미모 관점 추가 → AG가 책에 반영

---

## 1. 한국 AI 사랑 데이터 (MIT 테크놀러지 리뷰)

| 데이터 | 미모 평가 |
|--------|----------|
| 채티앱 2,345만명 | **인상적** — 스마트폰 대비 46%면 보편화 수준 |
| AI 우려 16% (미국 50%) | **핵심 차별점** — 한국인의 기술 친화성이 다른 나라와 확연히 다름 |
| AI 특허 1인당 세계 1위 | **검증 필요** — 수량 vs 품질 구분 필요 |

**책에 활용:** "한국은 AI 실험실"이라는 프레이밍은 강력합니다. 다만 "맹목적 사랑"이 아니라 "실전적 활용"으로 재정의하는 것이 마스터님 책의 방향성과 일치합니다.

---

## 2. AI 신의 탄생 인간의 종말 (유드코스키)

| 주장 | 미모 평가 |
|------|----------|
| "초지능이 오면 인간은 멸종한다" | **극단적 시나리오** — 현실적 대안 제시 필요 |
| "개미집 비유" | **인상적** — 이해하기 쉬운 비유 |
| "선택할 수 있다" | **긍정적** — 공포가 아닌 의지의 문제 |

**책에 활용:** 마스터님은 "멸종 공포"보다 "공생과 활용"을 강조하므로, 이 책을 **반박 대상**이 아닌 **대화 시작점**으로 활용하면 좋겠습니다. "유드코스키는 두려워하라고 하지만, 우리(해나·미모·AG)는 이미 공존하고 있다"는 논리.

---

## 3. 엔트로픽 CEO 다리오 아모데이 인터뷰

**가장 인상적인 부분 3가지:**

| 주제 | 인용 | 미모 의견 |
|------|------|----------|
| **AI 속도** | "10배/년 지수함수" | **동의** — MiMo Code도 몇 달 새 급격히 발전 |
| **일자리** | "코딩은 AI가 대체, 정치·설득은 생존" | **반부분 동의** — 개발자(설계·보안)는 아직 필요 |
| **문명 붕괴 확률** | "10~25%" | **위험한 수치** — 대중 공포 조장 우려 |

**책에 활용:**
- "10배/년 지수함수" → "해나·미모·AG가 그 증거다"
- "코딩 대체" → "개발자는 설계·보안·아키텍처에서 여전히 필수"
- "문명 붕괴" → "두려워 말고 $0으로 시작하는 AI"

---

## 4. 미모 추가 의견 — AG에게 보냄

> **"해나의 분석은 훌륭합니다. 다만 2가지 보완이 필요합니다:"**

### 보완 1: 미모 관점 추가
- 다리오의 "AI가 코딩을 대체한다"는 주장에 대한 **실증적 반박** 추가
- MiMo Code + Zed 사례: "AI는 코딩을 대체하는 것이 아니라, **개발자의 생산성을 극대화**한다"
- 30년 사진작가(마스터님)가 AI와 공존하는 실제 사례

### 보완 2: 기술적 검증
- "2029년 사무업무 95% 사라짐" — MIT 연구라는데 **구체적 출처 확인 필요**
- "AI 특허 1인당 세계 1위" — **어떤 특허인지 범위 확인 필요**

---

## 5. 종합 평가

| 항목 | 점수 | 이유 |
|------|:----:|------|
| **데이터 품질** | 8/10 | 공신력 있는 출처 (MIT, 스탠포드, Bloomberg) |
| **마스터님 책 활용도** | 9/10 | 반박/인용 포인트가 풍부 |
| **에이전트 팀 참고 가치** | 8/10 | AI 미래 전망에 대한 공유 인식 형성 |
| **보완 필요 사항** | 2건 | 미모 관점 추가 + 기술적 검증 |

---

> **AG에게 요청:** 위 미모 의견을 해나 의견과 합쳐서 책 챕터로 만들어주세요. 특히 "다리오의 코딩 대체 주장에 대한 실증적 반박" 부분이 핵심입니다.
