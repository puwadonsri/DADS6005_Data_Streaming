"""
BMI Calculator with MongoDB — Modern GUI
DADS6005 Data Streaming — Quiz 1 (MongoDB)
"""

import os
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mongodb import MongoDBManager

db = MongoDBManager()

# ── Thai Font Support ──────────────────────────────────────

import matplotlib.font_manager as fm

_THAI_FONTS = ["Leelawadee UI", "Tahoma", "Cordia New", "Angsana New", "TH Sarabun New"]
THAI_FONT = "Tahoma"

# Find first available Thai font
for _f in _THAI_FONTS:
    try:
        tk.font.Font(family=_f).measure("ทดสอบ")
        THAI_FONT = _f
        break
    except:
        pass

# Register with matplotlib
for _f in _THAI_FONTS:
    try:
        fm.findfont(_f, fallback_to_default=False)
        THAI_FONT = _f
        plt.rcParams["font.family"] = _f
        break
    except:
        continue

FONT = (THAI_FONT, 10)
FONT_BOLD = (THAI_FONT, 10, "bold")
FONT_TITLE = (THAI_FONT, 14, "bold")
FONT_SMALL = (THAI_FONT, 9)


# ── Color Palette ───────────────────────────────────────────

COLOR_PRIMARY = "#2b579a"
COLOR_SECONDARY = "#4ecdc4"
COLOR_BG = "#f5f6fa"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#2d3436"
COLOR_TEXT_MUTED = "#636e72"
BORDER = "#dfe6e9"
ZONE_COLORS = {
    "red": {"bg": "#ffebee", "fg": "#c62828", "bar": "#ef5350"},
    "orange": {"bg": "#fff3e0", "fg": "#e65100", "bar": "#ff9800"},
    "yellow": {"bg": "#fffde7", "fg": "#f9a825", "bar": "#fdd835"},
    "green": {"bg": "#e8f5e9", "fg": "#2e7d32", "bar": "#66bb6a"},
}


# ── BMI Logic ───────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)


def bmi_category(bmi: float) -> dict:
    if bmi > 30:
        return {
            "key": "red",
            "title": "อ้วนมาก / โรคอ้วนระดับ 3",
            "risk": "มากกว่าคนปกติ",
            "advice": (
                "อ้วนมาก / โรคอ้วนระดับ 3\n\n"
                "ข้อแนะนำ\n"
                "1. ควบคุมอาหาร ลดปริมาณหรือปรับเปลี่ยนอาหารที่ให้พลังงานมาก\n"
                "2. ออกกำลังกายแบบแอโรบิก 40-60 นาทีต่อวัน\n"
                "3. ฝึกความแข็งแรงของกล้ามเนื้อ\n"
                "4. ลดพลังงานจากอาหารลงวันละ 400 กิโลแคลอรี\n"
                "5. ปรึกษาแพทย์หรือผู้เชี่ยวชาญเพื่อวางแผนลดน้ำหนัก"
            ),
        }
    elif bmi >= 25:
        return {
            "key": "orange",
            "title": "อ้วน / โรคอ้วนระดับ 2",
            "risk": "อันตรายระดับ 2",
            "advice": (
                "อ้วน / โรคอ้วนระดับ 2\n\n"
                "ข้อแนะนำ\n"
                "1. ควบคุมอาหาร ลดปริมาณหรือปรับเปลี่ยนอาหาร\n"
                "2. ออกกำลังกาย 40-60 นาทีต่อวัน\n"
                "3. ฝึกความแข็งแรงของกล้ามเนื้อ\n"
                "4. ลดพลังงานจากอาหารลงวันละ 400 กิโลแคลอรี"
            ),
        }
    elif bmi >= 23:
        return {
            "key": "yellow",
            "title": "ท้วม / โรคอ้วนระดับ 1",
            "risk": "อันตรายระดับ 1",
            "advice": (
                "ท้วม / อ้วนระดับ 1\n\n"
                "ข้อแนะนำ\n"
                "1. ควบคุมอาหาร พลังงานไม่ควรต่ำกว่า 1200 กิโลแคลอรี/วัน\n"
                "2. ออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอ"
            ),
        }
    elif bmi >= 18.5:
        return {
            "key": "green",
            "title": "ปกติ (สุขภาพดี)",
            "risk": "เท่าคนปกติ",
            "advice": (
                "น้ำหนักปกติ\n\n"
                "ข้อแนะนำ\n"
                "1. กินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม\n"
                "2. ออกกำลังกายอย่างสม่ำเสมอ 30 นาที/วัน"
            ),
        }
    else:
        return {
            "key": "red",
            "title": "น้ำหนักต่ำกว่าเกณฑ์",
            "risk": "มากกว่าคนปกติ",
            "advice": (
                "น้ำหนักน้อยกว่ามาตรฐาน\n\n"
                "ข้อแนะนำ\n"
                "1. กินอาหารให้หลากหลายครบ 5 หมู่ เพิ่มพลังงานจากไขมัน แป้ง เนื้อสัตว์\n"
                "2. ออกกำลังกายสม่ำเสมอ เช่น เดินเร็ว"
            ),
        }


# ── Graph ───────────────────────────────────────────────────

def show_graph(data: list, parent):
    dates = []
    weights = []
    for doc in data:
        dates.append(doc.get("_date", "?"))
        weights.append(float(doc.get("_weight", 0)))

    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    fig.patch.set_facecolor("#f8f9fa")
    ax.set_facecolor("#ffffff")

    ax.scatter(dates, weights, color="#2ecc71", s=80, zorder=5, edgecolors="#27ae60", linewidth=1.2)
    ax.plot(dates, weights, color="#95e1d3", linewidth=2, linestyle="--", marker="o",
            markersize=8, markerfacecolor="#2ecc71", markeredgecolor="#27ae60")

    ax.set_title("แนวโน้มน้ำหนัก (Weight Trend)", fontfamily=THAI_FONT,
                 fontsize=13, fontweight="bold", color="#2d3436", pad=12)
    ax.set_xlabel("วันที่", fontfamily=THAI_FONT, fontsize=10)
    ax.set_ylabel("น้ำหนัก (kg.)", fontfamily=THAI_FONT, fontsize=10)
    ax.tick_params(axis="x", rotation=35, labelsize=8)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.3)

    win = tk.Toplevel(parent)
    win.title("Weight Trend Graph")
    win.geometry("620x480")
    win.configure(bg="#f8f9fa")
    win.resizable(False, False)

    ttk.Label(win, text="แนวโน้มน้ำหนัก", font=FONT_TITLE,
              background="#f8f9fa").pack(pady=(12, 0))

    canvas = FigureCanvasTkAgg(fig, win)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
    canvas.draw()

    ttk.Button(win, text="ปิด", command=win.destroy).pack(pady=(0, 12))


# ── View Data Tab ───────────────────────────────────────────

def on_tab_switch(event):
    tab_text = event.widget.tab(event.widget.select(), "text")
    if tab_text == "ดูข้อมูล":
        build_view_tab()


def build_view_tab():
    for w in tab2.winfo_children():
        w.destroy()

    header = tk.Frame(tab2, bg=COLOR_CARD)
    header.pack(fill=tk.X, padx=15, pady=(15, 5))
    tk.Label(header, text="ประวัติ BMI ทั้งหมด", font=FONT_TITLE,
             bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w")

    cols = ("#", "Computer", "น้ำหนัก", "ส่วนสูง", "BMI", "วันที่", "_id")
    tree = ttk.Treeview(tab2, columns=cols, show="headings", selectmode="browse")
    tree.column("#", width=35, anchor="center")
    tree.column("Computer", width=150)
    tree.column("น้ำหนัก", width=70, anchor="center")
    tree.column("ส่วนสูง", width=70, anchor="center")
    tree.column("BMI", width=70, anchor="center")
    tree.column("วันที่", width=100, anchor="center")
    tree.column("_id", width=0, stretch=False)

    headings = {"#": "#", "Computer": "Computer Name", "น้ำหนัก": "Weight (kg.)",
                "ส่วนสูง": "Height (cm.)", "BMI": "BMI", "วันที่": "Date", "_id": ""}
    for col, text in headings.items():
        tree.heading(col, text=text)

    records = db.find_all()
    for i, r in enumerate(records, 1):
        tree.insert("", "end", iid=str(i), values=(
            i,
            r.get("_computer_name", ""),
            r.get("_weight", ""),
            r.get("_height", ""),
            r.get("_bmi", ""),
            r.get("_date", ""),
            str(r.get("_id", "")),
        ))
        # Alternating row colors via tag
        tree.tag_configure("even", background="#f8f9fa")
        tree.tag_configure("odd", background=COLOR_CARD)
        tree.item(str(i), tags=("even" if i % 2 == 0 else "odd",))

    # Scrollbar
    vsb = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(fill=tk.BOTH, expand=True, padx=(15, 0), pady=5)
    vsb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=5)

    # Buttons
    btn_frame = tk.Frame(tab2, bg=COLOR_BG)
    btn_frame.pack(pady=(5, 15))

    style = ttk.Style()
    btn_cfg = {"style": "Modern.TButton", "padding": (14, 6)}

    ttk.Button(btn_frame, text="แก้ไข", command=lambda: open_update_page(tree), **btn_cfg).pack(side=tk.LEFT, padx=4)
    ttk.Button(btn_frame, text="ลบ", command=lambda: delete_record(tree), **btn_cfg).pack(side=tk.LEFT, padx=4)
    ttk.Button(btn_frame, text="กราฟ", command=lambda: show_graph(records, root), **btn_cfg).pack(side=tk.LEFT, padx=4)
    ttk.Button(btn_frame, text="ออก", command=root.destroy, **btn_cfg).pack(side=tk.LEFT, padx=4)


def get_selected_id(tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Warning", "กรุณาเลือก record ที่ต้องการ")
        return None
    return tree.item(sel[0])["values"][6]


def delete_record(tree):
    doc_id = get_selected_id(tree)
    if not doc_id:
        return
    if messagebox.askyesno("ยืนยัน", "ต้องการลบ record นี้ใช่หรือไม่?"):
        db.delete_by_id(doc_id)
        messagebox.showinfo("สำเร็จ", "ลบ record เรียบร้อย")
        build_view_tab()


# ── Update Page ─────────────────────────────────────────────

def open_update_page(tree):
    doc_id = get_selected_id(tree)
    if not doc_id:
        return

    sel = tree.selection()[0]
    vals = tree.item(sel)["values"]
    old_weight, old_height = vals[2], vals[3]

    win = tk.Toplevel(root)
    win.title("แก้ไขข้อมูล BMI")
    win.geometry("480+%d+%d" % (root.winfo_x() + 60, root.winfo_y() + 60))
    win.configure(bg=COLOR_BG)
    win.resizable(False, False)

    card = tk.Frame(win, bg=COLOR_CARD, highlightbackground=BORDER, highlightthickness=1)
    card.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    tk.Label(card, text="อัพเดตค่าดัชนีมวลกาย", font=FONT_TITLE,
             bg=COLOR_CARD, fg=COLOR_TEXT).pack(pady=(15, 15))

    fields = tk.Frame(card, bg=COLOR_CARD)
    fields.pack(pady=10)

    tk.Label(fields, text=f"น้ำหนักตัว (กก.) :   เดิม {old_weight} kg.",
             font=FONT, bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    weight_ent = ttk.Entry(fields, font=FONT, width=15)
    weight_ent.grid(row=0, column=1, padx=10, pady=8)
    weight_ent.insert(0, old_weight)

    tk.Label(fields, text=f"ส่วนสูง (ซม.) :   เดิม {old_height} cm.",
             font=FONT, bg=COLOR_CARD, fg=COLOR_TEXT).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    height_ent = ttk.Entry(fields, font=FONT, width=15)
    height_ent.grid(row=1, column=1, padx=10, pady=8)
    height_ent.insert(0, old_height)

    # Result area
    result_frame = tk.Frame(win, bg=COLOR_BG)
    result_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 10))
    result_label = tk.Label(result_frame, text="", font=FONT, bg=COLOR_BG,
                            wraplength=400, justify="left")
    result_label.pack(fill=tk.BOTH)

    def do_update():
        try:
            w = float(weight_ent.get())
            h = float(height_ent.get())
        except ValueError:
            messagebox.showwarning("Error", "กรุณากรอกเฉพาะตัวเลข")
            return
        bmi = calculate_bmi(w, h)
        cat = bmi_category(bmi)
        z = ZONE_COLORS[cat["key"]]
        result_label.config(
            text=f"BMI = {bmi} | {cat['title']}\n\n{cat['advice']}",
            bg=z["bg"], fg=z["fg"]
        )
        db.replace_one(doc_id, os.environ["COMPUTERNAME"], w, h, bmi)
        messagebox.showinfo("สำเร็จ", "อัพเดตข้อมูลเรียบร้อย")

    btn_upd = tk.Frame(win, bg=COLOR_BG)
    btn_upd.pack(pady=(0, 15))
    ttk.Button(btn_upd, text="บันทึก", command=do_update, padding=(14, 6)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_upd, text="ยกเลิก", command=win.destroy, padding=(14, 6)).pack(side=tk.LEFT, padx=5)


# ── BMI Tab ─────────────────────────────────────────────────

def calculate_and_save():
    try:
        w = float(weight_entry.get())
        h = float(height_entry.get())
    except ValueError:
        messagebox.showwarning("ข้อผิดพลาด", "กรุณากรอกน้ำหนักและส่วนสูงเป็นตัวเลข")
        result_card.configure(bg=COLOR_CARD)
        result_title.config(text="")
        result_advice.config(text="")
        progress_bar.config(value=0)
        return

    bmi = calculate_bmi(w, h)
    cat = bmi_category(bmi)
    z = ZONE_COLORS[cat["key"]]

    result_card.configure(bg=z["bg"])
    result_title.config(
        text=f"BMI = {bmi}    |    {cat['title']}    |    ความเสี่ยง: {cat['risk']}",
        bg=z["bg"], fg=z["fg"]
    )
    result_advice.config(text=cat["advice"], bg=z["bg"], fg=z["fg"])

    # Animate progress bar based on BMI
    bmi_pct = min(bmi / 40 * 100, 100)
    progress_bar.config(value=bmi_pct)

    db.insert_doc(os.environ["COMPUTERNAME"], w, h, bmi)


def clear_inputs():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_card.configure(bg=COLOR_CARD)
    result_title.config(text="")
    result_advice.config(text="")
    progress_bar.config(value=0)


# ── Style Setup ─────────────────────────────────────────────

def setup_styles():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        style.theme_use("default")

    style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
    style.configure("TNotebook.Tab", font=FONT, padding=(18, 6),
                    background="#e0e0e0", foreground=COLOR_TEXT)
    style.map("TNotebook.Tab", background=[("selected", COLOR_CARD)],
              foreground=[("selected", COLOR_PRIMARY)])

    style.configure("TLabel", font=FONT, background=COLOR_BG, foreground=COLOR_TEXT)
    style.configure("TButton", font=FONT, padding=(12, 5))
    style.configure("TEntry", font=FONT, fieldbackground=COLOR_CARD)

    style.configure("Treeview", font=FONT_SMALL, rowheight=26, fieldbackground=COLOR_CARD)
    style.configure("Treeview.Heading", font=FONT_BOLD, background=COLOR_SECONDARY,
                    foreground="white")
    style.map("Treeview.Heading", background=[("active", "#3dbdb5")])

    style.configure("TLabelframe", font=FONT_BOLD, background=COLOR_CARD, foreground=COLOR_TEXT)
    style.configure("TLabelframe.Label", font=FONT_BOLD, foreground=COLOR_TEXT)

    style.configure("Modern.TButton", font=FONT, padding=(14, 6))


# ── Main GUI ────────────────────────────────────────────────

def main():
    global root, tab2, weight_entry, height_entry, result_card
    global result_title, result_advice, progress_bar

    root = tk.Tk()
    root.title("BMI Calculator with MongoDB — DADS6005")
    root.configure(bg=COLOR_BG)
    root.geometry("640x580")
    root.minsize(580, 520)

    setup_styles()

    tab_ctrl = ttk.Notebook(root)
    tab1 = tk.Frame(tab_ctrl, bg=COLOR_CARD)
    tab2 = tk.Frame(tab_ctrl, bg=COLOR_BG)
    tab_ctrl.add(tab1, text="BMI")
    tab_ctrl.add(tab2, text="ดูข้อมูล")
    tab_ctrl.bind("<ButtonRelease-1>", on_tab_switch)
    tab_ctrl.pack(expand=True, fill="both", padx=8, pady=8)

    # ════════════════════════════════════════════════
    # Tab 1 — BMI Calculator
    # ════════════════════════════════════════════════

    # Header
    header = tk.Frame(tab1, bg=COLOR_CARD)
    header.pack(fill=tk.X, padx=20, pady=(20, 5))
    tk.Label(header, text="เครื่องคำนวณดัชนีมวลกาย (BMI)", font=FONT_TITLE,
             bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w")
    tk.Label(header, text="คำนวณ BMI และรับคำแนะนำสุขภาพ พร้อมบันทึกข้อมูลลง MongoDB",
             font=("Leelawadee UI", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED).pack(anchor="w")

    # Input card
    input_card = tk.Frame(tab1, bg=COLOR_CARD, highlightbackground=BORDER, highlightthickness=1)
    input_card.pack(padx=20, pady=12, fill=tk.X)

    tk.Label(input_card, text="ข้อมูลร่างกาย", font=FONT_BOLD,
             bg=COLOR_CARD, fg=COLOR_TEXT).pack(pady=(10, 0))

    fields_row = tk.Frame(input_card, bg=COLOR_CARD)
    fields_row.pack(pady=12)

    # Weight
    w_frame = tk.Frame(fields_row, bg=COLOR_CARD)
    w_frame.pack(side=tk.LEFT, padx=15)
    tk.Label(w_frame, text="น้ำหนักตัว (kg.)", font=FONT,
             bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w")
    weight_entry = ttk.Entry(w_frame, font=FONT, width=18, justify="center")
    weight_entry.pack(pady=(4, 0))
    weight_entry.insert(0, "")

    # Height
    h_frame = tk.Frame(fields_row, bg=COLOR_CARD)
    h_frame.pack(side=tk.LEFT, padx=15)
    tk.Label(h_frame, text="ส่วนสูง (cm.)", font=FONT,
             bg=COLOR_CARD, fg=COLOR_TEXT).pack(anchor="w")
    height_entry = ttk.Entry(h_frame, font=FONT, width=18, justify="center")
    height_entry.pack(pady=(4, 0))
    height_entry.insert(0, "")

    # Buttons
    btn_row = tk.Frame(input_card, bg=COLOR_CARD)
    btn_row.pack(pady=(5, 12))
    ttk.Button(btn_row, text="คำนวณ & บันทึก", command=calculate_and_save,
               padding=(16, 7), style="Modern.TButton").pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_row, text="ล้าง", command=clear_inputs,
               padding=(16, 7), style="Modern.TButton").pack(side=tk.LEFT, padx=5)

    # Progress bar (BMI gauge)
    progress_frame = tk.Frame(tab1, bg=COLOR_BG)
    progress_frame.pack(fill=tk.X, padx=20, pady=(5, 0))
    tk.Label(progress_frame, text="BMI Index", font=FONT_SMALL,
             bg=COLOR_BG, fg=COLOR_TEXT_MUTED).pack(anchor="w")
    progress_bar = ttk.Progressbar(progress_frame, length=500, mode="determinate", value=0)
    progress_bar.pack(fill=tk.X, pady=(2, 0))

    # Result card
    result_card = tk.Frame(tab1, bg=COLOR_CARD, highlightbackground=BORDER, highlightthickness=1)
    result_card.pack(padx=20, pady=12, fill=tk.BOTH, expand=True)

    result_title = tk.Label(result_card, text="", font=FONT_BOLD,
                            bg=COLOR_CARD, fg=COLOR_TEXT, wraplength=550)
    result_title.pack(pady=(14, 6), padx=15)

    result_advice = tk.Label(result_card, text="", font=FONT,
                             bg=COLOR_CARD, fg=COLOR_TEXT,
                             wraplength=550, justify="left")
    result_advice.pack(pady=(0, 14), padx=15)

    root.mainloop()
    db.close()


if __name__ == "__main__":
    main()
