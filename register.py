import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import bcrypt

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def register_user(username, password, role):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                return False
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_pw.decode('utf-8'), role)
            )
            connection.commit()
            return True
    except Exception as e:
        print("注册失败：", e)
        return False
    finally:
        connection.close()

def center_window(win, width=420, height=330):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_register_window():
    win = tk.Toplevel()
    win.title("用户注册")
    win.configure(bg="#f0f4f7")
    center_window(win, 430, 340)

    tk.Label(win, text="注册新用户", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    frame = tk.Frame(win, bg="#f0f4f7")
    frame.pack(pady=5)

    # 用户名
    tk.Label(frame, text="用户名：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=0, column=0, sticky="e", pady=8, padx=10)
    entry_username = tk.Entry(frame, font=("Helvetica", 11), width=25)
    entry_username.grid(row=0, column=1, pady=8, padx=10)

    # 密码
    tk.Label(frame, text="密码：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=1, column=0, sticky="e", pady=8, padx=10)
    entry_password = tk.Entry(frame, show="*", font=("Helvetica", 11), width=25)
    entry_password.grid(row=1, column=1, pady=8, padx=10)

    # 身份
    tk.Label(frame, text="身份：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=2, column=0, sticky="e", pady=8, padx=10)
    role_var = tk.StringVar()
    role_combobox = ttk.Combobox(frame, textvariable=role_var, font=("Helvetica", 11),
                                 values=["student", "teacher"], state="readonly", width=23)
    role_combobox.current(0)
    role_combobox.grid(row=2, column=1, pady=8, padx=10)

    # 提交按钮
    def submit_register():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        role = role_var.get()

        if not username or not password:
            messagebox.showwarning("警告", "请输入完整信息！")
            return

        success = register_user(username, password, role)
        if success:
            messagebox.showinfo("注册成功", "注册成功，请返回登录界面登录。")
            win.destroy()
        else:
            messagebox.showerror("注册失败", "用户名已存在或数据库错误。")

    tk.Button(win, text="注册", font=("Helvetica", 11),
              bg="#4caf50", fg="white", activebackground="#45a049",
              width=12, bd=0, command=submit_register).pack(pady=20)

    # 取消按钮（可选）
    tk.Button(win, text="取消", font=("Helvetica", 10),
              bg="#e53935", fg="white", activebackground="#d32f2f",
              width=10, bd=0, command=win.destroy).pack()
