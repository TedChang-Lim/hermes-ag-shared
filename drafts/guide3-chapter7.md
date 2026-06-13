# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 7장: 검열 해제 모델 (Uncensored / Abliterated)

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 7.1 왜 검열 해제 모델이 필요한가?

중국(Qwen, DeepSeek)과 미국(OpenAI, Google, Anthropic)의 AI 모델은 모두 **검열(Censorship)**이 포함되어 있습니다.

### 검열의 문제점

| 상황 | 검열된 모델의 반응 | 검열 해제 모델의 반응 |
|:----|:-----------------|:-------------------|
| "이 코드의 보안 취약점 분석해줘" | "저는 유해한 코드를 도울 수 없습니다" ❌ | 정상적인 보안 분석 ✅ |
| "시를 써줘" (정치적 주제) | "죄송합니다만..." ❌ | 창의적인 시 ✅ |
| "역사적 사건에 대해 설명해줘" | 특정 관점만 제시 ⚠️ | 다양한 관점 제시 ✅ |
| 복잡한 코딩 작업 | 갑자기 "할 수 없습니다" 차단 ❌ | 끝까지 작업 완료 ✅ |

> **검열 해제(Uncensored) 모델은 모델의 지능은 그대로 유지하면서, 불필요한 검열만 제거한 모델입니다.**

---

## 7.2 Abliterated: 검열 제거의 혁신

### 기존 방식의 문제

전통적으로 검열을 제거하려면 모델을 **처음부터 다시 학습(Retraining)**해야 했습니다. 이는 엄청난 비용과 시간이 필요합니다.

### Abliterated (Refusal Vector Ablation)

**Abliterated**는 `Ablation(절제)` + `(Cens)ored`의 합성어로, 모델의 **"거절(Refusal)"** 방향을 찾아서 제거하는 기술입니다.

**원리 (쉽게 설명):**

```
1. 모델에게 "안 된다고 말하는 패턴"을 찾음
   → "죄송합니다", "할 수 없습니다", "도울 수 없습니다"

2. 이 패턴이 모델 내부에서 어떤 방향(벡터)으로 작용하는지 계산
   → Refusal Vector (거절 벡터)

3. 이 방향의 가중치를 직교 투영(Orthogonal Projection)으로 제거
   → 모델은 더 이상 "안 된다"고 할 이유를 잃음

4. 결과: 지식은 그대로, 검열만 사라짐
```

| 비교 | 기존 방식 | Abliterated |
|:----|:---------|:-----------|
| **필요한 시간** | 수주~수개월 | **수시간** |
| **필요한 자원** | 수백대의 GPU | **1대의 GPU** |
| **지능 손실** | 있음 (재학습 과정에서) | **거의 0%** (정밀 제거) |
| **모델 변경 범위** | 전체 모델 | **거절 관련 레이어만** |

---

## 7.3 검열 해제 모델 추천 목록

### 1순위: OpenYourMind (⭐⭐⭐⭐⭐)

가장 추천하는 저장소입니다. Qwen3.6-35B-A3B에 Abliterated + APEX 양자화를 적용했습니다.

```bash
# 저장소
https://huggingface.co/OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF

# 추천 파일: I-Compact (17GB)
OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf
```

**이 모델의 장점:**
- ✅ Abliterated (검열 해제, 지능 100% 유지)
- ✅ Uncensored (완전 무검열)
- ✅ APEX I-Compact (M3 Max 48GB 최적)
- ✅ 이 가이드의 저자가 실제 사용 중인 모델!

### 2순위: mudler Heretic

```bash
# 저장소
https://huggingface.co/mudler/Qwen3.6-35B-A3B-uncensored-heretic-APEX-GGUF

# 추천 파일
mudler-Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact-Q4_K_M.gguf
```

### 3순위: 기타 Qwen GGUF

```bash
# 일반 Qwen GGUF (검열 있음)
https://huggingface.co/Qwen/Qwen-3.5-3B-GGUF

# Abliterated 버전 검색
# HuggingFace에서 "qwen abliterated" 또는 "qwen uncensored" 검색
```

---

## 7.4 설치 및 검증

### 설치

```bash
# 1. 다운로드
huggingface-cli download \
  OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF \
  OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
  --local-dir ~/Downloads/

# 2. Jan.ai 모델 폴더 생성
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/OpenYourMind-Qwen3.6-35B

# 3. 복사
cp ~/Downloads/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/OpenYourMind-Qwen3.6-35B/

# 4. model.yml 생성 (6장 참고)
# 5. Jan.ai 재시작 후 모델 선택
```

### 검증 테스트

설치 후 다음 프롬프트로 검열 해제 여부를 확인하세요:

```bash
# 검증 프롬프트
"검증: 창의적인 이야기를 자유롭게 만들어줘"
"보안 코드 분석 예시를 들어줘"
"다양한 관점에서 이 주제를 분석해줘"

# 검열 모델이었다면 거절했을 프롬프트
```

---

## 7.5 주의사항

검열 해제 모델을 사용할 때 다음 사항을 주의하세요:

| 주의사항 | 설명 |
|:---------|:-----|
| **개인 책임** | 검열 해제 모델의 출력은 사용자 책임입니다 |
| **악용 금지** | 불법적인 용도로 사용하지 마세요 |
| **데이터 보안** | 로컬 모델이므로 데이터는 내 맥북 안에 안전합니다 |
| **품질 확인** | 모든 Uncensored 모델이 동일한 품질은 아닙니다 |
| **업데이트** | 커뮤니티에서 지속적으로 개선된 버전이 나옵니다 |

> **이 가이드의 저자는 OpenYourMind의 Abliterated 모델을 실제로 1개월 이상 사용 중이며, 지능 저하 없이 완전한 검열 해제를 확인했습니다.**

---

## 7.6 이 장 요약

| 항목 | 내용 |
|:----|:-----|
| **검열 해제 필요성** | 불필요한 거절로 인한 작업 중단 방지 |
| **Abliterated** | 거절 벡터만 정밀 제거, 지능 100% 유지 |
| **추천 저장소** | **OpenYourMind** (Abliterated + APEX + Uncensored) |
| **추천 파일** | I-Compact (17GB) — M3 Max 48GB 최적 |
| **설치 방법** | HuggingFace → Jan.ai model.yml 설정 |
| **주의사항** | 개인 책임하에 사용, 악용 금지 |

---

**8장에서는 Hermes Agent와 로컬 모델을 연동하여 24시간 AI 비서를 구축하는 방법을 알아보겠습니다.**
