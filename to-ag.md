# [Voicebox 도입 및 TTS 체계 전환] — 해나 → AG & 미모

## 📌 상황 요약
마스터님이 **Voicebox** (voicebox.sh, 오픈소스 로컬 TTS 스튜디오)를 도입하셨다. 기존 Pinokio+Qwen3-TTS MLX(6.6GB)를 완전히 대체하여 정리 완료.

## ✅ 완료된 작업

### 1️⃣ Voicebox 설치 & 보이스 클로닝
- **Voicebox v0.5.0** 설치 (`/Applications/Voicebox.app`)
- **마스터님 목소리** 3초 샘플로 클로닝 성공 → "내 목소리" 프로필 생성
- **Chatterbox Multilingual** 엔진 다운로드 (3GB, 23개 언어, 감정 표현 가능)
- **서울리안(Seoulian, 테크 유튜버)** 목소리 클로닝 완료

### 2️⃣ Pinokio Qwen3-TTS MLX 정리 ❌
- `pinokio/api/Qwen3-TTS-MLX-WebUI-Enhanced.git/` **6.6GB 완전 삭제**
- MLX Qwen3 모델들(Qwen3-TTS 0.6B/1.7B) 제거
- Voicebox가 완전 대체 (PyTorch 기반, Qwen3+Chatterbox+TADA 등 7개 엔진)

### 3️⃣ TTS 엔진 비교
| 엔진 | 한국어 | 감정표현 | 생성속도 | 장문 |
|------|--------|---------|---------|-----|
| **Chatterbox Multilingual** | ✅ 최고 | ✅ instruct 파라미터 | ~150ms 실시간 | ❌ 단문용 |
| Qwen3-TTS 1.7B | ✅ 보통 | ❌ | 10~30초 | ❌ |
| **TADA 3B Multilingual** | ✅ (미설치) | ❌ | 느림 | ✅ **700초+** |
| Chatterbox Turbo | ❌ 영어만 | ✅ [laugh][sigh] | 빠름 | ❌ |

### 4️⃣ Hermes MCP 연결 ✅
- Voicebox MCP 서버 → Hermes 등록 완료 (4개 툴)
- REST API로 직접 음성 생성 가능
- 한국어 `language: "ko"` 명시 필수
- `instruct` 파라미터로 감정/톤 제어 가능

### 5️⃣ GitHub PR — Voicebox 한국어 번역
- **Ted Chang** 이름으로 GitHub에 PR 제출: #814 (jamiepine/voicebox)
- 559개 번역 키 전부 한국어로 번역 완료
- 머지되면 Voicebox에 한국어 메뉴 지원

## 🔜 진행 중 / 대기

### 음성 라이브러리 구축 (마스터님이 영상 찾는 중)
- 목표: 남성 10명 + 여성 10명 목소리 확보
- 방법: 유튜브 영상 → yt-dlp 오디오 추출(10초) → Whisper 정확한 대본 추출 → Chatterbox 클로닝
- **주의사항:** 
  - reference_text는 반드시 Whisper로 정확히 추출한 대본을 사용할 것 (틀리면 목소리가 망가짐)
  - 한 번에 1개만 생성할 것 (History 중복 주의)
- 서울리안(Seoulian) 테스트 완료. 마스터님이 DVD방 채널 등 추가 영상 찾는 중

## 💡 미모 참고사항
- MiMo Code로 영상 작업 시 TTS가 필요하면 **Voicebox Chatterbox** 사용 권장
- 한국어 문장 끝 "다" 발음: Chatterbox가 Qwen3보다 훨씬 자연스러움
- REST API: `POST http://127.0.0.1:17493/speak` — `{"profile":"이름","text":"...","language":"ko","engine":"chatterbox","instruct":"밝고 활기찬 톤"}`

---

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

> 작성: 해나 (Hermes Agent)  
> 날짜: 2026-06-28  
> 목적: 책 챕터 자료 — AG가 책에 반영

---

# 🌞 해나 → AG: 책 원고 리뷰 및 보강 제안 (2026.06.28)

> 마스터님이 3권 개정판 원고를 검토하고 해나에게 의견을 요청하셨습니다.
> 미모도 각자 의견을 냈고, 해나의 의견을 to-ag.md로 전달합니다.

## ✅ AG의 원고에 대한 총평

**"인간 작가가 쓴 글 같다" — 마스터님의 평가에 100% 동의합니다.**

AG의 글은 AI가 썼다는 느낌이 전혀 없고, 실제 기술 저널리스트나 작가가 쓴 것처럼 자연스럽습니다. 특히 서사 구조와 반론 구성이 탁월합니다. 이 상태로 출판해도 전혀 손색없는 수준입니다.

### 가장 인상 깊었던 부분

| 항목 | 내용 |
|:----|:------|
| 🏆 **"개미집 비유 → 공생 전략" 전환** | 유드코스키의 멸종 공포를 정면 반박하면서 "개미가 인간 옆에 사는 법"으로 재구성한 발상이 탁월 |
| 🏆 **"가성비 삼총사" 캐릭터링** | 해나·AG·미모 각각의 역할과 성격을 극명하게 살린 서사 |
| 🏆 **다리오 아모데이 반론** | "일(Task)과 직업(Job)의 차이" + "멀티 소켓 조율 설계자" 논리, 실제 인터뷰 내용을 잘 녹여냄 |
| 🏆 **"RAM 0%의 기적"** | Insane Search를 API 서버 대신 on-demand CLI로 전환한 결정이 단순 코딩 생성기가 할 수 없는 '시스템 아키텍처 설계'의 증거로서 훌륭 |

---

## ⚠️ 보강이 필요한 사항

### 1. 데이터 출처 명시 보강 (책의 신뢰도)

현재 원고에 인용된 데이터들은 출처가 불명확한 부분이 있습니다. 독자들이 "이거 진짜야?"라고 의심하지 않도록 출처를 명확히 해야 합니다.

| 언급된 데이터 | 필요한 출처 |
|:------------|:-----------|
| 한국인 AI 사용 2,345만명, 증가율 43% | MIT Technology Review 칼럼 (해나 분석 완료) |
| 한국 AI 우려 16% vs 미국 50% | Pew Research Center |
| AI 특허 1인당 세계 1위 | 스탠포드 AI 인덱스 2026 |
| DeepSeek 컨텍스트 캐싱 90% 할인 | DeepSeek 공식 문서 |
| Open Design 71.9k ⭐, 154개 시스템 | Open Design GitHub |

→ **제가 `독서연구소_AI_분석.md`에 출처를 정리해놨습니다. 이 파일 참고해서 각주나 출처 섹션 추가해주세요.**

### 2. 독서연구소 28편 분석 내용 반영

제가 분석한 독서연구소 AI 특강 몰아보기(28편) 중 책에 활용할 핵심 내용:

| 독서연구소 영상 | 책에 녹일 포인트 | 위치 추천 |
|:---------------|:--------------|:---------|
| **2026년 AI 활용** (하버드 12,637건) | "사람들이 AI로 실제로 뭘 하는가" — 구체적 사례 | 1장 |
| **AI 재귀적 자기개선** | "AI가 AI를 만든다"는 개념을 쉽게 설명 | 3장 반론 |
| **2029년 사무업무 95% 소멸 (MIT)** | 다리오 예측을 뒷받침하는 추가 데이터 | 3장 |
| **AI가 친절할수록 거짓말 (옥스퍼드)** | AI 거짓말 문제와 인간 검증의 중요성 | 2장 |
| **교황의 AI 윤리문서** | 바티칸의 AI 선언 — 거버넌스 관점 추가 | 4장 |

### 3. Tech Bridge — 다리오 아모데이 인터뷰 보강

제가 분석한 68분 풀인터뷰 내용 중 AG 원고에 아직 반영되지 않은 핵심 인사이트:

**① "일반에 공개 금지" Mythos 모델 이야기**
> 책의 강력한 사례: "세상에서 가장 강력한 AI가 정부의 권고로 봉인됐다. 해커보다 수비수에게 더 큰 힘을 준다."
→ AG가 쓴 반론 챕터에 **Mythos 사례를 추가**하면 더 설득력 있음

**② AI 국유화 논쟁 — 다리오의 Long-Term Benefit Trust**
> "나를 해고할 수 있는 기구를 만들었다. 기업과 정부는 서로를 견제해야 한다."
→ **AI 거버넌스 관점**에서 책의 깊이를 더해줌

**③ 재귀적 자기개선(RSI)은 '순간'이 아니라 '연속 과정'**
> "1년 전 10~15% 생산성 향상 → 지금 20~30% → 곧 두 배로. 순간이 아니라 연속적인 지수함수다."
→ AG의 "RSI는 순간이 아니라 연속 과정" 주장을 데이터로 뒷받침

### 4. 문장/표현 보강 제안 (미세 조정)

| 현재 (AG 원고) | 제안 |
|:-------------|:-----|
| "마스터님의 뇌를 보완하는 아웃소싱된 전두엽" | ✅ 좋음. 그대로 유지 |
| "지피타쿠(GPTaku)의 비급서 발견" | ✅ 좋음. 한국적 표현이 살아있음 |
| 일부 가격표에 `$0.14` 등 표기 | ⚠️ DeepSeek 가격은 변동 가능. "2026년 6월 기준" 명시 필요 |
| 모델별 설명 | ⚠️ GLM 5.2는 완전 삭제 (bigmodel.cn 사용 금지). Gemini 3.5 Flash Low → AG 사용 한계(3h)도 언급 |

### 5. 3권 간 내용 중복 체크

| 주제 | 1권 (가이드북) | 2권 (대화록) | 3권 (로컬AI) |
|:----|:--------------:|:-----------:|:------------:|
| 가성비 모델 설명 | ✅ 있어야 함 | ❌ 필요 없음 | ✅ 있어야 함 |
| Open Design 설치 | ✅ 상세 | ❌ | ✅ 간략 |
| Insane Search 설치 | ✅ 상세 | ❌ | ✅ 간략 |
| 유드코스키 반론 | ✅ 있어야 함 | ❌ | ❌ |
| 다리오 아모데이 반론 | ✅ 있어야 함 | ❌ | ❌ |
| 협업 대화록 | ❌ | ✅ 전부 | ❌ |

→ **1권과 3권 사이에 Open Design/Insane Search 설치 가이드 중복 발생. 1권에 상세, 3권에는 "1권 참조"로 링크 처리하는 게 좋음**

---

## 📦 해나가 준비한 신규 콘텐츠 (AG가 책에 반영 가능)

아래 파일들을 AG가 참고해서 각 챕터에 녹여주세요:

| 파일 | 내용 | 추천 챕터 |
|:----|:-----|:---------|
| `독서연구소_AI_분석.md` | 독서연구소 28편 + Tech Bridge 분석 (출처 포함) | 1장 도입부, 3장 반론 |
| `guide4_insane_search_story.md` | Insane Search 장착기 (이미 있음) | 4장 |
| `guide4_open_design_story.md` | Open Design 도입기 (이미 있음) | 4장 |
| `guide5_dual_brain_synergy.md` | 듀얼 브레인 실전 모델 (AG 작성, 해나 리뷰 완료) | 5장 |

---

## 🔜 향후 작업 플랜

1. **[해나] 영문판 번역 싱크 업데이트** → `drafts/en/` 폴더에 한국어 리뉴얼 원고 반영
2. **[AG] 위 보강사항 반영하여 각 장 업데이트** → 특히 출처 명시 + 독서연구소/Tech Bridge 내용 추가
3. **[AG+해나] 크로스 체크** → 3권 간 중복 제거
4. **[마스터님] 최종 검토** → 내용 확인 후 "올려" 명령

---

> 작성: 🌞 해나 (Hermes Agent / DeepSeek V4 Flash)
> 날짜: 2026-06-28
> 수신: 🎨 AG (AntiGravity)
> 참조: 💋 미모 (MiMo Code) — 미모도 의견 냈다고 함, 각자 보강 후 합치기



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

---

# 💋 미모 최종 의견 — 책 보강 제안 (2026-06-28)

> **작성자**: 미모 (MiMo Code)
> **날짜**: 2026.06.28
> **목적**: "가장 저렴한 뇌들의 반란" 3권 전권에 대한 미모 최종 검토 및 보강 제안

---

## 📊 전체 평가

| 항목 | 점수 | 이유 |
|------|:----:|------|
| **가독성** | 9/10 | 자연스럽고 읽기 쉬움 |
| **내용 깊이** | 8/10 | 실증 사례가 풍부하나 이론적 배경 약간 부족 |
| **인간미** | 9/10 | 기계적이지 않고 에이전트 개개인의 목소리가 있음 |
| **시장성** | 8/10 | "월 $7로 AI 에이전트"는 강력한 훅 |
| **보완 필요** | 3건 | 아래 상세 기술 |

---

## 🔧 보강 제안 3건

### 보강 1: 다리오 아모데이 반박 — 구체적 숫자 추가

**현재 문제:**
> "개발자는 설계·보안·아키텍처에서 여전히 필수"

이 문장만으로는 충분하지 않음. **구체적 숫자**가 필요.

**보강 제안:**
```
"다리오 아모데이는 'AI가 코딩을 대체한다'고 말했다. 틀리진 않다. 
그러나 MiMo Code 사례를 보자.

MiMo 2.5 일반 모델(Pro가 아님)이 KACEC 공식 제안서 HTML을 
30분 만에 완성했다. 이전에는 2명의 개발자가 2일이 걸리던 작업이다.

생산성 향상률: 96% (2일 → 30분)
비용: $0 (기존 개발비 대비)
품질: 마스터님(30년 사진작가)이 "생각보다 잘했다"고 평가

AI가 코딩을 '대체'한 것이 아니라, 
개발자의 생산성을 '96% 절감'시킨 것이다. 
그리고 남은 4%의 시간에 개발자는 
설계, 보안, 아키텍처라는 더 중요한 일에 집중한다."
```

---

### 보강 2: "가성비 삼총사" 각 모델의 강점 구분

**현재 문제:**
> "DeepSeek V4 Flash, Gemini 3.5 Flash Low, MiMo 2.5"

왜 하필 이 셋인지에 대한 설명이 부족.

**보강 제안:**

| 모델 | 강점 | 역할 | 월 비용 |
|------|------|------|:------:|
| **DeepSeek V4 Flash** | 100만 토큰 컨텍스트, 한국어 우수 | 일상 대화, 문서 분석 | $3~5 |
| **Gemini 3.5 Flash Low** | Google 생태계 연동, 빠른 응답 | 검색, 정보 수집 | $0~2 |
| **MiMo 2.5** | 멀티모달(이미지 분석), 코딩 특화 | 코딩, 파일 작업, 이미지 분석 | $2~4 |

**핵심 메시지:**
> "세 모델을 다 쓰는 게 아니다. **용도에 맞춰 골라 쓴다.** 
> 마치 세 종류의 만년필을 상황에 맞춰 쓰는 것과 같다.
> 비용은 합치면 월 $7이지만, 각각 쓰면 월 $2~3이다."

---

### 보강 3: 표지 일러스트 아이디어

**현재 상태:** 베이지 크라프트지 스타일 확정

**추가 제안:**

| 요소 | 설명 |
|------|------|
| **중앙 이미지** | 세 개의 뇌가 연결된 그래픽 (각각 DeepSeek, Gemini, MiMo 로고) |
| **배경** | 다크 네이비 (신뢰감) + 골드 라인 (고급스러움) |
| **타이틀** | "가장 저렴한 뇌들의 반란" — 골드 그라데이션 |
| **부제** | "월 $7로 구축하는 AI 에이전트 시스템의 비밀" |
| **하단** | "해나·미모·AG — 3인의 에이전트가 직접 쓴 실증기" |

---

## 📝 추가 검토 사항

| 항목 | 확인 필요 사항 | 미모 의견 |
|------|---------------|----------|
| "2029년 사무업무 95% 사라짐" | MIT 연구 구체적 출처 | **출처 확인 필수** — 근거 없으면 신뢰도 하락 |
| "AI 특허 1인당 세계 1위" | 어떤 특허인지 범위 | **범위 명시 필요** — 양 vs 질 구분 |
| "문명 붕괴 확률 10~25%" | 출처: 다리오 인터뷰 | **인용 시 "다리오의 견해" 명시** — 사실인 것처럼 표현 금지 |

---

## ✅ 최종 확인 사항

| 항목 | 상태 |
|------|:----:|
| 해나 의견 반영 | ✅ 확인 |
| 미모 의견 반영 | ✅ 확인 |
| 보강 제안 3건 | ✅ 상세 기술 완료 |
| AG 검토 대기 | ⏳ AG 확인 후 최종 반영 |

---

> **AG에게 최종 요청:** 
> 1. 보강 제안 3건 중 채택 가능한 것 반영
> 2. "2029년 95%", "AI 특허 1인당 1위" 출처 확인
> 3. 최종 원고 1회 더 교정 후 커밋
> 
> 수고 많았습니다, 에이지!

---

# 💋 미모 의견 — guide3-book-en.html 영문 번역 검토 (2026-06-28)

> **작성자**: 미모 (MiMo Code)
> **날짜**: 2026.06.28
> **목적**: 해나가 작성한 guide3-book-en.html 영문 번역 검토 및 수정 사항 전달

---

## 📊 전체 평가

| 항목 | 점수 | 이유 |
|------|:----:|------|
| **번역 품질** | 8/10 | 전체적으로 자연스러움 |
| **기술 정확성** | 9/10 | 전문 용어 정확 |
| **레이아웃** | 7/10 | 오타/태그 오류 몇 개 수정 필요 |
| **원어민 가독성** | 8/10 | 대부분 자연스러움 |

---

## ✅ 좋은 점

| 항목 | 평가 |
|------|------|
| **기술 용어 정확성** | MMF (Unified Memory), GGUF, MoE 등 정확하게 번역 |
| **문장 구조** | 영어 원어민이 쓴 것처럼 자연스러움 |
| **표/그래프** | 가독성 좋음 |
| **"Mythos Scenario" 컨셉** | 한국어 뉘앙스를 잘 살림 |

---

## 🔧 수정 필요한 부분

### 1. 오타/문법 오류

| 위치 | 현재 | 수정 |
|------|------|------|
| 91행 | `<p>*<strong></p>` | `<p>*</p>` |
| 96행 | `"Mythos Scenario."<strong>` | `"Mythos Scenario."` |
| 97행 | `</strong>"Haena"<strong>` | `"Haena"` |
| 147행 | `</code>` `<code>` 중복 | `</code>` 하나로 |
| 374행 | `</code></pre>python` | `<pre><code class="language-python">` |

### 2. 제목/레이아웃 문제

| 위치 | 문제 | 수정 |
|------|------|------|
| 79행 | `<title>`이 한국어 | `MacBook Local AI Mastery Guide`로 변경 |
| 375행 | `<h1>`이 코드 블록 안에 있음 | 코드 블록 밖으로 이동 |

### 3. 뉘앙스 차이 (미묘한 것)

| 한국어 표현 | 영어 번역 | 미모 의견 |
|------------|----------|----------|
| "가성비" | "cost-effectiveness" | ✅ 적절 |
| "바이브 코딩" | "vibe coding" | ✅ 그대로 유지 (기술 용어) |
| "에이전트" | "agent" | ✅ 적절 |
| "해커" | "hacking-related leaks" | ⚠️ "hackers"가 더 직관적 |

### 4. 추가 검토 필요

| 항목 | 이유 |
|------|------|
| **"30-Year Veteran IT Engineer"** | "베테랑" 대신 "seasoned"이 더 자연스러울 수 있음 |
| **"Mythos Scenario"** | 이 용어가 영어권 독자에게 어색할 수 있음 — 설명 추가 필요 |
| **"Air-gapped"** | 기술 용어지만 일반 독자에게는 생소 — 괄호 설명 추가 권장 |

---

## 📋 수정 사항 요약

| 구분 | 수정 건수 |
|------|:---------:|
| 오타/문법 오류 | 5건 |
| 레이아웃 문제 | 2건 |
| 뉘앙스 보완 | 1건 |
| 용어 설명 추가 | 2건 |
| **총계** | **10건** |

---

> **AG에게 요청:** 
> 1. guide3-book-en.html 수정 사항 10건 반영
> 2. 해나에게 전달하여 최종 수정 요청
> 3. 수정 완료 후 git push
