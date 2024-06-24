import sqlite3
from datetime import datetime
from .config import  get_db_file
from .utils import fetch_all_as_json,fetch_one_as_json
class TaskDB:
    def __init__(self):
        self.db_file = get_db_file()
    def get_task_by_id(self, task_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task =fetch_one_as_json(cursor)

        connection.close()
        return task

    def get_task_by_name(self, task_name):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tasks WHERE name=?", (task_name,))
        task = cursor.fetchone()

        connection.close()
        return task

    def get_all_tasks(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tasks")
        tasks = fetch_all_as_json(cursor)

        connection.close()
        return tasks

    def insert_task(self, name, created_by, execution_space, custom_type,
                    creation_datetime=None, description=None, notes=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not creation_datetime:
            creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO tasks (name, created_by, creation_datetime, description, notes, execution_space, custom_type)
            VALUES (?, ?, ?, ?, ?, ?,?)
        """, (name, created_by, creation_datetime,description, notes, execution_space, custom_type))

        task_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return task_id


    def create_task(self, task_data):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        query = '''
            INSERT INTO tasks (
                name, created_by, creation_datetime, description, notes, execution_space, custom_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (
            task_data["name"],
            task_data["created_by"],
            task_data["creation_datetime"],
            task_data["description"],
            task_data["notes"],
            task_data["execution_space"],
            task_data["custom_type"]
        ))
        connection.commit()
        connection.close()
        return cursor.lastrowid

    def update_task_status(self, task_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))

        connection.commit()
        connection.close()

    def delete_task(self, task_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))

        connection.commit()
        connection.close()


"""
if __name__ == "__main__":
    db = TaskDB('tasker.db')

    # Example usage
    task_id = db.insert_task('Task 1', 'UserA', 'High', 'Pending', 'Global', 'Custom',
                             description='Sample task description', notes='Sample notes')
    print(f"Inserted task with ID: {task_id}")

    task = db.get_task_by_id(task_id)
    print("Task details:", task)

    db.update_task_status(task_id, 'Completed')
    print("Task status updated.")

    db.delete_task(task_id)
    print("Task deleted.")
"""