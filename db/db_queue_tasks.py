import sqlite3
from datetime import datetime


import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
print(tasker_dir)
sys.path.insert(0, tasker_dir)
from db.config import get_db_file
from db.utils import fetch_all_as_json,fetch_one_as_json




class QueueTasksDB:
    def __init__(self):
        self.db_file = get_db_file()
        self.conn = sqlite3.connect(self.db_file)


    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS queue_tasks (
                    id INTEGER PRIMARY KEY,
                    template_task_id INTEGER,
                    status TEXT,
                    created_datetime TEXT,
                    updated_datetime TEXT,
                    execution_space TEXT,
                    FOREIGN KEY (template_task_id) REFERENCES tasks (id)
                )
            ''')

    def get_running_tasks(self, limit=5):
        query = '''
            SELECT id, template_task_id, status, created_datetime, updated_datetime, execution_space
            FROM queue_tasks
            WHERE status = 'running'
            LIMIT ?
        '''
        with self.conn:
            cursor = self.conn.execute(query, (limit,))
            rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_pending_tasks(self, limit=5):
        query = '''
            SELECT id, template_task_id, status, created_datetime, updated_datetime, execution_space
            FROM queue_tasks
            WHERE status = 'pending'
            LIMIT ?
        '''
        with self.conn:
            cursor = self.conn.execute(query, (limit,))
            rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_all_tasks(self):
        query = '''
            SELECT id, template_task_id, status, created_datetime, updated_datetime, execution_space
            FROM queue_tasks
        '''
        with self.conn:
            cursor = self.conn.execute(query)
            rows = cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def create_task(self, task):
        query = '''
            INSERT INTO queue_tasks (template_task_id, status, created_datetime, updated_datetime, execution_space)
            VALUES (?, ?, ?, ?, ?)
        '''
        with self.conn:
            cursor = self.conn.execute(query, (
                task['template_task_id'], task.get('status', 'pending'),
                task['created_datetime'], task['updated_datetime'], task['execution_space']
            ))
        return cursor.lastrowid

    def _row_to_dict(self, row):
        return {
            'id': row[0],
            'template_task_id': row[1],
            'status': row[2],
            'created_datetime': row[3],
            'updated_datetime': row[4],
            'execution_space': row[5]
        }


    def get_task_by_id(self, task_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM queue_tasks WHERE id=?", (task_id,))
        task = cursor.fetchone()

        connection.close()
        return task

    def get_tasks_by_status(self, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM queue_tasks WHERE status=?", (status,))
        tasks = cursor.fetchall()

        connection.close()
        return tasks

    def insert_task(self, task_id, status, created_datetime=None, updated_datetime=None, execution_space=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not created_datetime:
            created_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not updated_datetime:
            updated_datetime = created_datetime

        cursor.execute("""
            INSERT INTO queue_tasks (id, status, created_datetime, updated_datetime, execution_space)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, status, created_datetime, updated_datetime, execution_space))

        connection.commit()
        connection.close()

    def update_task_status(self, task_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE queue_tasks SET status=? WHERE id=?", (status, task_id))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = QueueTasksDB()

    # Example usage
    task_id = 1  # Assuming this task ID exists in your tasks table
    #db.insert_task(task_id, 'Pending', execution_space='Global')
    #print(f"Inserted task with ID: {task_id}")

    #task = db.get_task_by_id(task_id)
    #print("Task details by ID:", task)

    #tasks_by_status = db.get_tasks_by_status('Pending')
    #print("Tasks details by status:", tasks_by_status)

    #db.update_task_status(task_id, 'Completed')
    print("Task status updated.")
    x={
        'template_task_id': 1,
        'status': 'running',
        'created_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'execution_space': 'Space1'
    }
    obj=QueueTasksDB()
    obj.create_task(x)

    x1={
        'template_task_id': 2,
        'status': 'pending',
        'created_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'execution_space': 'Space2'
    }
    obj.create_task(x1)

    running_tasks = obj.get_running_tasks()
    pending_tasks = obj.get_pending_tasks()
    all_tasks = obj.get_all_tasks()

    print('Running Tasks:', running_tasks)
    print('Pending Tasks:', pending_tasks)
    print('All Tasks:', all_tasks)

