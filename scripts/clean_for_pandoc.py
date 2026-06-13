#!/usr/bin/env python3
"""
Clean the markdown for pandoc conversion.
Removes: progress dashboards, image references, special formatting.
Keeps: clean dialogue with speaker labels.
"""
import re

MD_PATH = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/drafts/guide2-collaboration-transcripts.md"
OUT_MD = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/drafts/guide2-clean.md"

with open(MD_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Remove YAML front matter
text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

# Remove progress dashboard blocks
text = re.sub(r'> \*\*📊.*?\n(> \* .*?\n)*', '', text)
text = re.sub(r'> \* \*\*.*?\n', '', text)

# Replace avatar/image references with simple speaker labels
text = re.sub(r'!\[해나.*?\]\(.*?\).*?\*\*해나.*?\*\*', '#### 🤖 해나 (Haena)', text)
text = re.sub(r'!\[AG.*?\]\(.*?\).*?\*\*AG.*?\*\*', '#### 🧠 AG (Advantage Guide)', text)

# Remove markdown image references
text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

# Clean up excessive blank lines
text = re.sub(r'\n{4,}', '\n\n\n', text)

# Replace 한자
text = text.replace("痛点", "고민")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(text)

print(f"✅ Clean markdown: {OUT_MD}")
print(f"   Size: {len(text)} chars")
