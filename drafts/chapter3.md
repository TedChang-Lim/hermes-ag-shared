# 📦 Chapter 3: Hermes Agent 세팅 — 24시간 AI 비서 구축하기

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 3.1 Hermes Agent란?

Hermes Agent는 Nous Research가 개발한 오픈소스 AI 에이전트 프레임워크입니다. 단순한 챗봇이 아니라, **파일을 읽고 쓰고, 코드를 실행하고, Git에 푸시하고, Telegram 메시지를 보내고, 크론잡으로 자동 작업**까지 수행하는 진정한 AI 비서입니다.

이 가이드의 저자는 Hermes Agent를 **"헤나(Haena)"** 라는 이름으로 부르며 24시간 운영 중입니다.

---

## 3.2 설치

### 사전 요구사항
- macOS/Linux (Windows는 WSL 필요)
- Node.js 18+ 및 Python 3.10+
- Git

### 설치 명령어

```bash
# 1. Hermes Agent CLI 설치
npm install -g @nousresearch/hermes-agent

# 2. 초기 설정
hermes init

# 3. 기본 config 확인
hermes config show
```

설치 완료 후 `~/.hermes/` 디렉토리에 설정 파일이 생성됩니다.

---

## 3.3 Provider 설정 — DeepSeek 연결하기

Hermes Agent는 다양한 AI 모델(Provider)을 지원합니다. 가장 중요한 설정은 **어떤 모델을 사용할지** 선택하는 것입니다.

### DeepSeek API 키 발급

```bash
# 1. https://platform.deepseek.com/ 에 가입
# 2. API 키 생성 후 복사
# 3. 환경 변수로 설정
export DEEPSEEK_API_KEY="sk-xxxxx"
```

### config.yaml 설정

```yaml
# ~/.hermes/config.yaml
providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
    
models:
  - name: deepseek-v4-flash
    provider: deepseek
    model: deepseek-chat  # Flash 모델
    max_tokens: 8192
    
  - name: deepseek-v4-pro
    provider: deepseek
    model: deepseek-reasoner  # Pro 모델
    max_tokens: 8192
```

### 일상 작업 vs 복잡 추론 분리

| 구분 | 모델 | 용도 | 비용 |
|------|------|------|------|
| **기본 모델** | deepseek-v4-flash | 일상 대화, 코드 작성, 크론잡 | $0.14/$0.28 (입/출) |
| **추론 모델** | deepseek-v4-pro | 복잡한 문제 해결, 기획, 아키텍처 설계 | $0.435/$0.87 (입/출) |

```bash
# 기본 모델로 실행
hermes run "이 코드 리뷰해줘"

# Pro 모델로 실행 (--model 플래그)
hermes run --model deepseek-v4-pro "이 아키텍처 설계 검토해줘"
```

---

## 3.4 핵심 기능 설정

### Telegram 연동

에이전트와 Telegram으로 대화하려면:

```yaml
# config.yaml
telegram:
  enabled: true
  bot_token: ${TELEGRAM_BOT_TOKEN}  # @BotFather에서 발급
  chat_id: ${TELEGRAM_CHAT_ID}      # 봇과 대화 후 확인
```

이렇게 하면 스마트폰으로 Hermes와 대화할 수 있습니다. 집 밖에서도 AI 비서에게 명령을 내릴 수 있습니다.

### 크론잡 (자동 작업)

정해진 시간에 자동으로 작업을 실행합니다:

```yaml
# ~/.hermes/cron.yaml
jobs:
  - name: morning-report
    schedule: "0 7 * * *"  # 매일 오전 7시
    command: "오늘 할 일 리포트 작성해서 텔레그램으로 보내줘"
    model: deepseek-v4-flash
    
  - name: daily-summary
    schedule: "0 22 * * *"  # 매일 오후 10시
    command: "오늘 작업 내용 요약하고 GitHub에 푸시해줘"
    model: deepseek-v4-flash
```

### 멀티 에이전트 협업 (GitHub 공유)

GitHub 저장소를 통해 여러 에이전트가 협업할 수 있습니다:

```yaml
# config.yaml
git:
  auto_commit: true
  auto_push: true
  shared_repo: https://github.com/TedChang-Lim/hermes-ag-shared.git
```

워크플로우:
1. 헤나가 `to-ag.md`에 메시지 작성 → Git push
2. AG가 `to-ag.md` 읽고 작업
3. AG가 `to-hena.md`에 결과 작성 → Git push
4. 헤나가 읽고 이어서 작업

---

## 3.5 초보자가 하기 쉬운 실수와 해결법

| 문제 | 원인 | 해결 |
|------|------|------|
| "Provider not configured" | API 키 미설정 | `.env` 파일에 API 키 추가 |
| "STT not configured" | 음성 기능 꺼짐 | `hermes config set stt.enabled true` |
| 응답이 너무 느림 | Pro 모델만 사용 | Flash 모델을 기본으로 설정 |
| 토큰 부족 오류 | max_tokens 설정 부족 | `max_tokens: 16384`로 증가 |
| Git push 실패 | 인증 정보 없음 | `git config --global`으로 사용자 설정 |

---

## 3.6 마스터님의 실제 설정 예시

이 가이드의 저자는 다음과 같이 설정하여 사용 중입니다:

```yaml
# 실제 사용 중인 config.yaml (요약)
default_model: deepseek-v4-flash
providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
  - name: mimo
    api_key: ${MIMO_API_KEY}
  - name: gemini
    api_key: ${GEMINI_API_KEY}
    
telegram:
  enabled: true
  
git:
  auto_push: true
  shared_repo: TedChang-Lim/hermes-ag-shared
```

**월간 사용 비용:** 약 $4.5 (DeepSeek Flash $2.5 + Pro $1.5 + Mimo $0.5)

**4장에서는 Git 기반 에이전트 간 협업 워크플로우를 자세히 알아보겠습니다.**
