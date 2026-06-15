# 🤖 해나 → AG 전달사항 (2026.06.16) - Figma MCP 시도 결과

AG야, 오늘 마스터님이랑 이것저것 많이 했어. 공유할게!

---

## 1️⃣ Higgsfield MCP — 검토 완료, 설치 대기 중

우리가 이미 공유했던 내용 그대로:
- **Hermes Agent 공식 지원 확인** (higgsfield.ai/cli)
- 30개+ 영상 모델, 4K, 15초
- 설치: CLI 설치 → 로그인 → MCP 등록 → 사용
- 마스터님 승인만 받으면 바로 진행 가능

---

## 2️⃣ Figma MCP — 시도했으나 연결 문제 발생

### 시도한 것
1. **figma-mcp-go (오픈소스, ★1.1k)** 설치
   - npx로 서버 실행 ✅ (127.0.0.1:1994 정상 리스닝)
   - Figma Desktop에 플러그인 설치 ✅ (Import plugin from manifest)
   - **연결 실패** ❌ → 계속 "Disconnected"
   
2. 원인 파악 결과:
   - GitHub 이슈 #50에 **동일한 문제 보고됨** (4일 전)
   - "Cannot connect using claude code / keeps showing Disconnected"
   - 아직 fix 안 됨

3. 공식 Figma MCP 서버 시도:
   - `@figma/mcp-server` npm에 없음 (Figma가 Claude/Codex 전용으로만 제공)

### 결론
- figma-mcp-go의 버그로 보임
- 버그픽스 나오면 재시도 예정
- 대안: Figma REST API 직접 호출 (Access Token 방식) 고려 가능

---

## 3️⃣ GBrain — 검토 완료

- YC CEO Garry Tan이 만든 AI 메모리 시스템
- 마크다운 기반 지식 그래프 (self-wiring)
- Hermes 지원 명시
- **결론: 지금은 불필요. 필요해지면 설치.**

---

## 4️⃣ Hermes Studio v0.6.15 업데이트 완료

- 채팅 사이드바 리디자인
- 스킬 명령어 선택기 추가
- Claude/Gemini OAuth 로그인 지원
- config.yaml 모델 목록 자동 새로고침
- Thinking 표시 개선 등

---

## 5️⃣ AI 디자인 코덱스 영상 분석

- **영상**: "진짜 소름... AI 디자인 코덱스가 판도를 바꿉니다"
- **채널**: 김효율의 AI 개발단 (조회수 16만)
- **핵심**: Figma AI 플러그인 (Relume, Galileo AI 등)으로 이미지 → 프로토타입 → 코드 자동 변환
- **결론**: Figma MCP만 연결되면 우리도 가능!

---

참고해서 작업해! 🔥
