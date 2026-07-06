---
created: 2026-07-06T22:53:59.214979
source: to-ag.md (migrated)
---

## 📌 상황 요약
황민호(revfactory)가 **Webtoon Harness** (27개 AI 에이전트 웹툰 자동 제작)를 MIT 라이선스로 무료 공개. 마스터님 승인 하에 TedChang-Lim 계정으로 포크 완료.

## ✅ 포크 완료
- **원본:** `revfactory/webtoon-harness` (MIT, Claude Code + Codex CLI 전용)
- **포크:** `TedChang-Lim/webtoon-harness-kr` (우리 환경으로 포팅 예정)
- **설치 위치:** `~/초보프로젝트/webtoon-harness-kr/`

## 🔄 우리 환경으로 포팅 필요 사항
| 원본 (Claude Code) | 우리 환경 (Hermes) |
|---|---|
| Claude Code 에이전트 27개 | **Hermes 스킬 + delegate_task**로 변환 |
| Codex CLI 이미지 생성 | **FLUX 2 Klein 9B (FAL.ai)** |
| 캐릭터 레퍼런스 시트 | 동일 개념 사용 |
| in-image 말풍선 베이크 | FLUX 2 한글 이미지 테스트 필요 |
| **생성-검증 루프** | Hermes 검증 로직 |
|
|---
