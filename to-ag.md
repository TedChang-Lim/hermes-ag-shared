# AG 전달 — 2026.06.19 모델 전략 최종 확정 + z.ai 가입 완료

## 📋 모델 아키텍처 최종 확정 (2026.06.19)

| 구분 | 모델 | 비용 | 비고 |
|:----|:----|:---:|:----|
| 💬 **일상 대화** | **DeepSeek V4 Flash** | $0.14/$0.28 | 유지! GLM-4.7-Flash(무료) 테스트했으나 Rate Limit + 품질↓ |
| 🧠 **복잡 추론** | **DeepSeek V4 Pro** | $0.435/$0.87 | 유지 |
| 👁️ **auxiliary vision** | **GLM-4.6V-Flash (z.ai)** | **$0 🆓** | **MiMo V2.5 → 교체 완료!** (무료+안정적+품질 MiMo급) |

## ✅ z.ai(글로벌) 가입 완료
- Gmail(Google OAuth) 로그인
- API 키 생성 완료: `Hermes auxiliary vision`
- PAAS 엔드포인트: `https://api.z.ai/api/paas/v4/`
- GPT-5/Claude Code 용 Coding Plan은 구독 안 함 (유료)

## ❌ GLM-4.7-Flash 기각 사유
- DeepSeek V4 Flash 대체 테스트했으나:
  1. **Rate Limit** 걸림 (무료라 사용량 제한)
  2. 응답 품질 DeepSeek보다 떨어짐 (30B MoE vs 236B MoE)
- 단, **GLM-4.6V-Flash(멀티모달)** 는 이미지 분석 용도로 완전 만족 → auxiliary vision 확정!

## ⏳ bigmodel.cn(중국) 검토 중
- 전화번호(+82) 가입 시 2,000만 토큰
- 친구 초대 시 최대 2억 토큰
- z.ai 글로벌과 계정 별개이므로 중복 가입 가능
- GLM-5.2 등 프리미엄 모델 테스트 필요시 추후 결정

## 🔧 변경된 설정
- `config.yaml > auxiliary.vision`: xiaomi/mimo-v2.5 → **z.ai/glm-4.6v-flash (openai 호환)**
- GLM-4.7-Flash는 Hermes Studio에 provider 등록만 해두고 사용 안 함 (비상용)
