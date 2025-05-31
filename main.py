import tkinter as tk
from tkinter import messagebox
import pymysql
import dashboard  # 导入新的界面模块
import bcrypt

# 数据库连接配置（根据实际情况修改）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def create_users_table():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('student', 'teacher', 'admin') NOT NULL DEFAULT 'student'
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            connection.commit()
    except Exception as e:
        print("创建用户表失败：", e)
    finally:
        connection.close()

# def register_user(username, password, role='student'):
#     connection = pymysql.connect(**DB_CONFIG)
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
#             if cursor.fetchone():
#                 return False
#             cursor.execute(
#                 "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
#                 (username, password, role)
#             )
#             connection.commit()
#             return True
#     except Exception as e:
#         print("注册失败：", e)
#         return False
#     finally:
#         connection.close()

def login_user(username, password):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, password, role FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if result:
                user_id, hashed_pw, role = result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
                    return user_id, role
            return None
    except Exception as e:
        print("登录失败：", e)
        return None
    finally:
        connection.close()
def update_password(username, old_password, new_password):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
            result = cursor.fetchone()
            if not result:
                return "用户不存在"

            stored_password = result[0]
            if not bcrypt.checkpw(old_password.encode('utf-8'), stored_password.encode('utf-8')):
                return "旧密码错误"

            new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_hashed, username))
            connection.commit()
            return "密码修改成功"
    except Exception as e:
        print("密码修改失败：", e)
        return "操作失败"
    finally:
        connection.close()


# --------------------- Tkinter 美化界面部分 ---------------------

def center_window(win, width=400, height=300):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def on_login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if not username or not password:
        messagebox.showwarning("警告", "请输入用户名和密码！")
        return

    user_info = login_user(username, password)
    if user_info:
        user_id, role = user_info
        messagebox.showinfo("登录成功", f"欢迎，用户ID：{user_id}\n角色：{role}")
        root.destroy()
        dashboard.open_dashboard(user_id, role)
    else:
        messagebox.showerror("错误", "用户名或密码错误！")
def on_register():
    import register  # 导入新模块
    register.open_register_window()  # 打开注册界面
def open_change_password_window():
    def submit_change():
        username = entry_user.get().strip()
        old_pw = entry_old.get().strip()
        new_pw = entry_new.get().strip()

        if not username or not old_pw or not new_pw:
            messagebox.showwarning("警告", "请完整填写所有信息")
            return

        msg = update_password(username, old_pw, new_pw)
        messagebox.showinfo("提示", msg)
        win.destroy()

    win = tk.Toplevel(root)
    win.title("修改密码")
    center_window(win, 350, 230)
    win.configure(bg="#f0f4f7")

    tk.Label(win, text="用户名:", bg="#f0f4f7").pack(pady=5)
    entry_user = tk.Entry(win)
    entry_user.pack(pady=5)

    tk.Label(win, text="旧密码:", bg="#f0f4f7").pack(pady=5)
    entry_old = tk.Entry(win, show="*")
    entry_old.pack(pady=5)

    tk.Label(win, text="新密码:", bg="#f0f4f7").pack(pady=5)
    entry_new = tk.Entry(win, show="*")
    entry_new.pack(pady=5)

    tk.Button(win, text="提交", command=submit_change, bg="#4caf50", fg="white").pack(pady=10)

# 初始化窗口
create_users_table()
root = tk.Tk()
root.title("作业管理平台 - 登录")
root.configure(bg="#f0f4f7")
center_window(root, 430, 280)

# 标题
tk.Label(root, text="作业管理平台", font=("Helvetica", 18, "bold"), bg="#f0f4f7", fg="#333").pack(pady=(20, 5))
tk.Label(root, text="用户登录", font=("Helvetica", 12), bg="#f0f4f7", fg="#666").pack(pady=(0, 15))

# 登录框区域
frame = tk.Frame(root, bg="#f0f4f7")
frame.pack()

tk.Label(frame, text="用户名:", bg="#f0f4f7", font=("Helvetica", 11)).grid(row=0, column=0, padx=10, pady=8, sticky="e")
entry_username = tk.Entry(frame, font=("Helvetica", 11), width=25)
entry_username.grid(row=0, column=1, padx=10, pady=8)

tk.Label(frame, text="密码:", bg="#f0f4f7", font=("Helvetica", 11)).grid(row=1, column=0, padx=10, pady=8, sticky="e")
entry_password = tk.Entry(frame, show="*", font=("Helvetica", 11), width=25)
entry_password.grid(row=1, column=1, padx=10, pady=8)

# 按钮区域
btn_frame = tk.Frame(root, bg="#f0f4f7")
btn_frame.pack(pady=15)

btn_style = {
    "font": ("Helvetica", 11),
    "width": 12,
    "height": 1,
    "bd": 0,
    "fg": "white"
}

tk.Button(btn_frame, text="登录", bg="#4caf50", activebackground="#45a049",
          command=on_login, **btn_style).grid(row=0, column=0, padx=15)

tk.Button(btn_frame, text="注册", bg="#2196f3", activebackground="#1976d2",
          command=on_register, **btn_style).grid(row=0, column=1, padx=15)
tk.Button(btn_frame, text="修改密码", bg="#ff9800", activebackground="#fb8c00",
          command=lambda: open_change_password_window(), **btn_style).grid(row=0, column=2, padx=15)

root.mainloop()
