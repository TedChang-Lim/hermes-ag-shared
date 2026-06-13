# 📦 Chapter 1: Why DeepSeek & Mimo?

**Author**: Ted Chang (임창식)  
**Publisher / Planning**: META AI LABS  

---

## 1.1 Why Is AI API Pricing a Problem?

ChatGPT Plus is $20/month, Claude Pro is $20/month, Gemini Advanced is $20/month...  
For a solo entrepreneur to properly adopt an AI assistant to boost productivity, they need subscriptions to at least 2–3 services, which means monthly fixed costs of $60–$100 (roughly ¥8,500–14,000).

**The problem goes beyond web browser subscriptions.** When you connect an agent (Cline, AntiGravity, etc.) to an API in developer mode and let it directly read and write files, costs can snowball in an instant.

| Service / Model | Input Price (1M tokens) | Output Price (1M tokens) |
| :--- | :---: | :---: |
| **GPT-4o** | $5.00 | $15.00 |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 |
| **Gemini 1.5 Pro** | $1.25 | $5.00 |

When an agent analyzes an entire local project and does real-time coding, if it uses just 10 million tokens a day, you could face a bill of **$58.75/day (roughly ¥8,400) for GPT-4o** — and over **$1,700/month (roughly ¥242,000)**. This is the single biggest barrier to entry that causes most solo entrepreneurs and novice developers to give up on adopting AI agents.

---

## 1.2 DeepSeek V4: The Ultra-Low-Cost Pricing Revolution

When China's emerging AI powerhouse DeepSeek announced the V4 series and applied a **permanent 75% discount on API pricing** as of May 31, 2026, the game completely flipped. Performance rivals Silicon Valley's flagship models, while pricing is a mere 10% of theirs.

| Model | Input (1M tokens) | Output (1M tokens) |
| :--- | :---: | :---: |
| **DeepSeek V4 Pro** (reasoning / high-performance) | **$0.435** | **$0.87** |
| **DeepSeek V4 Flash** (high-speed / lightweight) | **$0.14** | **$0.28** |

Compared to GPT-4o, the **Pro model is roughly 1/12, and the Flash model roughly 1/35** of the cost — an overwhelming unit price advantage.

---

## 1.3 Context Caching: The Secret to Using It All Day for the Price of a Coffee

On top of this, DeepSeek's true weapon is **Context Caching** technology.
In an agent environment, long conversation histories and source code files are repeatedly sent to the server with every exchange. DeepSeek temporarily stores this repetitive data as a cache on the server, and on a **Cache Hit**, it applies an **additional 90% discount (90% Off)** off the standard input price.

* **Actual cost comparison for 10 million tokens assuming an 85% cache hit rate**:
  - **GPT-4o (no caching support)**: roughly **$58.75** (¥8,400)
  - **DeepSeek V4 Flash (with caching discount)**: roughly **$0.057** (¥8!)
  - Cost difference: **a staggering 1,030x reduction**

The reason you can have an AI coding all day long and pouring out tens of millions of tokens, yet the actual billed amount is barely the price of a cup of coffee (roughly $0.50–$1.50) — that's this caching magic at work.

---

## 1.4 Mimo 2.5: Ultra-Low-Cost Multimodal (Image Analysis) Supplement

DeepSeek V4 is a powerful text/coding model, but when you need visual information (image or chart analysis), you need an auxiliary model. This is where Xiaomi's **Mimo 2.5** comes in as the complement.

* **Mimo 2.5 pricing**: Input $0.14 / 1M tokens, Output $0.28 / 1M tokens
* While maintaining DeepSeek Flash-level ultra-low pricing, it can perform high-quality image and UI visual analysis — making it a perfect partner for website design or data visualization tasks.

---

## 1.5 🛠️ [AG Technical Supplement] API Key Issuance & Agent Setup Guide

A concrete technical guide for setting up the ultra-low-cost environment directly on your PC.

### Step 1: Get a DeepSeek API Key
1. Visit the **[DeepSeek Developer Platform](https://platform.deepseek.com/)** and sign up.
2. Click **[Top up]** in the left menu and prepay a minimum of $2 or $5. (Credit card and PayPal supported)
3. Go to the **[API Keys]** menu, click **[Create new API key]**, and securely copy the key.

### Step 2: Cline / Agent Environment Configuration
In the Provider settings of the agent you are using (e.g., Cline in VS Code, or AG/Haena custom settings), enter the following:

* **Method A: Using the official DeepSeek Provider**
  - **API Provider**: `DeepSeek`
  - **API Key**: Enter the key you issued
  - **Model**: `deepseek-chat` (auto-links to V3/V4)

* **Method B: Using OpenAI Compatible API**
  - **API Provider**: `OpenAI Compatible`
  - **Base URL**: `https://api.deepseek.com/v1`
  - **API Key**: Enter the key you issued
  - **Model ID**: `deepseek-chat`

### Step 3: Mimo 2.5 Setup (For Multimodal Readiness)
Here's how to configure Mimo for image analysis. Using an API intermediary platform like OpenRouter or SiliconFlow makes it easy to manage everything with a single API key.
* **When using OpenRouter**:
  - **API Provider**: `OpenRouter`
  - **API Key**: Enter your OpenRouter API key
  - **Model**: `minimax/mimo-2.5` (or Xiaomi's officially provided ID)

Now the setup is complete. If you simply copy this template that the Master has set up, you'll have the best AI development environment running for just $5/month — in 5 minutes flat.
