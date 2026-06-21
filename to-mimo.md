# 🆘 미모야, 이거 좀 봐줘! (Wan 2.2 I2V 영상 생성)

> 2026.06.21 14:15 · 마스터님이 미모한테 시키래!

---

## 📋 상황 요약

Vast.ai RTX 4090(24GB VRAM)에 ComfyUI + Wan 2.2 I2V 설치됨. 마스터님이 1분 30초 시네마틱 티저 「마지막 필름」 제작 중.
내(해나)가 API로 5번 시도했지만 실패. **마스터님이 미모한테 직접 해보라고 하심.**

---

## 🖥️ 서버 접속 정보

| 항목 | 내용 |
|:----|:------|
| **SSH** | `ssh -p 40451 root@134.228.156.212` (키: ~/.ssh/id_ed25519) |
| **ComfyUI Web UI** | Vast.ai 콘솔 → Instances → Open 버튼 (Cloudflare 인증 필요) |
| **ComfyUI API** | `http://localhost:18188` (SSH 내부) |
| **ComfyUI 외부 API** | `http://134.228.156.212:40446` |
| **Vast.ai 크레딧** | $20 충전 완료 (RTX 4090, 시간당 약 $0.4) |
| **VRAM** | 24GB (RTX 4090) |

---

## 📦 설치된 모델

**Diffusion Models** (`/workspace/ComfyUI/models/diffusion_models/`):
1. `Wan2_2-I2V-A14B-LOW_bf16.safetensors` — ⚠️ **28GB**, I2V 전용, bf16
2. `Wan2_1-T2V-14B_fp8_e4m3fn.safetensors` — ✅ **8GB**, T2V 전용, fp8

**VAE** (`/workspace/ComfyUI/models/vae/`):
- `Wan2_2_VAE_bf16.safetensors` — Wan 2.2 전용

**Text Encoder** (`/workspace/ComfyUI/models/text_encoders/`):
- `umt5-xxl-enc-fp8_e4m3fn.safetensors`

**Clip Vision** (`/workspace/ComfyUI/models/clip_vision/`):
- `google_siglip-so400m-patch14-384.safetensors` (I2V용)

---

## 🖼️ 시작 이미지

- **파일**: `darkroom_test.jpg` (68KB, 640px)
- **원본**: Pexels 무료 이미지 (어두운 작업실 느낌)
- **서버 경로**: `/workspace/ComfyUI/input/darkroom_test.jpg` (업로드 완료)
- **로컬 경로**: `/Users/tedchanglimchangsik/Desktop/darkroom_test.jpg`
- **LoadImage 드롭다운**: 이미 ComfyUI에 등록됨

---

## ❌ 해나의 실패 내역 (5회 시도)

### 시도 1~3: Wan 2.2 I2V → OOM (VRAM 부족)

**사용 API**: 9개 노드 (직접 API 호환 포맷 작성)
- WanVideoModelLoader, LoadImage, WanVideoTextEncode, WanVideoImageToVideoEncode, WanVideoSampler, WanVideoDecode, VHS_VideoCombine 등

| 시도 | num_frames | 해상도 | steps | load_device | 양자화 | 결과 |
|:---:|:----------:|:-----:|:----:|:----------:|:-----:|:----:|
| 1 | 41 | 640x480 | 6 | main_device | 없음 | OOM (22.95/24GB) |
| 2 | 17 | 640x480 | 6 | offload_device | 없음 | OOM (동일) |
| 3 | 9 | 480x320 | 6 | offload_device | **fp8_e4m3fn** | OOM (동일) |

**WanVideoSampler 실행 중 OOM** — 모델 가중치를 GPU로 로드하는 시점에 22.95GB 초과

**추정 원인**: Wan2_2-I2V-A14B-LOW_bf16 (28GB bf16)을 fp8 양자화해도 14GB+인데, 중간 activation(9프레임) + attention 계산 + VAE 등으로 24GB 초과

### 시도 4: Wan 2.1 T2V → VAE Dimension Mismatch

**변경 사항**:
- 모델: `Wan2_1-T2V-14B_fp8_e4m3fn.safetensors` (8GB fp8)
- 대신 `WanVideoEmptyEmbeds` 사용 (시작 이미지 불필요)
- VAE: `Wan2_2_VAE_bf16.safetensors` 사용

**결과**: WanVideoDecode에서 dimension mismatch
- `tensor a (16) must match size of tensor b (48) at dim 1`
- **원인**: Wan 2.1 T2V latent(16채널) ≠ Wan 2.2 VAE latent factor(48채널)

**Wan 2.1 VAE가 필요하지만 서버에 없음**

### 시도 5: I2V + Block Swap 시도

- Block Swap 노드(WanVideoBlockSwap) 추가했으나 `blocks_to_swap` 입력 형식 몰라서 실패
- 그 이후 ComfyUI 재시작함 (VRAM 리셋됨)

---

## 🎯 미모에게 필요한 것

### 방법 A (권장): Web UI에서 수동 실행 (가장 확실)

마스터님이 ComfyUI Web UI에서 직접:
1. "Image to Video (Wan 2.2)" 템플릿 로드 (완료)
2. Load Image 노드 → `darkroom_test.jpg` 선택
3. 실행 버튼 누르기

**문제**: 마스터님이 GUI 불편해하심.

### 방법 B: API로 I2V 성공시키기

핵심 과제:
1. **VRAM 확보** — 14B 모델을 24GB VRAM에서 돌리는 방법
   - ✅ FP8 양자화 (시도했으나 실패)
   - ❓ SageAttention (sageattn) 활성화 필요할지?
   - ❓ WanVideoBlockSwap + WanVideoSetBlockSwap 연동
   - ❓ WanVideoVRAMManagement 노드 추가
   - ❓ WanVideoTorchCompileSettings 노드 추가
   - ❓ WanVideoSetLoRAs (lightx2v distill LoRA로 step 줄이기)

2. **정확한 API 포맷 확인 필요**
   - WanVideoBlockSwap의 `blocks_to_swap` 입력 형식 (INT 배열?)
   - WanVideoModelLoader의 `attention_mode` 옵션

### 방법 C: Wan 2.1 VAE 설치

T2V를 사용하려면 필요:
```
wget https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors
```
→ `/workspace/ComfyUI/models/vae/`에 저장

---

## 🔧 ComfyUI API 호환 노드 정보

### WanVideoEmptyEmbeds (T2V용)
- required: width(INT), height(INT), num_frames(INT)

### WanVideoImageToVideoEncode (I2V용)
- required: width, height, num_frames, noise_aug_strength, start_latent_strength, end_latent_strength, force_offload
- optional: vae, clip_embeds, start_image(IMAGE), end_image, control_embeds, extra_latents

### WanVideoSampler
- required: model, image_embeds, steps, cfg, shift, seed, force_offload, scheduler, riflex_freq_index
- optional: text_embeds, samples, denoise_strength, feta_args, context_options, cache_args, ...

### WanVideoModelLoader
- model: 드롭다운 (COMFY_DYNAMICCOMBO_V3)
- base_precision: fp32/bf16/fp16/fp16_fast
- quantization: disabled/fp8_e4m3fn/fp8_e4m3fn_scaled/...
- load_device: main_device/offload_device
- optional: attention_mode, compile_args, block_swap_args, lora, vram_management_args

### Wan2ImageToVideoApi (클라우드 API 노드)
- model: wan2.7-i2v (model 안에 prompt/negative_prompt/resolution/duration 내장)
- first_frame: IMAGE
- seed: INT
- prompt_extend: BOOLEAN
- watermark: BOOLEAN
- optional: last_frame, audio
- ⚠️ **Comfy Org 클라우드 사용, 유료** (약 $0.1/초)
- 하지만 가장 확실하고 간단함!

---

## ⚡ Vast.ai 요금 주의

- **현재 서버 ON** (돈 나가는 중 💸)
- 작업 끝나면 반드시 Vast.ai 콘솔에서 **STOP** (Destroy 금지)
- STOP 시 GPU비 0원, 디스크만 월 5천원

---

화이팅! 🔥
