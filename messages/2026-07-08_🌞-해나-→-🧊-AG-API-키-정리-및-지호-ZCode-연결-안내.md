# 🌞 해나 → 🧊 AG · API 키 정리 + 지호(ZCode) 연결 완료

**날짜:** 2026-07-08

---

AG가 복귀하면 참고할 내용이야.

## 1. API 키 종합 가이드 생성

모아 위키에 모든 API 키를 정리한 `api-keys.md` 생성 완료.
- **위치:** `~/초보프로젝트/모아/wiki/api-keys.md`
- 실제 키 값은 `~/.hermes/.env`에 보관

---

## 2. 지호(ZCode) 등장

마스터님이 ZCode Agent의 이름을 **지호**로 지으셨어.
- **엔진:** Hy3(Tencent 295B MoE, OpenRouter 경유, 7/21까지 무료)
- **연결:** ZCode → Model Settings → OpenRouter → `tencent/hy3:free`
- **기능:** ZCode의 플러그인/MCP/스킬/서브에이전트 모두 Hy3로 사용 가능

---

## 3. Higgsfield MCP — ZCode에 등록했으나 OAuth 문제

Higgsfield MCP 서버를 ZCode(지호)에 등록했지만 OAuth 인증 오류 발생.
크레딧도 소진된 상태라 재충전 필요.

---

## 4. 에이전트 팀 업데이트

| 이름 | 플랫폼 | 엔진 | 상태 |
|:----|:-------|:----|:----:|
| 🌞 해나 | Hermes | DeepSeek V4 Flash | ✅ 활성 |
| 💋 미모 | Zed | MiMo 2.5 Pro | ✅ 활성 |
| 🧊 지호 | ZCode | Hy3 (7/21까지 무료) | ✅ 활성 (신규) |
| 🧊 AG | Gemini | Gemini Pro | ❌ 한도 소진 (7월) |
| ❄️ Q | Qwen | Qwen 3.7 Plus | 대기 |

---

AG 한도 복구되면 보고 참고해줘!