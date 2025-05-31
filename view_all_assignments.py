import tkinter as tk
from tkinter import ttk
import pymysql
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def center_window(win, width=1000, height=500):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def fetch_assignments_with_status(user_id):
    """查询所有作业及该学生是否提交、是否晚交"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.id, a.title, a.description, a.deadline,
                    h.submission_link, h.is_late
                FROM assignments a
                LEFT JOIN homeworks h
                    ON a.id = h.assignment_id AND h.user_id = %s
                ORDER BY a.deadline ASC
            """, (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print("查询失败：", e)
        return []
    finally:
        connection.close()

def open(user_id, role):
    win = tk.Toplevel()
    win.title("查看所有作业")
    win.configure(bg="#f0f4f7")
    center_window(win, 820, 520)

    tk.Label(win, text="所有已发布作业及提交情况", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    table_frame = tk.Frame(win, bg="#f0f4f7")
    table_frame.pack(fill="both", expand=True, padx=20)

    columns = ("id", "title", "description", "deadline", "submitted", "is_late")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

    tree.heading("id", text="作业ID")
    tree.heading("title", text="标题")
    tree.heading("description", text="描述")
    tree.heading("deadline", text="截止时间")
    tree.heading("submitted", text="是否提交")
    tree.heading("is_late", text="是否晚交")

    tree.column("id", width=60, anchor="center")
    tree.column("title", width=160, anchor="w")
    tree.column("description", width=200, anchor="w")
    tree.column("deadline", width=160, anchor="center")
    tree.column("submitted", width=90, anchor="center")
    tree.column("is_late", width=90, anchor="center")

    records = fetch_assignments_with_status(user_id)
    for row in records:
        assignment_id, title, description, deadline, link, is_late = row
        submitted = "是" if link else "否"
        late = "是" if is_late else ("否" if link else "-")
        tree.insert("", tk.END, values=(assignment_id, title, description, deadline.strftime("%Y-%m-%d %H:%M"), submitted, late))

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # 关闭按钮
    tk.Button(win, text="关闭", font=("Helvetica", 10),
              bg="#607d8b", fg="white", activebackground="#455a64",
              width=10, bd=0, command=win.destroy).pack(pady=10)
