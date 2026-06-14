import os
import shutil

src_dir = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/templates"
dst_dir = "/Users/tedchanglimchangsik/초보프로젝트/tedchang-work/images"

# Create destination folder
os.makedirs(dst_dir, exist_ok=True)
print(f"Created directory: {dst_dir}")

# List of covers to copy
covers = [
    "ai_agent_guide_cover_ko.png",
    "guide2_cover.png",
    "local_ai_guide_cover_ko.png",
    "guide1_cover_en.png",
    "guide2_cover_en.png",
    "guide3_cover_en.png"
]

for cover in covers:
    src_path = os.path.join(src_dir, cover)
    dst_path = os.path.join(dst_dir, cover)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"✅ Copied {cover} to tedchang-work/images/")
    else:
        print(f"❌ Source not found: {src_path}")
