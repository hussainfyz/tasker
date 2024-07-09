# db/database_operations.py
import sqlite3,json
from datetime import datetime
from .utils import fetch_all_as_json
from .db_tasks import TaskDB
from .db_subtasks import SubtaskDB
from .db_steps import StepDB
from .db_tasks import TaskDB
from .config import get_db_file
    #exit()
    #result = [dict_factory(cursor, row) for row in rows]
    #return json.dumps(result, default=str)
def connect_db():
    return sqlite3.connect(get_db_file())

def dict_factory(cursor, row):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}

def get_all_tasks():
    return TaskDB().get_all_tasks()

def get_all_subtasks():
    return SubtaskDB().get_all_subtasks()
def get_subtasks_by_task_id(task_id):
    connection = connect_db()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("""
        SELECT subtasks.* 
        FROM subtasks 
        JOIN tasks_subtasks ON subtasks.id = tasks_subtasks.subtask_id 
        WHERE tasks_subtasks.task_id = ?
    """, (task_id,))
    subtasks = cursor.fetchall()
    connection.close()
    print("All subtasks for the task id",task_id)
    print(subtasks)
    return subtasks

def get_steps_by_subtask_id(subtask_id):
    connection = connect_db()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("""
        SELECT steps.* 
        FROM steps 
        JOIN subtasks_steps ON steps.id = subtasks_steps.step_id 
        WHERE subtasks_steps.subtask_id = ?
    """, (subtask_id,))
    steps = cursor.fetchall()
    print("All steps for the subtask",steps)
    connection.close()
    return steps

def insert_step(file_path, function_name,description, created_by, priority=1, status='created', duration=0,notes=''):
    connection = connect_db()
    cursor = connection.cursor()
    creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO steps (file_path, function_name, created_by, creation_datetime, priority, status, duration, description, notes, log_file)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (file_path, function_name, created_by, creation_datetime, priority, status, duration, description, notes, ""))
    step_id = cursor.lastrowid

    connection.commit()
    print("Inserted")
    print(get_step_byid(step_id))
    connection.close()
    return step_id

def insert_step_param(step_id, param_name, param_value):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO step_params (step_id, param_name, param_value)
        VALUES (?, ?, ?)
    ''', (step_id, param_name, param_value))
    connection.commit()
    connection.close()

def insert_subtask(name, task_id, created_by, priority, status, duration, description, notes):
    connection = connect_db()
    cursor = connection.cursor()
    creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO subtasks (name, task_id, created_by, creation_datetime, priority, status, duration, description, notes, log_directory)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, task_id, created_by, creation_datetime, priority, status, duration, description, notes, ""))
    subtask_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return subtask_id

def insert_task(name, created_by, priority, status, duration, description, notes, execution_space, custom_type):
    connection = connect_db()
    cursor = connection.cursor()
    creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO tasks (name, created_by, creation_datetime, priority, status, duration, description, notes, execution_space, custom_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, created_by, creation_datetime, priority, status, duration, description, notes, execution_space, custom_type))
    task_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return task_id

def create_task_subtask_association(task_id, subtask_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO tasks_subtasks (task_id, subtask_id)
        VALUES (?, ?)
    ''', (task_id, subtask_id))
    connection.commit()
    connection.close()


def get_step_id_by_name(function_name):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM steps WHERE function_name = ?", (function_name,))
    step_id = cursor.fetchone()
    connection.close()
    return step_id[0] if step_id else None
def get_step_params_by_step_id(step_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM step_params WHERE step_id = ?", (step_id,))
    step_params = cursor.fetchall()
    connection.close()
    return step_params
def get_step_byid(id):
    connection = connect_db()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM steps where id="+str(id))
    tasks = fetch_all_as_json(cursor)
    connection.close()
    return tasks

def get_all_steps():
    StepDB().get_all_steps()

def create_subtask_step_association(subtask_id, step_id):
    connection = connect_db()
    print("Recieved1")
    print(subtask_id)
    print(step_id)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO subtasks_steps (subtask_id, step_id)
        VALUES (?, ?)
    ''', (subtask_id, step_id))
    connection.commit()
    connection.close()
# db/database_operations.py


# db/database_operations.py


def get_subtasks_by_task_name(task_name):
    connection = connect_db()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("""
        SELECT subtasks.* 
        FROM subtasks 
        JOIN tasks_subtasks ON subtasks.id = tasks_subtasks.subtask_id 
        JOIN tasks ON tasks_subtasks.task_id = tasks.id 
        WHERE tasks.name = ?
    """, (task_name,))
    subtasks = cursor.fetchall()
    connection.close()
    return subtasks

def get_steps_by_subtask_name(subtask_name):
    connection = connect_db()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute("""
        SELECT steps.* 
        FROM steps 
        JOIN subtasks_steps ON steps.id = subtasks_steps.step_id 
        JOIN subtasks ON subtasks_steps.subtask_id = subtasks.id 
        WHERE subtasks.name = ?
    """, (subtask_name,))
    steps = cursor.fetchall()
    connection.close()
    return steps
