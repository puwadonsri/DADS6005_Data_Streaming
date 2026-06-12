"""
Generate mockup screenshots for MongoDB project README
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 520, 480
FONT = "Tahoma"
COLORS = {
    "bg": "#f0f0f0",
    "frame_bg": "#d9d9d9",
    "tab": "#e1e1e1",
    "tab_active": "#ffffff",
    "green": "#d4edda",
    "green_text": "#155724",
    "btn": "#0078d7",
    "btn_text": "#ffffff",
    "border": "#cccccc",
}

OUT = "assets/screenshots"
os.makedirs(OUT, exist_ok=True)


def getfont(size, bold=False):
    try:
        return ImageFont.truetype(f"{FONT}{'bd' if bold else ''}.ttf", size)
    except:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()


def mock_window(draw, title="BMI Calculator with MongoDB"):
    draw.rectangle([0, 0, W, 30], fill="#2b579a")
    draw.text((10, 6), title, fill="white", font=getfont(11))


def mock_tab(draw, tabs=["BMI", "View Data"], active=0):
    x = 10
    for i, t in enumerate(tabs):
        bg = COLORS["tab_active"] if i == active else COLORS["tab"]
        w = 100 if t == "BMI" else 120
        draw.rectangle([x, 35, x + w, 60], fill=bg, outline=COLORS["border"])
        draw.text((x + 10, 42), t, fill="black", font=getfont(10))
        x += w + 2


def mock_label_frame(draw, x, y, w, h, text):
    draw.rectangle([x, y, x + w, y + h], fill="white", outline=COLORS["border"])
    draw.text((x + 8, y + 4), text, fill="black", font=getfont(10, bold=True))
    return (x, y + 20, x + w, y + h)


# ============================================================
# Screenshot 1: BMI Calculator Tab (Active Tab)
# ============================================================
img1 = Image.new("RGB", (W, H), COLORS["bg"])
d1 = ImageDraw.Draw(img1)
mock_window(d1)
mock_tab(d1, active=0)

# BMI form frame
fx, fy, fw, fh = 30, 75, 460, 120
mock_label_frame(d1, fx, fy, fw, fh, "คำนวณค่าดัชนีมวลกาย (BMI)")

d1.text((50, fy + 30), "น้ำหนักตัว (kg.) :", fill="black", font=getfont(10))
d1.rectangle([170, fy + 28, 330, fy + 48], fill="white", outline="#aaa")
d1.text((175, fy + 30), "70", fill="#666", font=getfont(10))

d1.text((50, fy + 60), "ส่วนสูง (cm.) :", fill="black", font=getfont(10))
d1.rectangle([170, fy + 58, 330, fy + 78], fill="white", outline="#aaa")
d1.text((175, fy + 60), "175", fill="#666", font=getfont(10))

# Buttons
d1.rectangle([50, fy + 90, 150, fy + 112], fill=COLORS["btn"])
d1.text((58, fy + 92), "Calculate & Save", fill=COLORS["btn_text"], font=getfont(10))
d1.rectangle([160, fy + 90, 220, fy + 112], fill=COLORS["frame_bg"], outline="#aaa")
d1.text((175, fy + 93), "Clear", fill="black", font=getfont(10))

# BMI result
d1.rectangle([30, 210, 490, 260], fill=COLORS["green"], outline="#c3e6cb")
d1.text(
    (40, 218),
    "BMI : 22.86\nปกติ (สุขภาพดี)\nภาวะเสี่ยงต่อโรค : เท่าคนปกติ",
    fill=COLORS["green_text"],
    font=getfont(10),
)

# Advice
d1.rectangle([30, 265, 490, 430], fill="white", outline=COLORS["border"])
d1.text(
    (40, 270),
    "น้ำหนักปกติ\nค่าดัชนีมวลกายของคุณอยู่ระหว่าง 18.50 - 22.90\n\n"
    "ข้อแนะนำ\n"
    "1. กินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม\n"
    "2. ออกกำลังกายอย่างสม่ำเสมออย่างน้อย 30 นาที/วัน",
    fill="black",
    font=getfont(10),
)

img1.save(f"{OUT}/screenshot_bmi_tab.png")
print(f"[OK] {OUT}/screenshot_bmi_tab.png")


# ============================================================
# Screenshot 2: View Data Tab
# ============================================================
img2 = Image.new("RGB", (W, H), COLORS["bg"])
d2 = ImageDraw.Draw(img2)
mock_window(d2)
mock_tab(d2, active=1)

d2.text((20, 70), "BMI Data", fill="black", font=getfont(14, bold=True))

# Treeview header
cols_x = [20, 130, 240, 320, 20]
cols_w = [110, 110, 80, 100, 200]
headers = ["Computer Name", "Weight", "Height", "BMI", "Action"]
d2.rectangle([20, 95, 500, 115], fill="#4ecdc4")
x = 25
for h in headers[:4]:
    d2.text((x, 97), h, fill="white", font=getfont(10, bold=True))
    x += cols_w[headers.index(h)]

# Sample rows
sample_data = [
    ("DESKTOP-ABC", "70", "175", "22.86"),
    ("DESKTOP-ABC", "68", "175", "22.20"),
    ("DESKTOP-XYZ", "85", "180", "26.23"),
    ("DESKTOP-ABC", "72", "175", "23.51"),
    ("LAPTOP-001", "55", "160", "21.48"),
]
y = 116
for i, (name, w, h, b) in enumerate(sample_data):
    bg_s = "white" if i % 2 == 0 else "#f8f9fa"
    d2.rectangle([20, y, 500, y + 22], fill=bg_s)
    d2.text((25, y + 2), name, fill="black", font=getfont(9))
    d2.text((135, y + 2), w, fill="black", font=getfont(9))
    d2.text((245, y + 2), h, fill="black", font=getfont(9))
    d2.text((325, y + 2), b, fill="black", font=getfont(9))
    y += 23

# Buttons
bx = [30, 110, 190, 270]
bt = ["Update", "Delete", "Show Graph", "Exit"]
for i in range(4):
    d2.rectangle([bx[i], 260, bx[i] + 70, 280], fill=COLORS["btn"])
    d2.text((bx[i] + 5, 263), bt[i], fill=COLORS["btn_text"], font=getfont(9))

img2.save(f"{OUT}/screenshot_view_tab.png")
print(f"[OK] {OUT}/screenshot_view_tab.png")


# ============================================================
# Screenshot 3: Weight Trend Graph
# ============================================================
img3 = Image.new("RGB", (550, 480), "white")
d3 = ImageDraw.Draw(img3)
d3.rectangle([0, 0, 550, 30], fill="#2b579a")
d3.text((10, 6), "Weight Trend Graph", fill="white", font=getfont(11))

# Draw axes
d3.line([60, 420, 520, 420], fill="black", width=2)
d3.line([60, 40, 60, 420], fill="black", width=2)

# X-axis labels (dates)
dates = ["May", "Jun", "Jul", "Aug", "Sep"]
for i, dd in enumerate(dates):
    x = 100 + i * 90
    d3.text((x - 10, 425), dd, fill="black", font=getfont(9))
    d3.line([x, 418, x, 422], fill="black")

# Y-axis labels
for i, yy in enumerate(range(50, 90, 5)):
    y = 420 - (yy - 50) * 3
    d3.text((15, y - 6), str(yy), fill="black", font=getfont(9))
    d3.line([58, y, 62, y], fill="black")

# Data points and line
points = [(100, 380), (190, 360), (280, 340), (370, 310), (460, 330)]
for i, (px, py) in enumerate(points):
    d3.ellipse([px - 4, py - 4, px + 4, py + 4], fill="#2ecc71", outline="black")
    if i > 0:
        d3.line([points[i - 1][0], points[i - 1][1], px, py], fill="gray", width=1)

# Title
d3.text((180, 50), "Weight Over Time", fill="black", font=getfont(12, bold=True))
d3.text((180, 68), "Scatter plot showing weight trend by date", fill="#666", font=getfont(9))

img3.save(f"{OUT}/screenshot_graph.png")
print(f"[OK] {OUT}/screenshot_graph.png")


print("\n=== All screenshots generated ===")
