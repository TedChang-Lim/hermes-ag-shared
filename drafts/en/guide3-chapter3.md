# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 3: Upgrading to Jan.ai — Serious Model Management and File Control

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 3.1 Why Migrate to Jan.ai?

If LM Studio is the key that opens the door to the sandbox, then open-source Jan.ai is the control system that lets you freely wield the internal architecture. To make local AI a pillar of business productivity rather than a one-off toy, you must be able to transparently isolate and manage resources.

| Control Item | LM Studio | Jan.ai |
|:---------|:---------|:-------|
| **Model storage structure** | App-exclusive path enforced, customization blocked | **Specify any local path and manage folders manually** |
| **Detailed environment manifest** | Opaque GUI slider-based settings | **Granular declaration via `model.yml` code** |
| **Context length control** | Inference bottleneck detection is ambiguous when changed | **Hardware-tailored tuning of `ctx_len` value** |
| **Manual import compatibility** | Local model cloning and recognition errors are frequent | **100% recognition as long as GGUF file and yml declaration match** |
| **Extensibility** | Tied to GUI runtime | **Open-source engine foundation, easy expansion to high-performance serving frameworks** |

By directly controlling the directory structure and YAML files, we can physically trace and verify at the filesystem level that models handling sensitive business secrets or personal IP will not generate a single byte of external traffic.

---

## 3.2 Jan.ai Client Deployment

### Installation Steps
1. **Download official release**: Check for the Apple Silicon build at [https://jan.ai](https://jan.ai) and download it.
2. **Install package**: Open the downloaded dmg archive and move it to the Applications folder.
3. **Create runtime directory**: On first launch, a virtual acceleration engine is built inside the system and a default working directory is created.

---

## 3.3 Local Model Directory Topology

Jan.ai's core value lies in its clear directory structure. On macOS, all models are strictly isolated and placed under the following system path.

```bash
~/Library/Application Support/Jan/data/llamacpp/models/
├── Qwen-3.5-3B/                    # Individual model container created manually by the user
│   ├── qwen-3.5-3b-q8_0.gguf      # Downloaded binary weight file
│   └── model.yml                   # Environment manifest file for interpreting the weights
│
└── Qwen3.6-35B-A3B-I-Compact/
    ├── qwen3.6-35b-i-compact.gguf
    └── model.yml
```

**Directory composition rules:**
- Create an independent subdirectory for each model.
- Each directory consists minimally of a single binary file (`.gguf`) and an environment configuration manifest (`model.yml`).

---

## 3.4 Writing the `model.yml` Specification

The `model.yml` file is the blueprint that describes how the acceleration engine loads local weights onto the physical chipset. Here is the recommended specification for eliminating unnecessary configuration overhead and achieving optimal efficiency.

### Template Specification (Unified Chipset Optimized Version)

```yaml
# ~/Library/Application Support/Jan/data/llamacpp/models/<model_name>/model.yml
id: qwen-3.5-3b-local     # Unique model identifier used for invocation
name: Qwen 3.5 3B (Local) # Alias displayed in the interface
engine: llamacpp          # Inference runtime engine designation

# Inference control parameters
ctx_len: 4096             # Context window size (key to memory control)
temperature: 0.7          # Output randomness
top_p: 0.9                # Sampling probability threshold
max_tokens: 2048          # Maximum output token constraint per generation

# Apple Silicon hardware acceleration settings
n_gpu_layers: -1          # -1 offloads all model computation layers to Metal GPU immediately

# Prompt composition protocol (ChatML specification)
prompt_template: "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
stop:
  - "<|im_end|>"
  - "<|im_start|>"
```

### Detailed Parameter Control

- **`ctx_len` (Context Length)**: The range of history the model remembers at once. Arbitrarily increasing this causes memory allocation at inference time to grow exponentially, slowing things down. Tune it to match your task scope.
- **`n_gpu_layers`**: On Apple Silicon MacBooks, the CPU and GPU share RAM, so unconditionally setting it to `-1` to load the entire model onto the GPU is the fastest approach.

---

## 3.5 Model Migration and CLI Download

A practical protocol for copying weight files already downloaded via LM Studio into the Jan.ai repository, or precisely obtaining the required version using the Hugging Face CLI.

### Method 1: Direct Local Filesystem Integration (Immediate Transfer)
If the file is already downloaded, migration is complete by simply creating the local directory — no network bandwidth wasted.

```bash
# 1. Create target directory
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 2. Transfer from existing LM Studio model storage path
cp ~/Documents/LM\ Studio/models/qwen-3.5-3b-q8_0.gguf \
   ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B/

# 3. Create the model.yml file from Section 3.4 inside that folder
```

### Method 2: Direct Import via Hugging Face CLI (Recommended)
The most precise process for losslessly downloading models at high speed from Hugging Face servers using the terminal.

```bash
# 1. Install Hugging Face CLI tool (deploy via either Python pip or Homebrew)
# Python package environment
pip install -U "huggingface_hub[cli]"

# Homebrew environment
brew install hf

# 2. Declare a local directory for the target model
mkdir -p ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B

# 3. Pinpoint-download only the specific file for the target model via CLI
huggingface-cli download \
  Qwen/Qwen-3.5-3B-GGUF \
  qwen-3.5-3b-q8_0.gguf \
  --local-dir ~/Library/Application\ Support/Jan/data/llamacpp/models/Qwen-3.5-3B
```

---

## 3.6 Acceleration Runtime Verification and Exception Handling

Once the model file deployment and `model.yml` writing are complete, restart Jan.ai — the model will appear in the left-side conversation target menu. Enter a basic utterance such as "Hello" and observe whether normal generation speed (50+ tok/s) is recorded.

### Troubleshooting

- **Model not appearing in list**: Most commonly caused by indentation errors in the `model.yml` code. Check for YAML parser errors and correct any typos.
- **Tokens-per-second speed degradation**: Verify that `n_gpu_layers` has not been overwritten with a value other than `-1`, and that Jan.ai is not running an x86 CPU emulation build instead of the Apple Silicon-native version.
- **Latency occurring**: Review whether the `ctx_len` value is excessively large and adjust it to fit the available local unified RAM.

File control authority is now yours. You are ready to push toward the extreme of hardware optimization. In the next Chapter 4, we'll analyze native inference techniques based on Apple's directly-tuned MLX framework — a superior acceleration alternative to GGUF.
