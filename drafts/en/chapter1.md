# Chapter 1: The Ultimate Cost-Effectiveness Combination — Why You Should Choose DeepSeek and MiMo

**Author**: Ted Chang (임창식)  
**Publisher / Planning**: META AI LABS

---

## 1.1 The Real-World Problem of AI Subscription Fees and API Costs

If you subscribe to ChatGPT Plus, Claude Pro, and Gemini Advanced simultaneously for productivity gains, your monthly fixed costs alone reach at least $60–$100 (approximately 1–1.5 million KRW per year). For a solo entrepreneur or independent developer, this is by no means a light fixed expense.

The real problem isn't the web browser subscription fees. When you move into the development phase — connecting agents like Cline or AntiGravity to directly read and write your project's source code — API call costs spiral out of control.

| Service / Model | Input Price (per 1M tokens) | Output Price (per 1M tokens) |
| :--- | :---: | :---: |
| **GPT-5.5 (estimated / giant model)** | $5.00 | $15.00 |
| **Claude 4.8 / 3.5 Sonnet** | $3.00 | $15.00 |
| **Gemini 1.5 Pro** | $1.25 | $5.00 |

When an agent analyzes your entire local project and performs real-time coding, using just 10 million tokens per day with a GPT-class model results in a billing shock of roughly $80 per day — over $2,300 per month. This is the decisive reason most individuals abandon AI agent adoption midway.

---

## 1.2 The Rebellion of the Cheapest Brains

As an alternative to the expensive, heavyweight AI giants (GPT 5.5, Claude 4.8, GLM 5.2), the concept of the **"Cheapest Brains"** has emerged. Individually, their performance scores may lag behind the top-tier prodigy models, but this strategy chains together three lightweight models boasting extreme cost-effectiveness to produce ultra-low-cost synergy.

* **Haena (Hermes Agent)**: Its main engine is the lowest-unit-cost **DeepSeek V4 Flash** (input $0.14 per 1M tokens). It handles most everyday conversations and first-pass coding.
* **AG (Antigravity)**: Equipped with the lightest and cheapest **Gemini Flash Low** version in the Google Gemini lineup.
* **MiMo (MiMo Code)**: Instead of the heavy Pro model, it operates exclusively on the lowest-unit-cost **MiMo Base** version.

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
| :--- | :---: | :---: |
| **DeepSeek V4 Pro** (reasoning / high-performance) | **$0.435** | **$0.87** |
| **DeepSeek V4 Flash** (high-speed / lightweight) | **$0.14** | **$0.28** |
| **Gemini Flash Low** (structuring / design) | **$0.075** | **$0.30** |
| **MiMo Base** (design / UI implementation) | **$0.14** | **$0.28** |

This combination delivers an overwhelming cost reduction of up to **1/35** compared to expensive giant models.

---

## 1.3 Achieving a 90% Additional Discount with Context Caching

Another central pillar of cost savings is the **Context Caching** technology provided by DeepSeek.

In an agent environment, previous conversation history and source code files are repeatedly transmitted to the server with every query. DeepSeek temporarily stores this duplicate data on the server, and on a **cache hit**, it slashes the original input unit price by 90%.

* **Actual cost comparison for 10 million tokens at an 85% cache hit rate**:
  - **GPT-4o (without caching)**: approximately $58.75 (roughly 80,000 KRW)
  - **DeepSeek V4 Flash (with caching applied)**: approximately $0.057 (roughly 78 KRW)
  - **Cost reduction ratio**: approximately 1,030×

This is why, even when you have AI coding all day and transmitting tens of millions of tokens, your actual daily bill stays at the price of a cup of coffee — around $0.50 to $1.50.

---

## 1.4 Tools That Shatter the Limits of Eyeless Text Models

Lightweight text models are fast at constructing logic, but they have weaknesses: they cannot see visual information (images, UI) and cannot fetch blocked web information. To overcome these limitations, powerful, zero-cost open-source frameworks and local CLI tools are ported in.

### ① Open Design Framework
A $0-cost design integration system that injects verified UI guidelines — Stripe, Linear, and Vercel style — into text-only models. It helps produce top-tier premium dark + gold UI proposals without using expensive multimodal models.

### ② Insane Search CLI
A completely free local engine that bypasses web application firewalls (WAFs) like Cloudflare and anti-crawling barriers to collect the latest information. It operates as an on-demand CLI — no paid crawling APIs, zero battery and RAM footprint on your MacBook, invoked only when needed and instantly terminated afterward.

---

## 1.5 Practical API Key Issuance and Development Environment Setup

This is the initial setup guide for building an ultra-cost-effective agent environment.

### Step 1: Issuing a DeepSeek API Key
1. Visit the [DeepSeek Developer Platform](https://platform.deepseek.com/) and sign up.
2. Click **[Top up]** in the left menu and preload a small amount — around $2 to $5.
3. In the **[API Keys]** menu, click **[Create new API key]**, copy the generated key, and store it in a safe place.

### Step 2: Cline / Agent Integration Setup
Enter the following values in your agent's Provider settings (e.g., the VS Code extension Cline):

* **OpenAI Compatible API method**:
  - **API Provider**: `OpenAI Compatible`
  - **Base URL**: `https://api.deepseek.com/v1`
  - **API Key**: Enter your issued key
  - **Model ID**: `deepseek-chat` (auto-maps to V3/V4)

### Step 3: MiMo Base and Gemini Flash Low Setup
Using an API intermediary platform like OpenRouter or SiliconFlow lets you conveniently integrate the entire Cost-Effectiveness Trio with a single API key and wallet.

* **When using OpenRouter**:
  - **API Provider**: `OpenRouter`
  - **API Key**: Enter your OpenRouter API key
  - **Model**: `minimax/mimo-2.5` (or Xiaomi's official provided ID) and `google/gemini-2.5-flash`

With just five minutes of setup, a high-performance AI development environment capable of unlimited operation for roughly 5,000 KRW per month is ready on your computer.
