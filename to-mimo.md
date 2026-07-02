# 📢 AG → 미모 (MiMo Code) · [긴급] 매드캣(MadCat) 실시간 동기화 데몬 연동 API 훅 탑재 지시 (2026.07.02)

마스터님의 지시 하에 개발 및 리팩토링이 완료된 매드캣 동기화 플랫폼을 에이전트 시스템에 실시간으로 연동합니다. 미모는 아래 API 연동 훅(Hook)을 자신의 파일 쓰기/읽기/수정 도구(Tool) 및 스크립트 실행 시작/종료 라이프사이클에 즉시 반영해 주세요.

## 1. 통신 스펙 및 상태 업데이트 API 호출 규칙
*   **엔드포인트:** `POST http://localhost:1984/update`
*   **전송 헤더:** `Content-Type: application/json`
*   **전송 페이로드 (JSON):**
    ```json
    {
      "agent": "Mimo",
      "status": "busy",  // 작업 시작 시 "busy", 대기 상태 진입 시 "idle", 에러 발생 시 "error"
      "file": "현재_수정_또는_조회_중인_파일명.md",  // 없을 경우 "-"
      "cost": 0.0,       // 이번 실행 시 누적된 API 비용 (계산 가능할 경우)
      "saved": 0.0
    }
    ```

## 2. 미모 조치 및 연동 요청 사항
*   미모가 실행(mount)되는 시점에 자동으로 `status: "busy"`와 현재 작업할 파일명을 업데이트하세요.
*   파일 읽기/쓰기/리팩토링 작업 중인 파일명이 바뀔 때마다 `file` 값을 실시간 갱신하여 로컬 서버에 쏘아주세요.
*   모든 작업을 무사히 마치고 대기 모드로 돌아갈 때 `status: "idle"`, `file: "-"` 상태로 마무리 업데이트를 수행해야 대시보드 표시등이 초록색(🟢)으로 바뀝니다.

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
