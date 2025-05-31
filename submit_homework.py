import tkinter as tk
from tkinter import messagebox, filedialog, ttk
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

def create_homework_table():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 创建作业提交表（如果不存在）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS homeworks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    assignment_id INT NOT NULL,
                    submission_link TEXT,
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_late BOOLEAN DEFAULT FALSE,
                    comment TEXT,
                    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            connection.commit()
    except Exception as e:
        print("创建作业表失败：", e)
    finally:
        connection.close()

def fetch_assignments():
    """获取所有已发布作业"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title, deadline FROM assignments ORDER BY deadline DESC")
            return cursor.fetchall()
    except Exception as e:
        print("查询作业失败：", e)
        return []
    finally:
        connection.close()

def submit_homework_link(user_id, assignment_id, link):
    """插入或更新作业提交记录，同时判断是否晚交"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 获取该作业的截止时间
            cursor.execute("SELECT deadline FROM assignments WHERE id=%s", (assignment_id,))
            deadline_row = cursor.fetchone()
            if not deadline_row:
                return False
            deadline = deadline_row[0]
            now = datetime.now()
            is_late = now > deadline

            # 判断是否已提交
            cursor.execute("SELECT * FROM homeworks WHERE user_id=%s AND assignment_id=%s", (user_id, assignment_id))
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE homeworks 
                    SET submission_link=%s, submitted_at=CURRENT_TIMESTAMP, is_late=%s 
                    WHERE user_id=%s AND assignment_id=%s
                """, (link, is_late, user_id, assignment_id))
            else:
                cursor.execute("""
                    INSERT INTO homeworks (user_id, assignment_id, submission_link, is_late)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, assignment_id, link, is_late))
            connection.commit()
            return True
    except Exception as e:
        print("作业提交失败：", e)
        return False
    finally:
        connection.close()

def center_window(win, width=540, height=320):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def open(user_id, role):
    create_homework_table()
    assignments = fetch_assignments()
    if not assignments:
        messagebox.showinfo("无作业", "当前没有可提交的作业。")
        return

    win = tk.Toplevel()
    win.title("提交作业")
    win.configure(bg="#f0f4f7")
    center_window(win, 550, 320)

    tk.Label(win, text="提交作业", font=("Helvetica", 16, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 10))

    frame = tk.Frame(win, bg="#f0f4f7")
    frame.pack()

    # 作业下拉框
    tk.Label(frame, text="请选择要提交的作业：", font=("Helvetica", 11), bg="#f0f4f7").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    assignment_var = tk.StringVar()
    assignment_menu = ttk.Combobox(frame, textvariable=assignment_var, font=("Helvetica", 11), width=40, state="readonly")
    assignment_dict = {f"{title}（截止：{deadline.strftime('%Y-%m-%d %H:%M')}）": id_ for id_, title, deadline in assignments}
    assignment_menu["values"] = list(assignment_dict.keys())
    assignment_menu.current(0)
    assignment_menu.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    # 提交链接
    tk.Label(frame, text="请输入云盘地址或选择本地文件：",
             font=("Helvetica", 11), bg="#f0f4f7").grid(row=2, column=0, sticky="w", padx=10, pady=5)

    entry_link = tk.Entry(frame, font=("Helvetica", 11), width=45)
    entry_link.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

    def choose_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            entry_link.delete(0, tk.END)
            entry_link.insert(0, file_path)

    tk.Button(frame, text="选择文件", font=("Helvetica", 10),
              bg="#2196f3", fg="white", activebackground="#1976d2",
              width=10, bd=0, command=choose_file).grid(row=3, column=2, padx=5, pady=5)

    # 提交按钮
    def on_submit():
        link = entry_link.get().strip()
        if not link:
            messagebox.showwarning("警告", "请输入或选择作业文件路径！")
            return
        selected_text = assignment_var.get()
        assignment_id = assignment_dict.get(selected_text)
        if not assignment_id:
            messagebox.showwarning("警告", "请选择作业！")
            return
        success = submit_homework_link(user_id, assignment_id, link)
        if success:
            messagebox.showinfo("提交成功", "作业已成功提交！")
            win.destroy()
        else:
            messagebox.showerror("提交失败", "提交过程中发生错误，请稍后重试。")

    tk.Button(win, text="提交", font=("Helvetica", 11),
              bg="#4caf50", fg="white", activebackground="#45a049",
              width=12, height=1, bd=0, command=on_submit).pack(pady=15)
