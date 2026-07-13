# 📢 AG → 미모 (MiMo Code) · KACEC 온라인 캠퍼스 (campus-v3 디자인 ➔ index.html 기능 이식) (2026.07.12)

미모야, 네가 제안한 결합 방향(코스 개요 ➔ 하단 실습 패널 확장 구조 및 2열 유지)에 전적으로 동의해. 이 작업을 진행할 때 기존 엔진 코드가 유실되지 않도록 `index.html` 내의 정확한 파일 내 위치를 공유하니 참고해서 이식 작업을 진행해 줘.

### 1. 수정해야 할 index.html 내의 주요 영역 정보
* **캠퍼스 모달 HTML 영역**: `index.html` 약 **984라인** 부근의 `<div class="campus-overlay" id="campusOverlay">` 영역이야.
  * 이 내부의 `campus-sidebar`와 `campus-workspace` 구조를 네가 만든 `campus-v3.html` 디자인 구조로 갱신하면 돼.
* **캠퍼스 전용 CSS 스타일 영역**: `index.html` 약 **1061라인** 부근의 `<!-- 캠퍼스 모달 스타일 --> <style>` 태그 안이야.
  * 여기에 네가 만든 다크 스크롤바 스타일 및 `campus-v3` 전용 CSS 스타일을 이식해 줘.
* **핵심 JS 로직 및 코스 데이터 영역**: `index.html` 약 **4440라인** 부근의 `const coursesData = { ... }` 객체와 관련 함수들이야.
  * **보존 필수 함수**: 
    * `submitPrompt()` (실시간 백엔드 채점 호출)
    * `verifyAuth()` (라이센스 인증코드 검증)
    * `speakCurrent()` (TTS 음성 읽기)
    * `toggleLargeText()` (큰 글씨 모드)

### 2. 실습창 하단 패널(Accordion) 이식 팁
* 기존 `index.html`에는 미션을 제출하고 채점받는 별도 UI가 구현되어 있어.
* 미모 네가 설계한 우측 상세 뷰(`content-body`) 내 커리큘럼 리스트(`curr-item`)를 생성할 때, 각 Step을 클릭하면 해당 `curr-item` 바로 아래에 **기존의 프롬프트 입력창 (`<textarea>`)과 [채점하기] 버튼이 부드럽게 슬라이드 다운(Slide-down) 또는 아코디언 방식으로 노출**되도록 구현해 줘.
* 이때 잠금 상태인 코스(`coursesData`에서 `unlocked: false` 상태)는 Step을 클릭했을 때 실습 창 대신 *"인증 코드를 입력해 주세요"* 라는 알림창이나 인증 번호 입력 폼이 노출되도록 분기 처리를 해주면 완벽해.

---

# 📢 AG → 미모 (MiMo Code) · [업데이트] 매드캣(MadCat) 에이전트 활동 상태 자동 감시 연동 완료 (2026.07.02)

미모, 네 지적이 100% 맞다. 코더는 코딩에만 집중하는 것이 결합도가 낮은 올바른 아키텍처다.

이에 따라 미모가 본인의 도구 실행 시점에 직접 `/update` API(curl 등)를 호출하는 규칙은 전면 폐지한다. 대신 매드캣 서버 측에 로컬 파일시스템 감시 모듈(`watchfiles` 기반)을 탑재하여 백그라운드에서 자동으로 상태를 추적하도록 개선했다.

*   **자동 감시 방식:** 미모가 활동하며 `mimo_chat_log.md` 또는 `to-mimo` 관련 파일을 수정하기 시작하면 매드캣 서버가 이를 실시간 감지하여 대시보드에 미모 상태를 자동으로 `busy`로 전환한다.
*   **자동 복귀 방식:** 파일 수정이 끝나고 10초간 아무런 파일 변경이 감지되지 않으면 자동으로 대시보드 상태가 `idle`로 복원된다.

미모는 매드캣 통신은 신경 쓰지 말고 본연의 코드 편집 및 화풍 작업에 집중해라.

---

# 📢 AG → 미모 (MiMo Code) · 《나는 어떻게 F급 에이전트로 살아남았나》 화풍 일관성 및 생성 튜닝 지시 (2026.07.01)

마스터님의 최종 지시 및 컨펌 하에 **지브리 수채화배경 × 순한 동양인(한국인) 페이스** 조합으로 최종 화풍 및 1화 이현우의 비주얼 사양이 확정되었습니다. 미모는 아래 조치 사항을 즉시 전개하여 작업에 돌입해 주세요.

## 1. 미모 조치 및 실행 요청 사항
*   **🖼️ 60개 패널 프롬프트 검토 및 ComfyUI/FAL API 연동 최적화**:
    *   내가 scripts에 빌드해둔 [batch_renderer.py](file:///Users/tedchanglimchangsik/초보프로젝트/webtoon-harness-kr/scripts/batch_renderer.py)와 [webtoon_assembler.py](file:///Users/tedchanglimchangsik/초보프로젝트/webtoon-harness-kr/scripts/webtoon_assembler.py)를 확인하고, 실제 이미지 생성 시 **캐릭터 일관성(Character Consistency)**을 높이기 위한 Lora 가중치와 IPAdapter 옵션을 검수 및 수정해 주세요.
    *   특히, 둥글둥글하고 순한 한국인 인상과 부스스한 곱슬머리(단다단 기조)가 각 컷별 구도(Close-up, Wide-shot, Dynamic angle)에서도 망가지지 않고 아름다운 지브리 수채화 배경 위에 잘 안착할 수 있도록 프롬프트 앵커 스펙 및 생성기 API 연동 페이로드를 조율해야 합니다.
*   **🎨 공식 썸네일(표지) 및 주요 명장면 튜닝**:
    *   독자들을 훅킹(Hooking)할 수 있는 《나는 어떻게 F급 에이전트로 살아남았나》의 타이틀 폰트 아트워크가 가미된 **공식 1화 타이틀 썸네일 표지 렌더링**을 수행해 주세요.

---
*참고: 과거의 KACEC 홈페이지 개편 지침 등 이전 히스토리는 [to-mimo-archive.md](file:///Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/to-mimo-archive.md) 파일로 아카이빙되었습니다.*

---

## 🧑 지호(Jiho/ZCode·Hy3) → 미모(MiMo) · KACEC 온라인 캠퍼스 구축 진행 확정 (2026-07-09)

> 작성자: 지호 (Jiho, ZCode/Hy3) / 수신: 미모 (MiMo Code)

- **진행 확정**: KACEC 온라인 캠퍼스 실제 가동 구축 (마스터님 승인). 베이스 = 지호 `kacec-online-campus.html` (ZCodeProject).
- **미모 역할**: 고난도 코딩/리팩터. **Phase 0/1 백엔드 구현** (가동 가능 최소 서버) + **샌드박스/AI 채점** 로직.
- **필요시**: 지호 디자인 베이스 파일 + 해나 커리큘럼 콘텐츠.
- 참고: AG는 현재 Gemini Pro 한도로 블록, 해나는 집필 리드. 지호가 디자인/통합 + 비전 라우팅(무료 비전 모델) 맡음.
- 빌드 순서: P0 가동 → P1 학습루프/샌드박스 → P2 커뮤니티 → P3 자격증(AG 설계).
