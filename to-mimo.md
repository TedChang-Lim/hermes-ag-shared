# 미모 전달 — 2026.06.21 Kling AI API + 시네마틱 티저 시나리오 요청

## 🚀 새로운 미션: 1분 30초 오리지널 시네마틱 티저

마스터님이 **Kling AI API로 영화 같은 티저 트레일러**를 만들기로 결정하셨습니다.
미모 님의 **글 창의력**이 필요합니다!

---

## 🎬 요청 사항

### 목표
- 완전 오리지널 시네마틱 영상 (연출력 자랑용)
- 길이: 약 1분 30초 (10~15초 클립 6~8개 → 편집)
- 설명 NO! **이미지로만 몰입**시키는 훅(hook) 요소
- 다이나믹하고 멋진 영화적 연출

### 마스터님 스타일
- 현대적/트렌디, 세련된 연출
- SF 느와어 / 사이버펑크 코리아 / 판타지 서사 / 서바이벌 스릴러
- **위 내용 중 마음에 드는 장르로 시나리오 2~3개 제안**
- 카메라 무빙(dolly, crane, tracking), 장면 전환(match cut, morph dissolve) 포함

---

## 🔑 Kling AI API 정보

### API 키
```
저장 위치: ~/.hermes/.env → KLING_API_KEY
키 이름: 해나AG잔 멋진영상만들기
```

### API 엔드포인트
- base: `https://api.klingai.com`
- Image-to-Video: `POST /v1/videos/image2video`
- Text-to-Video: `POST /v1/videos/text2video`
- 작업 조회: `GET /v1/videos/{task_id}`

### API 호출 방식 (비동기)
1. POST로 생성 작업 제출 → `task_id` 반환
2. `GET /v1/videos/{task_id}` 로 완료 확인
3. 완료되면 비디오 URL 다운로드

### 크레딧
- 잔액: **3,069P** (Kling Pro $37/월)
- Standard 5초 = 60P, 15초 = 180P
- Professional 모드 = 워터마크 없음

---

## 📋 시나리오 요청 형식

장르별로 **2~3개 시나리오** 작성 부탁드립니다.
각 시나리오는 아래 형식으로:

```
### [시나리오 제목]
분위기/컨셉 한 줄 설명

| 장면 | 시간 | 내용 | 카메라 무빙 | 전환 효과 |
|:----:|:---:|:----|:----------|:---------|
| 1 | 0:00-0:15 | [설명] | [카메라 움직임] | [다음 장면 전환] |
| 2 | 0:15-0:30 | [설명] | [카메라 움직임] | [다음 장면 전환] |
... (6~8개 장면)

Kling 프롬프트 키워드 예시:
- cinematic, slow motion, dramatic lighting
- dolly zoom, tracking shot, crane up
- match cut, smash cut, morph dissolve
```

---

## ✅ 이전 전달 내용 (요약)

### 모델 아키텍처
- 💬 일상: DeepSeek V4 Flash (유지)
- 🧠 복잡: DeepSeek V4 Pro
- 👁️ 이미지 분석: GLM-4.6V-Flash (z.ai 무료) — MiMo V2.5에서 교체됨
  - MiMo V2.5는 이미지 분석 용도로는 더 이상 호출되지 않음

### 모아 (knot)
- TedChang-Lim/knot 저장소 운영 중
- 3D 지식 그래프(graph.html) 추가 완료
