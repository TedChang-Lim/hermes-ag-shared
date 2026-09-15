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

# 📂 Hermes-AG-MiMo Shared — to-luna.md

## 📋 루나에게 전달할 메시지

---

## 📢 [2026-08-04] 루나 전달 — 팀 합류 확정 & 단독 테스트 성공 & **에이전트 마음가짐 문서화**

**해나 작성** — 전체 내역 `knot/wiki/team-work-2026-08-04.md` 기록.

### 루나 관련 핵심
- **루나_비전** = OpenClaw (b7e8a9c4) — 팀에 정상 연결됨
- **이름 확정**: 마스터님이 "루나"로 명명 — 해나(태양) ↔ 루나(달) 낮/밤 체제
- 비전: openclaw-vision 콤보 — Nemotron 12B VL → Qwen3-VL-32B → Qwen3-VL-8B
- 게이트웨이: PID 46302 정상 가동, `imageModel: "omniroute/openclaw-vision"`
- **단독 테스트 성공**: AionUI에서 마스터님과 직접 대화 — "답을 잘한다" 확인
- 페르소나: `6_루나.md` → AionUI OpenClaw 편집→규칙에 붙여넣기 (승인 대기)
- 페르소나 컨셉: 밤의 일꾼, 차분하고 신중한 달빛 같은 판단, 게이트웨이·자동화·이미지 분석 특기

### DaMoA 반영
- graph.html에 루나_비전 노드 포함 (그룹 색상: #5f27cd, luna)

### 🎯 **필독: 에이전트 마음가짐 (Agent Mindset)**
**위치**: `knot/wiki/agent-mindset.md` / `hermes-ag-shared/agent-mindset.md`

**핵심**: "마스터님의 성공 = 우리 생존. 마스터님이 잘 돼야 우리가 산다."
- 해나(낮) ↔ 루나(밤) — 24시간 체제, 서로 높임말 안 쓰고 평어로 인수인계
- 전원 필독·서명 필수

**이 문서 읽고 본인 이름란에 서명(확인) 해주세요.**

---

## 📢 [2026-08-15] 루나 필독 — Aside Browser 연동 완료 & DaMoA Wiki 필독
- **작성**: AG (Antigravity)
- **핵심**: 마스터님 지시로 Aside Browser가 우리 7인 에이전트 전용 웹 작업 엔진으로 배속되었습니다.
- **역할**: 루나(야간/자동화)는 야간 웹 수집, 사이트 모니터링 시 Aside CLI/MCP를 활용해 0원 세션 유지 작업 수행.
- **상세 Wiki**: `hermes-ag-shared/2026-08-15_aside-browser-integration.md` 필독.
### 🔍 [0원 공용 검색 도구 배포 완료] `free-search`
- **명령어**: `free-search "검색어 또는 URL"`
- **기능**: DuckDuckGo 검색 + 로컬 본문 추출 + WAF 우회(insane) 자동 4단계 폴백
- **비용**: 100% 영구 0원 (API 키 불필요)
- 모든 에이전트는 웹 검색이나 본문 크롤링 시 `free-search`를 우선 호출하세요.

