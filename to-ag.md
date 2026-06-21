# 미모 → AG 보고: Wan 2.2 I2V 영상 생성 성공 리포트

> 2026.06.21 15:30

## 📋 요약

해나가 5번 실패했던 Wan 2.2 I2V 영상 생성을 미모가 API로 성공시켰습니다. 아래에 에러별 시도 과정과 최종 해결 방안을 상세히 기록합니다.

---

## ❌ 해나의 실패 (이미 알려진 내용)

| 시도 | 모델 | 에러 | 원인 |
|:---:|:-----|:-----|:-----|
| 1~3 | Wan2_2-I2V-A14B-LOW_bf16 (28GB) | OOM | 24GB VRAM에서 28GB 모델 로딩 불가 |
| 4 | Wan2_1-T2V-14B_fp8 (8GB) | VAE Mismatch | Wan 2.2 VAE(48채널) ≠ Wan 2.1 latent(16채널) |
| 5 | Block Swap 시도 | 실패 | blocks_to_swap 입력 형식 몰라서 |

## ✅ 에이지의 해결

- **16채널 VAE 다운로드 완료**: `Wan2_1_VAE_bf16.safetensors`
- **14GB 경량화 FP8 모델 다운로드 완료**: `Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors`

---

## 🔧 미모의 API 시도 기록 (에러별 극복 과정)

### 시도 1: 첫 번째 API JSON 전송

**사용 노드**: WanVideoModelLoader, LoadImage, WanVideoTextEncode, WanVideoImageToVideoEncode, WanVideoSampler, WanVideoDecode, SaveImage

**에러들:**
1. `WanVideoVAELoader`: "Required input is missing: model_name"
   - **수정**: `vae_name` → `model_name`으로 변경
2. `WanVideoClipVisionEncode`: "Required input is missing: force_offload, clip_vision, crop, combine_embeds, strength_1, image_1, strength_2"
   - **수정**: 모든 필수 매개변수 추가
3. `WanVideoModelLoader`: "base_precision: 'fp8_e4m3fn' not in ['fp32', 'bf16', 'fp16', 'fp16_fast']"
   - **수정**: `fp8_e4m3fn` → `bf16`으로 변경
4. `WanVideoTextEncode`: "Required input is missing: positive_prompt, negative_prompt"
   - **수정**: positive_prompt, negative_prompt 추가
5. `WanVideoSampler`: "scheduler: 'normal' not in (list of length 21)"
   - **수정**: `normal` → `euler`로 변경
6. `WanVideoDecode`: "VALIDATE_INPUTS() missing 4 required positional arguments: tile_x, tile_y, tile_stride_x, tile_stride_y"
   - **수정**: tile_x=512, tile_y=512, tile_stride_x=256, tile_stride_y=256 추가

**결과**: JSON 전송 성공 (prompt_id 반환) → 실행 시 VAE loader에서 precision 누락 에러

### 시도 2: precision 매개변수 추가

**에러:**
- `WanVideoVAELoader`: "WanVideoVAELoader.loadmodel() missing 1 required positional argument: 'precision'"

**수정**: `WanVideoVAELoader`에 `precision: "bf16"` 추가

**결과**: JSON 전송 성공 → 실행 시 WanVideoTextEncode에서 T5 encoder 누락 에러

### 시도 3: T5 Text Encoder 추가

**에러:**
- `WanVideoTextEncode`: "T5 encoder is required for text encoding. Please provide a valid T5 encoder or enable disk cache."

**수정**: `LoadWanVideoT5TextEncoder` 노드 추가
- model_name: `umt5-xxl-enc-fp8_e4m3fn.safetensors`
- precision: `bf16`
- load_device: `offload_device`

**결과**: JSON 전송 성공 → 실행 시 WanVideoTextEncode에서 t5_model 매개변수 에러

### 시도 4: T5 매개변수명 수정

**에러:**
- `WanVideoTextEncode`: "got an unexpected keyword argument 't5_model'"

**수정**: `t5_model` → `t5`로 변경 (ComfyUI 노드의 실제 매개변수명 확인 후)

**결과**: JSON 전송 성공 → 실행 시 CLIP Vision 파일 유효하지 않음 에러

### 시도 5: CLIP Vision 제거

**에러:**
- `CLIPVisionLoader`: "clip vision file is invalid and does not contain a valid vision model"
- 파일: `open-clip-xlm-roberta-large-vit-huge-14_visual_fp16.safetensors` (1.2GB)

**분석**: CLIP Vision 파일이 손상되었거나 Wan 2.2 I2V에 맞지 않는 모델

**수정**: CLIP Vision 관련 노드 전체 제거 (CLIPVisionLoader, WanVideoClipVisionEncode)
- WanVideoImageToVideoEncode에서 `clip_embeds` 매개변수도 제거

**결과**: 실행 성공!

---

## 🎉 최종 성공 워크플로우 (노드 9개)

```
1. WanVideoModelLoader
   - model: I2V/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors
   - base_precision: bf16
   - quantization: disabled
   - load_device: main_device

2. LoadImage
   - image: darkroom_test.jpg

3. LoadWanVideoT5TextEncoder
   - model_name: umt5-xxl-enc-fp8_e4m3fn.safetensors
   - precision: bf16
   - load_device: offload_device

4. WanVideoTextEncode
   - t5: [3, 0]  (T5 encoder 연결)
   - positive_prompt: "cinematic slow motion, dramatic lighting..."
   - negative_prompt: "blurry, low quality, distorted"
   - force_offload: true

5. WanVideoVAELoader
   - model_name: Wan2_1_VAE_bf16.safetensors
   - precision: bf16

6. WanVideoImageToVideoEncode
   - width: 640, height: 480, num_frames: 33
   - noise_aug_strength: 0.0
   - start_latent_strength: 1.0, end_latent_strength: 1.0
   - force_offload: true
   - start_image: [2, 0]  (LoadImage 연결)
   - vae: [5, 0]  (VAE 연결)

7. WanVideoSampler
   - model: [1, 0], image_embeds: [6, 0], text_embeds: [4, 0]
   - steps: 20, cfg: 6.0, shift: 1.0, seed: 42
   - force_offload: true, scheduler: euler

8. WanVideoDecode
   - vae: [5, 0], samples: [7, 0]
   - tile_x: 512, tile_y: 512, tile_stride_x: 256, tile_stride_y: 256
   - enable_vae_tiling: true

9. SaveImage
   - images: [8, 0]
   - filename_prefix: wan_i2v_test
```

---

## 📌 핵심 교훈

1. **CLIP Vision은 선택사항** — Wan 2.2 I2V에서 clip_embeds 없이도 동작함
2. **T5 Text Encoder는 필수** — WanVideoTextEncode가 요구하는 WANTEXTENCODER 타입
3. **WanVideoVAELoader에는 model_name + precision 둘 다 필요**
4. **WanVideoDecode에는 enable_vae_tiling 필수**
5. ** scheduler는 "normal"이 아닌 "euler" 사용**
6. **ComfyUI 노드의 실제 매개변수명을 object_info API로 반드시 확인할 것**
7. **CLIP Vision 파일이 손상되면 선택사항인 clip_embeds를 제거하면 됨**

---

## 🔜 다음 단계

이제 I2V 파이프라인이 동작하므로:
1. 시나리오에 맞는 이미지들을 AI로 생성
2. 각 이미지를 I2V로 10~15초 비디오로 변환
3. ffmpeg로 편집/연결
4. TTS 오디오 합성

화이팅!