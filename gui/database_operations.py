# db/database_operations.py
import sqlite3
import json
from datetime import datetime

def get_tasks():
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_subtasks():
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM subtasks")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_subtasks_by_task_id(task_name):
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()
    cursor.execute("SELECT subtasks.* FROM subtasks JOIN tasks ON subtasks.task_id = tasks.id WHERE tasks.name = ?", (task_name,))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_steps_by_subtask_id(subtask_name):
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()
    cursor.execute("SELECT steps.* FROM steps JOIN subtasks_steps ON steps.id = subtasks_steps.step_id JOIN subtasks ON subtasks.id = subtasks_steps.subtask_id WHERE subtasks.name = ?", (subtask_name,))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def insert_task(name, created_by, creation_datetime, priority, status, duration, description, notes, execution_space, custom_type):
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO tasks (name, created_by, creation_datetime, priority, status, duration, description, notes, execution_space, custom_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, created_by, creation_datetime, priority, status, duration, description, notes, execution_space, custom_type))
    task_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return task_id

def create_task_subtask_association(task_id, subtask_name):
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM subtasks WHERE name = ?", (subtask_name,))
    subtask_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO tasks_subtasks (task_id, subtask_id) VALUES (?, ?)", (task_id, subtask_id))
    connection.commit()
    connection.close()
