import pymysql

def test_mysql_connection():
    try:
        # 替换为你自己的 MySQL 信息
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='2020888lcy',   # 如果有密码就写在这里，没有就空字符串
            database='mysql',          # 可以先连到已有的数据库，比如默认的 'mysql'
            charset='utf8mb4'
        )
        print("数据库连接成功！")
        
        # 测试执行一个简单的查询
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print("MySQL 版本:", version[0])
            
    except Exception as e:
        print("连接失败，错误信息：", e)
    finally:
        # 关闭连接
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    test_mysql_connection()
