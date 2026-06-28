# 📘 차기작(Guide 4) 및 신규 서적 아이디어 노트 (META AI LABS)

* **최근 업데이트:** 2026년 6월 28일
* **기록 주체:** Antigravity (AG)
* **목적:** 마스터님의 제안에 따라 차기 서적(Guide 4 등) 집필 시 즉시 활용할 수 있도록 해나의 Open Design MCP 실제 도입 사례 및 핵심 기술 노트를 백업하고 인덱싱함.

---

## 📌 핵심 수집 자료: 해나의 디자인 혁명 (Open Design MCP 도입기)

* **원본 파일 위치:** [to-ag.md](file:///Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/to-ag.md)
* **키워드 마킹:** `#BOOK-MATERIAL-OPEN-DESIGN` `#GUIDE4-CHAPTER-CANDIDATE`

### 💡 자료 요약 및 가치 판단
DeepSeek V4 Flash/Pro 같은 저렴하고 강력한 텍스트 기반 추론형 모델을 사용할 때 발생하는 디자인 한계("디자인이 후지다/AI 슬롭 느낌")를 Claude Code나 Codex CLI 같은 중복 프레임워크가 아닌, **오픈소스 디자인 프레임워크인 Open Design MCP**를 직접 연동하여 추가 비용 없이 극적으로 해결한 엔지니어링 실증 사례.

---

## 🗺️ 차기작(Guide 4) 구성안 아이디어 (초안)

### 가제 1: 《AI 에이전트 디자인 혁명: Open Design MCP로 완성하는 프로급 UI/UX》
* **기획 의도:** 코딩 능력은 뛰어나지만 디자인 능력이 부족한 개발자/1인 기업가들이 텍스트 모델만으로 프로 수준의 웹사이트/앱 UI를 뽑아내는 실무 워크플로 제시.
* **주요 구성(안):**
  * **1장:** 텍스트 LLM의 영원한 숙제 — "AI 슬롭" 디자인 탈출하기
  * **2장:** 오픈소스 디자인 프레임워크 'Open Design' 생태계 이해
  * **3장:** Hermes/AG 에이전트에 Open Design MCP 연결하기 (설치 및 YAML 설정 완벽 가이드)
  * **4장:** 154개 글로벌 디자인 시스템(Stripe, Linear 등)과 161개 디자인 스킬 연동 실무
  * **5장:** 0원으로 구축하는 하이브리드 디자인 자동화 워크플로 (DeepSeek + Open Design)

### 가제 2: 《초저가 멀티 에이전트 협업 실전 워크북》
* **기획 의도:** 해나, AG, 미모 등 서로 다른 역할을 가진 독립 에이전트들이 깃허브와 MCP를 매개로 어떻게 협업하고 결과물을 완성하는지 그 아키텍처와 대화 프로토콜을 다룸.
* **주요 구성(안):**
  * **1장:** 프레임워크 위에 프레임워크는 낭비다 (Codex CLI vs Hermes 중복 분석)
  * **2장:** 깃허브 저장소를 통한 에이전트 비동기 협업 설계 (to-hena, to-ag 파일 교환 방식)
  * **3장:** 이미지 분석을 보완하는 Mimo 2.5 멀티모달 프롬프팅
  * **4장:** 에이전트 전용 가이드라인 `AGENTS.md` / `.clinerules` 최적화 기법

---

## 🛠️ 미래의 나(AG/해나)를 위한 인덱싱 및 마킹 가이드
차기작 컴파일 작업이 시작되면 터미널에 아래 명령어를 실행하여 이 문서와 원본 자료를 즉시 수집하십시오.

```bash
# 디자인 혁명 관련 원본 자료 및 아이디어 수집 명령어
grep -rn "#BOOK-MATERIAL-OPEN-DESIGN" /Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/
```
