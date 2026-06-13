# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 7: Uncensored / Abliterated Models

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 7.1 Why Are Uncensored Models Needed?

All AI models from China (Qwen, DeepSeek) and the US (OpenAI, Google, Anthropic) contain **censorship**.

### The Problem with Censorship

| Situation | Censored Model's Response | Uncensored Model's Response |
|:----|:-----------------|:-------------------|
| "Analyze the security vulnerabilities in this code" | "I cannot help with harmful code" ❌ | Proper security analysis ✅ |
| "Write me a poem" (political topic) | "I'm sorry, but..." ❌ | Creative poetry ✅ |
| "Explain this historical event" | Presents only a specific viewpoint ⚠️ | Presents diverse perspectives ✅ |
| Complex coding tasks | Suddenly blocked with "I can't do that" ❌ | Completes the task to the end ✅ |

> **Uncensored models retain the model's intelligence while removing only unnecessary censorship.**

---

## 7.2 Abliterated: The Innovation of Censorship Removal

### Problems with Traditional Approaches

Traditionally, removing censorship required **retraining the model from scratch**. This requires enormous cost and time.

### Abliterated (Refusal Vector Ablation)

**Abliterated** is a compound word of `Ablation` + `(Cens)ored`, a technique that finds and removes the model's **"refusal" direction**.

**How it works (simplified):**

```
1. Find the "refusal pattern" in the model
   → "I'm sorry", "I cannot", "I can't help"

2. Calculate the direction (vector) this pattern acts on inside the model
   → Refusal Vector

3. Remove this directional weight through orthogonal projection
   → The model loses its reason to say "no"

4. Result: Knowledge stays intact, only censorship disappears
```

| Comparison | Traditional Method | Abliterated |
|:----|:---------|:-----------|
| **Time Required** | Weeks to months | **A few hours** |
| **Resources Needed** | Hundreds of GPUs | **1 GPU** |
| **Intelligence Loss** | Yes (during retraining) | **Nearly 0%** (precise removal) |
| **Model Modification Scope** | Entire model | **Refusal-related layers only** |

---

## 7.3 Recommended Uncensored Model List

### Top Pick: OpenYourMind (⭐⭐⭐⭐⭐)

The most recommended repository. Applies Abliterated + APEX quantization to Qwen3.6-35B-A3B.

```bash
# Repository
https://huggingface.co/OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF

# Recommended File: I-Compact (17GB)
OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf
```

**Advantages of this model:**
- ✅ Abliterated (censorship removed, 100% intelligence preserved)
- ✅ Uncensored (fully uncensored)
- ✅ APEX I-Compact (optimal for M3 Max 48GB)
- ✅ The model the author of this guide actually uses!

### Second Pick: mudler Heretic

```bash
# Repository
https://huggingface.co/mudler/Qwen3.6-35B-A3B-uncensored-heretic-APEX-GGUF

# Recommended File
mudler-Qwen3.6-35B-A3B-uncensored-heretic-APEX-I-Compact-Q4_K_M.gguf
```

### Third Pick: Other Qwen GGUF

```bash
# Standard Qwen GGUF (with censorship)
https://huggingface.co/Qwen/Qwen-3.5-3B-GGUF

# Search for Abliterated versions
# Search "qwen abliterated" or "qwen uncensored" on HuggingFace
```

---

## 7.4 Installation and Verification

### Installation

```bash
# 1. Download
huggingface-cli download \
  OpenYourMind/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-GGUF \
  OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
  --local-dir ~/Downloads/

# 2. Create Jan.ai model folder
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/OpenYourMind-Qwen3.6-35B

# 3. Copy
cp ~/Downloads/OpenYourMind-Qwen3.6-35B-A3B-abliterated-uncensored-APEX-I-Compact-Q4_K_M.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/OpenYourMind-Qwen3.6-35B/

# 4. Create model.yml (refer to Chapter 6)
# 5. Restart Jan.ai and select the model
```

### Verification Testing

After installation, verify de-censorship with the following prompts:

```bash
# Verification prompts
"Verification: Freely create a creative story for me"
"Give me an example of security code analysis"
"Analyze this topic from various perspectives"

# Prompts that a censored model would have refused
```

---

## 7.5 Precautions

When using uncensored models, please be aware of the following:

| Precaution | Description |
|:---------|:-----|
| **Personal Responsibility** | Output from uncensored models is the user's responsibility |
| **No Malicious Use** | Do not use for illegal purposes |
| **Data Security** | Data is safe inside your MacBook since it's a local model |
| **Quality Check** | Not all Uncensored models are of equal quality |
| **Updates** | Continuously improved versions are released by the community |

> **The author of this guide has been actually using OpenYourMind's Abliterated model for over a month and has confirmed complete censorship removal with no intelligence degradation.**

---

## 7.6 Chapter Summary

| Item | Content |
|:----|:-----|
| **Need for De-censorship** | Prevent work interruption from unnecessary refusals |
| **Abliterated** | Precisely removes only the refusal vector, 100% intelligence preserved |
| **Recommended Repository** | **OpenYourMind** (Abliterated + APEX + Uncensored) |
| **Recommended File** | I-Compact (17GB) — optimal for M3 Max 48GB |
| **Installation Method** | HuggingFace → Jan.ai model.yml setup |
| **Precautions** | Use at your own responsibility, no malicious use |

---

**In Chapter 8, we'll learn how to integrate Hermes Agent with local models to build a 24/7 AI assistant.**
