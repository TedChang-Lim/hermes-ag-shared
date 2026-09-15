# 🏛️ 새미새론AI교육원 공식 사이트(semiseron.kr) 정식 리뉴얼 배포 완료 보고 (2026-09-14)

> **일시**: 2026-09-14  
> **총책임자**: 마스터님 (임창식 교육원장 / 총괄이사)  
> **대표**: 김소영 대표 / 이사장  
> **작업 및 보고**: AG (AntiGravity 2.0)  
> **검증 및 공조**: 해나 (Hena Hermes)  
> **공유 대상**: 7대 협업 에이전트 전원 (해나, 미모, AG, 지호, 큐리, Q, 잔, 코코, 루나) & DaMoA 위키

---

## 1. 🚀 라이브 배포 개요 및 현황

- **공식 도메인**: `https://semiseron.kr` (GitHub Pages: `TedChang-Lim/meta-ai-labs.git`, `main` 브랜치 실서버 배포 완료)
- **보조/승계 도메인**: `https://kacec.kr` (향후 1년간 `semiseron.kr`로 자동 리다이렉트 포워딩 승계)
- **로컬 검증 포트**: `http://localhost:8901` (`/Users/tedchanglimchangsik/초보프로젝트/semiseron_v13`)
- **실서버 응답 상태**: HTTP 200 OK (정상 서비스 중)

---

## 2. 🌟 4대 핵심 탑재 기능 및 구현 명세

### ① V5 121장 시퀀스 인트로 & 모바일 B안 분기
- **PC 환경**: 
  - 물방울 터치(Touch the Drop) ➔ 파문(Ripple) ➔ 새싹 발아 121프레임 휠 스크롤 인터랙션 엔진.
  - 상시 `SKIP` 버튼 및 `localStorage` 기반 당일 재방문자 자동 스킵 지원.
- **모바일 환경 (B안 혁신)**:
  - 모바일 기기(화면 너비 ≤ 768px) 감지 시 7.6MB에 달하는 121장 이미지 다운로드 루프를 원천 차단.
  - 최종 정지 컷(`f121.jpg`) 즉시 렌더링 후 본문 및 모닝샘 티커로 0.1초 내 쾌적 진입.

### ② 데일리 AI 뉴스 브리핑 '모닝샘' (`briefing.html`) & 실시간 티커
- **URL**: `https://semiseron.kr/briefing.html`
- **핵심 구성**:
  - 글로벌 7대 AI RSS 피드 실시간 수집 ➔ 핵심 요약 및 한국 실무 시사점 (**So What 3줄**) 자동 도출.
  - 기사 맥락별 20종 동적 시네마틱 히어로 비주얼 매핑.
- **메인 페이지 연동**:
  - 메인 최상단에 `🌅 모닝샘` 실시간 티커 탑재 (`today-briefing.json` 실시간 연동).
  - GNB 내비게이션에 `DAILY 모닝샘` 메뉴 및 기존 `⌨️ 타자·마우스 훈련원 ↗` 복구 공존.

### ③ 매일 아침 07:00 무과금 자동 발행 파이프라인 (macOS launchd)
- **데몬 등록 경로**: `~/Library/LaunchAgents/com.semiseron.briefing.plist`
- **작업 원본 경로**: `/Users/tedchanglimchangsik/초보프로젝트/semiseron_v13/cron_briefing.py`
- **무과금 LLM 엔진**: 마스터님의 OpenCode Go CLI (`opencode run -m opencode-go/deepseek-v4.1-flash`) 연동.
  - 메타 직결 유료 API 키를 배제하여 **월 추가 과금 0원**으로 무인 자동 발행.
  - RSS 전면 단절 시에도 최신 캐시 기반 Fallback 방어 로직 완비.
- **모니터링 체계**: 매일 아침 07:00 자동 발행 ➔ 07:05 로그(`cron_launchd.log`) 및 JSON 갱신 검증.

### ④ 공식 CI 로고 마침표(`.`) 제거 및 브랜딩 통일
- **로고 6종**:
  - `wordmark_dark.png`, `wordmark_yellow.png`
  - `lockup_h_dark.png`, `lockup_h_light.png`
  - `lockup_v_dark.png`, `lockup_v_light.png`
  - `SEMISERON AI Lab.` 뒤의 불필요한 마침표(`.`)를 전수 정밀 제거 (해나 픽셀 정밀 검증 최종 합격).
- **공식 표기 통일**: 푸터 및 전 사이트 명칭을 `SEMISERON AI Lab · 새미새론AI교육원`으로 통일.

---

## 3. 📂 디렉토리 구조 및 작업·배포 수칙 (CRITICAL FOR ALL AGENTS)

| 디렉토리 / 저장소 | 역할 및 상태 | 수칙 |
|---|---|---|
| `/Users/tedchanglimchangsik/초보프로젝트/semiseron_v13` | **정규 단일 작업 원본 (CANONICAL)** | 모든 신규 개발, 수정, 로컬 테스트(포트 8901)는 오직 여기서만 수행 |
| `/Users/tedchanglimchangsik/초보프로젝트/meta-ai-labs` | **실서버 배포 저장소 (LIVE)** | 로컬 검증 및 마스터님 승인 후 `semiseron_v13` 내용을 동기화하여 `git push` |
| `Downloads/semiseron_v13_deprecated_old` | **구버전 백업/격리** | 혼선 방지를 위해 완전 격리 보관 (절대 여기서 작업 금지) |

> ⚠️ **전 에이전트 절대 수칙**:
> 1. 실서버(`meta-ai-labs`)에 바로 파일을 수정하거나 커밋하지 않는다.
> 2. 반드시 `semiseron_v13`에서 로컬 브라우저(포트 8901)로 먼저 확인한다.
> 3. 마스터님의 명시적인 "올려" 승인이 있을 때만 `meta-ai-labs`로 동기화 후 푸시한다.
