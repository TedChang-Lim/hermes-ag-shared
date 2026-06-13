# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 6장: APEX 양자화 — MoE 모델의 비밀

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 6.1 MoE(Mixture of Experts)란?

MoE는 **"전문가 혼합"**이라는 뜻으로, 하나의 큰 모델 안에 여러 개의 작은 "전문가(Expert)"를 두고, 입력에 따라 필요한 전문가만 선택적으로 사용하는 구조입니다.

### Dense vs MoE

```
Dense 모델 (예: Gemma 4 12B)
┌─────────────────────────────────────┐
│ 모든 입력이 모든 파라미터(12B)를 거침 │  → 항상 12B 전부 연산
└─────────────────────────────────────┘

MoE 모델 (예: Qwen3.6-35B-A3B)
┌─────────────────────────────────────┐
│ Router가 입력 보고 필요한 전문가만   │
│ 선택 → 35B 중 3B만 활성화           │  → 필요한 3B만 연산
└─────────────────────────────────────┘
```

| 비교 | Dense (밀집) | MoE (전문가 혼합) |
|:----|:-----------|:-----------------|
| **전체 파라미터** | 12B | 35B |
| **활성화 파라미터** | 12B (100%) | **3B (8.6%)** |
| **추론 속도** | 25~35 tok/s | **50~60 tok/s** |
| **메모리 사용** | 많음 | 전체 로드는 필요하지만 연산 적음 |
| **양자화 효과** | 일반적 | **APEX 특화** |

> **핵심:** MoE는 35B 모델이지만 3B만 활성화되므로, 12B Dense 모델보다 **2배 빠르면서도** 35B의 지식을 가질 수 있습니다.

---

## 6.2 APEX 양자화란?

APEX(**A**daptive **P**recision for **E****x**pert Models)는 MoE 모델을 위해 특별히 설계된 양자화 방식입니다.

### 일반 양자화의 문제

일반 양자화(Q4_K_M 등)는 모델의 모든 부분을 동일한 정밀도로 압축합니다. 하지만 MoE 모델은 구조가 다릅니다:
- **Edge Layers** (첫 번째와 마지막 몇 개 층) — 모든 입력이 반드시 거침, 중요도 높음
- **Middle Routed Experts** (중간 전문가 층) — 한 번에 일부만 활성화됨
- **Shared Expert** — 모든 입력이 공유하는 전문가

### APEX의 차별점

| 모델 부분 | 일반 양자화 | APEX 양자화 |
|:---------|:----------|:-----------|
| Edge Layers | 동일 정밀도 | **높은 정밀도 유지** |
| Middle Experts | 동일 정밀도 | **낮은 정밀도로 압축** |
| Shared Expert | 동일 정밀도 | **높은 정밀도 유지** |
| Attention | 동일 정밀도 | **높은 정밀도 유지** |

> APEX는 **중요한 부분은 살리고, 덜 중요한 부분은 더 많이 압축**하는 스마트한 양자화입니다.

---

## 6.3 APEX 프로필 선택 가이드

Qwen3.6-35B-A3B 모델 기준으로 제공되는 APEX 프로필입니다:

### 프로필별 크기와 용도

| 프로필 | 크기 | 용도 | M3 Max 48GB |
|:------|:---:|:----|:-----------:|
| **I-Compact** ⭐ | **17GB** | **범용 최적** | ✅ **추천! Hermes와 동시 운영 가능** |
| I-Mini | 14GB | 가장 가벼움 | ✅ 충분 |
| I-Balanced | 24GB | 최고 품질 | ⚠️ 비어 있으면 가능 |
| I-Quality | 22GB | 고품질 | ⚠️ 가능 |

### I-Compact가 추천되는 이유

M3 Max 48GB에서 I-Compact(17GB)를 선택하면:
- 모델이 17GB 사용
- Hermes Agent 등 다른 앱이 10~15GB 사용
- 남은 16GB + @로 여유 있음
- **55~60 tok/s** 속도 유지

I-Balanced(24GB)를 선택하면:
- 모델이 24GB 사용
- 다른 앱/시스템이 15~20GB 사용
- **스왑(Swap) 발생 → 속도 30% 저하**
- tok/s가 절반 이하로 떨어질 수 있음

> **M3 Max 48GB에서 I-Compact는 속도와 품질의 황금비율입니다.**

---

## 6.4 APEX 설치 방법

### 다운로드

```bash
# 추천 저장소
# 1. OpenYourMind (Abliterated + APEX)
#    https://huggingface.co/OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF

# 2. mudler (APEX GGUF)
#    https://huggingface.co/mudler/Qwen3.6-35B-A3B-uncensored-heretic-APEX-GGUF

# 다운로드 예시
huggingface-cli download \
  OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF \
  OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
  --local-dir ~/Downloads/
```

### Jan.ai에 설치

```bash
# 1. Jan.ai 모델 폴더 생성
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact

# 2. 다운로드한 파일 복사
cp ~/Downloads/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact/

# 3. model.yml 생성
cat > ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact/model.yml << 'EOF'
id: qwen-3.6-35b-i-compact
name: Qwen 3.6 35B APEX I-Compact (Uncensored)
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
EOF

# 4. Jan.ai 재시작 후 모델 선택
```

---

## 6.5 APEX vs 일반 양자화 속도 비교

### Qwen3.6-35B-A3B (M3 Max 48GB 기준)

| 양자화 방식 | 파일 크기 | 속도 | 품질 |
|:----------:|:--------:|:----:|:----:|
| 일반 Q4_K_M | 약 20GB | 48 tok/s | 좋음 |
| APEX I-Compact | **17GB** | **55~60 tok/s** | **좋음** |
| 일반 Q3_K_M | 약 14GB | 50 tok/s | 보통 |
| APEX I-Mini | 14GB | 55 tok/s | 보통 |
| 일반 Q2_K | 약 10GB | 52 tok/s | 낮음 |

> APEX I-Compact는 일반 Q4_K_M보다 **파일 크기는 15% 작고, 속도는 20% 더 빠릅니다.**
> 동시에 품질은 Q4_K_M과 거의 동일합니다.

---

## 6.6 iMatrix: 추가 최적화

APEX는 **iMatrix(iMatrix 보정)**라는 추가 최적화를 지원합니다. iMatrix는 실제 사용 패턴을 분석하여 양자화 최적화를 위한 중요도를 측정합니다.

```bash
# Hermes Agent 세션 trace로 iMatrix 생성 (고급)
# 도구 호출, 코드 생성 등의 패턴에 최적화

# 이미 iMatrix가 적용된 모델:
# - mudler/Qwen3.6-35B-A3B-uncensored-heretic-APEX-GGUF
# - OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF
```

> 일반 사용자는 **이미 iMatrix가 적용된 APEX GGUF 파일을 다운로드**하기만 하면 됩니다.

---

## 6.7 이 장 요약

| 항목 | 내용 |
|:----|:-----|
| **MoE란?** | 여러 전문가 중 필요한 것만 활성화 (35B 중 3B만) |
| **APEX란?** | MoE 전용 양자화, 중요한 부분은 살리고 덜 중요한 부분은 압축 |
| **추천 프로필** | **I-Compact (17GB)** — M3 Max 48GB에 최적 |
| **속도** | 일반 Q4보다 20% 빠름 (55~60 tok/s) |
| **설치** | HuggingFace → Jan.ai model.yml 설정 |
| **iMatrix** | 실제 사용 패턴 기반 추가 최적화 (이미 적용된 파일 사용) |

---

**7장에서는 검열 해제(Uncensored / Abliterated) 모델을 선택하고 설치하는 방법을 알아보겠습니다.**
