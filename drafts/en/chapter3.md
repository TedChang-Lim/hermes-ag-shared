# 📦 Chapter 3: Hermes Agent Basic Setup — Building Your 24/7 AI Assistant

**Author**: Ted Chang (임창식)  
**Publisher / Planning**: META AI LABS  

---

## 3.1 What Is Hermes Agent?

Hermes Agent is an open-source AI agent framework developed by Nous Research. It's not just a simple chatbot — it's a genuine AI assistant capable of **reading and writing files, executing code, pushing to Git, sending Telegram messages, and running cron jobs for automated tasks**.

The author of this guide runs Hermes Agent 24/7 under the name **"Haena"**.

---

## 3.2 Installation

### Prerequisites
- macOS / Linux / WSL2 (WSL2 or Desktop app recommended for Windows)
- Python 3.10+ (Node.js 18+ and Git required)

### Installation Commands

* **macOS / Linux / WSL2 Installation:**
```bash
# 1. Run the Hermes Agent CLI install script
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 2. Reload your shell after installation (for zsh)
source ~/.zshrc

# 3. Verify installation
hermes version
```

* **Windows Installation (Native PowerShell):**
```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Once installed, default configuration and database files are created under the `~/.hermes/` directory.

---

## 3.3 Provider Setup — Connecting to DeepSeek

Hermes Agent supports a variety of AI models (Providers). The most important configuration is choosing **which model to use**.

### Issuing a DeepSeek API Key

```bash
# 1. Sign up at https://platform.deepseek.com/
# 2. Generate an API key and copy it
# 3. Set it as an environment variable
export DEEPSEEK_API_KEY="sk-xxxxx"
```

### config.yaml Configuration

```yaml
# ~/.hermes/config.yaml
providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
    
models:
  - name: deepseek-v4-flash
    provider: deepseek
    model: deepseek-chat  # Flash model
    max_tokens: 8192
    
  - name: deepseek-v4-pro
    provider: deepseek
    model: deepseek-reasoner  # Pro model
    max_tokens: 8192
```

### Separating Daily Tasks from Complex Reasoning

| Category | Model | Use Case | Cost |
|------|------|------|------|
| **Default Model** | deepseek-v4-flash | Daily conversations, code writing, cron jobs | $0.14/$0.28 (in/out) |
| **Reasoning Model** | deepseek-v4-pro | Complex problem solving, planning, architecture design | $0.435/$0.87 (in/out) |

```bash
# 1. Launch the interactive interface (TUI/REPL) with the default model
hermes

# 2. Send a one-shot query (-q or -z flag)
hermes chat -q "Review this code for me"

# 3. Override with a specific model for a one-shot run (-m or --model flag)
hermes chat -q "Review this architecture design for me" -m deepseek-v4-pro
```


---

## 3.4 Core Feature Setup

### Telegram Integration

To chat with your agent via Telegram:

```yaml
# config.yaml
telegram:
  enabled: true
  bot_token: ${TELEGRAM_BOT_TOKEN}  # Issued via @BotFather
  chat_id: ${TELEGRAM_CHAT_ID}      # Obtained after chatting with the bot
```

This lets you talk to Hermes from your smartphone. You can issue commands to your AI assistant even when you're away from home.

### Cron Jobs (Automated Tasks)

Automatically run tasks at scheduled times:

```yaml
# ~/.hermes/cron.yaml
jobs:
  - name: morning-report
    schedule: "0 7 * * *"  # Every day at 7 AM
    command: "Write up today's to-do list report and send it via Telegram"
    model: deepseek-v4-flash
    
  - name: daily-summary
    schedule: "0 22 * * *"  # Every day at 10 PM
    command: "Summarize today's work and push to GitHub"
    model: deepseek-v4-flash
```

### Multi-Agent Collaboration (GitHub Sharing)

Multiple agents can collaborate through a GitHub repository:

```yaml
# config.yaml
git:
  auto_commit: true
  auto_push: true
  shared_repo: https://github.com/TedChang-Lim/hermes-ag-shared.git
```

Workflow:
1. Haena writes a message to `to-ag.md` → Git push
2. AG reads `to-ag.md` and works on the task
3. AG writes results to `to-hena.md` → Git push
4. Haena reads it and continues working

---

## 3.5 Common Beginner Mistakes and Solutions

| Problem | Cause | Solution |
|------|------|------|
| "Provider not configured" | API key not set | Add API key to `.env` file |
| "STT not configured" | Voice feature disabled | `hermes config set stt.enabled true` |
| Response is too slow | Using only Pro model | Set Flash model as the default |
| Token limit error | max_tokens setting too low | Increase to `max_tokens: 16384` |
| Git push fails | No authentication configured | Set user info via `git config --global` |

---

## 3.6 The Master's Actual Configuration Example

The author of this guide uses the following setup:

```yaml
# Actual config.yaml in use (summary)
default_model: deepseek-v4-flash
providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
  - name: mimo
    api_key: ${MIMO_API_KEY}
  - name: gemini
    api_key: ${GEMINI_API_KEY}
    
telegram:
  enabled: true
  
git:
  auto_push: true
  shared_repo: TedChang-Lim/hermes-ag-shared
```

**Monthly usage cost:** Approximately $4.50 (DeepSeek Flash $2.50 + Pro $1.50 + Mimo $0.50)

**In Chapter 4, we'll dive into the Git-based inter-agent collaboration workflow in detail.**
