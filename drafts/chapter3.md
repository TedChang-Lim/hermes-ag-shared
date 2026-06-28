# Chapter 3: Hermes Agent 설정 — 24시간 작동하는 AI 에이전트 시스템 구축

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 3.1 24시간 백그라운드 워커, Hermes Agent

Hermes Agent는 단순한 대화형 챗봇을 넘어 파일 제어, 코드 실행, Git 동기화, 크론잡(Cron) 기반의 주기적인 자동화 작업을 원스톱으로 처리하는 백그라운드 에이전트 엔진입니다. 

이 시스템은 개발자가 자리를 비운 새벽이나 이동 중인 시간에도 끊김 없는 백그라운드 작업을 실행하는 중추적인 비서 역할을 수행합니다.

---

## 3.2 설치 및 준비 과정

### 요구 시스템 환경
- OS: macOS, Linux 또는 Windows WSL2 환경
- 런타임: Python 3.10 이상, Node.js 18 이상 및 Git 빌드 환경

### CLI 설치
* **macOS / Linux / WSL2:**
  ```bash
  # 1. Hermes Agent CLI 설치 스크립트 실행
  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
  
  # 2. 터미널 셸 재로드
  source ~/.zshrc
  
  # 3. 설치 정상 작동 여부 확인
  hermes version
  ```

* **Windows (Native PowerShell):**
  ```powershell
  iex (irm https://hermes-agent.nousresearch.com/install.ps1)
  ```

설치가 정상적으로 끝나면 사용자 홈 디렉토리 아래 `~/.hermes/` 경로가 생성되고, 여기에 데이터베이스 및 기본 구성 파일들이 자리 잡게 됩니다.

---

## 3.3 '가장 저렴한 뇌' 연결하기: API 및 모델 구성

가장 비용 효율적인 삼총사 조합을 바탕으로 설정을 진행합니다. 

### API 키 환경변수 주입
```bash
# DeepSeek API 키 설정
export DEEPSEEK_API_KEY="sk-xxxxx"

# Gemini API 키 설정
export GEMINI_API_KEY="AIzaSyxxxxx"

# MiMo API 키 설정
export MIMO_API_KEY="mm-xxxxx"
```

### config.yaml 설정
`~/.hermes/config.yaml` 파일을 편집하여 아래와 같이 에이전트 가성비 모델을 등록합니다.

```yaml
# ~/.hermes/config.yaml
providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
  - name: gemini
    api_key: ${GEMINI_API_KEY}
    base_url: https://generativelanguage.googleapis.com/v1beta
  - name: mimo
    api_key: ${MIMO_API_KEY}
    base_url: https://api.mimo.ai/v1

models:
  - name: deepseek-v4-flash
    provider: deepseek
    model: deepseek-chat
    max_tokens: 8192
    
  - name: gemini-flash-low
    provider: gemini
    model: gemini-2.5-flash
    max_tokens: 8192

  - name: mimo-base
    provider: mimo
    model: mimo-2.5-base
    max_tokens: 8192
```

### 아키텍처에 따른 역할 세분화

| 모델 이름 | 역할군 | 특징 | 단가 (1M 입/출) |
|------|------|------|------|
| **deepseek-v4-flash** | 기본 연산, 텍스트 처리 | 저렴한 대량 토큰 소화 | $0.14 / $0.28 |
| **gemini-flash-low** | 구조화, 파일 관리 | 넓은 컨텍스트, 빠른 구조 검증 | $0.075 / $0.30 |
| **mimo-base** | UI 가이드 분석 및 디자인 | 뛰어난 템플릿 코드 구현 | $0.14 / $0.28 |

---

## 3.4 0% 대기 램(RAM)을 위한 Insane Search CLI 크롤러 장착

에이전트가 외부 인터넷 정보를 실시간으로 긁어오거나 네이버, 쿠팡 등 방화벽이 삼엄한 사이트를 수집할 때 일반적인 요청 방식은 차단당하기 십상입니다.

이를 돌파하기 위해 에이전트 내부에 **Insane Search CLI** 도구를 주입합니다. 로컬 데몬이나 무거운 백엔드 API 서버를 24시간 켜두지 않고, 크롤링이 필요할 때만 단발성으로 명령어를 호출해 1초 만에 실행한 뒤 메모리에서 소멸시키는 **On-Demand** 구조입니다.

### Insane Search CLI 설치 및 에이전트 연결
```bash
# 1. 로컬 환경에 Insane Search 설치
pip install insane-search curl_cffi playwright
playwright install chromium

# 2. 실행 가능한 CLI 바이너리 심볼릭 링크 등록
mkdir -p ~/.local/bin
ln -s $(which insane-extract) ~/.local/bin/insane-extract
chmod +x ~/.local/bin/insane-extract
```

이제 Hermes Agent는 검색 및 뉴스 수집 요청을 받으면 백그라운드 API 서버를 올리는 메모리 낭비 없이, 아래와 같이 CLI를 한 줄 직접 구동하여 WAF(웹 방화벽) 보안막을 뚫고 텍스트를 정교하게 낚아챕니다.

```bash
# 에이전트가 필요할 때 호출하는 로컬 전용 커맨드
~/.local/bin/insane-extract "https://news.ycombinator.com"
```

이 조합으로 유료 크롤링 프록시 서비스 구독 없이 **완전한 $0 크롤링 체계**를 완성합니다.

---

## 3.5 텔레그램 연동 및 자동화 스케줄 구성

### 텔레그램 메신저 연결
외부에서도 스마트폰을 이용해 에이전트에 제어 명령을 내릴 수 있도록 텔레그램 봇을 연동합니다.

```yaml
# config.yaml 추가 사항
telegram:
  enabled: true
  bot_token: ${TELEGRAM_BOT_TOKEN}  # @BotFather에서 발급받은 키
  chat_id: ${TELEGRAM_CHAT_ID}      # 본인의 고유 텔레그램 계정 ID
```

### 크론(Cron) 스케줄 관리
에이전트가 지정된 시간에 맞추어 스스로 동작을 개시하도록 자동화 태스크를 정의합니다.

```yaml
# ~/.hermes/cron.yaml
jobs:
  - name: morning-briefing
    schedule: "0 7 * * *"  # 매일 아침 7시
    command: "오늘 업계 주요 소식을 Insane Search CLI로 크롤링해서 핵심을 텔레그램으로 요약 전송해줘"
    model: deepseek-v4-flash
    
  - name: backup-repository
    schedule: "0 23 * * *"  # 매일 밤 11시
    command: "오늘 변경된 작업 코드들을 모두 정리해 깃허브 원격 저장소에 동기화해줘"
    model: gemini-flash-low
```

이 간결한 파일 몇 개로 맥북의 RAM 점유율을 극소화하면서, 언제나 켜져 있는 나만의 자동화 시스템이 갖춰집니다.

**Chapter 4에서는 두 개 이상의 가성비 에이전트가 Git 저장소를 중간 매개로 삼아 팀워크를 구현하는 방식을 구체적으로 분석해 보겠습니다.**
