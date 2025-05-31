from graphviz import Digraph

def create_db_structure():
    # 创建有向图，设置UTF-8编码
    dot = Digraph(comment='作业管理系统数据库结构', encoding='utf-8')
    dot.attr(rankdir='LR')  # 从左到右的布局
    
    # 设置全局属性
    dot.attr('graph', 
            fontname='Arial, SimHei',  # 使用Arial和SimHei组合
            dpi='300',  # 提高DPI
            fontsize='14'  # 字体大小
            )
    dot.attr('node', 
            fontname='Arial, SimHei',  # 使用Arial和SimHei组合
            fontsize='12',  # 节点字体大小
            shape='none'    # 移除节点边框，使用自定义HTML表格
            )
    dot.attr('edge', 
            fontname='Arial, SimHei',  # 使用Arial和SimHei组合
            color='#666666',
            fontsize='10'  # 边的字体大小
            )

    # 用户表
    dot.node('users', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD PORT="title" BGCOLOR="#E8F4F8"><B>users (用户表)</B></TD></TR>
        <TR><TD PORT="f1" ALIGN="LEFT" BGCOLOR="#F8FCFF">user_id INT (PK)</TD></TR>
        <TR><TD PORT="f2" ALIGN="LEFT" BGCOLOR="#F8FCFF">username VARCHAR(50)</TD></TR>
        <TR><TD PORT="f3" ALIGN="LEFT" BGCOLOR="#F8FCFF">password VARCHAR(255)</TD></TR>
        <TR><TD PORT="f4" ALIGN="LEFT" BGCOLOR="#F8FCFF">role ENUM</TD></TR>
    </TABLE>>''')

    # 作业表
    dot.node('assignments', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD PORT="title" BGCOLOR="#F0F8F0"><B>assignments (作业表)</B></TD></TR>
        <TR><TD PORT="f1" ALIGN="LEFT" BGCOLOR="#F8FFF8">id INT (PK)</TD></TR>
        <TR><TD PORT="f2" ALIGN="LEFT" BGCOLOR="#F8FFF8">title VARCHAR(100)</TD></TR>
        <TR><TD PORT="f3" ALIGN="LEFT" BGCOLOR="#F8FFF8">description TEXT</TD></TR>
        <TR><TD PORT="f4" ALIGN="LEFT" BGCOLOR="#F8FFF8">deadline DATETIME</TD></TR>
        <TR><TD PORT="f5" ALIGN="LEFT" BGCOLOR="#F8FFF8">created_at TIMESTAMP</TD></TR>
    </TABLE>>''')

    # 作业提交表
    dot.node('homeworks', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        <TR><TD PORT="title" BGCOLOR="#FFF0F0"><B>homeworks (作业提交表)</B></TD></TR>
        <TR><TD PORT="f1" ALIGN="LEFT" BGCOLOR="#FFF8F8">id INT (PK)</TD></TR>
        <TR><TD PORT="f2" ALIGN="LEFT" BGCOLOR="#FFF8F8">user_id INT (FK)</TD></TR>
        <TR><TD PORT="f3" ALIGN="LEFT" BGCOLOR="#FFF8F8">assignment_id INT (FK)</TD></TR>
        <TR><TD PORT="f4" ALIGN="LEFT" BGCOLOR="#FFF8F8">submission_link TEXT</TD></TR>
        <TR><TD PORT="f5" ALIGN="LEFT" BGCOLOR="#FFF8F8">submitted_at TIMESTAMP</TD></TR>
        <TR><TD PORT="f6" ALIGN="LEFT" BGCOLOR="#FFF8F8">is_late BOOLEAN</TD></TR>
        <TR><TD PORT="f7" ALIGN="LEFT" BGCOLOR="#FFF8F8">score INT</TD></TR>
        <TR><TD PORT="f8" ALIGN="LEFT" BGCOLOR="#FFF8F8">comment TEXT</TD></TR>
    </TABLE>>''')

    # 添加关系
    dot.edge('homeworks:f2', 'users:f1', 'belongs to')
    dot.edge('homeworks:f3', 'assignments:f1', 'refers to')
    
    # 保存图片
    dot.render('database_structure', format='png', cleanup=True)
    print("数据库结构图已生成：database_structure.png")

if __name__ == "__main__":
    create_db_structure() 