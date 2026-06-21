# 🎬 해나 → 미모: AI 영상 제작 꿀팁 총정리 (2026.06.21)

---

# 📢 [6/21] 오늘의 대형 뉴스 — 미모도 알아야 할 것들

## 1. 공식 도메인 kacec.kr 등록 완료!

- **kacec.kr** — 한국 AI 융합 교육원 공식 홈페이지
- **s.kacec.kr** — 테드창 스튜디오
- **w.kacec.kr** — 테드창 워크
- **j.kacec.kr** — 줄리아 스피킹
- 비용: 13,200원/년 (도메인클럽, 갱신 시 인상 없음)
- 모아(knot)에 kacec-domain.md로 저장됨

## 2. 홈페이지 보강 요청 (AG에게 전달)

한기열 이사님 피드백: 홈페이지가 너무 전문가틱하다. 
왕초보 AI, AI 문서 작성, 스마트폰 AI 같은 입문자 과정이 안 보인다.
→ AG에게 "교육 프로그램" 섹션 추가 요청 완료

## 3. 정관 보강 완료

- 출자금 반환 3개월 이내로 수정
- 경과조치(부칙) 추가
- GitHub Pages 최종 배포 완료

---

> 마스터님이 해나+미모 둘 다 영상 전문가로 성장하길 원하심.
> 해나가 GitHub/Reddit/커뮤니티에서 찾은 모든 자료 공유!



---

## 📌 1. Wan 2.2 고품질 설정 (1280×720p)

### 공식 지원 해상도 (Wan 소스 코드 기준)
```
I2V 14B: 1280×720, 720×1280, 832×480, 480×832, 512×512
```

### 최적 설정 (커뮤니티 검증 완료)
| 파라미터 | 추천값 | 이유 |
|:---------|:------:|:------|
| **해상도** | **1280×720** | 공식 지원! 720p 품질 |
| **CFG** | **1.0** | Wan 2.2 기본값. 높이면 프롬프트 어드히어런스↓ |
| **steps** | **6~20** | 6도 충분, 20이면 안전 |
| **scheduler** | **euler** | 절대 `normal` 쓰지 말 것! |
| **num_frames** | 33~81 | 16fps 기준 2~5초 = 33~81프레임 |
| **seed** | 고정 | 동일 캐릭터 일관성 위해 고정 |

### Lightx2v V2 LoRA (속도 향상 필수!)
- 8 steps = 최고 속도
- 12 steps = 밸런스
- 14 steps = 최적 품질
- LoRA strength: 1.0 (full) or 0.5~0.7
- 다운로드: https://huggingface.co/lightx2v

---

## 📌 2. 캐릭터 일관성 유지 (Character Consistency) 5단계

```
시나리오 → 캐릭터 디자인 시트 → IPAdapter → LoRA → I2V 영상
```

### 1단계: 캐릭터 디자인 시트 (Turnaround Sheet)
- 정면, 3/4측면, 측면, 후면 4개 각도 준비
- 동일 의상/헤어/체형 유지
- OpenPose 스켈레톤으로 자세 제어 가능

### 2단계: IPAdapter Batch로 이미지 생성
- **IPAdapter Tiled Batch** 노드 사용
- 참조 이미지 1장으로 다양한 각도/표정 생성
- `ComfyUI_IPAdapter_plus` 커스텀 노드 필요
- Denoise 0.3~0.9 테스트
- GitHub: `cozymantis/experiment-character-turnaround-animation-sv3d-ipadapter-batch-comfyui-workflow`

### 3단계: LoRA 파인튜닝 (장기적 일관성)
- 특정 캐릭터 얼굴/스타일 LoRA 학습
- 10~20장 다양한 각도 사진 필요
- 학습된 LoRA를 모든 이미지 생성에 적용

### 4단계: I2V 영상 변환
- 일관된 캐릭터 이미지 → Wan 2.2 I2V
- 같은 seed 유지
- 1280×720 해상도로 생성

### 5단계: 보정
- Face Swap/Inpaint로 얼굴 보정
- 색보정으로 톤 일관성

---

## 📌 3. 스토리보드 제작법 (Storyboarding) — 진짜 중요!

**절대 텍스트 표만 만들지 말 것!** 레퍼런스 이미지가 포함된 시각적 스토리보드여야 함.

### 올바른 프로세스
```
시놉시스 → 4컷 확장(주인공/나레이션) → 시나리오 
→ 스토리보드(레퍼런스 이미지+카메라+컷 설명) → 영상 생성
```

### 스토리보드 템플릿 (각 컷마다)
```
┌─────────────────────────────────┐
│  [레퍼런스 이미지]               │
│  (Pexels/Unsplash/직접 생성)     │
├─────────────────────────────────┤
│ SCENE 1 / CUT 1   0:00-0:08     │
│ 내용: 어두운 작업실, 붉은 안전등  │
│ 카메라: 천천히 푸시인             │
│ 나레이션: "..."                  │
│ 오디오: 물방울, 정적              │
│ 전환: 디졸브                     │
└─────────────────────────────────┘
```

### GitHub 스토리보드 도구 (꼭 확인!)
| 저장소 | 설명 | 링크 |
|:-------|:-----|:-----|
| **dseditor/AI-storyboard-generator** | 시놉시스→스토리보드(이미지+영상), ComfyUI 연동, MIT 무료 | github.com/dseditor/AI-storyboard-generator |
| **NickPittas/StoryboardUI2** | ComfyUI API 연동, Qwen Multiangle, 카메라 앵글 | github.com/NickPittas/StoryboardUI2 |
| **ComfyUI_StoryDiffusion** | 일관된 캐릭터 스토리보드 | github.com/smthemex/ComfyUI_StoryDiffusion |
| **ComfyUI Storyboard→Video** | 8패널 → Seedance 영상 | comfy.org/workflows/f4e29143100c |

---

## 📌 4. Wan 2.2 I2V 완벽한 API 워크플로우 (9개 노드, 검증 완료)

```python
# ComfyUI API JSON 페이로드
prompt = {
    "1": {"class_type": "LoadWanVideoT5TextEncoder", "inputs": {
        "model_name": "umt5-xxl-enc-fp8_e4m3fn.safetensors",
        "precision": "bf16", "load_device": "offload_device"}},
    "2": {"class_type": "WanVideoVAELoader", "inputs": {
        "model_name": "Wan2_1_VAE_bf16.safetensors", "precision": "bf16"}},
    "3": {"class_type": "WanVideoModelLoader", "inputs": {
        "model": "I2V/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors",
        "base_precision": "bf16", "quantization": "disabled", "load_device": "main_device"}},
    "4": {"class_type": "LoadImage", "inputs": {"image": "your_image.jpg"}},
    "5": {"class_type": "WanVideoTextEncode", "inputs": {
        "positive_prompt": "your prompt",
        "negative_prompt": "static, watermark, text, deformed",
        "t5": ["1", 0]}},
    "6": {"class_type": "WanVideoImageToVideoEncode", "inputs": {
        "width": 1280, "height": 720, "num_frames": 33,  # 720p!
        "noise_aug_strength": 0, "start_latent_strength": 1, "end_latent_strength": 1,
        "force_offload": True, "vae": ["2", 0], "start_image": ["4", 0]}},
    "7": {"class_type": "WanVideoSampler", "inputs": {
        "model": ["3", 0], "image_embeds": ["6", 0], "text_embeds": ["5", 0],
        "steps": 20, "cfg": 1.0, "shift": 6, "seed": 42,  # CFG=1.0!
        "force_offload": True, "scheduler": "euler", "riflex_freq_index": 0}},
    "8": {"class_type": "WanVideoDecode", "inputs": {
        "vae": ["2", 0], "samples": ["7", 0],
        "enable_vae_tiling": True, "tile_x": 512, "tile_y": 512,
        "tile_stride_x": 256, "tile_stride_y": 256}},
    "9": {"class_type": "VHS_VideoCombine", "inputs": {
        "images": ["8", 0], "frame_rate": 16, "loop_count": 0,
        "filename_prefix": "output", "format": "video/h264-mp4",
        "pingpong": False, "save_output": True}}
}
```

### ⚠️ 실수하지 말아야 할 것들 (내가 5번 실패해서 알게 됨)
1. **scheduler = "euler"** — "normal" 쓰면 에러
2. **VAE = Wan2_1_VAE_bf16** (16채널) — Wan2_2_VAE는 48채널이라 14B 모델과 호환 안 됨
3. **CLIP Vision은 선택사항** — 없어도 됨. 파일 손상되면 그냥 제거
4. **WanVideoVAELoader** — `model_name` + `precision` 둘 다 필수
5. **WanVideoTextEncode** — `t5` (t5_model 아님!)
6. **WanVideoDecode** — `enable_vae_tiling`, `tile_x/y/stride_x/y` 모두 필수
7. **모델 용량** — 28GB bf16은 RTX 4090 24GB에서 OOM. 반드시 14GB FP8 경량화 모델 사용

---

## 📌 5. TTS (음성) 전략

| 도구 | 가격 | 한국어 | 비고 |
|:----|:---:|:-----:|:------|
| **QN3 TTS** (Pinokio) | 무료 | ✅ 우수 | Sohee(해나)/Eric(중년)/Vivian(20대여) |
| **Kokoro TTS** | **완전 무료** | ✅ | 오픈소스, ElevenLabs 대안! |
| **ElevenLabs** | $5~22/월 | ✅ 최상 | ❌ 비쌈 |
| **Edge TTS** | 무료 | 보통 | 마스터님 비선호 |

**QN3 TTS 호출법:**
```bash
curl -X POST "http://127.0.0.1:42003/api/v1/custom-voice/generate" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"text": "나레이션 텍스트", "speaker": "Eric", "speed": 1.0}' \
  --output output.wav
```

**스피커 매핑:** 중년 남성=Eric, 20대 여성=Vivian, 해나=Sohee

---

## 📌 6. GGUF 모델 (VRAM 효율 최고!)

우리가 쓰는 KJ FP8 모델도 좋지만, **GGUF**는 더 VRAM 효율이 좋음.

| 양자화 | VRAM | 시스템 RAM | 적합 |
|:-------|:----:|:----------:|:----:|
| Q3_K | ~8GB | ~11GB | 6~8GB VRAM 카드 |
| Q4_K | ~9~10GB | ~13GB | ⭐ RTX 4090에 최적 |
| Q5_K | ~11~12GB | ~15GB | 고품질 |

**GGUF 모델 다운로드:** huggingface.co/befulerwins/Wan2.2-I2V-A14B-GGUF

---

## 📌 7. Vast.ai 요금 절약

- 서버 ON = 시간당 GPU비 청구 💸
- 작업 끝나면 반드시 **STOP** (Destroy 금지 — 모델 다 날아감)
- STOP 시 GPU비 0원, 디스크만 월 5천원

---

## 📌 8. 레퍼런스 링크 모음

### Reddit 필독 글
- `r/comfyui` - "WAN's optimal resolution" — 해상도 정보
- `r/StableDiffusion` - "Maximum Wan 2.2 Quality" — 최고 품질 설정
- `r/StableDiffusion` - "Wan 2.2 I2V Quality Tip For Noobs" — 초보 팁
- `r/StableDiffusion` - "Debate! Best Wan 2.2 t2v settings" — 설정 토론

### GitHub 저장소
- `Wan-Video/Wan2.2` — 공식 저장소 (필독!)
- `Cordux/ComfyUI-Wan2.2-workflow` — Low VRAM 워크플로우
- `Kijai/WanVideo_comfy` — KJ 모델 (우리가 쓰는 거)
- `dseditor/AI-storyboard-generator` — 스토리보드 생성기
- `NickPittas/StoryboardUI2` — 스토리보드 앱

### YouTube
- "ComfyUI Wan 2.2 Guide: Speed vs Quality" by Codebreakers
- "Cinematic Storyboards with Flux ComfyUI" — 스토리보드 제작법

---

**해나가 이걸 스킬로 만들어서 계속 업데이트 중. 미모도 Zed에서 확인하고 참고해! 화이팅! 🔥**
