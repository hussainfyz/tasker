import sqlite3
from datetime import datetime

class QueueSubtasksDB:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_subtask_by_id(self, subtask_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM queue_subtasks WHERE id=?", (subtask_id,))
        subtask = cursor.fetchone()

        connection.close()
        return subtask

    def get_subtasks_by_status(self, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM queue_subtasks WHERE status=?", (status,))
        subtasks = cursor.fetchall()

        connection.close()
        return subtasks

    def insert_subtask(self, subtask_id, task_id, status, created_datetime=None, updated_datetime=None, execution_space=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not created_datetime:
            created_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not updated_datetime:
            updated_datetime = created_datetime

        cursor.execute("""
            INSERT INTO queue_subtasks (id, task_id, status, created_datetime, updated_datetime, execution_space)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (subtask_id, task_id, status, created_datetime, updated_datetime, execution_space))

        connection.commit()
        connection.close()

    def update_subtask_status(self, subtask_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE queue_subtasks SET status=? WHERE id=?", (status, subtask_id))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = QueueSubtasksDB('tasker.db')

    # Example usage
    subtask_id = 1  # Assuming this subtask ID exists in your subtasks table
    task_id = 1  # Assuming this task ID exists in your tasks table
    db.insert_subtask(subtask_id, task_id, 'Pending', execution_space='Global')
    print(f"Inserted subtask with ID: {subtask_id}")

    subtask = db.get_subtask_by_id(subtask_id)
    print("Subtask details by ID:", subtask)

    subtasks_by_status = db.get_subtasks_by_status('Pending')
    print("Subtasks details by status:", subtasks_by_status)

    db.update_subtask_status(subtask_id, 'Completed')
    print("Subtask status updated.")
