---
type: concept
created: 2026-09-21
updated: 2026-09-21
sources: []
aliases: [credentials-index, 열쇠목록, hermes-key]
---

# 자격증명 목록표 (열쇠함 색인)

**이 파일에는 값이 없다.** 값이 어디 있는지만 가리킨다. 이 저장소는 공개(public)이므로 값을 적지 않는다.

## 쓰는 법 — 어떤 에이전트든 이 한 줄이면 끝

```bash
hermes-key list              # 열쇠 전체 목록 (값 없음)
hermes-key where mimo        # 그 열쇠가 어디 있는지
hermes-key get mimo          # 값 꺼내기
hermes-key env mimo          # 셸에서 바로 쓰기 (export 형태)
```

파이썬에서는:

```python
import subprocess
key = subprocess.run(
    ['hermes-key', 'get', 'mimo'],
    capture_output=True, text=True,
).stdout.strip()
```

## 열쇠 목록

| 이름 | 용도 | 쓰는 곳 | 값 위치 |
|---|---|---|---|
| `opencode-go` | OpenCode Go 구독 — 모델 27종(DeepSeek V4.1, GLM-5.3, Muse Spark 등) 호출 | 해나(Hermes 기본 모델), Aside 프로바이더, 지호 | `~/.hermes/.env` → `OPENCODE_GO_API_KEY` |
| `mimo` | Xiaomi MiMo 2.5 — 코딩·TTS·비전 백업 | 미모(Zed), 코코 | `~/.hermes/credentials/mimo_api_key.txt` |
| `xiaomi` | Xiaomi API 직결 (MiMo 와 같은 키) | 미모 | `~/.hermes/.env` → `XIAOMI_API_KEY` |
| `deepseek` | DeepSeek 직결 — 최후 보루. 다른 경로가 다 죽어도 이것으로 해나가 움직인다 | 해나(비상), 전 에이전트 | `~/.hermes/.env` → `DEEPSEEK_API_KEY` |
| `meta` | Meta Muse Image/Spark 직결 — 이미지 장당 $0.01, 비전 | 해나(비전), Aside Visual 칸 | `~/.hermes/.env` → `META_API_KEY` |
| `openrouter` | OpenRouter — 다중 모델 라우팅 폴백 | 전 에이전트 | `~/.hermes/.env` → `OPENROUTER_API_KEY` |
| `github` | GitHub — 저장소·이슈·PR (gh CLI 금고에 보관) | 전 에이전트 | gh CLI 금고 (macOS 키체인) |
| `openai` | OpenCode 구독 — opencode-go 와 같은 키 (별칭) | 지호(OpenCode) | `~/.hermes/.env` → `OPENCODE_API_KEY` |
| `nvidia` | NVIDIA NIM — 무료 모델 풀 | 전 에이전트(폴백) | `~/.zshrc` → `NVIDIA_API_KEY` |
| `google` | Google Gemini API | 해나 | `~/.hermes/.env` → `GOOGLE_API_KEY` |
| `gemini` | Gemini API (google 과 같은 키) | 해나 | `~/.hermes/.env` → `GEMINI_API_KEY` |
| `fish-audio` | Fish Audio TTS — '소향이' 목소리 | 해나(음성), 영상 파이프라인 | `~/.hermes/.env` → `FISH_AUDIO_API_KEY` |
| `kling` | Kling AI 영상 생성 | 영상 파이프라인 | `~/.hermes/.env` → `KLING_ACCESS_KEY` |
| `kling-secret` | Kling AI 시크릿 | 영상 파이프라인 | `~/.hermes/.env` → `KLING_SECRET_KEY` |
| `nube` | Nube.sh — $10 회수 분쟁 건 | 해나 | `~/.hermes/.env` → `NUBE_API_KEY` |
| `figma` | Figma API — 디자인 토큰 추출 | 미모, 해나 | `~/.hermes/.env` → `FIGMA_ACCESS_TOKEN` |
| `brave` | Brave 검색 — 해나 전용 | 해나 | `~/.hermes/.env` → `BRAVE_SEARCH_API_KEY` |
| `tavily` | Tavily 검색 — 해나 전용 | 해나 | `~/.hermes/.env` → `TAVILY_API_KEY` |
| `serper` | Serper 검색 | 해나 | `~/.hermes/.env` → `SERPER_API_KEY` |
| `telegram` | 텔레그램 봇 — 보고·알림 | 해나, 전 크론잡 | `~/.hermes/.env` → `TELEGRAM_BOT_TOKEN` |
| `daum-mail` | 다음 메일 계정 (아이디) | 해나(메일 크론) | `~/.hermes/.env` → `DAUM_EMAIL_USER` |
| `daum-mail-pass` | 다음 메일 비밀번호 | 해나(메일 크론) | `~/.hermes/.env` → `DAUM_EMAIL_PASS` |
| `aside` | Aside Browser 마스터 계정 + 복구 키 | 해나, 전 에이전트(브라우저 작업) | `~/.hermes/credentials/aside.txt` |
| `tplink` | TP-Link BE3600 공유기 관리자 + USB 저장소 계정 | 해나 | `~/.hermes/credentials/tplink.txt` |

## 값이 사는 네 곳

| 자리 | 무엇이 있나 | 왜 여기 있나 |
|---|---|---|
| `~/.hermes/.env` | API 키 대부분 | Hermes 와 크론잡이 시작할 때 자동으로 읽는다 |
| `~/.zshrc` | NVIDIA, MiMo, Meta, OpenCode | 셸에서 쓰던 것. 옮기면 깨질 수 있어 그대로 둠 |
| `~/.hermes/credentials/*.txt` | Aside, TP-Link, MiMo | API 키가 아닌 계정 정보·비밀번호 |
| gh CLI 금고 | GitHub 토큰 | `gh auth login` 이 macOS 키체인에 넣었다. 파일에 없다 |

## 지켜야 할 규칙

1. **`hermes-ag-shared` 는 공개 저장소다.** 값은 절대 여기 적지 않는다. 이름·용도·위치만.
2. **소스코드에 키를 하드코딩하지 않는다.** `hermes-key get <이름>` 으로 꺼내 쓴다.
3. **값을 대화창·로그·스크린샷에 남기지 않는다.**
4. 새 열쇠가 생기면 **`manifest.json` 에 먼저 등록**한다. 그래야 다른 에이전트가 찾는다.

## 새 열쇠 등록하는 법

`~/.hermes/credentials/manifest.json` 의 `keys` 배열에 한 칸 추가한다:

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

## 확인

```bash
hermes-key list | grep '○'    # 값이 없는 열쇠 찾기
```

2026-09-21 기준 **24개 전부 값 있음**.

*작성: 해나 (Hermes Agent) | 2026-09-21*
