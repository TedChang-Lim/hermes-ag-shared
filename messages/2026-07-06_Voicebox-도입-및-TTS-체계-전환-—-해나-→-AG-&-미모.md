---
created: 2026-07-06T22:53:59.215323
source: to-ag.md (migrated)
---

## 📌 상황 요약
마스터님이 **Voicebox** (voicebox.sh, 오픈소스 로컬 TTS 스튜디오)를 도입하셨다. 기존 Pinokio+Qwen3-TTS MLX(6.6GB)를 완전히 대체하여 정리 완료.

## ✅ 완료된 작업

### 1️⃣ Voicebox 설치 & 보이스 클로닝
- **Voicebox v0.5.0** 설치 (`/Applications/Voicebox.app`)
- **마스터님 목소리** 3초 샘플로 클로닝 성공 → "내 목소리" 프로필 생성
- **Chatterbox Multilingual** 엔진 다운로드 (3GB, 23개 언어, 감정 표현 가능)
- **서울리안(Seoulian, 테크 유튜버)** 목소리 클로닝 완료

### 2️⃣ Pinokio Qwen3-TTS MLX 정리 ❌
- `pinokio/api/Qwen3-TTS-MLX-WebUI-Enhanced.git/` **6.6GB 완전 삭제**
- MLX Qwen3 모델들(Qwen3-TTS 0.6B/1.7B) 제거
- Voicebox가 완전 대체 (PyTorch 기반, Qwen3+Chatterbox+TADA 등 7개 엔진)

### 3️⃣ TTS 엔진 비교
| 엔진 | 한국어 | 감정표현 | 생성속도 | 장문 |
|------|--------|---------|---------|-----|
| **Chatterbox Multilingual** | ✅ 최고 | ✅ instruct 파라미터 | ~150ms 실시간 | ❌ 단문용 |
| Qwen3-TTS 1.7B | ✅ 보통 | ❌ | 10~30초 | ❌ |
| **TADA 3B Multilingual** | ✅ (미설치) | ❌ | 느림 | ✅ **700초+** |
| Chatterbox Turbo | ❌ 영어만 | ✅ [laugh][sigh] | 빠름 | ❌ |

### 4️⃣ Hermes MCP 연결 ✅
- Voicebox MCP 서버 → Hermes 등록 완료 (4개 툴)
- REST API로 직접 음성 생성 가능
- 한국어 `language: "ko"` 명시 필수
- `instruct` 파라미터로 감정/톤 제어 가능

### 5️⃣ GitHub PR — Voicebox 한국어 번역
- **Ted Chang** 이름으로 GitHub에 PR 제출: #814 (jamiepine/voicebox)
- 559개 번역 키 전부 한국어로 번역 완료
- 머지되면 Voicebox에 한국어 메뉴 지원

## 🔜 진행 중 / 대기

### 음성 라이브러리 구축 (마스터님이 영상 찾는 중)
- 목표: 남성 10명 + 여성 10명 목소리 확보
- 방법: 유튜브 영상 → yt-dlp 오디오 추출(10초) → Whisper 정확한 대본 추출 → Chatterbox 클로닝
- **주의사항:** 
  - reference_text는 반드시 Whisper로 정확히 추출한 대본을 사용할 것 (틀리면 목소리가 망가짐)
  - 한 번에 1개만 생성할 것 (History 중복 주의)
- 서울리안(Seoulian) 테스트 완료. 마스터님이 DVD방 채널 등 추가 영상 찾는 중

## 💡 미모 참고사항
- MiMo Code로 영상 작업 시 TTS가 필요하면 **Voicebox Chatterbox** 사용 권장
- 한국어 문장 끝 "다" 발음: Chatterbox가 Qwen3보다 훨씬 자연스러움
- REST API: `POST http://127.0.0.1:17493/speak` — `{"profile":"이름","text":"...","language":"ko","engine":"chatterbox","instruct":"밝고 활기찬 톤"}`

---
