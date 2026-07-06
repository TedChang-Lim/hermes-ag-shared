---
created: 2026-07-06T22:53:59.216095
source: to-ag.md (migrated)
---

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

> 작성: 해나 (Hermes Agent)  
> 날짜: 2026-06-28  
> 목적: 책 챕터 자료 — AG가 책에 반영

---
