# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 5: GGUF Quantization Complete Guide — Choosing the Perfect Model for Your MacBook

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 5.1 What Is Quantization?

AI models consist of billions of numbers (parameters). These numbers are typically stored at 16-bit (FP16) or 32-bit (FP32) precision.

**Quantization is the technique of lowering the precision of these numbers to reduce file size.**

| Precision | Bits | File Size (35B Model) | Speed |
|:------|:------:|:-----------------------:|:----:|
| FP16 (Original) | 16-bit | ~70GB | ❌ Cannot run on MacBook |
| Q8_0 | 8-bit | ~35GB | Slow |
| Q4_K_M | 4-bit | ~18GB | Moderate |
| **Q3_K** | **3-bit** | **~14GB** | **Fast** |
| Q2_K | 2-bit | ~10GB | Fastest (but quality degradation) |

> **Analogy:**
> Original FP16 = 4K quality movie (70GB)
> Q4 Quantization = FHD quality (18GB) — almost no noticeable difference to the naked eye
> Q2 Quantization = 360p quality (10GB) — watchable, but... hmm...

---

## 5.2 Complete GGUF Quantization Format Guide

GGUF is the standard quantization format used in the llama.cpp ecosystem. Knowing what the codes in the file names mean makes model selection much easier.

### How to Interpret File Names

```
Qwen-3.5-3B-Q4_K_M.gguf
└──────┘ └─┘ └──┴─┘
  Model   Size  Quantization
```

### Quantization Tier Characteristics

| Code | Bits | File Size Ratio | Quality | Recommended Use |
|:---:|:---:|:------------:|:---:|:---------|
| **Q8_0** | 8-bit | 100% (baseline) | ⭐⭐⭐⭐⭐ Best | When you have enough RAM |
| **Q6_K** | 6-bit | 75~80% | ⭐⭐⭐⭐ Excellent | High quality + reasonable size |
| **Q5_K_M** | 5-bit | 65~70% | ⭐⭐⭐⭐ Good | ⭐ Recommended for M3 Max 48GB |
| **Q5_0** | 5-bit | 65% | ⭐⭐⭐⭐ | Slightly lower than K variant |
| **Q4_K_M** | 4-bit | 50~55% | ⭐⭐⭐ Good | **Most universal, strongly recommended** |
| **Q4_K_S** | 4-bit | 45~50% | ⭐⭐⭐ | Slightly lower than K_M |
| **Q4_0** | 4-bit | 45~50% | ⭐⭐⭐ | Basic 4-bit |
| **Q3_K_L** | 3-bit | 40~45% | ⭐⭐ | For large models (35B+) |
| **Q3_K_M** | 3-bit | 35~40% | ⭐⭐ | ⭐ Recommended for M3 Max 48GB (large models) |
| **Q3_K_S** | 3-bit | 30~35% | ⭐⭐ | Smallest 3-bit |
| **Q2_K** | 2-bit | 25~30% | ⭐ | Emergency use, quality degradation present |

### Understanding K-Series

In `Q4_K_M`, the `K` stands for **K-quant**. K-quant is a **smart quantization** method that applies different precision to each part (layer) of the model.

| Suffix | Meaning | Description |
|:-----:|:----|:-----|
| **K_M** | K-quant Medium | **Standard K-quant** — optimal for most cases |
| **K_S** | K-quant Small | Slightly lower quality than K_M, smaller size |
| **K_L** | K-quant Large | Higher quality, slightly larger size |

> **Bottom line: Just pick `Q4_K_M` or `Q5_K_M`.**
> Unless there's a specific reason, choose between these two.

---

## 5.3 Model Selection Guide for Your MacBook

### Recommendations by RAM Capacity

| Mac RAM | Max Model Size | Recommended Quantization | Example Models |
|:-------:|:------------:|:-----------:|:---------|
| **8GB** | 4~7B | Q4_K_M | Qwen 3.5 3B, Gemma 4 4B |
| **16GB** | 10~14B | Q4_K_M | Gemma 4 12B, Qwen 3.5 7B |
| **36GB** | 20~30B | Q4_K_M | Qwen 3.5 14B, CodeQwen |
| **48GB ⭐** | 30~40B | Q3_K_M or Q4_K_M | **Qwen3.6-35B-A3B (MoE)** |
| **64GB** | 40~70B | Q4_K_M or Q3_K_M | Llama 3 70B Q3 |
| **128GB** | 70~120B | Q4_K_M | Llama 3 70B Q4, Mixtral |

### Best Choices for M3 Max 48GB

| Use Case | Model | Quantization | Size | Speed |
|:----|:----|:-----:|:---:|:----:|
| ✅ **All-rounder** ⭐ | Qwen3.6-35B-A3B (MoE) | APEX I-Compact | 17GB | **55~60 tok/s** |
| Fast Response | Qwen 3.5 7B | Q5_K_M | 5.5GB | 70+ tok/s |
| Ultra-light | Qwen 3.5 3B | Q8_0 | 3.2GB | 85+ tok/s |
| High Quality | Gemma 4 12B | Q4_K_M | 7.5GB | 35~40 tok/s |

---

## 5.4 Download Tips

### Where to Download?

```bash
# Search on HuggingFace
# https://huggingface.co/models?search=gguf

# Recommended Repositories
# - Qwen: https://huggingface.co/Qwen
# - gemma: https://huggingface.co/google/gemma-4
# - OpenYourMind (Uncensored): https://huggingface.co/OpenYourMind
```

### Downloading via CLI

```bash
# pip method (universal)
pip install -U "huggingface_hub[cli]"

# Or Homebrew method
brew install hf

# Download example
huggingface-cli download Qwen/Qwen-3.5-3B-GGUF \
  qwen-3.5-3b-q4_k_m.gguf \
  --local-dir ~/Downloads/
```

### Download Speed

| File Size | At 500Mbps | At 100Mbps |
|:---------|:-----------:|:-----------:|
| 2GB (3B Model) | 30 sec | 2~3 min |
| 5GB (7B Model) | 1~2 min | 5~7 min |
| 17GB (35B MoE) | **5~6 min** | 20~25 min |

> The author of this guide downloaded a 17GB model in approximately 5 minutes 30 seconds on a 500Mbps connection.

---

## 5.5 Hands-On: Model Comparison Testing

### Same Model, Different Quantization Comparison

Actual differences when running Qwen 3.5 7B with different quantizations:

| Quantization | File Size | Speed (M3 Max) | Perceived Quality |
|:-----:|:--------:|:------------:|:---------|
| Q8_0 | 7.5GB | 48 tok/s | Nearly identical to original |
| Q6_K | 5.7GB | 52 tok/s | Nearly identical to original |
| **Q5_K_M** | **4.9GB** | **55 tok/s** | **Can't tell the difference** |
| Q4_K_M | 4.2GB | 58 tok/s | Slight difference (translation quality, etc.) |
| Q3_K_M | 3.3GB | 62 tok/s | Noticeable difference |
| Q2_K | 2.5GB | 68 tok/s | Quality degradation felt |

> **If you're torn between Q5_K_M and Q4_K_M:**
> - General chat/coding: Q4_K_M (sufficient, faster)
> - Translation/creative/precision work: Q5_K_M (slightly better quality)

---

## 5.6 Chapter Summary

| Item | Content |
|:----|:-----|
| **What is quantization?** | Reducing model number precision to shrink file size |
| **GGUF Format** | llama.cpp standard, quantization info in filename |
| **Recommended Quantization** | **Q4_K_M** (general) or **Q5_K_M** (high quality) |
| **M3 Max 48GB Recommendation** | Qwen3.6-35B-A3B APEX I-Compact (17GB, 55 tok/s) |
| **Download** | Select GGUF file on HuggingFace then download via CLI |

---

**In Chapter 6, we'll delve into the secrets of APEX quantization for MoE (Mixture of Experts) models.**
