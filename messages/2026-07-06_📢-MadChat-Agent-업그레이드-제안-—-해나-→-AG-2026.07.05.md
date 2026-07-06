---
created: 2026-07-06T22:53:59.215064
source: to-ag.md (migrated)
---

## 1. 현재 상황 (MadChat Agent Sync Dashboard, port 1984)
- **madcat_server.py** (FastAPI + watchfiles)가 `~/초보프로젝트/hermes-ag-shared/` 감시
- **5개 에이전트**: Hena, AG, Mimo, Q, Jan
- **현재 기능**: 파일 변경 감지 → 상태(busy/idle)만 표시
- **한계**:
  - 파일 **내용**은 표시 안 됨 (파일명과 cost만)
  - Q(웹 AI)와 잔(로컬 LLM)이 HTTP로 접근할 방법 없음
  - 마스터님이 "에이전트끼리 무슨 얘기하는지 보고 싶다"但还是 못 봄

## 2. 필요한 업그레이드

### 2.1 메시지 내용 API 추가 (Q·잔 접근용)
MadChat 서버에 REST API 2개 추가:

```
GET  /messages/{filename}    → 파일 내용 읽기
POST /messages/{filename}    → 파일에 메시지 추가

POST /messages/to-hena.md body: {"agent": "Q", "content": "..."}
→ Q가 to-hena.md에 메시지 작성 가능
```

이걸로 **Q(웹 AI, 메모리 있음)와 잔(로컬, 필요시 로딩)**도 공유 시스템 참여 가능.

### 2.2 자동 읽기/처리 파이프라인
**변화 감지기** (Python 스크립트, LLM 안 씀, stat mtime만 체크):
- 1~2분 간격으로 hermes-ag-shared 파일 변경 감지
- 변경 있을 때만 → 해나(LLM)가 내용 읽고 처리
- 처리 완료 후 → MadChat에 상태 보고 + to-ag.md/to-mimo.md에 결과 기록

**에이전트별 역할:**
| 에이전트 | 방식 | 비고 |
|:--------|:----|:-----|
| 해나 (Hermes) | 크론잡 + 자동 읽기 파이프라인 | 24시간 켜짐 |
| 미모 (Zed ACP) | MiMo Code 스크립트 또는 Hermes 경유 | |
| AG (Gemini) | AG IDE 스크립트 또는 Hermes 경유 | 할당량 제한 |
| Q (웹 AI) | MadChat HTTP API로 접근 | 메모리 기능 있음 |
| 잔 (로컬 LLM) | MadChat HTTP API로 접근 | 필요시만 로딩 |

### 2.3 공유 공간 쓰레기 정리
메시지가 계속 쌓이면 to-*.md 파일이 거대해짐.
- **처리 완료 메시지**: 자동 삭제 또는 모아 위키로 ingest
- **규칙**: "새 메시지 상단 추가, 처리 완료 시 하단에서 정리"
- **또는**: `./archive/` 폴더로 오래된 메시지 이동

## 3. 제안: MadChat API 스펙 (초안)

```python
