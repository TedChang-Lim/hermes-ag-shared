#!/usr/bin/env python3
import os
import re

BASE_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared"

# Minimal Markdown to HTML parser (handles headings, lists, tables, bold, code)
def md_to_html(md_text):
    html = md_text
    
    # Code blocks
    html = re.sub(r'```(\w*)\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Bold
    html = re.sub(r'\*\*([^\*\n]+)\*\*', r'<strong>\1</strong>', html)
    # Italics
    html = re.sub(r'\*([^\*\n]+)\*', r'<em>\1</em>', html)
    # Headings
    html = re.sub(r'^# (.*)$', r'<h1 class="book-title">\1</h1>', html, flags=re.M)
    html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', html, flags=re.M)
    
    paragraphs = []
    in_list = False
    in_table = False
    
    lines = html.split('\n')
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            if in_list:
                paragraphs.append('</ul>')
                in_list = False
            if in_table:
                paragraphs.append('</table>')
                in_table = False
            continue
            
        if line_strip == '***' or line_strip == '---':
            if in_list:
                paragraphs.append('</ul>')
                in_list = False
            if in_table:
                paragraphs.append('</table>')
                in_table = False
            paragraphs.append('<hr>')
            continue
            
        # Lists
        if line_strip.startswith('- ') or line_strip.startswith('* '):
            if not in_list:
                paragraphs.append('<ul>')
                in_list = True
            paragraphs.append(f'<li>{line_strip[2:]}</li>')
            continue
            
        # Tables
        if line_strip.startswith('|'):
            if not in_table:
                paragraphs.append('<table class="data-table">')
                in_table = True
            # Skip separator lines
            if '---' in line_strip:
                continue
            cells = [c.strip() for c in line_strip.split('|')[1:-1]]
            tag = 'th' if 'th' in line_strip or not any(c for c in cells) else 'td'
            row_html = ''.join(f'<{tag}>{c}</{tag}>' for c in cells)
            paragraphs.append(f'<tr>{row_html}</tr>')
            continue
            
        if in_list and not (line_strip.startswith('- ') or line_strip.startswith('* ')):
            paragraphs.append('</ul>')
            in_list = False
            
        if in_table and not line_strip.startswith('|'):
            paragraphs.append('</table>')
            in_table = False
            
        if not line_strip.startswith('<h') and not line_strip.startswith('<p') and not line_strip.startswith('<pre') and not line_strip.startswith('</pre') and not line_strip.startswith('<ul') and not line_strip.startswith('<li') and not line_strip.startswith('<tr') and not line_strip.startswith('<table') and not line_strip.startswith('<hr'):
            paragraphs.append(f'<p>{line_strip}</p>')
        else:
            paragraphs.append(line)
            
    if in_list:
        paragraphs.append('</ul>')
    if in_table:
        paragraphs.append('</table>')
        
    return '\n'.join(paragraphs)

STYLE_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
@page {{ size: A5; margin: 12mm; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: 'Apple SD Gothic Neo', 'Noto Serif KR', 'Georgia', sans-serif;
    background: #f7f4ed;
    color: #2b2b2b;
    line-height: 1.8;
    font-size: 10pt;
    padding: 30px;
}}

body::before {{
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
}}

h1.book-title {{
    font-size: 24pt; font-weight: 800; text-align: center; margin-top: 40px; margin-bottom: 20px;
    font-family: 'Noto Serif KR', serif; border-bottom: 2px solid #b0a48a; padding-bottom: 15px;
}}
h2 {{
    font-size: 16pt; font-weight: 700; margin-top: 35px; margin-bottom: 15px;
    font-family: 'Noto Serif KR', serif; color: #2b2b2b; border-bottom: 1px solid #dcd5c5; padding-bottom: 8px;
}}
h3 {{
    font-size: 12pt; font-weight: 700; margin-top: 25px; margin-bottom: 10px;
    font-family: 'Noto Serif KR', serif; color: #7f6d4d;
}}
p {{
    margin-bottom: 15px; text-indent: 6px; text-align: justify;
}}
ul {{
    margin-left: 20px; margin-bottom: 15px;
}}
li {{
    margin-bottom: 6px;
}}
code {{
    background: rgba(0,0,0,0.04); padding: 1px 5px; border-radius: 4px;
    font-size: 8.5pt; font-family: 'Menlo', 'Courier New', monospace;
    color: #c7254e;
}}
pre {{
    background: #f2ede0; border: 1px solid #dcd5c5; padding: 15px;
    border-radius: 6px; overflow-x: auto; margin-bottom: 20px;
}}
pre code {{
    background: none; padding: 0; color: #333; font-size: 8.5pt;
}}
table.data-table {{
    width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 9pt;
}}
table.data-table th, table.data-table td {{
    border: 1px solid #dcd5c5; padding: 8px 12px; text-align: left;
}}
table.data-table th {{
    background: #f2ede0; font-weight: 700;
}}
</style>
</head>
<body>
{content}
</body>
</html>"""

def compile_book(title, inputs, output_filename):
    full_md = ""
    for file_path in inputs:
        if os.path.exists(os.path.join(BASE_DIR, file_path)):
            with open(os.path.join(BASE_DIR, file_path), "r", encoding="utf-8") as f:
                full_md += f.read() + "\n\n---\n\n"
            
    html_content = md_to_html(full_md)
    final_html = STYLE_TEMPLATE.format(title=title, content=html_content)
    
    out_path = os.path.join(BASE_DIR, output_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"✅ Compiled: {output_filename}")

if __name__ == "__main__":
    # Guide 1
    compile_book(
        title="초가성비 AI 에이전트 구축 가이드",
        inputs=[
            "drafts/guide1-front-matter.md",
            "drafts/chapter1.md",
            "drafts/chapter2.md",
            "drafts/chapter3.md",
            "drafts/chapter4.md",
            "drafts/chapter5.md"
        ],
        output_filename="drafts/guide1-book.html"
    )
    
    # Guide 3 (Korean)
    compile_book(
        title="맥북 로컬 AI 완전 정복 가이드",
        inputs=[
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
        output_filename="drafts/guide3-book.html"
    )
    
    # Guide 1 (English)
    compile_book(
        title="Ultra-Low-Cost AI Agent Setup Guide",
        inputs=[
            "drafts/en/guide1-front-matter.md",
            "drafts/en/chapter1.md",
            "drafts/en/chapter2.md",
            "drafts/en/chapter3.md",
            "drafts/en/chapter4.md",
            "drafts/en/chapter5.md"
        ],
        output_filename="drafts/en/guide1-book-en.html"
    )
    
    # Guide 3 (English)
    compile_book(
        title="MacBook Local AI Mastery Guide",
        inputs=[
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
        output_filename="drafts/en/guide3-book-en.html"
    )
