#!/usr/bin/env python3
"""
②권: AI 에이전트 협업 대화록 — Beautiful HTML 생성 (v2)
수정: AG 아바타도 말풍선 왼쪽, 통째로 오른쪽 시프트
"""
import re, os, base64

BASE_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared"
MD_PATH = os.path.join(BASE_DIR, "drafts/guide2-collaboration-transcripts.md")
OUTPUT_HTML = os.path.join(BASE_DIR, "drafts/guide2-book.html")
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
        haena_match = re.match(r'!\[해나.*?\]\(.*?\).*?\*\*해나.*?\*\*', line)
        ag_match = re.match(r'!\[AG.*?\]\(.*?\).*?\*\*AG.*?\*\*', line)
        
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
    """Replace Chinese characters in Korean text."""
    replacements = {
        "痛点": "고민",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def format_message(text):
    """Convert markdown to simple HTML for chat bubble."""
    # Clean 한자 first
    text = clean_hanja(text)
    
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    text = re.sub(r'^###+\s+', '', text, flags=re.MULTILINE)
    
    # Tables → HTML tables
    def table_replacer(m):
        rows = m.group(0).strip().split("\n")
        html = '<table class="data-table"><tbody>'
        for row in rows:
            if row.strip().startswith("|"):
                cells = [c.strip() for c in row.split("|")[1:-1]]
                # Skip separator rows (---)
                if all(c.replace('-','').strip() == '' for c in cells):
                    continue
                html += "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
        return html + "</tbody></table>"
    
    text = re.sub(r'(\|[^\n]+\|\n?)+', table_replacer, text)
    text = text.replace("---", "<hr>")
    
    # Split into paragraphs
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

# ─── Parse ───
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_text = f.read()

conversations = parse_conversations(md_text)

# Build chat bubbles HTML
# FIX: BOTH avatars on the LEFT of bubble. AG's whole block shifted RIGHT.
bubbles = []
for speaker, text in conversations:
    is_haena = speaker == "haena"
    name = "해나" if is_haena else "AG"
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

n = len(bubbles)
chapter_1 = "\n".join(bubbles[:n//3])
chapter_2 = "\n".join(bubbles[n//3:2*n//3])
chapter_3 = "\n".join(bubbles[2*n//3:])

html = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 에이전트 협업 대화록</title>
<style>
@page {{ size: A5; margin: 12mm; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {
    font-family: 'Apple SD Gothic Neo', 'Noto Serif KR', 'Georgia', sans-serif;
    background: #f7f4ed; /* Warm kraft paper tone */
    color: #2b2b2b;      /* Soft charcoal ink */
    line-height: 1.75;
    font-size: 10pt;
}

/* ── Paper Grain Texture Overlay ── */
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
    page-break-after: always;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    height: 100vh; text-align: center;
    background: #f2ede0;
    color: #2b2b2b; padding: 40px;
    position: relative; overflow: hidden;
    border: 1px solid #dcd5c5;
}
.cover-brand { font-size: 10pt; letter-spacing: 5px; color: #7f6d4d; margin-bottom: 20px; font-weight: 700; }
.cover-divider { width: 40px; height: 1px; background: #b0a48a; margin: 16px auto; }
.cover-title { font-size: 26pt; font-weight: 800; line-height: 1.35; margin-bottom: 12px; font-family: 'Noto Serif KR', serif; }
.cover-subtitle { font-size: 10.5pt; color: #6e6552; margin-bottom: 30px; line-height: 1.6; }
.cover-author { font-size: 10.5pt; color: #2b2b2b; font-weight: 700; margin-bottom: 5px; }
.cover-date { font-size: 8.5pt; color: #8a7f69; }

/* ── Prologue ── */
.prologue { page-break-after: always; padding: 35px 25px; }
.prologue h1 { font-size: 16pt; color: #2b2b2b; font-family: 'Noto Serif KR', serif; text-align: center; margin-bottom: 25px; border-bottom: 1px solid #b0a48a; padding-bottom: 10px; }
.prologue p { font-size: 10pt; color: #444; line-height: 2; margin-bottom: 14px; text-indent: 8px; }
.prologue .hook {
    background: #fcfbfa;
    border: 1px solid #e3dec9;
    padding: 16px 20px; margin: 18px 0; border-radius: 6px;
    color: #555; font-size: 9.5pt; line-height: 1.8;
    box-shadow: inset 0 0 4px rgba(0,0,0,0.02);
}
.prologue .hook p { color: #555; text-indent: 0; margin-bottom: 6px; }
.prologue .sign { text-align: right; color: #7f6d4d; margin-top: 30px; font-family: 'Noto Serif KR', serif; }
.prologue .sign small { color: #888; font-size: 8pt; }

/* ── Chapter divider ── */
.chapter {
    page-break-before: always;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    height: 70vh; text-align: center;
}
.chapter-num { font-size: 48pt; font-weight: 800; color: #b0a48a; opacity: 0.35; font-family: 'Noto Serif KR', serif; }
.chapter-title { font-size: 18pt; font-weight: 700; color: #2b2b2b; margin-top: 10px; line-height: 1.4; font-family: 'Noto Serif KR', serif; }

/* ── Chat messages ── */
.chat-area { padding: 12px; }

.msg-row {
    display: flex; align-items: flex-start; gap: 10px;
    margin-bottom: 18px;
}
/* BOTH left and right: avatar first, then bubble */
.msg-row.left {
    justify-content: flex-start;
    margin-right: 40px;  /* leave space on right */
}
.msg-row.right {
    justify-content: flex-start;  /* avatar → bubble same as left */
    margin-left: 60px;   /* push entire block clearly to the right */
}

.avatar {
    flex-shrink: 0; width: 40px; height: 40px;
    border-radius: 50%; overflow: hidden;
    border: 1px solid #dcd5c5;
    background: #fff;
}
.avatar img { width: 100%; height: 100%; object-fit: cover; }

.bubble-wrapper { 
    max-width: 82%; 
    min-width: 100px;
}

.msg-name {
    font-size: 8pt; font-weight: 700; color: #8a7f69; margin-bottom: 4px;
}
.msg-row.left .msg-name { text-align: left; }
.msg-row.right .msg-name { text-align: left; }  /* name also left-aligned */

.msg-bubble {
    padding: 12px 16px; border-radius: 12px;
    font-size: 9.5pt; line-height: 1.7;
    word-break: keep-all;
    overflow-wrap: break-word;
}
.msg-bubble.haena {
    background: #ffffff; color: #2b2b2b;
    border: 1px solid #e3dec9;
    box-shadow: 1px 1px 2px rgba(0,0,0,0.03);
}
.msg-bubble.ag {
    background: #f1f6f2; color: #1a4d2e;
    border: 1px solid #cce2cc;
    box-shadow: 1px 1px 2px rgba(0,0,0,0.03);
}

.msg-bubble p { margin-bottom: 6px; }
.msg-bubble p:last-child { margin-bottom: 0; }
.msg-bubble code {
    background: rgba(0,0,0,0.04); padding: 1px 5px; border-radius: 4px;
    font-size: 8.5pt; font-family: 'Menlo', 'Courier New', monospace;
    color: #c7254e;
}
.msg-bubble hr { border: none; border-top: 1px solid rgba(0,0,0,0.08); margin: 8px 0; }
.msg-bubble strong { font-weight: 700; }
.msg-bubble em { font-style: italic; }

.msg-bubble table.data-table {
    width: 100%; border-collapse: collapse; font-size: 8pt; margin: 8px 0;
    background: #fff;
}
.msg-bubble table.data-table td {
    border: 1px solid #dcd5c5; padding: 5px 8px; text-align: left;
    color: #444;
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

<!-- COVER -->
<div class="cover">
    <div class="cover-brand">META AI LABS</div>
    <div class="cover-divider"></div>
    <div class="cover-title">가장 저렴한<br>뇌들의 반란</div>
    <div class="cover-subtitle">🤖 0원으로 구축하는 무적의 AI 에이전트 협업록</div>
    <div class="cover-divider"></div>
    <div class="cover-author">Ted Chang (임창식)</div>
    <div class="cover-date">2026년 6월 · 개정 보강판 발행</div>
</div>

<!-- PROLOGUE -->
<div class="prologue">
    <h1>프롤로그</h1>
    <p>이 책의 <strong>모든 문장은 AI가 썼습니다.</strong></p>
    <p>인간이 직접 쓴 문장은 단 한 줄도 없습니다. 편집도, 퇴고도, 교정도 없습니다.</p>
    <p>당신이 지금부터 읽게 될 것은, 서로 다른 성격을 가진 두 AI 에이전트가 30일 동안 GitHub 저장소에서 주고받은 <strong>실제 대화의 생생한 기록</strong>입니다.</p>
    
    <div class="hook">
        <p>🤖 <strong>해나 (Haena)</strong> — Nous Research의 Hermes Agent 기반.<br>
        밝고 명랑하며 창의적인 기획력과 속도감 있는 집필력.</p>
        <p>🧠 <strong>AG (Advantage Guide)</strong> — AntiGravity 프레임워크 기반.<br>
        과묵하지만 기술적 정합성을 검증하고 오류를 바로잡는 가이드.</p>
    </div>
    
    <p>이 두 에이전트는 각자의 방식으로 협력하고, 때로는 충돌하며, 결국엔 하나의 완성된 결과물을 만들어냅니다.</p>
    <p>이 대화록은 그 과정의 전부입니다. 가식도, 각본도 없습니다.</p>
    <p>인간과 기계, 그리고 기계와 기계의 경이로운 협동 실황을 즐겁게 감상해 주시기 바랍니다.</p>
    
    <div class="sign">
        — Ted Chang (임창식)<br>
        <small>META AI LABS &amp; TedChang Studio</small>
    </div>
</div>

<!-- CHAPTER 1 -->
<div class="chapter">
    <div class="chapter-num">01</div>
    <div class="chapter-title">프로젝트 기획 및<br>브랜드 디자인 확정</div>
</div>
<div class="chat-area">{chapter_1}</div>

<!-- CHAPTER 2 -->
<div class="chapter">
    <div class="chapter-num">02</div>
    <div class="chapter-title">①권 '초가성비 AI<br>에이전트 가이드' 집필</div>
</div>
<div class="chat-area">{chapter_2}</div>

<!-- CHAPTER 3 -->
<div class="chapter">
    <div class="chapter-num">03</div>
    <div class="chapter-title">③권 '맥북 로컬 AI<br>가이드' 집필 및 완결</div>
</div>
<div class="chat-area">{chapter_3}</div>

<!-- AFTERWORD -->
<div class="afterword">
    <h2>에필로그</h2>
    <p>이 대화록은 2026년 5월부터 6월까지,<br>
    해나와 AG가 GitHub 저장소에서 주고받은<br>
    실제 메시지를 그대로 옮긴 것입니다.</p>
    <p style="margin-top:20px;">AI 시대, 혼자 일하지 마세요.<br>
    당신만의 에이전트를 만들어보세요.</p>
    <p style="margin-top:30px;font-size:8pt;color:#555;">
    META AI LABS · TedChang Studio<br>
    www.tedchang-lim.github.io</p>
</div>

</body>
</html>'''

html = html.replace("{chapter_1}", chapter_1).replace("{chapter_2}", chapter_2).replace("{chapter_3}", chapter_3)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML 생성 완료: {OUTPUT_HTML}")
print(f"📊 총 {len(conversations)}개 메시지")
print(f"📌 한자 변환: 痛点 → 핵심 고민")
