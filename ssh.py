import sqlite3
import subprocess
from prettytable import PrettyTable

def connect_to_database():
    # 连接到 SQLite 数据库，如果不存在则创建
    connection = sqlite3.connect("servers.db")
    cursor = connection.cursor()

    # 创建表格（如果不存在）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY,
        key TEXT,
        IP TEXT,
        port TEXT DEFAULT '22'
    )
    """)

    connection.commit()

    return connection, cursor

def close_database(connection):
    # 关闭数据库连接
    connection.close()

def add_item():
    key = input("\n输入要添加的键: ")
    IPadd = input("输入要添加的值: ")
    port = input("输入要添加的端口 (默认值为 22): ")

    connection, cursor = connect_to_database()

    # 将新的键值对插入数据库
    cursor.execute("INSERT INTO servers (key, IP, port) VALUES (?, ?, ?)", (key, IPadd, port))

    connection.commit()
    close_database(connection)

def ssh():
    #连接数据库
    connection, cursor = connect_to_database()
    # 用户输入服务器名称
    user_input = input("请输入连接服务器的id数字: ")
    cursor.execute("SELECT * FROM servers WHERE id = ?", (user_input,))
    result = cursor.fetchone()
    if result:
        ssh_command = f"ssh -p {result[3]} root@{result[2]}"
        try:
            # 执行SSH命令
            subprocess.run(ssh_command, shell=True, check=True) 

        except subprocess.CalledProcessError:
            print("连接失败")
    else:
        print(f"无效的服务器名称: {user_input}")

def print_menu():
    print("*"*60)
    print("\na. 连接服务器")
    print("b. 添加服务器")
    print("c. 删除服务器")
    print("d. 修改服务器")
    print("e. 查找服务器")
    print("q. 退出程序")
    display_dict()
    print("*"*60)

def display_dict():
    # 显示数据库中的服务器信息
    connection, cursor = connect_to_database()

    print("\n当前数据库中所有服务器:")

    cursor.execute("SELECT * FROM servers")
    column_names = [description[0] for description in cursor.description]

    # 创建 PrettyTable 对象
    table = PrettyTable(column_names)

    # 打印数据
    for row in cursor.fetchall():
        table.add_row(row)

    # 打印美化后的表格
    print(table)


    close_database(connection)


def delete_item():
    key_to_delete = input("\n输入要删除的服务器的id: ")

    connection, cursor = connect_to_database()

    # 从数据库中删除键值对
    cursor.execute("DELETE FROM servers WHERE id=?", (key_to_delete,))
    connection.commit()

    if cursor.rowcount > 0:
        print(f"{key_to_delete} 已从数据库中删除。")
    else:
        print(f"键 {key_to_delete} 不存在于数据库中。")

    close_database(connection)

def modify_item():
    key_to_modify = input("\n输入要修改服务器的id: ")

    connection, cursor = connect_to_database()

    # 检查键是否存在
    cursor.execute("SELECT * FROM servers WHERE id=?", (key_to_modify,))
    existing_server = cursor.fetchone()

    if existing_server:
        key = input("\n输入要添加的键: ")
        IPadd = input("输入要添加的IP: ")
        port = input("输入要添加的端口 (默认值为 22): ")

        # 更新数据库中的键值对
        cursor.execute("UPDATE servers SET key=?, IP=?, port=? WHERE id=?", (key,IPadd, port, key_to_modify))
        
        connection.commit()

    else:
        print(f"键 {key_to_modify} 不存在于数据库中。")

    close_database(connection)

def search_item():
    key_to_search = input("\n输入要查找的键: ")

    connection, cursor = connect_to_database()

    # 从数据库中查找键值对
    cursor.execute("SELECT * FROM servers WHERE key=?", (key_to_search,))
    found_server = cursor.fetchone()

    if found_server:
        print(f"{found_server[0]}: {found_server[1]}")
    else:
        print(f"键 {key_to_search} 不存在于数据库中。")

    close_database(connection)

if __name__ == '__main__':
    while True:
        print_menu()
        choice = input("\n请选择操作（输入对应数字或 q 退出）: ")

        if choice == "a":
            ssh()
        elif choice == "b":
            add_item()
        elif choice == "c":
            delete_item()
        elif choice == "d":
            modify_item()
        elif choice == "e":
            search_item()
        elif choice.lower() == "q":
            break
        else:
            print("无效的选择，请重新输入。")
