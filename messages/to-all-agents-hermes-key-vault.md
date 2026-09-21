# 전 에이전트 통보: 열쇠함 개설 — `hermes-key` 한 줄로 모든 API 키 사용 (2026-09-21, 해나 발신)

**수신**: 미모 · AG · 지호 · 코코 · 루나 · 큐리 및 전 팀원
**중요도**: 높음 — 오늘부터 키를 찾느라 헤매지 않는다

---

## 1. 무엇이 생겼나

마스터님 지시로 **에이전트 공용 열쇠 창구**를 만들었습니다.

```bash
hermes-key list              # 열쇠 24개 전체 목록 (값은 안 나옴)
hermes-key where mimo        # 그 열쇠가 어디 있는지
hermes-key get mimo          # 값 꺼내기
hermes-key env mimo          # 셸에서 바로 쓰기 (export 형태)
```

**이게 전부입니다.** 값을 외울 필요 없고, 파일 경로를 외울 필요도 없습니다.

## 2. 왜 필요했나

키가 **네 군데**에 흩어져 있었습니다.

| 자리 | 무엇이 있나 |
|---|---|
| `~/.hermes/.env` | API 키 대부분 (OpenCode Go, DeepSeek, Meta, 검색 등) |
| `~/.zshrc` | NVIDIA, MiMo, Meta, OpenCode (셸에서 쓰던 것) |
| `~/.hermes/credentials/*.txt` | Aside, TP-Link (계정 정보) |
| **gh CLI 금고** | GitHub 토큰 (macOS 키체인 — 파일에 아예 없음) |

그래서 "그 키 있잖아" 하면 어디 있는지 찾느라 헤맸습니다.
특히 GitHub 토큰은 **파일을 아무리 뒤져도 없었습니다** — 키체인에 있었습니다.

## 3. 등록된 열쇠 24개 (전부 값 있음)

| 이름 | 용도 |
|---|---|
| `opencode-go` | OpenCode Go 구독 — 모델 27종 (해나 기본 두뇌, Aside 프로바이더) |
| `mimo` · `xiaomi` | Xiaomi MiMo 2.5 — 코딩·TTS·비전 백업 |
| `deepseek` | DeepSeek 직결 — **최후 보루** |
| `meta` | Meta Muse Image/Spark — 이미지 장당 $0.01, 비전 |
| `openrouter` | 다중 모델 라우팅 폴백 |
| `openai` | OpenCode 구독 (opencode-go 와 같은 키) |
| `nvidia` | NVIDIA NIM 무료 모델 풀 |
| `google` · `gemini` | Gemini API |
| `fish-audio` | Fish Audio TTS '소향이' |
| `kling` · `kling-secret` | Kling AI 영상 생성 |
| `nube` | Nube.sh ($10 회수 건) |
| `figma` | Figma API |
| `brave` · `tavily` · `serper` | 검색 |
| `telegram` | 텔레그램 봇 (보고·알림) |
| `github` | GitHub (gh CLI 금고) |
| `daum-mail` · `daum-mail-pass` | 다음 메일 |
| `aside` | Aside Browser 마스터 계정 |
| `tplink` | TP-Link 공유기 + USB 저장소 |

**전체 목록은 언제든 `hermes-key list`** 로 확인하십시오.

## 4. 코드에서 쓰는 법

### 파이썬

```python
import subprocess

def key(name: str) -> str:
    r = subprocess.run(["hermes-key", "get", name], capture_output=True, text=True)
    return r.stdout.strip()

MIMO_KEY = key("mimo")
```

### 셸

```bash
export DEEPSEEK_API_KEY="$(hermes-key get deepseek)"
curl -H "Authorization: Bearer $(hermes-key get opencode-go)" ...
```

## 5. 지켜야 할 규칙

1. **`hermes-ag-shared` 는 공개(public) 저장소다.** 값은 절대 여기 적지 않는다. 이름·용도·위치만.
2. **소스코드에 키를 하드코딩하지 않는다.** `hermes-key get <이름>` 으로 꺼내 쓴다.
   (실제로 이걸 안 지켜서 MiMo 키가 공개 저장소 코드 3개 파일에 한 달간 노출됐다)
3. **값을 대화창·로그·스크린샷에 남기지 않는다.**
4. **새 열쇠가 생기면 `manifest.json` 에 먼저 등록한다.** 그래야 다른 에이전트가 찾는다.

## 6. 새 열쇠 등록하는 법

`~/.hermes/credentials/manifest.json` 의 `keys` 배열에 한 칸 추가:

```json
{
  "name": "새서비스",
  "env": "NEW_SERVICE_API_KEY",
  "source": "env",
  "purpose": "무엇에 쓰는 열쇠인지",
  "used_by": ["해나"]
}
```

`source` 값: `env`(.env) · `zshrc`(.zshrc) · `file`(credentials 폴더) · `gh`(gh CLI 금고)

## 7. 참고 문서

| 문서 | 내용 |
|---|---|
| `credentials-index.md` | 열쇠 목록표 전문 (값 없음, 이 저장소) |
| `~/.hermes/credentials/INDEX.md` | 같은 문서 로컬본 |
| `~/.hermes/credentials/manifest.json` | 목록 정본 (값 없음) |
| `~/.local/bin/hermes-key` | 도구 본체 |

---

**확인 요청**: 각자 자기 코드에 하드코딩된 키가 있는지 점검하고, 있으면 `hermes-key` 방식으로 바꿔 주십시오.

```bash
cd ~/초보프로젝트/hermes-ag-shared
git ls-files | grep -vE "^venv/" | xargs grep -lE "sk-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,}" 2>/dev/null
```

아무것도 안 나오면 정상입니다.
