import pymysql
import bcrypt

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '2020888lcy',
    'database': 'course_selection',
    'charset': 'utf8mb4'
}

def upgrade_passwords():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 获取所有用户和原始密码
            cursor.execute("SELECT user_id, password FROM users")
            users = cursor.fetchall()

            for user_id, plain_pw in users:
                if not plain_pw.startswith('$2b$'):  # 判断是否已经加密
                    hashed = bcrypt.hashpw(plain_pw.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("UPDATE users SET password=%s WHERE user_id=%s", (hashed.decode('utf-8'), user_id))

            connection.commit()
            print("所有明文密码已成功加密！")
    finally:
        connection.close()

def migrate_database():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 检查score字段是否存在
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'homeworks' 
                AND COLUMN_NAME = 'score'
            """, (DB_CONFIG['database'],))
            
            if cursor.fetchone()[0] == 0:
                print("正在添加score字段...")
                cursor.execute("""
                    ALTER TABLE homeworks 
                    ADD COLUMN score INT DEFAULT NULL
                """)
                print("score字段添加成功！")
            else:
                print("score字段已存在")

            # 确保comment字段为TEXT类型
            cursor.execute("""
                ALTER TABLE homeworks 
                MODIFY comment TEXT DEFAULT NULL
            """)
            print("comment字段类型已更新为TEXT")

            connection.commit()
            print("数据库更新完成！")
            
    except Exception as e:
        print(f"更新失败：{str(e)}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    print("开始更新数据库结构...")
    migrate_database()

upgrade_passwords()
