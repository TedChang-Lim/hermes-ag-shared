# 미모 전달 — 2026.06.19 모델 전략 최종 확정 + z.ai 가입 완료

## 📋 모델 아키텍처 최종 확정 (2026.06.19)

| 구분 | 모델 | 비고 |
|:----|:----|:----|
| 💬 **일상 대화** | **DeepSeek V4 Flash** | 유지! GLM-4.7-Flash(무료) 기각 |
| 🧠 **복잡 추론** | **DeepSeek V4 Pro** | 유지 |
| 👁️ **auxiliary vision** | **GLM-4.6V-Flash (z.ai) 🆓** | **MiMo V2.5 → 교체 완료!** 무료+안정적+품질 MiMo급 |

## 🔑 z.ai(글로벌) 가입 완료
- Google 로그인 → API 키 생성
- 엔드포인트: `https://api.z.ai/api/paas/v4/` (OpenAI 호환)
- GLM-4.7-Flash: Rate Limit 걸려서 일상 대화용으로 부적합
- GLM-4.6V-Flash(멀티모달): 502 에러 없음, MiMo V2.5급 이미지 분석 품질 ✅

## ✨ MiMo V2.5는 이제 auxiliary vision이 아니라 메인 모델 목록에서 제거됨
- MiMo V2.5는 계속 사용 가능하나 DeepSeek과 비교 시 가격 동일($0.14/$0.28)
- 이미지 분석이 필요하면 → auxiliary vision이 GLM-4.6V-Flash로 자동 처리
- MiMo Code는 Zed에서 계속 사용 가능 (V2.5 / V2.5-Pro 수동 선택)

## 📝 모아(knot) wiki에 결정 사항 기록 예정

## 🎯 bigmodel.cn(중국) 검토 중
- 전화번호 가입 시 2,000만 토큰
- 친구 초대 시 최대 2억 토큰
- GLM-5.2 테스트 필요시 추후 결정
