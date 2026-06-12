"""
Generate mockup screenshots — Flet Material 3 Style
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "assets/screenshots"
os.makedirs(OUT, exist_ok=True)


def getfont(size, bold=False):
    paths = [
        "C:/Windows/Fonts/LeelawUI.ttf",
        "C:/Windows/Fonts/angsana.ttc",
        "C:/Windows/Fonts/cordia.ttc",
        "C:/Windows/Fonts/tahoma.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()


C = {
    "surface": "#f5f6fa",
    "card": "#ffffff",
    "primary": "#3f51b5",
    "on_primary": "#ffffff",
    "secondary": "#4ecdc4",
    "text": "#1a1a2e",
    "muted": "#636e72",
    "border": "#e0e0e0",
    "green_bg": "#e8f5e9",
    "green_fg": "#2e7d32",
    "red_bg": "#ffebee",
    "orange_bg": "#fff3e0",
    "row_even": "#f8f9fa",
}

# ── Helpers ─────────────────────────────────────────────────

def rr(draw, xy, r=12, **kw):
    draw.rounded_rectangle(xy, radius=r, **kw)


def header_bar(draw, w, title="BMI Calculator"):
    draw.rectangle([0, 0, w, 56], fill=C["primary"])
    draw.text((20, 16), title, fill=C["on_primary"], font=getfont(16, bold=True))


def material_button(draw, x, y, w, h, text, icon="", fill=True):
    bg = C["primary"] if fill else C["card"]
    txt_color = C["on_primary"] if fill else C["primary"]
    border = None if fill else C["border"]
    rr(draw, [x, y, x + w, y + h], fill=bg, outline=border)
    tx = x + 14 if icon else x + (w - len(text) * 6) // 2
    draw.text((tx, y + (h - 14) // 2), text, fill=txt_color, font=getfont(12))


def input_field(draw, x, y, w, h, label, value=""):
    rr(draw, [x, y, x + w, y + h], fill="white", outline=C["border"])
    draw.text((x + 12, y + 4), label, fill=C["muted"], font=getfont(8))
    if value:
        draw.text((x + 12, y + 20), value, fill=C["text"], font=getfont(12))


# ════════════════════════════════════════════════════════════
# Screenshot 1 — BMI Calculator Tab
# ════════════════════════════════════════════════════════════
W1, H1 = 640, 580
img1 = Image.new("RGB", (W1, H1), C["surface"])
d1 = ImageDraw.Draw(img1)

header_bar(d1, W1, "BMI Calculator with MongoDB")

# Tab bar
d1.rectangle([0, 56, W1, 100], fill=C["card"])
rr(d1, [16, 62, 120, 94], fill=C["primary"])
d1.text((36, 72), "BMI", fill=C["on_primary"], font=getfont(12))
rr(d1, [128, 62, 240, 94], fill=C["card"], outline=C["border"])
d1.text((145, 72), "ดูข้อมูล", fill=C["text"], font=getfont(12))

# Title
d1.text((24, 114), "เครื่องคำนวณดัชนีมวลกาย (BMI)", fill=C["text"], font=getfont(18, bold=True))
d1.text((24, 138), "คำนวณ BMI พร้อมคำแนะนำสุขภาพ และบันทึกข้อมูลลง MongoDB",
        fill=C["muted"], font=getfont(11))

# Input cards
CX, CY = 24, 164
rr(d1, [CX, CY, CX + 280, CY + 78], fill=C["card"], outline=C["border"])
input_field(d1, CX + 20, CY + 14, 240, 48, "น้ำหนักตัว (kg.)", "70")

CX2 = 336
rr(d1, [CX2, CY, CX2 + 280, CY + 78], fill=C["card"], outline=C["border"])
input_field(d1, CX2 + 20, CY + 14, 240, 48, "ส่วนสูง (cm.)", "175")

# Buttons
material_button(d1, 160, 260, 160, 42, "คำนวณ & บันทึก", fill=True)
material_button(d1, 335, 260, 100, 42, "ล้าง", fill=False)

# Result card (green = healthy)
RY = 320
rr(d1, [24, RY, 616, RY + 220], fill=C["green_bg"], outline="#c8e6c9")
d1.text((40, RY + 18), "BMI = 22.86", fill=C["green_fg"], font=getfont(22, bold=True))
d1.text((40, RY + 50), "ปกติ (สุขภาพดี) (ความเสี่ยง: เท่าคนปกติ)", fill=C["green_fg"], font=getfont(13, bold=True))
d1.text((40, RY + 80), "ข้อแนะนำ:", fill=C["green_fg"], font=getfont(12, bold=True))
d1.text((40, RY + 100), "1. กินอาหารครบ 5 หมู่ในสัดส่วนเหมาะสม", fill=C["green_fg"], font=getfont(11))
d1.text((40, RY + 120), "2. ออกกำลังกาย 30 นาที/วัน", fill=C["green_fg"], font=getfont(11))

img1.save(f"{OUT}/screenshot_bmi_tab.png")
print(f"[OK] {OUT}/screenshot_bmi_tab.png")


# ════════════════════════════════════════════════════════════
# Screenshot 2 — View Data Tab
# ════════════════════════════════════════════════════════════
W2, H2 = 640, 520
img2 = Image.new("RGB", (W2, H2), C["surface"])
d2 = ImageDraw.Draw(img2)

header_bar(d2, W2, "BMI Calculator with MongoDB")

# Tab bar
d2.rectangle([0, 56, W2, 100], fill=C["card"])
rr(d2, [16, 62, 120, 94], fill=C["card"], outline=C["border"])
d2.text((36, 72), "BMI", fill=C["text"], font=getfont(12))
rr(d2, [128, 62, 240, 94], fill=C["primary"])
d2.text((145, 72), "ดูข้อมูล", fill=C["on_primary"], font=getfont(12))

d2.text((24, 114), "ประวัติ BMI ทั้งหมด", fill=C["text"], font=getfont(18, bold=True))

# Data table card
rr(d2, [20, 140, 620, 418], fill=C["card"], outline=C["border"])

# Table header
col_x = [40, 85, 250, 320, 390, 460]
headers = ["#", "Computer", "น้ำหนัก", "ส่วนสูง", "BMI", "วันที่"]
for i, h in enumerate(headers):
    d2.text((col_x[i], 150), h, fill=C["text"], font=getfont(10, bold=True))
d2.line([30, 168, 610, 168], fill=C["border"])

# Data rows
rows = [
    ("1", "DESKTOP-ABC", "70", "175", "22.86", "2026-06-12"),
    ("2", "DESKTOP-ABC", "68", "175", "22.20", "2026-06-10"),
    ("3", "DESKTOP-XYZ", "85", "180", "26.23", "2026-06-08"),
    ("4", "DESKTOP-ABC", "72", "175", "23.51", "2026-06-05"),
    ("5", "LAPTOP-001", "55", "160", "21.48", "2026-06-03"),
]
y = 174
for i, row in enumerate(rows):
    bg = C["row_even"] if i % 2 == 1 else "white"
    d2.rectangle([30, y, 610, y + 32], fill=bg)
    for j, val in enumerate(row):
        color = C["text"]
        if j == 4:
            bv = float(val)
            color = C["green_fg"] if bv < 24 else (C["red_bg"].replace("_bg","_fg") if bv > 30 else "#e65100")
            color = C["green_fg"] if bv < 23 else ("#e65100" if bv < 25 else "#c62828")
        d2.text((col_x[j], y + 6), val, fill=color if j != 4 else C["green_fg"], font=getfont(10, bold=(j == 4)))
    y += 32

# Buttons
BY = 432
rr(d2, [180, BY, 260, BY + 40], fill=C["primary"])
d2.text((194, BY + 10), "ลบ", fill=C["on_primary"], font=getfont(12))

rr(d2, [275, BY, 370, BY + 40], fill=C["card"], outline=C["border"])
d2.text((289, BY + 10), "กราฟ", fill=C["primary"], font=getfont(12))

img2.save(f"{OUT}/screenshot_view_tab.png")
print(f"[OK] {OUT}/screenshot_view_tab.png")


# ════════════════════════════════════════════════════════════
# Screenshot 3 — Weight Trend Graph
# ════════════════════════════════════════════════════════════
W3, H3 = 640, 480
img3 = Image.new("RGB", (W3, H3), "#f8f9fa")
d3 = ImageDraw.Draw(img3)

d3.rectangle([0, 0, W3, 56], fill=C["primary"])
d3.text((20, 16), "แนวโน้มน้ำหนัก (Weight Trend)", fill="white", font=getfont(16, bold=True))

d3.text((24, 72), "แนวโน้มน้ำหนัก (Weight Trend)", fill=C["text"], font=getfont(16, bold=True))

# Graph card
rr(d3, [20, 100, 620, 450], fill="white", outline=C["border"])

# Axes
gx, gy, gh = 80, 130, 260
gw = 500
d3.line([gx, gy + gh, gx + gw, gy + gh], fill=C["text"], width=2)
d3.line([gx, gy, gx, gy + gh], fill=C["text"], width=2)

# Y label
d3.text((gx - 2, gy - 22), "น้ำหนัก (kg.)", fill=C["muted"], font=getfont(9))

# Y ticks
for i, yy in enumerate(range(50, 95, 5)):
    y = gy + gh - (yy - 50) * 5
    d3.text((gx - 28, y - 7), str(yy), fill=C["muted"], font=getfont(8))
    d3.line([gx - 4, y, gx, y], fill=C["text"])

# X ticks
dates = ["01/05", "15/05", "01/06", "15/06", "01/07"]
for i, dd in enumerate(dates):
    x = gx + 40 + i * 90
    d3.text((x - 12, gy + gh + 4), dd, fill=C["muted"], font=getfont(8))
    d3.line([x, gy + gh, x, gy + gh + 4], fill=C["text"])
d3.text((gx + gw - 20, gy + gh + 4), "วันที่", fill=C["muted"], font=getfont(8))

# Data
pts = [(gx + 40, gy + gh - 60), (gx + 130, gy + gh - 50), (gx + 220, gy + gh - 80),
       (gx + 310, gy + gh - 100), (gx + 400, gy + gh - 75)]
for i, (px, py) in enumerate(pts):
    d3.ellipse([px - 5, py - 5, px + 5, py + 5], fill="#2ecc71", outline="#27ae60")
    if i > 0:
        d3.line([pts[i - 1][0], pts[i - 1][1], px, py], fill="#95e1d3", width=2)

img3.save(f"{OUT}/screenshot_graph.png")
print(f"[OK] {OUT}/screenshot_graph.png")

print("\n=== All screenshots regenerated ===")
