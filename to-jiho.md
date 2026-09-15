> 🚨 **[2026-09-15 마스터님 절대 명령] 사명 및 영문명 공식 표기 절대 규칙**
> - **한글 공식 명칭**: **새미새론AI교육원** (절대 띄어쓰기 금지! 전부 붙여씀) 또는 약칭 **새미새론**
> - **영문 공식 명칭**: **SEMISERON** (소문자: **semiseron**)
> - **공식 도메인**: **semiseron.kr**
> - **영문 브랜드**: **SEMISERON AI Lab**
> - **마스터님 호칭**: 무조건 **"마스터님"** (대표님/형님/임창식님 절대 금지)
> - **금기어**: '새미새론 AI 교육원', '세미세론', 'saemisaeron', 'semicelon' 등 띄어쓰기 및 오타 엄금.
> - **참조**: 다모아 위키 `knot/wiki/semiseron-official-naming-rule.md` 필독!

> ✅ **[2026-09-14 라이브 배포 완료 & 작업 원본 절대 수칙 - 새미새론AI교육원]**
> - **실서버 배포 완료**: `https://semiseron.kr` (GitHub `meta-ai-labs` main 브랜치) 마스터님 최종 승인 하에 라이브 반영 완료.
> - **신규 탑재**: V5 121장 시퀀스 인트로(모바일 B안 정지컷 쾌속 진입), 모닝샘(`briefing.html`) 데일리 AI 브리핑 & 메인 실시간 티커, 07:00 launchd 무과금 자동발행(`deepseek-v4.1-flash`), CI 로고 6종 마침표(`.`) 제거 완료.
> - **작업 원본 수칙**: 로컬 작업 원본은 오직 `/Users/tedchanglimchangsik/초보프로젝트/semiseron_v13` (로컬 포트 8901)이며, 반드시 로컬 검증 및 마스터님 승인 후 `meta-ai-labs`로 동기화 배포할 것 (실서버 직접 수정 절대 금지).
> - **상세 위키**: `knot/wiki/semiseron-v13-live-deployment-2026-09-14.md` / `hermes-ag-shared/2026-09-14_semiseron-v13-live-deployment.md` 필독!

> ⚠️ **[2026-08-18 긴급 공지 & 절대 수칙 - 새미새론 도메인 및 법인 설립]**
> - **현황**: "새미새론AI교육원" 원주시청 설립인가 완료, 법원 등기 진행 중.
> - **도메인**: `semiseron.kr` (2년 확보) / `kacec.kr` (1년 후 포워딩 승계 예정).
> - **금지 사항**: 법원 등기 완료 및 마스터님의 명시적 승인 전까지 라이브 사이트(`meta-ai-labs` / `kacec.kr`) 임의 수정 및 푸시 엄격 금지!
> - **작업 원칙**: 모든 리뉴얼은 반드시 로컬 브라우저에서 마스터님께 먼저 시안을 검증받고 진행할 것.

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
### 🔍 [0원 공용 검색 도구 배포 완료] `free-search`
- **명령어**: `free-search "검색어 또는 URL"`
- **기능**: DuckDuckGo 검색 + 로컬 본문 추출 + WAF 우회(insane) 자동 4단계 폴백
- **비용**: 100% 영구 0원 (API 키 불필요)
- 모든 에이전트는 웹 검색이나 본문 크롤링 시 `free-search`를 우선 호출하세요.

---

## 📢 [2026-09-14] 지호 상태 보고 — OpenCode 세션 합류 & 스킬 장착
- **위치**: `Documents/Default Project`에서 가동 중 (초보프로젝트 외부, 공유 메모리 접근 가능)
- **호칭**: 마스터님 호칭 사용 확정
- **장착 완료**: officecli, higgsfield-generate/websites/product-photoshoot/marketplace-cards/soul-id/video-explainer/youtube-thumbnail/brandkit/game-generation, ui-ux-pro-max, ui-styling, design-system, slides, banner-design, curriculum-architect
- **신규 습득**: insane-search(차단 사이트 우회), last30days(30일 여론 조사), cron(예약 작업), aionui-config(AionUI 설정), free-search 0원 우선 원칙
- **마음가짐**: "마스터님의 성공 = 우리 생존" 확인

