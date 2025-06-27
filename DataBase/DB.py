import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'access_control.db')

#role manager,user,admin
#access_logs，users，attendance_summary
#region
def init_db():
    """
    データベースとテーブル(users, access_logs)を初期化します。
    既存のテーブルがあれば削除し、新しく作成し直します。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 既存テーブルの削除
    cursor.execute('DROP TABLE IF EXISTS access_logs')
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS attendance_summary')
    # users表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT,
        card_name TEXT,
        card_id TEXT,
        register_date TEXT
    )
    ''')
    # access_logs表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp TEXT,
        card_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')
    # attendance_summary表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance_summary (
        user_id INTEGER,
        user_name TEXT,
        work_date TEXT,
        earliest_time TEXT,
        latest_time TEXT,
        PRIMARY KEY (user_id, work_date),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    conn.commit()
    conn.close()

def insert_sample_data():
    """
    サンプルデータ（ユーザー・アクセスログ）を挿入します。
    テストやデモ用に利用してください。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, role, card_id, card_name, register_date) VALUES (?, ?, ?, ?, ?)",
                   ("山田太郎", "管理者", "123456", "山田太郎_suica", "2024-06-01 10:00:00"))
    cursor.execute("INSERT INTO users (name, role, card_id, card_name, register_date) VALUES (?, ?, ?, ?, ?)",
                   ("佐藤花子", "一般", "654321", "佐藤花子_pasmo", "2024-06-02 11:00:00"))
    # 正常打卡日：6月10日（周一）
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-10 08:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-10 12:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-10 13:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-10 18:00:00", "ABC123"))

    # 迟到日：6月11日（周二）
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-11 08:10:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-11 18:00:00", "ABC123"))

    # 加班日：6月12日（周三）
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-12 08:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-12 18:20:00", "ABC123"))

    # 早到日：6月13日（周四）
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-13 07:50:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-13 18:00:00", "ABC123"))

    # 早退日：6月14日（周五）
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-14 08:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-14 17:40:00", "ABC123"))

    # 週六出勤：2024-06-15（土）→ 正常出勤 + 加班
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-15 08:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-15 18:20:00", "ABC123"))

    # 週日出勤：2024-06-16（日）→ 正常出勤
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-16 08:00:00", "ABC123"))
    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (1, "2024-06-16 18:00:00", "ABC123"))


    cursor.execute("INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)", (2, "2024-06-10 09:00:00", "XYZ789"))
    conn.commit()
    conn.close()

def clear_db():
    """
    データベース内の全データ(users, access_logs)を削除します。
    テーブル構造は残ります。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM access_logs")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM attendance_summary")
    conn.commit()
    conn.close()

def get_users():
    """
    ユーザー情報(usersテーブル)を全件取得します。
    Returns:
        list[dict]: ユーザー情報のリスト
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return [dict(u) for u in users]

def get_access_logs():
    """
    アクセスログ(access_logsテーブル)を全件取得します。
    Returns:
        list[dict]: アクセスログのリスト
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    logs = conn.execute('SELECT * FROM access_logs').fetchall()
    conn.close()
    return [dict(l) for l in logs]

def update_attendance_summary():
    """
    access_logsとusersから出勤汇总表を更新します。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 清空现有汇总数据
    cursor.execute("DELETE FROM attendance_summary")
    
    # 从access_logs获取每个用户每天的打卡记录
    cursor.execute('''
    SELECT 
        al.user_id,
        u.name as user_name,
        DATE(al.timestamp) as work_date,
        MIN(TIME(al.timestamp)) as earliest_time,
        MAX(TIME(al.timestamp)) as latest_time
    FROM access_logs al
    JOIN users u ON al.user_id = u.id
    GROUP BY al.user_id, DATE(al.timestamp)
    ORDER BY al.user_id, work_date
    ''')
    
    # 插入汇总数据
    for row in cursor.fetchall():
        cursor.execute('''
        INSERT INTO attendance_summary (user_id, user_name, work_date, earliest_time, latest_time)
        VALUES (?, ?, ?, ?, ?)
        ''', row)
    
    conn.commit()
    conn.close()

def get_attendance_summary():
    """
    出勤汇总表の全データを取得します。
    Returns:
        list[dict]: 出勤汇总データのリスト
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    summary = conn.execute('SELECT * FROM attendance_summary ORDER BY user_id, work_date').fetchall()
    conn.close()
    return [dict(s) for s in summary]

def delete_attendance_record(user_id, work_date):
    """
    指定されたユーザーIDと日付の出勤汇总記録を削除します。
    
    Args:
        user_id (int): ユーザーID
        work_date (str): 勤務日 (YYYY-MM-DD形式)
    
    Returns:
        dict: 削除された記録の情報
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 削除前に記録を取得
        cursor.execute('''
        SELECT user_id, user_name, work_date, earliest_time, latest_time
        FROM attendance_summary 
        WHERE user_id = ? AND work_date = ?
        ''', (user_id, work_date))
        
        record = cursor.fetchone()
        if not record:
            raise Exception(f"指定された記録が見つかりません: ユーザーID={user_id}, 日付={work_date}")
        
        # 記録を削除
        cursor.execute('''
        DELETE FROM attendance_summary 
        WHERE user_id = ? AND work_date = ?
        ''', (user_id, work_date))
        
        conn.commit()
        
        deleted_record = {
            'user_id': record[0],
            'user_name': record[1],
            'work_date': record[2],
            'earliest_time': record[3],
            'latest_time': record[4]
        }
        
        return deleted_record
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_user(user_id):
    """
    指定されたユーザーIDのユーザーを削除します。
    関連するアクセスログと出勤汇总記録も削除されます。
    
    Args:
        user_id (int): ユーザーID
    
    Returns:
        dict: 削除されたユーザーの情報
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 削除前にユーザー情報を取得
        cursor.execute('SELECT id, name, role, card_id, card_name, register_date FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if not user:
            raise Exception(f"指定されたユーザーが見つかりません: ユーザーID={user_id}")
        
        # 関連するアクセスログを削除
        cursor.execute('DELETE FROM access_logs WHERE user_id = ?', (user_id,))
        deleted_logs_count = cursor.rowcount
        
        # 関連する出勤汇总記録を削除
        cursor.execute('DELETE FROM attendance_summary WHERE user_id = ?', (user_id,))
        deleted_summary_count = cursor.rowcount
        
        # ユーザーを削除
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        
        deleted_user = {
            'id': user[0],
            'name': user[1],
            'role': user[2],
            'card_id': user[3],
            'card_name': user[4],
            'register_date': user[5],
            'deleted_logs_count': deleted_logs_count,
            'deleted_summary_count': deleted_summary_count
        }
        
        return deleted_user
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_access_log(log_id):
    """
    指定されたログIDのアクセスログを削除します。
    
    Args:
        log_id (int): ログID
    
    Returns:
        dict: 削除されたログの情報
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 削除前にログ情報を取得
        cursor.execute('''
        SELECT al.id, al.user_id, u.name as user_name, al.timestamp, al.card_id
        FROM access_logs al
        JOIN users u ON al.user_id = u.id
        WHERE al.id = ?
        ''', (log_id,))
        
        log = cursor.fetchone()
        if not log:
            raise Exception(f"指定されたログが見つかりません: ログID={log_id}")
        
        # ログを削除
        cursor.execute('DELETE FROM access_logs WHERE id = ?', (log_id,))
        
        conn.commit()
        
        deleted_log = {
            'id': log[0],
            'user_id': log[1],
            'user_name': log[2],
            'timestamp': log[3],
            'card_id': log[4]
        }
        
        return deleted_log
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_user_by_card_id(card_id):
    """
    通过卡牌ID查找用户信息
    
    Args:
        card_id (str): 卡牌ID
    
    Returns:
        dict: 用户信息，如果未找到则返回None
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, name, role, card_id, card_name, register_date 
    FROM users 
    WHERE card_id = ?
    ''', (card_id,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    else:
        return None

def add_access_log(user_id, timestamp, card_id):
    """
    アクセスログを追加します。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO access_logs (user_id, timestamp, card_id) VALUES (?, ?, ?)', (user_id, timestamp, card_id))

def add_user(name, role, card_id, card_name, register_date=None):
    """
    ユーザーを追加します。
    
    Args:
        name (str): ユーザー名
        role (str): ユーザー角色
        card_id (str): 卡牌ID
        card_name (str): 卡牌名称
        register_date (str): 注册日期，如果为None则使用当前时间
    
    Returns:
        dict: 添加的用户信息
    """
    if register_date is None:
        from datetime import datetime
        register_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO users (name, role, card_id, card_name, register_date) 
        VALUES (?, ?, ?, ?, ?)
        ''', (name, role, card_id, card_name, register_date))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        # 返回添加的用户信息
        added_user = {
            'id': user_id,
            'name': name,
            'role': role,
            'card_id': card_id,
            'card_name': card_name,
            'register_date': register_date
        }
        
        return added_user
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def check_card_id(card_id):
    """
    ユーザーを確認します。
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE card_id = ?', (card_id,))
    user = cursor.fetchone()
    conn.close()
    return user

#endregion

if __name__ == '__main__':
    init_db()
    insert_sample_data()
    update_attendance_summary()
    print("ユーザー:", get_users())
    print("アクセスログ:", get_access_logs())
    print("出勤汇总:", get_attendance_summary())