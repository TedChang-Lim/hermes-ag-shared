# Chapter 3: Hermes Agent Configuration — Building a 24/7 AI Agent System

**Author**: Ted Chang (임창식) | **Published/Planned by**: META AI LABS

---

## 3.1 Hermes Agent: The 24-Hour Background Worker

Hermes Agent goes far beyond a simple conversational chatbot. It is a background agent engine that handles file control, code execution, Git synchronization, and Cron-based periodic automation tasks — all in one stop.

The system serves as a pivotal assistant that executes uninterrupted background jobs even while the developer is away — whether during the early hours of the morning or while on the move.

---

## 3.2 Installation and Preparation

### System Requirements
- **OS**: macOS, Linux, or Windows WSL2 environment
- **Runtime**: Python 3.10+, Node.js 18+, and a Git build environment

### CLI Installation
* **macOS / Linux / WSL2:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
  source ~/.zshrc
  hermes version
  ```

* **Windows (Native PowerShell):**
  ```powershell
  iex (irm https://hermes-agent.nousresearch.com/install.ps1)
  ```

---

## 3.3 Connecting the "Cheapest Brain": API and Model Configuration

### Injecting API Key Environment Variables
```bash
export DEEPSEEK_API_KEY="sk-xxxxx"
export GEMINI_API_KEY="AIzaSyxxxxx"
export MIMO_API_KEY="mm-xxxxx"
```

### config.yaml Setup
```yaml
providers:
  - name: deepseek
    api_key: ${DEEPSEEK_API_KEY}
    base_url: https://api.deepseek.com/v1
  - name: gemini
    api_key: ${GEMINI_API_KEY}
    base_url: https://generativelanguage.googleapis.com/v1beta
  - name: mimo
    api_key: ${MIMO_API_KEY}
    base_url: https://api.mimo.ai/v1

models:
  - name: deepseek-v4-flash
    provider: deepseek
    model: deepseek-chat
    max_tokens: 8192
  - name: gemini-flash-low
    provider: gemini
    model: gemini-2.5-flash
    max_tokens: 8192
  - name: mimo-base
    provider: mimo
    model: mimo-2.5-base
    max_tokens: 8192
```

| Model Name | Role | Characteristics | Unit Price (1M in/out) |
|------|------|------|------|
| **deepseek-v4-flash** | General computation, text processing | Low-cost bulk token processing | $0.14 / $0.28 |
| **gemini-flash-low** | Structuring, file management | Wide context window, fast structure validation | $0.075 / $0.30 |
| **mimo-base** | UI guide analysis & design | Superior template code implementation | $0.14 / $0.28 |

---

## 3.4 Equipping the Insane Search CLI Crawler for Near-Zero RAM Overhead

When the agent needs to scrape external internet information in real time or collect data from sites with heavy firewall protection — such as Naver, Coupang, and the like — conventional request methods are easily blocked.

To overcome this, we inject the **Insane Search CLI** tool into the agent. The architecture is **on-demand**: rather than keeping a local daemon or heavy backend API server running 24/7, commands are invoked as one-shot operations only when crawling is needed, executing in under a second before vanishing from memory.

### Installing Insane Search CLI and Connecting It to the Agent
```bash
pip install insane-search curl_cffi playwright
playwright install chromium
mkdir -p ~/.local/bin
ln -s $(which insane-extract) ~/.local/bin/insane-extract
chmod +x ~/.local/bin/insane-extract
```

```bash
~/.local/bin/insane-extract "https://news.ycombinator.com"
```

With this combination, you achieve a **completely free $0 crawling system** — no paid crawling proxy service subscription required.

---

## 3.5 Telegram Integration and Automation Schedule Configuration

### Connecting Telegram Messenger
```yaml
telegram:
  enabled: true
  bot_token: ${TELEGRAM_BOT_TOKEN}
  chat_id: ${TELEGRAM_CHAT_ID}
```

### Cron Schedule Management
```yaml
jobs:
  - name: morning-briefing
    schedule: "0 7 * * *"
    command: "Crawl today's major industry news using Insane Search CLI, then summarize the key points and send them via Telegram."
    model: deepseek-v4-flash
  - name: backup-repository
    schedule: "0 23 * * *"
    command: "Organize all of today's changed work code and sync it to the GitHub remote repository."
    model: gemini-flash-low
```

**In Chapter 4, we will take a detailed look at how two or more cost-effective agents implement teamwork using a Git repository as an intermediary.**
