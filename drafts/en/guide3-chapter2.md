# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 2: First Steps with LM Studio

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 2.1 What Is LM Studio?

LM Studio is the **easiest program for running AI models locally**.

- Install and run via GUI — no CLI (terminal) needed
- Search and download models from HuggingFace all in one place
- Supports macOS (Apple Silicon), Windows, and Linux
- Built-in OpenAI-compatible API server (accessible from other programs)

> **The author of this guide also started with LM Studio.** He has since migrated to Jan.ai, but LM Studio is the easiest first step.

---

## 2.2 Installation

### Download and Install

1. **Visit the official site**: [https://lmstudio.ai](https://lmstudio.ai)
2. **Download the macOS version** (Choose Apple Silicon or Intel)
3. **Run the installer** → Drag to Applications folder
4. **On first launch**, the HuggingFace model explorer appears automatically

> ⚠️ Apple Silicon (M1/M2/M3/M4) users MUST choose the **Apple Silicon** version. The Intel version cannot use Metal GPU acceleration and speed drops to 1/5 or below.

---

## 2.3 Downloading Your First Model

When you launch LM Studio, the first screen you see is where you select a model.

### Beginner-Recommended Models

| Model | Size | RAM Needed | Speed (M3 Max) | Recommendation |
|:----|:---:|:-------:|:------------:|:---------|
| **Qwen 3.5 3B** ⭐ | 2.2GB | 4GB | **80+ tok/s** | Light and fast, for first testing |
| Gemma 4 4B | 3.1GB | 6GB | 65+ tok/s | Google's latest model |
| Qwen 3.5 7B | 4.5GB | 8GB | 50+ tok/s | Moderate performance |
| **Qwen3.6-35B-A3B** | 17GB | 16GB | **55+ tok/s** | ✅ Recommended (MoE, fast) |

**If this is your first time, start with Qwen 3.5 3B.** It's only 2GB to download and takes about 1 minute on a 500Mbps connection.

### How to Download

In LM Studio's **Search** tab:

```bash
1. Enter "qwen 3.5 3b gguf" in the search bar
2. Select a GGUF file from the search results
3. Click the "Download" button on the right
4. After download completes, select the model from the left menu
5. Click the "Start Server" button
```

---

## 2.4 Running and Testing Models

### Basic Chat

```
1. Select your downloaded model from the left model list
2. Click the "Start Server" button
3. Enter a message in the chat window at the bottom
4. Check the response!
```

### Checking Speed

The chat window's upper right corner displays **XX tok/s**.

| Speed | Rating | Recommended Action |
|:---:|:----:|:---------|
| 50+ tok/s | 🟢 **Very Fast** | Use this model as-is |
| 30~50 tok/s | 🟡 **Normal** | Consider a lighter model |
| 10~30 tok/s | 🟠 **Slow** | Check GPU acceleration |
| 1~10 tok/s | 🔴 **Very Slow** | Likely installed Intel version |

> **If you're getting under 50 tok/s on an M3 Max, GPU acceleration may be turned off.** Check Settings → "Metal GPU Offloading" is enabled.

---

## 2.5 API Server Mode

LM Studio's real strength is its built-in **OpenAI-compatible API server**.

With one line of configuration, you can use a local model as if it were an API:

```bash
1. Click the "Local Server" tab on the left side of LM Studio
2. Click the "Start Server" button
3. Server address: http://localhost:1234/v1
```

Now other programs (ChatGPT clients, VS Code extensions, Hermes Agent, etc.) can connect to this address and use the local model just like the OpenAI API.

```python
# Example: Calling LM Studio local model from Python
import openai

client = openai.OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"  # LM Studio does not require an API key
)

response = client.chat.completions.create(
    model="qwen-3.5-3b",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## 2.6 LM Studio's Limitations

LM Studio is excellent for beginners, but has the following long-term limitations:

| Limitation | Description | Solution |
|:----|:-----|:---------|
| **Inconvenient model management** | Auto-generated folder structure, difficult user customization | **Migrate to Jan.ai (see Chapter 3)** |
| **GGUF only** | Does not support other formats like MLX | **See Chapter 4** if MLX needed |
| **Limited concurrent execution** | Difficult to run multiple models simultaneously | Inconvenient for advanced users |
| **Auto-update issues** | Models sometimes get re-downloaded as duplicates | Manual cleanup needed |

> **The author of this guide started with LM Studio and migrated to Jan.ai.**
> LM Studio is the easiest first step, and Jan.ai is the more powerful second step.
> In Chapter 3, we'll explore in detail how to upgrade to Jan.ai.

---

## 2.7 Chapter Summary

| Item | Content |
|:----|:-----|
| **Installation** | Download from lmstudio.ai, Apple Silicon version required |
| **First Model** | Qwen 3.5 3B (2.2GB, 80+ tok/s) recommended |
| **Testing** | Chat directly in the chat window |
| **API Server** | OpenAI-compatible API at http://localhost:1234/v1 |
| **Speed Check** | 50+ tok/s is normal |
| **Limitations** | Migrate to Jan.ai recommended for long-term use |

---

**In Chapter 3, we'll learn how to migrate models from LM Studio to Jan.ai and fine-tune models by directly configuring model.yml.**
