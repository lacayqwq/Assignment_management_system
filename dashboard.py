import tkinter as tk
import submit_homework
import view_grades
import view_submissions
import publish_assignment
import manage_assignments
import view_all_assignments
def center_window(win, width=400, height=300):
    """将窗口居中显示"""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def open_dashboard(user_id, role):
    dashboard_win = tk.Tk()
    dashboard_win.title("作业提交平台 - 欢迎页面")
    center_window(dashboard_win, 450, 320)
    dashboard_win.configure(bg="#f0f4f7")  # 背景浅灰蓝

    # 标题 + 欢迎信息
    tk.Label(dashboard_win, text="作业提交平台", font=("Helvetica", 18, "bold"),
             bg="#f0f4f7", fg="#333").pack(pady=(20, 5))
    tk.Label(dashboard_win, text=f"欢迎，用户ID：{user_id}（角色：{role}）",
             font=("Helvetica", 12), bg="#f0f4f7", fg="#555").pack(pady=(0, 20))

    # 按钮区域
    btn_frame = tk.Frame(dashboard_win, bg="#f0f4f7")
    btn_frame.pack()

    button_style = {
        "font": ("Helvetica", 11),
        "width": 20,
        "height": 2,
        "bg": "#4caf50",         # 绿色背景
        "fg": "white",           # 白色字体
        "activebackground": "#45a049",  # 点击时变深
        "bd": 0,
        "relief": "ridge"
    }

    if role == "student":
        tk.Button(btn_frame, text="提交作业",
                  command=lambda: submit_homework.open(user_id, role), **button_style).pack(pady=10)
        tk.Button(btn_frame, text="查看评分",
                  command=lambda: view_grades.open(user_id, role), **button_style).pack(pady=10)
        tk.Button(dashboard_win, text="查看所有作业",
                    command=lambda: view_all_assignments.open(user_id, role), **button_style).pack(pady=10)
    elif role == "teacher":
        tk.Button(btn_frame, text="查看作业提交情况",
                  command=lambda: view_submissions.open(user_id, role), **button_style).pack(pady=10)
        tk.Button(dashboard_win, text="发布作业",
                  command=lambda: publish_assignment.open(user_id, role), **button_style).pack(pady=10)
        tk.Button(dashboard_win, text="管理已发布作业",
                  command=lambda: manage_assignments.open(user_id, role), **button_style).pack(pady=10)


    # 退出按钮
    tk.Button(dashboard_win, text="退出系统", command=dashboard_win.destroy,
              bg="#e53935", fg="white", font=("Helvetica", 10),
              width=12, height=1, activebackground="#d32f2f", bd=0).pack(pady=15)

    dashboard_win.mainloop()

# 测试用
if __name__ == '__main__':
    open_dashboard("2023001", "student")
