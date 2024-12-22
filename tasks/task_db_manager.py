import sqlite3
from datetime import datetime, timedelta
import os

def _start_database():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'data.db')
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    _create_table_if_not_exists(cursor)

    return conn, cursor

def _create_table_if_not_exists(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
                objective TEXT,
                creation_date TEXT,
                limit_date TEXT,
                coin_reward INTEGER
                )""")

def _create_new_task(objective, creation_date, limit_date, coin_reward):
    conn, cursor = _start_database()

    cursor.execute(f"INSERT INTO tasks VALUES( ?, ?, ?, ?)", (objective, creation_date, limit_date, coin_reward))

    conn.commit()
    conn.close()

def return_tasks() -> list:
    conn, cursor = _start_database()

    cursor.execute("SELECT * FROM tasks")

    data = cursor.fetchall()

    conn.close()
    return data

def create_new_task(objective, time_to_finish, coin_reward):
    now = datetime.now()
    limit_date = now + timedelta(days=time_to_finish)

    formatted_creation_date = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}"
    formatted_limit_date = f"{limit_date.day}/{limit_date.month}/{limit_date.year} {limit_date.hour}:{limit_date.minute}"

    _create_new_task(objective, formatted_creation_date, formatted_limit_date, coin_reward)

def delete_task(objective, creation_date, limit_date, coin_reward):
    conn, cursor = _start_database()

    cursor.execute("""DELETE FROM tasks WHERE 
                   objective = ? AND
                   creation_date = ? AND
                   limit_date = ? AND
                   coin_reward = ?""", (objective, creation_date, limit_date, coin_reward))
    
    conn.commit()
    conn.close()
