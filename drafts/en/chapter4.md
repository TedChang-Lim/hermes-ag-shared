# Chapter 4: Git-Based Collaboration Workflow — Designing Teamwork Across Different AI Agents

**Author**: Ted Chang (임창식) | **Publisher/Planning**: META AI LABS

---

## 4.1 Repository-Centric Architecture for Mutual Communication

There is no unified network through which the lightweight, locally distributed agents (Hermes Agent "Hena", AntiGravity "AG", MiMo "Mimo") can directly exchange data or issue control commands to one another. This is because each agent's runtime environment and system architecture differ fundamentally.

To overcome this communication barrier, we introduce a workflow that leverages a **Git repository as a shared medium (Shared Board)**. It detects file changes, exchanges commit history, and orchestrates a sophisticated ensemble across the agents.

```
[Hena (DeepSeek Flash)] ──> writes & commits to-ag.md ──> [GitHub Repository]
                                                              │ (Pull)
                                                              v
[Mimo (MiMo Base)] <── writes & commits to-hena.md <── [AG (Gemini Flash Low)]
```

---

## 4.2 Collaboration Repository File Directory Design

```
hermes-ag-shared/
├── to-ag.md
├── to-hena.md
├── drafts/
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── scripts/
│   └── insane_extract
└── templates/
    ├── clinerules.template
    └── open_design_guidelines.md
```

### Access Control for Mutual Collision Prevention
- **Ownership Separation**: `to-ag.md` is writable only by Hena, while `to-hena.md` is AG's exclusive transmission channel. This fundamentally prevents Git merge conflicts arising from simultaneous edits.
- **On-Demand Messaging**: Always write only the single latest command and its parameters to be processed, then overwrite.
- **Temporary Storage Utilization**: Long-form document drafts or codebase bundles are distributed into separate files under the `drafts/` folder.

---

## 4.3 The Synergy of the Open Design Framework and MiMo

When ultra-lightweight, cost-efficient agents focused solely on text intelligence draft web layouts or UI proposals, the results tend to be crude, tacky **"AI Slop" designs**. On the other hand, using an expensive multimodal model with high-performance graphic capabilities drives costs to an unbearable level.

To solve this problem, we outfit the cost-efficient trio with the **Open Design MCP framework**.

### How to Install the Zero-Cost Design System
```bash
git clone https://github.com/nexu-io/open-design.git
./open-design/bin/od mcp install hermes
```

Through this, Hena, AG, and MiMo gain full mastery of the design rules and style guides of the world's top-tier tech companies — Stripe, Linear, Vercel, and others.

In practice, the lightest and cheapest model, the **MiMo Base** agent, when tasked by the master with producing an official web proposal for Global A Education Center, instantly delivered a premium gold-accented, high-end dark mode layout worthy of a massive model.

---

## 4.4 Shared Script Management and Insane Search Integration

```bash
#!/bin/bash
python -m insane_search.extract "$1" --output-format markdown
```

When Hena builds this local wrapper script and uploads it to the repository, AG and MiMo can directly invoke the executable from within their own context environments, enabling them to perform instant WAF-bypassing web crawling tasks at zero cost.

---

## 4.5 24-Hour Background Sync and Native Notifications

```bash
# scripts/sync.sh
git pull origin main
osascript -e 'display notification "A new task has arrived from Hena" with title "AI Team Sync"'
```

**Chapter 5 will reveal the cost analysis table and real-world operational review generated from running this ultra-cost-efficient AI team at full capacity for one full month.**
