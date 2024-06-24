# db/db_step_params.py
import sqlite3
from .config import get_db_file
class StepParamDB:
    def __init__(self):
        self.connection = sqlite3.connect(get_db_file())
        self.connection.row_factory = sqlite3.Row

    def get_params_by_step_id(self, step_id):
        query = """
        SELECT param_name, param_value
        FROM step_params
        WHERE step_id = ?
        """
        cursor = self.connection.execute(query, (step_id,))
        return cursor.fetchall()
