# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 6: APEX Quantization — Secrets of MoE Models

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 6.1 What Is MoE (Mixture of Experts)?

MoE stands for **"Mixture of Experts"** — an architecture where a single large model contains multiple smaller "experts" and selectively uses only the experts needed based on the input.

### Dense vs MoE

```
Dense Model (e.g., Gemma 4 12B)
┌─────────────────────────────────────┐
│ All inputs pass through all          │  → Always computes all 12B
│ parameters (12B)                     │
└─────────────────────────────────────┘

MoE Model (e.g., Qwen3.6-35B-A3B)
┌─────────────────────────────────────┐
│ Router examines input and selects    │
│ only needed experts → Only 3B of     │  → Only computes needed 3B
│ 35B activated                        │
└─────────────────────────────────────┘
```

| Comparison | Dense | MoE (Mixture of Experts) |
|:----|:-----------|:-----------------|
| **Total Parameters** | 12B | 35B |
| **Activated Parameters** | 12B (100%) | **3B (8.6%)** |
| **Inference Speed** | 25~35 tok/s | **50~60 tok/s** |
| **Memory Usage** | High | Full load needed but less computation |
| **Quantization Effect** | Standard | **APEX specialized** |

> **Key point:** MoE is a 35B model but only 3B are activated, so it can be **2x faster than a 12B Dense model** while possessing 35B-level knowledge.

---

## 6.2 What Is APEX Quantization?

APEX (**A**daptive **P**recision for **E****x**pert Models) is a quantization method specifically designed for MoE models.

### Problems with Standard Quantization

Standard quantization (Q4_K_M, etc.) compresses all parts of the model at the same precision. But MoE models have a different structure:
- **Edge Layers** (the first and last few layers) — every input must pass through, high importance
- **Middle Routed Experts** (intermediate expert layers) — only some activated at a time
- **Shared Expert** — an expert shared by all inputs

### APEX's Differentiation

| Model Part | Standard Quantization | APEX Quantization |
|:---------|:----------|:-----------|
| Edge Layers | Same precision | **Maintains high precision** |
| Middle Experts | Same precision | **Compressed at lower precision** |
| Shared Expert | Same precision | **Maintains high precision** |
| Attention | Same precision | **Maintains high precision** |

> APEX is smart quantization that **preserves important parts and compresses less important parts more aggressively**.

---

## 6.3 APEX Profile Selection Guide

These are the APEX profiles available for the Qwen3.6-35B-A3B model:

### Profile Sizes and Use Cases

| Profile | Size | Use Case | M3 Max 48GB |
|:------|:---:|:----|:-----------:|
| **I-Compact** ⭐ | **17GB** | **General-purpose optimal** | ✅ **Recommended! Can run alongside Hermes** |
| I-Mini | 14GB | Lightest | ✅ Sufficient |
| I-Balanced | 24GB | Highest quality | ⚠️ Possible if free memory available |
| I-Quality | 22GB | High quality | ⚠️ Possible |

### Why I-Compact Is Recommended

Choosing I-Compact (17GB) on M3 Max 48GB:
- Model uses 17GB
- Hermes Agent and other apps use 10~15GB
- 16GB + extra remaining with room to spare
- Maintains **55~60 tok/s** speed

Choosing I-Balanced (24GB):
- Model uses 24GB
- Other apps/system use 15~20GB
- **Swap occurs → 30% speed degradation**
- tok/s may drop to less than half

> **On M3 Max 48GB, I-Compact is the golden ratio of speed and quality.**

---

## 6.4 How to Install APEX

### Download

```bash
# Recommended Repositories
# 1. OpenYourMind (Abliterated + APEX)
#    https://huggingface.co/OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF

# 2. mudler (APEX GGUF)
#    https://huggingface.co/mudler/Qwen3.6-35B-A3B-uncensored-heretic-APEX-GGUF

# Download example
huggingface-cli download \
  OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF \
  OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
  --local-dir ~/Downloads/
```

### Installing to Jan.ai

```bash
# 1. Create Jan.ai model folder
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact

# 2. Copy downloaded file
cp ~/Downloads/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact/

# 3. Create model.yml
cat > ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact/model.yml << 'EOF'
id: qwen-3.6-35b-i-compact
name: Qwen 3.6 35B APEX I-Compact (Uncensored)
engine: llamacpp
ctx_len: 32768
temperature: 0.7
top_p: 0.9
max_tokens: 4096
n_gpu_layers: -1
prompt_template: "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
stop:
  - "<|im_end|>"
  - "<|im_start|>"
EOF

# 4. Restart Jan.ai and select the model
```

---

## 6.5 APEX vs Standard Quantization Speed Comparison

### Qwen3.6-35B-A3B (M3 Max 48GB)

| Quantization Method | File Size | Speed | Quality |
|:----------:|:--------:|:----:|:----:|
| Standard Q4_K_M | ~20GB | 48 tok/s | Good |
| APEX I-Compact | **17GB** | **55~60 tok/s** | **Good** |
| Standard Q3_K_M | ~14GB | 50 tok/s | Moderate |
| APEX I-Mini | 14GB | 55 tok/s | Moderate |
| Standard Q2_K | ~10GB | 52 tok/s | Low |

> APEX I-Compact has a **file size 15% smaller and speed 20% faster** than standard Q4_K_M.
> At the same time, quality is nearly identical to Q4_K_M.

---

## 6.6 iMatrix: Additional Optimization

APEX supports an additional optimization called **iMatrix (iMatrix calibration)**. iMatrix analyzes actual usage patterns to measure importance for quantization optimization.

```bash
# Generate iMatrix from Hermes Agent session traces (advanced)
# Optimized for tool calling, code generation, and other patterns

# Models with iMatrix already applied:
# - mudler/Qwen3.6-35B-A3B-uncensored-heretic-APEX-GGUF
# - OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF
```

> General users just need to **download APEX GGUF files that already have iMatrix applied**.

---

## 6.7 Chapter Summary

| Item | Content |
|:----|:-----|
| **What is MoE?** | Only needed experts activated among many (only 3B of 35B) |
| **What is APEX?** | MoE-specific quantization, preserves important parts, compresses less important ones |
| **Recommended Profile** | **I-Compact (17GB)** — optimal for M3 Max 48GB |
| **Speed** | 20% faster than standard Q4 (55~60 tok/s) |
| **Installation** | HuggingFace → Jan.ai model.yml setup |
| **iMatrix** | Additional optimization based on actual usage patterns (use pre-applied files) |

---

**In Chapter 7, we'll learn how to select and install Uncensored / Abliterated models.**
