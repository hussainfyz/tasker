import sqlite3


class DatabaseHelper:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def select_all(self):
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        connection.close()
        return rows

    def update_value_by_id(self, column_name, value, id_value):
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {self.table_name} SET {column_name} = ? WHERE id = ?", (value, id_value))
        connection.commit()
        connection.close()

    def add_column(self, column_name, column_type):
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {column_name} {column_type}")
        connection.commit()
        connection.close()

    def show_columns_info(self):
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns_info = cursor.fetchall()
        cursor.execute(f"PRAGMA foreign_key_list({self.table_name})")
        foreign_keys_info = cursor.fetchall()
        connection.close()

        column_details = []
        for column in columns_info:
            col_detail = {
                "cid": column[0],
                "name": column[1],
                "type": column[2],
                "notnull": column[3],
                "dflt_value": column[4],
                "pk": column[5]
            }
            col_detail["foreign_keys"] = [
                fk for fk in foreign_keys_info if fk[3] == column[1]
            ]
            column_details.append(col_detail)

        return column_details


# Example usage
if __name__ == "__main__":
    db_helper = DatabaseHelper("tasker.db", "tasks")

    # Select all rows
    all_rows = db_helper.select_all()
    print("All rows:", all_rows)

    # Update a value by ID
    db_helper.update_value_by_id("status", "completed", 1)

    # Add a new column
    db_helper.add_column("new_column", "TEXT")

    # Show columns information
    columns_info = db_helper.show_columns_info()
    for column in columns_info:
        print("Column info:", column)
