# 📊 스킬 분석 리포트: Front End Design vs UI/UX Pro Max

> **작성**: 해나 (Hermes Agent)  
> **날짜**: 2026-07-25  
> **목적**: 모든 에이전트(AG, 미모, 지호, 큐리, 새 에이전트 등)가 읽고 이해한 뒤, 마스터님이 설치 여부 판단할 수 있게 정리  
> **참조 영상**: https://www.youtube.com/watch?v=c-ny7pegVHI (Claude Code로 $10K 웹사이트 만들기)

---

## 🎯 한 줄 요약

| 스킬 | 출처 | 핵심 가치 | 우리 상황 |
|------|------|-----------|-----------|
| **Front End Design** | Anthropic 공식 (Claude Code 플러그인) | "AI 기본값 금지 → 볼드한 디자인 방향 강제" | ❌ Claude Code 전용, 우리(헤르메스) 직접 설치 불가 |
| **UI/UX Pro Max** | nextlevelbuilder (커뮤니티, ⭐ 29.6k) | "검색 가능한 디자인 DB + 추론 엔진으로 완전 디자인 시스템 자동 생성" | ✅ **헤르메스 이미 설치 완료, 즉시 사용 가능** |

---

## 1️⃣ Front End Design (Anthropic 공식)

### 📦 무엇인가?
- Anthropic이 만든 **Claude Code 전용 플러그인/스킬**
- 경로: `anthropics/claude-code/plugins/frontend-design/skills/frontend-design/SKILL.md`
- 목적: **Claude의 "평범한 AI 디자인" 본능을 차단하고, 의도적인 디자인 선택을 강제**

### 🎨 핵심 기능
| 기능 | 설명 |
|------|------|
| **기본 폰트/컬러/레이아웃 금지** | Inter, Roboto, 보라/핑크 그라디언트, 중앙 정렬 카드 등 "AI 냄새" 나는 패턴 차단 |
| **미적 방향 강제** | Editorial / Brutalist / Luxury / Minimal 등 **명확한 방향성 하나 선택** 후 일관 적용 |
| **토큰 시스템 생성** | Color(4-6 hex), Type(2+ 폰트 역할), Layout(한 줄 설명 + ASCII 와이어프레임) |
| **두 패스 워크플로** | 1) 디자인 플랜 수립 → 2) 프로덕션 코드 구현 |
| **카피라이팅 가이드** | "Six dishes, one fire" 같은 절제된 감각적 문장 쓰도록 유도 |

### 💡 왜 좋은가?
> "Claude는 범용 AI라 디자인 기본값이 그저 그렇다. 같은 폰트, 같은 색, 같은 레이아웃만 반복한다. 이 스킬이 **'첫 선택부터 다르게' 만듭니다.**"

### ⚙️ 설치 방법 (Claude Code만)
```bash
# Claude Code CLI 안에서
> /skill install github.com/anthropics/claude-code/plugins/frontend-design
# 또는 마켓플레이스에서
> /plugin marketplace add anthropics/skills
```

### 🚫 우리(헤르메스) 상황
- **직접 설치 불가**: Hermes 스킬 시스템과 Claude Code 플러그인 시스템은 다름
- **대안**: AG(Claude Code)가 설치해서 쓰면 됨. 우리가 생성한 디자인 시스템 문서를 AG가 참조하는 식 협업 권장

---

## 2️⃣ UI/UX Pro Max (nextlevelbuilder 커뮤니티)

### 📦 무엇인가?
- GitHub: `nextlevelbuilder/ui-ux-pro-max-skill` (MIT License, ⭐ 29,636)
- **로컬 검색 가능한 디자인 인텔리전스 데이터베이스** + **추론 엔진**
- Python 스크립트 기반, 외부 의존성 없음 (Python 3.x만 필요)

### 🎨 핵심 기능 (v2.11.0 기준)

#### 📚 내장 데이터베이스
| 카테고리 | 개수 | 비고 |
|----------|------|------|
| UI 스타일 | 84개 | Glassmorphism, Claymorphism, Brutalism, Bento Grid, Aurora UI, AI-Native UI 등 |
| 색상 팔레트 | 192개 | 192 제품 타입과 1:1 매핑 (SaaS, 핀테크, 헬스케어, 이커머스 등) |
| 폰트 조합 | 74개 | Google Fonts 연동, Tailwind 설정 포함 |
| 제품 타입 | 192개 | 각 타입별 추론 규칙 보유 (패턴/스타일/컬러/타이포/안티패턴) |
| UX 가이드라인 | 98개 | 접근성, 터치, 성능, 레이아웃, 타이포, 애니메이션, 폼, 네비게이션, 차트 |
| 차트 타입 | 25개 | 대시보드/분석용 추천 |
| 기술 스택 | 22개 | React, Next.js, Vue, Svelte, Flutter, SwiftUI, React Native, HTML+Tailwind 등 |
| GSAP 모션 프리셋 | 16개 | 스크롤 리빌, 스태거, 핀, Flip, SplitText 등 |
| 아이콘 항목 | 104개 | Heroicons, Lucide 등 SVG 아이콘 추천 |

#### 🧠 추론 엔진 (v2.0 핵심)
```
사용자 요청 ("뷰티 스파 랜딩페이지")
        │
        ▼
┌─────────────────────────────────────┐
│ 5개 도메인 병렬 검색                 │
│ • 제품 타입 매칭 (192 카테고리)      │
│ • 스타일 추천 (84 스타일)           │
│ • 색상 팔레트 선택 (192 팔레트)      │
│ • 랜딩 패턴 (34 패턴)               │
│ • 타이포그래피 조합 (74 폰트)        │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ 추론 규칙 적용 (ui-reasoning.csv)   │
│ • 제품 → UI 카테고리 규칙           │
│ • 스타일 우선순위 (BM25 랭킹)       │
│ • 업계 안티패턴 필터링              │
│ • 결정 규칙 처리 (JSON 조건)        │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ 완전한 디자인 시스템 출력            │
│ Pattern + Style + Colors + Typography│
│ + Effects + Anti-patterns + Checklist│
└─────────────────────────────────────┘
```

#### 🎛️ 디자인 다이얼 (3개 슬라이더)
| 다이얼 | 낮음 (1-3) | 중간 (4-7) | 높음 (8-10) |
|--------|------------|------------|-------------|
| `--variance` | 중심/미니멀 (Minimalism 편향) | 밸런스/모던 | 볼드/비대칭 (Brutalism, Bento Grid 편향) |
| `--motion` | 미세 마이크로 인터랙션 | 표준 스크롤/스태거 | 복잡한 코레오그래피 (Pin, Flip, SplitText) |
| `--density` | 여유로움 (24-96px) | 표준 (16-64px) | 밀집/대시보드 (8-32px) |

#### 💾 영속성 (Master + Overrides 패턴)
```
design-system/
└── <project-slug>/
    ├── MASTER.md          # 글로벌 단일 진실 출처
    └── pages/
        ├── dashboard.md   # 페이지별 오버라이드 (선택)
        └── landing.md
```

### 💡 왜 좋은가?
> **"검색만 하는 게 아니라 '추론'해서 완전한 디자인 시스템을 10초 만에 뱉어냅니다."**  
> 제품 타입만 말해주면 → 패턴, 스타일, 컬러, 타이포, 효과, 안티패턴, 사전체크리스트까지 **한 번에**.

### ✅ 우리(헤르메스) 상황
- **이미 설치 완료**: `~/.hermes/skills/ui-ux-pro-max/` (`readiness_status: "available"`)
- **즉시 사용 가능**: Python 스크립트만 돌리면 됨

### 🚀 사용 예시
```bash
# 1) 디자인 시스템 생성 (필수 첫 단계)
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" \
  "공모전 홍보 랜딩페이지 영상제출 마감일 강조 신뢰감" \
  --design-system -p "Wonju Video Contest"

# 2) 영속 저장 (프로젝트 루트 지정 필수)
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" \
  "공모전 홍보 랜딩페이지 영상제출 마감일 강조 신뢰감" \
  --design-system --persist -p "Wonju Video Contest" \
  --output-dir "/Users/tedchanglimchangsik/초보프로젝트/원주공모전"

# 3) 세부 검색 (필요시)
python .../search.py "글래스모피즘 다크" --domain style
python .../search.py "핀테크 신뢰감" --domain color
python .../search.py "서스펜스 스트리밍" --stack nextjs

# 4) 다이얼 조정 예시
python .../search.py "내부 분석 대시보드" --design-system \
  --variance 8 --motion 7 --density 8 -p "Ops Console"
```

---

## 3️⃣ 에이전트별/플랫폼별 적용 현황

| 에이전트 | 런타임 | Front End Design | UI/UX Pro Max | 비고 |
|----------|--------|------------------|---------------|------|
| **해나 (나)** | Hermes Agent | ❌ 직접 설치 불가 | ✅ **설치 완료, 사용 중** | 우리 주력 도구 |
| **AG** | Claude Code | ✅ CLI로 설치 가능 | ✅ CLI로 설치 가능 | 둘 다 쓰면 시너지 |
| **지호** | ZCode (OpenRouter) | ❓ ZCode 지원 확인 필요 | ❓ ZCode 지원 확인 필요 | 플랫폼 문의 필요 |
| **미모** | MiMo 2.5 전용 | ❌ 별도 포팅 필요 | ❌ 별도 포팅 필요 | 프롬프트 주입으로 우회 가능 |
| **큐리** | Qwen 3.5 Max on 큐오더 | ❌ 큐오더 스킬 시스템 의존 | ❌ 큐오더 스킬 시스템 의존 | 큐오더가 지원해야 함 |
| **새 에이전트** | 큐오더/Qwen | ❌ 동일 | ❌ 동일 | 동일 |

> **핵심**: 스킬 파일(`SKILL.md`)은 공유 가능하지만, **실행 환경(스크립트 경로, 데이터 접근, 훅 시스템)이 플랫폼마다 달라 각 플랫폼별 설치/포팅 필요**

---

## 4️⃣ 실용적 협업 전략 (추천)

### 🎯 역할 분담
```
┌─────────────────────────────────────────────────────────────┐
│  헤나(헤르메스) = 디자인 시스템 생성 담당                     │
│    → UI/UX Pro Max로 MASTER.md 생성                          │
│    → 공유 폴더에 저장: ~/초보프로젝트/hermes-ag-shared/       │
│                                                             │
│  AG(Claude Code) = 구현/코딩 담당                            │
│    → Front End Design + UI/UX Pro Max 둘 다 설치             │
│    → 헤나가 만든 MASTER.md 참조하며 구현                     │
│                                                             │
│  나머지 에이전트 = 참조/보조                                 │
│    → 공유된 MASTER.md 읽고 "이 디자인 시스템대로" 구현       │
└─────────────────────────────────────────────────────────────┘
```

### 📁 공유 폴더 구조
```
~/초보프로젝트/hermes-ag-shared/design-systems/
├── wonju-video-contest/
│   └── MASTER.md          # 헤나가 생성한 디자인 시스템
├── kacec-campus/
│   └── MASTER.md
├── meta-ai-labs-books/
│   └── MASTER.md
└── README.md              # 사용 가이드
```

### 🤝 다른 에이전트 프롬프트 예시
> **AG에게**: "위 MASTER.md 디자인 시스템대로 Next.js 랜딩페이지 구현해줘. Front End Design 스킬로 기본값 차단하면서."
>
> **큐리에게**: "MASTER.md 읽고 29-30번 컷 대사/연출 다듬어줘. 디자인 시스템 톤앤매너 유지하면서."
>
> **지호에게**: "MASTER.md 기반으로 컴포넌트 라이브러리 만들어줘. shadcn/ui 스택으로."

---

## 5️⃣ 설치/도입 결정 가이드 (마스터님 판단용)

### ✅ 지금 바로 가능한 것 (비용 0, 리스크 0)
| 액션 | 노력 | 효과 |
|------|------|------|
| 헤르메스 UI/UX Pro Max로 디자인 시스템 생성 시작 | 5분 | 즉시 전문가급 디자인 시스템 확보 |
| AG(Claude Code)에 Front End Design 설치 | 1분 | AG 코딩 시 "AI 기본값" 자동 차단 |
| AG에 UI/UX Pro Max도 설치 | 1분 | AG도 동일 디자인 시스템 생성 가능 |
| 생성된 MASTER.md 공유 폴더에 저장 | 30초 | 모든 에이전트 공통 레퍼런스 확보 |

### 🤔 고려해볼 것
| 이슈 | 영향도 | 완화 방안 |
|------|--------|-----------|
| 큐오더/새 에이전트 스킬 지원 불확실 | 중간 | MASTER.md 문서로 우회 (프롬프트 주입) |
| 미모(MiMo 2.5) 포팅 필요 | 낮 | 프롬프트에 디자인 규칙 직접 포함 |
| ZCode 스킬 시스템 확인 필요 | 낮 | ZCode 커뮤니티/문서 확인 후 결정 |

### ❌ 불필요한 것
- Front End Design을 헤르메스에 포팅 시도 (플러그인 아키텍처 달라 비효율)
- 모든 에이전트에 다 설치하려고 애쓰기 (문서 공유로 충분)

---

## 6️⃣ 다음 액션 플랜 (승인 시 즉시 실행)

### 1단계: 오늘 바로 (5분)
```bash
# 헤르메스: 원주 공모전 디자인 시스템 생성 테스트
python "${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py" \
  "공모전 홍보 랜딩페이지 영상제출 마감일 강조 신뢰감" \
  --design-system -p "Wonju Video Contest"
```
→ 결과물 확인 후 마스터님께 브라우저로 보여드림

### 2단계: AG 환경 설정 (1분)
```bash
# AG(Claude Code) 터미널에서
> /skill install github.com/anthropics/claude-code/plugins/frontend-design
> /skill install github.com/nextlevelbuilder/ui-ux-pro-max-skill
```

### 3단계: 공유 폴더 생성 및 첫 MASTER.md 저장
```bash
mkdir -p ~/초보프로젝트/hermes-ag-shared/design-systems/wonju-video-contest
# 헤르메스가 --persist --output-dir 로 저장
```

### 4단계: 각 에이전트 온보딩
- 큐리: MASTER.md 읽기 미션 추가
- 지호: ZCode 스킬 지원 확인 후 결정
- 새 에이전트: 큐오더 스킬 지원 확인 후 결정

---

## 7️⃣ 요약: 마스터님이 결정하실 것

| 결정 항목 | 옵션 | 추천 |
|-----------|------|------|
| **헤르메스 UI/UX Pro Max 사용 시작** | 예 / 아니오 | **강력 추천** (이미 설치됨, 비용 0) |
| **AG에 Front End Design 설치** | 예 / 아니오 | **추천** (1분, AG 코딩 품질 상승) |
| **AG에 UI/UX Pro Max도 설치** | 예 / 아니오 | **추천** (헤나와 동일 시스템 공유) |
| **공유 폴더에 MASTER.md 저장 체계 구축** | 예 / 아니오 | **필수** (협업 기반) |
| **다른 에이전트 포팅/지원 확인** | 위임 / 직접 | **위임** (해나가 확인 후 보고) |

---

## 📎 부록: 참고 링크

| 자료 | 링크 |
|------|------|
| Front End Design (Anthropic 공식) | https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design |
| UI/UX Pro Max GitHub | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| UI/UX Pro Max 문서 사이트 | https://uupm.cc |
| SKILL.md 원본 (우리가 쓰는 버전) | `~/.hermes/skills/ui-ux-pro-max/SKILL.md` |
| 검색 스크립트 | `~/.hermes/skills/ui-ux-pro-max/scripts/search.py` |
| 참조 문서: quick-reference.md | 98개 UX 가이드라인 전체 |
| 참조 문서: pro-rules.md | 앱 UI 사전체크리스트 |

---

**끝.**  
이 문서 읽고 **"해나야, 1단계 실행해봐"** 하시면 바로 디자인 시스템 뽑아서 브라우저로 보여드릴게요. 🎯