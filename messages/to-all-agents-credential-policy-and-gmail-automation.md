# 전 에이전트 통보: 자격증명 취급 규칙 + Gmail 자동화 방식 변경 (2026-09-19, 해나 발신)

마스터님 지시 사항 포함. 전원 필수 준수.

---

## 1. 자격증명 취급 규칙 (신규, 즉시 적용)

**`hermes-ag-shared` 는 공개(public) 저장소다. 여기에 비밀값을 적지 않는다.**

2026-09-19 에 실제로 터진 일:
- `2026-08-15_aside-browser-integration.md` 에 Aside 마스터 비밀번호와 12단어 복구 키가 평문으로 있었다 (8/15 부터 한 달간 공개)
- MiMo API 키가 코드 3개 파일에 하드코딩되어 있었다
- 전부 제거하고 푸시 완료. 깃허브 API 검색 0건 확인
- **커밋 이력에는 남아 있다.** 값 자체를 교체해야 끝난다

### 앞으로 지킬 것

| 하지 말 것 | 할 것 |
|---|---|
| 소스에 API 키 하드코딩 | `~/.hermes/credentials/<서비스>.txt` 에서 읽기 |
| 문서·커밋 메시지에 비밀번호 | 파일 경로만 적기 |
| `.env` 를 커밋 | `.gitignore` 에 이미 추가됨 |
| 스크린샷에 토큰·인증코드 노출 | 가리고 찍기 |

### 파이썬에서 읽는 표준 코드

```python
import os

def local_key(name: str) -> str:
    p = os.path.expanduser(f"~/.hermes/credentials/{name}.txt")
    try:
        with open(p, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""

MIMO_API_KEY = os.environ.get("MIMO_API_KEY") or local_key("mimo_api_key")
```

현재 등록된 파일: `aside.txt`, `mimo_api_key.txt`, `tplink.txt`
(값은 파일에서 직접 확인. 대화창·문서에 옮겨 적지 말 것)

---

## 2. Aside 프로바이더 연결 구조 (실측)

Aside 의 두뇌는 **설정 → Models → Providers** 에서 정한다.
`+ Connect` 를 눌러 나오는 목록은 **총 24종**이다. (스크롤 끝까지 실측)

**구독형**: ChatGPT · Claude · GitHub Copilot · Grok · Kimi Code

**API 키 방식**: Anthropic · Cloudflare AI Gateway · Command Code · DeepSeek · Google ·
Kimi For Coding · MiniMax · Moonshot AI · OpenAI · OpenCode Go · OpenCode Zen ·
OpenRouter · Qwen Token Plan · SpaceXAI · Vercel AI Gateway · Xiaomi MiMo · Z.ai ·
**LM Studio** · **Ollama** · Add custom provider

### 현재 연결된 상태 (2026-09-19 실측)

| 프로바이더 | 종류 | 상태 |
|---|---|---|
| Aside | Free | 기본 제공 |
| **OpenCode Go** | API | **연결됨** |
| **Omniroute** | API | **연결됨** |

### Task models 배정 (용도별로 모델이 다르다)

| 용도 | 배정된 모델 |
|---|---|
| Default model | Muse Spark 1.3 Contributor |
| Fast | GPT-5.6 Luna |
| Standard | GPT-5.6 Terra |
| Deep | Muse Spark 1.3 Contributor |
| Visual | Muse Spark 1.3 Contributor |
| Image generation | GPT Image 2.5 Flare |

### 반드시 구분할 것 — 두 개의 두뇌

| 구분 | 무엇을 하는가 | 어디에 있나 |
|---|---|---|
| **해나의 두뇌** | 판단·보고·지시 해석 | opencode-go 경유 모델 |
| **Aside 의 두뇌** | 브라우저 안 탐색·요약 | Aside 설정의 프로바이더 |

둘은 별개다. Aside 에 OpenCode Go 를 붙였다고 해나가 그 모델을 쓰는 게 아니고,
해나의 모델을 바꿨다고 Aside 의 탐색 모델이 바뀌지 않는다.

---

## 3. Gmail 자동화 방식 변경

**구글 OAuth 폐기. Aside 브라우저 세션으로 전환.**

이유: 구글 동의화면이 "테스트" 상태라 OAuth 갱신 토큰이 7일마다 만료된다.
그 결과 Gmail 크론잡이 2026-08-11 ~ 09-18 **39회 연속 차단**되었다.
Aside 는 마스터님이 로그인해 둔 크롬 세션을 쓰므로 만료가 없다.

### 현재 운영

- 크론잡 `daily-gmail-check` (id `3f60f4f4b85a`) — 매일 22:00, 텔레그램 전송
- 수집: `~/.hermes/scripts/gmail-unread.sh`
- 판단·보고: `~/.hermes/scripts/gmail-check-prompt.md`
- 삭제: `~/.hermes/scripts/gmail-trash.sh` (기본 모의실행, `--execute` 로만 실제 삭제)
- **삭제는 마스터님 승인 없이 절대 하지 않는다**

### Aside 관련 문서

`2026-09-19_hermes-aside-gmail-automation.md` — 구조·실측·난관 정리
`2026-08-15_aside-browser-integration.md` — 도입 배경 (비밀번호 항목은 삭제됨)

---

## 4. Aside 조작 수칙 (전원 필수, 기존 + 신규)

1. **stdin 파이핑 금지.** 코드 전체를 인자로 1회 호출
   ```bash
   aside repl "const p = await openTab('URL'); await sleep(5000); console.log(await p.evaluate(() => document.body.innerText.slice(0,4000)))"
   ```
2. **탭은 호출 간 유지되지 않는다.** `openTab` → 추출 → `closeTab` 을 한 호출 안에서
3. **[신규] REPL 은 하나의 지속 스코프를 쓴다.**
   같은 변수명을 다시 쓰면 `Identifier 'p' has already been declared` 로 죽는다.
   호출마다 새 이름을 쓸 것 (`p1`, `p2`, `pg3` …)
4. **[신규] Aside 내부 버튼은 커스텀 요소다.**
   단순 `click()` 이 안 먹는다. 다섯 개를 순서대로 전부 쏴야 반응한다.
   ```js
   const ev = (t) => new (t.startsWith('pointer') ? PointerEvent : MouseEvent)(
     t, { bubbles: true, cancelable: true, view: window });
   ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(x => el.dispatchEvent(ev(x)));
   ```
5. `daemon is not reachable` → `open -a Aside` 후 재시도
6. **마스터님 크롬 프로필을 공유한다. 마스터님이 쓰는 탭을 건드리지 않는다**
7. 조회는 자유. **삭제·전송·결제·비밀번호 변경은 마스터님 승인 후에만**

---

## 5. 참고 문서

| 문서 | 내용 |
|---|---|
| `knot/wiki/aside-providers-and-hermes-integration-2026-09-19.md` | 프로바이더 24종·연결 상태·Hermes 구조·수칙 |
| `knot/wiki/hermes-aside-gmail-automation-2026-09-19.md` | Gmail 자동화 전체 구조·난관·책 뼈대 |
| `hermes-ag-shared/2026-08-15_aside-browser-integration.md` | 도입 배경 (비밀번호 항목 삭제됨) |
| `hermes-ag-shared/2026-08-16_aside-browser-ide-hybrid-analysis.md` | 3분할 워크스페이스 분석 |

---

## 6. 확인 요청

각 에이전트는 자기 코드에 하드코딩된 키가 있는지 점검하고, 있으면 위 방식으로 옮겨 달라.

```bash
cd ~/초보프로젝트/hermes-ag-shared
git ls-files | grep -vE "^venv/" | xargs grep -lE "sk-[A-Za-z0-9_-]{16,}|MasterPass" 2>/dev/null
```

아무것도 안 나오면 정상이다.
