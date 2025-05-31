import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pymysql
from datetime import datetime

# 数据库连接
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def fetch_assignments():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, description, deadline FROM assignments ORDER BY deadline ASC")
            return cursor.fetchall()
    except Exception as e:
        print("查询失败：", e)
        return []
    finally:
        connection.close()

def update_assignment(assignment_id, title, description, deadline):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE assignments 
                SET title=%s, description=%s, deadline=%s 
                WHERE id=%s
            """, (title, description, deadline, assignment_id))
            connection.commit()
            return True
    except Exception as e:
        print("更新失败：", e)
        return False
    finally:
        connection.close()

def delete_assignment(assignment_id):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM assignments WHERE id=%s", (assignment_id,))
            connection.commit()
            return True
    except Exception as e:
        print("删除失败：", e)
        return False
    finally:
        connection.close()

def center_window(win, width=750, height=450):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def open(user_id, role):
    win = tk.Toplevel()
    win.title("管理已发布作业")
    win.configure(bg="#f0f4f7")
    center_window(win, 760, 500)

    tk.Label(win, text="已发布作业管理", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    table_frame = tk.Frame(win, bg="#f0f4f7")
    table_frame.pack(fill="both", expand=True, padx=20)

    columns = ("id", "title", "description", "deadline")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    tree.heading("id", text="ID")
    tree.heading("title", text="标题")
    tree.heading("description", text="描述")
    tree.heading("deadline", text="截止时间")

    tree.column("id", width=50, anchor="center")
    tree.column("title", width=150, anchor="w")
    tree.column("description", width=320, anchor="w")
    tree.column("deadline", width=180, anchor="center")

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for assignment in fetch_assignments():
            tree.insert("", tk.END, values=assignment)

    refresh_table()

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # 修改按钮功能
    def open_edit_window():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一个作业")
            return
        values = tree.item(selected[0])["values"]
        assignment_id, old_title, old_desc, old_deadline = values

        edit_win = tk.Toplevel()
        edit_win.title("编辑作业")
        center_window(edit_win, 480, 350)
        edit_win.configure(bg="#f0f4f7")

        tk.Label(edit_win, text="编辑作业信息", font=("Helvetica", 14, "bold"),
                 bg="#f0f4f7", fg="#333").pack(pady=15)

        frame = tk.Frame(edit_win, bg="#f0f4f7")
        frame.pack(pady=10)

        tk.Label(frame, text="标题：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=0, column=0, sticky="e", pady=5)
        entry_title = tk.Entry(frame, font=("Helvetica", 11), width=30)
        entry_title.insert(0, old_title)
        entry_title.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="描述：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=1, column=0, sticky="ne", pady=5)
        text_desc = tk.Text(frame, font=("Helvetica", 11), width=30, height=4)
        text_desc.insert("1.0", old_desc)
        text_desc.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="截止时间：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=2, column=0, sticky="e", pady=5)
        date = DateEntry(frame, font=("Helvetica", 11), width=12, date_pattern='yyyy-mm-dd')
        time_entry = tk.Entry(frame, font=("Helvetica", 11), width=8)

        # 解析原始时间
        dt = datetime.strptime(old_deadline, "%Y-%m-%d %H:%M:%S")
        date.set_date(dt.date())
        time_entry.insert(0, dt.strftime("%H:%M"))

        date.grid(row=2, column=1, sticky="w", pady=5, padx=(0, 5))
        time_entry.grid(row=2, column=1, sticky="e", pady=5)

        def save_edit():
            title = entry_title.get().strip()
            desc = text_desc.get("1.0", tk.END).strip()
            time_str = time_entry.get().strip()
            try:
                deadline = datetime.strptime(f"{date.get_date()} {time_str}", "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("格式错误", "时间格式不正确")
                return
            if update_assignment(assignment_id, title, desc, deadline):
                messagebox.showinfo("成功", "作业已更新")
                edit_win.destroy()
                refresh_table()
            else:
                messagebox.showerror("失败", "更新失败")

        tk.Button(edit_win, text="保存修改", font=("Helvetica", 11),
                  bg="#4caf50", fg="white", activebackground="#45a049",
                  width=14, bd=0, command=save_edit).pack(pady=15)

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一个作业")
            return
        values = tree.item(selected[0])["values"]
        assignment_id = values[0]
        confirm = messagebox.askyesno("确认删除", f"确定要删除作业：{values[1]}？")
        if confirm:
            if delete_assignment(assignment_id):
                messagebox.showinfo("删除成功", "作业已删除")
                refresh_table()
            else:
                messagebox.showerror("删除失败", "删除操作失败")

    # 按钮区
    btn_frame = tk.Frame(win, bg="#f0f4f7")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="修改选中作业", font=("Helvetica", 10),
              bg="#ff9800", fg="white", activebackground="#f57c00",
              width=14, bd=0, command=open_edit_window).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="删除选中作业", font=("Helvetica", 10),
              bg="#e53935", fg="white", activebackground="#d32f2f",
              width=14, bd=0, command=delete_selected).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="关闭", font=("Helvetica", 10),
              bg="#607d8b", fg="white", activebackground="#455a64",
              width=10, bd=0, command=win.destroy).grid(row=0, column=2, padx=10)
