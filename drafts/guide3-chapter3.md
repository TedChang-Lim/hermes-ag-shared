# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 3장: Jan.ai로 업그레이드 — 본격적인 모델 관리

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 3.1 왜 LM Studio에서 Jan.ai로 옮겨야 할까?

LM Studio는 처음 시작하기에는 최고의 도구입니다. 설치만 하면 바로 쓸 수 있으니까요. 하지만 몇 주 사용하다 보면 이런 불편함이 생깁니다:

| 비교 항목 | LM Studio | Jan.ai |
|:---------|:---------|:-------|
| 모델 폴더 구조 | 자동 생성, 커스터마이징 어려움 | **직접 제어 가능** |
| 설정 파일 | UI에서만 설정 가능 | **model.yml로 세밀 튜닝** |
| 컨텍스트 길이 | 기본값 고정 | **ctx_size 자유 설정** |
| 모델 이전 | 다른 폴더로 복사 어려움 | **GGUF 파일만 있으면 OK** |
| 동시 실행 | 1개 모델만 | 여러 모델 전환 쉬움 |
| 커뮤니티 | 상대적으로 폐쇄적 | **오픈소스, 확장성 높음** |

> **이 가이드의 저자도 LM Studio로 시작해 지금은 Jan.ai를 메인으로 사용 중입니다.**
> LM Studio는 모델 다운로드 용도로만 남겨두고, 실제 운영은 Jan.ai로 하고 있습니다.

---

## 3.2 Jan.ai 설치

### 다운로드 및 설치

```bash
1. 공식 사이트 방문: https://jan.ai
2. macOS 버전 다운로드 (Apple Silicon)
3. Applications 폴더에 설치
4. 실행 후 모델 폴더 자동 생성 확인
```

### 첫 실행 시 확인사항

Jan.ai를 처음 실행하면 좌측 하단에 **"No model selected"** 메시지가 표시됩니다. 아직 모델을 설치하지 않았기 때문입니다. 정상입니다.

---

## 3.3 Jan.ai 모델 폴더 구조 이해하기

가장 중요한 부분입니다. Jan.ai의 모델 폴더 구조는 다음과 같습니다:

```bash
~/Library/Application Support/Jan/data/llamacpp/models/
├── Qwen-3.5-3B/                    # 모델 폴더 (직접 생성)
│   ├── qwen-3.5-3b-q8_0.gguf      # 실제 모델 파일 (1~30GB)
│   └── model.yml                   # 설정 파일 (직접 작성)
│
├── Gemma-4-4B/
│   ├── gemma-4-4b-q4_k_m.gguf
│   └── model.yml
│
└── Qwen3.6-35B-A3B-I-Compact/
    ├── qwen3.6-35b-i-compact.gguf
    └── model.yml
```

**규칙은 간단합니다:**
- 모델 하나당 폴더 하나
- 폴더 안에 `model.gguf` (또는 아무 이름 .gguf) + `model.yml`

---

## 3.4 model.yml 완벽 설정 가이드

`model.yml`이 Jan.ai의 핵심입니다. 이 파일 하나로 모델의 모든 설정이 결정됩니다.

### 기본 템플릿 (AG 제공)

```yaml
# ~/Library/Application Support/Jan/data/llamacpp/models/<모델명>/model.yml
id: qwen-3.5-3b          # 고유 식별자
name: Qwen 3.5 3B        # Jan.ai에 표시될 이름
engine: llamacpp          # 엔진 (고정)

# 주요 설정
ctx_len: 4096             # 컨텍스트 길이 (모델 기본값 기준)
temperature: 0.7          # 창의성 조절
top_p: 0.9                # 샘플링 방식
max_tokens: 2048          # 최대 응답 토큰 수

# Apple Silicon GPU 가속 (중요!)
n_gpu_layers: -1          # -1 = 모든 레이어를 GPU로 오프로드

# 프롬프트 템플릿 (ChatML 방식, Qwen/Gemma 권장)
prompt_template: "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
stop:
  - "<|im_end|>"
  - "<|im_start|>"
```

### 파라미터 상세 설명

| 파라미터 | 설명 | 추천값 |
|:---------|:-----|:------|
| `ctx_len` | 한 번에 기억할 수 있는 토큰 수 | Qwen 3.5: 4096, Qwen3.6: 32768, Gemma 4: 131072 |
| `n_gpu_layers` | GPU에 올릴 레이어 수 | **-1 (전체)** — M Mac은 항상 이 값 |
| `temperature` | 응답의 창의성 (낮을수록 보수적) | 0.5 ~ 0.9 |
| `max_tokens` | 한 번에 생성할 최대 토큰 | 2048 ~ 8192 |

### ctx_len 설정 팁

| 모델 | 기본 ctx_len | 최대 ctx_len | 비고 |
|:----|:-----------:|:-----------:|:-----|
| Qwen 3.5 3B | 32,768 | 32,768 | 그대로 사용 |
| Qwen 3.5 7B | 32,768 | 32,768 | 그대로 사용 |
| Qwen3.6-35B | 32,768 | 131,072 (YaRN) | 기본값 권장 |
| Gemma 4 4B | 131,072 | 262,144 | 너무 크면 느려짐 |

> ⚠️ ctx_len을 너무 크게 설정하면 속도가 크게 느려집니다.
> 기본값에서 시작해서 필요할 때만 늘리세요.

---

## 3.5 LM Studio → Jan.ai 모델 이전

LM Studio에서 이미 다운로드한 모델을 Jan.ai로 옮기는 방법입니다.

### 방법 1: 파일 직접 복사 (가장 간단)

```bash
# 1. LM Studio 모델 폴더 찾기
ls ~/.lmstudio/models/
# 또는
ls ~/Documents/LM\ Studio/models/

# 2. 원하는 GGUF 파일 확인
ls ~/.lmstudio/models/*.gguf

# 3. Jan.ai 모델 폴더에 복사
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/MyModel
cp ~/.lmstudio/models/모델파일.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/MyModel/

# 4. model.yml 작성 (위 템플릿 참고)
```

### 방법 2: HuggingFace CLI로 직접 다운로드 (권장)

```bash
# 1. HuggingFace CLI 설치
brew install huggingface-cli

# 2. 모델 폴더 생성
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 3. 모델 다운로드
huggingface-cli download \
  Qwen/Qwen-3.5-3B-GGUF \
  qwen-3.5-3b-q8_0.gguf \
  --local-dir ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 4. model.yml 작성
nano ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B/model.yml
```

> **다운로드 시간:** 17GB 모델 기준, 500Mbps 인터넷에서 약 5~6분 소요됩니다.

---

## 3.6 모델 적용 확인

모델 폴더에 파일을 추가한 후:

```bash
1. Jan.ai 앱 완전 종료 (메뉴바 아이콘도 Quit)
2. Jan.ai 재실행
3. 좌측 모델 목록에 새 모델이 나타나는지 확인
4. 모델 선택 후 채팅창에서 "안녕하세요" 입력
5. 우측 상단 속도 확인: 50+ tok/s 정상
```

### 속도가 느릴 때 확인사항

| 문제 | 원인 | 해결 방법 |
|:----|:-----|:---------|
| 30 tok/s 미만 | GPU 가속 꺼짐 | model.yml에서 `n_gpu_layers: -1` 확인 |
| 10 tok/s 미만 | Intel 버전 설치 | Jan.ai 공식 사이트에서 Apple Silicon 버전 재설치 |
| 응답이 늦게 시작됨 | ctx_len 너무 큼 | ctx_len을 기본값으로 줄이기 |
| 모델이 안 보임 | model.yml 오류 | id, engine 필드 확인 |

---

## 3.7 추천 초기 설정 (이 가이드 저자의 실제 설정)

```yaml
# Qwen3.6-35B-A3B APEX I-Compact (17GB)
id: qwen-3.6-35b
name: Qwen 3.6 35B APEX I-Compact
engine: llamacpp
ctx_len: 32768
temperature: 0.7
top_p: 0.9
max_tokens: 4096
n_gpu_layers: -1
prompt_template: "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
stop:
  - "<|im_end|>"
  - "<|im_start|>"
```

이 설정으로 M3 Max 48GB에서 **55~60 tok/s**의 속도를 유지합니다.

---

## 3.8 이 장 요약

| 단계 | 내용 |
|:----|:------|
| **설치** | jan.ai에서 다운로드, Apple Silicon 버전 필수 |
| **폴더 구조** | `~/Library/Application Support/Jan/data/llamacpp/models/<모델명>/` |
| **설정 파일** | `model.yml` 직접 작성 (ctx_len, n_gpu_layers 핵심) |
| **모델 이전** | LM Studio 폴더 → Jan.ai 폴더로 GGUF 복사 |
| **속도 확인** | 50+ tok/s 정상, `n_gpu_layers: -1` 반드시 확인 |

---

**4장에서는 Apple Silicon의 성능을 100% 활용하는 MLX 프레임워크 설정을 알아보겠습니다.**
