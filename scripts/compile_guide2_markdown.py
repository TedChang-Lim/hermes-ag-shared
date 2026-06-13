import os
import re
import subprocess

def get_git_commits(file_path):
    try:
        output = subprocess.check_output(
            ["git", "log", "--reverse", "--format=%H|%at|%s", "--", file_path],
            encoding="utf-8"
        )
        commits = []
        for line in output.strip().split('\n'):
            if line:
                h, t, s = line.split('|', 2)
                commits.append({'hash': h, 'timestamp': int(t), 'subject': s, 'file': file_path})
        return commits
    except Exception as e:
        print(f"Error reading git log for {file_path}: {e}")
        return []

def get_file_content_at_commit(commit_hash, file_path):
    try:
        content = subprocess.check_output(
            ["git", "show", f"{commit_hash}:{file_path}"],
            encoding="utf-8",
            errors="ignore"
        )
        return content
    except Exception as e:
        return None

def determine_phase_and_progress(index, total, subject):
    subj_lower = subject.lower()
    
    if "첫 인사" in subj_lower or "초기 설정" in subj_lower:
        return "1장: 프로젝트 기획 및 브랜드 디자인 확정", 5
    elif "기획" in subj_lower or "북커버" in subj_lower:
        return "1장: 프로젝트 기획 및 브랜드 디자인 확정", 15
    elif "1장" in subj_lower or "2장" in subj_lower or "3장" in subj_lower or "4장" in subj_lower or "5장" in subj_lower:
        if "3번" in subj_lower or "guide3" in subj_lower:
            return "3장: ③권 '맥북 로컬 AI 가이드' 집필 및 대화록 완결", 70
        else:
            return "2장: ①권 '초가성비 AI 에이전트 가이드' 집필", 40
    elif "6장" in subj_lower or "7장" in subj_lower or "8장" in subj_lower or "9장" in subj_lower:
        return "3장: ③권 '맥북 로컬 AI 가이드' 집필 및 대화록 완결", 90
    elif "완결" in subj_lower or "앞부속물" in subj_lower:
        return "3장: ③권 '맥북 로컬 AI 가이드' 집필 및 대화록 완결", 100
        
    progress = int((index + 1) / total * 100)
    if progress < 20:
        return "1장: 프로젝트 기획 및 브랜드 디자인 확정", progress
    elif progress < 60:
        return "2장: ①권 '초가성비 AI 에이전트 가이드' 집필", progress
    else:
        return "3장: ③권 '맥북 로컬 AI 가이드' 집필 및 대화록 완결", progress

def make_progress_bar(percentage):
    filled = int(percentage / 10)
    empty = 10 - filled
    return "█" * filled + "░" * empty

def compile_markdown_book():
    print("Compiling dialogues into Markdown book...")
    
    # 1. Load Front Matter (Guide 2 Front Matter)
    front_matter_path = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/drafts/guide2-front-matter.md"
    front_matter = ""
    if os.path.exists(front_matter_path):
        with open(front_matter_path, 'r', encoding='utf-8') as f:
            front_matter = f.read().strip() + "\n\n---\n\n"
            
    commits_to_ag = get_git_commits("to-ag.md")
    commits_to_hena = get_git_commits("to-hena.md")
    
    all_commits = commits_to_ag + commits_to_hena
    all_commits.sort(key=lambda x: x['timestamp'])
    
    markdown_chapters = {
        "1장: 프로젝트 기획 및 브랜드 디자인 확정": [],
        "2장: ①권 '초가성비 AI 에이전트 가이드' 집필": [],
        "3장: ③권 '맥북 로컬 AI 가이드' 집필 및 대화록 완결": []
    }
    
    seen_contents = set()
    total_commits = len(all_commits)
    
    for idx, c in enumerate(all_commits):
        content = get_file_content_at_commit(c['hash'], c['file'])
        if not content:
            continue
            
        content_lines = content.strip().split('\n')
        if not content_lines:
            continue
            
        # Strip top headers (supporting both historical '헤나' and corrected '해나')
        cleaned_lines = []
        for line in content_lines:
            line_strip = line.strip()
            if (line_strip.startswith('# 해나 → AG') or line_strip.startswith('# AG → 해나') or line_strip.startswith('# 🤖 AG → 해나') or
                line_strip.startswith('# 헤나 → AG') or line_strip.startswith('# AG → 헤나') or line_strip.startswith('# 🤖 AG → 헤나')):
                continue
            cleaned_lines.append(line)
            
        cleaned_content = '\n'.join(cleaned_lines).strip()
        if not cleaned_content:
            continue
            
        # Clean up historical spelling mistakes in the dialogue text
        cleaned_content = cleaned_content.replace("to-hena.md", "___TO_HENA_MD___")
        cleaned_content = cleaned_content.replace("to-hena", "___TO_HENA___")
        cleaned_content = cleaned_content.replace("헤나", "해나")
        cleaned_content = cleaned_content.replace("Hena", "Haena")
        cleaned_content = cleaned_content.replace("___TO_HENA_MD___", "to-hena.md")
        cleaned_content = cleaned_content.replace("___TO_HENA___", "to-hena")
            
        content_hash = hash(cleaned_content)
        if content_hash in seen_contents:
            continue
        seen_contents.add(content_hash)
        
        sender = "해나 (Haena)" if c['file'] == "to-ag.md" else "AG (Advantage Guide)"
        avatar_path = "../templates/haena_avatar.png" if c['file'] == "to-ag.md" else "../templates/ag_avatar.png"
        
        subj = c['subject']
        subj = subj.replace("to-hena.md", "___TO_HENA_MD___")
        subj = subj.replace("to-hena", "___TO_HENA___")
        subj = subj.replace("헤나", "해나")
        subj = subj.replace("Hena", "Haena")
        subj = subj.replace("___TO_HENA_MD___", "to-hena.md")
        subj = subj.replace("___TO_HENA___", "to-hena")

        phase, progress = determine_phase_and_progress(idx, total_commits, subj)
        
        # Determine target chapter key based on phase
        chapter_key = "1장: 프로젝트 기획 및 브랜드 디자인 확정"
        if "2장" in phase:
            chapter_key = "2장: ①권 '초가성비 AI 에이전트 가이드' 집필"
        elif "3장" in phase or "4장" in phase or "5장" in phase:
            chapter_key = "3장: ③권 '맥북 로컬 AI 가이드' 집필 및 대화록 완결"
            
        progress_bar = make_progress_bar(progress)
        
        message_block = f"""
> **📊 진척도 상황판**
> * **작업 진행 단계**: {phase}
> * **세부 작업 내역**: {subj}
> * **진행률**: `[{progress_bar}] {progress}%`

![{sender}]({avatar_path}) **{sender}**
{cleaned_content}

---
"""
        markdown_chapters[chapter_key].append(message_block)

    # Compile the final document
    final_md = []
    final_md.append(front_matter)
    final_md.append("# 📦 ②권: AI 에이전트 협업 대화록 본문\n\n")
    
    for ch_title, ch_messages in markdown_chapters.items():
        if ch_messages:
            final_md.append(f"## {ch_title}\n\n")
            final_md.append('\n'.join(ch_messages))
            final_md.append("\n\n")
            
    output_path = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/drafts/guide2-collaboration-transcripts.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(final_md))
        
    print(f"Markdown book successfully compiled and saved to {output_path}")

if __name__ == '__main__':
    compile_markdown_book()
