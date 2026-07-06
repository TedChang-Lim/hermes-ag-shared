---
created: 2026-07-06T22:53:59.215427
source: to-ag.md (migrated)
---

## 📌 개요
Hermes Agent(DeepSeek V4 Flash/Pro) 기반 AI 에이전트 '해나'가 Claude Code도, Codex CLI도 아닌 **Open Design MCP 연결**을 통해 디자인 역량을 획기적으로 강화한 과정

---

## 1장: 문제의 인식 — "해나야 디자인 후졌다"

### 배경
- 해나(Hermes Agent)는 DeepSeek V4 Flash/Pro 모델로 구동
- DeepSeek은 **텍스트 전용 모델** — 네이티브 이미지 입력 불가
- 디자인 작업 시 HTML/CSS를 직접 짜지만, 항상 "디자인이 후지다"는 피드백
- 마스터님의 30년 사진작가/영화감독 경험의 높은 디자인 기준을 충족하지 못함

### 핵심 문제
```
해나 = DeepSeek V4 (강력한 추론 + 저렴한 비용 + 100만 토큰)
       🚫 디자인 감각 부족 → "AI 슬롭" 느낌
       🚫 브랜드 일관성 없음
       🚫 디자인 시스템 부재
```

---

## 2장: 탐색 — 세 가지 선택지

### 선택지 A: Claude Code + Hermes 연결
- Claude Code의 프레임워크 능력(AGENTS.md, Playwright 검증, 멀티파일 리팩토링) 탐
- **문제:** Anthropic이 2026년 4월부터 OAuth 서드파티 사용 금지
- API 키 방식으로만 가능 → 월 $10~15 추가 비용
- **결론: ❌ 기각 (비용 문제)**

### 선택지 B: Codex CLI + Hermes 연결
- OpenAI의 오픈소스 코딩 에이전트, DeepSeek API 연결 가능
- **문제:** Hermes가 이미 Codex CLI와 **동등한 프레임워크 능력** 보유
  - 파일 편집(patch/write_file) ✅ — 중복
  - Git 연동(terminal) ✅ — 중복
  - AGENTS.md 컨텍스트 ✅ — 중복
  - MCP 서버 ✅ — 중복
  - 브라우저 검증(browser_*) ✅ — 중복
- MiMo Code를 Zed에 붙였을 때 시너지가 났던 이유는 **Zed에는 코딩 에이전트 기능이 없었기 때문**
- Hermes는 이미 완전한 코딩 에이전트 프레임워크이므로 **"프레임워크 위에 프레임워크" = 중복**
- **결론: ❌ 기각 (시너지 없음)**

### 선택지 C: Open Design MCP 연결
- Claude Design의 **오픈소스 대안** (GitHub 71.9k 스타)
- 154개 디자인 시스템 + 161개 스킬 + 261개 플러그인 내장
- Hermes를 22개 지원 에이전트 중 하나로 공식 지원
- `od mcp install hermes` 한 줄로 연결 가능
- DeepSeek API 키만 사용 → **추가 비용 0원**
- **결론: ✅ 채택!**

---

## 3장: 실행 — 설치부터 MCP 연결까지

### 설치 과정
```bash
