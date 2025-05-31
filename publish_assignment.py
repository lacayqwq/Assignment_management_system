import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
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

def create_assignment_table():
    """确保作业表存在"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assignments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    deadline DATETIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            connection.commit()
    except Exception as e:
        print("作业表创建失败：", e)
    finally:
        connection.close()

def insert_assignment(title, description, deadline):
    """将新作业插入数据库"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO assignments (title, description, deadline)
                VALUES (%s, %s, %s)
            """, (title, description, deadline))
            connection.commit()
            return True
    except Exception as e:
        print("作业发布失败：", e)
        return False
    finally:
        connection.close()

def center_window(win, width=500, height=400):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def open(user_id, role):
    create_assignment_table()

    win = tk.Toplevel()
    win.title("发布新作业")
    win.configure(bg="#f0f4f7")
    center_window(win, 520, 450)

    tk.Label(win, text="发布新作业", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    frame = tk.Frame(win, bg="#f0f4f7")
    frame.pack(pady=10, padx=20)

    # 标题
    tk.Label(frame, text="作业标题：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=0, column=0, sticky="e", pady=8)
    entry_title = tk.Entry(frame, font=("Helvetica", 11), width=35)
    entry_title.grid(row=0, column=1, pady=8)

    # 描述
    tk.Label(frame, text="作业描述：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=1, column=0, sticky="ne", pady=8)
    text_description = tk.Text(frame, font=("Helvetica", 11), width=35, height=5)
    text_description.grid(row=1, column=1, pady=8)

    # 截止日期
    tk.Label(frame, text="截止日期：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=2, column=0, sticky="e", pady=8)
    deadline_date = DateEntry(frame, font=("Helvetica", 11), width=15, date_pattern='yyyy-mm-dd')
    deadline_date.grid(row=2, column=1, sticky="w", pady=8)

    # 截止时间
    tk.Label(frame, text="截止时间：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=3, column=0, sticky="e", pady=8)
    entry_time = tk.Entry(frame, font=("Helvetica", 11), width=10)
    entry_time.insert(0, "23:59")  # 默认时间
    entry_time.grid(row=3, column=1, sticky="w", pady=8)

    # 提交按钮
    def submit_assignment():
        title = entry_title.get().strip()
        description = text_description.get("1.0", tk.END).strip()
        date = deadline_date.get_date()
        time_str = entry_time.get().strip()

        if not title or not description or not time_str:
            messagebox.showwarning("警告", "请填写完整信息！")
            return

        try:
            deadline = datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("格式错误", "请输入正确的时间格式，如 23:59")
            return

        success = insert_assignment(title, description, deadline)
        if success:
            messagebox.showinfo("成功", "作业已成功发布！")
            win.destroy()
        else:
            messagebox.showerror("失败", "发布失败，请重试。")

    tk.Button(win, text="发布作业", font=("Helvetica", 11),
              bg="#4caf50", fg="white", activebackground="#45a049",
              width=14, bd=0, command=submit_assignment).pack(pady=20)

    # 关闭按钮
    tk.Button(win, text="取消", font=("Helvetica", 10),
              bg="#e53935", fg="white", activebackground="#d32f2f",
              width=10, bd=0, command=win.destroy).pack()
