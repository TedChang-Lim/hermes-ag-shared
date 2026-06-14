#!/usr/bin/env python3
"""
scripts/build_all_books.py
AI 에이전트 가이드 시리즈 (한글판 3권, 영문판 3권) 통합 ePUB 컴파일러
"""
import subprocess
import os

BASE_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared"

def run_cmd(cmd_list):
    try:
        res = subprocess.run(cmd_list, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✅ Success: {' '.join(cmd_list)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {' '.join(cmd_list)}")
        print(f"   Stderr: {e.stderr}")
        return False

def build_books():
    print("🚀 starting compilation of 6 books (Korean and English versions)...")

    # 1. 한글판 2권 정제 스크립트 사전 실행
    # (이미 clean_for_pandoc.py를 거쳐 drafts/guide2-clean.md가 잘 생성되지만, 스크립트 상에서 강제로 최신 갱신을 실행해줍니다.)
    clean_script = os.path.join(BASE_DIR, "scripts/clean_for_pandoc.py")
    print("\n[Step 1] Running cleanup script for Guide 2 (Korean)...")
    if not run_cmd(["python3", clean_script]):
        print("Stopping compilation due to pre-cleaning failure.")
        return

    # 2. 책별 컴파일 세부 정보 설정
    books_config = [
        # --- 한글판 패키지 ---
        {
            "name": "Guide ① (Korean) - 초가성비 AI 에이전트 구축 가이드",
            "inputs": [
                "drafts/guide1-front-matter.md",
                "drafts/chapter1.md",
                "drafts/chapter2.md",
                "drafts/chapter3.md",
                "drafts/chapter4.md",
                "drafts/chapter5.md"
            ],
            "output": "drafts/guide1-book.epub",
            "cover": "templates/ai_agent_guide_cover_v4.png",
            "title": "초가성비 AI 에이전트 구축 가이드",
            "author": "Ted Chang (임창식)",
            "publisher": "META AI LABS"
        },
        {
            "name": "Guide ② (Korean) - AI 에이전트 협업 대화록",
            "inputs": [
                "drafts/guide2-clean.md"
            ],
            "output": "drafts/guide2-book.epub",
            "cover": "templates/guide2_cover.png",
            "title": "AI 에이전트 협업 대화록",
            "author": "Ted Chang (임창식)",
            "publisher": "META AI LABS"
        },
        {
            "name": "Guide ③ (Korean) - 맥북 로컬 AI 완전 정복 가이드",
            "inputs": [
                "drafts/guide3-front-matter.md",
                "drafts/guide3-toc.md",
                "drafts/guide3-chapter1.md",
                "drafts/guide3-chapter2.md",
                "drafts/guide3-chapter3.md",
                "drafts/guide3-chapter4.md",
                "drafts/guide3-chapter5.md",
                "drafts/guide3-chapter6.md",
                "drafts/guide3-chapter7.md",
                "drafts/guide3-chapter8.md",
                "drafts/guide3-chapter9.md"
            ],
            "output": "drafts/guide3-book.epub",
            "cover": "templates/local_ai_guide_cover.png",
            "title": "맥북 로컬 AI 완전 정복 가이드",
            "author": "Ted Chang (임창식)",
            "publisher": "META AI LABS"
        },
        
        # --- 영문판 패키지 (drafts/en/) ---
        {
            "name": "Guide ① (English) - Ultra-Low-Cost AI Agent Setup Guide",
            "inputs": [
                "drafts/en/guide1-front-matter.md",
                "drafts/en/chapter1.md",
                "drafts/en/chapter2.md",
                "drafts/en/chapter3.md",
                "drafts/en/chapter4.md",
                "drafts/en/chapter5.md"
            ],
            "output": "drafts/en/guide1-book-en.epub",
            "cover": "templates/guide1_cover_en.png",
            "title": "Ultra-Low-Cost AI Agent Setup Guide",
            "author": "Ted Chang (임창식)",
            "publisher": "META AI LABS"
        },
        {
            "name": "Guide ② (English) - AI Agent Collaboration Transcripts",
            "inputs": [
                "drafts/en/guide2-front-matter.md",
                "drafts/en/guide2-collaboration-transcripts.md"
            ],
            "output": "drafts/en/guide2-book-en.epub",
            "cover": "templates/guide2_cover_en.png",
            "title": "AI Agent Collaboration Transcripts",
            "author": "Ted Chang (임창식)",
            "publisher": "META AI LABS"
        },
        {
            "name": "Guide ③ (English) - MacBook Local AI Mastery Guide",
            "inputs": [
                "drafts/en/guide3-front-matter.md",
                "drafts/en/guide3-toc.md",
                "drafts/en/guide3-chapter1.md",
                "drafts/en/guide3-chapter2.md",
                "drafts/en/guide3-chapter3.md",
                "drafts/en/guide3-chapter4.md",
                "drafts/en/guide3-chapter5.md",
                "drafts/en/guide3-chapter6.md",
                "drafts/en/guide3-chapter7.md",
                "drafts/en/guide3-chapter8.md",
                "drafts/en/guide3-chapter9.md"
            ],
            "output": "drafts/en/guide3-book-en.epub",
            "cover": "templates/guide3_cover_en.png",
            "title": "MacBook Local AI Mastery Guide",
            "author": "Ted Chang (임창식)",
            "publisher": "META AI LABS"
        }
    ]

    print("\n[Step 2] Compiling ePUBs using Pandoc...")
    success_count = 0
    
    for book in books_config:
        print(f"\n--- Compiling: {book['name']} ---")
        
        # 입력 파일 경로 조합
        input_paths = [os.path.join(BASE_DIR, path) for path in book["inputs"]]
        
        # 파일 존재성 선제 확인
        missing_file = False
        for path in input_paths:
            if not os.path.exists(path):
                print(f"❌ Missing file: {path}")
                missing_file = True
        
        if missing_file:
            print("Skipping this book compilation.")
            continue
            
        output_path = os.path.join(BASE_DIR, book["output"])
        cover_path = os.path.join(BASE_DIR, book["cover"])
        css_path = os.path.join(BASE_DIR, "templates/epub_style.css")
        
        # pandoc 명령어 구성
        cmd = [
            "pandoc"
        ] + input_paths + [
            "-o", output_path,
            "--epub-cover-image=" + cover_path,
            "--css=" + css_path,
            "--metadata", "title=" + book["title"],
            "--metadata", "author=" + book["author"],
            "--metadata", "publisher=" + book["publisher"]
        ]
        
        if run_cmd(cmd):
            success_count += 1
            # 용량 출력
            file_size = os.path.getsize(output_path)
            print(f"   Saved to: {book['output']} ({file_size / 1024:.1f} KB)")
            
    print(f"\n🎉 Compilation Completed: {success_count} / {len(books_config)} books compiled successfully.")

if __name__ == "__main__":
    build_books()
