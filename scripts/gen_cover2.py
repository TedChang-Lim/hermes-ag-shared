#!/usr/bin/env python3
"""Generate Book ② cover image - chat bubble theme matching META AI LABS series style"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

OUTPUT = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared/templates/guide2_cover.png"
W, H = 1024, 1536

img = Image.new("RGBA", (W, H), (26, 26, 46))
draw = ImageDraw.Draw(img)

# Gradient background (dark blue)
for y in range(H):
    r = int(26 - (26 - 22) * y / H)
    g = int(26 - (26 - 30) * y / H)
    b = int(46 - (46 - 60) * y / H)
    draw.rectangle([0, y, W, y+1], fill=(r, g, b))

# Background glow
draw.ellipse([-200, 200, 500, 800], fill=(78, 204, 163, 8))
draw.ellipse([600, 600, 1200, 1200], fill=(255, 243, 205, 6))

# Try to load fonts
def get_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/AppleSDGothicNeo-Bold.otf",
        "/Library/Fonts/AppleSDGothicNeo.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

font_brand = get_font(36)
font_title = get_font(72)
font_sub = get_font(28)
font_author = get_font(32)
font_small = get_font(22)

# ── Chat bubble decorations ──
# Haena's bubble (yellow, left-ish)
bubble1_x1, bubble1_y1 = 120, 400
bubble1_x2, bubble1_y2 = 500, 540
draw.rounded_rectangle([bubble1_x1, bubble1_y1, bubble1_x2, bubble1_y2], radius=20,
                       fill=(255, 243, 205, 220), outline=(255, 234, 167), width=2)
draw.text((bubble1_x1 + 25, bubble1_y1 + 20), "🤖 이거 완전 대박인데요!?", 
          fill=(50, 50, 50), font=get_font(24))

# Haena avatar circle (next to her bubble)
haena_cx, haena_cy = bubble1_x1 - 35, bubble1_y1 + 40
draw.ellipse([haena_cx-30, haena_cy-30, haena_cx+30, haena_cy+30], 
             fill=(78, 204, 163), outline=(255, 255, 255, 50), width=2)
draw.text((haena_cx-8, haena_cy-10), "해", fill=(255, 255, 255), font=get_font(24, True))

# AG's bubble (green, right-ish)
bubble2_x1, bubble2_y1 = 460, 600
bubble2_x2, bubble2_y2 = 850, 760
draw.rounded_rectangle([bubble2_x1, bubble2_y1, bubble2_x2, bubble2_y2], radius=20,
                       fill=(212, 237, 218, 220), outline=(195, 230, 203), width=2)
draw.text((bubble2_x1 + 25, bubble2_y1 + 20), "잠만, 가격부터 확인하자.",
          fill=(21, 87, 36), font=get_font(24))
draw.text((bubble2_x1 + 25, bubble2_y1 + 55), "네가 쓴 가격이 틀렸어.",
          fill=(21, 87, 36), font=get_font(24))

# AG avatar circle (next to his bubble)
ag_cx, ag_cy = bubble2_x1 - 35, bubble2_y1 + 40
draw.ellipse([ag_cx-30, ag_cy-30, ag_cx+30, ag_cy+30], 
             fill=(78, 204, 163), outline=(255, 255, 255, 50), width=2)
draw.text((ag_cx-8, ag_cy-10), "AG", fill=(255, 255, 255), font=get_font(20, True))

# ── Brand ──
draw.text((W//2, 100), "META AI LABS", fill=(78, 204, 163), font=font_brand, anchor="mt")

# Divider line
draw.line([(W//2 - 60, 140), (W//2 + 60, 140)], fill=(78, 204, 163), width=2)

# ── Title ──
draw.text((W//2, 920), "AI 에이전트", fill=(255, 255, 255), font=font_title, anchor="mt")
draw.text((W//2, 1000), "협업 대화록", fill=(255, 255, 255), font=font_title, anchor="mt")

# ── Subtitle ──
draw.text((W//2, 1090), "두 인공지능이 책을 쓰기 위해", fill=(180, 180, 180), font=font_sub, anchor="mt")
draw.text((W//2, 1130), "나눈 30일간의 실제 대화 기록", fill=(180, 180, 180), font=font_sub, anchor="mt")

# Divider
draw.line([(W//2 - 60, 1190), (W//2 + 60, 1190)], fill=(78, 204, 163), width=2)

# ── Author ──
draw.text((W//2, 1240), "Ted Chang (임창식)", fill=(78, 204, 163), font=font_author, anchor="mt")

# ── Date ──
draw.text((W//2, 1290), "2026년 6월 · 초판 발행", fill=(120, 120, 120), font=font_small, anchor="mt")

# ── Chat icon row at bottom ──
draw.text((W//2, 1400), "💬 💬 💬", fill=(78, 204, 163, 60), font=get_font(48), anchor="mt")

img.save(OUTPUT)
print(f"✅ ②권 표지 생성 완료: {OUTPUT}")
