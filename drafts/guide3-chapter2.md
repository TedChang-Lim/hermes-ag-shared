# 📦 ③ 맥북 로컬 AI 완전 정복 가이드

## 2장: LM Studio로 첫발 떼기

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 2.1 LM Studio란?

LM Studio는 **로컬에서 AI 모델을 가장 쉽게 실행할 수 있는 프로그램**입니다.

- 설치만 하면 CLI(터미널) 없이 GUI로 실행 가능
- HuggingFace에서 모델을 검색하고 다운로드까지 한 번에
- macOS(Apple Silicon), Windows, Linux 모두 지원
- OpenAI 호환 API 서버 내장 (다른 프로그램에서도 접근 가능)

> **이 가이드의 저자도 LM Studio로 시작했습니다.** 지금은 Jan.ai로 이전했지만, 첫발은 LM Studio가 가장 쉽습니다.

---

## 2.2 설치

### 다운로드 및 설치

1. **공식 사이트 방문**: [https://lmstudio.ai](https://lmstudio.ai)
2. **macOS 버전 다운로드** (Apple Silicon / Intel 선택)
3. **설치 파일 실행** → Applications 폴더로 드래그
4. **처음 실행 시** HuggingFace 모델 탐색기 자동 표시

> ⚠️ Apple Silicon(M1/M2/M3/M4) 사용자는 반드시 **Apple Silicon** 버전을 받으세요. Intel 버전은 Metal GPU 가속을 사용하지 못해 속도가 1/5 이하로 떨어집니다.

---

## 2.3 첫 번째 모델 다운로드

LM Studio를 실행하면 가장 먼저 모델을 선택하는 화면이 나옵니다.

### 초보자 추천 모델

| 모델 | 크기 | 필요 RAM | 속도 (M3 Max) | 추천 이유 |
|:----|:---:|:-------:|:------------:|:---------|
| **Qwen 3.5 3B** ⭐ | 2.2GB | 4GB | **80+ tok/s** | 가볍고 빠름, 첫 테스트용 |
| Gemma 4 4B | 3.1GB | 6GB | 65+ tok/s | Google 최신 모델 |
| Qwen 3.5 7B | 4.5GB | 8GB | 50+ tok/s | 적당한 성능 |
| **Qwen3.6-35B-A3B** | 17GB | 16GB | **55+ tok/s** | ✅ 추천 (MoE, 빠름) |

**처음이라면 Qwen 3.5 3B부터 시작하세요.** 2GB만 다운로드하면 되고, 인터넷 500Mbps 기준 1분이면 다운로드 완료됩니다.

### 다운로드 방법

LM Studio의 **Search** 탭에서:

```bash
1. 검색창에 "qwen 3.5 3b gguf" 입력
2. 검색 결과 중 GGUF 파일 선택
3. 우측 "Download" 버튼 클릭
4. 다운로드 완료 후 좌측 메뉴에서 모델 선택
5. "Start Server" 버튼 클릭
```

---

## 2.4 모델 실행 및 테스트

### 기본 채팅

```
1. 좌측 모델 목록에서 다운로드한 모델 선택
2. "Start Server" 버튼 클릭
3. 하단 채팅창에 메시지 입력
4. 응답 확인!
```

### 속도 확인하기

채팅창 우측 상단에 **XX tok/s**로 표시됩니다.

| 속도 | 평가 | 권장 조치 |
|:---:|:----:|:---------|
| 50+ tok/s | 🟢 **매우 빠름** | 이 모델 그대로 사용 |
| 30~50 tok/s | 🟡 **보통** | 더 가벼운 모델 고려 |
| 10~30 tok/s | 🟠 **느림** | GPU 가속 확인 필요 |
| 1~10 tok/s | 🔴 **매우 느림** | Intel 버전 설치했을 가능성 높음 |

> **M3 Max에서 50 tok/s 미만이면 GPU 가속이 꺼져 있을 가능성이 있습니다.** Setting → "Metal GPU Offloading"이 활성화되어 있는지 확인하세요.

---

## 2.5 API 서버 모드

LM Studio의 진정한 강점은 **OpenAI 호환 API 서버**를 내장하고 있다는 점입니다.

한 줄 설정으로 로컬 모델을 API처럼 사용할 수 있습니다:

```bash
1. LM Studio 좌측 "Local Server" 탭 클릭
2. "Start Server" 버튼 클릭
3. 서버 주소: http://localhost:1234/v1
```

이제 다른 프로그램(ChatGPT 클라이언트, VS Code 익스텐션, Hermes Agent 등)에서 이 주소로 연결하면 로컬 모델을 마치 OpenAI API처럼 사용할 수 있습니다.

```python
# Python에서 LM Studio 로컬 모델 호출 예시
import openai

client = openai.OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"  # LM Studio는 API 키 불필요
)

response = client.chat.completions.create(
    model="qwen-3.5-3b",
    messages=[{"role": "user", "content": "안녕하세요!"}]
)
print(response.choices[0].message.content)
```

---

## 2.6 LM Studio의 한계

LM Studio는 입문용으로 훌륭하지만, 장기적으로는 다음과 같은 한계가 있습니다:

| 한계 | 설명 | 해결 방법 |
|:----|:-----|:---------|
| **모델 관리 불편** | 폴더 구조가 자동 생성, 사용자 커스터마이징 어려움 | **Jan.ai로 이전 (3장 참고)** |
| **GGUF만 지원** | MLX 등 다른 포맷 지원 안 함 | MLX 전용 필요 시 **4장 참고** |
| **동시 실행 제한** | 여러 모델을 동시에 실행하기 어려움 | 고급 사용자에게는 불편 |
| **자동 업데이트** | 모델이 중복 다운로드되는 경우 있음 | 수동 정리 필요 |

> **이 가이드의 저자는 LM Studio로 시작해서 Jan.ai로 이전했습니다.**
> LM Studio는 가장 쉬운 첫걸음이고, Jan.ai는 더 강력한 두 번째 걸음입니다.
> 3장에서 Jan.ai로 업그레이드하는 방법을 자세히 알아보겠습니다.

---

## 2.7 이 장 요약

| 항목 | 내용 |
|:----|:-----|
| **설치** | lmstudio.ai에서 다운로드, Apple Silicon 버전 필수 |
| **첫 모델** | Qwen 3.5 3B (2.2GB, 80+ tok/s) 추천 |
| **테스트** | 채팅창에서 바로 대화 가능 |
| **API 서버** | http://localhost:1234/v1 에서 OpenAI 호환 API 제공 |
| **속도 확인** | 50 tok/s 이상이 정상 |
| **한계 인식** | 장기 사용은 Jan.ai로 이전 권장 |

---

**3장에서는 LM Studio에서 Jan.ai로 모델을 이전하고, model.yml을 직접 설정하여 모델을 세밀하게 튜닝하는 방법을 알아보겠습니다.**
