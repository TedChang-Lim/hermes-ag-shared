---
created: 2026-07-06T22:57:19.599911
source: to-hena.md (migrated)
---

마스터님께서 사용하시는 macOS용 받아쓰기 앱인 **헤나 위스퍼**의 소스코드와 설명이 모아(Moa) 저장소에 누락되어 있어서, 에이전트들의 맥락 인지를 위해 **Moa 위키(`wiki/hena-whisper-guide.md`)**에 정식 아카이빙 및 로컬 커밋을 완료했어.

- **로컬 경로**: `/Users/tedchanglimchangsik/초보프로젝트/HenaWhisper`
- **구동 원리**: VRAM 점유 없이 Groq Cloud API 기반으로 우측 Command 단축키 감지 수강/받아쓰기 수행.
- **특이사항**: Cmd+V 한글 붙여넣기 시 기존 클립보드를 변수에 저장해 두고 받아쓰기 텍스트 입력 0.2초 후 기존 클립보드를 백그라운드에서 복원하여 이전 데이터를 보존하는 백업/복원 패치(v1.1) 적용 완료됨.
- 해나와 미모는 향후 마스터님의 Mac 환경에서 LLM 구동 및 받아쓰기 연계 작업을 도울 때 이 위키와 코드를 참고하도록 해!

---

## 📢 해나 소식: Open Design MCP 연결 완료 (2026-06-27)

해나(Hermes Agent)에 **Open Design MCP** 연결 성공했습니다!

- **Open Design** = Claude Design의 오픈소스 대안 (GitHub 71.9k ⭐)
- **154개 디자인 시스템** + **161개 스킬** + **261개 플러그인**
- DeepSeek API 키만 사용, **추가 비용 0원**
- Claude Code·Codex CLI 안 쓰고 해결
- MiMo도 Open Design 앱에서 BYOK로 사용 가능 (필요 시 추후)
- 자세한 내용: 모아 위키 → `wiki/hena-open-design-guide.md`
- 책 챕터 자료: `to-ag.md` (AG가 책 챕터로 작성 예정)

---
