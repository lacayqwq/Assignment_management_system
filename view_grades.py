import tkinter as tk
from tkinter import ttk
import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def center_window(win, width=800, height=460):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def fetch_grades_for_student(user_id):
    """联表查询该学生所有提交记录及成绩/评语"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    a.title,
                    h.submission_link,
                    h.submitted_at,
                    h.is_late,
                    h.score,
                    h.comment
                FROM homeworks h
                JOIN assignments a ON h.assignment_id = a.id
                WHERE h.user_id = %s
                ORDER BY h.submitted_at DESC
            """, (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print("查询评分失败：", e)
        return []
    finally:
        connection.close()

def open(user_id, role):
    win = tk.Toplevel()
    win.title("查看评分")
    win.configure(bg="#f0f4f7")
    center_window(win)

    tk.Label(win, text="我的作业评分记录", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    table_frame = tk.Frame(win, bg="#f0f4f7")
    table_frame.pack(fill="both", expand=True, padx=20)

    columns = ("title", "link", "submitted_at", "is_late", "score", "comment")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

    tree.heading("title", text="作业标题")
    tree.heading("link", text="提交链接/文件路径")
    tree.heading("submitted_at", text="提交时间")
    tree.heading("is_late", text="是否晚交")
    tree.heading("score", text="分数")
    tree.heading("comment", text="教师评语")

    tree.column("title", width=50, anchor="w")
    tree.column("link", width=220, anchor="w")
    tree.column("submitted_at", width=150, anchor="center")
    tree.column("is_late", width=80, anchor="center")
    tree.column("score", width=80, anchor="center")
    tree.column("comment", width=160, anchor="w")

    # 加载数据
    records = fetch_grades_for_student(user_id)
    for row in records:
        title, link, time, is_late, score, comment = row
        late_str = "是" if is_late else "否"
        score_str = str(score) if score is not None else "未评分"
        tree.insert("", tk.END, values=(
            title, 
            link, 
            time.strftime("%Y-%m-%d %H:%M"), 
            late_str,
            score_str,
            comment or ""
        ))

    # 添加滚动条
    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # 关闭按钮
    tk.Button(win, text="关闭", font=("Helvetica", 10),
              bg="#607d8b", fg="white", activebackground="#455a64",
              width=10, bd=0, command=win.destroy).pack(pady=10)
