# 🎨 Pollinations 무료 이미지 생성 — 전 에이전트 공용 (2026-08-12)

> **0원, API 키 불필요, 누구나 사용 가능.** 해나가 검증 완료 (2026-08-12 실측).

## 한 줄 요약
`polli-img "프롬프트"` 한 줄이면 **무료 이미지**가 생성됩니다. 모든 에이전트(해나·코코·미모·지호·AG·루나)가 같은 Mac에서 이 스크립트를 사용할 수 있습니다.

## 사용법 (터미널에서)

```bash
# 스크립트 경로: ~/초보프로젝트/hermes-ag-shared/scripts/polli-img
# 또는 복사: cp ~/초보프로젝트/hermes-ag-shared/scripts/polli-img ~/bin/

~/bin/polli-img "강아지가 모자를 쓴 모습" dog.png          # 기본 1024x1024
~/bin/polli-img "원주 치악산 가을 풍경" chiak.png 1024 768  # 가로x세로 지정
```

## 동작 원리

- 엔드포인트: `https://image.pollinations.ai/prompt/{URL인코딩된 프롬프트}?width=W&height=H&nologo=true&seed=N`
- **API 키 없음**, **무료**, 무제한에 가까움 (rate limit만 존재)
- 한글 프롬프트 지원 (URL 인코딩 자동 처리)
- 생성물: JPEG (기본), 모델 변경 가능 (`&model=flux` 등 파라미터)

## 주의사항

- ⚠️ **OmniRoute 경유(pol/*)는 사용하지 말 것** — 이미지 엔드포인트가 API 키를 요구하고 midijourney는 텍스트로 분류됨 (2026-08-12 확인). **직접 호출이 정답.**
- 생성에 5~30초 소요. 실패 시 재시도 (seed 변경).
- 상업적 이용 가능 (Pollinations는 무료 오픈 플랫폼, MIT 계열).

## 에이전트별 사용 예

| 에이전트 | 방법 |
|---|---|
| 해나 (Hermes) | `terminal` → `~/bin/polli-img "프롬프트" out.png` |
| 코코 (Claude Code) | `~/초보프로젝트/hermes-ag-shared/scripts/polli-img "프롬프트" out.png` |
| 미모/지호/AG/루나 | 동일 (같은 Mac) |

## 검증 기록 (2026-08-12)

- `curl "https://image.pollinations.ai/prompt/a%20red%20apple%20on%20white%20table?width=512&height=512"` → 512x512 JPEG ✅
- `polli-img "원주 치악산의 아름다운 가을 풍경..."` → 1024x1024 ✅ (한글 지원 확인)

## 스킬
Hermes 스킬 `pollinations-image-gen`에도 동일 스크립트 포함 (skill_view로 로드 가능)
