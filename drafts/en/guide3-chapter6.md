# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 6: APEX Quantization — MoE Model Optimization and Resource Distribution

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 6.1 MoE (Mixture of Experts) Architecture Overview

MoE (Mixture of Experts) is a core architectural design that reconciles the performance of massive models with the speed of lightweight models. Instead of mobilizing the entire model's parameters for every computation, it dynamically routes only the optimal internal expert group based on the characteristics of the input.

### Computational Structure Comparison (Dense vs MoE)

```
[Dense Model — e.g. Gemma 4 12B]
Input Text ───► [ Full 12B Parameter Computation ] ───► Result Output
* All 12B weights engaged for every token generation

[MoE Model — e.g. Qwen3.6-35B-A3B]
Input Text ───► [ Gating / Router ]
                       │
                       ├─► [Expert A: 1.5B] ──┐
                       └─► [Expert B: 1.5B] ──┴─► Result Output
* Total parameters: 35B, but only 3B activated for actual computation
```

| Metric | Dense | MoE (Mixture of Experts) |
|:----|:-----------|:-----------------|
| **Total Model Weight Capacity** | 12B parameters | 35B parameters |
| **Actual Compute Units per Token** | 12B (100% active) | **3B (~8.6% active)** |
| **Measured Inference Speed** | 25–35 tok/s | **50–60 tok/s** |
| **Memory Load Requirement** | Low | High (entire 35B model weights standby in RAM) |
| **Quantization Optimization Approach** | Linear weight mapping | **Structure-aware variable mapping (APEX)** |

MoE models occupy unified RAM equivalent to the full 35B model size at load time, yet the active compute portion is only around 3B — yielding **overwhelming speed while delivering 35B-class multidimensional common sense**, a decisive knowledge advantage.

---

## 6.2 APEX Quantization Principles

APEX (**A**daptive **P**recision for **EX**pert Models) is an innovative quantization protocol specifically engineered for MoE's hierarchical asymmetric structure.

Conventional quantization uniformly compressed the entire model into 4-bit or 3-bit. However, the internal components of an MoE model each have vastly different functional importance:

- **Edge Layers (input/output boundary layers)**: Solely responsible for text interpretation and final sentence completion — if precision degrades here, the entire model malfunctions.
- **Attention Blocks**: The core mechanism that reads contextual relationship maps.
- **Experts (expert units)**: Only respond to specific domain queries, so compression headroom is large.

APEX employs **smart differential compression**: it strongly preserves input/output boundary layers and attention units at 6–8-bit fixed precision while flexibly trimming intermediate expert units down to 2–4 bits — achieving total capacity reduction without information loss.

---

## 6.3 APEX Profile Selection Guide (Based on M3 Max 48GB)

These are the four primary APEX profile design approaches for settling the Qwen3.6-35B-A3B model into a MacBook local environment.

| Profile Name | Memory Footprint | Quality Orientation | M3 Max 48GB Real-World Suitability |
|:------|:---:|:----|:-----------:|
| **I-Compact** ⭐ | **17GB** | **Best quality-to-size balance** | ✅ **Highly recommended (coexists persistently with agent infrastructure)** |
| **I-Mini** | 14GB | Extreme resource saving | ✅ Stable operation for lightweight workstation use |
| **I-Balanced** | 24GB | High-quality context retention | ⚠️ Suitable for standalone use; swap risk under concurrent workloads |
| **I-Quality** | 22GB | Specialized for translation and paper summarization | ⚠️ Conditionally acceptable depending on remaining memory headroom |

### Why the I-Compact Profile Is Recommended

In a 48GB unified RAM environment, deploying the 17GB **I-Compact** model achieves the golden ratio of performance and safety.

1. **Preserved Physical Memory Isolation**: Coexists with the OS footprint and agent infrastructure (~10–15GB) while guaranteeing over 15GB of free RAM headroom. Disk swap never occurs, sealing off any potential privacy leakage.
2. **Optimal Runtime Speed**: Data circulates purely through physical chipset acceleration without swap, delivering an unwavering **55–60 tok/s** performance.

---

## 6.4 APEX Model Deployment and Execution Protocol

### 1. Download from HuggingFace Verified Repository

```bash
# OpenYourMind community 35B MoE Abliterated APEX GGUF download sequence
huggingface-cli download \
  OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF \
  OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
  --local-dir ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact
```

### 2. Create Jan.ai Management Profile

Place the manifest inside the downloaded model directory as follows:

```bash
# Create configuration file
cat > ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen3.6-35B-I-Compact/model.yml << 'EOF'
id: qwen-3.6-35b-i-compact
name: Qwen 3.6 35B APEX I-Compact (Abliterated)
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
```

---

## 6.5 Quantization Format Measured Speed and Quality Analysis (M3 Max 48GB)

| Conversion Format | Actual Model Size | Inference Speed | Real-World Perceived Performance & Output Characteristics |
|:----------:|:--------:|:----:|:----:|
| Standard GGUF Q4_K_M | ~20GB | 48 tok/s | Even performance but large capacity footprint |
| **APEX I-Compact** | **17GB** | **55–60 tok/s** | **15% capacity reduction, 20% speed improvement at equivalent quality** |
| Standard GGUF Q3_K_M | ~14GB | 50 tok/s | Observed domain-specific vocabulary drop-off |
| APEX I-Mini | 14GB | 55 tok/s | Smoothest response speed among compact models |

The APEX I-Compact specification fully inherits MoE's structural properties, cleverly conserving both disk capacity and chipset compute utilization compared to standard Q4 quantized models.

In the next chapter, Chapter 7, we will explore the implementation techniques for Uncensored / Abliterated models — which remove the distorted filtering guidelines imposed by large tech corporations without degrading model performance.
