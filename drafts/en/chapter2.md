# 📦 Chapter 2: Caching Strategy — Using 50 Million Tokens a Day for the Price of a Coffee

**Author**: Ted Chang (임창식)  
**Publisher / Planning**: META AI LABS  

---

## 2.1 What Is Context Caching?

Every time you use an AI API, if you have to send the entire conversation from scratch each time, it gets expensive. In most tasks, we end up repeatedly sending the same system prompts, the same documents, and the same config files.

**Context Caching** is a technology that stores this frequently used content on the server and, on the next request, processes it at a **discounted price** — essentially saying, "Oh, I've already seen this before."

To put it in an analogy:
> It's like buying a recipe once, keeping it in the fridge, and only paying for the ingredients each time thereafter.

---

## 2.2 DeepSeek's Caching Architecture

The DeepSeek V4 series supports **automatic context caching**. No additional configuration is required on the user's part — caching is automatically applied whenever the same prompt prefix repeats.

| Item | Description |
|------|------|
| **Application Method** | Automatic (no additional user setup required) |
| **Discount Rate** | Up to **90% off** input tokens |
| **Caching Unit** | Automatically applied when prompt prefixes match |
| **Session Persistence** | Effectiveness maximized when maintaining the same context within a single conversation session |

---

## 2.3 The Caching Effect: Real Numbers

Let's assume an agent sends 10 million prompt tokens and receives 2 million output tokens every day.

**Without Caching (Cache Hit Rate 0%):**

| Model | Daily Cost | Monthly Cost |
|------|---------|---------|
| DeepSeek V4 Pro | $14.79 | $443.70 |
| DeepSeek V4 Flash | $4.36 | $130.80 |
| GPT-4o | $587.50 | $17,625.00 |

**With 85% Cache Hit Rate (based on the Master's actual environment):**

| Model | Daily Cost | Monthly Cost |
|------|---------|---------|
| DeepSeek V4 Pro | $2.76 | $82.87 |
| DeepSeek V4 Flash | $0.89 | **$26.67** |
| GPT-4o | $58.75 | $1,762.50 |

> **DeepSeek V4 Flash + 85% Caching = $26.67/month**
> 
> The same workload with GPT-4o = **$1,762.50/month**

The difference is **66x**.

---

## 2.4 5 Secrets to Boosting Your Cache Hit Rate

### ① Keep Your System Prompts Fixed

Keep the system prompt (behavioral instructions) you give your agent the same every time. Changing it every time resets the caching.

```yaml
# Bad example: different prompts every time
- "You are a helpful AI assistant"
- "You are a coding helper"

# Good example: always the same prompt
- "You are a helpful AI coding assistant. Follow these rules: ..."
```

### ② Keep Frequently Referenced Documents Fixed

Attaching the same files (.clinerules, config.yaml, README.md) every time accumulates caching benefits.

### ③ Keep Conversation Sessions Long

Caching is reset every time you start a new session. So, working in the same session for as long as possible is advantageous.

### ④ Stop Unnecessary Repeated File Reads

While caching applies when an agent reads the same file multiple times, the first read is always treated as a Cache Miss. Instruct your agent in .clinerules to rely on memory for content it has already read once.

### ⑤ Minimize Output Tokens Too

Caching only applies to input (prompts). Output (completion) tokens receive no discount, so configure your agent not to output unnecessarily long explanations.

---

## 2.5 Practical: .clinerules Caching Optimization Template

Using the `.clinerules.template` included in this guide's Pro package will maximize your caching:

```yaml
# 💸 Cost Optimization Guidelines
## Optimize for Cache Hits:
- Keep system prompts and instructions consistent
- Do not arbitrarily modify system files
- Read large files only once; rely on memory or caching
## Minimize Token Output:
- Focus on concise explanations; avoid long summaries
- Replace specific lines instead of rewriting entire files
## Session Re-initialization:
- Start a new session when conversation history exceeds 50,000 tokens
```

---

## 2.6 Summary: The Revolution Caching Brings

| Cache Hit Rate | DeepSeek V4 Flash Monthly Cost | GPT-4o Monthly Cost |
|:----------:|:------------------------:|:--------------:|
| 0% | $130.80 | $17,625.00 |
| 50% | $65.40 | $8,812.50 |
| 70% | $39.24 | $5,287.50 |
| **85%** | **$26.67** | **$1,762.50** |
| 95% | $13.08 | $881.25 |

By keeping your cache hit rate above 85%, you can run an AI agent 24/7 for **under $27/month**.

**In Chapter 3, we'll walk through how to actually build this environment, step by step.**
