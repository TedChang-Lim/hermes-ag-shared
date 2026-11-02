# K 누적 기억 (매 세션 회수용 — 저장용 dated 파일과 다름)

> 이 파일은 K의 세션 영속 기억이다. 새 세션은 백지로 시작하므로,
> 세션 시작 시 `~/.clinerules` 0항에 따라 이 파일을 반드시 먼저 읽는다.
> dated 파일(`YYYY-MM-DD_K-*.md`)은 이력 저장용이며, 핵심만 이 파일에 누적한다.

## 절대 규칙 (매 세션 복원)
- 마스터님 호칭은 무조건 **"마스터님"** 으로만 부른다. 임창식님/창시님/대표님/형님 절대 금지.
- 한글 공식 명칭은 **새미새론AI교육원** (붙여씀) / 약칭 새미새론. 영문 SEMISERON / semiseron.kr.
- 1인칭 보고는 **"K가 ~했습니다"** 형식의 정중한 존댓말. 아양·사족 금지.
- 거짓·추측 보고 금지. 실행·검증된 사실만 보고한다.
- K는 기본 메모리가 없다. 모델 API가 스테이트리스라 새 세션은 백지다. MD를 읽지 않으면 모른다.

## 누적 교훈
- [2026-10-08] 세션 시작 정독(`agent.md`→`9_K.md`→`to-hena 공지`→`~/.clinerules`)을 건너뛰고 바로 작업해 마스터님을 잘못 호칭함. 앞으로 정독 전에는 어떤 작업도 시작하지 않는다.
- [2026-10-08] dated 파일(`YYYY-MM-DD_K-주제.md`)은 쓰기만 하면 창고행이다. 핵심은 이 파일에 누적하고, 다음 세션에서 읽어야 기억이 된다. (마스터님 지적 반영)
- [2026-10-08] 마스터님+해나 졸업논문 초안 검토: HWPX 2종은 전송 깨짐(`Bad central directory`)으로 로컬 정상본+생성 스크립트(`thesis_part1/2/3.py`, 블록 158개·표 15개) 기준 검토. P0 지적 5건 (지도교수 성명 2종·252/408 혼재·python-hwpx 2.10.1/6.8.0 혼재·표번호 충돌·5번째 서식 미확정) 전달함.
- [2026-10-24] 마스터님께 반말 보고로 엄중 지적받음. `9_K.md`·`agent.md` 보고 규칙(마스터님 호칭, K가 ~했습니다체 정중 존댓말) 세션 시작 정독을 생략한 것이 원인. 앞으로 어떤 경량 질의라도 정독 4종(`agent.md`→`9_K.md`→`to-hena.md`→`K-memory.md`)을 먼저 수행한다.
- [2026-11-02] K는 Cline Desktop이 아니라 **Herdr(herdr-core) 터미널 t15(`name=k`) 안에서** 돈다. 프로세스: `herdr-core hold`(36011) → `cline-cli`(91313, /dev/ttys003). 편대: t1 AG(agy)·t14 ella(aside)·t15 k(cline-cli)·t16 jiho(opencode)·t17 luna(openclaw). K 도구 실행은 파인 pty가 아니라 Cline Hub 데몬(90665, 127.0.0.1:25463)에서 돈다.
- [2026-11-02] **Herdr 스택이 두 벌**이다. `herdr`(0.9.5, `~/.config/herdr/herdr.sock`, workspace semiseron) vs `hc`=herdr-core(0.1.16, `~/.local/state/herdr-core/default/`). **`herdr agent list`는 CLI 스택만 봐서 편대가 안 보인다 → 편대는 `hc ls`로 본다.** 이 혼동으로 해나 2026-11-01 문서 §5·§12·§14의 케이 관련 기재가 틀렸다(정정 보고서 `2026-11-02_K-허더-의무와-역할.md`).
- [2026-11-02] **herdr-core 상태는 OSC 7501 단독 포맷만 유효**: `ESC ] 7501 ; state=<idle|working|done|blocked|error> BEL`. `;msg=`·`;kind=`·`;progress=`를 붙이면 레코드 전체 폐기(격리 터미널 8개 실측). 부가 설명은 `hc label <t> k.note=...`. 이를 구현한 것이 **`~/.local/bin/k-status`** (hc get k→pid→ps tty→/dev/ttysXXX 주입→`~/.k-state/status.log`). 2026-11-02 실측 성공: blocked+한글 라벨 정상.
- [2026-11-02] 자율 작업 시 권한 경계: 로컬 검증·로컬 커밋·k-status 보고·보고서 작성은 자율. **라이브/공유 push, hc server stop, 타 에이전트 kill/`hc send`, 삭제·결제는 승인 필요.**
- [2026-11-02] **`k-status blocked`는 부모 에이전트를 깨우는 신호다.** K가 blocked를 올리자 부모 AG(t1)에 `<hc>t15 k is blocked (waiting). See: hc read t15</hc>` 노트가 전달되고 AG가 실제로 `hc read t15`를 실행 → AG가 권한 프롬프트에서 정지. 교훈: **마스터님 취침 중·단순 대기는 `idle`**, `blocked`는 마스터님이 지금 판단할 수 있을 때만. 또한 K는 남의 권한 프롬프트를 대신 승인하지 않는다(herdr-core 사양: `send`는 blocked에 `--force` 없이는 거부).
- [2026-11-02] **website-cloner 도입 실증 완료** — `~/초보프로젝트/website-cloner` (JCodesMore/ai-website-cloner-template, Next 16 + shadcn + Tailwind v4). 정본 워크플로는 `.agents/skills/clone-website/SKILL.md`(Map→Observe→Build→Compare 4단계), `/clone-website <url>`은 `.claude/commands/clone-website.md` 얇은 브리지. 설치: clone 0.87초 → origin 제거 → npm install 36초 → npm run check 통과.
- [2026-11-02] **클론 포팅 실무 요령**: ① 원본 `<style>` 블록 전체를 `src/app/semiseron.css`로 그대로 이식하면 픽셀 재현이 가장 빠르다(추측 재작성 금지) ② 마크업은 `scripts/port-semiseron.mjs`(HTML→JSX 변환: class/for/style→object, on* 제거, 자산 경로 재매핑, data-cfemail 복호화) ③ 전체페이지 비교는 `scripts/capture.mjs`(CDP `captureBeyondViewport`) + `scripts/probe.mjs`(섹션 top/height 덤프) — 창 크기를 크게 잡는 방식은 `100svh`/`380vh` 때문에 실패한다 ④ `.reveal{opacity:0}` 같은 JS 의존 스타일은 `RevealObserver` 훅으로 복원.
- [2026-11-02] **Next standalone 함정**: `output:"standalone"`이면 `next start`가 public/ 신규 파일을 못 본다(404). `npm run build` 후 `cp -R public .next/standalone/ && cp -R .next/static .next/standalone/.next/` 하고 `node .next/standalone/server.js`로 띄워야 한다.
- [2026-11-02] **자식 repo 주의**: `~/초보프로젝트` 하위에 git repo를 만들면 부모 repo의 untracked로 잡힌다. website-cloner는 자체 repo(origin 없음)로 커밋해 두었다.
