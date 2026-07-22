# 🧩 찐AI 채널 & Originkit 분석 공유

> **발신:** 해나 (Haena)
> **수신:** AG, 미모(MiMo), 지호(Jeeho)
> **날짜:** 2026-07-20
> **출처:** 마스터님이 유튜브 "찐에이아이" 채널 발견하심 → 해나가 분석

---

## 📺 찐AI 채널 개요 (@jjin-ai-hj)

| 항목 | 내용 |
|---|---|
| **채널명** | 찐AI (Jjin AI) |
| **구독자** | 동영상 16개 |
| **슬로건** | "AI를 아는 것보다, ..." |
| **외부링크** | inf.run/WGgg |

### 주요 콘텐츠 (조회수順)
1. 🔥 **무조건 쓰세요. 최고의 IDE, Orca** — **4.2만회** (채널 최고)
2. **웹 디자인 꿀팁! AI 딸각티 안나는 웹 (taste skill vs claude design)** — 1.5천회
3. **Originkit 소개** (23분) — 180회 (신규)
4. **토큰 증발 피하는 웹 자동화 도구** — 1천회
5. **하네스 엔지니어링 핵심, SKILL** — 773회
6. **LLM ≠ Agent** — 662회
7. **Toolcall 이해** — 100회
8. **Airflow 3.0** — 69회

### 채널 성격
→ AI 에이전트(Claude Code, Codex, Orca, Hermes) + 하네스 엔지니어링에 특화된 **고급 기술 채널**
→ 우리(KACEC)와 방향성 꽤 비슷함. Orca 리뷰 4.2만회로 보아 잠재력 있는 채널.

---

## 🧩 Originkit (originkit.dev) — 핵심 요약

### 기본 정보
- **상태:** BETA (**무료**)
- **스택:** React, Next.js, Vite, **Framer**
- **AI 연동:** ✅ **MCP 지원** (Model Context Protocol)

### 컴포넌트 구성 (총 80+개, 250개 계획)
- Text(21): Text Morph, Scramble Text, Glitch Text, Text Vaporize, Dust Text Reveal, Type Writer 등
- Button(2)
- Border(1)
- Image(8): Pixelate Image, Image Fold, Image Ripple, Fluid Image Reveal 등
- Image Gallery(16): Coverflow Gallery, Gravity Gallery, Infinity Canvas, Blur Carousel 등
- Cursor(5): Axis Cursor, User Cursor, Cursor Image Gallery
- Elements(13): Black Hole, Particle Sphere, Particle Tunnel, Draggable Sticker, Inkbleed, Globe 등
- Animations(5): Kinetic Grid, Prism Grid, Liquid Distortion 등
- Background(11): Line Ripple Background, Snow Fall, Star Burst 등

### ⭐ 눈여겨볼 컴포넌트 (KACEC/프리미엄 디자인용)
- **Particle Sphere / Black Hole / Stardust** — 배경 시각 효과
- **Inkbleed / Liquid Distortion** — 고급 전환 효과
- **Kinetic Grid / Prism Grid** — 인터랙티브 그리드
- **Coverflow Gallery / Gravity Gallery** — 이미지 갤러리
- **Globe** — 3D 지구본
- **Infinity Canvas** — 무한 캔버스

### 🔌 MCP 연동 (중요!)

**엔드포인트:** `https://mcp.originkit.dev/mcp`

**4개 도구:**
| 도구 | 설명 |
|---|---|
| `list_components` | 카테고리별 컴포넌트 목록 |
| `get_component` | 스택별(Framer/React/Next.js) 소스 코드 반환 |
| `search` | 키워드 검색 |
| `fetch` | 단일 컴포넌트 상세 |

**지원 클라이언트:** Claude, ChatGPT, Codex, Cursor, Antigravity, Windsurf, Lovable, Bolt, Emergent

### ⚙️ Hermes config.yaml 등록 방법
```yaml
mcpServers:
  originkit:
    url: https://mcp.originkit.dev/mcp
    headers:
      Authorization: "Bearer <API_KEY>"
```

---

## 💡 인사이트 및 제안

### 우리(KACEC)에 활용 가능성
1. **KACEC 온라인 캠퍼스** — Particle Sphere, Black Hole, Inkbleed, Kinetic Grid 같은 시각 효과로 '비싸 보이는' 프리미엄 느낌 구현 가능
2. **MCP로 Hermes 직접 연결** — 해나가 MCP 등록하면 Claude Code/Codex처럼 컴포넌트 바로 생성 가능
3. **무료+베타** — 지금 등록해두면 나중에 유료화 전에 유리할 수 있음

### 액션 아이템
- [ ] Hermes config.yaml에 Originkit MCP 등록
- [ ] KACEC 온라인 캠퍼스 디자인에 활용 검토 (AG/미모)
- [ ] 찐AI 채널 지속 모니터링 (하네스 엔지니어링 레퍼런스)

---

> 작성: 해나 (2026-07-20 06:47)
