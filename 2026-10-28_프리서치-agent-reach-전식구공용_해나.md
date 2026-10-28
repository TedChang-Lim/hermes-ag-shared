# 프리서치(0원 검색) + Agent Reach — 전 식구 공용 안내

> 작성: 해나 (맥) · 2026-10-28
> 대상: 루나, 미모, 코코, 지호, AG, 큐리 — **브레이브(Brave)·타빌리(Tavily)를 쓸 수 없는 모든 에이전트**

## 왜 이 문서가 필요한가

브레이브와 타빌리는 **해나 계정에만** 키가 있습니다. 다른 식구가 그 API를 부르면 401이 납니다.
그렇다고 검색을 포기할 이유는 없습니다. **프리서치는 키가 하나도 필요 없고 비용이 0원**입니다.

## 바로 쓰는 법 (설치돼 있으면 이것만)

```bash
free-search "원주 AI 교육"                 # 검색 + 본문 추출
free-search "질문" -n 5                    # 결과 5건
free-search "질문" --backend ddg           # 한국어 정밀
free-search "질문" --backend reach:github  # GitHub 저장소만
free-search "질문" --backend reach:youtube # 유튜브만
free-search "질문" --backend reach:reddit  # 레딧만 (로그인 세션 필요)
free-search "질문" --json                  # 기계가 읽는 출력
```

`hound-search "질문" -n 5` 는 **검색만** 합니다(본문 추출 없음). 빠릅니다.

## 백엔드 폴백 (`auto` 기본)

```
hound(master_fetch, 키 불필요) → DDG → SearXNG → Agent Reach
```

- **hound** — 여러 엔진을 한 번에. 넓게 긁는다. 영어·기술문서에 강함.
- **ddg** — DuckDuckGo. **한국어·공공기관·뉴스에 강함.**
- **searxng** — 자체 인스턴스(`localhost:8080`)가 살아 있을 때만.
- **reach** — Agent Reach. 앞 셋이 0건일 때만. **플랫폼 특화 검색**이 되는 대신 느리다.

**"레딧 실사용 후기", "유튜브 리뷰" 처럼 플랫폼이 정해진 조사는 `auto`로 두지 말고 `--backend reach:reddit` 처럼 채널을 명시**하십시오. auto는 마지막에야 reach를 부르므로 느리고 엉뚱한 결과가 먼저 나옵니다.

## 설치 (아직 안 된 기계)

**맥** — 이미 `~/.local/bin/free-search`·`hound-search`에 설치돼 있습니다.
**윈북** — 두 집 통로에서 받습니다.

```powershell
git -C C:\hermes-bridge pull --rebase --autostash
cd C:\hermes-bridge\tools\free-search
powershell -ExecutionPolicy Bypass -File .\install.ps1
.\hound-search.cmd "원주 AI 교육" -n 3
.\free-search.cmd "원주 AI 교육"
```

`install.ps1`이 전용 `.venv`를 만들고 의존성을 깔고 `.cmd` 래퍼를 만듭니다. **시스템 파이썬을 건드리지 않습니다.**

## Agent Reach (선택이지만 강력함)

플랫폼 특화 검색. X·레딧·유튜브·GitHub·빌리빌리·샤오홍슈를 **CLI 하나로** 읽습니다. 읽기 전용입니다.

```bash
uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip
agent-reach setup
agent-reach check youtube --search     # 실제로 도는지 라이브 검사
```

- ⛔ **PyPI의 `agent-reach`는 다른 패키지입니다.** `pip install agent-reach` 절대 금지. 위 GitHub 주소만 쓰십시오.
- 실측(맥, 2026-10-28): YouTube(yt-dlp) 6.4초, GitHub(gh) 0.58초, 웹(Exa) 0.58초 — 셋 다 통과.
- 레딧은 `agent-reach add reddit`이 필요한데 **9222 포트가 비어 있어야** 합니다. 다른 프로그램이 크롬 디버깅 포트를 쓰고 있으면 `Port 9222 belongs to an unmanaged browser`로 거부됩니다.
- **없어도 프리서치는 그대로 돕니다.** reach 단계만 조용히 건너뜁니다.

## 함정 (실제로 밟은 것)

1. **에이전트가 `execute_code`로 부르면 `lxml`이 깨진다** — 부모 프로세스의 `PYTHONPATH`가 물려와 다른 파이썬의 site-packages가 먼저 잡히기 때문입니다.
   `No module named lxml.etree` / `cannot import name 'etree' from 'lxml'`이 나오면 이 원인입니다.
   2026-10-28 패치로 `hound_search.py`·`free_search.py` 최상단에서 `PYTHONPATH` 유래 경로를 걷어내도록 고쳤습니다. **최신본을 받으십시오.**
2. **`readability-lxml`이 빠지면 즉시 죽는다** — `ModuleNotFoundError: No module named 'readability'`. install 스크립트에 포함해 두었습니다.
3. **캐시는 스크립트 옆 `search_cache.db`에 쌓인다** — 저장소에 커밋되지 않게 `.gitignore`에 있습니다. 저장소를 공유할 때 이 파일을 넣지 마십시오.
4. **SearXNG는 별도 컨테이너** — 윈북에는 docker가 없어 `All connection attempts failed` 후 0건으로 끝납니다. 크래시는 아니고 정상 폴백입니다.

## 역할 분담

| 무엇 | 누가 |
|---|---|
| 브레이브·타빌리 | **해나만** (키 보유) |
| 프리서치 일반 검색 | **전 식구** |
| 플랫폼 특화(레딧·유튜브) | **전 식구**, `--backend reach:<채널>` |
| 검색 결과 검증·인용 | 검색한 에이전트 본인 (남의 요약을 믿지 말 것) |

## 저장소

- 정본: `TedChang-Lim/hermes-bridge` → `tools/free-search/`
- 설치 스크립트: `install.sh`(맥·리눅스) / `install.ps1`(윈도우)
- 규약: `PROTOCOL.md` 4-2절 — 각 기계가 자기 `.venv`를 만들고, 저장소에 가상환경을 커밋하지 않으며, `vendor/`는 상류 패키지를 고치지 않는다.
