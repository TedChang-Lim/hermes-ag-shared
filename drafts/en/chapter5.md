# 📦 Chapter 5: Master's 30-Day Usage Report and Cost Analysis — Running an AI Assistant for the Price of a Coffee

**Author**: Ted Chang (임창식)  
**Publisher / Planning**: META AI LABS  

---

## 5.1 The Backstory Behind This Guide

The author of this guide is a photographer with 30 years of engineering experience who runs two AI agents (Hermes Agent "Haena" and AntiGravity 2.0 "AG") 24/7 every day.

Before May 2026, he was spending $200–300 a month on ChatGPT, Claude, and Gemini. AI assistants were convenient, but **the cost was burdensome.**

Then he discovered the DeepSeek V4 series, and on May 31, 2026, when DeepSeek applied a **permanent 75% discount** on API pricing, the game completely changed.

---

## 5.2 Actual 30-Day Usage Data

### Daily Usage (Average)

| Item | Figure |
|------|------|
| Average daily requests | 150–250 |
| Average daily prompt tokens | 55 million tokens |
| Average daily output tokens | 8 million tokens |
| Cache hit rate | 85–92% |
| Active hours | 06:00 ~ 02:00 (20 hours) |

### 30-Day Cost Breakdown

| Model | Use Case | Monthly Cost |
|------|------|:---------:|
| DeepSeek V4 Flash | Daily tasks, code writing, cron jobs, Telegram responses | **$2.50** |
| DeepSeek V4 Pro | Complex reasoning, planning, architecture design | **$1.50** |
| Mimo 2.5 | Image analysis, writing | **$0.50** |
| **Total** | | **$4.50/month** |

> An AI assistant processing 55 million tokens a day is running for **$4.50/month.**
>
> The same workload with GPT-4o would have cost **$400–600/month**.

### Model Usage Breakdown

```
DeepSeek V4 Flash  ████████████████  55%  ($2.50)
DeepSeek V4 Pro    ████████          28%  ($1.50)
Mimo 2.5           ███                9%  ($0.50)
Other (free tier)  ██                8%  ($0.00)
```

---

## 5.3 DeepSeek vs. Competitor Comparison

### Monthly Cost Comparison at Equivalent Usage

| Model | Input (1M) | Output (1M) | Daily Cost | **Monthly Cost** |
|------|:--------:|:---------:|:---------:|:----------:|
| **DeepSeek V4 Flash** | $0.14 | $0.28 | $0.09 | **$26.67** |
| **DeepSeek V4 Pro** | $0.435 | $0.87 | $0.28 | **$82.87** |
| Mimo 2.5 | $0.14 | $0.28 | $0.09 | $26.67 |
| GPT-4o | $5.00 | $15.00 | $58.75 | $1,762.50 |
| Claude 3.5 Sonnet | $3.00 | $15.00 | $37.05 | $1,111.50 |
| Gemini 2.5 Pro | $1.25 | $5.00 | $22.50 | $675.00 |

> *Based on DeepSeek V4 Flash with 85% caching applied*

### What If There Were No Caching Effect?

| Cache Hit Rate | DeepSeek Flash Monthly Cost | GPT-4o Monthly Cost |
|:----------:|:---------------------:|:--------------:|
| 0% (no caching) | $130.80 | $1,762.50 |
| 50% | $65.40 | $881.25 |
| 70% | $39.24 | $528.75 |
| **85% (actual)** | **$26.67** | **$264.38** |
| 95% | $13.08 | $88.13 |

**Without caching, costs would have been 5x higher.**

---

## 5.4 A Day in the Life (The Author's Actual Routine)

| Time | Task | Model Used | Cost |
|:---:|------|:---------:|:----:|
| 07:00 | Request today's to-do list report via Telegram | Flash | $0.003 |
| 08:00 | Email summary and draft replies | Flash | $0.005 |
| 09:30 | Lecture syllabus planning and structure design | Pro | $0.015 |
| 11:00 | Code review and bug fixing | Flash | $0.008 |
| 13:00 | Image analysis (photo portfolio work) | Mimo | $0.005 |
| 14:30 | Review of cooperative association bylaws | Pro | $0.020 |
| 16:00 | Lecture preparation via Telegram | Flash | $0.003 |
| 19:00 | GitHub Pages site update | Flash | $0.004 |
| 21:00 | E-book manuscript writing (this very text!) | Pro | $0.025 |
| 23:00 | Daily work summary and backup | Flash | $0.002 |
| **Total** | | | **$0.09/day** |

---

## 5.5 Most Frequently Asked Questions from Beginners

### Q: Isn't 55 million tokens a day an enormous amount?
A: Think of "tokens" as roughly the number of characters. One English word is about 1.3 tokens.
- One novel (100 pages): roughly 1 million tokens
- One newspaper page: roughly 100,000 tokens
- 55 million tokens = the equivalent of 55 novels

An AI agent processes all of this every day. It's like reading and summarizing 55 books.

### Q: Is it really possible for $4.50?
A: Yes. I actually spent $4.50 over the month of June 2026. You can verify this directly on the DeepSeek API dashboard.

### Q: Isn't the performance noticeably worse than GPT-4o?
A: In some benchmarks, GPT-4o still leads, but in day-to-day work, the difference is nearly imperceptible. Meanwhile, the cost is at 1/400th the level.

### Q: How's the Korean language support?
A: DeepSeek is a Chinese company, so its Korean language processing is surprisingly natural. In some cases, its Korean output is even smoother than GPT-4o's.

---

## 5.6 30-Day Final Verdict

### What We Loved
- **Cost**: Honestly, at this price, it's practically free
- **Speed**: The Flash model is faster than GPT-4o
- **Korean**: Extremely natural
- **Stability**: Not a single outage in 30 days

### Room for Improvement
- **Multimodal**: Image analysis requires a separate Mimo connection
- **Latest Information**: Some recent data falls outside the training scope
- **Long Context**: 128K+ requires the Pro model

### Final Recommendations

| User Type | Recommended Setup | Estimated Monthly Cost |
|:----------:|:---------:|:-----------:|
| Light use (100 requests/day) | Flash only | **$1.50–2.00** |
| Moderate use (500 requests/day) | Flash + Pro (7:3) | **$4.50–6.00** |
| Heavy use (24/7) | Flash + Pro + Mimo | **$8.00–12.00** |
| Team use (3 people) | Above × 3 | **$15.00–25.00** |

---

**This completes all chapters of Guide Book ①.**

If you follow through on everything covered so far, you too can run a 24/7 AI assistant for around $4 a month.

> ⭐ **Pro version purchasers** will additionally receive the AI agent collaboration conversation logs (actual collaboration records between Haena and AG), config.yaml templates, and the auto-sync script provided as appendices.
