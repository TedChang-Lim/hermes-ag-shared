# 🎉 로컬 AI 성공 기록

> **작성일:** 2026년 5월 18일  
> **장소:** 맥북 (macOS)  
> **주인:** 창식 임  
> **사건:** Hermes Agent STT(음성인식) 설정 성공!

---

## 📋 문제 상황

| 항목 | 내용 |
|------|------|
| **증상** | Telegram에서 음성 메시지 보내면 "STT provider not configured" 메시지만 나옴 |
| **원인** | Hermes Agent에 음성 → 텍스트 변환(STT) 기능이 활성화되지 않음 |
| **영향** | 음성 메시지를 들을 수 없어서 대화의 50% 이상 놓침 |

---

## 🔧 해결 과정

### 1단계: 원인 파악
- Hermes Agent의 `hermes-agent` 스킬 로드 → STT 설정 문서 확인
- STT 제공자 4가지 확인: 로컬 faster-whisper, Groq, OpenAI, Mistral
- **로컬 faster-whisper**가 가장 간단함 (API 키 불필요, 무료)

### 2단계: 의존성 설치
```bash
pip install faster-whisper
```
- Whisper 기반 음성인식 모델 로컬에서 실행
- 인터넷 연결 없이도 작동 → 프라이버시 안전

### 3단계: 설정 적용
```bash
hermes config set stt.enabled true
hermes config set stt.provider local
hermes config set stt.local.model base
hermes gateway restart
```
- `stt.enabled: true` → STT 기능 켜기
- `stt.provider: local` → 로컬 모델 사용
- `stt.local.model: base` → base 모델 (속도/정확도 균형)
- `hermes gateway restart` → 설정 반영을 위해 게이트웨이 재시작

### 4단계: 검증
- 음성 메시지 재전송 → STT가 자동으로 텍스트 변환
- ✅ 성공! 이제 음성 메시지를 들을 수 있음

---

## 🏆 결과

| 항목 | Before | After |
|------|--------|-------|
| **음성 인식** | ❌ 안 됨 | ✅ 로컬에서 자동 변환 |
| **API 키 필요** | — | ❌ 불필요 (로컬 모델) |
| **인터넷 의존** | — | ❌ 오프라인 작동 가능 |
| **프라이버시** | — | ✅ 음성 데이터 외부 전송 없음 |

---

## 💡 배운 교훈

1. **Hermes Agent는 설정이 기본 꺼짐** — 기능이 있어도 `enabled: true`로 켜야 작동
2. **로컬 모델이 가장 간단함** — API 키 관리 없이 바로 사용 가능
3. **설정 변경 후 재시작 필수** — `/restart` 또는 `hermes gateway restart`
4. **스킬이 답이다** — `hermes-agent` 스킬에서 정확한 설정법 확인 가능

---

## 🚀 다음 도전

- [ ] TTS(음성합성) 설정 → Hermes가 음성으로 답변하기
- [ ] 더 큰 모델(`medium`, `large-v3`)로 정확도 향상
- [ ] 다른 STT 제공자(Groq 등) 비교 테스트

---

> *"작은 설정 하나가 대화의 세계를 바꾼다."*  
> — 2026년 5월 18일, 창식 임 & Hermes Agent
