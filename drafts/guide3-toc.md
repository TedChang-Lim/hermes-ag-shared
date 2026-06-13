# 📦 맥북 로컬 AI 완전 정복 가이드 (목차)

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 목차

### 1장: 왜 로컬 AI인가?

- 클라우드 API의 문제점 (비용, 프라이버시, 속도)
- 로컬 AI의 장점: 무료, 오프라인, 무제한
- Apple Silicon(M 시리즈)이 특별한 이유
- 이 가이드의 목표: 맥북 하나로 AI 비서 완성하기

### 2장: LM Studio로 첫발 떼기

- LM Studio 설치 (공식 사이트)
- 첫 번째 모델 다운로드 (Qwen 3.5, Gemma 4)
- 모델 실행 및 채팅 테스트
- 속도 확인: tok/s 의미와 정상 범위
- 한계점 인식: LM Studio의 문제

### 3장: Jan.ai로 업그레이드

- LM Studio에서 Jan.ai로 이전해야 하는 이유
- Jan.ai 설치 및 기본 설정
- GGUF 모델 폴더 구조 이해
  ```bash
  ~/Library/Application Support/Jan/data/llamacpp/models/
  └── <모델명>/
      ├── model.gguf
      ├── mmproj.gguf (선택)
      └── model.yml
  ```
- model.yml 설정 완벽 가이드
  - batch_size, ctx_size, n_gpu_layers
- HuggingFace CLI로 모델 다운로드

### 4장: MLX — Apple 순정 최적화

- MLX 프레임워크란? (Apple의 Metal Performance Shaders)
- GGUF vs MLX: 언제 무엇을 써야 하나?
- MLX 모델 설치 및 실행
- vLLM(Mac)과 MLX 비교
- 실제 속도 비교 차트

### 5장: GGUF 양자화 완벽 이해

- 양자화(Quantization)란?
- Q2_K, Q3_K, Q4_K, Q5_K, Q6_K, Q8_0 차이
  - 작은 모델(Qwen 3B 등): Q8_0 권장
  - 중간 모델(Gemma 4 12B 등): Q4_K_M 권장
  - 큰 모델(Qwen 35B 등): Q3_K 또는 Q2_K
- 메모리 vs 품질 트레이드오프 표

### 6장: APEX 양자화 — MoE 모델의 비밀

- MoE(Mixture of Experts) 아키텍처 이해
  - Qwen3.6-35B-A3B = 35B 파라미터 중 3B만 활성화
  - Dense vs MoE 속도 비교
- APEX(Adaptive Precision for EXpert Models)란?
- APEX 프로필 선택 가이드
  - I-Compact (17GB) ⭐ 추천
  - I-Mini (14GB)
  - I-Balanced (24GB)
  - I-Quality (22GB)

### 7장: 검열 해제(Uncensored) 모델 선택

- 중국 모델의 정치적 검열 문제
- Abliterated (diff-in-means) 방식
- 추천 저장소
  - OpenYourMind
  - mudler APEX GGUF
- 설치 및 검증

### 8장: Hermes Agent + 로컬 모델 연동

- Hermes Agent에 로컬 모델 연결
  ```bash
  hermes config set model.base_url http://localhost:1337/v1
  ```
- 클라우드 + 로컬 하이브리드 전략
  - 일상 작업: DeepSeek V4 Flash (클라우드)
  - 민감한 작업: 로컬 모델
  - 이미지 분석: Mimo 2.5 (클라우드)
- Profile로 모델 전환 자동화

### 9장: 실제 마스터님의 하루

- 아침: DeepSeek Flash로 메일/리포트 확인
- 낮: Hermes Agent + AG 협업 (클라우드)
- 저녁: Jan.ai 로컬 모델로 테스트
- 밤: 크론잡 자동 실행
- 월간 비용 리포트

### 부록

- A. 추천 모델 사양표
- B. 문제 해결 (FAQ)
- C. 유용한 명령어 모음

---

**예상 분량:** Lite: 약 50페이지 / Pro: 약 80페이지 + 설정 파일 패키지
**예상 가격:** Lite $9.90 / Pro $24.90 (Guide 1과 동일)
