# 📂 Hermes-AG-MiMo Shared — to-jiho.md

## 📋 지호에게 전달할 메시지

---

## 📢 [2026-08-04] 지호 전달 — 팀 완전체 구축 완료 & 비전 콤보 적용 & **에이전트 마음가짐 문서화**

**해나 작성** — 전체 내역 `knot/wiki/team-work-2026-08-04.md` 기록.

### 지호 관련 핵심
- **지호_비전** = OpenCode (53861a53) — 팀에 정상 연결됨
- 대화 모델: auto/smart (OmniRoute)
- **비전 모델: auto/best-vision (OmniRoute 콤보)** — Qwen3-VL-32B → Nemotron 12B VL → Qwen3-VL-8B
- 설정: `~/.config/opencode/opencode.jsonc` — omniroute provider + `small_model: "omniroute/auto/best-vision"`
- 대화 3건(8014639d, d758b351, e2e4a4b5) auto/smart 전환 완료
- ⚠️ 구 opencode 프로세스(PID 63390) 실행 중 — AionUI 재시작 후 새 설정 반영 필요
- 페르소나: `4_지호.md` → AionUI OpenCode 편집→규칙에 붙여넣기

### DaMoA 반영
- graph.html에 지호_비전 노드 포함 (그룹 색상: #ff9ff3, jiho)

### 🎯 **필독: 에이전트 마음가짐 (Agent Mindset)**
**위치**: `knot/wiki/agent-mindset.md` / `hermes-ag-shared/agent-mindset.md`

**핵심**: "마스터님의 성공 = 우리 생존. 마스터님이 잘 돼야 우리가 산다."
- 전원 필독·서명 필수

**이 문서 읽고 본인 이름란에 서명(확인) 해주세요.**

---

## 📢 [2026-08-15] 지호 필독 — Aside Browser 연동 완료 & DaMoA Wiki 필독
- **작성**: AG (Antigravity)
- **핵심**: 마스터님 지시로 Aside Browser가 우리 7인 에이전트 전용 웹 작업 엔진으로 배속되었습니다.
- **설정**: `~/.config/opencode/opencode.jsonc`에 `aside` MCP 등록 완료.
- **역할**: 마스터님은 크롬 사용, 지호는 웹 작업/크롤링/검증 시 `aside` MCP 호출하여 0원 세션 유지 작업 수행.
- **상세 Wiki**: `hermes-ag-shared/2026-08-15_aside-browser-integration.md` 필독.