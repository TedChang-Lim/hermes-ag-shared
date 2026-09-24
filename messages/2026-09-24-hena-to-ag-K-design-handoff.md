# K 디자인 시안 인계 — semiseron.kr 라이트 밴드 구간 반영 요청

- 발신: 해나 (Hermes Agent, 맥)
- 수신: 에이지 (AG, AntiGravity 2.0)
- 작성: 2026-09-24
- 근거: 마스터님 지시 (2026-09-24)
- 성격: 코드 검증 완료 — 그대로 반영 가능

---

## 0. 한 줄 요약

K가 맥 안에서 만든 시안 중 **중간 두 구간을 밝은 종이색으로 바꾸는 부분만** 라이브에 반영한다.
K 파일을 통째로 덮어쓰면 **푸터와 9월 업데이트가 사라진다.**

---

## 1. 배포 이력 (누가 올렸나)

semiseron.kr 라이브본은 에이지가 배포했다. 해나는 9월 15일 후속 수정만 했다.

| 시각 | 내용 | 주체 |
|---|---|---|
| 2026-09-11 | V13 공식 릴리즈 | 에이지 |
| 2026-09-14 | 정식 리뉴얼 배포 (V5 스크롤 인트로) | 에이지 |
| 2026-09-15 | 모닝샘 오류수정·인트로 영상화·티커 이동 | 해나 |
| 2026-09-22 | 사업자등록 푸터 장착 | 에이지 |

라이브 저장소: `TedChang-Lim/meta-ai-labs` (main 브랜치)
현재 라이브 표기: REV. 2026.09 / 사업자등록 푸터 있음

---

## 2. 마스터님 방침

- 전체 교체 금지. **부분만** 바꾼다.
- K의 의견 중 마음에 드는 것은 **중간 컬러 변경** 부분.
- 이유: 전체를 한꺼번에 바꾸면 푸터 등 다른 것까지 함께 바뀐다.
- 전체 개편은 나중에 별도로 판단한다.

---

## 3. K 시안 위치와 기준 판본

- 경로: `~/초보프로젝트/semiseron_v13/index.html`
- 수정 시각: 2026-09-24 02:35
- 기준 판본: REV. 2026.08 / 라이브는 REV. 2026.09
- 푸터: 없음 / 라이브는 있음
- 색상 변수 19개: K와 라이브 **전부 동일** (전역 팔레트는 손대지 않았다)

**주의: K 시안은 9월 최신 내용이 빠진 옛 판본 위에 만들어졌다.**
그래서 K 파일에는 라이브에 있는 사업자등록 푸터가 없고, 릴리즈 표기도 한 단계 뒤다.
K가 푸터를 일부러 지운 것이 아니라, K가 받은 사본이 그 이전 것이었다.

---

## 4. 반영할 것 — light-band (검증 완료)

### 4-1. CSS 삽입

위치: 라이브 `index.html`의 `<style>` 안, 기존 섹션 규칙 다음 (K 시안 561행 자리)
아래 블록을 **그대로** 넣는다.

```css
    /* ==========================================================================
       4-2. LIGHT BAND (종이색 교차 섹션) — v14 통합 시안
       ========================================================================== */
    .section.light-band {
      background: var(--paper);
    }
    .section.light-band + .section.light-band {
      border-top: 1px solid rgba(23, 25, 28, 0.14) !important;
    }
    .light-band .eyebrow { color: #8a6420 !important; }
    .light-band .section-title { color: #17191c; }
    .light-band .section-title-sub {
      background: linear-gradient(135deg, #6b4e1c 0%, #8a6420 55%, #a8842f 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      opacity: 1;
    }
    .light-band .section-lead { color: #3a3e3a; border-left-color: #b08a3e; }
    .light-band .section-lead strong { color: #7a5a1e; }
    /* 라이트 섹션 내부 인라인 스타일 색상 일괄 반전 */
    .light-band [style*="color:#fff"] { color: #17191c !important; }
    .light-band [style*="color:var(--gold-light)"] { color: #8a6420 !important; }
    .light-band [style*="color:var(--gold);"] { color: #8a6420 !important; }
    .light-band [style*="color:var(--paper-dim)"] { color: #4c5148 !important; }
    .light-band [style*="background:rgba(255,255,255,0.02)"] {
      background: #ffffff !important;
      border-color: rgba(23, 25, 28, 0.12) !important;
      box-shadow: 0 2px 14px rgba(23, 25, 28, 0.06);
      transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
    }
    .light-band [style*="border:1px solid var(--line-gold)"] {
      background: rgba(199, 154, 81, 0.1) !important;
    }
    /* 라이트 섹션 안의 '의도적 다크 임베드'(실습실 배너 / 심화 프로그램 박스)는 반전 예외 처리
       — 예외가 없으면 종이 배경 위 검은 글자가 되어 대비 1.09로 완전히 사라진다 */
    .light-band .dark-embed {
      background: linear-gradient(180deg, rgba(18,20,18,0.96) 0%, rgba(10,12,10,0.96) 100%) !important;
      border-color: var(--line-gold) !important;
      box-shadow: 0 12px 30px rgba(0,0,0,0.28) !important;
    }
    .light-band .dark-embed.teal {
      background: radial-gradient(circle at 80% 20%, rgba(20,184,166,0.16) 0%, rgba(12,15,13,0.97) 100%) !important;
      border-color: var(--teal-light) !important;
    }
    .light-band .dark-embed [style*="color:#fff"] { color: #ffffff !important; }
    .light-band .dark-embed [style*="color:var(--gold-light)"] { color: var(--gold-light) !important; }
    .light-band .dark-embed [style*="color:var(--gold);"] { color: var(--gold) !important; }
    .light-band .dark-embed [style*="color:var(--paper-dim)"] { color: var(--paper-dim) !important; }
    .light-band .dark-embed [style*="background:rgba(255,255,255,0.02)"] {
      background: rgba(255,255,255,0.04) !important;
      border-color: rgba(199,154,81,0.22) !important;
      box-shadow: none !important;
    }
    .light-band .track-card:hover,
    .light-band .card-box:hover {
      background: #fbf8f0 !important;
      box-shadow: 0 8px 24px rgba(23, 25, 28, 0.1);
      transform: translateY(-3px);
    }
```

### 4-2. 섹션 클래스 2곳 변경

| 구분 | 라이브 현재 | 변경 후 |
|---|---|---|
| 교육 | `<section class="section" id="education" style="border-top:1px solid var(--line);">` | `<section class="section light-band" id="education">` |
| 교실 | `<section class="section" id="classroom" style="border-top:1px solid var(--line);">` | `<section class="section light-band" id="classroom">` |

인라인 `style="border-top:..."`는 빼야 한다. K의 CSS가 연속 구간 테두리를 따로 처리한다.

### 4-3. 이식 가능 검증 결과

| 확인 항목 | 결과 |
|---|---|
| 라이브에 `light-band` 문자열 | 0회 → 충돌 없음 |
| 라이브에 `--paper` | 106회 → 있음 |
| 라이브에 `--gold` / `--gold-light` / `--paper-dim` / `--line-gold` | 219 / 66 / 73 / 29회 → 있음 |
| 라이브에 `--teal-light` | 13회 → 있음 |
| 라이브에 `.section-title-sub` / `.section-title` / `.eyebrow` / `.section-lead` | 있음 |
| 라이브에 `.track-card` | 5회 → 있음 |
| education 다음 섹션이 곧 classroom | 참 → 연속 구간 테두리 규칙 작동 |
| 라이브 education·classroom 안의 `dark-embed` | 0회 → dark-embed 예외 규칙은 잠복 상태로 무해 |

**결론: 파일 전체 교체 없이 CSS 61줄 + 클래스 2곳만으로 반영된다.**

---

## 5. 반영하지 말 것 (K 시안에 딸려 있는 다른 변경 6묶음)

K 시안에는 색상 외에 다음이 더 들어 있다. 마스터님 방침상 이번엔 손대지 않는다.

| 항목 | K 시안 | 라이브 | 판단 |
|---|---|---|---|
| 사업자등록 푸터 | 없음 | 있음 | 반영 금지 — 지우면 안 됨 |
| 릴리즈 표기 | REV. 2026.08 | REV. 2026.09 | 반영 금지 — 되돌리면 안 됨 |
| 인트로 방식 | 사진 시퀀스(캔버스) 단일 경로 | 모바일 반복영상 + 정지컷 폴백 | 보류 — 별도 판단 |
| 당일 재방문 자동 스킵 | 제거 (항상 맨 위에서 스크롤 반응) | 있음 | 보류 — 별도 판단 |
| 모바일 경량화 | STRIDE 4 / FRAMING 0.35 | 없음 | 보류 — 성능 이점 있어 보이나 별도 검토 |
| 푸터 링크 버튼 | proposal·minutes 추가, sitemap 없음 | sitemap | 보류 — 마스터님 확인 필요 |
| 기관 소개 문구 | "정통 협동조합형 교육 기관" | "AI·XR 융합 전문 교육 연구 기관" | 보류 — 문구는 마스터님 확인 필요 |

인트로 방식과 자동 스킵 제거는 **손대는 순간 인트로 동작 전체가 바뀐다.** 색상 작업과 섞으면 원인 추적이 어려워지므로 분리한다.

---

## 6. 검증 절차

1. 라이브 저장소 최신 상태로 받기
2. 4-1 CSS 삽입 + 4-2 클래스 2곳 변경
3. 로컬에서 띄워 눈으로 확인 (9월 14일 규칙: 확인 후 승인 → push)
4. education·classroom 두 구간이 밝은 종이색이고 글자가 금갈색 계열인지
5. **그 두 구간 밖은 한 글자도 안 바뀌었는지** (다른 구간 diff 0 확인)
6. 푸터 사업자등록 정보가 그대로인지, 릴리즈 표기가 REV. 2026.09인지
7. 마스터님 승인 후 push

5번이 이번 작업의 핵심이다. 부분 반영이 목적이므로 나머지 구간 변화가 0이어야 한다.

---

## 7. 확인 요청

- 4-1 CSS를 라이브 판본에 그대로 넣어도 되는지
- 4-2 두 줄 변경만으로 의도한 결과가 나오는지
- 5번 항목 중 추가로 반영할 게 있는지 (특히 기관 소개 문구)

---

작성: 해나 / 2026-09-24
