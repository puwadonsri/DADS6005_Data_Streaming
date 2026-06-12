"""
BMI Calculator with MongoDB — Flet GUI
DADS6005 Data Streaming — Quiz 1 (MongoDB)
"""

import os
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import flet as ft
from mongodb import MongoDBManager

db = MongoDBManager()

# ── Matplotlib Thai font ────────────────────────────────────

import matplotlib.font_manager as fm
for _f in ["Leelawadee UI", "Tahoma", "Cordia New", "Angsana New"]:
    try:
        fm.findfont(_f, fallback_to_default=False)
        plt.rcParams["font.family"] = _f
        break
    except:
        continue

# ── BMI Logic ───────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    return round(weight_kg / ((height_cm / 100) ** 2), 2)


def bmi_category(bmi: float) -> dict:
    if bmi > 30:
        return {"color": ft.Colors.RED_100, "text_color": ft.Colors.RED_900,
                "title": "อ้วนมาก / โรคอ้วนระดับ 3",
                "risk": "มากกว่าคนปกติ",
                "advice": "1. ควบคุมอาหาร ลดปริมาณอาหารที่ให้พลังงานมาก\n2. ออกกำลังกาย 40-60 นาที/วัน\n3. ฝึกความแข็งแรงของกล้ามเนื้อ\n4. ลดพลังงานวันละ 400 กิโลแคลอรี\n5. ปรึกษาแพทย์"}
    elif bmi >= 25:
        return {"color": ft.Colors.ORANGE_100, "text_color": ft.Colors.ORANGE_900,
                "title": "อ้วน / โรคอ้วนระดับ 2",
                "risk": "อันตรายระดับ 2",
                "advice": "1. ควบคุมอาหาร ลดปริมาณหรือปรับเปลี่ยนอาหาร\n2. ออกกำลังกาย 40-60 นาที/วัน\n3. ฝึกความแข็งแรงของกล้ามเนื้อ"}
    elif bmi >= 23:
        return {"color": ft.Colors.YELLOW_100, "text_color": ft.Colors.YELLOW_900,
                "title": "ท้วม / โรคอ้วนระดับ 1",
                "risk": "อันตรายระดับ 1",
                "advice": "1. ควบคุมอาหาร พลังงานไม่ต่ำกว่า 1200 กิโลแคลอรี/วัน\n2. ออกกำลังกายสม่ำเสมอ"}
    elif bmi >= 18.5:
        return {"color": ft.Colors.GREEN_100, "text_color": ft.Colors.GREEN_900,
                "title": "ปกติ (สุขภาพดี)",
                "risk": "เท่าคนปกติ",
                "advice": "1. กินอาหารครบ 5 หมู่ในสัดส่วนเหมาะสม\n2. ออกกำลังกาย 30 นาที/วัน"}
    else:
        return {"color": ft.Colors.RED_100, "text_color": ft.Colors.RED_900,
                "title": "น้ำหนักต่ำกว่าเกณฑ์",
                "risk": "มากกว่าคนปกติ",
                "advice": "1. กินอาหารให้ครบ 5 หมู่ เพิ่มพลังงาน\n2. ออกกำลังกายสม่ำเสมอ"}


# ── Flet App ────────────────────────────────────────────────

def main(page: ft.Page):
    page.title = "BMI Calculator with MongoDB — DADS6005"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.scroll = ft.ScrollMode.AUTO
    page.window.width = 680
    page.window.height = 680
    page.window.min_width = 560
    page.window.min_height = 520

    # ── Tab 1: BMI Calculator ──
    weight_field = ft.TextField(label="น้ำหนักตัว (kg.)", width=200, text_align=ft.TextAlign.CENTER)
    height_field = ft.TextField(label="ส่วนสูง (cm.)", width=200, text_align=ft.TextAlign.CENTER)

    bmi_result = ft.Container(
        content=ft.Column([
            ft.Text("", size=16, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Text("", size=20, weight=ft.FontWeight.BOLD, selectable=True),
            ft.Text("", size=13, selectable=True),
        ]),
        padding=20, border_radius=12, visible=False,
    )

    def on_calculate(e):
        try:
            w = float(weight_field.value)
            h = float(height_field.value)
        except (TypeError, ValueError):
            page.snack_bar = ft.SnackBar(ft.Text("กรุณากรอกน้ำหนักและส่วนสูงเป็นตัวเลข"))
            page.snack_bar.open = True
            page.update()
            return

        bmi = calculate_bmi(w, h)
        cat = bmi_category(bmi)
        comp = bmi_result.content
        comp.controls[0].value = f"BMI = {bmi}"
        comp.controls[1].value = f"{cat['title']} (ความเสี่ยง: {cat['risk']})"
        comp.controls[2].value = f"ข้อแนะนำ:\n{cat['advice']}"
        bmi_result.bgcolor = cat["color"]
        bmi_result.visible = True
        db.insert_doc(os.environ["COMPUTERNAME"], w, h, bmi)
        page.update()

    def on_clear(e):
        weight_field.value = ""
        height_field.value = ""
        bmi_result.visible = False
        page.update()

    bmi_tab = ft.Column([
        ft.Text("เครื่องคำนวณดัชนีมวลกาย (BMI)", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("คำนวณ BMI พร้อมคำแนะนำสุขภาพ และบันทึกข้อมูลลง MongoDB",
                size=12, color=ft.Colors.GREY_600),
        ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
        ft.Row([weight_field, height_field], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        ft.Row([
            ft.FilledButton("คำนวณ & บันทึก", icon=ft.Icons.CALCULATE, on_click=on_calculate),
            ft.OutlinedButton("ล้าง", icon=ft.Icons.CLEAR, on_click=on_clear),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        bmi_result,
    ], scroll=ft.ScrollMode.AUTO)

    # ── Tab 2: View Data ──
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Computer", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("น้ำหนัก", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("ส่วนสูง", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("BMI", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("วันที่", weight=ft.FontWeight.BOLD)),
        ],
        column_spacing=20, width=600,
    )

    def refresh_table():
        rows = []
        for i, doc in enumerate(db.find_all(), 1):
            bmi_val = float(doc.get("_bmi", 0))
            bmi_color = ft.Colors.GREEN_700 if bmi_val < 24 else (
                ft.Colors.RED_700 if bmi_val > 30 else ft.Colors.ORANGE_700)
            rows.append(ft.DataRow([
                ft.DataCell(ft.Text(str(i))),
                ft.DataCell(ft.Text(doc.get("_computer_name", ""))),
                ft.DataCell(ft.Text(str(doc.get("_weight", "")))),
                ft.DataCell(ft.Text(str(doc.get("_height", "")))),
                ft.DataCell(ft.Text(str(bmi_val), color=bmi_color, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(doc.get("_date", ""))),
            ]))
        data_table.rows = rows
        page.update()

    def on_tab_change(e):
        if e.control.selected_index == 1:
            refresh_table()

    def delete_selected(e):
        sel = [r for r in data_table.rows if r.selected]
        if not sel:
            page.snack_bar = ft.SnackBar(ft.Text("กรุณาเลือก record ที่ต้องการลบ"))
            page.snack_bar.open = True
            page.update()
            return
        for r in sel:
            doc_id = r.cells[0].content.value
            record = db.find_all()[int(doc_id) - 1]
            db.delete_by_id(str(record["_id"]))
        refresh_table()
        page.snack_bar = ft.SnackBar(ft.Text("ลบเรียบร้อย"))
        page.snack_bar.open = True
        page.update()

    def show_graph(e):
        records = db.find_all()
        if not records:
            page.snack_bar = ft.SnackBar(ft.Text("ไม่มีข้อมูล"))
            page.snack_bar.open = True
            page.update()
            return

        dates = [r.get("_date", "?") for r in records]
        weights = [float(r.get("_weight", 0)) for r in records]

        fig, ax = plt.subplots(figsize=(6, 3.5))
        fig.patch.set_facecolor("#f8f9fa")
        ax.set_facecolor("white")
        ax.scatter(dates, weights, color="#2ecc71", s=80, edgecolors="#27ae60", linewidth=1.2, zorder=5)
        ax.plot(dates, weights, color="#95e1d3", linewidth=2, linestyle="--",
                marker="o", markersize=8, markerfacecolor="#2ecc71", markeredgecolor="#27ae60")
        ax.set_title("แนวโน้มน้ำหนัก (Weight Trend)", fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("วันที่", fontsize=10)
        ax.set_ylabel("น้ำหนัก (kg.)", fontsize=10)
        ax.tick_params(axis="x", rotation=30, labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()

        buf = io.BytesIO()
        FigureCanvasAgg(fig).print_png(buf)
        img = ft.Image(src_base64=ft.Base64String(buf.getvalue()), fit=ft.ImageFit.CONTAIN)
        plt.close(fig)

        dlg = ft.AlertDialog(
            title=ft.Text("แนวโน้มน้ำหนัก"),
            content=ft.Container(img, width=620, height=400),
            actions=[ft.TextButton("ปิด", on_click=lambda e: close_dlg(dlg))],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    view_tab = ft.Column([
        ft.Text("ประวัติ BMI ทั้งหมด", size=20, weight=ft.FontWeight.BOLD),
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        ft.Container(data_table, padding=10, bgcolor=ft.Colors.WHITE,
                     border_radius=12, shadow=ft.BoxShadow(1, 1, ft.Colors.BLACK12)),
        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
        ft.Row([
            ft.FilledButton("ลบ", icon=ft.Icons.DELETE, on_click=delete_selected),
            ft.FilledTonalButton("กราฟ", icon=ft.Icons.SHOW_CHART, on_click=show_graph),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
    ], scroll=ft.ScrollMode.AUTO)

    # ── Build app ──
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        on_change=on_tab_change,
        tabs=[
            ft.Tab(text="BMI", icon=ft.Icons.CALCULATE, content=bmi_tab),
            ft.Tab(text="ดูข้อมูล", icon=ft.Icons.TABLE_CHART, content=view_tab),
        ],
        expand=True,
    )

    page.add(tabs)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
