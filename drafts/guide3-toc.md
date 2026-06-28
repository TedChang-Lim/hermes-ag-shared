# 📦 맥북 로컬 AI 완전 정복 가이드 (목차)

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 목차

### 1장: 왜 로컬 AI인가?

- 클라우드 AI와 데이터 주권 (비용, 프라이버시, 속도)
- 로컬 AI의 본질적 가치: 무검열, 오프라인, 제로 비용
- Apple Silicon(통합 메모리) 하드웨어가 바꾼 패러다임
- Mythos 시나리오: 내 맥북에 구축하는 격리된 인공지능 연구소

### 2장: LM Studio로 첫발 떼기

- 온디바이스 AI 입문 도구, LM Studio
- 첫 번째 모델 다운로드 및 구동 (Qwen 3.5, Gemma 4)
- Metal GPU 가속 활성화 및 추론 속도(tok/s) 최적화
- 로컬 OpenAI 호환 API 서버 가동
- LM Studio의 구조적 한계와 극복 방안

### 3장: Jan.ai로 업그레이드 — 본격적인 모델 관리

- 왜 Jan.ai인가? 로컬 파일 제어권 확보
- Jan.ai 설치 및 환경 구성
- GGUF 모델 폴더와 yml 설정 구조 분석
- model.yml 설정 가이드 (batch_size, ctx_size, n_gpu_layers)
- HuggingFace CLI를 통한 정밀한 모델 반입

### 4장: MLX — Apple Silicon 순정 최적화 프레임워크

- Apple 공식 MLX 프레임워크의 메커니즘
- GGUF vs MLX: 아키텍처와 성능 트레이드오프
- mlx-lm 라이브러리 설치 및 모델 구동
- MLX-Audio를 활용한 오프라인 음성 처리 (STT/TTS)
- MLX-VLM 기반의 온디바이스 이미지 분석

### 5장: GGUF 양자화 아키텍처 완벽 이해

- 정밀도 압축(Quantization)의 수학적 이해
- 비트별 특성과 트레이드오프 (Q2_K부터 Q8_0까지)
- 하드웨어 사양별(RAM 용량) 최적의 양자화 프로필 매핑
- iMatrix 보정을 통한 양자화 손실 최소화 전략

### 6장: APEX 양자화 — MoE 모델 최적화의 핵심

- MoE(Mixture of Experts) 아키텍처와 추론 속도의 비밀
- APEX(Adaptive Precision for EXpert Models) 작동 원리
- 하드웨어 리소스 효율을 극대화하는 프로필 설계 (I-Compact 등)
- M3 Max 48GB 환경에서의 APEX 실전 적용

### 7장: 무검열(Uncensored) 모델 빌드 및 도입

- 거대 IT 기업의 정밀한 모델 검열 필터링 실태
- Abliterated (거절 벡터 절제) 기법의 원리와 효과
- 신뢰할 수 있는 무검열 모델 배포 채널 (OpenYourMind, mudler)
- 로컬 환경 탑재 및 정상 작동 테스트

### 8장: Hermes Agent + 로컬 모델 연동

- Nous Research의 오픈소스 에이전트 프레임워크, Hermes Agent
- 클라우드와 온디바이스의 시너지: 하이브리드 인텔리전스 아키텍처
- config.yaml 정밀 설정 가이드
- Telegram 연동 및 오프라인 음성 에이전트 구축 실전

### 9장: 실전 운영 가이드 — 24시간 로컬 에이전트 라이프

- 30년 IT 엔지니어 출신 창작자가 설계한 AI 협업 일상
- 아침 브리핑부터 야간 자동 백업까지의 실전 타임라인
- 하이브리드 연동을 통한 월 $4.50 초저비용 시스템의 실체
- 1인 대기업을 실현하는 로컬 AI 인프라의 미래

### 부록

- A. Apple Silicon 사양별 권장 모델 매핑 테이블
- B. 자주 겪는 트러블슈팅 및 예외 처리
- C. 로컬 AI 관리자 필수 명령어 레퍼런스

---

**예상 분량:** 약 80페이지 내외 (실전 설정 코드 포함)  
**출판 포맷:** e-Book (PDF / EPUB)  
