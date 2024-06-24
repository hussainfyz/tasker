import sqlite3
from datetime import datetime

class QueueStepsDB:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_step_by_id(self, step_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM queue_steps WHERE id=?", (step_id,))
        step = cursor.fetchone()

        connection.close()
        return step

    def get_steps_by_status(self, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM queue_steps WHERE status=?", (status,))
        steps = cursor.fetchall()

        connection.close()
        return steps

    def insert_step(self, step_id, subtask_id, status, created_datetime=None, updated_datetime=None, execution_space=None, params_list_filename=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not created_datetime:
            created_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not updated_datetime:
            updated_datetime = created_datetime

        cursor.execute("""
            INSERT INTO queue_steps (id, subtask_id, status, created_datetime, updated_datetime, execution_space, params_list_filename)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (step_id, subtask_id, status, created_datetime, updated_datetime, execution_space, params_list_filename))

        connection.commit()
        connection.close()

    def update_step_status(self, step_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE queue_steps SET status=? WHERE id=?", (status, step_id))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = QueueStepsDB('tasker.db')

    # Example usage
    step_id = 1  # Assuming this step ID exists in your steps table
    subtask_id = 1  # Assuming this subtask ID exists in your subtasks table
    params_list_filename = 'params.txt'
    db.insert_step(step_id, subtask_id, 'Pending', execution_space='Global', params_list_filename=params_list_filename)
    print(f"Inserted step with ID: {step_id}")

    step = db.get_step_by_id(step_id)
    print("Step details by ID:", step)

    steps_by_status = db.get_steps_by_status('Pending')
    print("Steps details by status:", steps_by_status)

    db.update_step_status(step_id, 'Completed')
    print("Step status updated.")
