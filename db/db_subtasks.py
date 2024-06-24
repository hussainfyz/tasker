import sqlite3
from datetime import datetime
from .config import get_db_file
from .utils import fetch_all_as_json
class SubtaskDB:
    def __init__(self):
        self.db_file = get_db_file()

    def get_all_subtasks(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM subtasks")
        subtasks = fetch_all_as_json(cursor)
        connection.close()
        return subtasks

    def get_subtask_by_id(self, subtask_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM subtasks WHERE id=?", (subtask_id,))
        subtask = cursor.fetchone()

        connection.close()
        return subtask

    def get_subtasks_by_task_id(self, task_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM subtasks WHERE task_id=?", (task_id,))
        subtasks = cursor.fetchall()

        connection.close()
        return subtasks

    def get_subtask_by_name(self, subtask_name):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM subtasks WHERE name=?", (subtask_name,))
        subtask = fetch_all_as_json(cursor)

        connection.close()
        return subtask

    def insert_subtask(self, name, created_by,creation_datetime=None, description=None, notes=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not creation_datetime:
            creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO subtasks (name, created_by, creation_datetime,
                                 description, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (name, created_by, creation_datetime, description, notes))

        subtask_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return subtask_id

    def update_subtask_status(self, subtask_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE subtasks SET status=? WHERE id=?", (status, subtask_id))

        connection.commit()
        connection.close()

    def delete_subtask(self, subtask_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM subtasks WHERE id=?", (subtask_id,))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = SubtaskDB('tasker.db')

    # Example usage
    task_id = 1  # Assuming this task ID exists in your tasks table
    subtask_id = db.insert_subtask('Subtask 1', task_id, 'UserB', 'Medium', 'Pending', 'Global', 'Custom',
                                   description='Sample subtask description', notes='Sample notes')
    print(f"Inserted subtask with ID: {subtask_id}")

    subtask = db.get_subtask_by_id(subtask_id)
    print("Subtask details by ID:", subtask)

    subtask_by_name = db.get_subtask_by_name('Subtask 1')
    print("Subtask details by name:", subtask_by_name)

    db.update_subtask_status(subtask_id, 'Completed')
    print("Subtask status updated.")

    db.delete_subtask(subtask_id)
    print("Subtask deleted.")
