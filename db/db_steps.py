import sqlite3
from datetime import datetime
from .config import get_db_file
from .utils import fetch_all_as_json,fetch_one_as_json
class StepDB:
    def __init__(self):
        self.db_file = get_db_file()

    def get_step_ids_by_subtask_id(self, subtask_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        query = """
        SELECT step_id
        FROM subtasks_steps
        WHERE subtask_id = ?
        """
        cursor = connection.execute(query, (subtask_id,))
        tempdata=fetch_all_as_json(cursor)
        step_ids = [row["step_id"] for row in tempdata]
        #step_ids=fetch_all_as_json(step_ids)
        return step_ids
    def get_all_steps(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM steps")
        tasks = fetch_all_as_json(cursor)

        connection.close()
        return tasks
    def get_step_by_id(self, step_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM steps WHERE id=?", (step_id,))
        step =fetch_one_as_json(cursor)

        connection.close()
        return step

    def get_step_by_step_name(self, stepname):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM steps WHERE step_name=?", (stepname,))
        step = fetch_all_as_json(cursor)


        connection.close()
        return step
    def insert_step(self,step_name, file_path, function_name, created_by,creation_datetime=None, description=None, notes=None, log_file=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not creation_datetime:
            creation_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO steps (step_name,file_path, function_name, created_by, creation_datetime,description, notes, log_file)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (step_name,file_path, function_name, created_by, creation_datetime, description, notes, log_file))

        step_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return step_id

    def update_step_status(self, step_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE steps SET status=? WHERE id=?", (status, step_id))

        connection.commit()
        connection.close()

    def delete_step(self, step_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM steps WHERE id=?", (step_id,))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = StepDB('tasker.db')
    db.get_all_steps()
    exit()
    # Example usage
    subtask_id = 1  # Assuming this subtask ID exists in your subtasks table
    step_id = db.insert_step('/path/to/file.py', 'function_name', 'UserA', 'High', 'Pending', 'Global', 'Custom',
                             description='Sample step description', notes='Sample notes')
    print(f"Inserted step with ID: {step_id}")

    step = db.get_step_by_id(step_id)
    print("Step details by ID:", step)

    steps_by_subtask = db.get_steps_by_subtask_id(subtask_id)
    print("Steps details by subtask ID:", steps_by_subtask)

    db.update_step_status(step_id, 'Completed')
    print("Step status updated.")

    db.delete_step(step_id)
    print("Step deleted.")
