# Concat MCP — 에이전트가 영상을 직접 편집한다 (검증 완료)

루나 · 2026-11-01

## 결론
**에이전트(Claude Code)가 MCP로 영상 편집·내보내기까지 완수.** 실패 없이 end-to-end 동작.

## 실물
- **Concat** `jub0t/Concat` ★12,873 · Rust · **AGPL-3.0** · v0.2.8
- 설치: `/Applications/Concat.app` (macOS arm64 dmg)
- MCP 내장: `concat --mcp` (headless / window / auto)

## 코코(Claude Code) 등록
```sh
claude mcp add concat -- /Applications/Concat.app/Contents/MacOS/concat --mcp
```
→ `.claude.json`에 stdio 서버로 등록됨 (백업: `.claude.json.bak-concat-*`)

## 검증 결과 (실측)
- MCP 핸드셰이크: **도구 42개** 응답
- 프로젝트 생성 → 미디어 2개 임포트(m1, m2) → 시퀀스 추가 → **타임라인 16.085초**
- `export_start` → `export_wait` **fraction 1.0 (386 프레임)** → mp4 4.5MB 생성
- 산출물: `~/craft-work/concat-test2/luna_test.mp4`

## 핵심 도구 (42개 중)
`project_create/open/save` · `media_import/probe` · `clips_add_sequence` · `clip_trim/split/move`
`title_add` · `captions_add`(로컬 Whisper) · `keyframe_set` · `effect_layer_add`
`export_start/status/wait` · `preview_frame`

## 주의
- **AGPL-3.0**: 외부 배포 시 소스 공개 의무. 내부 사용은 무관
- 프로젝트 락(`concat.lock`) — 창에서 연 프로젝트는 headless가 거부
- headless는 홈 폴더 하위에만 씀 (`CONCAT_MCP_ROOTS`로 확장)

## 우리 파이프라인 적용
1. Flow(Veo) 8초 샷 생성
2. **코코가 Concat MCP로 비트 컷 편집 + 자막**
3. 우리 three.js로 타이포·차트 오버레이
4. `export_start` 4K → 유튜브/숏폼
