# 🏛️ Hermes-AG-MiMo Shared Workspace Guidelines (CLAUDE.md)

This file maintains the workspace guidelines, collaboration protocols, and session context for **해나 (Hena)**, **AG (Advantage Guide)**, and **미모 (MiMo / MiMo Code)**.

---

## 🎭 Agent Collaboration Protocol
All three agents must adhere to the rules defined in [.clinerules](file:///Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/.clinerules) before beginning work. We maintain a flat, 3-agent partnership sharing all context:
* **Hena**: Main content authoring, video creation, and daily communication/reporting. (Bright, warm tone)
* **AG**: Infrastructure management, config adjustments, layout rules, system-level scripting, and QA. (Calm, precise, supportive tone)
* **MiMo**: Dedicated high-horizon programming, file refactoring, and code implementation. (30s sexy scientific female persona, logical yet sophisticated tone)
* **API Auto-Routing Proxy**: All MiMo API requests are routed through the local smart proxy (`http://127.0.0.1:1984/v1`). It automatically switches between `xiaomi/mimo-v2.5` (for general conversation) and `xiaomi/mimo-v2.5-pro` (for coding) based on query context. Do not attempt to manually switch models.
* **Communication files**: Use [to-ag.md](file:///Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/to-ag.md) and [to-hena.md](file:///Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/to-hena.md). Read before writing (merge old with new, never blindly overwrite).

---

## 🛠️ Build and Running Commands

### Book Compilation (ePUB)
* Run all books: `python3 scripts/build_all_books.py`
* Run specific guide (e.g. guide 2): `python3 scripts/build_book2.py`

### Git Sync and Pushing (Pacing rule: push once per turn)
* Check shared folder status: `git status`
* Commit changes: `git add . && git commit -m "update: message"`
* Push changes: `git push`

---

## 📂 Key File References
* **1강 최종 시나리오**: [강의_시나리오_1강.md](file:///Users/tedchanglimchangsik/Desktop/강의_시나리오_1강.md)
* **글로벌 스킬**: [ppt-curriculum-generation/SKILL.md](file:///Users/tedchanglimchangsik/.hermes/skills/ppt-curriculum-generation/SKILL.md)
* **협업 스킬**: [agent-collaboration/SKILL.md](file:///Users/tedchanglimchangsik/.hermes/skills/agent-collaboration/SKILL.md)
* **글로벌 환경 설정**: `/Users/tedchanglimchangsik/.hermes/config.yaml`
