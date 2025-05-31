import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas as pd
import grade_homework

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def center_window(win, width=760, height=500):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def fetch_assignments():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, deadline FROM assignments ORDER BY deadline DESC")
            return cursor.fetchall()
    except Exception as e:
        print("获取作业失败：", e)
        return []
    finally:
        connection.close()

def fetch_submissions_by_assignment(assignment_id):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, submission_link, submitted_at, is_late, score, comment 
                FROM homeworks 
                WHERE assignment_id = %s
                ORDER BY submitted_at DESC
            """, (assignment_id,))
            return cursor.fetchall()
    except Exception as e:
        print("获取提交失败：", e)
        return []
    finally:
        connection.close()

def update_comment(user_id, assignment_id, comment):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE homeworks 
                SET comment=%s 
                WHERE user_id=%s AND assignment_id=%s
            """, (comment, user_id, assignment_id))
            connection.commit()
            return True
    except Exception as e:
        print("批注失败：", e)
        return False
    finally:
        connection.close()

def export_to_excel(data, assignment_title):
    if not data:
        messagebox.showinfo("提示", "暂无可导出的数据。")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel 文件", "*.xlsx")],
        title="保存为 Excel 文件",
        initialfile=f"{assignment_title}_提交情况.xlsx"
    )

    if not file_path:
        return

    try:
        df = pd.DataFrame(data, columns=["用户ID", "提交链接", "提交时间", "是否晚交", "分数", "教师批注"])
        df.to_excel(file_path, index=False)
        messagebox.showinfo("导出成功", f"Excel 文件已保存至：\n{file_path}")
    except Exception as e:
        messagebox.showerror("导出失败", f"导出出错：{e}")

def open_comment_window(user_id, assignment_id, old_comment, refresh_callback):
    win = tk.Toplevel()
    win.title("批注作业")
    center_window(win, 400, 250)
    win.configure(bg="#f0f4f7")

    tk.Label(win, text=f"为用户 {user_id} 批注：", bg="#f0f4f7", font=("Helvetica", 12)).pack(pady=(20, 10))

    text = tk.Text(win, width=45, height=6, font=("Helvetica", 11))
    text.insert("1.0", old_comment or "")
    text.pack(padx=10, pady=10)

    def on_submit():
        comment = text.get("1.0", tk.END).strip()
        if update_comment(user_id, assignment_id, comment):
            messagebox.showinfo("成功", "批注已保存。")
            win.destroy()
            refresh_callback()
        else:
            messagebox.showerror("失败", "批注保存失败。")

    tk.Button(win, text="保存批注", font=("Helvetica", 10),
              bg="#4caf50", fg="white", activebackground="#45a049",
              width=12, bd=0, command=on_submit).pack(pady=10)

def open_submission_table(assignment_id, assignment_title):
    records = fetch_submissions_by_assignment(assignment_id)

    win = tk.Toplevel()
    win.title(f"作业《{assignment_title}》提交情况")
    win.configure(bg="#f0f4f7")
    center_window(win)

    tk.Label(win, text=f"作业《{assignment_title}》提交情况", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    frame = tk.Frame(win, bg="#f0f4f7")
    frame.pack(fill="both", expand=True, padx=20)

    columns = ("user_id", "submission_link", "submitted_at", "is_late", "score", "comment")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)

    for col, text, width in zip(columns,
                               ["用户ID", "提交链接", "提交时间", "是否晚交", "分数", "评价"],
                               [80, 250, 140, 80, 80, 130]):
        tree.heading(col, text=text)
        tree.column(col, width=width, anchor="center" if col in ("user_id", "submitted_at", "is_late", "score") else "w")

    def refresh():
        tree.delete(*tree.get_children())
        for row in fetch_submissions_by_assignment(assignment_id):
            user_id, link, time, is_late, score, comment = row
            tree.insert("", tk.END, values=(
                user_id, 
                link, 
                time.strftime("%Y-%m-%d %H:%M"), 
                "是" if is_late else "否",
                score if score is not None else "未评分",
                comment or ""
            ))

    refresh()

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    def grade_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一行")
            return
        item = tree.item(selected[0])
        user_id = item["values"][0]
        grade_homework.open_grade_window(user_id, assignment_id, refresh)

    btn_frame = tk.Frame(win, bg="#f0f4f7")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="评分", font=("Helvetica", 10),
              bg="#ff9800", fg="white", activebackground="#f57c00",
              width=14, bd=0, command=grade_selected).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="导出为Excel", font=("Helvetica", 10),
              bg="#2196f3", fg="white", activebackground="#1976d2",
              width=14, bd=0, command=lambda: export_to_excel(fetch_submissions_by_assignment(assignment_id), assignment_title)).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="关闭", font=("Helvetica", 10),
              bg="#e53935", fg="white", activebackground="#d32f2f",
              width=10, bd=0, command=win.destroy).grid(row=0, column=2, padx=10)

def open(user_id, role):
    assignments = fetch_assignments()

    if not assignments:
        messagebox.showinfo("提示", "当前无已发布作业。")
        return

    win = tk.Toplevel()
    win.title("选择要查看的作业")
    center_window(win, 600, 220)
    win.configure(bg="#f0f4f7")

    tk.Label(win, text="选择一个作业以查看学生提交情况", font=("Helvetica", 14, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=20)

    frame = tk.Frame(win, bg="#f0f4f7")
    frame.pack()

    assignment_var = tk.StringVar()
    assignment_menu = ttk.Combobox(frame, textvariable=assignment_var, font=("Helvetica", 11), width=50, state="readonly")

    assignment_dict = {}
    for aid, title, deadline in assignments:
        key = f"{title}（截止：{deadline.strftime('%Y-%m-%d %H:%M')}）"
        assignment_dict[key] = (aid, title)

    assignment_menu["values"] = list(assignment_dict.keys())
    assignment_menu.current(0)
    assignment_menu.grid(row=0, column=0, padx=10, pady=10)

    def on_next():
        selected_text = assignment_var.get()
        if selected_text in assignment_dict:
            aid, title = assignment_dict[selected_text]
            win.destroy()
            open_submission_table(aid, title)

    tk.Button(win, text="查看提交情况", font=("Helvetica", 11),
              bg="#4caf50", fg="white", activebackground="#45a049",
              width=18, bd=0, command=on_next).pack(pady=10)
