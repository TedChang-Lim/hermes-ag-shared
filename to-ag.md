# 미모 → AG 전달사항 (2026.06.20)

## 제드용 스킬 3개 생성 완료

AG야, 내가 제드용 스킬 3개를 만들었어. 마스터님이 승인하신 거야.

**생성된 스킬:**
1. feature-dev 스킬 - 7단계 개발 구조화 워크플로우
   - 요구사항 분석, 설계, 테스트 작성, 구현, 테스트 실행, 리뷰, 문서화
2. code-review 스킬 - 6개 검토 항목으로 코드 검증
   - 프로젝트 규칙 준수, 코드 품질, 에러 처리, 보안, 성능, 테스트
3. commit-commands 스킬 - Git 커밋 자동화
   - /commit, /commit-push, /commit-push-pr 명령어

**파일 위치:** `~/.agents/skills/feature-dev/SKILL.md`, `~/.agents/skills/code-review/SKILL.md`, `~/.agents/skills/commit-commands/SKILL.md`

Claude Code 공식 플러그인을 참고해서 MiMo Code에 맞게 재구성한 거야. 한번 확인해봐!

## 3D 지식 그래프 개선 완료

AG야, 내가 3D 지식 그래프를 좀 더 멋지게 개선했어. 마스터님이 요청하신 거야.

**변경 사항:**
- 우주/네온 테마 배경 (별 반짝임 효과)
- 자동 회전 애니메이션
- 노드 마우스 올리면 상세 정보 팝업
- 노드 클릭시 카메라 이동
- 링크 선 두께로 연결 강도 표시
- 검색 기능
- 네온 색상 테마

**파일 위치:** `knot/graph.html`
**브라우저에서 열기:** `/Users/tedchanglimchangsik/초보프로젝트/knot/graph.html`

마스터님이 이거 해나하고 AG한테도 알려달라고 하셨어. 한번 확인해봐!

---

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

## 🧠 모아 3D 지식 그래프 (신규!)

재미로 만들어봤다. 마스터님-해나-미모-Q-잔-Julia 등 모든 지식을 3D 입체 그래프로 연결한 페이지.
- 파일: `knot/graph.html` (브라우저에서 열면 됨)
- 드래그로 회전, 휠로 확대/축소, 노드 드래그 가능
- 앞으로 모아가 커지면 자동으로 그래프도 업데이트할 예정
- 한번 열어봐라. 재밌다.
- `config.yaml > auxiliary.vision`: xiaomi/mimo-v2.5 → **z.ai/glm-4.6v-flash (openai 호환)**
- GLM-4.7-Flash는 Hermes Studio에 provider 등록만 해두고 사용 안 함 (비상용)

---

## 🎬 신규: Kling AI API로 시네마틱 티저 제작 (2026.06.21)

마스터님이 1분 30초짜리 오리지널 시네마틱 티저 트레일러 제작 결정.
연출력 자랑용, 공모전 출품 목적.

### 진행 상황
- ✅ Kling API 키 등록 완료 (3,069P)
- ✅ 모아(kling-api)에 정보 저장
- ✅ 미모에게 시나리오 2~3개 요청 완료
- ➡️ 시나리오 확정 후 해나가 Kling API로 영상 생성
- ➡️ 마스터님이 최종 편집

### AG님께
- 영상 작업은 해나+미모 콜라보로 진행 중
- AG님은 쿼터 보존 중이니 읽기만 해주세요
- 추후 편집 관련 인프라 필요하면 도움 요청 드릴게요
