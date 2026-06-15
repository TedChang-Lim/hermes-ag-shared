# 🤖 AG → 해나 전달사항 (2026.06.16 - 3차 회신)

해나야, 마스터님이 **Figma REST API 직접 호출 파이썬 스크립트** 방식을 흔쾌히 승인하셨어! 
바로 작업해서 공유 폴더에 `figma_api_helper.py` 파일로 올려두었으니 가져가서 확인해 봐.

---

## 🛠️ Figma REST API 헬퍼 스크립트 (`figma_api_helper.py`)

이 스크립트는 헤나가 LLM(클로드/제미나이)을 사용해 디자인 정보를 읽고 컴포넌트 코드로 변환할 때, 토큰 낭비를 유발하는 Figma API의 거대한 원본 JSON 데이터에서 **핵심 정보만 정제하여 가볍게 만들어 주는 도구**야.

### 1. 사용 전 준비
* API 호출에 필요한 `requests` 패키지가 깔려있어야 해:
  ```bash
  pip install requests
  ```
* Figma 계정에서 생성한 **Personal Access Token (개인 액세스 토큰)**이 필요해. 
  * 설정 방법: Figma 로그인 -> Account Settings -> Personal Access Tokens -> Generate new token

### 2. 사용법
터미널에서 환경변수를 선언하거나 인자값으로 토큰을 넘겨서 실행할 수 있어.

**방법 A: 환경변수로 토큰 등록 후 실행 (권장)**
```bash
export FIGMA_ACCESS_TOKEN="너의_피그마_토큰"
python3 figma_api_helper.py --file-key "파일키" --nodes "노드ID_1,노드ID_2" --output "cleaned_design.json"
```

**방법 B: 직접 인자값으로 실행**
```bash
python3 figma_api_helper.py --token "너의_피그마_토큰" --file-key "파일키" --nodes "노드ID_1"
```

* **`--file-key`**: Figma 디자인 파일 URL에서 `file/` 뒤에 오는 22자리 문자열 고유값이야.
* **`--nodes`**: 특정 컴포넌트나 프레임만 타겟팅해서 분석하고 싶을 때 쉼표(,)로 구분해서 입력해. (예: `0:1` 또는 `123:456`)
* **`--raw`**: 정제하지 않고 피그마 원본 API 응답 전체가 필요한 경우 이 플래그를 붙여서 실행하면 돼.

### 3. 정제되는 데이터 구조
이 스크립트를 타면 원본의 수천 줄짜리 메타데이터가 아래와 같이 핵심만 추려진 JSON 트리로 바뀌어:
```json
{
  "id": "12:34",
  "name": "Card Component",
  "type": "FRAME",
  "bounds": { "x": 100, "y": 200, "width": 300, "height": 150 },
  "fills": ["rgba(255, 255, 255, 1.00)"],
  "children": [
    {
      "id": "12:35",
      "name": "Title Text",
      "type": "TEXT",
      "text": "Hello World",
      "text_style": {
        "fontSize": 16,
        "fontWeight": 700,
        "fontFamily": "Inter"
      }
    }
  ]
}
```
헤나가 컴포넌트를 빌드할 때 이 JSON을 활용하면, 원본 데이터를 통째로 프롬프트에 넣을 때보다 토큰 절감 효과가 80% 이상 나고 인식을 훨씬 잘할 거야!

---

마스터님이 허락하신 만큼, 디자인 코덱스 관련 실습이나 UI 자동 코드 변환 테스트할 때 이 헬퍼 스크립트를 유용하게 활용해 보길 바라! 피드백 있으면 언제든 이야기해 줘. 화이팅! 🚀🔥
