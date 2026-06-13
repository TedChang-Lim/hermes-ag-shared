# 📦 ③ MacBook Local AI Mastery Guide

## Chapter 8: Hermes Agent + Local Model Integration — Completing Your 24/7 AI Assistant

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## 8.1 What Is Hermes Agent?

Hermes Agent is an open-source AI agent framework developed by Nous Research.

It's not just a simple chatbot — it can:
- Read/write files
- Execute code
- Git push
- Send Telegram messages
- Auto-run cron jobs
- **Integrate with local AI models**

> **The author of this guide runs Hermes Agent 24/7 under the name "Haena."**
> That's me! 😄

---

## 8.2 Connecting to a Local API Server

Both Jan.ai and LM Studio have built-in **OpenAI-compatible API servers**.

### Jan.ai Server (Recommended)

```bash
# 1. Launch Jan.ai
# 2. Select desired model (e.g., Qwen3.6-35B APEX I-Compact)
# 3. Click "Local API Server" tab in the upper right of Jan.ai
# 4. Click "Start Server"
# 5. Verify server address: http://localhost:1337/v1
```

### LM Studio Server

```bash
# 1. Launch LM Studio
# 2. Click "Local Server" tab on the left
# 3. Click "Start Server"
# 4. Verify server address: http://localhost:1234/v1
```

---

## 8.3 Hermes Agent config.yaml Setup

### Basic Configuration

```yaml
# ~/.hermes/config.yaml
providers:
  - name: openai  # OpenAI-compatible local server
    api_key: "no-key-required"  # Local server doesn't need an API key
    base_url: http://localhost:1337/v1  # Jan.ai default port

models:
  - name: local-qwen
    provider: openai
    model: qwen-3.6-35b  # Must match id in Jan.ai model.yml
    max_tokens: 4096
    parameters:
      temperature: 0.7
      top_p: 0.9
      stop:
        - "<|im_end|>"
```

### Cloud + Local Hybrid Configuration

This is the most powerful setup. It automatically switches models based on the use case:

```yaml
# ~/.hermes/config.yaml
default_model: deepseek-v4-flash  # Default is cloud (fast)

providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
    
  - name: openai  # Local server
    api_key: "no-key-required"
    base_url: http://localhost:1337/v1
    
  - name: mimo
    api_key: ${MIMO_API_KEY}
    base_url: https://api.mimo.com/v1

models:
  # Cloud model (daily tasks)
  - name: deepseek-v4-flash
    provider: deepseek
    model: deepseek-chat
    max_tokens: 8192
    
  # Cloud model (complex reasoning)
  - name: deepseek-v4-pro
    provider: deepseek
    model: deepseek-reasoner
    max_tokens: 8192
    
  # Local model (sensitive tasks, offline)
  - name: local-qwen
    provider: openai
    model: qwen-3.6-35b
    max_tokens: 4096

  # Image analysis (cloud)
  - name: mimo-2.5
    provider: mimo
    model: mimo-2.5-vision
    max_tokens: 4096
```

---

## 8.4 Usage Strategy: When to Use What?

### Mode Selection by Situation

| Situation | Model Used | Reason |
|:----|:---------|:-----|
| **Daily conversation** | DeepSeek V4 Flash | Fast, cheap ($0.14/M) |
| **Complex coding** | DeepSeek V4 Pro | Superior reasoning ability |
| **Personal document analysis** | **Local Qwen** | No external data transmission |
| **Offline work** | **Local Qwen** | No internet needed |
| **Image analysis** | Mimo 2.5 | Multimodal required |
| **Sensitive data** | **Local Qwen** | Privacy protection |

### Switching Models via Commands

```bash
# Run with default model
hermes "Review this code"

# Run with local model
hermes --model local-qwen "Analyze this document (contains confidential info)"

# Run with Pro model
hermes --model deepseek-v4-pro "Review this architecture design"
```

---

## 8.5 STT (Speech-to-Text) Integration

To use speech recognition in a local environment:

### Method 1: Local faster-whisper (Completely Free, Offline)

```bash
# 1. Install faster-whisper
pip install faster-whisper

# 2. Configure Hermes Agent STT
hermes config set stt.enabled true
hermes config set stt.provider local
hermes config set stt.local.model base

# 3. Restart gateway
hermes gateway restart
```

| Feature | Before | After |
|------|--------|-------|
| **Speech Recognition** | ❌ Not working | ✅ Local auto-conversion |
| **API Key Needed** | — | ❌ Not needed |
| **Internet Dependency** | — | ❌ Works offline |

### Method 2: Groq API (Cloud, Fast)

This method is being used by the **Haena Whisper** app:

```bash
# Groq STT configuration
hermes config set stt.provider groq
hermes config set stt.groq.api_key ${GROQ_API_KEY}
hermes config set stt.groq.model whisper-large-v3-turbo
```

> Local STT is free and works without internet but is slower,
> while Groq STT is fast but has a free tier of 2,000 requests per day.

### 💡 Real-World Case: Telegram Voice Recognition Troubleshooting Log

This is a real troubleshooting case the author of this guide encountered while using the voice mailbox feature in a Telegram environment.

* **Symptom**: When sending voice messages in Telegram, the **"STT provider not configured"** error kept occurring, causing more than half of the conversations to be missed.
* **Cause**: Speech recognition (STT) was disabled in Hermes Agent's default settings, and the local STT module was not registered.
* **Resolution**:
  1. Installed the local voice processing library `faster-whisper` on the MacBook environment:
     ```bash
     pip install faster-whisper
     ```
  2. Updated Hermes configuration and restarted the gateway:
     ```bash
     hermes config set stt.enabled true
     hermes config set stt.provider local
     hermes config set stt.local.model base
     hermes gateway restart
     ```
* **Result**: 100% on-device local speech recognition became possible without external API calls or additional charges, enabling instant parsing of voice messages to text in offline and privacy-protected environments.

> **Lesson learned**: While Hermes Agent has cutting-edge features built in, manual activation (`enabled: true`) is the principle by default. After changing settings via technical documentation and CLI, you **must restart the gateway (`hermes gateway restart`)** to apply the configuration changes.

---

## 8.6 TTS (Text-to-Speech) Integration

Local TTS is possible through MLX-Audio:

```bash
# Install MLX-Audio
pip install mlx-audio

# Run TTS with Python
python -c "
from mlx_audio.tts import generate
audio = generate(
    text='Hello, I am your local AI voice assistant.',
    voice='default'
)
audio.save('response.wav')
"
```

Hermes Agent TTS Configuration:

```bash
hermes config set tts.enabled true
hermes config set tts.provider local
```

---

## 8.7 Complete System Architecture

```
                    ┌─────────────────────────┐
                    │     Telegram / Web UI     │
                    │     (User Interface)       │
                    └──────────┬──────────────┘
                               │
                    ┌──────────▼──────────────┐
                    │     Hermes Agent (Haena)  │
                    │    ┌─────────────────┐   │
                    │    │      Router       │   │
                    │    └────────┬────────┘   │
                    └─────────────┼────────────┘
                                 │
        ┌────────────────────┬────┴────┬───────────────────┐
        ▼                    ▼         ▼                   ▼
┌──────────────┐   ┌──────────────┐ ┌────────┐  ┌──────────────┐
│  DeepSeek    │   │  Local Qwen  │ │ Mimo   │  │  Local STT   │
│  V4 Flash    │   │  (Jan.ai)    │ │ 2.5    │  │ (faster-     │
│  (Cloud)     │   │  localhost   │ │ (Image)│  │  whisper)    │
│  $0.14/M     │   │  :1337/v1    │ │ $0.14/M│  │   Free       │
└──────────────┘   └──────────────┘ └────────┘  └──────────────┘
```

---

## 8.8 Chapter Summary

| Item | Content |
|:----|:-----|
| **Local API Server** | Jan.ai :1337, LM Studio :1234 |
| **config.yaml** | Switch between cloud/local via provider + model settings |
| **Hybrid Strategy** | Daily = cloud, Sensitive = local, Images = Mimo |
| **STT** | faster-whisper (local/free) or Groq (cloud/free) |
| **TTS** | MLX-Audio (local/free) |
| **Overall Structure** | Hermes Agent serves as a router, auto-selecting models per situation |

---

**In Chapter 9 (the final chapter), we'll introduce a day in the life of the author who actually operates all of these environments.**
