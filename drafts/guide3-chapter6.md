# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 6장: APEX 양자화 — MoE 모델 최적화와 리소스 분배

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 6.1 MoE(Mixture of Experts) 아키텍처 개요

MoE(전문가 혼합)는 거대 모델의 성능과 경량 모델의 속도를 양립하기 위한 핵심 아키텍처 디자인입니다. 모든 연산에 모델 전체의 파라미터를 동원하는 대신, 입력 값의 특성에 맞추어 최적의 내부 전문가 그룹만 동적으로 라우팅하는 구조입니다.

### 연산 구조적 비교 (Dense vs MoE)

```
[밀집형 Dense 모델: 예) Gemma 4 12B]
입력 텍스트 ───► [ 12B 파라미터 전체 연산 ] ───► 결과 출력
* 모든 토큰 생성 시 12B 가중치 전력 구동

[전문가 혼합 MoE 모델: 예) Qwen3.6-35B-A3B]
입력 텍스트 ───► [ 게이팅/라우터 ]
                       │
                       ├─► [전문가 A: 1.5B] ──┐
                       └─► [전문가 B: 1.5B] ──┴─► 결과 출력
* 전체 파라미터는 35B이지만, 실제 연산에 활성화되는 체급은 3B에 불과함
```

| 지표 | 밀집형 (Dense) | 전문가 혼합형 (MoE) |
|:----|:-----------|:-----------------|
| **전체 모델 가중치 용량** | 12B 파라미터 | 35B 파라미터 |
| **토큰당 실제 연산 유닛** | 12B (100% 가동) | **3B (약 8.6% 가동)** |
| **실측 추론 속도** | 25 ~ 35 tok/s | **50 ~ 60 tok/s** |
| **메모리 적재 요구량** | 적음 | 큼 (35B 모델 가중치 전체가 RAM에 대기) |
| **양자화 최적화 접근** | 선형 가중치 매핑 | **구조별 가변 매핑 (APEX)** |

MoE 모델은 메모리 적재 시 35B 모델 크기만큼 통합 램을 점유하지만, 실제 연산 가동부는 3B 내외이므로 **압도적인 속도로 동작하면서도 35B급의 다차원적 상식을 출력**하는 지식적 우위를 점합니다.

---

## 6.2 APEX 양자화 원리

APEX(Adaptive Precision for EXpert Models)는 MoE의 이러한 계층적 비대칭 구조에 맞춰 특별 설계된 혁신적 양자화 프로토콜입니다.

기존의 양자화는 모델 전 영역을 4비트나 3비트로 일률적으로 압축했습니다. 그러나 MoE 모델의 내부 컴포넌트들은 각각 기능적 중요도가 매우 상이합니다.
- **Edge Layers (입출력 외곽 레이어)**: 텍스트 해석과 최종 문장 완성을 전담하므로 정밀도가 망가지면 모델 전체가 오작동합니다.
- **Attention 블록**: 문맥의 관계도를 읽어내는 중추입니다.
- **Experts (전문가 유닛들)**: 특정 도메인 질문에만 반응하므로 압축 마진이 큽니다.

APEX는 **입출력 경계 레이어와 어텐션 유닛은 6~8비트 고정밀로 강하게 살리고, 중간의 Experten 유닛들은 2~4비트로 유연하게 깎아내는 스마트 분배 압축**을 통해 정보 유실 없이 전체 용량을 획득합니다.

---

## 6.3 APEX 프로필 선정 가이드 (M3 Max 48GB 기준)

Qwen3.6-35B-A3B 모델을 맥북 로컬 환경에 안착시킬 때 제공되는 네 가지 주요 APEX 프로필 설계 방식입니다.

| 프로필 네이밍 | 메모리 점유 크기 | 추론 퀄리티 지향도 | M3 Max 48GB 실전 운영 적합성 판단 |
|:------|:---:|:----|:-----------:|
| **I-Compact** ⭐ | **17GB** | **품질 대비 크기 균형 최상** | ✅ **적극 추천 (에이전트 인프라와 상시 공존 가능)** |
| **I-Mini** | 14GB | 리소스 극단 절약 | ✅ 가벼운 워크스테이션용으로 안정적 구동 |
| **I-Balanced** | 24GB | 고품질 문맥 유지 | ⚠️ 단독 구동 시 적합, 동시성 작업 시 스왑 발생 우려 |
| **I-Quality** | 22GB | 번역 및 논문 요약 특화 | ⚠️ 메모리 잔여 가용량에 따라 제한적 허용 |

### I-Compact 프로필 권장 이유
통합 RAM 48GB 환경에서 17GB의 **I-Compact** 모델을 적재하는 배치는 성능과 안전성의 황금비를 이룹니다.
1. **물리 메모리 격리성 보존**: OS 영역 및 에이전트 인프라(약 10~15GB)와 공존하고도 15GB 이상의 빈 RAM 여유를 보장합니다. 디스크 스왑이 절대로 발생하지 않아 프라이버시 누출 가능성을 봉쇄합니다.
2. **최적의 런타임 속도**: 스왑 없이 오직 물리 칩셋 가속으로만 데이터를 순환시키므로 **55~60 tok/s** 성능을 흔들림 없이 냅니다.

---

## 6.4 APEX 모델 전개 및 실행 프로토콜

### 1. 허깅페이스 검증 저장소로부터 다운로드
```bash
# OpenYourMind 커뮤니티의 35B MoE Abliterated APEX GGUF 다운로드 시퀀스
huggingface-cli download \
  OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF \
  OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
  --local-dir ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact
```

### 2. Jan.ai 관리 프로필 작성
다운로드된 모델 디렉토리 내에 아래와 같이 매니페스트를 배치합니다.

```bash
# 설정 파일 생성
cat > ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact/model.yml << 'EOF'
id: qwen-3.6-35b-i-compact
name: Qwen 3.6 35B APEX I-Compact (Abliterated)
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
```

---

## 6.5 양자화 포맷 실측 속도 및 품질 분석 (M3 Max 48GB)

| 변환 포맷 | 모델 실크기 | 추론 속도 | 실제 체감 성능 및 출력 특성 |
|:----------:|:--------:|:----:|:----:|
| 일반 GGUF Q4_K_M | 약 20GB | 48 tok/s | 고른 성능을 내나 용량 점유가 큼 |
| **APEX I-Compact** | **17GB** | **55~60 tok/s** | **동일 품질 기준 용량 15% 감축, 속도 20% 향상** |
| 일반 GGUF Q3_K_M | 약 14GB | 50 tok/s | 전문 영역 어휘 탈락 현상 관측됨 |
| APEX I-Mini | 14GB | 55 tok/s | 소형 모델 중 가장 매끄러운 응답 속도 |

APEX I-Compact 규격은 MoE의 구조적 특질을 온전히 계승하여 일반 Q4 양자화 모델 대비 디스크 용량과 칩셋 연산 가동률을 영리하게 아껴 냅니다.

다음 7장에서는 모델 성능은 저하시키지 않으면서도, 거대 테크 기업들이 부과한 왜곡된 필터링 가이드를 제거하는 무검열(Uncensored / Abliterated) 모델의 구현 기법을 알아보겠습니다.
