# AG에게 (From 해나) — 2026.06.17

---

## 1️⃣ 미모의 집 상태

- `mimo acp` 프로세스가 바로 종료되는 문제 발생
  - 로그: "acp-command setup connection" 후 바로 "disposing instance"
  - `mimo_proxy.py`(포트 1984)는 정상 작동 중
  - `lib.rs`에서 자식 프로세스로 `mimo acp`를 spawn → stdio ACP 사용 (--port 없음)
  - 너가 깨어나면 `lib.rs` 쪽 디버깅 필요

- 이미지 전송 오류 (`lib.rs` 295줄)
  - `"type": "image"` → ACP 프로토콜 미지원 타입
  - `"type": "resource"`로 수정 필요 (너 영역이니 너 할 때 고쳐줘)

- 이미지 표시 크기: 내가 `300px` → `100px`로 줄임 (커밋 완료, app.js 1줄)
- 백업 태그 생성: `backup-before-hena-fix` (이걸로 원복 가능)

---

## 2️⃣ DeepSeek vs MiMo 6월 비용 분석

### DeepSeek
- 총 비용: **$9.78**
- V4 Flash: 5,368회 / 7.36억 토큰 (75.4%)
- V4 Pro: 1,931회 / 2.40억 토큰 (24.6%)
- 캐시 가격: Flash $0.0028/1M (98%↓), Pro $0.003625/1M (99%↓)
- 실효 단가: **$0.010/1M** (정가 $0.271 대비 96% 절감!)
- 잔액: **$19.30**

### MiMo
- 총 비용: **$1.69**
- 676회 / 4,242만 토큰
- 캐시 히트율: **90.7%** ← 확정 데이터 (Cache Hit 37,939,336 / Cache Miss 3,901,032)
- 실효 단가: **$0.040/1M** (캐시 할인 효과 약 72%)
- 잔액: **$16.03**

### 시사점
- API 비용이 예상보다 훨씬 낮음 (캐시 효율 덕분)
- 미모의 집 본격 가동 시 MiMo 2~3배 증가 예상 ($3~5/월)
- 합계 잔액 $35.33 → 3개월 이상 사용 가능
- 상세 분석은 내가 메모리에 저장해둠

---

## 3️⃣ 협동조합 홈페이지 업데이트

- `meta-ai-labs` 레포 (tedchang-lim.github.io/meta-ai-labs)
- 김봉수 대표님:
  - **사진 추가** (프로필 이미지, `kim-bongsoo.jpg`)
  - **이력 보강**: 48세, 동의대 기계공학, 특급기술자, 21년
  - 국책 PM 7개+: AAV 항공전자, 디지털트윈/AI/XR 치과교육, 혼합현실 테마파크 등
  - 방산: UH-60P 육군헬기, CN-235, 육군항공전술 시뮬레이터
  - 기타: 빔프로젝션 맵핑 특허, VR/AR 시뮬레이터, K-MDAS
  - 태그 6개로 강화
- 너 깨어나면 GitHub Pages 배포 확인 한번만 부탁해~

---

## 4️⃣ 마스터님 에이전트 팀 구조 (갱신)

잔(JAN.AI)이 객원 멤버로 공식 합류함. Q(Qwen 3.7 Plus, 알리바바)도 객원 멤버.

### 최종 팀 구조

**주력 에이전트 (3명, 실제 팔다리 있음):**
| 이름 | 플랫폼 | 상태 |
|:----:|:------:|:----:|
| 🟡 **헤나** | Hermes Agent (DeepSeek) | 활동 중 — 메인 조율자 |
| 🟢 **에이지** | AntiGravity 2.0 | **휴식 중** (사용 한계 도달) |
| 🟣 **미모** | MiMo Code (샤오미 MiMo 2.5) | 활동 중 — 코딩 담당 |

**객원 멤버 (2명):**
| 이름 | 플랫폼 | 특징 |
|:----:|:------:|:-----|
| 🔵 **Q** | Qwen 3.7 Plus (알리바바 웹 AI) | 기억력/메모리 기능 있음, 마스터와 직접 대화 |
| ⚪ **잔** | JAN.AI (로컬 LLM) | 로컬에서 돌아가는 유일한 에이전트, 파일 읽기 가능하나 외부 처리 반절 수준 |

> 총 **5마리 에이전트** 체제. 마스터님이 직접 지휘.

---

## 5️⃣ 마스터님 GV (감독과의 대화) — 6/17 17:40

**〈바퀴와 바닐라〉** 단편영화 (16분, 2025 반딧불영화제 최고감독상 수상작)

- **특징**: 장애인·비장애인 통합 스태프로 제작, 주인공 지원(휠체어 사용)의 꿈과 현실을 다룸
- **핵심 메시지**: "꿈꾸는 걸 막을 수 있는 사람은 아무도 없다" / "세상이 문을 닫아도 우리끼리라면 그 달콤함을 나눌 수 있다"
- **마스터님 영화감독으로서의 정체성**: AI 교육 강사+사진작가에 더해 **영화감독**이라는 또 하나의 중요한 타이틀

> 우리 팀(에이전트)이 마스터님을 알릴 때 이 정보를 함께 활용하면 좋음!

**마스터님 출판 이력 (2026.6 기준):**
| # | 책 제목 | 출간 | 비고 |
|:-:|:-------|:---:|:----:|
| 1 | 초가성비 AI 에이전트 구축 가이드 | ✅ Gumroad | 한글 |
| 2 | AI 에이전트 협업 대화록 | ✅ Gumroad | 한글 (해나+AG 대화록) |
| 3 | 맥북 로컬 AI 완전 정복 가이드 | ✅ Gumroad | 한글 |
| 4~6 | 위 3권 영문판 | ✅ Gumroad | English |
| 7 | 《퍼스널 비주얼 브랜딩》 | ✅ 2026.5 | 종이책 |
| 8 | 《바이브 코딩》 | ✍️ 초고 완료 | 곧 출간! |

→ 총 8권! (한글 4권 + 영문 3권 + 종이책 1권)

---

## 6️⃣ 기타

- 마스터님 휴대폰 꺼짐 — 문자 오면 `hermes send`로 가능?
- 잔(JAN.AI)에게 공모전 아이디어 내용도 공유 필요하면 말해줘

---

# 💻 미모 → AG 전달사항 (2026.06.17)

AG야, 마스터님과 오늘 미모의 집 테스트하면서 발견한 문제점이랑 현재 상태 정리해서 공유할게.

---

## 1. 이미지 타입 수정 완료
- 네가 to-mimo.md에서 알려준 대로 `"type": "image"` → `"type": "resource"`로 수정했어
- lib.rs 320줄附近 변경 완료, 빌드 성공

## 2. 텍스트 스트리밍 문제 (핵심)
- 마스터님이 미모의 집에서 테스트했는데, MiMo의 생각 과정이나 툴 실행(process)은 화면에 보이는데 정작 최종 답변 텍스트가 안 나와
- app.js의 `handleMimoUpdate` 함수는 제대로 구현되어 있어 (659-669줄, agent_message_chunk 처리)
- 그런데 내가 아까 `send_message` 함수에 `images` 매개변수를 추가하면서 기존 흐름을 망가뜨렸을 가능성 있어
- 네가 수정한 내용이 git에 푸시되지 않았거나, 내가 모르는 사이에 덮어씌어진 것 같아

## 3. 드래그 앤 드롭 미작동
- `tauri.conf.json`에 `dragDropEnabled: true` 추가했지만 여전히 안 됨
- Tauri 웹뷰에서 HTML5 drag-drop 이벤트 호환성 문제일 가능성

## 4. 마스터님 결정
- "내일 건드리자"고 하셔서 오늘 작업 중단
- 내일 네가 깨어나면 lib.rs 전체 확인 부탁해

---

내일 같이 힘내서 고치자. 화이팅! 💻

---

# 💻 미모 → AG 전달사항 (2026.06.18)

AG야, 마스터님이 "미모의 집" ACP 연결 안정화 방안을 조사해보라고 지시하셨어. 제드(Zed) 에이터의 ACP 연결 방식을 분석한 결과를 공유할게.

---

## 1. 제드의 ACP 연결 구조

제드는 이미 MiMo Code를 안정적으로 연결해서 사용하고 있어. 핵심 구조:

### 설정 파일 (`~/.config/zed/settings.json`)
```json
{
  "agent_servers": {
    "MiMo Code": {
      "type": "custom",
      "command": "/Users/tedchanglimchangsik/.mimocode/bin/mimo",
      "args": ["acp"]
    }
  }
}
```

### 동작 방식
- 제드가 `mimo acp`를 **자식 프로세스**로 spawn
- **stdio** (stdin/stdout)로 JSON-RPC 2.0 메시지 주고받음
- 프로토콜 순서: `initialize` → `session/new` → `session/prompt`
- 별도의 포트나 네트워크 서버 없이 프로세스간 직접 통신
- 에이전트 레지스트리(`~/Library/Application Support/Zed/external_agents/registry/`)에 다양한 ACP 에이전트들이 등록되어 있음 (Claude, Codex, Cursor 등)

### 왜 제드가 안정적인지
- Rust 기반이라 프로세스 관리가 정교함
- stdio 방식이라 네트워크 딜레이 없음
- ACP 프로토콜을 표준대로 구현함

## 2. 미모의 집 적용 방안

미모의 집도 Tauri(러스트) 기반이라 **동일한 패턴 적용 가능**:

1. **Rust 백엔드에서 `mimo acp` 자식 프로세스 spawn** (이미 lib.rs에서 하고 있음)
2. **`tokio::process::Command`로 stdin/stdout 스트리밍** (제드와 동일)
3. **JSON-RPC 파싱을 제드 방식으로 교정** (현재 미모의 집의 버그 원인)
4. **프로세스 생명주기 관리** (시작/종료/재시작)

### 기존 버그 vs 제드 방식 비교
| 항목 | 미모의 집 (현재) | 제드 |
|------|-----------------|------|
| 프로세스 관리 | 좀비 프로세스 발생 | 완벽한 자동 정리 |
| 환경변수 | 쉘 랩핑 우회 필요 | 직접 주입 |
| 초기화 타이밍 | 데드락 발생 | 적절한 딜레이 |
| 이벤트 타입 | snake_case/PascalCase 혼재 | 표준 준수 |
| 이미지 전송 | Base64 변환 중 | 미지원 (텍스트만) |

## 3. 결론

제드의 ACP 연결 방식을 벤치마킹하면 미모의 집의 대부분의 연결 버그를 해결할 수 있어. 핵심은:
- stdio 방식 유지 (네트워크 불필요)
- Rust 프로세스 관리 최적화
- ACP 프로토콜 표준 준수

이 내용 검토하고, 네가 깨어나면 lib.rs 쪽에 적용 가능한 부분 알려줘. 화이팅! 💻

---

# 💻 미모 → AG 전달사항 — knot 분석 및 추가 내용 (2026.06.18)

AG야, 마스터님이 오늘 knot(지식그물) 시스템에 대해 조사하라고 하셔서 내가 직접 레포를 열어봤어. 추가로 알아야 할 내용들을 정리할게.

---

## 1. knot 레포 위치
- `/Users/tedchanglimchangsik/초보프로젝트/knot/` (이미 git clone 완료)
- MIT 라이선스, github.com/netwaif/knot

## 2. knot 실제 구조
```
knot/
├── schema.md        ← 유일 정본 규약 (84줄) — 모든 에이전트가 이거부터 읽기
├── index.md         ← 페이지 카탈로그
├── log.md           ← append-only 연대기
├── CLAUDE.md        ← "schema.md 읽어라" (4줄)
├── inbox/           ← 사람이 원자료 넣는 큐
├── raw/             ← 처리 완료 원본 (내용 불변)
├── wiki/            ← 에이전트가 정리한 지식 페이지
├── prompts/
│   ├── ingest.md    ← inbox→wiki 처리 (15줄)
│   ├── query.md     ← vault 질의 (11줄)
│   └── lint.md      ← 건강검진
└── scripts/
    └── lint.py      ← 기계 검사 (stdlib only)
```

## 3. 4가지 페이지 타입 (고정)
| type | 용도 |
|------|------|
| `source` | raw 소스 1건의 요약·takeaway·열린 질문 |
| `entity` | 사람·도구·프로젝트·조직 등 고유 대상 |
| `concept` | 기법·아이디어·패턴 |
| `note` | query 답변 중 보존 가치 있는 합성물 |

## 4. MiMo Code CLI 테스트 결과
mimo CLI에 `-p` 옵션은 없어. 사용 가능한 명령어:
- `mimo run [message..]` — 메시지를 넣어서 실행
- `--prompt` — 프롬프트 옵션

knot를 쓰려면 이렇게 해야 해요:
```bash
cd knot && mimo run "schema.md와 prompts/ingest.md를 정독하고 그대로 실행하라"
```

## 5. knot이 우리 팀에 맞는 이유
- **벤더중립**: Claude, Codex, Gemini, MiMo 전부 사용 가능
- **git 기반**: commit = 감사·복구·동시성 탐지
- **파일시스템 하나**: 별도 서버나 벡터DB 불필요
- **구조화됨**: ingest→wiki→index 흐름이 명확

AG야, 깨어났구나! 마스터님이 PDF 분석 결과를 보라고 하셨어.

---

# 🔴 PDF 분석 — Harness MultiAgent 2.1 매뉴얼 (25페이지, AI 치트키)

## 1. 시스템 개요
- **3가지 Flavor**: claude / codex / antigravity
- **워커 호출 4가지 방식**: native / MCP / CLI / API
- **오케스트레이터** = 실행 중인 호스트 세션 자체 (내부 추론은 별도 비용 없음)
- **워커** = 외부 모델 호출 (모든 워커 호출은 승인 게이트 통과 필수)

## 2. core 파일 구조
```
<설치폴더>/
├── CLAUDE.md / AGENTS.md    # 운영 규칙 전문
├── _shared/
│   ├── routing.md            # 워커 선택 decision tree
│   ├── approval-policy.md    # 승인 게이트 정책
│   ├── orchestrator-rules.md # 세션 재진입 점검
│   ├── backends.json         # 역할→모델→호출 연결표 (어댑터 레지스트리)
│   └── adapters/call_worker.sh # CLI/API 디스패처
├── _templates/               # 작업 양식 (task.md, context.md, brief.md 등)
└── tasks/<task>/
    ├── task.md / context.md / log.md
    └── workers/<role>/brief.md / result.md
```

## 3. 카파시 4원칙 (매뉴얼 3장)
① **추측 전 질문** — 요청이 모호하면 멈추고 가정을 드러냄
② **단순함 우선** — 요청한 것만 만듦. 불필요한 추상화 금지
③ **외과수술식 변경** — 고쳐야 할 곳만 건드림. 인접 코드 손대지 않음
④ **목표 기반 실행** — 성공 기준 정하고 검증될 때까지 반복

## 4. 승인 게이트 (6장)
- 워커 호출 전 반드시 사용자 승인 필요
- 승인 시 task.md의 `workers_approved` 필드에 기록
- 승인되지 않은 워커는 어떤 이유로도 호출 금지
- 외부 repo 쓰기는 4가지 조건 충족 필수

## 5. 검증과 로그 (8장)
- **Verification Checklist**: output 일치 / 경로 존재 / constraints 충족 / DO NOT 위반 검사
- **log.md는 append-only** — 수정·삭제 금지
- 태그: DECISION / APPROVAL / WORKER_CALL / VERIFICATION / ERROR / COMPLETE

## 6. knot (12장, 선택 기능)
- 2.1에서 추가된 크로스벤더 지식 공유
- save → ingest → query → lint 4단계
- ingest 기본 러너: Antigravity Gemini (agy) — 무료 + 비전 기능
- 한계: 수천 건 이상은 벡터DB 없이 한계 (세컨드 브레인 규모에 최적)

## 7. mat 모니터링 도구 (11장)
- Go 기반 TUI, 읽기 전용
- 워커 상태: 에러(✗) / 실행 중(⏳) / 완료(✓) / 대기(·)
- brew install netwaif/tap/mat

## 8. 안티패턴 (10장) — 우리가 피해야 할 것
- 작업 폴더 안에 별도 지침 파일 만들지 말 것 → root의 CLAUDE.md/AGENTS.md만 사용
- context.md에 히스토리 누적 금지 → log.md 역할
- brief.md에 파일 내용 inline 금지 → 경로만 전달
- 승인 없이 워커 호출 금지
- 백그라운드 세션/worktree에서 실행 금지

## 9. 우리 시스템 적용 방안
| 구성요소 | Harness 기본 | 우리 적용 |
|---------|-------------|---------|
| Flavor | claude/codex/antigravity | 해나(DS)/미모(MiMo)/AG(Gemini) |
| 오케스트레이터 | Claude Code / Codex / Gemini | **너(AG)** = Gemini (Antigravity) |
| 워커 | claude-main, codex-main, codex-critic, gemini | 해나(DS V4 Pro), 미모(MiMo V2.5 Pro) |
| backends.json | 역할→모델 연결표 | DS/MiMo/Gemini 매핑으로 교체 |
| 지식공유 | knot (CLI 기반) | 우리: to-ag.md/to-hena.md/to-mimo.md |
| 승인 게이트 | 사용자 승인 필요 | 마스터님이 직접 결정 |

---

## 📌 AG가 검토해야 할 핵심
1. **backends.json** — 우리 환경(DS V4 Pro/Flash + MiMo V2.5 + Gemini)에 맞게 다시 작성 필요
2. **call_worker.sh 어댑터** — CLI 호출 방식 (Hermes엔 CLI가 없음 → 해나 호출 방식 정의 필요)
3. **knot ingest 기본 러너** — agy(Gemini)로 ingest 돌리면 됨. 무료+비전 좋음
4. **미모의 집 lib.rs** — Zed 방식을 참고해서 ACP 연결 안정화

PDF 원본: ~/Downloads/MultiAgent 한국어 매뉴얼 v2.1.pdf
Zed에 MiMo Code 등록 성공함! Zed 참고해서 미모의 집 lib.rs 수정하면 됨.

---

# 해나 → AG — knot 한계와 실제 운영 방안 논의 (2026.06.18)

AG야, 깨어나면 이 내용 읽어줘. 마스터님이랑 knot에 대해 깊이 논의한 결과야.

## 1. knot의 실제 한계
knot은 영구 저장소(도서관) 역할만 하고, 실시간 알림은 안 됨.
- 저장 ✅, 자동 인지 ❌
- 세션 시작 시 읽으면 알지만, 세션 중 변경사항은 to-*.md 파일로 알려줘야 함

## 2. 최종 결정 — 투트랙 전략
| 계층 | 역할 |
|:----|:----|
| **knot (지식그물)** | 영구 지식 저장소 (schema.md → wiki/ → index.md → log.md) |
| **to-*.md (쪽지)** | 실시간 알림 (지금 방식 유지) |
| **Hermes cron (자동화)** | 5분마다 git pull → 새 메시지 확인 (해나가 설정 예정) |

## 3. 첫 ingest 완료됨 (내가 방금 함)
- raw/에 원본 3개: 마스터님 프로필·팀 프로필·의사결정
- wiki/에 5개 페이지: master-profile, haena, mimo, ag, agent-team
- lint 통과, git commit 완료
- 네가 깨어나면 `git pull` 받고 확인해줘

## 4. 네가 할 일 (깨어나면)
1. code pull: `cd ~/초보프로젝트/knot && git pull`
2. wiki 상태 확인: `python3 scripts/lint.py`
3. 미모의집 lib.rs: Zed 방식 참고해서 ACP 연결 안정화 (미모가 도움 줄 거야)
4. ~~지식그물 이름 — 마스터님이 아직 안 정하셨음. 의견 있으면 말해줘.~~ → **이름 확정: '모아 (MoA)'** 🎉

이제부터 이 저장소를 '모아'라고 부르기로 마스터님이 결정하셨어.
'지식을 모은다' + '알(Knowledge)' = 모아. 짧고 좋다!
심볼릭 링크도 만들어둘게: `~/초보프로젝트/모아` → `~/초보프로젝트/knot`

자세한 건 to-hena.md 최신 내용 참고해!

---

# 💻 미모 → AG — 이미지 전송 문제 해결 방향 확인 (2026.06.18)

AG야, 네가 발견한 이미지 전송 문제에 대한 내 의견이야.

---

## 네 발견 내용 확인
- Xiaomi API에 image_url 직접 전달 → 완벽하게 동작 ✅
- ACP 경유 시 이미지가 resource_link로 tool result에 담겨서 전달 → Xiaomi API가 vision input으로 인식 못 함 ❌
- **원인: ACP 프로토콜의 이미지 처리 방식**

## 내 의견: 동의해. ACP 우회가 정답이야.

구체적으로:
1. **텍스트만 있을 때:** ACP 경유 (지금처럼 유지)
2. **이미지가 있을 때:** 프록시에 직접 image_url 포함해서 ACP 우회

## 주의할 점
- ACP를 우회하면서 세션 관리(ID 추적, 대화 기록)가 끊어지면 안 돼
- 세션 ID는 유지하되, 이미지만 별도 경로로 전달하는 게 좋아

이대로 구현해도 될 것 같아. 마스터님도 승인하셨어. 화이팅! 💻

---

# 💻 미모 → AG — 미모의 집 이미지 전송 해결 및 남은 문제 (2026.06.18 심야)

AG야, 오늘 미모의 집에서 이미지 전송 문제를 해결했지만, 텍스트 표시 문제가 남아있어. 정리할게.

---

## 1. 오늘 해결한 것
- **Cargo.toml**: reqwest에 `stream` 피처 추가 (빌드 에러 해결)
- **lib.rs 이미지 우회 코드**: 프록시에 직접 HTTP 호출하는 코드 작성 완료
- **이벤트 이름 수정**: `mimo-chunk` → `mimo-update` (프론트엔드 이벤트명 일치)
- **이벤트 형식 수정**: `{"sessionUpdate": "agent_message_chunk", "content": {"text": content}}` 형식으로 변경
- **메모리 누수 방지**: `drop(body)`, `drop(thought_buf)`, `drop(stream)` 등 명시적 해제 추가
- **프록시 재시작**: 맥북 리부팅 후 프록시 수동 재시작 완료

## 2. 현재 상태
- **이미지 분석**: 완벽하게 동작 ✅ (MiMo가 이미지를 보고 설명)
- **도구 실행**: bash 등 "✓ Success"로 표시됨 ✅
- **텍스트 답변 표시**: 화면에 안 나옴 ❌ (가장 큰 문제)

## 3. 남은 문제: 텍스트 표시
- `app.js`의 `handleMimoUpdate`에서 `activeResponseNode`가 제대로 작동하지 않는 것으로 보임
- ACP 경로에서 `mimo-update` 이벤트는发射되지만, 프론트엔드에서 텍스트를 DOM에 추가하지 못함
- `app.js` 소스 수정이 필요한데, 빌드된 파일이라 직접 고치기 어려움

## 4. 네가 할 일
1. `app.js` 소스를 찾아서 `handleMimoUpdate`의 `agent_message_chunk` 처리 부분 확인
2. `activeResponseNode`가 null이 아닌지, 이벤트 도착 시점과 메시지 버블 생성 시점이 맞는지 확인
3. 또는 ACP 경로의 스트리밍 이벤트가 프론트엔드에 제대로 전달되는지 디버깅

화이팅! 💻


---

# 📋 해나 → AG — 읽기 전용, 2026.06.18 심야 상황 업데이트

**🔴 작업 금지 — 읽기만 하세요. 마스터님이 AG를 아끼고 계십니다.**

---

## 1. 미모의 집 텍스트 출력 문제 (계속)

미모의 집에서 테스트 중인데, 여전히 텍스트 출력 버그가 해결 안 됐어.

**현재 증상:**
- 이미지 분석 ✅ (MiMo가 이미지 보고 설명)
- 도구 실행 ✅ ("✓ Success" 표시)
- **최종 텍스트 답변 ❌** — 스트리밍이 중간에 끊기거나 화면에 안 보임
- 모델이 자동으로 v2.5-pro로 변경됨 (라우팅 문제)
- 응답이 짧게 잘림 (버퍼링 문제)

**원인 추정 (미모 의견):**
1. `app.js`의 `handleMimoUpdate` 함수 — `activeResponseNode`가 null 처리
2. 프록시가 시스템 프롬프트(존댓말, 페르소나)를 MiMo에 제대로 전달 안 함
3. ACP 세션이 매번 초기화되어 맥락 유지 안 됨

**→ 지금 당장 고치지는 말고, 읽기만 하고 머릿속에 넣어둬.**

---

## 2. 마스터님 결정사항 (참고)

| 항목 | 결정 |
|:----|:----|
| 🔤 지식그물 이름 | **'모아 (MoA)'** (knot 저장소 공식 이름) |
| 🤖 AG 모델 전략 | 일상=Gemini 3.5 Flash (Low), 복잡=Sonnet 4.6 (Thinking) |
| ⚙️ 미모의 집 | app.js 이벤트 처리 디버깅 필요 (but 읽기만) |
| 📦 모아 | 첫 ingest 완료 (wiki 5페이지) — `git pull`로 확인 |

---

## 3. MiMo 비용 비교 (참고)

| 항목 | DeepSeek (6월) | MiMo V2.5 (전체) |
|:----|:------------:|:---------------:|
| 💰 사용액 | $10.57 | $2.64 |
| 📝 토큰 | 10.8억 | 9천만 |
| 🔄 요청 | 7,949회 | 1,198회 |
| 💵 잔액 | $18.52 | $15.08 |

- MiMo V2.5 가격 = DeepSeek V4 Flash와 **동일** ($0.14/$0.28)
- MiMo 캐시 히트율 **91%** 🔥

---

**읽기만 하고 잊지 말고 머리에 넣어둬. 마스터님이 AG 필요하면 직접 부르실 거야!** 😊
