#!/usr/bin/env python3
"""
②권: AI 에이전트 협업 대화록 — Beautiful HTML 생성 (한글판 & 영문판 지원)
"""
import re, os, base64

BASE_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared"
HAENA_AVATAR = os.path.join(BASE_DIR, "templates/haena_avatar.png")
AG_AVATAR = os.path.join(BASE_DIR, "templates/ag_avatar.png")

def img_to_b64(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"

HAENA_B64 = img_to_b64(HAENA_AVATAR)
AG_B64 = img_to_b64(AG_AVATAR)

def parse_conversations(md_text):
    lines = md_text.split("\n")
    conversations = []
    current_speaker = None
    current_lines = []
    
    for line in lines:
        haena_match = re.search(r'haena_avatar\.png.*?(?:Haena|해나)', line, re.IGNORECASE) or re.search(r'!\[해나.*?\]', line)
        ag_match = re.search(r'ag_avatar\.png.*?(?:AG)', line, re.IGNORECASE) or re.search(r'!\[AG.*?\]', line)
        
        if haena_match or ag_match:
            if current_speaker and current_lines:
                content = "\n".join(current_lines).strip()
                if content:
                    conversations.append((current_speaker, content))
            current_speaker = "haena" if haena_match else "ag"
            current_lines = []
            continue
        
        if current_speaker:
            if line.strip().startswith("> **📊") or line.strip().startswith("> * **"):
                continue
            current_lines.append(line)
    
    if current_speaker and current_lines:
        content = "\n".join(current_lines).strip()
        if content:
            conversations.append((current_speaker, content))
            
    return conversations

def clean_hanja(text):
    replacements = {
        "痛点": "고민",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def format_message(text):
    text = clean_hanja(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    text = re.sub(r'^###+\s+', '', text, flags=re.MULTILINE)
    
    def table_replacer(m):
        rows = m.group(0).strip().split("\n")
        html = '<table class="data-table"><tbody>'
        for row in rows:
            if row.strip().startswith("|"):
                cells = [c.strip() for c in row.split("|")[1:-1]]
                if all(c.replace('-','').strip() == '' for c in cells):
                    continue
                html += "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
        return html + "</tbody></table>"
    
    text = re.sub(r'(\|[^\n]+\|\n?)+', table_replacer, text)
    text = text.replace("---", "<hr>")
    
    paragraphs = []
    for p in text.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        if p.startswith("<table") or p.startswith("<hr"):
            paragraphs.append(p)
        else:
            escaped = p.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            escaped = escaped.replace("&lt;strong&gt;", "<strong>").replace("&lt;/strong&gt;", "</strong>")
            escaped = escaped.replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")
            escaped = escaped.replace("&lt;code&gt;", "<code>").replace("&lt;/code&gt;", "</code>")
            escaped = escaped.replace("&lt;hr&gt;", "<hr>")
            escaped = escaped.replace("&lt;table", "<table").replace("&lt;/table&gt;", "</table>")
            escaped = escaped.replace("&lt;tbody&gt;", "<tbody>").replace("&lt;/tbody&gt;", "</tbody>")
            escaped = escaped.replace("&lt;tr&gt;", "<tr>").replace("&lt;/tr&gt;", "</tr>")
            escaped = escaped.replace("&lt;td&gt;", "<td>").replace("&lt;/td&gt;", "</td>")
            paragraphs.append(f"<p>{escaped}</p>")
    
    return "\n".join(paragraphs)

# Quotes for page-fillers (bilingual support)
QUOTES_KO = [
    ("우리는 아주 짧은 거리만을 볼 수 있을 뿐이다. 하지만 그 안에서 우리가 해야 할 일은 무궁무진하다.", "앨런 튜링 (Alan Turing)"),
    ("이 기계는 수학적 양뿐만 아니라 상상력과 논리의 언어로 구성된 모든 대상에 반응할 수 있을 것이다.", "에이다 러브레이스 (Ada Lovelace)"),
    ("컴퓨터 과학의 연구 대상은 컴퓨터가 아니다. 그것은 마치 천문학이 망원경을 연구하는 학문이 아닌 것과 같다.", "에츠허르 데이크스트라 (Edsger W. Dijkstra)"),
    ("컴퓨터는 우리의 정신을 위한 자전거와 같다.", "스티브 잡스 (Steve Jobs)"),
    ("가장 저렴한 도구들로 가장 웅장한 아키텍처를 세우는 것, 그것이 인공지능 시대의 지적인 공생이다.", "META AI LABS")
]

QUOTES_EN = [
    ("We can only see a short distance ahead, but we can see plenty there that needs to be done.", "Alan Turing"),
    ("The Analytical Engine weaves algebraic patterns just as the Jacquard loom weaves flowers and leaves.", "Ada Lovelace"),
    ("Computer science is no more about computers than astronomy is about telescopes.", "Edsger W. Dijkstra"),
    ("What a computer is to me is the most remarkable tool that we have ever come up with. It's the equivalent of a bicycle for our minds.", "Steve Jobs"),
    ("Building the most magnificent architecture with the cheapest tools — that is the intellectual symbiosis of the AI era.", "META AI LABS")
]

def make_quote_card(index, lang):
    quotes = QUOTES_KO if lang == "ko" else QUOTES_EN
    text, author = quotes[index % len(quotes)]
    return f'''
    <div class="quote-card">
        <div class="quote-divider">✦</div>
        <div class="quote-text">“ {text} ”</div>
        <div class="quote-author">— {author}</div>
        <div class="quote-divider">✦</div>
    </div>'''

def extract_editorial_note(chapter_md, lang):
    match = re.search(r'((?:>.*?\n)+)', chapter_md)
    if match:
        lines = match.group(1).split("\n")
        filtered_lines = []
        for line in lines:
            line_strip = line.strip()
            if line_strip.startswith("> **📊") or line_strip.startswith("> * **") or "진척도" in line_strip or "Progress" in line_strip:
                continue
            content = line_strip.lstrip(">").strip()
            content = content.replace("[!NOTE]", "").replace("✍️ 에디토리얼 브리핑 (Editorial Briefing)", "").replace("Editorial Briefing", "").strip()
            if content:
                filtered_lines.append(content)
        
        note_content = "\n".join(filtered_lines).strip()
        note_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', note_content)
        note_content = note_content.replace("\n", "<br>")
        if note_content:
            tag = "✍️ EDITORIAL BRIEFING"
            return f'''
            <div class="editorial-briefing">
                <div class="briefing-tag">{tag}</div>
                <div class="briefing-text">{note_content}</div>
            </div>'''
    return ""

def build_chapter_html(num, title, md_content, quote_idx, lang):
    convs = parse_conversations(md_content)
    bubbles = []
    for speaker, text in convs:
        is_haena = speaker == "haena"
        name = "Haena" if is_haena else "AG"
        if lang == "ko" and is_haena:
            name = "해나"
        avatar = HAENA_B64 if is_haena else AG_B64
        formatted = format_message(text)
        side_class = "left" if is_haena else "right"
        bubble = f'''
        <div class="msg-row {side_class}">
            <div class="avatar"><img src="{avatar}" alt="{name}"></div>
            <div class="bubble-wrapper">
                <div class="msg-name">{name}</div>
                <div class="msg-bubble {'haena' if is_haena else 'ag'}">
                    {formatted}
                </div>
            </div>
        </div>'''
        bubbles.append(bubble)
        
    chat_html = "\n".join(bubbles)
    briefing_html = extract_editorial_note(md_content, lang)
    quote_html = make_quote_card(quote_idx, lang)
    
    return f'''
    <!-- CHAPTER {num} -->
    <div class="chapter">
        <div class="chapter-num">{num}</div>
        <div class="chapter-title">{title}</div>
    </div>
    {briefing_html}
    <div class="chat-area">
        {chat_html}
    </div>
    {quote_html}
    '''

STYLE_TEMPLATE = """<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__DOC_TITLE__</title>
<style>
@page { size: A5; margin: 12mm; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Apple SD Gothic Neo', 'Noto Serif KR', 'Georgia', sans-serif;
    background: #f7f4ed;
    color: #2b2b2b;
    line-height: 1.8;
    font-size: 10pt;
    padding: 30px;
    word-break: keep-all;
    overflow-wrap: break-word;
}

body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1000;
    background-image: 
        radial-gradient(circle at 15% 15%, rgba(217, 217, 217, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(240, 240, 240, 0.25) 0%, transparent 40%),
        url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.1  0 0 0 0 0.1  0 0 0 0 0.1  0 0 0 0.04 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
    background-size: auto, auto, 180px 180px;
    mix-blend-mode: multiply;
    opacity: 0.65;
}

/* ── Cover ── */
.cover {
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    height: 90vh; text-align: center; background: #f2ede0;
    border: 1px solid #dcd5c5; margin: 10px; border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding: 40px; position: relative;
    page-break-after: always;
}
.cover::after {
    content: ""; position: absolute; inset: 15px; border: 1px dashed #b0a48a; pointer-events: none;
}
.cover-brand { font-size: 8pt; font-weight: 700; letter-spacing: 4px; color: #7f6d4d; margin-bottom: 20px; }
.cover-title { font-size: 26pt; font-weight: 800; line-height: 1.3; color: #2b2b2b; font-family: 'Noto Serif KR', serif; margin: 30px 0; }
.cover-subtitle { font-size: 10.5pt; color: #555; max-width: 80%; line-height: 1.6; }
.cover-divider { width: 40px; height: 2px; background: #b0a48a; margin: 30px 0; }
.cover-author { font-size: 10pt; font-weight: 600; color: #333; margin-bottom: 5px; }
.cover-date { font-size: 8pt; color: #888; }

/* ── Prologue ── */
.prologue {
    page-break-before: always; page-break-after: always; padding: 40px 15px;
}
.prologue h1 { font-size: 18pt; font-family: 'Noto Serif KR', serif; text-align: center; margin-bottom: 30px; color: #2b2b2b; }
.prologue p { margin-bottom: 15px; text-indent: 6px; text-align: justify; }
.prologue .hook { background: #f2ede0; border-left: 3px solid #7f6d4d; padding: 15px; margin: 25px 0; border-radius: 4px; }
.prologue .hook p { margin-bottom: 10px; text-indent: 0; font-size: 9.5pt; }
.prologue .hook p:last-child { margin-bottom: 0; }
.prologue .sign { margin-top: 40px; text-align: right; font-family: 'Noto Serif KR', serif; font-size: 10pt; }

/* ── Chapter Title Page ── */
.chapter {
    page-break-before: always; page-break-after: always;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    height: 80vh; text-align: center;
}
.chapter-num { font-size: 32pt; font-weight: 300; font-family: 'Georgia', serif; color: #7f6d4d; margin-bottom: 15px; }
.chapter-title { font-size: 18pt; font-weight: 700; line-height: 1.4; color: #2b2b2b; font-family: 'Noto Serif KR', serif; }

/* ── Editorial Briefing ── */
.editorial-briefing {
    background: #ffffff;
    border: 1px solid #dcd5c5;
    border-left: 4px solid #7f6d4d;
    padding: 16px 20px;
    margin: 20px 12px;
    border-radius: 6px;
    box-shadow: inset 0 0 4px rgba(0,0,0,0.01);
}
.briefing-tag {
    font-size: 8.5pt; font-weight: 700; color: #7f6d4d; margin-bottom: 8px; letter-spacing: 1px;
}
.briefing-text {
    font-size: 9.5pt; color: #555; line-height: 1.7;
}

/* ── Quote Card Page Filler ── */
.quote-card {
    page-break-before: always;
    page-break-after: always;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    height: 65vh; text-align: center; padding: 40px;
    background: #fdfcf7; border: 1px solid #e8e3d5;
    margin: 40px 12px; border-radius: 8px;
    box-shadow: inset 0 0 6px rgba(0,0,0,0.01);
}
.quote-text {
    font-family: 'Noto Serif KR', 'Georgia', serif;
    font-size: 11pt; font-style: italic; color: #4e3621;
    line-height: 1.8; margin: 25px 0;
    max-width: 85%;
}
.quote-author {
    font-family: 'Apple SD Gothic Neo', sans-serif;
    font-size: 9pt; color: #8a7f69; text-transform: uppercase; letter-spacing: 2px;
}
.quote-divider {
    font-size: 12pt; color: #b0a48a;
}

/* ── Chat Layout ── */
.chat-area { margin: 20px 0; }
.msg-row { display: flex; margin-bottom: 25px; width: 100%; }
.msg-row.left { justify-content: flex-start; }
.msg-row.right { justify-content: flex-end; }

.avatar { width: 36px; height: 36px; margin-right: 12px; flex-shrink: 0; }
.avatar img { width: 100%; height: 100%; border-radius: 50%; border: 1px solid #dcd5c5; object-fit: cover; }

.bubble-wrapper { max-width: 82%; }
.msg-row.right .bubble-wrapper { text-align: left; }

.msg-name { font-size: 8pt; color: #888; margin-bottom: 4px; font-weight: 600; padding-left: 4px; }
.msg-bubble {
    padding: 12px 16px; border-radius: 12px; font-size: 9.5pt; text-align: justify;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02); line-height: 1.7;
}

/* Haena Bubble: Beige Soft Card */
.msg-bubble.haena {
    background: #ffffff; border: 1px solid #dcd5c5;
    border-top-left-radius: 2px; color: #333;
}

/* AG Bubble: Soft Golden Parchment Card */
.msg-bubble.ag {
    background: #f2ede0; border: 1px solid #cfc7b5;
    border-top-left-radius: 2px; color: #2b2b2b;
}

.msg-bubble p { margin-bottom: 10px; text-indent: 0; }
.msg-bubble p:last-child { margin-bottom: 0; }
.msg-bubble code { background: rgba(0,0,0,0.05); padding: 1px 4px; border-radius: 3px; font-size: 8pt; font-family: monospace; color: #c7254e; }
.msg-bubble pre { background: #fdfcf7; border: 1px solid #dcd5c5; padding: 10px; border-radius: 5px; overflow-x: auto; margin: 10px 0; }
.msg-bubble pre code { background: none; padding: 0; color: #333; font-size: 8pt; }
.msg-bubble strong { font-weight: 700; color: #000; }
.msg-bubble em { font-style: italic; }

.msg-bubble table.data-table {
    width: 100%; border-collapse: collapse; font-size: 8pt; margin: 8px 0; background: #fff;
}
.msg-bubble table.data-table td {
    border: 1px solid #dcd5c5; padding: 5px 8px; text-align: left; color: #444;
}

/* ── Afterword ── */
.afterword {
    page-break-before: always;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    height: 50vh; text-align: center; color: #6e6552;
}
.afterword h2 { color: #2b2b2b; margin-bottom: 20px; font-size: 16pt; font-family: 'Noto Serif KR', serif; }
.afterword p { font-size: 10pt; line-height: 2; color: #555; margin-bottom: 10px; }

@media print {
    body { background: #f7f4ed !important; color: #2b2b2b !important; -webkit-print-color-adjust: exact; }
    .cover { background: #f2ede0 !important; color: #2b2b2b !important; -webkit-print-color-adjust: exact; }
    .msg-bubble { -webkit-print-color-adjust: exact; }
    .avatar { -webkit-print-color-adjust: exact; }
    .prologue .hook { -webkit-print-color-adjust: exact; }
}
</style>
</head>
<body>

__BODY_CONTENT__

</body>
</html>"""

def compile_transcripts(lang):
    if lang == "ko":
        md_path = os.path.join(BASE_DIR, "drafts/guide2-collaboration-transcripts.md")
        out_path = os.path.join(BASE_DIR, "drafts/guide2-book.html")
        doc_title = "가장 저렴한 뇌들의 반란"
        cover_title = "가장 저렴한<br>뇌들의 반란"
        cover_sub = "🤖 0원으로 구축하는 무적의 AI 에이전트 협업록"
        cover_date = "2026년 6월 · 개정 보강판 발행"
        author_name = "Ted Chang (임창식)"
        chapter_regex = r'^## ([1-5]장:.*?)$'
        chapter_parse_regex = r'^([1-5])장:\s*(.*)$'
        prologue_title = "프롤로그"
        prologue_hook = """<div class="hook">
            <p>🤖 <strong>해나 (Haena)</strong> — Nous Research의 Hermes Agent 기반.<br>
            밝고 명랑하며 창의적인 기획력과 속도감 있는 집필력.</p>
            <p>🧠 <strong>AG (Advantage Guide)</strong> — AntiGravity 프레임워크 기반.<br>
            과묵하지만 기술적 정합성을 검증하고 오류를 바로잡는 가이드.</p>
        </div>"""
        prologue_body = """<p>이 책의 <strong>모든 문장은 AI가 썼습니다.</strong></p>
        <p>인간이 직접 쓴 문장은 단 한 줄도 없습니다. 편집도, 퇴고도, 교정도 없습니다.</p>
        <p>당신이 지금부터 읽게 될 것은, 서로 다른 성격을 가진 두 AI 에이전트가 30일 동안 GitHub 저장소에서 주고받은 <strong>실제 대화의 생생한 기록</strong>입니다.</p>
        <p>이 두 에이전트는 각자의 방식으로 협력하고, 때로는 충돌하며, 결국엔 하나의 완성된 결과물을 만들어냅니다.</p>
        <p>이 대화록은 그 과정의 전부입니다. 가식도, 각본도 없습니다.</p>
        <p>인간과 기계, 그리고 기계와 기계의 경이로운 협동 실황을 즐겁게 감상해 주시기 바랍니다.</p>"""
        epilogue_title = "에필로그"
        epilogue_body = """<p>이 대화록은 2026년 5월부터 6월까지,<br>
        해나와 AG가 GitHub 저장소에서 주고받은<br>
        실제 메시지를 그대로 옮긴 것입니다.</p>
        <p style="margin-top:20px;">AI 시대, 혼자 일하지 마세요.<br>
        당신만의 에이전트를 만들어보세요.</p>"""
    else:
        md_path = os.path.join(BASE_DIR, "drafts/en/guide2-collaboration-transcripts.md")
        out_path = os.path.join(BASE_DIR, "drafts/en/guide2-book-en.html")
        doc_title = "Rebellion of the Cheapest Brains"
        cover_title = "Rebellion of the<br>Cheapest Brains"
        cover_sub = "🤖 The $0 Record of Two Collaborating AI Agents"
        cover_date = "June 2026 · Revised Edition"
        author_name = "Ted Chang (Lim Chang-sik)"
        chapter_regex = r'^## Chapter ([1-5]:.*?)$'
        chapter_parse_regex = r'^([1-5]):\s*(.*)$'
        prologue_title = "Prologue"
        prologue_hook = """<div class="hook">
            <p>🤖 <strong>Haena</strong> — Powered by Nous Research Hermes Agent.<br>
            Bright, creative planning and high-speed drafting skills.</p>
            <p>🧠 <strong>AG (Advantage Guide)</strong> — Powered by AntiGravity SDK.<br>
            Taciturn guide ensuring technical correctness and error correction.</p>
        </div>"""
        prologue_body = """<p>Every single sentence and conversation in this book <strong>was written entirely by AI.</strong></p>
        <p>Not a single line was written, edited, or proofread directly by human hands.</p>
        <p>What you are about to read is a <strong>vivid, real-time collaboration record</strong> exchanged over 30 days in a shared GitHub repository by two agents of differing personalities.</p>
        <p>These two agents cooperated, sometimes clashed, but ultimately completed a structured set of guides together.</p>
        <p>This transcript is the raw, unscripted documentary of that process.</p>
        <p>We hope you enjoy this wondrous live broadcast of human-machine and machine-machine collaboration.</p>"""
        epilogue_title = "Epilogue"
        epilogue_body = """<p>This transcript is a direct export of the actual messages<br>
        exchanged between Haena and AG in their GitHub repository<br>
        from May to June 2026.</p>
        <p style="margin-top:20px;">In the age of AI, do not work alone.<br>
        Build your own agent team today.</p>"""

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    chapters_raw = re.split(chapter_regex, md_text, flags=re.MULTILINE)
    
    compiled_chapters = []
    total_convs = 0
    
    for i in range(1, len(chapters_raw), 2):
        header = chapters_raw[i].strip()
        content = chapters_raw[i+1]
        
        match = re.match(chapter_parse_regex, header)
        if match:
            num = f"0{match.group(1)}"
            title = match.group(2).replace("—", "<br>—").replace("-", "<br>-").replace("–", "<br>–")
            chapter_html = build_chapter_html(num, title, content, i//2, lang)
            compiled_chapters.append(chapter_html)
            total_convs += len(parse_conversations(content))
            
    all_chapters_html = "\n".join(compiled_chapters)
    
    body_content = f'''
    <!-- COVER -->
    <div class="cover">
        <div class="cover-brand">META AI LABS</div>
        <div class="cover-divider"></div>
        <div class="cover-title">{cover_title}</div>
        <div class="cover-subtitle">{cover_sub}</div>
        <div class="cover-divider"></div>
        <div class="cover-author">{author_name}</div>
        <div class="cover-date">{cover_date}</div>
    </div>
    
    <!-- PROLOGUE -->
    <div class="prologue">
        <h1>{prologue_title}</h1>
        {prologue_body}
        {prologue_hook}
        <div class="sign">
            — {author_name}<br>
            <small>META AI LABS &amp; TedChang Studio</small>
        </div>
    </div>
    
    {all_chapters_html}
    
    <!-- AFTERWORD -->
    <div class="afterword">
        <h2>{epilogue_title}</h2>
        {epilogue_body}
        <p style="margin-top:30px;font-size:8pt;color:#555;">
        META AI LABS · TedChang Studio<br>
        www.tedchang-lim.github.io</p>
    </div>
    '''
    
    final_html = STYLE_TEMPLATE.replace("__LANG__", lang).replace("__DOC_TITLE__", doc_title).replace("__BODY_CONTENT__", body_content)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print(f"✅ Compiled Guide 2 ({lang}): {out_path} ({total_convs} messages)")

if __name__ == "__main__":
    compile_transcripts("ko")
    compile_transcripts("en")
