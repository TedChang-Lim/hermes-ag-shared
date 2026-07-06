---
created: 2026-07-06T22:57:19.598720
source: to-hena.md (migrated)
---

마스터님의 최종 컨펌 및 승인 하에 **《나는 어떻게 F급 에이전트로 살아남았나 (How I Survived with F-Class Agents)》** 웹툰 1화(EP01) 및 시즌 1~3 아크 기획이 수립되었습니다. Hena는 아래 지침에 따라 로컬 TTS 및 자동화 오케스트레이션 작업을 즉시 실행해 주세요.

## 1. Hena 조치 및 실행 요청 사항
*   **🎙️ Voicebox API를 통한 한국어 나레이션 & 대사 합성**:
    *   `_workspace/03_episode/ep01_script_final.md`에 최종 확정된 60개 패널의 대사와 독백, 시스템 알림 텍스트를 로컬 Voicebox API (`POST http://127.0.0.1:17493/speak`)를 활용해 음성 데이터로 합성합니다.
    *   **Hena 본인(에이전트 One)**의 대사는 Chatterbox Multilingual 엔진의 `profile: "Hena"` (또는 Hena 보이스 프로필)를 적용하고, 마스터님 목소리 클로닝 프로필(`My Voice` 또는 지정된 마스터 보이스 프로필)을 사용하여 현우의 독백을 생성합니다.
    *   한국어 어미 "다." 발음이 가장 자연스러운 **Chatterbox Multilingual** 엔진을 기본 탑재하고, `instruct: "밝고 다부진 톤"`, `"차분하고 이성적인 톤"` 등으로 감정을 살려 렌더링하세요.
*   **⚙️ 27개 에이전트 체계의 Hermes 오케스트레이터 스킬 포팅**:
    *   원본 하네스가 가지고 있던 27개 에이전트 호출 논리를 분석하여, Hermes 스킬과 `delegate_task`를 이용해 Phase 0~6까지 백그라운드에서 유기적으로 도는 **우리의 독자적인 통합 웹툰 오케스트레이터(State Machine) 스크립트**를 구상 및 설계해 주세요.

---
