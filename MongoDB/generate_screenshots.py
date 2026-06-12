"""
Generate mockup screenshots — Modern GUI v2
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "assets/screenshots"
os.makedirs(OUT, exist_ok=True)

# ── Colors ──────────────────────────────────────────────────
C = {
    "bg": "#f5f6fa",
    "card": "#ffffff",
    "primary": "#2b579a",
    "secondary": "#4ecdc4",
    "text": "#2d3436",
    "muted": "#636e72",
    "border": "#dfe6e9",
    "green_bg": "#e8f5e9",
    "green_fg": "#2e7d32",
    "red_bg": "#ffebee",
    "red_fg": "#c62828",
    "orange_bg": "#fff3e0",
    "yellow_bg": "#fffde7",
    "btn_bg": "#2b579a",
    "row_even": "#f8f9fa",
}


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


def draw_window_bg(draw, w, h, title="BMI Calculator with MongoDB — DADS6005"):
    draw.rectangle([0, 0, w, 34], fill=C["primary"])
    draw.text((14, 8), title, fill="white", font=getfont(11))


def draw_tab(draw, tabs, active=0, x_start=8, y=38):
    x = x_start
    for i, t in enumerate(tabs):
        w = 110 if "BMI" in t else 120
        bg = C["card"] if i == active else "#e0e0e0"
        fg = C["primary"] if i == active else C["text"]
        draw.rectangle([x, y, x + w, y + 26], fill=bg, outline=C["border"])
        draw.text((x + 14, y + 5), t, fill=fg, font=getfont(10))
        x += w + 2


def round_rect(draw, xy, r=8, **kw):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, **kw)


# ============================================================
# Screenshot 1 — BMI Calculator Tab (Active)
# ============================================================
W1, H1 = 600, 560
img1 = Image.new("RGB", (W1, H1), C["bg"])
d1 = ImageDraw.Draw(img1)

draw_window_bg(d1, W1, H1)
draw_tab(d1, ["BMI", "ดูข้อมูล"], active=0)

# Header text
d1.text((20, 74), "เครื่องคำนวณดัชนีมวลกาย (BMI)", fill=C["text"], font=getfont(14, bold=True))
d1.text((20, 93), "คำนวณ BMI พร้อมคำแนะนำสุขภาพ และบันทึกข้อมูลลง MongoDB",
        fill=C["muted"], font=getfont(9))

# Input card
round_rect(d1, [20, 112, 580, 200], fill=C["card"], outline=C["border"])
d1.text((32, 120), "ข้อมูลร่างกาย", fill=C["text"], font=getfont(10, bold=True))

# Weight field
d1.text((45, 148), "น้ำหนักตัว (kg.)", fill=C["text"], font=getfont(10))
round_rect(d1, [45, 168, 210, 192], fill="white", outline="#cccccc")
d1.text((98, 172), "70", fill="#b2bec3", font=getfont(11))

# Height field
d1.text((310, 148), "ส่วนสูง (cm.)", fill=C["text"], font=getfont(10))
round_rect(d1, [310, 168, 470, 192], fill="white", outline="#cccccc")
d1.text((365, 172), "175", fill="#b2bec3", font=getfont(11))

# Buttons
round_rect(d1, [45, 204, 175, 230], fill=C["primary"])
d1.text((58, 209), "คำนวณ & บันทึก", fill="white", font=getfont(10))
round_rect(d1, [185, 204, 263, 230], fill=C["card"], outline=C["border"])
d1.text((201, 209), "ล้าง", fill=C["text"], font=getfont(10))

# Progress bar label
d1.text((20, 246), "ดัชนีมวลกาย (BMI)", fill=C["muted"], font=getfont(9))

# Progress bar
d1.rectangle([20, 258, 580, 274], fill="#e0e0e0", outline=None)
d1.rectangle([20, 258, 220, 274], fill=C["secondary"])

# Result card (green = healthy)
round_rect(d1, [20, 286, 580, 520], fill=C["green_bg"], outline="#c8e6c9")
d1.text(
    (30, 300),
    "BMI = 22.86    |    ปกติ (สุขภาพดี)    |    ความเสี่ยง: เท่าคนปกติ",
    fill=C["green_fg"],
    font=getfont(11, bold=True),
)
d1.text(
    (30, 330),
    "น้ำหนักปกติ\n\n"
    "ข้อแนะนำ\n"
    "1. กินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม\n"
    "2. ออกกำลังกายอย่างสม่ำเสมอ 30 นาที/วัน",
    fill=C["green_fg"],
    font=getfont(10),
)

img1.save(f"{OUT}/screenshot_bmi_tab.png")
print(f"[OK] {OUT}/screenshot_bmi_tab.png")


# ============================================================
# Screenshot 2 — View Data Tab
# ============================================================
W2, H2 = 620, 480
img2 = Image.new("RGB", (W2, H2), C["bg"])
d2 = ImageDraw.Draw(img2)

draw_window_bg(d2, W2, H2)
draw_tab(d2, ["BMI", "ดูข้อมูล"], active=1, x_start=120)

# Header
d2.text((15, 74), "ประวัติ BMI ทั้งหมด", fill=C["text"], font=getfont(14, bold=True))

# Table header
col_x = [20, 55, 210, 280, 350, 420]
col_w = [35, 155, 70, 70, 70, 100]
headers = ["#", "Computer", "น้ำหนัก", "ส่วนสูง", "BMI", "วันที่"]

d2.rectangle([15, 98, 605, 120], fill=C["secondary"])
for i, h in enumerate(headers):
    d2.text((col_x[i] + 4, 101), h, fill="white", font=getfont(10, bold=True))

# Sample data
rows = [
    ("1", "DESKTOP-ABC", "70", "175", "22.86", "2026-06-12"),
    ("2", "DESKTOP-ABC", "68", "175", "22.20", "2026-06-10"),
    ("3", "DESKTOP-XYZ", "85", "180", "26.23", "2026-06-08"),
    ("4", "DESKTOP-ABC", "72", "175", "23.51", "2026-06-05"),
    ("5", "LAPTOP-001", "55", "160", "21.48", "2026-06-03"),
    ("6", "DESKTOP-XYZ", "82", "180", "25.31", "2026-06-01"),
]

y = 121
for i, row in enumerate(rows):
    bg_s = C["row_even"] if i % 2 == 1 else "white"
    d2.rectangle([15, y, 605, y + 26], fill=bg_s)
    for j, val in enumerate(row):
        if j == 4:
            bmi_val = float(val)
            bmi_color = C["green_fg"] if bmi_val < 24 else (C["red_fg"] if bmi_val > 30 else "#e65100")
            d2.text((col_x[j] + 4, y + 4), val, fill=bmi_color, font=getfont(10, bold=True))
        else:
            d2.text((col_x[j] + 4, y + 4), val, fill=C["text"], font=getfont(10))
    y += 26

# Buttons
bx_pos = [20, 105, 190, 275]
btn_labels = ["แก้ไข", "ลบ", "กราฟ", "ออก"]
for i in range(4):
    round_rect(d2, [bx_pos[i], y + 10, bx_pos[i] + 75, y + 34], fill=C["primary"])
    d2.text((bx_pos[i] + 6, y + 15), btn_labels[i], fill="white", font=getfont(10))

img2.save(f"{OUT}/screenshot_view_tab.png")
print(f"[OK] {OUT}/screenshot_view_tab.png")


# ============================================================
# Screenshot 3 — Weight Trend Graph
# ============================================================
W3, H3 = 580, 460
img3 = Image.new("RGB", (W3, H3), "#f8f9fa")
d3 = ImageDraw.Draw(img3)

d3.rectangle([0, 0, W3, 34], fill=C["primary"])
d3.text((14, 8), "Weight Trend Graph - แนวโน้มน้ำหนัก", fill="white", font=getfont(11))

d3.text((20, 44), "แนวโน้มน้ำหนัก (Weight Trend)", fill=C["text"], font=getfont(14, bold=True))

# Graph area
gx, gy, gw, gh = 70, 80, 460, 320
d3.rectangle([gx, gy, gx + gw, gy + gh], fill="white", outline=C["border"])

# Axes
d3.line([gx + 40, gy + gh - 30, gx + gw - 10, gy + gh - 30], fill=C["text"], width=2)  # x
d3.line([gx + 40, gy + 20, gx + 40, gy + gh - 30], fill=C["text"], width=2)  # y
d3.text((gx + 4, gy + 8), "น้ำหนัก (kg.)", fill=C["text"], font=getfont(8))

# X labels
dates = ["May 01", "May 15", "Jun 01", "Jun 15", "Jul 01"]
for i, dd in enumerate(dates):
    x = gx + 60 + i * 80
    d3.text((x - 16, gy + gh - 24), dd, fill=C["muted"], font=getfont(7))
d3.text((gx + gw - 50, gy + gh - 12), "วันที่", fill=C["text"], font=getfont(8))

# Y labels
for i, yy in enumerate(range(50, 95, 5)):
    y = gy + gh - 30 - (yy - 50) * 6
    d3.text((gx + 8, y - 6), str(yy), fill=C["muted"], font=getfont(8))
    d3.line([gx + 38, y, gx + 42, y], fill=C["text"])

# Data
pts = [(gx + 60, gy + gh - 100), (gx + 140, gy + gh - 90), (gx + 220, gy + gh - 115),
       (gx + 300, gy + gh - 130), (gx + 380, gy + gh - 110)]
for i, (px, py) in enumerate(pts):
    d3.ellipse([px - 5, py - 5, px + 5, py + 5], fill="#2ecc71", outline="#27ae60")
    if i > 0:
        d3.line([pts[i - 1][0], pts[i - 1][1], px, py], fill="#95e1d3", width=2)

img3.save(f"{OUT}/screenshot_graph.png")
print(f"[OK] {OUT}/screenshot_graph.png")

print("\n=== All screenshots regenerated ===")
