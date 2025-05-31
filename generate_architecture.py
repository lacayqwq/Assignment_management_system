from graphviz import Digraph

def create_architecture_diagram():
    # 创建有向图，设置UTF-8编码
    dot = Digraph(comment='作业管理系统架构图', encoding='utf-8')
    dot.attr(rankdir='TB')  # 从上到下的布局
    
    # 设置全局属性
    dot.attr('graph', 
            fontname='SimHei',
            dpi='300',  # 提高DPI
            fontsize='14'  # 增大字体
            )
    dot.attr('node', 
            fontname='SimHei',
            fontsize='12'  # 节点字体大小
            )
    dot.attr('edge', 
            fontname='SimHei',
            color='#666666',
            fontsize='10'  # 边的字体大小
            )
    
    # 设置图形属性
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='white')
    
    # 添加用户界面层
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='用户界面层 (Tkinter GUI)', 
              style='rounded,filled', 
              color='#E8F4F8', 
              fillcolor='#E8F4F8', 
              fontname='SimHei',
              fontsize='16',  # 增大标题字体
              labelloc='t')  # 标题在顶部
        c.node('login', '登录界面')
        c.node('register', '注册界面')
        c.node('dashboard', '主控面板')
        c.node('student_ui', '学生功能')
        c.node('teacher_ui', '教师功能')
    
    # 添加业务逻辑层
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='业务逻辑层 (Python + bcrypt)', 
              style='rounded,filled', 
              color='#F0F8F0', 
              fillcolor='#F0F8F0', 
              fontname='SimHei',
              fontsize='16',  # 增大标题字体
              labelloc='b', 
              labeljust='r')  # 标题在底部右侧
        c.node('auth', '用户认证')
        c.node('assignment_mgmt', '作业管理')
        c.node('submission_mgmt', '提交管理')
        c.node('grading_mgmt', '评分管理')
        c.node('file_mgmt', '文件管理')
    
    # 添加数据访问层
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='数据访问层 (MySQL + PyMySQL)', 
              style='rounded,filled', 
              color='#FFF0F0', 
              fillcolor='#FFF0F0', 
              fontname='SimHei',
              fontsize='16',  # 增大标题字体
              labelloc='b')  # 标题在底部
        c.node('db_users', '用户数据')
        c.node('db_assignments', '作业数据')
        c.node('db_submissions', '提交数据')
        c.node('db_grades', '成绩数据')
    
    # 用户界面层的交互
    dot.edge('login', 'dashboard')
    dot.edge('register', 'login')
    dot.edge('dashboard', 'student_ui')
    dot.edge('dashboard', 'teacher_ui')
    
    # 界面层到业务层的连接
    dot.edge('login', 'auth')
    dot.edge('register', 'auth')
    dot.edge('student_ui', 'submission_mgmt')
    dot.edge('student_ui', 'assignment_mgmt')
    dot.edge('teacher_ui', 'assignment_mgmt')
    dot.edge('teacher_ui', 'grading_mgmt')
    
    # 业务层内部交互
    dot.edge('submission_mgmt', 'file_mgmt')
    dot.edge('assignment_mgmt', 'file_mgmt')
    
    # 业务层到数据层的连接
    dot.edge('auth', 'db_users')
    dot.edge('assignment_mgmt', 'db_assignments')
    dot.edge('submission_mgmt', 'db_submissions')
    dot.edge('grading_mgmt', 'db_grades')
    dot.edge('file_mgmt', 'db_submissions')
    
    # 保存图片
    dot.render('system_architecture', format='png', cleanup=True)
    print("架构图已生成：system_architecture.png")

if __name__ == "__main__":
    create_architecture_diagram() 