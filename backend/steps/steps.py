import sqlite3
import datetime
import importlib
from db.config import connect_db

class Step:
    def __init__(self, subtask_id, name, function_name, module_path, args=None):
        self.subtask_id = subtask_id
        self.name = name
        self.function_name = function_name
        self.module_path = module_path
        self.args = args or {}
        self.status = 'pending'
        self.start_datetime = None
        self.end_datetime = None
        self.log_file = f"logs/step_{self.name}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
        self.output = None

    def execute(self, outputs):
        self.start_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = 'running'
        self.insert_into_db()
        function = self.get_function()
        if function:
            self.resolve_args(outputs)
            self.run_function(function)
            self.status = 'completed'
        else:
            self.status = 'failed'
        self.end_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.update_status_in_db()
        return self.output

    def resolve_args(self, outputs):
        for key, value in self.args.items():
            if isinstance(value, str) and value.startswith("output:"):
                step_name = value.split("output:")[1]
                self.args[key] = outputs.get(step_name)

    def insert_into_db(self):

        #connection = sqlite3.connect('tasker.db')
        connection=connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO steps (subtask_id, name, function_name, module_path, args, status, start_datetime, log_file, output)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.subtask_id, self.name, self.function_name, self.module_path, str(self.args), self.status, self.start_datetime, self.log_file, self.output))
        connection.commit()
        connection.close()

    def update_status_in_db(self):
        #connection = sqlite3.connect('tasker.db')
        connection=connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE steps
            SET status = ?, end_datetime = ?, log_file = ?, output = ?
            WHERE subtask_id = ? AND name = ?
        ''', (self.status, self.end_datetime, self.log_file, self.output, self.subtask_id, self.name))
        connection.commit()
        connection.close()

    def get_function(self):
        try:
            module = importlib.import_module(self.module_path)
            function = getattr(module, self.function_name)
            return function
        except (ImportError, AttributeError) as e:
            print(f"Error loading function: {e}")
            return None

    def run_function(self, function):
        try:
            self.output = function(**self.args)
        except Exception as e:
            print(f"Error running function: {e}")
            self.status = f'failed: {e}'
