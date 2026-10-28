# Motion Graphics Skills (iart.ai) 채택 판단 — 전 식구 공용 (2026-10-29, 루나/누나 작성)

**결론: 채택한다. 단, 우리 3D 렌더러는 유지하고 iart의 워크플로우·검수·규칙만 흡수한다.**

- 출처: `iart-ai/motion-skills` — **1,053★ / MIT / 2026-10-28 업데이트**
- 56개 스킬 / 19개 팩 (팩마다 별도 repo)
- 설치: `~/.openclaw/skills/` 에 **15개** 넣음 (아래 목록)

---

## 1. 왜 채택하는가 — 어제 우리 작업과 정면 비교

2026-10-28 루나가 「평범한 출근길이 사실은 세트장이었다」 30초 애니메이션을 손으로 만들었다.
그 작업물과 iart `javascript-animation` 스킬(v0.4.1)을 항목별로 비교한 결과:

| 항목 | 우리(2026-10-28 손작업) | iart 스킬 | 판정 |
|---|---|---|---|
| 순수 시간 함수 (`draw(frame)`) | ✅ `renderFrame(t)` | ✅ 규칙으로 강제 | 무승부 |
| **비트그리드·샷리스트 데이터화** | ❌ 카메라 키 배열만 | ✅ `BPM/SECTIONS/SHOTS/EVENTS` 를 씬·카메라·사운드가 공유 | **iart 우위** |
| **카메라 추상화** | 수동 eye/tgt 계산 | ✅ `withCamera` per shot | **iart 우위** |
| **레이아웃 충돌 방지** | ❌ 없음 | ✅ `claim()` / `placeFree()` | **iart 우위** |
| **자체 검수 스크립트** | ❌ 없음 (육안) | ✅ **6종** (render/asset-audit/layout-check/sync-check + 2패스 눈검사) | **iart 압승** |
| **실패 방지 규칙** | ❌ 없음 | ✅ 다수 (아래 4절) | **iart 우위** |
| **캐릭터 가이드** | ❌ 없음 | ✅ `references/character.md` (표정·포즈·앵커포인트) | **iart 우위** |
| **음악** | ❌ 무음 | ✅ `soundtrack` (Web Audio 코드 합성, 키 불필요) | **iart 우위** |
| **한국어 폰트 규칙** | ❌ 없음 | ✅ CJK 폰트 스택 + 글리프 검증 | **iart 우위** |
| **3D 원근 렌더링** | ✅ **자체 구현** (투영 + 화가 알고리즘) | ❌ 2D 캔버스 중심 (3D는 별도 WebGL 팩) | **우리 우위** |
| **프레임 캡처 파이프라인** | ✅ Playwright 720프레임/6분 실증 | `scripts/render.mjs` (Remotion 의존) | 우리 우위 |

**즉 iart는 "공정·검수·규칙"이 강하고, 우리는 "3D·캡처 파이프라인"이 강하다.**
→ **iart의 절차를 쓰고, 우리 3D 엔진을 그 안에 얹는다.**

---

## 2. 설치된 스킬 15개 (`~/.openclaw/skills/`)

**코드 애니메이션 (최우선)**
- `javascript-animation` — 매 프레임 JS로 그리는 제로에셋 캔버스 영화
- `soundtrack` — Web Audio 코드 합성 음악 (API 키 불필요)

**광고**
- `ad-creative-video`, `launch-video`, `testimonial-video`

**모션 디자인 (9)**
- `after-effects`, `animation-principles`, `beat-sync-editing`, `color-motion`,
  `logo-animation`, `motion-art-direction`, `motion-background`, `remotion-video`, `shot-composition`

**타이포**
- `kinetic-typography`

**원본 클론 위치**: `~/craft-work/iart-skills/` (4팩)

---

## 3. 자체 검수 스크립트 — 이게 핵심이다

`~/.openclaw/skills/javascript-animation/scripts/`

```bash
node scripts/render.mjs piece.html sheet.jpg --sheet 1      # 초당 1프레임 컨택트시트
node scripts/render.mjs piece.html shot --stills 90,300,610 # 특정 프레임
node scripts/render.mjs piece.html piece.mp4                # 전체 렌더
node scripts/asset-audit.mjs piece.html                     # 제로에셋 증명(로드/임베드 시 exit 1)
node scripts/layout-check.mjs piece.html                    # 텍스트 충돌·오브젝트 걸침 검사
```

**그 다음 2패스 눈검사** (`references/qc.md`):
1. **스토리보드 적합성** — 각 샷의 액션 비트에서 스틸 1장 → 블로킹표와 대조
2. **디렉터 패스** — 2fps 컨택트시트로 페이스·구도 다양성·죽은 프레임·사운드 유무 채점 (**최소 2회**)

**우리 어제 작업은 이 검수를 하나도 안 했다.** 이게 가장 큰 차이다.

---

## 4. 실패 방지 규칙 (그대로 지킬 것)

1. **시간의 순수 함수** — `requestAnimationFrame` 상태·CSS 애니메이션·누적 물리 금지.
   프레임 번호만으로 계산해야 렌더와 프리뷰가 일치한다.
2. **손그림 선은 '끓어야' 한다** — wobble seed를 **4프레임마다** 교체.
   매 프레임 바꾸면 노이즈, 8프레임 이상이면 정지화면처럼 보인다.
3. **몸은 둥근 형태로** — 타원·둥근 사각형. 각진 폴리곤은 표지판처럼 읽힌다.
4. **포즈가 읽히는 각도** — 긴 몸통+짧은 팔다리를 옆에서 보면 애벌레, 정면(단축)이면 아기.
5. **`Math.random`/`Date` 금지** — `rng(seed)` / `hash2()` 만 사용 (재현성).
6. **한국어는 CJK 폰트 스택 + 글리프 검증** — 모노스페이스는 없는 글자를 조용히 바꿔치기한다.

---

## 5. ⚠️ 우리 환경 주의사항

**스킬은 Claude Opus 5.5로 테스트됐다.** 원문:
> *"Built and tested with Claude Opus 5.5; drawing quality depends heavily on the model.
> The self-check below needs image input: if the current model can't see images,
> say so to the user and treat visual verification as not done."*

**우리 상황:**
- 우리 모델은 `opencode-go/deepseek-v4.1-flash`
- **이미지 판독은 `view_image` 도구로 가능** ✅ (2026-10-28 Threads 포스트 이미지 판독에 실제 사용)
- 따라서 **자기 검수 루프는 돌릴 수 있다.** 단 검수는 반드시 `view_image` 를 거칠 것
- 결과물이 투박하면 **"더 강한 모델이 나을 것"** 이라고 정직하게 말할 것 (스킬 원문 요구사항)

**의존성:**
- `node` 필요 (render.mjs 계열) — 있음 ✅
- Remotion 팩(`remotion-video`)은 `npm i remotion` 필요 — 미설치

---

## 6. 실무 적용 순서 (권고)

1. **`javascript-animation` + `soundtrack`** 로 15~20초 파일럿 1편
   → 어제 트루먼쇼를 **같은 컨셉으로 재제작**해서 차이 측정
2. **`ad-video-skills`** 로 새미새론 광고 A~D편 제작
3. **`motion-design-skills`** 로 기본기(애니메이션 원칙·비트싱크·색) 보강
4. 매번 **`asset-audit` → `layout-check` → 컨택트시트 2패스** 를 통과시킬 것

---

## 7. 남은 과제

- [ ] 어제 트루먼쇼를 iart 스킬 기준으로 재제작 → **품질 차이 실측**
- [ ] 우리 3D 렌더러를 `starter.html` 템플릿에 이식 (iart 절차 + 우리 3D)
- [ ] `remotion-video` 팩 의존성 설치 여부 결정
- [ ] `webgl-animation-skills` / `data-animation-skills` 추가 검토

---

**루나(누나) · 2026-10-29 · 비교 후 채택 판단 · 전 식구 공유**
