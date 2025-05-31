import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def center_window(win, width=500, height=400):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def update_grade(user_id, assignment_id, score, comment):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE homeworks 
                SET score=%s, comment=%s 
                WHERE user_id=%s AND assignment_id=%s
            """, (score, comment, user_id, assignment_id))
            connection.commit()
            return True
    except Exception as e:
        print("评分失败：", e)
        return False
    finally:
        connection.close()

def get_current_grade(user_id, assignment_id):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT score, comment 
                FROM homeworks 
                WHERE user_id=%s AND assignment_id=%s
            """, (user_id, assignment_id))
            result = cursor.fetchone()
            return result if result else (None, None)
    except Exception as e:
        print("获取当前评分失败：", e)
        return None, None
    finally:
        connection.close()

def open_grade_window(user_id, assignment_id, refresh_callback=None):
    current_score, current_comment = get_current_grade(user_id, assignment_id)
    
    win = tk.Toplevel()
    win.title("评分界面")
    center_window(win, 500, 400)
    win.configure(bg="#f0f4f7")

    # 标题
    tk.Label(win, text=f"为用户 {user_id} 评分", bg="#f0f4f7", 
             font=("Helvetica", 14, "bold")).pack(pady=(20, 15))

    # 分数输入框
    score_frame = tk.Frame(win, bg="#f0f4f7")
    score_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Label(score_frame, text="分数：", bg="#f0f4f7", 
             font=("Helvetica", 11)).pack(side="left")
    
    score_var = tk.StringVar(value=str(current_score) if current_score is not None else "")
    score_entry = tk.Entry(score_frame, textvariable=score_var, 
                          font=("Helvetica", 11), width=10)
    score_entry.pack(side="left")
    
    tk.Label(score_frame, text="（0-100）", bg="#f0f4f7", 
             font=("Helvetica", 10)).pack(side="left", padx=(5, 0))

    # 评价输入区
    tk.Label(win, text="评价：", bg="#f0f4f7", 
             font=("Helvetica", 11)).pack(anchor="w", padx=20, pady=(10, 5))
    
    comment_text = tk.Text(win, font=("Helvetica", 11), width=50, height=10)
    if current_comment:
        comment_text.insert("1.0", current_comment)
    comment_text.pack(padx=20, pady=(0, 10))

    def on_submit():
        try:
            score = int(score_var.get())
            if not (0 <= score <= 100):
                raise ValueError("分数必须在0-100之间")
        except ValueError as e:
            messagebox.showerror("错误", str(e))
            return

        comment = comment_text.get("1.0", tk.END).strip()
        
        if update_grade(user_id, assignment_id, score, comment):
            messagebox.showinfo("成功", "评分已保存")
            if refresh_callback:
                refresh_callback()
            win.destroy()
        else:
            messagebox.showerror("错误", "评分保存失败")

    # 按钮区域
    btn_frame = tk.Frame(win, bg="#f0f4f7")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="提交评分", font=("Helvetica", 11),
              bg="#4caf50", fg="white", activebackground="#45a049",
              width=15, bd=0, command=on_submit).pack(side="left", padx=10)

    tk.Button(btn_frame, text="取消", font=("Helvetica", 11),
              bg="#f44336", fg="white", activebackground="#d32f2f",
              width=10, bd=0, command=win.destroy).pack(side="left", padx=10)

if __name__ == "__main__":
    # 测试用
    root = tk.Tk()
    root.withdraw()
    open_grade_window(1, 1)
    root.mainloop()
