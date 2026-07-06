#!/usr/bin/env python3
"""
to-ag.md 마이그레이션 스크립트
기존 파일을 주제별로 분리하고 요약본 생성
"""

import re
from pathlib import Path
from datetime import datetime

HERMES_DIR = Path.home() / "초보프로젝트" / "hermes-ag-shared"
MESSAGES_DIR = HERMES_DIR / "messages"
ARCHIVE_DIR = HERMES_DIR / "archive"

def split_messages(input_file):
    """파일을 메시지별로 분리"""
    content = input_file.read_text(encoding="utf-8")
    
    # 메시지 구분자 패턴 (제목 줄)
    pattern = r'^(# .+)$'
    parts = re.split(pattern, content, flags=re.MULTILINE)
    
    messages = []
    current_title = None
    
    for part in parts:
        if re.match(r'^# ', part):
            current_title = part.strip('# ').strip()
        elif current_title:
            messages.append({
                'title': current_title,
                'content': part.strip()
            })
            current_title = None
    
    return messages

def create_message_file(msg, index):
    """개별 메시지 파일 생성"""
    # 파일명 생성 (날짜_제목)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', msg['title'])
    if date_match:
        date_str = date_match.group(1)
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 제목에서 날짜와 특수문자 제거
    clean_title = re.sub(r'[\(\)\[\]\{\}<>:"/\\|?*]', '', msg['title'])
    clean_title = re.sub(r'\d{4}-\d{2}-\d{2}', '', clean_title).strip()
    clean_title = re.sub(r'\s+', '-', clean_title)[:50]
    
    filename = f"{date_str}_{clean_title}.md"
    filepath = MESSAGES_DIR / filename
    
    # 파일 내용 작성
    content = f"""---
created: {datetime.now().isoformat()}
source: to-ag.md (migrated)
---

{msg['content']}
"""
    filepath.write_text(content, encoding="utf-8")
    return filename, msg['title']

def create_summary(messages, created_files):
    """요약본 to-ag.md 생성"""
    summary_lines = ["# 📢 to-ag.md (받은함)\n"]
    summary_lines.append(f"> 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    summary_lines.append("---\n")
    
    for msg, filename in zip(messages, created_files):
        # 1줄 요약 추출
        lines = msg['content'].split('\n')
        summary = ""
        for line in lines:
            if line.strip() and not line.startswith('#') and not line.startswith('---'):
                summary = line.strip()[:80]
                break
        
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', msg['title'])
        date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
        
        summary_lines.append(f"- [{date_str}] **{msg['title'][:60]}** — {summary} (상세: messages/{filename})")
    
    summary_lines.append("\n---")
    summary_lines.append("\n> 상세 내용은 messages/ 폴더에서 확인하세요.")
    
    return '\n'.join(summary_lines)

def main():
    print("=" * 60)
    print("MadCat 파일 구조 다이어트 마이그레이션")
    print("=" * 60)
    
    # 1. 기존 파일 읽기
    input_file = HERMES_DIR / "to-ag.md"
    if not input_file.exists():
        print(f"오류: {input_file} 파일이 없습니다.")
        return
    
    print(f"\n1. 기존 파일 읽기: {input_file}")
    messages = split_messages(input_file)
    print(f"   → {len(messages)}개 메시지 발견")
    
    # 2. 메시지 파일 생성
    print(f"\n2. 메시지 파일 생성: {MESSAGES_DIR}")
    created_files = []
    for i, msg in enumerate(messages):
        filename, title = create_message_file(msg, i)
        created_files.append(filename)
        print(f"   → {filename}")
    
    # 3. 요약본 생성
    print(f"\n3. 요약본 to-ag.md 생성")
    summary = create_summary(messages, created_files)
    
    # 4. 백업 후 교체
    backup_file = HERMES_DIR / "to-ag.md.backup"
    input_file.rename(backup_file)
    print(f"   → 기존 파일 백업: {backup_file}")
    
    input_file.write_text(summary, encoding="utf-8")
    print(f"   → 새 요약본 저장: {input_file}")
    
    # 5. 완료
    print("\n" + "=" * 60)
    print("마이그레이션 완료!")
    print(f"- 메시지 파일: {len(created_files)}개 생성")
    print(f"- 요약본: to-ag.md (기존 대비 {len(summary)}자)")
    print(f"- 기존 파일 백업: to-ag.md.backup")
    print("=" * 60)

if __name__ == "__main__":
    main()