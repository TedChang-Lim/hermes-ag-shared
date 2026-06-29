# Chapter 2: Caching Strategy — How to Control 50 Million Tokens a Day for the Price of a Coffee

**Author**: Ted Chang (임창식) | **Publisher/Planning**: META AI LABS

---

## 2.1 Context Caching: Turning Repetitive Resources Into Assets

When you deploy AI agents in the real world, the same prompt instructions, codebase information, and configuration files are sent to the server repeatedly with every call. Under a typical API calling model, you are billed for this duplicate data in full — resulting in bills that are impossible to sustain.

**Context Caching** is a technique that stores frequently referenced data in server memory and retrieves it directly from the cache when subsequent requests come in, rather than re-transmitting it. It works on the same principle as reaching into your refrigerator for prepped staple ingredients instead of buying everything fresh for every meal — cutting both preparation time and cost. DeepSeek offers an **aggressive discount of up to 90%** on these cache-hit segments.

---

## 2.2 DeepSeek's Automatic Caching Mechanism

The DeepSeek V4 lineup supports **automatic context caching** that operates without any dedicated API parameters or architectural redesign. When the data in the prefix portion of the prompt remains identical, the system applies caching on its own.

| Item | Details |
|------|---------|
| **How it works** | Automatic system detection (no user configuration required) |
| **Discount benefit** | **90% discount** on input tokens in cache-hit regions |
| **Detection criteria** | String/token match starting from the beginning of the prompt |
| **Optimal environment** | Maximized when maintaining consistent context within a single conversation thread |

---

## 2.3 Cost Simulation: The Power of Caching

We'll run a comparison against a hypothetical project environment where an agent transmits an average of 10 million prompt tokens per day and receives 2 million tokens of code in response.

**Without Caching (0% hit rate):**

| Model | Daily Cost | Monthly Equivalent |
|------|:---------:|:------------------:|
| DeepSeek V4 Pro | $14.79 | $443.70 |
| DeepSeek V4 Flash | $4.36 | $130.80 |
| GPT-4o (large model) | $587.50 | $17,625.00 |

**With 85% Cache Hit Rate (real-world development environment):**

| Model | Daily Cost | Monthly Equivalent |
|------|:---------:|:------------------:|
| DeepSeek V4 Pro | $2.76 | $82.87 |
| **DeepSeek V4 Flash** | **$0.89** | **$26.67** |
| GPT-4o (large model) | $58.75 | $1,762.50 |

With an 85% cache hit rate applied to DeepSeek V4 Flash, the monthly cost drops to $26.67. By contrast, running the same workload on a typical large model without caching rings up roughly $1,762 per month. This is not a performance difference — it is a **cost gap of over 66x driven purely by differences in operational architecture**.

---

## 2.4 Five Principles for Maximizing Caching Efficiency

### ① Lock Down System Instructions (System Prompt)
The behavioral rules and guidelines you assign to your agent must always remain in a fixed format and text. If the instructions change from call to call, the cache breaks and computation starts over from scratch.

### ② Lock Down Common Reference Files
Shared assets that must be read every time — project rule files (`.clinerules`), project overview (`README.md`), environment configuration files (`config.yaml`) — should be placed at the top of the prompt to accumulate the benefits of caching.

### ③ Careful Management of Conversation Threads
Starting a completely new session severs the server-side caching connection. It is therefore more economical to keep related tasks running uninterrupted within a single session for as long as possible.

### ④ Block Unnecessary Duplicate File Loads
The agent's rules (`.clinerules`) must explicitly instruct it not to read the same code snippets or large files repeatedly. Content that has already been loaded into memory should be digested through the context retention capability wherever possible.

### ⑤ Control Response Length
The context caching discount applies exclusively to **input tokens**. There is no discount on the **output tokens** that the AI agent generates. You must therefore tighten the response style so that the agent does not re-output whole files or produce unnecessarily verbose explanations every time.

---

## 2.5 The "Value Trio" Custom `.clinerules` Caching Template

This is the optimal `.clinerules` template recommended in this guide. Applying these rules enables the agent to self-organize input data and control its own responses, preventing cost waste.

```yaml
# 💸 Cost & Performance Optimization Rules
## Cache Alignment:
- Keep the system instructions and workspace rules identical.
- Put common configuration and static reference documentation at the top of the context.
- Avoid modifying system rule files during an active coding session.
## Output Control:
- Produce exact code diffs instead of rewriting the entire file.
- Keep explanations concise, professional, and directly address the problem.
## Resource & Session Management:
- Utilize local on-demand CLI utilities (such as 'Insane Search CLI') to fetch external web contents dynamically, avoiding heavy backend server states.
- Re-initialize the conversation session once the context reaches 50,000 tokens to balance caching hit and token decay.
```

---

## 2.6 Cost Gap by Model Across Cache Hit Rates

| Cache Hit Rate | DeepSeek V4 Flash Monthly Cost | GPT-4o Monthly Cost |
|:-------------:|:------------------------------:|:-------------------:|
| 0% (no caching) | $130.80 | $17,625.00 |
| 50% | $65.40 | $8,812.50 |
| 70% | $39.24 | $5,287.50 |
| **85%** | **$26.67** | **$1,762.50** |
| 95% | $13.08 | $881.25 |

When you defend a cache hit rate of 85% or higher, even an agent running coding and monitoring tasks around the clock keeps the monthly bill below the equivalent of roughly 30,000 KRW.

**Chapter 3 builds on this cost-control architecture to explore how to concretely set up a locally running 24-hour agent (Hermes Agent).**
