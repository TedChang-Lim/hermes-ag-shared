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

# Replace avatar/image references with temporary placeholders
text = re.sub(r'!\[해나.*?\]\(.*?\).*?\*\*해나.*?\*\*', '__HAENA_AVATAR__', text)
text = re.sub(r'!\[AG.*?\]\(.*?\).*?\*\*AG.*?\*\*', '__AG_AVATAR__', text)

# Remove all other markdown image references
text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

# Restore avatars with Pandoc class and size attributes
text = text.replace('__HAENA_AVATAR__', '#### ![](templates/haena_avatar.png){.avatar width=36px} 해나 (Haena)')
text = text.replace('__AG_AVATAR__', '#### ![](templates/ag_avatar.png){.avatar width=36px} AG (Advantage Guide)')

# Clean up excessive blank lines
text = re.sub(r'\n{4,}', '\n\n\n', text)

# Replace 한자
text = text.replace("痛点", "고민")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(text)

print(f"✅ Clean markdown: {OUT_MD}")
print(f"   Size: {len(text)} chars")
