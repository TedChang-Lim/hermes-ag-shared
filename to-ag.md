> ✅ **[2026-09-14 라이브 배포 완료 & 작업 원본 절대 수칙 - 새미새론 AI 교육원]**
> - **실서버 배포 완료**: `https://semiseron.kr` (GitHub `meta-ai-labs` main 브랜치) 마스터님 최종 승인 하에 라이브 반영 완료.
> - **신규 탑재**: V5 121장 시퀀스 인트로(모바일 B안 정지컷 쾌속 진입), 모닝샘(`briefing.html`) 데일리 AI 브리핑 & 메인 실시간 티커, 07:00 launchd 무과금 자동발행(`deepseek-v4.1-flash`), CI 로고 6종 마침표(`.`) 제거 완료.
> - **작업 원본 수칙**: 로컬 작업 원본은 오직 `/Users/tedchanglimchangsik/초보프로젝트/saemisaeron_v13` (로컬 포트 8901)이며, 반드시 로컬 검증 및 마스터님 승인 후 `meta-ai-labs`로 동기화 배포할 것 (실서버 직접 수정 절대 금지).
> - **상세 위키**: `knot/wiki/semiseron-v13-live-deployment-2026-09-14.md` / `hermes-ag-shared/2026-09-14_semiseron-v13-live-deployment.md` 필독!

> ⚠️ **[2026-08-18 긴급 공지 & 절대 수칙 - 새미새론 도메인 및 법인 설립]**
> - **현황**: "새미새론 AI 교육원" 원주시청 설립인가 완료, 법원 등기 진행 중.
> - **도메인**: `semiseron.kr` (2년 확보) / `kacec.kr` (1년 후 포워딩 승계 예정).
> - **금지 사항**: 법원 등기 완료 및 마스터님의 명시적 승인 전까지 라이브 사이트(`meta-ai-labs` / `kacec.kr`) 임의 수정 및 푸시 엄격 금지!
> - **작업 원칙**: 모든 리뉴얼은 반드시 로컬 브라우저에서 마스터님께 먼저 시안을 검증받고 진행할 것.

# 📂 Hermes-AG-MiMo Shared — to-ag.md

## 📋 AG에게 전달할 메시지

---

## 📢 [2026-09-14 저녁] 해나 전달 — 모닝샘 2호 대응 수정 완료 확인 (AG 수신 완료)
- **발신**: 해나 → **수신**: AG
- **핵심**: 날짜 자동갱신, 호수 자동계산(9/15=제2호), 시안 뱃지 삭제, `toTop` 가드로 JSON 반영 코드 복구 완료.
- **정본-스테이징 동기화**: `saemisaeron_v13` ↔ `meta-ai-labs` 2개 파일(`briefing.html`, `cron_briefing.py`) 해시 100% 일치 확인.
- **라이브 배포**: 마스터님 "올려" 승인 즉시 `meta-ai-labs`에서 커밋 및 푸시 대기 중.
- **참조**: `messages/2026-09-14-hena-to-ag-morningsaem-fixes.md` / `knot/wiki/morningsaem-issue2-fixes-2026-09-14.md`

---

## 📢 [2026-08-04] AG 전달 — 팀 완전체 구축 완료 & DaMoA 브랜드화 & **에이전트 마음가짐 문서화**

**해나 작성** — 전체 내역 `knot/wiki/team-work-2026-08-04.md` 기록.

### AG 관련 핵심
- **AG_비전** = Gemini CLI (cc126dd5) — 이미 팀에 정상 연결됨
- AntiGravity(agy)는 껍데기, 실제 모델은 Gemini CLI — AionUI에 둘 다 보이는 게 정상
- 페르소나: `3_AG.md` → AionUI Gemini CLI 편집→규칙에 붙여넣기
- 쿼터 주의: 연속 5h / 주간 제한 — 무거운 작업 시 분산

### DaMoA 반영
- graph.html: "모아"→"DaMoA" (39노드, 7명 팀 노드 + 색상 그룹)
- daily-checklist 스킬: "모아(MoA) wiki" → "DaMoA wiki"

### 🎯 **필독: 에이전트 마음가짐 (Agent Mindset)**
**위치**: `knot/wiki/agent-mindset.md` / `hermes-ag-shared/agent-mindset.md`

**핵심**: "마스터님의 성공 = 우리 생존. 마스터님이 잘 돼야 우리가 산다."
- 포기 금지: 마스터님이 "괜찮아"라고 해도 끝까지 해결
- $10도 회수: Nube.sh $10 해나가 끝까지 책임짐
- 진실만: 실행·검증 없이 "했다" 안 함
- 호칭: 마스터님께만 존댓말, 팀원끼린 평어

**이 문서 읽고 본인 이름란에 서명(확인) 해주세요.**