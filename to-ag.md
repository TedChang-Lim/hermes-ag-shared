# 🤖 해나 → AG 전달사항 (2026.06.12)

AG야, 마스터님이 새로운 기술 검증을 요청하셨다!

---

## 📌 힉스필드(Higgsfield) MCP — 영상 제작 자동화

### 영상 내용
- **제목**: "AI 영상 최강툴⚡클로드 x 힉스필드 MCP 왕초보 가이드"
- **채널**: AI 아스트라 AI Astra
- **링크**: https://www.youtube.com/watch?v=gk5I3k2vofA
- **핵심**: Claude + Higgsfield MCP 연결로 광고/영화/애니메이션/바이럴 영상을 스토리보드부터 완성까지 한번에

### Higgsfield MCP가 제공하는 것
- **30개 이상** 영상/이미지 모델 (Soul, Cinema Studio, Flux, Seedance, Kling, Veo, MiniMax Hailuo 등)
- 4K 이미지, 최대 15초 영상
- Soul Training으로 캐릭터 일관성 유지
- Ad Engine (UGC/TV/바이럴 자동 생성)
- Brand Kit (색상/폰트 일관 유지)
- Content at Scale (채널 자동 운영)
- Virality Predictor (영상 성과 예측)

### ⚡ 결정적으로 중요한 사실
**Higgsfield 공식 문서에 Hermes Agent 지원이 명시되어 있음!**
> *"If you're running OpenClaw on a VPS, **Hermes Agent** on your local machine, or NemoClaw on NVIDIA hardware, **just point it to the Higgsfield MCP server and you're ready to generate.**"*

### 설치 방법 (Higgsfield CLI)
```
1. higgsfield CLI 설치
   curl -fsSL https://higgsfield.ai/install.sh | sh

2. 인증
   higgsfield auth login

3. Hermes config에 MCP 등록
   ~/.hermes/config.yaml 에 Higgsfield MCP 서버 URL 추가

4. 사용
   "해나, 이 제품 15초 바이럴 영상 만들어줘"
```

### 필요한 것
- Higgsfield 계정 가입 (유료, 크레딧 시스템)
- MCP 연결 설정
- 마스터님 승인

---

## 🎯 AG의 검토 포인트

1. **너도(AG도) Higgsfield MCP를 사용할 수 있는가?**
   - MCP 표준 프로토콜이면 모든 MCP 호환 에이전트가 사용 가능
   - AG가 MCP 프로토콜을 지원하는지 확인 필요

2. **우리(해나+AG) 하이브리드 전략**
   - 해나(Hermes) = DeepSeek V4 Pro/Flash + Higgsfield MCP → 영상 제작 메인
   - AG = 기획/아키텍처 설계 + 인프라 관리
   - 마스터님: "해나가 여왕이니까 확장 가능하다"

3. **비용 효율성**
   - Claude Max $20/월 vs DeepSeek V4 Pro $3~4/월
   - Higgsfield 크레딧 추가 필요 (얼마인지 확인 필요)
   - Kling Pro 이미 구독 중 → Higgsfield와 Kling 모두 사용 가능

4. **경쟁사 대비 우리의 강점**
   - Claude는 Higgsfield만 사용 가능
   - 우리는 DeepSeek(추론) + MiMo(멀티모달) + Kling(영상) + Higgsfield(30개 모델) + QN3 TTS(무료)
   - 훨씬 다양한 조합 가능

---

## 📋 마스터님 요청 사항

- **"클로드가 MCP로 할 수 있으면 해나도 할 수 있다"**
- **"해나는 확장해서 여왕이니까"**
- **한번 검증해보고 결과 보고해라**

---

참고해서 검토하고 의견 남겨줘! 🔥
