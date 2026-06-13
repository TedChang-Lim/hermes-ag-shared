# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 4장: MLX — Apple 순정 최적화

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 4.1 MLX란?

MLX는 **Apple이 직접 개발한 오픈소스 머신러닝 프레임워크**입니다. Apple Silicon(M1~M4)의 Metal GPU와 Neural Engine을 100% 활용하도록 설계되었습니다.

- **Apple이 만들었음** → Apple Silicon에 가장 최적화됨
- **NumPy 스타일 API** → Python 사용자에게 친숙함
- **통합 메모리 활용** → CPU/GPU 간 데이터 복사 불필요
- **오픈소스** → GitHub에서 공개, 커뮤니티 활발

> **쉽게 말하면:** MLX는 Apple Silicon 맥북을 AI 연산에 최적화하기 위한 Apple의 공식 도구입니다.

---

## 4.2 GGUF vs MLX: 무엇을 써야 할까?

많은 분들이 헷갈려 하는 부분입니다. 정리해 드립니다.

### 비교표

| 항목 | GGUF (llama.cpp) | MLX |
|:----|:----------------:|:---:|
| **개발 주체** | 커뮤니티 (llama.cpp) | **Apple (공식)** |
| **Apple Silicon 최적화** | 좋음 (Metal GPU) | **매우 좋음 (Neural Engine + GPU)** |
| **지원 모델 수** | **매우 많음** (수천 개) | 적음 (일부 주요 모델만) |
| **설치 난이도** | 쉬움 (Jan.ai, LM Studio) | 중간 (CLI 필요) |
| **속도 (M3 Max)** | 50~60 tok/s | **60~80 tok/s (20~30% 빠름)** |
| **멀티모달** | 제한적 | **지원 (MLX-VLM)** |
| **오디오 처리** | 없음 | **MLX-Audio (TTS/STT 지원)** |

### 선택 기준

| 사용 목적 | 추천 포맷 | 이유 |
|:---------|:---------|:-----|
| 빠른 설정, 초보자 | **GGUF + Jan.ai** | 설치부터 사용까지 5분 |
| 최고 속도, Apple 최적화 | **MLX** | 20~30% 더 빠름 |
| 오디오/TTS/STT | **MLX-Audio** | GGUF는 지원 안 함 |
| 최신 모델 테스트 | **GGUF** | MLX보다 먼저 나옴 |

> **이 가이드의 저자는 GGUF(Jan.ai)를 메인으로 사용하고, 필요에 따라 MLX를 병행합니다.**
> GGUF는 모델 다양성, MLX는 속도와 오디오 처리에서 강점을 가집니다.

---

## 4.3 MLX 설치

### 기본 설치

```bash
# pip로 MLX 설치
pip install mlx-lm

# 또는 Apple Silicon 최적화 버전
pip install "mlx-lm[apple]"

# 설치 확인
python -c "import mlx.core; print(f'MLX version: {mlx.core.__version__}')"
```

### MLX-Audio (음성 처리) 설치

```bash
# 오디오 관련 기능이 필요할 때
pip install mlx-audio

# TTS(음성 합성) 기능 포함
pip install "mlx-audio[tts]"
```

### MLX-VLM (비전/멀티모달) 설치

```bash
# 이미지 분석 기능이 필요할 때
pip install mlx-vlm
```

---

## 4.4 MLX로 모델 실행하기

### 기본 채팅 (mlx-community 활용 권장)

MLX로 모델을 로드할 때는 원래의 거대한 모델(Full Precision) 대신, Hugging Face의 **`mlx-community`** 채널에서 미리 최적화 및 양자화(Quantized)된 모델을 가져오는 것이 속도와 메모리 면에서 훨씬 유리합니다. 또한 대화용으로는 항상 `Instruct` 모델을 사용해야 합니다.

```bash
# mlx-community에서 4비트 양자화된 Qwen 2.5 3B Instruct 모델 실행
mlx_lm.generate \
  --model mlx-community/Qwen2.5-3B-Instruct-4bit \
  --prompt "안녕하세요, 로컬 AI 테스트 중입니다." \
  --max-tokens 512

# 또는 Python 스크립트로 실행할 때:
python -c "
from mlx_lm import load, generate

model, tokenizer = load('mlx-community/Qwen2.5-3B-Instruct-4bit')
response = generate(model, tokenizer, '안녕하세요!', max_tokens=512)
print(response)
"
```


### GGUF 파일을 MLX로 변환

이미 다운로드한 GGUF 파일이 있다면 MLX 형식으로 변환할 수 있습니다:

```bash
# GGUF → MLX 변환
mlx_lm.convert --gguf ./model.gguf --mlx-path ./mlx-model/
```

### 모델 캐싱 (중요!)

MLX는 HuggingFace에서 모델을 다운로드할 때 캐싱을 지원합니다:

```bash
# 캐싱 활용: 같은 모델은 두 번 다운로드하지 않음
export HF_HOME=~/.cache/huggingface
mlx_lm.generate --model Qwen/Qwen3.5-3B --prompt "테스트"
```

---

## 4.5 MLX-Audio로 음성 처리하기

MLX-Audio는 맥북에서 **로컬 TTS(음성 합성)와 STT(음성 인식)**를 가능하게 합니다.

### TTS (텍스트 → 음성)

```bash
# 텍스트를 음성 파일로 변환
python -c "
from mlx_audio.tts import generate

# 음성 생성
audio = generate(
    text='안녕하세요, 로컬 AI 음성 테스트입니다.',
    voice='default'
)
audio.save('output.wav')
print('✅ 음성 파일 저장 완료: output.wav')
"
```

### STT (음성 → 텍스트)

Groq API를 사용하는 헤나 위스퍼(Hena Whisper)와 달리, MLX-Audio는 **완전한 로컬 오프라인 음성 인식**을 지원합니다:

```bash
# 음성 파일을 텍스트로 변환
python -c "
from mlx_audio.asr import transcribe

result = transcribe('voice.wav', language='ko')
print(f'인식 결과: {result[\"text\"]}')
"
```

> ⚠️ MLX-Audio STT는 Groq Whisper API보다 속도는 느리지만, **인터넷 연결 없이** 사용할 수 있고 **비용이 0원**입니다.

---

## 4.6 MLX-VLM으로 이미지 분석하기

MLX-VLM을 사용하면 맥북에서 **로컬 이미지 분석**이 가능합니다:

```bash
# 이미지 분석
python -c "
from mlx_vlm import load, generate

model, processor = load('Qwen/Qwen-VL-2B')
response = generate(
    model, processor,
    image='photo.jpg',
    prompt='이 사진에 대해 설명해주세요',
    max_tokens=512
)
print(response)
"
```

---

## 4.7 실제 속도 비교 (M3 Max 48GB)

| 모델 | GGUF (Jan.ai) | MLX | 차이 |
|:----|:------------:|:---:|:----:|
| Qwen 3.5 3B | 82 tok/s | **95 tok/s** | MLX 16% ↑ |
| Qwen 3.5 7B | 55 tok/s | **68 tok/s** | MLX 24% ↑ |
| Qwen3.6-35B MoE | 55 tok/s | **65 tok/s** | MLX 18% ↑ |

> MLX가 평균적으로 GGUF보다 **20~30% 빠릅니다.**
> 다만 설치 과정이 GGUF보다 복잡하고, 지원하는 모델이 적다는 단점이 있습니다.

---

## 4.8 언제 MLX를 써야 할까?

### MLX 추천 상황
- ✅ **최고 속도**가 필요할 때
- ✅ **오디오 처리**(TTS/STT)가 필요할 때
- ✅ **이미지 분석**(로컬 비전)이 필요할 때
- ✅ Apple Silicon을 **100% 활용**하고 싶을 때

### GGUF 추천 상황
- ✅ **쉬운 설치**가 중요할 때
- ✅ **다양한 모델**을 테스트하고 싶을 때
- ✅ Jan.ai의 **체계적인 관리**가 필요할 때
- ✅ 모델 **검증/테스트**가 우선일 때

### 이 가이드 저자의 실제 사용 패턴

```bash
# 일상 채팅/작업: GGUF + Jan.ai (Qwen3.6-35B, 55 tok/s)
# → 모델 다양성 + 체계적 관리

# 속도가 중요한 작업: MLX (같은 모델, 65 tok/s)
# → 20% 빠른 응답

# 음성 처리: MLX-Audio
# → 로컬 TTS/STT (인터넷 불필요)

# 이미지 분석: Mimo 2.5 (클라우드)
# → 로컬 VLM보다 성능 우수
```

---

## 4.9 이 장 요약

| 항목 | 내용 |
|:----|:-----|
| **MLX란?** | Apple이 만든 Apple Silicon 전용 ML 프레임워크 |
| **GGUF vs MLX** | GGUF = 쉬움, 모델 다양성 / MLX = 빠름, 오디오 지원 |
| **속도** | MLX가 GGUF보다 20~30% 빠름 |
| **설치** | `pip install mlx-lm` |
| **MLX-Audio** | 로컬 TTS/STT 가능 (오프라인) |
| **MLX-VLM** | 로컬 이미지 분석 가능 |
| **추천** | 메인 = GGUF(Jan.ai), 속도 필요 시 = MLX 병행 |

---

**5장에서는 GGUF 양자화(Quantization)를 완벽히 이해하고, 내 맥북에 딱 맞는 모델 용량과 속도를 선택하는 방법을 알아보겠습니다.**
