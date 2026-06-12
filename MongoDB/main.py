# coding=utf8
import tkinter as tk					
from tkinter import ttk,messagebox
import os, sys
from mongodb import insert_doc,find_all_people,delete_doc_by_id,replace_one
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date

def graph(_data):
  
    print(_data)
    lists1 = []
    lists2 = []

    for x in _data:
        tmp = list(x.values())
        print(tmp)
        lists1.append(tmp[5])
        lists2.append(tmp[2])
    
    print(lists1,lists2)
   
    data3 = { 'Month': lists1,
               'Weight': lists2
         }
    df3 = pd.DataFrame(data3)

    figure3 = plt.Figure(figsize=(5, 4), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax3.scatter(df3['Month'], df3['Weight'], color='g')
    scatter3 = FigureCanvasTkAgg(figure3, root)
    scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax3.legend(['Month'])
    ax3.set_xlabel('Month')
    ax3.set_title('Month Vs. Weight')
    root.mainloop()

def delete(_id):
    selected_item = _id.selection()[0]
    print(_id.item(selected_item)['values'][4])
    delete_doc_by_id(_id.item(selected_item)['values'][4])
    messagebox.showinfo("Success","Bmi record deleted")
    root.config()

def update(_id):
    selected_item = _id.selection()[0]  
    updatepage(_id.item(selected_item)['values'][0],_id.item(selected_item)['values'][1],_id.item(selected_item)['values'][2],_id.item(selected_item)['values'][3],_id.item(selected_item)['values'][4])

  
def clearToTextInput():
    tk.Entry.delete("1.0","end")

def fTabSwitched(event):
        global tabControl
        l_tabText = tabControl.tab(tabControl.select(), "text")
        if (l_tabText == 'View Data'):
            label = tk.Label(tab2, text="BMI Data", font=("Kanit",20)).grid(row=0, columnspan=2)
            # create Treeview with 3 columns
            cols = ('Computer Name','Weight','Height','BMI')
            listBox = ttk.Treeview(tab2, columns=cols, show='headings')
            # set column headings
            for col in cols:
                listBox.heading(col, text=col)    
            listBox.grid(row=1, column=0, columnspan=2)

            tempList = find_all_people()
            for x in tempList:
                tmp = list(x.values())
                listBox.insert("", "end", values=(tmp[1],tmp[2],tmp[3],tmp[4],tmp[0]))
                  
            b2 = tk.Button(tab2, text='Update',command=lambda: update(listBox)).grid(row=4, column=0,sticky="news", padx=5, pady=5)
            b1 = tk.Button(tab2, text='Delete',command=lambda: delete(listBox)).grid(row=4, column=1,sticky="news", padx=5, pady=5)
            b3 = tk.Button(tab2, text="Show Graph", command=lambda: graph(tempList)).grid(row=5, columnspan=2,sticky="news", padx=5, pady=5)
            closeButton = tk.Button(tab2, text="Exit", command=exit).grid(row=6, columnspan=2,sticky="news", padx=5, pady=5)
        
        
def find_bmi():
    weight = weight_entry.get()
    height = height_entry.get()
    h = height_entry.get()
    # check height and weight filled in
    if height and weight and h:
        height = float(height) / 100.0
        bmi = round(float(weight) / height ** 2, 2)
        print(f"h : {height}\nw : {weight}\nbmi : {bmi}\ncomputer name : {os.environ['COMPUTERNAME']}")
        if bmi > 30:
            color_zone = "red"
            texts1 = "อยู่ในเกณท์ : อ้วนมาก / โรคอ้วนระดับ 3"
            texts2 = "ภาวะเสี่ยงต่อโรค : มากกว่าคนปกติ"
            description = "อ้วนมาก / โรคอ้วนระดับ 3\nคุณ อ้วนมากแล้ว (อ้วนระดับ 3) โดยทั่วไปค่าดัชนีมวลกายปกติมีค่ามากกว่า 30\n\nข้อแนะนำ\n1. ควรควบคุมอาหารโดยลดปริมาณอาหารหรือปรับเปลี่ยนอาหารจากที่ให้พลังงานมากเป็นอาหารที่ให้พลังงานน้อย\n2. ควรเคลื่อนไหวและออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอทุกวัน 40-60 นาทีต่อวัน\n3. ควรฝึกความแข็งแรงของกล้ามเนื้อ ด้วยการฝึกกายบริหารหรือยกน้ำหนัก\n4. ถ้าคุณสามารถลดพลังงานเข้าจากอาหารลงได้วันละ 400 กิโลแคลอรี\n5. ควรปรึกษาแพทย์หรือผู้เชี่ยวชาญในการลดและควบคุมน้ำหนัก\n\n"
        elif bmi >= 25 and bmi <= 29.90:
            color_zone = "orange"
            texts1 = "อยู่ในเกณท์ : อ้วน / โรคอ้วนระดับ 2"
            texts2 = "ภาวะเสี่ยงต่อโรค : อันตรายระดับ 2"
            description = "อ้วน / โรคอ้วนระดับ 2\nคุณ อ้วนแล้ว (อ้วนระดับ 2) โดยทั่วไปค่าดัชนีมวลกายปกติมีค่าระหว่าง 25 - 29.90\n\nข้อแนะนำ\n1. ควรควบคุมอาหารโดยลดปริมาณอาหารหรือปรับเปลี่ยนอาหารจากที่ให้พลังงานมากเป็นอาหารที่ให้พลังงานน้อย\n2. ควรเคลื่อนไหวและออกกำลังกายประมาณ 40-60 นาทีต่อวัน\n3. ควรฝึกความแข็งแรงของกล้ามเนื้อ\n4. ถ้าคุณสามารถลดพลังงานเข้าจากอาหารลงได้วันละ 400 กิโลแคลอรี และเพิ่มการใช้พลังงาน\n\n"
        elif bmi >= 23 and bmi <= 24.90:
            color_zone = "yellow"
            texts1 = "อยู่ในเกณท์ : ท้วม / โรคอ้วนระดับ 1"
            texts2 = "ภาวะเสี่ยงต่อโรค : อันตรายระดับ 1"
            description = "ท้วม / อ้วนระดับ 1\nคุณมี น้ำหนักเกิน หรือรูปร่างท้วม โดยทั่วไปค่าดัชนีมวลกายปกติมีค่าระหว่าง 23 - 24.90\n\nข้อแนะนำ\n1. ควรควบคุมอาหาร โดยลดปริมาณอาหารพลังงานที่ได้รับไม่ควรต่ำกว่า 1200 กิโลแคลอรีต่อวัน\n2. ควรเคลื่อนไหวและออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอทุกวัน\n\n"
        elif bmi >= 18.5 and bmi <= 22.90:
            color_zone = "green"
            texts1 = "อยู่ในเกณท์ : ปกติ (สุขภาพดี)"
            texts2 = "ภาวะเสี่ยงต่อโรค : เท่าคนปกติ"
            description = "น้ำหนักปกติ\nคุณมี น้ำหนักปกติ โดยทั่วไปค่าดัชนีมวลกายปกติมีค่าระหว่าง 18.50 - 22.90\n\nข้อแนะนำ\n1. ควรกินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม\n2. ควรเคลื่อนไหวและออกกำลังกายอย่างสม่ำเสมอทุกวันอย่างน้อย 30 นาที\n\n"
        else:
            color_zone = "red"
            texts1 = "อยู่ในเกณท์ : น้ำหนักต่ำกว่าเกณฑ์"
            texts2 = "ภาวะเสี่ยงต่อโรค : มากกว่าคนปกติ"
            description = "น้ำหนักน้อยกว่ามาตรฐาน\nคุณมีน้ำหนักน้อยหรือผอม โดยทั่วไป ค่าดัชนีมวลกายปกติมีค่าน้อยกว่า 18.50\n\n1. ควรกินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม เพิ่มอาหารประเภทที่ให้พลังงานมากขึ้น เช่น ไขมัน แป้ง ข้าว เนื้อสัตว์ นม\n2. ควรเคลื่อนไหวและออกกำลังกายอย่างสม่ำเสมอทุกวันหรือเกือบทุกวัน ให้เหนื่อยพอควรโดยหายใจกระชั้นขึ้น เช่น เดินเร็ว\n\n"

        show_data.config(text = f"\nBMI : {bmi}\n{texts1}\n{texts2}\n" ,background=color_zone)
        show_desc.config(text = description)
        insert_doc(os.environ['COMPUTERNAME'],weight,h,bmi)

    else:
        tk.messagebox.showwarning(title="Error", message="Weight and Height are required.")
        show_data.config(text='')
        show_desc.config(text='')

def update_bmi(_id):
    weight2 = weight_entry2.get()
    height2 = height_entry2.get()
    h2 = height_entry2.get()
    # check height and weight filled in
    if height2 and weight2 and h2:
        height2 = float(height2) / 100.0
        bmi2 = round(float(weight2) / height2 ** 2, 2)
        print(f"h : {height2}\nw : {weight2}\nbmi : {bmi2}\ncomputer name : {os.environ['COMPUTERNAME']}")
        if bmi2 > 30:
            color_zone2 = "red"
            texts12 = "อยู่ในเกณท์ : อ้วนมาก / โรคอ้วนระดับ 3"
            texts22 = "ภาวะเสี่ยงต่อโรค : มากกว่าคนปกติ"
            description2 = "อ้วนมาก / โรคอ้วนระดับ 3\nคุณ อ้วนมากแล้ว (อ้วนระดับ 3) โดยทั่วไปค่าดัชนีมวลกายปกติมีค่ามากกว่า 30\n\nข้อแนะนำ\n1. ควรควบคุมอาหารโดยลดปริมาณอาหารหรือปรับเปลี่ยนอาหารจากที่ให้พลังงานมากเป็นอาหารที่ให้พลังงานน้อย\n2. ควรเคลื่อนไหวและออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอทุกวัน 40-60 นาทีต่อวัน\n3. ควรฝึกความแข็งแรงของกล้ามเนื้อ ด้วยการฝึกกายบริหารหรือยกน้ำหนัก\n4. ถ้าคุณสามารถลดพลังงานเข้าจากอาหารลงได้วันละ 400 กิโลแคลอรี\n5. ควรปรึกษาแพทย์หรือผู้เชี่ยวชาญในการลดและควบคุมน้ำหนัก\n\n"
        elif bmi2 >= 25 and bmi2 <= 29.90:
            color_zone2 = "orange"
            texts12 = "อยู่ในเกณท์ : อ้วน / โรคอ้วนระดับ 2"
            texts22 = "ภาวะเสี่ยงต่อโรค : อันตรายระดับ 2"
            description2 = "อ้วน / โรคอ้วนระดับ 2\nคุณ อ้วนแล้ว (อ้วนระดับ 2) โดยทั่วไปค่าดัชนีมวลกายปกติมีค่าระหว่าง 25 - 29.90\n\nข้อแนะนำ\n1. ควรควบคุมอาหารโดยลดปริมาณอาหารหรือปรับเปลี่ยนอาหารจากที่ให้พลังงานมากเป็นอาหารที่ให้พลังงานน้อย\n2. ควรเคลื่อนไหวและออกกำลังกายประมาณ 40-60 นาทีต่อวัน\n3. ควรฝึกความแข็งแรงของกล้ามเนื้อ\n4. ถ้าคุณสามารถลดพลังงานเข้าจากอาหารลงได้วันละ 400 กิโลแคลอรี และเพิ่มการใช้พลังงาน\n\n"
        elif bmi2 >= 23 and bmi2 <= 24.90:
            color_zone2 = "yellow"
            texts12 = "อยู่ในเกณท์ : ท้วม / โรคอ้วนระดับ 1"
            texts22 = "ภาวะเสี่ยงต่อโรค : อันตรายระดับ 1"
            description2 = "ท้วม / อ้วนระดับ 1\nคุณมี น้ำหนักเกิน หรือรูปร่างท้วม โดยทั่วไปค่าดัชนีมวลกายปกติมีค่าระหว่าง 23 - 24.90\n\nข้อแนะนำ\n1. ควรควบคุมอาหาร โดยลดปริมาณอาหารพลังงานที่ได้รับไม่ควรต่ำกว่า 1200 กิโลแคลอรีต่อวัน\n2. ควรเคลื่อนไหวและออกกำลังกายแบบแอโรบิกอย่างสม่ำเสมอทุกวัน\n\n"
        elif bmi2 >= 18.5 and bmi2 <= 22.90:
            color_zone2 = "green"
            texts12 = "อยู่ในเกณท์ : ปกติ (สุขภาพดี)"
            texts22 = "ภาวะเสี่ยงต่อโรค : เท่าคนปกติ"
            description2 = "น้ำหนักปกติ\nคุณมี น้ำหนักปกติ โดยทั่วไปค่าดัชนีมวลกายปกติมีค่าระหว่าง 18.50 - 22.90\n\nข้อแนะนำ\n1. ควรกินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม\n2. ควรเคลื่อนไหวและออกกำลังกายอย่างสม่ำเสมอทุกวันอย่างน้อย 30 นาที\n\n"
        else:
            color_zone2 = "red"
            texts12 = "อยู่ในเกณท์ : น้ำหนักต่ำกว่าเกณฑ์"
            texts22 = "ภาวะเสี่ยงต่อโรค : มากกว่าคนปกติ"
            description2 = "น้ำหนักน้อยกว่ามาตรฐาน\nคุณมีน้ำหนักน้อยหรือผอม โดยทั่วไป ค่าดัชนีมวลกายปกติมีค่าน้อยกว่า 18.50\n\n1. ควรกินอาหารให้หลากหลายครบ 5 หมู่ในสัดส่วนที่เหมาะสม เพิ่มอาหารประเภทที่ให้พลังงานมากขึ้น เช่น ไขมัน แป้ง ข้าว เนื้อสัตว์ นม\n2. ควรเคลื่อนไหวและออกกำลังกายอย่างสม่ำเสมอทุกวันหรือเกือบทุกวัน ให้เหนื่อยพอควรโดยหายใจกระชั้นขึ้น เช่น เดินเร็ว\n\n"

        show_data2.config(text = f"\nBMI : {bmi2}\n{texts12}\n{texts22}\n" ,background=color_zone2)
        show_desc2.config(text = description2)
        replace_one(_id,os.environ['COMPUTERNAME'],weight2,h2,bmi2)
       
    else:
        pages.destroy
        tk.messagebox.showwarning(title="Error", message="Weight and Height are required.")
        show_data2.config(text='')
        show_desc2.config(text='')

def updatepage(a,b,c,d,e):
    print(a,b,c,d,e)
    global pages
    global weight_entry2
    global height_entry2
    global show_data2
    global show_desc2
    pages = tk.Tk()
    pages.title("Health & Diet Calculators :")

    info_frame = ttk.LabelFrame(pages, text="อัพเดตค่าดัชนีมวลกาย")
    info_frame.grid(row= 0, column=0, padx=35, pady=30)

    weight_label = ttk.Label(info_frame, text=f"น้ำหนักตัว (kg.) : =>  เดิม {b} kg.")
    weight_label.grid(row=1, column=0)

    height_label = ttk.Label(info_frame, text=f"ส่วนสูง (cm.) : =>  เดิม {c} cm.")
    height_label.grid(row=2, column=0)

    weight_entry2 = ttk.Entry(info_frame)
    weight_entry2.grid(row=1, column=1)

    height_entry2 = ttk.Entry(info_frame)
    height_entry2.grid(row=2, column=1)

    for widget in info_frame.winfo_children():
        widget.grid_configure(padx=100, pady=15)

    # Button
    button = ttk.Button(info_frame, text="Update", command=lambda:update_bmi(e))
    button.grid(row=3, column=0, sticky="news", padx=5, pady=5)

    button = ttk.Button(info_frame, text="Exit",command=pages.destroy)
    button.grid(row=3, column=1, sticky="news", padx=5, pady=5)

    show_data2 = ttk.Label(pages, text="",background="")
    show_data2.grid(rowspan=3,columnspan=2)
    show_desc2 = ttk.Label(pages, text="")
    show_desc2.grid(rowspan=8,columnspan=2)

    pages.mainloop()


def mainpage():
    global root
    global tabControl
    global tab1
    global tab2
    global tab3
    global height_entry
    global weight_entry
    global show_data
    global show_desc
    root = tk.Tk()
    root.title("Health & Diet Calculators :")

    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)

    # Create an instance of ttk style
    s = ttk.Style()
    s.theme_use('default')
    s.configure('TNotebook.Tab', background="snow3")
    s.map("TNotebook", background= [("selected", "snow3")])

    tabControl.add(tab1, text ='BMI')
    tabControl.add(tab2, text ='View Data')
    tabControl.bind("<ButtonRelease-1>",fTabSwitched)
    tabControl.pack(expand = 1, fill ="both")

    info_frame = ttk.LabelFrame(tab1, text="คำนวณหาค่าดัชนีมวลกาย")
    info_frame.grid(row= 0, column=0, padx=35, pady=30)

    weight_label = ttk.Label(info_frame, text="น้ำหนักตัว (kg.) : ")
    weight_label.grid(row=1, column=0)

    height_label = ttk.Label(info_frame, text="ส่วนสูง (cm.) : ")
    height_label.grid(row=2, column=0)

    weight_entry = ttk.Entry(info_frame)
    weight_entry.grid(row=1, column=1)

    height_entry = ttk.Entry(info_frame)
    height_entry.grid(row=2, column=1)

    for widget in info_frame.winfo_children():
        widget.grid_configure(padx=100, pady=15)

    # Button
    button = ttk.Button(info_frame, text="Calculators & Save", command=find_bmi)
    button.grid(row=3, column=0, sticky="news", padx=5, pady=5)

    button = ttk.Button(info_frame, text="Clear", command=clearToTextInput)
    button.grid(row=3, column=1, sticky="news", padx=5, pady=5)

    button = ttk.Button(info_frame, text="Exit", command=root.destroy)
    button.grid(row=4, columnspan=2, sticky="news", padx=5, pady=5)

    show_data = ttk.Label(tab1, text="",background="")
    show_data.grid(rowspan=3,columnspan=2)
    show_desc = ttk.Label(tab1, text="")
    show_desc.grid(rowspan=8,columnspan=2)

    root.mainloop()

mainpage()