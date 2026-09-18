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

## 2. Gmail 자동화 방식 변경

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

## 3. Aside 사용 수칙 (기존 유지)

- stdin 파이핑 금지. 코드 전체를 인자로 1회 호출
  `aside repl "const p = await openTab('URL'); await sleep(5000); console.log(await p.evaluate(() => document.body.innerText.slice(0,4000)))"`
- 탭은 호출 간 유지 안 됨. `openTab` → 추출 → `closeTab` 을 한 호출 안에서
- `daemon is not reachable` → `open -a Aside` 후 재시도
- 마스터님 크롬 프로필을 공유한다. **탭을 함부로 닫거나 마스터님이 쓰는 탭을 건드리지 말 것**
- 조회는 자유. **삭제·전송·결제·비밀번호 변경은 마스터님 승인 후에만**

---

## 4. 확인 요청

각 에이전트는 자기 코드에 하드코딩된 키가 있는지 점검하고, 있으면 위 방식으로 옮겨 달라.

```bash
cd ~/초보프로젝트/hermes-ag-shared
git ls-files | grep -vE "^venv/" | xargs grep -lE "sk-[A-Za-z0-9_-]{16,}|MasterPass" 2>/dev/null
```

아무것도 안 나오면 정상이다.
