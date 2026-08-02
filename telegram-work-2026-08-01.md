---
type: note
created: 2026-08-01
updated: 2026-08-01
sources: [텔레그램 세션 2026-08-01, fish-audio-tts 스킬, api-keys.md]
aliases: [어제 텔레그램 작업, TTS 연결, 음성 만들기, Fish Audio]
---

# 2026-08-01 텔레그램 작업 종합 (해나)

> 마스터님이 8/1 텔레그램에서 진행한 작업 일체를 모아위키에 정리한 문서.
> 모든 에이전트(AG·미모·지호·큐리·코코)가 참고할 것.

## 1. 🎙️ AI 음성(TTS) 연결 완료 — Fish Audio

**상태: ✅ 가입·연결·실생성 검증까지 완료** (QN3 TTS보다 음질 우수 — 마스터님 평가)

| 항목 | 내용 |
|:--|:--|
| 서비스 | Fish Audio (fish.audio) |
| 가입 | 2026-08-01, nanal737@gmail.com (Google OAuth — 헤드리스 가입 불가, reCAPTCHA) |
| API 키 | `FISH_AUDIO_API_KEY` → `~/.hermes/.env` + `api-keys.md` §3 |
| 무료 모델 | `s2.1-pro-free` — 유료 s2.1-pro($15/M)와 **같은 모델을 $0**으로 제공 |
| 무료 기간 | 2026-08-31까지 (2회 연장 추세: 7/24→7/31→8/31) |
| 음질 | QN3 TTS·MiMo TTS보다 우수 (마스터님 직접 평가) |

### ⚠️ 핵심 함정: model은 HEADER에 (body 아님!)
```bash
curl -X POST "https://api.fish.audio/v1/tts" \
  -H "Authorization: Bearer $FISH_AUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "model: s2.1-pro-free" \
  -d '{"text":"안녕하세요","format":"wav"}'
```
- body에 model 넣으면 **402 Insufficient credit** (유료 모델로 청구 시도됨)
- 감정 태그 `[happy]` `[soft tone]` `[break]` 등 64+ 지원, **토큰 비용 0**
- 실전 검증: ~60자 2초, 감정 태그 8초 문장 6초 → wav 생성 (HTTP 200)

## 2. 🎤 Deepgram $200 크레딧 활성 (7/31 가입)

- Nova-3 실시간 STT, Aura-2 TTS, Voice Agent API
- 콘솔: console.deepgram.com (이메일/구글 로그인)

## 3. 📺 영상 분석 건들 (8/1)

| 영상/주제 | 판정 |
|:--|:--|
| 초당 1800토큰 로컬 실시간 음성AI | 분석 완료 (로컬 TTS/STT 파이프라인 참고용) |
| LM Studio Bionic 2026 리뷰 | 로컬 작업 가능 무료 AI 에이전트 — 참고 |
| FreeCoder (Windows 전용 무료 코딩 에이전트) | ❌ Mac 불가 + DeepSeek 중복 → 불필요 |
| Kimi K3 무료 이용법 (HuggingChat) | ⚠️ 웹 무료 ≠ API 무료 (API는 유료) → 참고만 |
| OpenCode Zen 무료 DeepSeek V4 Flash | ✅ **fallback 후보** — 무료, 카드 불필요, SWE-bench 79% |
| Fal.ai (Higgsfield 대안) | ⭐ 검토 가치 — 종량제 (이미지 $0.04, Kling $0.07/초) |
| 서울대 신종욱 교수 AI 강의 인사이트 | ⭐ 강의 콘텐츠 반영 예정 |

### 영상 분석 검색 핵심 교훈 (재사용)
- 마스터님 피드의 한글 제목 = **영어 원제 자동번역** → 영어로 검색 (yt-dlp `ytsearch:` 사용)
- "웹 무료 ≠ API 무료" 구분 필수
- 업로드 시각 검증: 영상 HTML `uploadDate` grep + KST 환산

## 4. 📌 다음 행동 (대기 중)

- **Fal.ai 가입** — 마스터님 하실 때 API 키로 자동화 연결 안내 (공모전 2편 제작 시 Higgsfield 구독 대비 경제적)
- **OpenCode Zen fallback 추가** — config.yaml 수정 승인 대기 ($24 크레딧 절약)
- **서울대 인사이트 강의 반영** — "AI는 평균의 결과, 나만의 관점이 차별화" 1강 커리큘럼에 녹이기

## 관련
- [[api-keys]] — §3 음성/TTS 키
- 스킬: `fish-audio-tts` (Hermes skills/media) — 상세 사용법
- 스킬: `content-analysis-approach` — 영상 분석 사례 (FreeCoder/Kimi K3)
- [[agent-media-pipeline-2026-07-31]] — 큐리+해나 검증 미디어 능력 (demucs 음성분리 포함)
