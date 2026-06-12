"""
BMI Calculator with MongoDB Storage
DADS6005 Data Streaming — Quiz 1 (MongoDB)
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mongodb import MongoDBManager

db = MongoDBManager()


# ─── BMI Logic ──────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)


def bmi_category(bmi: float) -> dict:
    if bmi > 30:
        return {
            "zone": "red",
            "title": "อ้วนมาก / โรคอ้วนระดับ 3",
            "risk": "มากกว่าคนปกติ",
            "advice": (
                "อ้วนมาก / โรคอ้วนระดับ 3\n"
                "คุณอ้วนมากแล้ว (อ้วนระดับ 3)\n\n"
                "ข้อแนะนำ\n"
                "1. ควรควบคุมอาหารโดยลดปริมาณอาหารหรือปรับเปลี่ยนอาหาร\n"
                "2. ควรเคลื่อนไหวและออกกำลังกายแบบแอโรบิก 40-60 นาทีต่อวัน\n"
                "3. ควรฝึกความแข็งแรงของกล้ามเนื้อ\n"
                "4. ลดพลังงานจากอาหารลงได้วันละ 400 กิโลแคลอรี\n"
                "5. ควรปรึกษาแพทย์หรือผู้เชี่ยวชาญในการลดน้ำหนัก\n"
            ),
        }
    elif bmi >= 25:
        return {
            "zone": "orange",
            "title": "อ้วน / โรคอ้วนระดับ 2",
            "risk": "อันตรายระดับ 2",
            "advice": (
                "อ้วน / โรคอ้วนระดับ 2\n"
                f"ค่าดัชนีมวลกายของคุณอยู่ระหว่าง 25 - 29.90\n\n"
                "ข้อแนะนำ\n"
                "1. ควบคุมอาหาร ลดปริมาณหรือปรับเปลี่ยนอาหาร\n"
                "2. ออกกำลังกาย 40-60 นาทีต่อวัน\n"
                "3. ฝึกความแข็งแรงของกล้ามเนื้อ\n"
                "4. ลดพลังงานเข้าจากอาหารวันละ 400 กิโลแคลอรี\n"
            ),
        }
    elif bmi >= 23:
        return {
            "zone": "yellow",
            "title": "ท้วม / โรคอ้วนระดับ 1",
            "risk": "อันตรายระดับ 1",
            "advice": (
                "ท้วม / อ้วนระดับ 1\n"
                f"ค่าดัชนีมวลกายของคุณอยู่ระหว่าง 23 - 24.90\n\n"
                "ข้อแนะนำ\n"
                "1. ควบคุมอาหาร พลังงานไม่ควรต่ำกว่า 1200 กิโลแคลอรี/วัน\n"
                "2. ออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอ\n"
            ),
        }
    elif bmi >= 18.5:
        return {
            "zone": "green",
            "title": "ปกติ (สุขภาพดี)",
            "risk": "เท่าคนปกติ",
            "advice": (
                "น้ำหนักปกติ\n"
                f"ค่าดัชนีมวลกายของคุณอยู่ระหว่าง 18.50 - 22.90\n\n"
                "ข้อแนะนำ\n"
                "1. กินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม\n"
                "2. ออกกำลังกายอย่างสม่ำเสมออย่างน้อย 30 นาที/วัน\n"
            ),
        }
    else:
        return {
            "zone": "red",
            "title": "น้ำหนักต่ำกว่าเกณฑ์",
            "risk": "มากกว่าคนปกติ",
            "advice": (
                "น้ำหนักน้อยกว่ามาตรฐาน\n"
                f"ค่าดัชนีมวลกายของคุณน้อยกว่า 18.50\n\n"
                "ข้อแนะนำ\n"
                "1. กินอาหารให้หลากหลายครบ 5 หมู่ เพิ่มพลังงาน เช่น ไขมัน แป้ง เนื้อสัตว์\n"
                "2. ออกกำลังกายอย่างสม่ำเสมอ เช่น เดินเร็ว\n"
            ),
        }


# ─── Graph ──────────────────────────────────────────────────

def show_graph(data: list, parent):
    months = []
    weights = []
    for doc in data:
        months.append(doc.get("_date", "?"))
        weights.append(float(doc.get("_weight", 0)))

    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.scatter(months, weights, color="g", s=60)
    ax.plot(months, weights, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("Weight Over Time")
    ax.tick_params(axis="x", rotation=45)

    win = tk.Toplevel(parent)
    win.title("Weight Trend Graph")
    canvas = FigureCanvasTkAgg(fig, win)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()


# ─── View Data Tab ──────────────────────────────────────────

def on_tab_switch(event):
    tab_text = event.widget.tab(event.widget.select(), "text")
    if tab_text == "View Data":
        build_view_tab()


def build_view_tab():
    for w in tab2.winfo_children():
        w.destroy()

    tk.Label(tab2, text="BMI Data", font=("Tahoma", 16)).pack(pady=10)

    cols = ("Computer Name", "Weight", "Height", "BMI", "_id")
    tree = ttk.Treeview(tab2, columns=cols, show="headings", selectmode="browse")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col != "_id" else 200)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    records = db.find_all()
    for r in records:
        tree.insert(
            "", "end",
            values=(
                r.get("_computer_name", ""),
                r.get("_weight", ""),
                r.get("_height", ""),
                r.get("_bmi", ""),
                str(r.get("_id", "")),
            ),
        )

    btn_frame = tk.Frame(tab2)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Update", command=lambda: open_update_page(tree)).pack(
        side=tk.LEFT, padx=5
    )
    tk.Button(btn_frame, text="Delete", command=lambda: delete_record(tree)).pack(
        side=tk.LEFT, padx=5
    )
    tk.Button(
        btn_frame, text="Show Graph", command=lambda: show_graph(records, root)
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Exit", command=root.destroy).pack(
        side=tk.LEFT, padx=5
    )


def get_selected_id(tree):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Warning", "กรุณาเลือก record ที่ต้องการ")
        return None
    return tree.item(sel[0])["values"][4]


def delete_record(tree):
    doc_id = get_selected_id(tree)
    if not doc_id:
        return
    if messagebox.askyesno("Confirm", "ลบ record นี้?"):
        db.delete_by_id(doc_id)
        messagebox.showinfo("Success", "ลบเรียบร้อย")
        build_view_tab()


# ─── Update Page ────────────────────────────────────────────

def open_update_page(tree):
    doc_id = get_selected_id(tree)
    if not doc_id:
        return

    sel = tree.selection()[0]
    old_weight = tree.item(sel)["values"][1]
    old_height = tree.item(sel)["values"][2]

    win = tk.Toplevel(root)
    win.title("Update BMI Record")

    frame = ttk.LabelFrame(win, text="อัพเดตค่าดัชนีมวลกาย")
    frame.pack(padx=30, pady=30)

    ttk.Label(frame, text=f"น้ำหนักตัว (kg.) :   เดิม {old_weight} kg.").grid(
        row=0, column=0, padx=10, pady=10
    )
    weight_ent = ttk.Entry(frame)
    weight_ent.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame, text=f"ส่วนสูง (cm.) :   เดิม {old_height} cm.").grid(
        row=1, column=0, padx=10, pady=10
    )
    height_ent = ttk.Entry(frame)
    height_ent.grid(row=1, column=1, padx=10, pady=10)

    result_label = ttk.Label(win, text="")
    result_label.pack()
    advice_label = ttk.Label(win, text="", wraplength=400, justify="left")
    advice_label.pack(padx=20, pady=10)

    def do_update():
        try:
            w = float(weight_ent.get())
            h = float(height_ent.get())
        except ValueError:
            messagebox.showwarning("Error", "กรุณากรอกตัวเลขเท่านั้น")
            return
        bmi = calculate_bmi(w, h)
        cat = bmi_category(bmi)
        result_label.config(
            text=f"\nBMI : {bmi}\n{cat['title']}\n{cat['risk']}\n",
            background=cat["zone"],
        )
        advice_label.config(text=cat["advice"])
        db.replace_one(doc_id, os.environ["COMPUTERNAME"], w, h, bmi)
        messagebox.showinfo("Success", "อัพเดตเรียบร้อย")

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Update", command=do_update).pack(
        side=tk.LEFT, padx=5
    )
    tk.Button(btn_frame, text="Close", command=win.destroy).pack(
        side=tk.LEFT, padx=5
    )


# ─── BMI Tab ────────────────────────────────────────────────

def calculate_and_save():
    try:
        w = float(weight_entry.get())
        h = float(height_entry.get())
    except ValueError:
        messagebox.showwarning("Error", "กรุณากรอกน้ำหนักและส่วนสูงเป็นตัวเลข")
        show_data.config(text="")
        show_desc.config(text="")
        return

    bmi = calculate_bmi(w, h)
    cat = bmi_category(bmi)
    show_data.config(
        text=f"\nBMI : {bmi}\n{cat['title']}\n{cat['risk']}\n",
        background=cat["zone"],
    )
    show_desc.config(text=cat["advice"])
    db.insert_doc(os.environ["COMPUTERNAME"], w, h, bmi)


def clear_inputs():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    show_data.config(text="", background="")
    show_desc.config(text="")


# ─── Main GUI ───────────────────────────────────────────────

def main():
    global root, tab2, weight_entry, height_entry, show_data, show_desc

    root = tk.Tk()
    root.title("BMI Calculator with MongoDB")
    root.geometry("600x550")

    tab_ctrl = ttk.Notebook(root)
    tab1 = ttk.Frame(tab_ctrl)
    tab2 = ttk.Frame(tab_ctrl)

    s = ttk.Style()
    s.theme_use("default")
    tab_ctrl.add(tab1, text="BMI")
    tab_ctrl.add(tab2, text="View Data")
    tab_ctrl.bind("<ButtonRelease-1>", on_tab_switch)
    tab_ctrl.pack(expand=True, fill="both")

    # ── Tab 1: BMI Calculator ──
    frame = ttk.LabelFrame(tab1, text="คำนวณค่าดัชนีมวลกาย (BMI)")
    frame.pack(pady=30, padx=35)

    ttk.Label(frame, text="น้ำหนักตัว (kg.) :").grid(row=0, column=0, padx=10, pady=10)
    weight_entry = ttk.Entry(frame)
    weight_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(frame, text="ส่วนสูง (cm.) :").grid(row=1, column=0, padx=10, pady=10)
    height_entry = ttk.Entry(frame)
    height_entry.grid(row=1, column=1, padx=10, pady=10)

    btn_frame = tk.Frame(frame)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
    ttk.Button(btn_frame, text="Calculate & Save", command=calculate_and_save).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(btn_frame, text="Clear", command=clear_inputs).pack(
        side=tk.LEFT, padx=5
    )

    show_data = ttk.Label(tab1, text="", font=("Tahoma", 11))
    show_data.pack(pady=5)
    show_desc = ttk.Label(tab1, text="", wraplength=500, justify="left")
    show_desc.pack(padx=20, pady=5)

    root.mainloop()
    db.close()


if __name__ == "__main__":
    main()
