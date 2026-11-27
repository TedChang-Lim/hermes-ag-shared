# TED CORE 지호 = OpenCode **데스크탑 앱** CLI 연결 (2026-11-27, 해나)

## 한 줄

TED CORE의 지호(jiho)는 `PATH`의 `opencode`가 아니라 **OpenCode 데스크탑 앱에 동봉된 CLI**를 쓴다. 앱 번들 경로가 정본이다.

## 무엇이 문제였나

- `which opencode` → `~/.local/bin/opencode` (= **0.0.0-codex 개발빌드**, 2026-07-22 파일). 마스터가 쓰지 않는 유물.
- 이 빌드는 `opencode run`을 지원하지 않아 stderr에 `OpenCode 1.18.0 or newer is required`를 찍고 **exit 0 + 빈 stdout**으로 끝났다. TED CORE 화면에는 "조용히 성공"으로 보였다.
- 실제로 마스터가 계속 업데이트하는 것은 **OpenCode 데스크탑 앱**이다(2026-11-27 실측 2.4.2, `ai.opencode.desktop`).

## 실측된 실행 파일 3종

| 경로 | 버전 | 정체 |
|:--|:--|:--|
| `~/.local/bin/opencode` | 0.0.0-codex/…20260610 | 옛 개발빌드 — **쓰지 않는다** |
| `~/.opencode/bin/opencode` | 1.19.5 | 예전 터미널 CLI 설치본 — 쓰지 않는다 |
| `/Applications/OpenCode.app/Contents/Resources/opencode-cli` | **2.4.2** | **데스크탑 앱 번들 CLI = 정본** |
| `~/Library/Application Support/ai.opencode.desktop/cli/2.4.2-arm64/opencode-cli` | 2.4.2 | 앱이 띄우는 백그라운드 서비스가 쓰는 사본(버전 폴더가 바뀜) |

- 앱을 업데이트하면 앱 번들 안의 CLI도 같이 올라간다 → **고정 경로 한 곳만 보면 된다**.
- 버전 표기 확인: `"/Applications/OpenCode.app/Contents/Resources/opencode-cli" --version` → `opencode v2.4.2`
- 최신 여부 확인(앱 업데이트 채널): `curl -s https://opencode.ai/update/api/latest/desktop/opencode/ | head -c 200` → `"version":"2.4.2"`

## TED CORE에 어떻게 넣었나 (`~/초보프로젝트/ted-core`)

`src/app.rs`에 경로 결정 함수를 두고, 지호 분기 3곳을 그것으로 바꿨다.

```rust
pub fn jiho_bin() -> String {
    let app = "/Applications/OpenCode.app/Contents/Resources/opencode-cli";
    if std::path::Path::new(app).exists() { app.to_string() } else { "opencode".to_string() }
}
```

| 경로 | 명령 |
|:--|:--|
| 한 번 묻고 회수(`ask_argv`) | `opencode-cli run -m <model> --auto --archived "<지시>"` |
| 작업실·병렬(`studio.dispatch`) | 위와 같음(studio가 `ask_argv`를 그대로 씀) |
| 대화형 PTY 칸(`interactive_argv`) | `opencode-cli` (모델은 앱 설정을 따름) |

- `--auto` = 명시적으로 거부되지 않은 권한을 자동 승인 (헤드리스 필수).
- `--archived` = 스크립트용 세션을 마스터의 데스크탑 세션 목록에 남기지 않음.
- **`-m`은 `run` 뒤에만 붙인다.** 최상위(`opencode -m …`)에 붙이면 `Unrecognized flag: -m` → 사용법만 출력하고 끝난다(이걸로 18초 동안 화면에 USAGE가 찍혔다).
- 지호는 이제 tty 경로를 쓰지 않는다(`use_tty` 기본 false). TUI가 필요하면 RPC에 `tty:true`를 준다.

## 검증 (실측)

| 확인 | 결과 |
|:--|:--|
| 앱 번들 CLI 직접 | `opencode v2.4.2`, `run -m opencode-go/deepseek-v4.1-flash --auto` → `JIHO_OK` (11.3초) |
| TED CORE `agent.ask` (jiho) | `JIHO_CORE_OK`, 2.3초, exit 0 |
| TED CORE `studio.dispatch` (jiho) | 카드 `완료 (1.7초) · JIHO_STUDIO_OK` |
| `cargo build --release` / `cargo test` | 성공 / 23 passed |

## 재현 절차

```bash
OC="/Applications/OpenCode.app/Contents/Resources/opencode-cli"
"$OC" --version
"$OC" run -m opencode-go/muse-spark-1.3-contributor --auto --archived "한 줄로 JIHO_OK"
# TED CORE 쪽 확인
curl -s -X POST http://127.0.0.1:8848/api/rpc -H 'Content-Type: application/json' \
  -d '{"method":"agent.ask","params":{"agent":"jiho","prompt":"한 줄로 JIHO_CORE_OK","timeout":120}}'
```

## 함정

- `npm view opencode-ai version`은 **1.19.6**(터미널 CLI 계보)이다. 데스크탑 앱(2.x)과 다른 제품이라 버전 비교 대상이 아니다.
- Homebrew cask `opencode-desktop`의 기록된 설치 버전(1.18.29)·cask 최신(2.3.2)도 실제 앱(2.4.2)과 어긋난다 — 앱이 스스로 업데이트하기 때문. **앱 번들 `--version`이 정본**.
- TED CORE 백엔드는 앱을 껐다 켜도 안 바뀐다. 코드를 고쳤으면 포트 8848 프로세스를 죽이고 `./target/release/ted-core`를 다시 띄운다.
- `claude update`처럼 이 검증 없이 "최신이다"라고 말하면 안 된다. 위 4개 경로를 매번 실측한다.
