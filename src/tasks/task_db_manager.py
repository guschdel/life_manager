"""handle the database connection and transactions"""
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TaskElement:
    objective: str
    creation_date: str
    time_limit: str
    coins: int


def _start_database() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """Opens the database connection and returns the connection and cursor to it"""
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'data.db')
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    _create_table_if_not_exists(cursor)

    return conn, cursor

def _create_table_if_not_exists(cursor):
    """If we start with a plain database, we create one"""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
                objective TEXT,
                creation_date TEXT,
                limit_date TEXT,
                coin_reward INTEGER
                )""")

def _create_new_task(task: TaskElement) -> None:
    """Insert a new task into the database"""
    conn, cursor = _start_database()
    cursor.execute(f"INSERT INTO tasks VALUES(\"{task.objective}\", \"{task.creation_date}\", \"{task.time_limit}\", {task.coins})")
    conn.commit()
    conn.close()

def return_tasks() -> list:
    """Get all tasks stored in the database"""
    conn, cursor = _start_database()

    cursor.execute("SELECT * FROM tasks")
    tasks = []
    data = cursor.fetchall()
    for i in data:
        task = TaskElement(i[0], i[1], i[2], i[3])
        tasks.append(task)
    conn.close()
    return tasks

def create_new_task(objective: str,
                    time_to_finish: str,
                    coin_reward: int) -> None:
    """Actually create the new task"""
    now = datetime.now()
    limit_date = now + timedelta(days=time_to_finish)

    formatted_creation_date = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}"
    formatted_limit_date = f"{limit_date.day}/{limit_date.month}/{limit_date.year} {limit_date.hour}:{limit_date.minute}"
    task = TaskElement(objective, formatted_creation_date, formatted_limit_date, coin_reward)

    _create_new_task(task)

def delete_task(task: TaskElement) -> None:
    """Delete a task from the database"""
    conn, cursor = _start_database()

    cursor.execute("""DELETE FROM tasks WHERE
                   objective = ? AND
                   creation_date = ? AND
                   limit_date = ? AND
                   coin_reward = ?""", (task.objective,
                                        task.creation_date,
                                        task.time_limit,
                                        task.coins))
    conn.commit()
    conn.close()
