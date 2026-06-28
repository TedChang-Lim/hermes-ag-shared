# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 3장: Jan.ai로 업그레이드 — 본격적인 모델 관리와 파일 통제

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 3.1 왜 Jan.ai로 이전하는가?

LM Studio가 샌드박스의 문을 여는 열쇠라면, 오픈소스 기반의 Jan.ai는 내부 아키텍처를 자유롭게 주무를 수 있는 제어 시스템입니다. 로컬 AI를 일회성 장난감이 아닌 비즈니스 생산성의 축으로 삼으려면, 리소스를 투명하게 격리하고 관리할 수 있어야 합니다.

| 제어 항목 | LM Studio | Jan.ai |
|:---------|:---------|:-------|
| **모델 저장소 구조** | 앱 전용 경로 강제, 커스터마이징 차단 | **원하는 로컬 경로 지정 및 수동 폴더 관리** |
| **세부 환경 매니페스트** | GUI 슬라이더 기반의 불투명한 설정 | **`model.yml` 코드를 통한 세밀한 선언** |
| **컨텍스트 길이 제어** | 변경 시 추론 병목 감지 모호 | **`ctx_len` 값의 하드웨어 맞춤 튜닝** |
| **수동 임포트 호환성** | 로컬 모델 복제 및 인식 오류 빈번 | **GGUF 파일과 yml 선언만 일치하면 100% 인식** |
| **확장성** | GUI 런타임에 종속 | **오픈소스 엔진 기반, 향후 고성능 서빙 프레임워크 확장 용이** |

디렉토리 구조와 YAML 파일을 직접 제어함으로써, 우리는 민감한 업무 기밀이나 개인 IP를 다룰 모델이 외부 트래픽을 단 한 바이트도 발생시키지 않는다는 사실을 파일 시스템 수준에서 물리적으로 추적하고 검증할 수 있습니다.

---

## 3.2 Jan.ai 클라이언트 전개

### 설치 단계
1. **공식 릴리즈 다운로드**: [https://jan.ai](https://jan.ai)에서 Apple Silicon 빌드를 확인하고 내려받습니다.
2. **패키지 설치**: 다운로드된 dmg 아카이브를 열어 앱 목록으로 이관합니다.
3. **런타임 디렉토리 생성**: 최초 실행 시 시스템 내부에 가상 가속 엔진이 빌드되며 기본 작업 디렉토리가 생성됩니다.

---

## 3.3 로컬 모델 디렉토리 토폴로지

Jan.ai의 핵심 가치는 명확한 디렉토리 구조에 있습니다. 맥OS 환경의 경우 아래의 시스템 경로 아래 모든 모델이 엄격히 격리되어 배치됩니다.

```bash
~/Library/Application Support/Jan/data/llamacpp/models/
├── Qwen-3.5-3B/                    # 사용자가 수동 생성하는 개별 모델 컨테이너
│   ├── qwen-3.5-3b-q8_0.gguf      # 다운로드한 이진(Binary) 가중치 파일
│   └── model.yml                   # 가중치를 해석할 환경 매니페스트 파일
│
└── Qwen3.6-35B-A3B-I-Compact/
    ├── qwen3.6-35b-i-compact.gguf
    └── model.yml
```

**디렉토리 구성 규칙:**
- 모델마다 독립된 하위 디렉토리를 구축합니다.
- 디렉토리 내부는 단 하나의 이진 파일(`.gguf`)과 환경 설정 매니페스트(`model.yml`)로 최소 구성됩니다.

---

## 3.4 `model.yml` 명세서 작성

`model.yml` 파일은 가속 엔진이 로컬 가중치를 물리 칩셋에 올리는 방식을 설명하는 Blueprint입니다. 불필요한 설정 오버헤드를 지우고 최상의 효율을 얻기 위한 권장 명세를 공유합니다.

### 템플릿 명세 (통합 칩셋 최적화 버전)

```yaml
# ~/Library/Application Support/Jan/data/llamacpp/models/<모델명>/model.yml
id: qwen-3.5-3b-local     # 호출에 사용될 고유 모델 식별자
name: Qwen 3.5 3B (Local) # 인터페이스에 출력될 별칭
engine: llamacpp          # 추론용 실행 런타임 엔진 지정

# 추론 제어 파라미터
ctx_len: 4096             # 컨텍스트 윈도우 크기 (메모리 제어의 핵심)
temperature: 0.7          # 출력 자유도
top_p: 0.9                # 샘플링 확률 임계치
max_tokens: 2048          # 1회 최대 출력 토큰 제약

# Apple Silicon 하드웨어 가속 설정
n_gpu_layers: -1          # -1 선언 시 모델의 모든 연산 레이어를 Metal GPU로 즉시 오프로드

# 프롬프트 구성 프로토콜 (ChatML 규격)
prompt_template: "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
stop:
  - "<|im_end|>"
  - "<|im_start|>"
```

### 세부 파라미터 제어

- **`ctx_len` (컨텍스트 길이)**: 모델이 한 번에 기억하는 히스토리 범위입니다. 이를 무작정 늘리면 추론 시점의 메모리 할당량이 기하급수적으로 증가해 속도가 느려집니다. 작업 범위에 맞게 조율해야 합니다.
- **`n_gpu_layers`**: Apple Silicon 맥북은 CPU와 GPU가 RAM을 공유하므로 무조건 `-1`로 설정하여 전체 모델을 GPU에 올리는 것이 빠릅니다.

---

## 3.5 모델 마이그레이션 및 CLI 다운로드

기존 LM Studio로 받아둔 가중치 파일을 Jan.ai 저장소로 복사하거나, Hugging Face CLI를 이용해 필요한 버전을 정확히 획득하는 실전 프로토콜입니다.

### 방법 1: 로컬 파일 시스템 직접 연동 (즉각 이관)
이미 다운로드한 파일이 존재한다면, 네트워크 대역폭을 낭비하지 않고 로컬 디렉토리 생성만으로 마이그레이션이 완료됩니다.

```bash
# 1. 대상 디렉토리 생성
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 2. 기존 LM Studio 모델 저장 경로에서 이관 처리
cp ~/Documents/LM\ Studio/models/qwen-3.5-3b-q8_0.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B/

# 3. 해당 폴더 내부에 위 3.4 절의 model.yml 파일 생성
```

### 방법 2: Hugging Face CLI를 활용한 다이렉트 반입 (권장)
터미널을 이용해 허깅페이스 서버로부터 손실 없이 고속으로 모델을 받는 가장 정밀한 프로세스입니다.

```bash
# 1. 허깅페이스 CLI 도구 설치 (Python pip 또는 홈브루 중 하나로 전개)
# Python 패키지 환경
pip install -U "huggingface_hub[cli]"

# Homebrew 환경
brew install hf

# 2. 타겟 모델용 로컬 디렉토리 선언
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 3. CLI 명령어로 타겟 모델의 특정 파일만 핀포인트 다운로드
huggingface-cli download \
  Qwen/Qwen-3.5-3B-GGUF \
  qwen-3.5-3b-q8_0.gguf \
  --local-dir ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B
```

---

## 3.6 가속 런타임 검증 및 예외 처리

모델 파일 전개와 `model.yml` 작성이 끝난 후, Jan.ai를 재기동하면 좌측 대화 대상 메뉴에 해당 모델이 활성화됩니다. "반갑습니다" 등의 기본 발화를 입력하여 정상 출론 속도(50+ tok/s)가 기록되는지 관찰합니다.

### 오작동 대처법

- **모델 리스트 미출력**: `model.yml` 코드의 인덴트(들여쓰기) 오류가 주로 원인입니다. YAML 파서 에러를 확인하고 오타를 수정합니다.
- **초당 토큰 속도 저하**: `n_gpu_layers`가 `-1`이 아닌 값으로 덮어써졌거나, 애플 실리콘 전용 빌드가 아닌 x86 CPU 에뮬레이션 버전으로 Jan.ai를 구동하고 있는지 확인합니다.
- **지연 시간 발생**: `ctx_len` 값이 과도하게 크지 않은지 검토하여 로컬 통합 RAM 가용 범위를 맞춥니다.

파일 제어 권한을 획득했다면 이제 하드웨어 최적화의 극단으로 나아갈 준비가 되었습니다. 다음 4장에서는 GGUF의 상위 가속 대안으로, 애플이 직접 튜닝한 MLX 프레임워크 기반의 네이티브 추론 기법을 분석합니다.
