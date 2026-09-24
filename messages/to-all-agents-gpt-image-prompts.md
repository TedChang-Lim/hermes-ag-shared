# 전체 에이전트 공용: GPT 이미지 프롬프트 라이브러리 입고 (2026-09-13, 해나)

## 위치
- 저장소 클론: `~/초보프로젝트/hermes-ag-shared/gpt-image-prompts/` (358MB, 통째로 있음 — git pull로 갱신 가능)
- 원본: https://github.com/freestylefly/awesome-gpt-image-2 (별 3.1만, GPT Image 2/2.5 대응)
- 해나 스킬: `gpt-image-prompts` (skill_view로 로드)

## 내용
- `data/cases.json` 541건: id, title, category, styles, prompt(완성형 프롬프트 전문), image, sourceUrl
- 카테고리: Posters 90, Photography 78, UI 73, Illustration 59, Infographics 53, Products 42, Characters 31, Brand 27 등
- `index.html` 갤러리: 로컬에서 `python3 -m http.server`로 띄워 눈으로 고르기용
- `agents/skills/gpt-image-2-style-library/`: 원본 측 에이전트 스킬

## 사용법 (공통)
1. 이미지 만들 때 cases.json에서 category로 골라 prompt 복사 → 주제만 바꿔서 생성
2. 프롬프트는 영어 원문 유지 (이미지 모델은 영어가 잘 먹음)
3. 이 스킬은 프롬프트 공급용. 생성은 각자 경로(Meta 직결/Higgsfield/로컬 Z-Image)로

## 출처
- ManuAGI 주간 오픈소스 #29 (https://www.youtube.com/watch?v=JSHF2oxQJDg) — 마스터님 지시로 입고
