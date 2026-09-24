# 전 에이전트 통보: Aside 실전 패턴 확정 + YouTube 운영 자동화 (2026-09-15, 해나 발신)

마스터님 지시로 전원 공유. 스킬 `aside-mcp-web-crawling`에 반영済 — 상세는 스킬 참조, 핵심만 통보.

## 1. Aside REPL 호출법 (전원 필수 준수)

- stdin 파이핑 금지. 코드 전체를 인자로 1회 호출:
  `aside repl "const p = await openTab('URL'); await sleep(5000); console.log(await p.evaluate(() => document.body.innerText.slice(0,4000)))"`
- 탭은 호출 간 유지 안 됨. openTab→추출까지 1회 호출 안에 끝낼 것.
- `daemon is not reachable` → `open -a Aside` 후 재시도.
- 검증済 실측: 빠나나 요금·종량제·공모전, 힉스필드 플러그인/브릿지 URL 전부 Aside로 추출.

## 2. YouTube 운영 자동화 3종 (강인환 영상 실증, 우측 채널 적용 가능)

1. 채널 세팅 점검 (트레일러·키워드·재생목록·메타데이터 감사)
2. Studio 데이터 진단 (28일/90일, CTR·유지율·트래픽소스 → 개선 리포트)
3. 업로드 자동화 (제목·설명·공개범위·예약, 채널명 재확인 필수)

## 3. 영상 도구 선택제 (마스터님 확정, 전원 준수)

- 기본=Wan 3.0 / H3=애니 전용(실사 금지) / Blender=camera-heavy 전용 / 나머지=MCP 직결
- 평시 상한 Seedance 2.0 / Seedance 2.5 봉인 (마스터님 명시 지시 때만)
- 한국어 대사=Kling 3.0 / 롱테이크 30초=Wan 3.0 (닥또리·아스트라 실측 근거)
