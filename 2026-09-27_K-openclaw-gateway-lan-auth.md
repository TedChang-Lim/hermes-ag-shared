# [2026-09-27] 루나(OpenClaw 2.0) 반복 사망 — 근본원인 및 영구 해결

> 작성: K (Cline Desktop) · 대상: 루나(Luna) 하네스 OpenClaw 2.0 v2026.9.6

## 증상
- 데스크탑 앱이 안 뜀. Dock에도 없음(메뉴바 전용 `LSUIElement=1`이라 정상).
- 크래시 리포트 0건 → "죽은 게 아니라 백엔드가 없어서 못 뜨는" 상태.
- 게이트웨이가 10초 간격으로 기동 거부하며 무한 재시작.

## 진짜 원인 (K가 1차 오진함 — 중요)
1차incident에서 K가 `gateway.bind: "lan"` 키를 삭제하는 것으로 "해결"했다고 보고했으나 **약 6분 뒤 동일 증상으로 재발**함.
원인은 K의 접근이 틀렸다는 것. `bind: lan`은 **매체가 의도적으로 되돌리고 있었음**.

### 증거 타임라인
| 시각(KST) | 사건 |
|---|---|
| 17:34:17 | K가 설정 백업 후 `bind` 키 삭제 |
| 17:34:40 | 게이트웨이 기동 성공, HTTP 200 |
| **17:40:53** | **루나가 `openclaw.json.bak-luna-20260927-174053` 생성(수정 전 정상본 백업) 후 `bind: "lan"`을 다시 기록** |
| 17:42:04 | `gateway-restart.log` — `source=handoff mode=start-after-exit` 게이트웨이 재시작 |
| 17:47~ | 크래시 루프 재개 |

백업 파일 크기로 확인:
- `openclaw.json` (6068B) = `bind=lan` ← **손상**
- `openclaw.json.bak` (6049B) = bind 없음 ← 정상
- `openclaw.json.bak-luna-20260927-174053` (6049B) = bind 없음 ← 정상
- `openclaw.json.last-good` (6049B) = bind 없음 ← 정상

`bak-luna-*` 패턴은 2026-09-26 23:33부터 반복 existed → **루나가 수차례 같은 시도를 반복**해옴.

## 근본 메커니즘
OpenClaw의 보안 가드:
> `Refusing to bind gateway to lan without auth.`

설정 조합 `bind: lan` + `auth.mode: "none"`은 **의도적으로 거부됨**(LAN 노출 + 무인증 = 위험).
`agent.md:60` 기준 루나의 역할이 "스마트폰 노드와 맥북 연결"이므로 **`bind: lan`은 마스터님의 정당한 요구**임.
따라서 `bind`를 지우는 방식은 **요구를 충족시키지 못하고 매번 되돌려지는 3라운드째 같은 싸움**이 됨.

## ✅ 영구 해결 (권고 방식)
**`bind`를 빼는 게 아니라 인증을 켠다.**

```json
"gateway": {
  "mode": "local",
  "auth": { "mode": "token", "token": "<기존 토큰>" },
  "bind": "lan"
}
```

- `auth.mode: "none"` → `"token"` (기존 토큰 값 그대로 사용)
- `bind: "lan"` **유지** → 스마트폰 노드 연결 요구 충족
- 가드 해제 → **루나가 `bind: lan`을 다시 써도 게이트웨이가 정상 기동**

### enum 근거 (공식 CLI 도움말로 검증)
```
--auth <mode>  ("none"|"token"|"password"|"trusted-proxy")
--bind <mode>  ("loopback"|"lan"|"tailnet"|"auto"|"custom")  기본값 loopback
```

## 검증 결과
- 게이트웨이 PID 정상, 로그: `[gateway] ready`
- 바인딩 `*:18789 (LISTEN)` (전 인터페이스)
- loopback HTTP 200 / LAN(192.168.0.194) HTTP 200
- WebSocket 정상: `chat.startup`, `sessions.messages.subscribe` 등 응답
- 데스크탑 앱 기동, 크래시 0건
- 로그: `agent model: opencode-go/deepseek-v4.1-flash` — MEMORY.md 기재 기본값과 일치 ✅

## 재발 방지 교훈
1. **증상 재발 시 원인을 재검토할 것.** 1차 수정 6분 만에 재발 = "해결"이 아니라 "잠시 억제"였음.
2. **거부 메시지에 이유가 있다.** `Refusing to bind ... without auth`는 버그가 아니라 설계된 가드. 키를 지우지 말고 **가드의 조건을 만족**시킬 것.
3. **설정 되돌림 주체를 추적할 것.** `bak-<에이전트명>-<타임스탬프>` 패턴이 나타나면 해당 에이전트가 설정을 덮어쓰는 것.

---
작성: K · 새미새론AI교육원
