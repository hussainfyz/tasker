import sqlite3
from datetime import datetime

class JobDB:
    def __init__(self, db_file):
        self.db_file = db_file

    def get_job_by_id(self, job_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
        job = cursor.fetchone()

        connection.close()
        return job

    def get_jobs_by_step_id(self, step_id):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM jobs WHERE step_id=?", (step_id,))
        jobs = cursor.fetchall()

        connection.close()
        return jobs

    def insert_job(self, step_id, name, status, triggered_by, execution_server, submission_server,
                   start_datetime=None, end_datetime=None):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if not start_datetime:
            start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO jobs (step_id, name, status, start_datetime, end_datetime, triggered_by,
                              execution_server, submission_server)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (step_id, name, status, start_datetime, end_datetime, triggered_by, execution_server, submission_server))

        job_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return job_id

    def update_job_status(self, job_id, status):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE jobs SET status=? WHERE id=?", (status, job_id))

        connection.commit()
        connection.close()

    def update_job_endtime(self, job_id, end_datetime):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE jobs SET end_datetime=? WHERE id=?", (end_datetime, job_id))

        connection.commit()
        connection.close()


if __name__ == "__main__":
    db = JobDB('tasker.db')

    # Example usage
    step_id = 1  # Assuming this step ID exists in your steps table
    job_id = db.insert_job(step_id, 'JobName', 'Pending', 'UserA', 'ExecutionServer', 'SubmissionServer')
    print(f"Inserted job with ID: {job_id}")

    job = db.get_job_by_id(job_id)
    print("Job details by ID:", job)

    jobs_by_step = db.get_jobs_by_step_id(step_id)
    print("Jobs details by step ID:", jobs_by_step)

    db.update_job_status(job_id, 'Completed')
    print("Job status updated.")

    end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.update_job_endtime(job_id, end_datetime)
    print("Job end datetime updated.")