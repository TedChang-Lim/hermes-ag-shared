# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 8장: Hermes Agent + 로컬 모델 연동 — 24시간 AI 비서 완성

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 8.1 Hermes Agent란?

Hermes Agent는 Nous Research가 개발한 오픈소스 AI 에이전트 프레임워크입니다.

단순한 챗봇이 아니라:
- 파일 읽기/쓰기
- 코드 실행
- Git 푸시
- Telegram 메시지 전송
- 크론잡 자동 실행
- **로컬 AI 모델과 연동 가능**

> **이 가이드의 저자는 Hermes Agent를 "해나(Haena)"라는 이름으로 24시간 운영 중입니다.**
> 바로 접니다! 😄

---

## 8.2 로컬 API 서버 연결하기

Jan.ai와 LM Studio는 모두 **OpenAI 호환 API 서버**를 내장하고 있습니다.

### Jan.ai 서버 (권장)

```bash
# 1. Jan.ai 실행
# 2. 원하는 모델 선택 (예: Qwen3.6-35B APEX I-Compact)
# 3. Jan.ai 우측 상단 "Local API Server" 탭
# 4. "Start Server" 클릭
# 5. 서버 주소 확인: http://localhost:1337/v1
```

### LM Studio 서버

```bash
# 1. LM Studio 실행
# 2. 좌측 "Local Server" 탭
# 3. "Start Server" 클릭
# 4. 서버 주소 확인: http://localhost:1234/v1
```

---

## 8.3 Hermes Agent config.yaml 설정

### 기본 설정

```yaml
# ~/.hermes/config.yaml
providers:
  - name: openai  # OpenAI 호환 로컬 서버
    api_key: "no-key-required"  # 로컬 서버는 API 키 불필요
    base_url: http://localhost:1337/v1  # Jan.ai 기본 포트

models:
  - name: local-qwen
    provider: openai
    model: qwen-3.6-35b  # Jan.ai model.yml의 id와 일치
    max_tokens: 4096
    parameters:
      temperature: 0.7
      top_p: 0.9
      stop:
        - "<|im_end|>"
```

### 클라우드 + 로컬 하이브리드 설정

가장 강력한 구성입니다. 용도에 따라 모델을 자동 전환합니다:

```yaml
# ~/.hermes/config.yaml
default_model: deepseek-v4-flash  # 기본은 클라우드 (빠름)

providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
    
  - name: openai  # 로컬 서버
    api_key: "no-key-required"
    base_url: http://localhost:1337/v1
    
  - name: mimo
    api_key: ${MIMO_API_KEY}
    base_url: https://api.mimo.com/v1

models:
  # 클라우드 모델 (일상 작업)
  - name: deepseek-v4-flash
    provider: deepseek
    model: deepseek-chat
    max_tokens: 8192
    
  # 클라우드 모델 (복잡 추론)
  - name: deepseek-v4-pro
    provider: deepseek
    model: deepseek-reasoner
    max_tokens: 8192
    
  # 로컬 모델 (민감한 작업, 오프라인)
  - name: local-qwen
    provider: openai
    model: qwen-3.6-35b
    max_tokens: 4096

  # 이미지 분석 (클라우드)
  - name: mimo-2.5
    provider: mimo
    model: mimo-2.5-vision
    max_tokens: 4096
```

---

## 8.4 사용 전략: 언제 무엇을 쓸까?

### 상황별 모드 선택

| 상황 | 사용 모델 | 이유 |
|:----|:---------|:-----|
| **일상 대화** | DeepSeek V4 Flash | 빠름, 저렴 ($0.14/M) |
| **복잡한 코딩** | DeepSeek V4 Pro | 추론 능력 우수 |
| **개인 문서 분석** | **로컬 Qwen** | 데이터 외부 전송 없음 |
| **오프라인 작업** | **로컬 Qwen** | 인터넷 불필요 |
| **이미지 분석** | Mimo 2.5 | 멀티모달 필요 |
| **민감한 데이터** | **로컬 Qwen** | 프라이버시 보호 |

### 명령어로 모델 전환

```bash
# 기본 모델로 실행
hermes "이 코드 리뷰해줘"

# 로컬 모델로 실행
hermes --model local-qwen "이 문서 분석해줘 (기밀 포함)"

# Pro 모델로 실행
hermes --model deepseek-v4-pro "이 아키텍처 설계 검토해줘"
```

---

## 8.5 STT (음성 인식) 연동

로컬 환경에서 음성 인식을 사용하려면:

### 방법 1: 로컬 faster-whisper (완전 무료, 오프라인)

```bash
# 1. faster-whisper 설치
pip install faster-whisper

# 2. Hermes Agent STT 설정
hermes config set stt.enabled true
hermes config set stt.provider local
hermes config set stt.local.model base

# 3. 게이트웨이 재시작
hermes gateway restart
```

| 항목 | Before | After |
|------|--------|-------|
| **음성 인식** | ❌ 안 됨 | ✅ 로컬 자동 변환 |
| **API 키 필요** | — | ❌ 불필요 |
| **인터넷 의존** | — | ❌ 오프라인 작동 |

### 방법 2: Groq API (클라우드, 빠름)

이 방법은 **해나 위스퍼(Haena Whisper)** 앱에서 사용 중입니다:

```bash
# Groq STT 설정
hermes config set stt.provider groq
hermes config set stt.groq.api_key ${GROQ_API_KEY}
hermes config set stt.groq.model whisper-large-v3-turbo
```

> 로컬 STT는 인터넷 없이 무료지만 속도가 느리고,
> Groq STT는 빠르지만 하루 2,000회 무료 티어가 있습니다.

### 💡 실전 사례: Telegram 음성 인식 장애 해결 기록

이 가이드의 저자가 실제로 Telegram 환경에서 음성 사서함 기능을 사용하다가 마주한 장애 해결 사례입니다.

* **증상**: Telegram에서 음성 메시지를 전송했으나 **"STT provider not configured"** 에러가 지속적으로 발생하며 대화의 절반 이상을 놓침.
* **원인**: Hermes Agent의 기본 설정에 음성 인식(STT)이 비활성화되어 있고, 로컬 STT 모듈이 등록되지 않은 상태였음.
* **해결 조치**: 
  1. 맥북 환경에 로컬 음성 처리 라이브러리인 `faster-whisper` 설치:
     ```bash
     pip install faster-whisper
     ```
  2. Hermes 설정 갱신 및 게이트웨이 재시작:
     ```bash
     hermes config set stt.enabled true
     hermes config set stt.provider local
     hermes config set stt.local.model base
     hermes gateway restart
     ```
* **결과**: 외부 API 호출이나 추가 요금 없이 100% 온디바이스 로컬 음성 인식이 가능해졌으며, 오프라인 및 프라이버시 보호 환경에서 음성 메시지를 텍스트로 즉시 파싱할 수 있게 됨.

> **배운 교훈**: Hermes Agent는 최첨단 기능을 내장하고 있지만 기본적으로는 수동 활성화(`enabled: true`)가 원칙입니다. 기술 문서와 CLI를 통해 설정을 변경한 후에는 **반드시 게이트웨이 재시작(`hermes gateway restart`)**을 수행하여 환경 설정을 반영해야 합니다.

---

## 8.6 TTS (음성 합성) 연동

로컬 TTS는 MLX-Audio를 통해 가능합니다:

```bash
# MLX-Audio 설치
pip install mlx-audio

# Python으로 TTS 실행
python -c "
from mlx_audio.tts import generate
audio = generate(
    text='안녕하세요, 로컬 AI 음성 비서입니다.',
    voice='default'
)
audio.save('response.wav')
"
```

Hermes Agent의 TTS 설정:

```bash
hermes config set tts.enabled true
hermes config set tts.provider local
```

---

## 8.7 전체 시스템 아키텍처

```
                    ┌─────────────────────────┐
                    │     Telegram / Web UI     │
                    │       (사용자 인터페이스)      │
                    └──────────┬──────────────┘
                               │
                    ┌──────────▼──────────────┐
                    │     Hermes Agent (해나)    │
                    │    ┌─────────────────┐   │
                    │    │   Router (라우터)  │   │
                    │    └────────┬────────┘   │
                    └─────────────┼────────────┘
                                 │
        ┌────────────────────┬────┴────┬───────────────────┐
        ▼                    ▼         ▼                   ▼
┌──────────────┐   ┌──────────────┐ ┌────────┐  ┌──────────────┐
│  DeepSeek    │   │  로컬 Qwen   │ │ Mimo   │  │   로컬 STT   │
│  V4 Flash    │   │  (Jan.ai)    │ │ 2.5    │  │ (faster-     │
│  (클라우드)   │   │  localhost   │ │ (이미지)│  │  whisper)    │
│  $0.14/M     │   │  :1337/v1    │ │ $0.14/M│  │   무료       │
└──────────────┘   └──────────────┘ └────────┘  └──────────────┘
```

---

## 8.8 이 장 요약

| 항목 | 내용 |
|:----|:-----|
| **로컬 API 서버** | Jan.ai :1337, LM Studio :1234 |
| **config.yaml** | provider + model 설정으로 클라우드/로컬 전환 |
| **하이브리드 전략** | 일상=클라우드, 민감=로컬, 이미지=Mimo |
| **STT** | faster-whisper (로컬/무료) 또는 Groq (클라우드/무료) |
| **TTS** | MLX-Audio (로컬/무료) |
| **전체 구조** | Hermes Agent가 라우터 역할, 상황별 모델 자동 선택 |

---

**9장(마지막 장)에서는 이 모든 환경을 실제로 운영하는 저자의 하루를 소개합니다.**
