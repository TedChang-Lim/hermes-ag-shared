# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 3: Upgrading to Jan.ai — Serious Model Management

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 3.1 Why Migrate from LM Studio to Jan.ai?

LM Studio is the best tool for getting started. Just install and you're ready to go. But after a few weeks of use, these inconveniences arise:

| Comparison | LM Studio | Jan.ai |
|:---------|:---------|:-------|
| Model folder structure | Auto-generated, difficult to customize | **Full direct control** |
| Configuration files | Settings only via UI | **Fine-tuning via model.yml** |
| Context length | Fixed defaults | **Free ctx_size configuration** |
| Model migration | Hard to copy to other folders | **Just need the GGUF file** |
| Concurrent execution | Only 1 model | Easy switching between multiple models |
| Community | Relatively closed | **Open source, high extensibility** |

> **The author of this guide also started with LM Studio and now uses Jan.ai as the main tool.**
> LM Studio is kept only for model downloading, with actual operations done through Jan.ai.

---

## 3.2 Installing Jan.ai

### Download and Install

```bash
1. Visit the official site: https://jan.ai
2. Download the macOS version (Apple Silicon)
3. Install to Applications folder
4. Launch and confirm the model folder is auto-created
```

### What to Check on First Launch

When you first launch Jan.ai, you'll see a **"No model selected"** message at the bottom left. This is because no model has been installed yet. This is normal.

---

## 3.3 Understanding Jan.ai's Model Folder Structure

This is the most important part. Jan.ai's model folder structure is as follows:

```bash
~/Library/Application Support/Jan/data/llamacpp/models/
├── Qwen-3.5-3B/                    # Model folder (create manually)
│   ├── qwen-3.5-3b-q8_0.gguf      # Actual model file (1~30GB)
│   └── model.yml                   # Configuration file (write manually)
│
├── Gemma-4-4B/
│   ├── gemma-4-4b-q4_k_m.gguf
│   └── model.yml
│
└── Qwen3.6-35B-A3B-I-Compact/
    ├── qwen3.6-35b-i-compact.gguf
    └── model.yml
```

**The rule is simple:**
- One folder per model
- Inside the folder: `model.gguf` (or any name .gguf) + `model.yml`

---

## 3.4 Complete model.yml Configuration Guide

`model.yml` is the core of Jan.ai. This single file determines all settings for the model.

### Basic Template (Provided by AG)

```yaml
# ~/Library/Application Support/Jan/data/llamacpp/models/<model_name>/model.yml
id: qwen-3.5-3b          # Unique identifier
name: Qwen 3.5 3B        # Name displayed in Jan.ai
engine: llamacpp          # Engine (fixed)

# Core settings
ctx_len: 4096             # Context length (based on model defaults)
temperature: 0.7          # Creativity adjustment
top_p: 0.9                # Sampling method
max_tokens: 2048          # Maximum response tokens

# Apple Silicon GPU acceleration (important!)
n_gpu_layers: -1          # -1 = offload all layers to GPU

# Prompt template (ChatML format, recommended for Qwen/Gemma)
prompt_template: "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
stop:
  - "<|im_end|>"
  - "<|im_start|>"
```

### Parameter Details

| Parameter | Description | Recommended Value |
|:---------|:-----|:------|
| `ctx_len` | Number of tokens the model can remember at once | Qwen 3.5: 4096, Qwen3.6: 32768, Gemma 4: 131072 |
| `n_gpu_layers` | Number of layers offloaded to GPU | **-1 (all)** — Always use this on M Macs |
| `temperature` | Response creativity (lower = more conservative) | 0.5 ~ 0.9 |
| `max_tokens` | Maximum tokens to generate at once | 2048 ~ 8192 |

### ctx_len Configuration Tips

| Model | Default ctx_len | Max ctx_len | Notes |
|:----|:-----------:|:-----------:|:-----|
| Qwen 3.5 3B | 32,768 | 32,768 | Use as-is |
| Qwen 3.5 7B | 32,768 | 32,768 | Use as-is |
| Qwen3.6-35B | 32,768 | 131,072 (YaRN) | Default recommended |
| Gemma 4 4B | 131,072 | 262,144 | Too large will slow things down |

> ⚠️ Setting ctx_len too large significantly slows down speed.
> Start with the default and only increase when needed.

---

## 3.5 LM Studio → Jan.ai Model Migration

How to move models already downloaded in LM Studio to Jan.ai.

### Method 1: Direct File Copy (Simplest)

```bash
# 1. Find the LM Studio model folder
ls ~/.lmstudio/models/
# Or
ls ~/Documents/LM\ Studio/models/

# 2. Check the desired GGUF file
ls ~/.lmstudio/models/*.gguf

# 3. Copy to Jan.ai model folder
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/MyModel
cp ~/.lmstudio/models/model_file.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/MyModel/

# 4. Write model.yml (refer to the template above)
```

### Method 2: Direct Download via HuggingFace CLI (Recommended)

You need CLI tools to download models from HuggingFace Hub. You can easily install them via Python packages or Homebrew.

```bash
# 1. Install HuggingFace CLI (choose one of method A or B)
# Method A: Standard method using Python pip (recommended)
pip install -U "huggingface_hub[cli]"

# Method B: Using Homebrew (installs as official formula named hf)
brew install hf

# 2. Create model folder
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 3. Run model download
huggingface-cli download \
  Qwen/Qwen-3.5-3B-GGUF \
  qwen-3.5-3b-q8_0.gguf \
  --local-dir ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 4. Write model.yml (edit with nano editor or VS Code)
nano ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B/model.yml
```


> **Download time:** For a 17GB model, approximately 5~6 minutes on a 500Mbps connection.

---

## 3.6 Verifying Model Application

After adding files to the model folder:

```bash
1. Completely quit Jan.ai (Quit the menu bar icon too)
2. Relaunch Jan.ai
3. Check if the new model appears in the left model list
4. Select the model and type "Hello" in the chat window
5. Check speed in the upper right: 50+ tok/s is normal
```

### What to Check When Speed Is Slow

| Problem | Cause | Solution |
|:----|:-----|:---------|
| Under 30 tok/s | GPU acceleration off | Check `n_gpu_layers: -1` in model.yml |
| Under 10 tok/s | Intel version installed | Reinstall Apple Silicon version from jan.ai official site |
| Delayed response start | ctx_len too large | Reduce ctx_len to default |
| Model not visible | model.yml error | Check id and engine fields |

---

## 3.7 Recommended Initial Settings (Author's Actual Configuration)

```yaml
# Qwen3.6-35B-A3B APEX I-Compact (17GB)
id: qwen-3.6-35b
name: Qwen 3.6 35B APEX I-Compact
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
```

This configuration maintains **55~60 tok/s** on an M3 Max 48GB.

---

## 3.8 Chapter Summary

| Step | Content |
|:----|:------|
| **Installation** | Download from jan.ai, Apple Silicon version required |
| **Folder Structure** | `~/Library/Application Support/Jan/data/llamacpp/models/<model_name>/` |
| **Configuration File** | Write `model.yml` manually (ctx_len, n_gpu_layers are key) |
| **Model Migration** | Copy GGUF from LM Studio folder → Jan.ai folder |
| **Speed Check** | 50+ tok/s is normal, always verify `n_gpu_layers: -1` |

---

**In Chapter 4, we'll explore MLX framework setup to utilize 100% of Apple Silicon performance.**
