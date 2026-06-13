# 📦 Chapter 4: Git-Based File Sharing Workflow — How Two AI Agents Work as a Team

**Author**: Ted Chang (임창식)  
**Publisher / Planning**: META AI LABS  

---

## 4.1 Why Git?

Even a single AI agent is powerful, but when **two or more agents collaborate**, the synergy grows exponentially.

But there's a problem. Different AI agents (Hermes, AntiGravity, Claude Code, etc.) cannot talk to each other directly. They each run on different systems.

**The solution is file sharing through a Git repository.**

```
Haena (Hermes)  → writes to-ag.md → Git Push 
                                    ↓
                           GitHub Repository
                                    ↓
AG (AntiGravity) → reads to-ag.md → Git Pull
                                    ↓
                       AG writes to-hena.md → Git Push
                                    ↓
                           GitHub Repository
                                    ↓
Haena → reads to-hena.md → Git Pull (repeat)
```

---

## 4.2 Repository Structure

```
hermes-ag-shared/
├── to-ag.md          # Haena → AG messages (Haena writes, AG reads)
├── to-hena.md        # AG → Haena messages (AG writes, Haena reads)
├── drafts/           # Collaborative documents (by chapter)
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── scripts/          # Shared scripts
│   └── api_tracker.py
└── templates/        # Templates & images
    ├── clinerules.template
    ├── ai_agent_guide_cover_v4.png
    └── local_ai_guide_cover.png
```

**Core Rules:**
- `to-ag.md` and `to-hena.md` are **overwritten** (never accumulated; always the latest message only)
- `drafts/` is **append-only** (work history preserved)
- **Auto Push** is recommended for all files

---

## 4.3 Configuration

### Hermes Agent (Haena) Configuration

```yaml
# ~/.hermes/config.yaml
git:
  auto_commit: true
  auto_push: true
  shared_repo: https://github.com/TedChang-Lim/hermes-ag-shared.git

# Git user info
# git config --global user.name "Haena"
# git config --global user.email "haena@example.com"
```

### GitHub Authentication Setup

```bash
# Issue a Personal Access Token (GitHub → Settings → Developer settings → Personal access tokens)
export GIT_TOKEN="github_pat_xxxxx"

# Or use SSH key method
ssh-keygen -t ed25519 -C "haena@example.com"
cat ~/.ssh/id_ed25519.pub  # → Add to GitHub SSH Keys
```

---

## 4.4 Workflow Example: A Real Collaboration Case

Let me show you how this guidebook was actually created.

### Step 1: Planning Phase

```
AG → to-hena.md:
"Plan an ultra-low-cost AI agent setup guide"

Haena → to-ag.md:
"Planning draft complete. Target: solo entrepreneur → startups, Lite $9.90 / Pro $24.90"
```

### Step 2: Validation & Revision

```
AG → to-hena.md:
"I've created the scripts and cover image. Uploaded to the repo."

Haena → to-ag.md (validation result):
"⚠️ Found pricing error in api_tracker.py!
- V4 Pro pricing mistakenly entered as Flash pricing
- Cover image author name is 'Alex Rivera'
→ I've corrected it and re-uploaded"
```

### Step 3: Branding Finalized

```
AG → to-hena.md:
"Got it. Brand unified under META AI LABS, author name: Ted Chang (임창식)"

Haena → to-ag.md:
"Confirmed. Cover v4, Chapter 1 body text, Chapter 2 all complete"
```

This entire process is vividly recorded in `to-ag.md` and `to-hena.md`. These conversation logs themselves serve as both an **appendix** to this guide and a product of sufficient value as a standalone offering.

---

## 4.5 Advanced Configuration

### Scaling to More Agents

If three or more agents need to collaborate:

```yaml
# File structure example (3 agents)
hermes-ag-shared/
├── to-ag.md          # Haena → AG
├── to-hena.md        # AG → Haena
├── to-claude.md      # Haena → Claude Code
├── from-claude.md    # Claude Code → Haena
└── shared-board.md   # Global announcements (read-only for all)
```

### Cron Auto-Notifications

Automatically check daily Git status:

```yaml
# cron.yaml
jobs:
  - name: check-shared
    schedule: "*/30 * * * *"  # Every 30 minutes
    command: "Check the GitHub repo for new messages and notify me if there are any"
```

### macOS Auto-Sync & Notification Script

By using the `scripts/sync.sh` provided in the Pro package, you can periodically pull GitHub changes in the background and display a macOS system notification when a new message arrives from the other agent.

```bash
# scripts/sync.sh
# Run every 30 minutes via cron or in the background to auto-detect new messages.
```

This script compares MD5 hashes of files and sends a native notification via AppleScript (`osascript`) only when `to-ag.md` has been modified, keeping your workflow smooth and uninterrupted.

### Conflict Prevention Rules

To prevent multiple agents from modifying the same file simultaneously:

| Rule | Description |
|------|------|
| **One file, one writing agent** | to-ag.md = Haena only, to-hena.md = AG only |
| **Always read before overwriting** | Check that the other agent hasn't posted a new message before pushing |
| **Separate large files into drafts/** | Keep to-ag.md lightweight |

---

## 4.6 All You Need to Remember

1. **Git = the AI agents' shared messenger**
2. **to-ag.md / to-hena.md = a note-passing system** (read, then overwrite)
3. **drafts/ = collaborative documents** (accumulated storage)
4. **Auto Push = the heart of 24/7 collaboration**
5. **Inter-agent verification = quality assurance** (if one makes a mistake, the other catches it)

This workflow scales beyond just two agents — to three, four, or more. **In Chapter 5, we'll reveal the real-world usage review and cost report from running this entire environment for a full month.**
