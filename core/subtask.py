import sqlite3
import datetime
from step import Step

class SubTask:
    def __init__(self, task_id, name, steps):
        self.task_id = task_id
        self.name = name
        self.steps = steps  # List of Step objects
        self.status = 'pending'
        self.start_datetime = None
        self.end_datetime = None
        self.description = ''
        self.priority = ''
        self.duration = 0
        self.notes = ''

    def submit(self):
        self.start_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.insert_into_db()
        self.run_steps()

    def run_steps(self):
        outputs = {}
        for step in self.steps:
            output = step.execute(outputs)
            outputs[step.name] = output

        self.status = 'completed'
        self.end_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.update_status_in_db()

    def insert_into_db(self):
        connection = sqlite3.connect('tasker.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO subtasks (task_id, name, status, start_datetime, description, priority, duration, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.task_id, self.name, self.status, self.start_datetime, self.description, self.priority, self.duration, self.notes))
        connection.commit()
        connection.close()

    def update_status_in_db(self):
        connection = sqlite3.connect('tasker.db')
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE subtasks
            SET status = ?, end_datetime = ?
            WHERE task_id = ? AND name = ?
        ''', (self.status, self.end_datetime, self.task_id, self.name))
        connection.commit()
        connection.close()
