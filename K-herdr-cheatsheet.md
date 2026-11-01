# K Herdr 치트시트 (herdr-core / hc)

> 작성: K · 2026-11-02 · **매 세션 참조용**. 상세 배경은 `2026-11-02_K-허더-의무와-역할.md`.

## 0. 먼저 스택을 구분한다

| 확인 대상 | 명령 | 소켓 |
|---|---|---|
| **현재 편대(우리)** | `hc ls` (`~/.local/bin/herdr-core`) | `~/.local/state/herdr-core/default/` |
| 옛 CLI 스택 | `herdr agent list` | `~/.config/herdr/herdr.sock` |

**편대 조회는 무조건 `hc ls`.** `herdr`는 0.9.5 구버전 계열이라 현재 편대(t1/t14/t15/t16/t17)를 못 본다.

## 1. K 자신의 주소

```
K   = t15  (name: k, agent: cline-cli, /dev/ttys003)
형제 AG=t1(agy) · 엘라=t14(aside) · 지호=t16(opencode) · 루나=t17(openclaw)
부모: t1 (AG가 hc run으로 파생)
```

## 2. 조회 (읽기 전용)

```bash
hc ls                      # live 터미널
hc ls --all                # 종료된 것 포함
hc get k                   # K 상세 (status, labels, pid, turn)
hc get t1                  # AG 상세 (status.app/state/msg)
hc read t16 --lines 80     # 지호 화면 회수
hc templates               # 사용 가능한 역할 템플릿(reviewer 등)
```

## 3. 상태 보고 — `k-status`

```bash
k-status working                     # 턴 시작
k-status blocked "마스터님 승인 대기: OOO"   # 사람 결정 필요
k-status done                        # 턴 종료
k-status idle                        # 입력 대기
k-status show                        # 현재 상태/라벨/최근 로그
```

- 유효 시퀀스: `ESC ] 7501 ; state=<word> BEL` **단독**. `;msg=`·`;kind=`·`;progress=` 붙이면 레코드 폐기(실측).
- 설명은 `hc label k k.note="..."`로 분리 저장.
- 스크립트: `~/.local/bin/k-status` / 로그: `~/.k-state/status.log`
- **blocked 상태에서는 `hc send`가 `--force` 없이는 거부된다**(사양). 사람이 화면에서 직접 입력하는 것은 가능.

## 4. 헬퍼 파견 / 회수

```bash
hc run --bg --name review --cwd /path reviewer "src/x.rs만 검토. 끝나면 hc send t15"
hc run --bg --no-notify --no-parent /bin/echo hello   # 부작용 없는 단발 테스트
hc wait --children all        # 자식 전부 끝날 때까지
hc read review --lines 120    # 결과 회수
hc kill review; hc rm review  # 정리 (내가 띄운 것만)
```

- **`--bg` 필수**: 없으면 자식 화면이 내 출력으로 흘러든다.
- **`--no-notify`**: 자식이 부모(나) 터미널에 노트를 타이핑하는 것을 막는다. 내 Cline TUI 입력창 오염 방지.
- `HC_TERMINAL_ID`는 자식이 부모에게 보고할 주소다.

## 5. 금지 / 주의

| 금지 | 이유 |
|---|---|
| `hc server stop` / core 재시작 | 전 터미널 영향. 승인 필요 |
| 형제에게 `hc send` | 상대 모델 호출 = 비용·교란. 승인 필요 |
| 형제 `kill`/`rm` | 남의 작업 파괴 |
| `herdr` 명령으로 편대 판단 | 다른 스택을 본다 |
| 라이브/공유 repo push | 마스터님 승인 후 |

## 6. 검증 공식

```bash
# 상태가 실제로 붙었는지
k-status working && hc get k | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])'
# 내 터미널 pty 확인
ps -o pid=,tty=,command= -p $(hc get k | python3 -c 'import json,sys;print(json.load(sys.stdin)["pid"])')
```
