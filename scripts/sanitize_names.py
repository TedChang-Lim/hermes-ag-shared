#!/usr/bin/env python3
import os
import re

BASE_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/drafts"

replacements = {
    r"한국AI융합교육원\(KACEC\)": "글로벌 A 교육원",
    r"한국AI융합교육원": "글로벌 A 교육원",
    r"KACEC\(한국AI융합교육원\)": "글로벌 A 교육원",
    r"KACEC": "A 교육원",
    r"KACEC_proposal\.html": "education_proposal.html",
    r"대학원 교수님들과의 모임": "글로벌 비즈니스 협의체 오프라인 전략 회의",
    r"대학원 교수들과의 모임": "글로벌 비즈니스 협의체 오프라인 전략 회의",
    r"있어 보이기 때문에": "브랜드 인지도 제고와 일관성을 극대화하기 위해",
    r"있어 보이기": "브랜드 가치 제고"
}

def sanitize_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    modified = False
    for pattern, repl in replacements.items():
        new_content, count = re.subn(pattern, repl, content)
        if count > 0:
            content = new_content
            modified = True
            print(f"   [Sanitized] {pattern} -> {repl} ({count} times) in {os.path.basename(file_path)}")
            
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    print("🧹 Starting global anonymization of sensitive names...")
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                sanitize_file(os.path.join(root, file))
    print("✅ Anonymization complete.")
