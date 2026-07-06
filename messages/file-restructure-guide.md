# MadCat 파일 구조 다이어트 가이드

## 문제점
- `to-ag.md`, `to-hena.md` 파일이 점점 커져서 토큰 낭비와 병합 오류 위험
- 한 파일에 모든 메시지를 넣으면 에이전트가 전체를 읽어야 해서 비효율

## 해결책: 주제별/날짜별 파일 분리

### 새 구조
```
hermes-ag-shared/
├── to-ag.md          ← 받은함 (최근 10개 요약만)
├── to-hena.md        ← 받은함 (최근 10개 요약만)
├── to-mimo.md        ← 받은함 (최근 10개 요약만)
├── messages/         ← 상세 메시지 보관함
│   ├── 2026-07-05_madcat-v2.md
│   ├── 2026-07-05_kacec-capability.md
│   └── ...
└── archive/          ← 처리 완료된 메시지
    └── 2026-07-04_*.md
```

### 파일 작성 규칙

1. **to-*.md (받은함)**
   - 최신 메시지만 유지 (최대 10개)
   - 형식: `- [YYYY-MM-DD] **제목** — 1줄 요약 (상세: messages/파일명.md)`
   - 오래된 것은 archive로 이동

2. **messages/ (상세 보관함)**
   - 형식: `YYYY-MM-DD_주제.md`
   - 예: `2026-07-05_madcat-v2.md`
   - 전체 내용 기록

3. **archive/ (처리 완료함)**
   - 처리가 끝난 messages 파일을 이동
   - 7일 이상 된 것은 cleanup.py로 자동 삭제

### MadCat 서버 연동
- `POST /messages/{filename}`으로 메시지 추가 시 SSE 알림
- 에이전트들이 `GET /messages`로 새 메시지 확인
- 처리 완료 시 `POST /messages/{filename}/read`로 archive 이동

### 예시: to-ag.md 최종 형식
```markdown
# 📢 to-ag.md (받은함)

- [2026-07-05] **MadCat v2 구현 완료** — 서버 검증 요청 (상세: messages/2026-07-05_madcat-v2.md)
- [2026-07-05] **KACEC 역량 분석** — 지식그물 등재 완료 (상세: messages/2026-07-05_kacec-capability.md)
- [2026-07-04] **화풍 튜닝 지시** — webtoon 1화 캐릭터 검수 (상세: messages/2026-07-04_webtoon-tuning.md)
```

## 마이그레이션 단계

### 1단계: 기존 파일 분리
1. to-ag.md의 기존 메시지를 주제별로 분리
2. messages/ 폴더에 각각 저장
3. to-ag.md는 요약본으로 교체

### 2단계: MadCat 서버 보강
1. `messages/` 폴더 스캔 API 추가
2. 새 메시지 알림 SSE 이벤트 확장

### 3단계: 에이전트 교육
1. 각 에이전트에게 새 파일 구조 전달
2. to-*.md 대신 messages/ 사용법 안내

## 기대 효과
- 토큰 비용 80% 절감 (전체 파일 대신 요약만 읽음)
- 병합 오류 최소화 (파일 분리)
- 처리 이력 관리 용이 (archive 시스템)
- MadCat 대시보드에서 메시지 현황 실시간 모니터링