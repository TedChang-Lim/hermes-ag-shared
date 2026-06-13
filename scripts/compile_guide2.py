import os
import re
import subprocess
import html

# Markdown to HTML converter
def md_to_html(text):
    # Convert code blocks: ```bash ... ```
    # Using a placeholder to avoid escaping and modifying code block contents
    code_blocks = []
    def code_placeholder(match):
        code_blocks.append(match.group(2))
        return f"<!--CODEBLOCK_{len(code_blocks)-1}-->"
        
    text = re.sub(r'```(\w*)\n(.*?)\n```', code_placeholder, text, flags=re.DOTALL)
    
    # Escape html characters for safety in normal text
    text = html.escape(text)
    
    # Convert inline code: `code`
    text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
    # Convert strong: **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Convert headers
    text = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    # Convert list items
    text = re.sub(r'^\s*[-*]\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Wrap li groups in ul
    lines = text.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<li>') or stripped.startswith('&lt;li&gt;'):
            # fix escaped li tags if any
            line_content = stripped.replace('&lt;li&gt;', '<li>').replace('&lt;/li&gt;', '</li>')
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(line_content)
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    text = '\n'.join(new_lines)
    
    # Paragraphs and line breaks
    parts = text.split('\n\n')
    for i in range(len(parts)):
        # Skip if it is a list or header block
        if not parts[i].strip().startswith('<ul') and not parts[i].strip().startswith('<h') and not parts[i].strip().startswith('<!--CODEBLOCK'):
            parts[i] = parts[i].strip().replace('\n', '<br>')
            parts[i] = f'<p>{parts[i]}</p>'
    text = '\n'.join(parts)
    
    # Restore code blocks
    for idx, code in enumerate(code_blocks):
        # Convert code contents to clean html pre blocks
        escaped_code = html.escape(code)
        code_html = f'<pre class="code-block"><code>{escaped_code}</code></pre>'
        text = text.replace(f"&lt;!--CODEBLOCK_{idx}--&gt;", code_html)
        text = text.replace(f"<!--CODEBLOCK_{idx}-->", code_html)
        
    return text

def get_git_commits(file_path):
    try:
        # Get commit hash, timestamp, and message for commits touching this file
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
        # Commit might be before file creation
        return None

def determine_phase_and_progress(index, total, subject):
    subj_lower = subject.lower()
    
    # Progress estimation logic
    if "첫 인사" in subj_lower or "초기 설정" in subj_lower:
        return "1단계: 프로젝트 기획", 5
    elif "기획" in subj_lower or "북커버" in subj_lower:
        return "2단계: 디자인 및 브랜딩", 15
    elif "1장" in subj_lower or "2장" in subj_lower or "3장" in subj_lower or "4장" in subj_lower or "5장" in subj_lower:
        if "3번" in subj_lower or "guide3" in subj_lower:
            return "4단계: ③권 맥북 로컬 AI 집필", 65
        else:
            return "3단계: ①권 가이성비 가이드 집필", 40
    elif "6장" in subj_lower or "7장" in subj_lower or "8장" in subj_lower or "9장" in subj_lower:
        return "4단계: ③권 맥북 로컬 AI 집필", 85
    elif "완결" in subj_lower or "앞부속물" in subj_lower:
        return "5단계: 최종 검수 및 빌드", 100
        
    # Fallback based on linear index
    progress = int((index + 1) / total * 100)
    if progress < 15:
        return "1단계: 프로젝트 기획", progress
    elif progress < 30:
        return "2단계: 디자인 및 브랜딩", progress
    elif progress < 60:
        return "3단계: ①권 가이성비 가이드 집필", progress
    elif progress < 90:
        return "4단계: ③권 맥북 로컬 AI 집필", progress
    else:
        return "5단계: 최종 검수 및 빌드", progress

def compile_book():
    print("Compiling dialogues...")
    commits_to_ag = get_git_commits("to-ag.md")
    commits_to_hena = get_git_commits("to-hena.md")
    
    all_commits = commits_to_ag + commits_to_hena
    # Sort chronologically by timestamp
    all_commits.sort(key=lambda x: x['timestamp'])
    
    messages = []
    seen_contents = set()
    
    for idx, c in enumerate(all_commits):
        content = get_file_content_at_commit(c['hash'], c['file'])
        if not content:
            continue
            
        # Clean content (strip empty lines, titles)
        content_lines = content.strip().split('\n')
        if not content_lines:
            continue
            
        # Strip the top title (e.g. '# 해나 → AG 전달사항')
        cleaned_lines = []
        for line in content_lines:
            if line.startswith('# 해나 → AG') or line.startswith('# AG → 해나') or line.startswith('# 🤖 AG → 해나'):
                continue
            cleaned_lines.append(line)
            
        cleaned_content = '\n'.join(cleaned_lines).strip()
        if not cleaned_content:
            continue
            
        # Avoid exact duplicate consecutive content (sometimes commits contain identical messages)
        content_hash = hash(cleaned_content)
        if content_hash in seen_contents:
            continue
        seen_contents.add(content_hash)
        
        # Identify sender
        sender = "해나 (Haena)" if c['file'] == "to-ag.md" else "AG (Advantage Guide)"
        avatar = "haena_avatar.png" if c['file'] == "to-ag.md" else "ag_avatar.png"
        sender_class = "haena" if c['file'] == "to-ag.md" else "ag"
        
        phase, progress = determine_phase_and_progress(idx, len(all_commits), c['subject'])
        
        messages.append({
            'sender': sender,
            'avatar': avatar,
            'class': sender_class,
            'content': md_to_html(cleaned_content),
            'subject': c['subject'],
            'phase': phase,
            'progress': progress,
            'timestamp': c['timestamp']
        })
        
    print(f"Total parsed messages: {len(messages)}")
    
    # Generate HTML content
    html_template = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 에이전트 협업 대화록 (META AI LABS)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --sidebar-bg: #111827;
            --bubble-haena: rgba(245, 158, 11, 0.08);
            --bubble-haena-border: rgba(245, 158, 11, 0.2);
            --bubble-ag: rgba(16, 185, 129, 0.08);
            --bubble-ag-border: rgba(16, 185, 129, 0.2);
            --text-color: #e5e7eb;
            --text-muted: #9ca3af;
            --accent-color: #f59e0b;
            --accent-ag: #10b981;
            --card-bg: rgba(31, 41, 55, 0.4);
            --border-color: rgba(255, 255, 255, 0.08);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* Sidebar styling */
        .sidebar {
            width: 350px;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            padding: 2.5rem 2rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow-y: auto;
        }

        .brand-header {
            margin-bottom: 2rem;
        }

        .brand-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .brand-subtitle {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* Project Status Panel */
        .status-panel {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }

        .status-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .progress-bar-container {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }

        .progress-bar-fill {
            height: 100%;
            width: 0%; /* Will animate or set statically */
            background: linear-gradient(90deg, var(--accent-ag), var(--accent-color));
            border-radius: 4px;
            transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .progress-percentage {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--accent-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .progress-percentage span {
            font-size: 0.8rem;
            color: var(--text-muted);
            font-weight: 400;
        }

        /* Timeline / Phase List */
        .timeline {
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
            margin-top: 1.5rem;
        }

        .timeline-item {
            display: flex;
            gap: 12px;
            position: relative;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: 7px;
            top: 20px;
            bottom: -20px;
            width: 2px;
            background: rgba(255, 255, 255, 0.05);
        }

        .timeline-item:last-child::before {
            display: none;
        }

        .timeline-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #374151;
            border: 3px solid var(--sidebar-bg);
            z-index: 1;
            margin-top: 4px;
            transition: all 0.3s ease;
        }

        .timeline-item.active .timeline-dot {
            background: var(--accent-color);
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
        }
        
        .timeline-item.completed .timeline-dot {
            background: var(--accent-ag);
        }

        .timeline-content {
            flex: 1;
        }

        .timeline-phase {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        .timeline-item.active .timeline-phase {
            color: #fff;
        }

        .timeline-desc {
            font-size: 0.75rem;
            color: #6b7280;
        }

        /* Chat view window */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: radial-gradient(circle at 50% 50%, #0e1626, #0b0f19);
            overflow-y: auto;
            padding: 3rem 2rem;
        }

        .chat-inner {
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
        }

        /* Chat Message bubble styling */
        .msg-wrapper {
            display: flex;
            gap: 1rem;
            width: 100%;
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 0.6s forwards cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .msg-wrapper.haena {
            flex-direction: row;
        }

        .msg-wrapper.ag {
            flex-direction: row-reverse;
        }

        .avatar-container {
            flex-shrink: 0;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid var(--border-color);
            background: #1e293b;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .avatar-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .msg-bubble-container {
            max-width: 75%;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .msg-wrapper.ag .msg-bubble-container {
            align-items: flex-end;
        }

        .msg-header {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .msg-phase-badge {
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 500;
        }

        .haena .msg-phase-badge {
            background: rgba(245, 158, 11, 0.1);
            color: var(--accent-color);
        }

        .ag .msg-phase-badge {
            background: rgba(16, 185, 129, 0.1);
            color: var(--accent-ag);
        }

        .msg-bubble {
            padding: 1.25rem 1.5rem;
            border-radius: 18px;
            font-size: 0.95rem;
            position: relative;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }

        .haena .msg-bubble {
            background: var(--bubble-haena);
            border: 1px solid var(--bubble-haena-border);
            border-top-left-radius: 4px;
            color: #fef08a; /* Warm white/light yellow for readability */
        }

        .ag .msg-bubble {
            background: var(--bubble-ag);
            border: 1px solid var(--bubble-ag-border);
            border-top-right-radius: 4px;
            color: #d1fae5; /* Emerald green tint */
        }

        /* Content Markdown Styling inside bubbles */
        .msg-bubble p {
            margin-bottom: 0.75rem;
        }

        .msg-bubble p:last-child {
            margin-bottom: 0;
        }

        .msg-bubble strong {
            color: #fff;
        }

        .msg-bubble ul, .msg-bubble ol {
            margin-left: 1.25rem;
            margin-bottom: 0.75rem;
        }

        .msg-bubble li {
            margin-bottom: 0.25rem;
        }

        .code-block {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin: 0.75rem 0;
            overflow-x: auto;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .code-block code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.85rem;
            color: #a7f3d0;
        }

        .inline-code {
            font-family: monospace;
            background: rgba(255, 255, 255, 0.08);
            padding: 2px 5px;
            border-radius: 4px;
            font-size: 0.9em;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        /* Responsive */
        @media (max-width: 900px) {
            body {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
                height: auto;
                border-right: none;
                border-bottom: 1px solid var(--border-color);
                padding: 1.5rem;
            }
            .timeline {
                display: none; /* Hide timeline list on mobile to save space */
            }
            .chat-container {
                padding: 1.5rem 1rem;
            }
        }
    </style>
</head>
<body>
    <!-- Sidebar / Left Panel -->
    <div class="sidebar">
        <div>
            <div class="brand-header">
                <div class="brand-title">
                    <span>🤖</span> META AI LABS
                </div>
                <div class="brand-subtitle">AI Agent Collaboration Transcripts</div>
            </div>

            <!-- Project Progress bar -->
            <div class="status-panel">
                <div class="status-title">Current Phase Progress</div>
                <div class="progress-bar-container">
                    <div id="progressFill" class="progress-bar-fill" style="width: 100%;"></div>
                </div>
                <div class="progress-percentage" id="progressText">
                    100% <span>Complete</span>
                </div>
            </div>

            <!-- Phase Timeline -->
            <div class="timeline">
                <div class="timeline-item completed">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-phase">1단계: 프로젝트 기획</div>
                        <div class="timeline-desc">3종 지식 상품 시리즈 컨셉 및 규격 수립</div>
                    </div>
                </div>
                <div class="timeline-item completed">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-phase">2단계: 디자인 및 브랜딩</div>
                        <div class="timeline-desc">북커버 확정 및 저자 브랜딩 방침 확인</div>
                    </div>
                </div>
                <div class="timeline-item completed">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-phase">3단계: ①권 가이성비 가이드 집필</div>
                        <div class="timeline-desc">월 5달러 초가성비 AI 환경 구축 챕터 작성</div>
                    </div>
                </div>
                <div class="timeline-item completed">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-phase">4단계: ③권 맥북 로컬 AI 집필</div>
                        <div class="timeline-desc">LM Studio, Jan.ai, MLX, APEX 양자화 및 연동</div>
                    </div>
                </div>
                <div class="timeline-item active">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-phase">5단계: 최종 검수 및 빌드</div>
                        <div class="timeline-desc">앞부속물 작성 및 Gumroad 업로드용 패키징</div>
                    </div>
                </div>
            </div>
        </div>

        <div style="margin-top: 2rem; font-size: 0.8rem; color: #4b5563; text-align: center;">
            &copy; 2026 META AI LABS. All rights reserved.
        </div>
    </div>

    <!-- Right Chat View -->
    <div class="chat-container">
        <div class="chat-inner">
            <!-- Dynamic Messages Go Here -->
            {messages_placeholder}
        </div>
    </div>

    <script>
        // Smooth scroll and visual effects
        document.addEventListener('DOMContentLoaded', () => {
            console.log('Dialogue Book Compiled & Rendered!');
            
            // Dynamic timeline highlighting as you scroll can be added here
            const chatContainer = document.querySelector('.chat-container');
            const messages = document.querySelectorAll('.msg-wrapper');
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            const timelineItems = document.querySelectorAll('.timeline-item');

            // Set initial state
            progressFill.style.width = '100%';
            
            chatContainer.addEventListener('scroll', () => {
                // Determine which message is in view to update sidebar progress
                let currentMsg = null;
                const containerTop = chatContainer.getBoundingClientRect().top;
                
                messages.forEach(msg => {
                    const rect = msg.getBoundingClientRect();
                    if (rect.top - containerTop < 200) {
                        currentMsg = msg;
                    }
                });

                if (currentMsg) {
                    const prog = currentMsg.getAttribute('data-progress');
                    const phase = currentMsg.getAttribute('data-phase');
                    
                    progressFill.style.width = prog + '%';
                    progressText.innerHTML = prog + '% <span>' + phase + '</span>';
                    
                    // Update timeline active state
                    timelineItems.forEach(item => {
                        const phaseName = item.querySelector('.timeline-phase').innerText;
                        if (phase.includes(phaseName.split(':')[0])) {
                            timelineItems.forEach(i => i.classList.remove('active'));
                            item.classList.add('active');
                        }
                    });
                }
            });
        });
    </script>
</body>
</html>
"""
    
    # Render individual messages
    message_htmls = []
    for m in messages:
        # Construct message wrapper with custom attributes for scroll animation
        msg_str = f"""
            <div class="msg-wrapper {m['class']}" data-progress="{m['progress']}" data-phase="{m['phase']}">
                <div class="avatar-container">
                    <img src="./templates/{m['avatar']}" alt="{m['sender']}">
                </div>
                <div class="msg-bubble-container">
                    <div class="msg-header">
                        {m['sender']}
                        <span class="msg-phase-badge">{m['phase']}</span>
                    </div>
                    <div class="msg-bubble">
                        {m['content']}
                    </div>
                </div>
            </div>"""
        message_htmls.append(msg_str)
        
    compiled_html = html_template.replace("{messages_placeholder}", '\n'.join(message_htmls))
    
    output_path = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/drafts/guide2-dialogue-transcripts.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(compiled_html)
        
    print(f"Book compiled and saved to {output_path}")

if __name__ == '__main__':
    compile_book()
