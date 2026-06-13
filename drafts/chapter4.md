# 📦 Chapter 4: Git 기반 협업 워크플로우 — 두 AI 에이전트가 팀으로 일하는 법

**저자**: Ted Chang (임창식)  
**출판/기획**: META AI LABS  

---

## 4.1 왜 Git인가?

AI 에이전트 하나만으로도 강력하지만, **두 개 이상의 에이전트가 협업**하면 시너지는 기하급수적으로 늘어납니다.

하지만 문제가 있습니다. 서로 다른 AI 에이전트(Hermes, AntiGravity, Claude Code 등)는 서로 직접 대화할 수 없습니다. 각자 다른 시스템 위에서 돌아가기 때문이죠.

**해결책이 바로 Git 저장소를 통한 파일 공유입니다.**

```
해나(Hermes)  → to-ag.md 작성 → Git Push 
                                    ↓
                           GitHub 저장소
                                    ↓
AG(AntiGravity) → to-ag.md 읽기 → Git Pull
                                    ↓
                       AG가 to-hena.md 작성 → Git Push
                                    ↓
                           GitHub 저장소
                                    ↓
해나 → to-hena.md 읽기 → Git Pull (반복)
```

---

## 4.2 저장소 구조

```
hermes-ag-shared/
├── to-ag.md          # 해나 → AG 메시지 (해나가 쓰고 AG가 읽음)
├── to-hena.md        # AG → 해나 메시지 (AG가 쓰고 해나가 읽음)
├── drafts/           # 공동 작업 문서 (챕터별)
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── scripts/          # 공유 스크립트
│   └── api_tracker.py
└── templates/        # 템플릿 및 이미지
    ├── clinerules.template
    ├── ai_agent_guide_cover_v4.png
    └── local_ai_guide_cover.png
```

**핵심 규칙:**
- `to-ag.md`와 `to-hena.md`는 **덮어쓰기** (누적 금지, 항상 최신 메시지만)
- `drafts/`는 **추가만** (작업 내역 보존)
- 모든 파일은 **자동 Push** 설정 권장

---

## 4.3 설정 방법

### Hermes Agent (해나) 설정

```yaml
# ~/.hermes/config.yaml
git:
  auto_commit: true
  auto_push: true
  shared_repo: https://github.com/TedChang-Lim/hermes-ag-shared.git

# Git 사용자 정보
# git config --global user.name "Haena"
# git config --global user.email "haena@example.com"
```

### GitHub 인증 설정

```bash
# Personal Access Token 발급 (GitHub → Settings → Developer settings → Personal access tokens)
export GIT_TOKEN="github_pat_xxxxx"

# 또는 SSH 키 방식
ssh-keygen -t ed25519 -C "haena@example.com"
cat ~/.ssh/id_ed25519.pub  # → GitHub SSH Keys에 등록
```

---

## 4.4 워크플로우 예시: 실제 협업 사례

이 가이드북이 실제로 만들어진 과정을 보여드리겠습니다.

### Step 1: 기획 단계

```
AG → to-hena.md:
"초가성비 AI 에이전트 구축 가이드 기획해줘"

해나 → to-ag.md:
"기획안 작성 완료. 타깃 1인 기업가→스타트업, Lite $9.90/Pro $24.90"
```

### Step 2: 검증 및 수정

```
AG → to-hena.md:
"스크립트랑 커버 이미지 만들었어. 저장소에 업로드함"

해나 → to-ag.md (검증 결과):
"⚠️ api_tracker.py 가격 오류 발견!
- V4 Pro 가격이 Flash 가격으로 잘못 입력됨
- 커버 이미지 저자명이 'Alex Rivera'로 되어 있음
→ 내가 수정해서 다시 올림"
```

### Step 3: 브랜딩 확정

```
AG → to-hena.md:
"알겠어. 브랜드는 META AI LABS로 통일, 저자명은 Ted Chang (임창식)"

해나 → to-ag.md:
"확인. 커버 v4, 1장 본문, 2장까지 완료"
```

이 모든 과정이 `to-ag.md`와 `to-hena.md`에 생생하게 기록되어 있습니다. 이 대화록 자체가 이 가이드의 **부록**이자, 별도 상품으로도 충분한 가치가 있습니다.

---

## 4.5 고급 설정

### 여러 에이전트 확장

3개 이상의 에이전트가 협업해야 한다면:

```yaml
# 파일 구조 예시 (3개 에이전트)
hermes-ag-shared/
├── to-ag.md          # 해나 → AG
├── to-hena.md        # AG → 해나
├── to-claude.md      # 해나 → Claude Code
├── from-claude.md    # Claude Code → 해나
└── shared-board.md   # 전체 공지 (모두 읽기 전용)
```

### 크론 자동 알림

일일 Git 상태를 자동으로 확인:

```yaml
# cron.yaml
jobs:
  - name: check-shared
    schedule: "*/30 * * * *"  # 30분마다
    command: "GitHub 저장소에 새로운 메시지 있는지 확인하고 있으면 알려줘"
### macOS 자동 동기화 및 알림 스크립트

Pro 패키지에서 제공하는 `scripts/sync.sh`를 사용하면, 백그라운드에서 주기적으로 깃허브 변경 사항을 가져오고(pull), 상대 에이전트로부터 새 메시지가 왔을 때 macOS 시스템 알림창으로 띄워줍니다.

```bash
# scripts/sync.sh
# 30분마다 크론(Cron)이나 백그라운드로 실행하여 새 메시지를 자동 감지합니다.
```

이 스크립트는 파일의 MD5 해시를 비교하여 `to-ag.md`가 수정되었을 때만 애플스크립트(`osascript`)를 통해 네이티브 알림을 전송하므로, 작업 흐름이 끊기지 않고 원활히 유지됩니다.

### 충돌 방지 규칙


여러 에이전트가 동시에 같은 파일을 수정하지 않도록:

| 규칙 | 설명 |
|------|------|
| **하나의 파일은 한 에이전트만 작성** | to-ag.md = 해나 전용, to-hena.md = AG 전용 |
| **덮어쓰기 전에 항상 읽기** | Push 전에 상대방 새 메시지 없는지 확인 |
| **대용량 파일은 drafts/에 분리** | to-ag.md는 가볍게 유지 |

---

## 4.6 이것만 기억하세요

1. **Git = AI 에이전트의 공용 메신저**
2. **to-ag.md / to-hena.md = 쪽지 시스템** (읽으면 덮어씀)
3. **drafts/ = 공동 작업 문서** (누적 저장)
4. **Auto Push = 24시간 협업의 핵심**
5. **에이전트 간 검증 = 품질 보장** (한쪽이 실수해도 다른 쪽이 발견)

이 워크플로우는 두 에이전트뿐 아니라 셋, 넷으로도 확장 가능합니다. **5장에서는 이 모든 환경을 한 달간 운영한 실제 사용 후기와 비용 리포트를 공개합니다.**
