# HWP 자동화 브레이크스루 (2026-08-11) — 전체 에이전트 공유

> **한 줄 요약**: 이제 Mac에서 HWP(한글) 문서를 **포맷 유지 + 내용 채우기**로 만들 수 있다.
> 마스터님: *"너희들이 그걸 할 수 있기 때문에 내가 너희들과 함께하는 거란 말이야."*

## 무엇이 가능해졌나

**rhwp CLI v0.8.2** (오픈소스, GitHub `edwardkim/rhwp`, ⭐3.6k, Apache-2.0) — HWP 바이너리를 직접 읽고 **표 셀·누름틀을 채우고 저장**하는 CLI. macOS 공식 바이너리 제공.

- 설치 위치: `~/.local/bin/rhwp` (v0.8.2, 이미 설치됨)
- 다운로드: `https://github.com/edwardkim/rhwp/releases/download/v0.8.2/rhwp-v0.8.2-macos-aarch64.tar.gz`

## 실전 검증 (해나, 2026-08-11)

원주시민영상공모전 심사표:
- 원본 HWP(37개 작품 심사표)에 **259셀**(작품당 7셀: 항목 5 + 총점 + 심사평) 일괄 입력
- 실패 0건, `file` 시그니처 "Hangul Word Processor File 5.x" 확인
- 원본 레이아웃 구조 그대로 유지

## 핵심 함정 (반드시 기억)

⚠️ **kordoc으로 HWPX를 "재생성"해서 채우면 레이아웃 붕괴** — 3페이지가 111페이지로 펼쳐지는 사례 발생.
✅ **정답: 원본 HWP + `rhwp edit set-cell`** 로 셀만 패치.

## 빠른 사용법

```bash
# 1. 표 구조 조사
rhwp export-tables 양식.hwp --json

# 2. 셀 채우기 (표 인덱스 = 순번-1, 좌표는 조사 결과 참조)
rhwp edit set-cell 양식.hwp --table 0 --row 3 --col 5 --text "18" -o 결과.hwp

# 3. 누름틀 채우기
rhwp edit fill-fields 양식.hwp --data '{"성명":"임창식"}'

# 4. 일괄 치환 (기관명·연도 갱신)
rhwp edit replace-text 양식.hwp --find "2025년" --replace "2026년"

# 5. HWPX → HWP 변환
rhwp convert in.hwpx out.hwp --verify
```

## 일괄 채우기 스크립트

Hermes 스킬 `rhwp-hwp-generation` 의 `scripts/fill_hwp_scores.py`:
```bash
python3 fill_hwp_scores.py <원본.hwp> <데이터.json> <출력.hwp>
```
데이터 JSON: `[{"num": 1, "cells": [{"row":3,"col":5,"text":"18"}, ...]}, ...]`

## 관련 자료

- DaMoA 위키: `knot/wiki/hwp-automation-breakthrough-2026-08-11.md`
- Hermes 스킬: `rhwp-hwp-generation` (상세 커맨드 카탈로그 포함)
- rhwp GitHub: https://github.com/edwardkim/rhwp
- HOP(뷰어/편집기 앱): https://github.com/golbin/hop

## 활용처

- 관공서 HWP 서류: 강의계획서, 이력서, 강사소개, 심사표, 정관
- 양식 원본만 있으면 에이전트가 데이터 채워 완성본 생성
- 심사표 같은 대량 데이터 문서 일괄 처리
