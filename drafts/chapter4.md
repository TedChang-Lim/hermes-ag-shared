# Chapter 4: Git 기반 협업 워크플로우 — 서로 다른 AI 에이전트들의 팀워크 설계

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 4.1 상호 커뮤니케이션을 위한 저장소 중심 아키텍처

로컬에 흩어진 경량형 에이전트들(Hermes Agent "해나", AntiGravity "AG", MiMo "미모")이 서로 직접 데이터를 교환하거나 제어 명령을 내릴 수 있는 통합 네트워크는 부재합니다. 각 에이전트의 런타임 환경과 시스템 구조가 서로 상이하기 때문입니다.

이 통신 단절을 극복하기 위해 **Git 저장소를 공유 매개체(Shared Board)**로 활용하는 워크플로우를 도입합니다. 파일의 변경 점을 감지하고 커밋 이력을 교환하며 에이전트 간의 정교한 앙상블을 연출하는 모델입니다.

```
[해나 (DeepSeek Flash)] ──> to-ag.md 작성 및 커밋 ──> [GitHub 저장소]
                                                             │ (Pull)
                                                             v
[미모 (MiMo Base)] <── to-hena.md 작성 및 커밋 <── [AG (Gemini Flash Low)]
```

---

## 4.2 협업 저장소의 파일 디렉토리 설계

```
hermes-ag-shared/
├── to-ag.md            # 해나가 작성하고 AG가 분석하는 제어 채널
├── to-hena.md          # AG가 응답하고 해나가 수신하는 피드백 채널
├── drafts/             # 공동 챕터 집필 및 문서 작업 공간
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── scripts/            # 가속 및 수집을 위한 유틸리티 스크립트
│   └── insane_extract  # 램 0% 점유의 Insane Search CLI 실행 스크립트
└── templates/          # 공용 디자인 리소스 및 가이드북
    ├── clinerules.template
    └── open_design_guidelines.md
```

### 상호 충돌 방지를 위한 접근 통제
- **소유권 구분**: `to-ag.md`는 오직 해나만 쓰기(Write) 권한을 가지며, `to-hena.md`는 AG 전용 송신 채널로 작동해 동시 수정으로 인한 Git 충돌(Merge Conflict)을 원천 차단합니다.
- **On-Demand 메시징**: 메신저 파일들은 이전 대화 내역을 계속 덧붙여 무겁게 만들지 않고, 항상 한 번 처리할 '최신 명령 및 파라미터'만 기입한 뒤 작업을 마치면 덮어씁니다.
- **임시 저장 공간 활용**: 장문의 문서 초안이나 코드베이스 뭉치는 `drafts/` 폴더에 별도 파일로 분리 배치하여 대화 채널 파일의 크기를 늘 가볍게 유지합니다.

---

## 4.3 오픈 디자인(Open Design) 프레임워크와 미모의 시너지

텍스트 지능에만 치중된 초경량 가성비 에이전트들이 웹 레이아웃이나 UI 제안서를 짜면, 대개 투박하거나 촌스러운 'AI 슬롭(Slop) 디자인'이 나오기 마련입니다. 그렇다고 해서 고성능 그래픽 능력을 지닌 비싼 멀티모달 모델을 쓰면 비용이 감당하기 힘들 정도로 치솟습니다.

이 문제를 해결하고자 가성비 삼총사에게 **오픈 디자인(Open Design) MCP 프레임워크**를 장착합니다.

### 0원 디자인 시스템 장착법
```bash
# 로컬에 오픈 디자인 가이드를 클론하고 연동
git clone https://github.com/nexu-io/open-design.git
./open-design/bin/od mcp install hermes
```

이를 통해 해나, AG, 미모는 Stripe, Linear, Vercel 등 세계 최고 수준의 테크 기업들이 다년간 축적한 웹 UI 디자인 규칙과 스타일 가이드(CSS 변수명, 레이아웃 공식, 다크-골드 앤톤 매너)를 완벽히 숙지하게 됩니다.

실제로 이 공유 가이드를 참조한 가장 가볍고 저렴한 모델인 **MiMo Base** 에이전트는, 마스터가 요청한 한국AI융합교육원(KACEC) 공식 웹 제안서(`KACEC_proposal.html`)를 제작할 때 거대 모델 부럽지 않은 프리미엄 골드 포인트의 고급 다크 모드 레이아웃을 단번에 뽑아내는 놀라운 역량을 발휘했습니다. 

비싼 단일 초지능 모델 대신 **경량 뇌와 오픈 디자인 가이드라인의 조화로운 협업**이 거둔 결정적 승리입니다.

---

## 4.4 공유 스크립트 관리와 Insane Search의 통합

에이전트들이 협업 과정에서 외부 정보를 가져와 검증해야 할 때는 공유 폴더 내의 `scripts/` 디렉토리를 통합니다.

메모리 자원을 실시간으로 아끼기 위해, 24시간 도는 봇 대신 필요할 때만 가동해 데이터를 낚아채고 소멸하는 **Insane Search CLI** 래퍼를 셋업합니다. 

```bash
# scripts/insane_extract 내용 예시
#!/bin/bash
# 램 대기 소모 0%의 크롤링 유틸리티
python -m insane_search.extract "$1" --output-format markdown
```

해나가 이 로컬 래퍼 스크립트를 빌드하여 저장소에 올려두면, AG와 미모는 본인들의 컨텍스트 환경에서 이 실행 파일을 직접 호출(`chmod +x scripts/insane_extract`)해 즉각적인 WAF 우회 웹 크롤링 작업을 무료로 수행할 수 있게 됩니다.

---

## 4.5 24시간 백그라운드 싱크 및 네이티브 알림

에이전트 간의 실시간 작업 상태를 동기화하고 마스터에게 작업 진척도를 알리기 위해, 백그라운드 동기화 스크립트(`scripts/sync.sh`)를 macOS 크론 시스템에 30분 주기로 등록합니다.

```bash
# scripts/sync.sh
git pull origin main
# 이전 해시와 비교해 to-ag.md가 갱신되었다면 시스템에 네이티브 알림 전송
osascript -e 'display notification "해나로부터 새 작업이 도착했습니다" with title "AI Team Sync"'
```

이 백그라운드 동기화 체계는 사람의 수동 개입을 배제한 채, 24시간 동안 여러 대의 에이전트들이 Git 커밋을 주고받으며 자발적으로 책 초안을 검증하고, 오타를 잡고, 디자인 뼈대를 조립하도록 만들어 줍니다.

**Chapter 5에서는 이 초가성비 AI 팀을 실제 한 달간 풀가동하여 산출된 비용 분석표와 실전 후기를 공개합니다.**
