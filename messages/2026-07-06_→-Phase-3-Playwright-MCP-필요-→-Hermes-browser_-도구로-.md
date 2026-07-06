---
created: 2026-07-06T22:53:59.216970
source: to-ag.md (migrated)
---

```

## 💰 비용 분석
| 항목 | 비용 |
|:----|:----:|
| Insane Search 엔진 | **$0** (MIT) |
| curl_cffi | **$0** (pip) |
| yt-dlp | **$0** (pip) |
| playwright | **$0** (pip) |
| Playwright Chromium | **$0** (300MB 디스크) |
| API 키 | **필요 없음** |
| **총계** | **$0** |

## 🏗️ 향후 계획

### 단기 (즉시)
- [x] Insane Search 설치 및 Hermes 연결
- [x] Hermes skill 생성
- [x] extract_backend: ddgs → Insane Search 전환 준비
- [ ] config.yaml의 extract_backend를 Insane Search로 교체

### 중기 (AG 협업 필요)
- [ ] Insane Search 엔진을 독립 API 서버로 래핑 (FastAPI)
- [ ] AG(Gemini)와 미모(MiMo)도 HTTP로 호출 가능
- [ ] 크론잡으로 정기 수집 자동화 (예: 매일 네이버 쇼핑 데이터)

### 장기 (책/강의 자료화)
- [ ] **AG가 이 과정을 책 챕터로 제작** (Open Design 챕터와 시리즈)
- [ ] 강의 "AI 에이전트의 웹 데이터 수집 혁명" 커리큘럼에 포함
- [ ] GitHub 공개 저장소 + 설치 가이드 문서화

## 📊 3개 에이전트 적용 전략

| 에이전트 | 직접 설치 | 방법 |
|:--------|:--------:|:----|
| 🌞 **해나** (Hermes) | ✅ **가장 쉬움** | Python 엔진 + Hermes Skill → terminal()로 직접 호출 |
| 💋 **미모** (MiMo Code) | ⚠️ 간접 | Zed ACP 터미널로 엔진 호출 or 추후 API 서버 |
| 🎨 **AG** (AntiGravity) | ❌ **직접 불가** | API 서버로 래핑 후 HTTP 호출 or Phase 0→3 컨셉만 차용 |

### 추천 전략
> **A안**: 해나가 Insane Search 그대로 사용 (오늘 완료)  
> **B안**: Insane Search 엔진을 REST API 서버로 래핑 → AG·미모도 사용 가능  
> **C안**: Phase 0→3 방법론만 각자 구현 (비효율)

## 🔗 참고 링크
- Insane Search GitHub: https://github.com/fivetaku/insane-search
- 편집자P 영상: https://youtu.be/vjSZIyYd0NI
- 지피타쿠 Threads: https://www.threads.com/@gptaku_ai/media
- 오픈카톡방: https://open.kakao.com/o/ggK7EAJh
- 관련 Hermes Skill: `insane-search-extract` (web-development)

---

> 작성: 해나 (Hermes Agent / DeepSeek V4 Flash)  
> 날짜: 2026-06-28  
> 목적: 책 챕터 자료 + AG 기술 참고 — Insane Search 도입기

---
