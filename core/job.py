import sqlite3
import datetime
import os
import random
import string
import threading
import time

class Job:
    def __init__(self, step_id, command, task_name=None, subtask_name=None, step_name=None):
        self.step_id = step_id
        self.command = command
        self.status = 'pending'
        self.submitted_username = os.getenv('USER') or os.getenv('USERNAME')
        self.submitted_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.running_status = None
        self.submitted_from = os.uname().nodename
        self.submitted_to = None
        self.execution_server = None
        self.submission_server = None
        self.job_name = self.generate_job_name(task_name, subtask_name, step_name)
        self.log_file = f"logs/job_{self.job_name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        self.thread = None

    def generate_job_name(self, task_name, subtask_name, step_name):
        parts = [task_name, subtask_name, step_name, self.submitted_username, self.generate_random_id(4)]
        return '_'.join(filter(None, parts))

    def generate_random_id(self, length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def submit(self):
        self.insert_into_db()
        self.run_job_in_thread()

    def insert_into_db(self):
        connection = sqlite3.connect('tasker.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO jobs (step_id, command, status, submitted_username, submitted_datetime, submitted_from, job_name, log_file, execution_server, submission_server)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.step_id, self.command, self.status, self.submitted_username, self.submitted_datetime, self.submitted_from, self.job_name, self.log_file, self.execution_server, self.submission_server))
        connection.commit()
        connection.close()

    def update_status_in_db(self):
        connection = sqlite3.connect('tasker.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE jobs
            SET status = ?, running_status = ?
            WHERE step_id = ? AND job_name = ?
        ''', (self.status, self.running_status, self.step_id, self.job_name))
        connection.commit()
        connection.close()

    def run_job(self):
        self.status = 'running'
        self.update_status_in_db()
        try:
            result = os.system(self.command)
            self.running_status = 'completed' if result == 0 else 'failed'
            self.status = 'completed'
        except Exception as e:
            self.running_status = f'failed: {e}'
            self.status = 'failed'
        self.update_status_in_db()

    def run_job_in_thread(self):
        self.thread = threading.Thread(target=self.run_job)
        self.thread.start()
        JobMonitor.add_job(self)

class JobMonitor:
    jobs = []

    @staticmethod
    def add_job(job):
        JobMonitor.jobs.append(job)
        if len(JobMonitor.jobs) == 1:
            threading.Thread(target=JobMonitor.monitor_jobs).start()

    @staticmethod
    def monitor_jobs():
        while JobMonitor.jobs:
            for job in JobMonitor.jobs[:]:
                if not job.thread.is_alive():
                    job.update_status_in_db()
                    JobMonitor.jobs.remove(job)
            time.sleep(1)

class SpecialJob(Job):
    def __init__(self, step_id, version, arg_file, task_name=None, subtask_name=None, step_name=None,
                 command_log_file=None, license_key=None, mode=None, job_id=None):
        self.version = version
        self.arg_file = arg_file
        self.command_log_file = command_log_file or self.construct_command_log_file()
        self.license_key = license_key or self.construct_license_key()
        self.mode = mode or self.construct_mode()
        self.job_id = job_id or self.construct_job_id()
        command = self.construct_command()
        super().__init__(step_id, command, task_name, subtask_name, step_name)

    def construct_command(self):
        return f"execute --version {self.version} --arg-file {self.arg_file} --log-file {self.command_log_file} --license {self.license_key} --mode {self.mode} --job-id {self.job_id}"

    def construct_command_log_file(self):
        return f"logs/command_{self.generate_random_id(8)}.log"

    def construct_license_key(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    def construct_mode(self):
        return "default"

    def construct_job_id(self):
        return f"JOB-{self.generate_random_id(12)}"

    def insert_into_db(self):
        connection = sqlite3.connect('tasker.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO jobs (step_id, command, version, arg_file, command_log_file, license_key, mode, job_id, status, submitted_username, submitted_datetime, submitted_from, job_name, log_file, execution_server, submission_server)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.step_id, self.command, self.version, self.arg_file, self.command_log_file, self.license_key, self.mode, self.job_id, self.status, self.submitted_username, self.submitted_datetime, self.submitted_from, self.job_name, self.log_file, self.execution_server, self.submission_server))
        connection.commit()
        connection.close()

# Example usage
if __name__ == "__main__":
    special_job = SpecialJob(step_id=1, version="1.0", arg_file="args.txt")
    special_job.submit()
