import sqlite3

def create_schema():
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_by TEXT,
            creation_datetime TEXT,
            duration TEXT,
            description TEXT,
            notes TEXT,
            execution_space TEXT,
            custom_type TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subtasks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_by TEXT,
            creation_datetime TEXT,
            description TEXT,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY,
            step_name TEXT,
            file_path TEXT,
            function_name TEXT,
            created_by TEXT,
            creation_datetime TEXT,
            description TEXT,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_jobs (
            id INTEGER PRIMARY KEY,
            task_id INTEGER,
            subtask_id INTEGER,
            step_id INTEGER,
            command TEXT,
            name TEXT,
            status TEXT,
            start_datetime TEXT,
            end_datetime TEXT,
            triggered_by TEXT,
            execution_server TEXT,
            submission_server TEXT,
            log_file TEXT,
            FOREIGN KEY (step_id) REFERENCES steps (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_tasks (
            id INTEGER PRIMARY KEY,
            template_task_id INTEGER,
            status TEXT,
            created_datetime TEXT,
            updated_datetime TEXT,
            execution_space TEXT,
            FOREIGN KEY (template_task_id) REFERENCES tasks (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_subtasks (
            id INTEGER PRIMARY KEY,
            template_subtask_id INTEGER,
            parent_task_id INTEGER,
            status TEXT,
            created_datetime TEXT,
            updated_datetime TEXT,
            execution_space TEXT,
            FOREIGN KEY (parent_task_id) REFERENCES queue_tasks (id),
            FOREIGN KEY (template_subtask_id) REFERENCES subtasks (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queue_steps (
            id INTEGER PRIMARY KEY,
            template_task_id INTEGER,
            template_subtask_id INTEGER,
            template_step_id INTEGER,
            parent_task_id INTEGER,
            parent_subtask_id INTEGER,
            status TEXT,
            created_datetime TEXT,
            updated_datetime TEXT,
            execution_space TEXT,
            FOREIGN KEY (template_task_id) REFERENCES steps (tasks),
            FOREIGN KEY (template_subtask_id) REFERENCES steps (subtasks),
            FOREIGN KEY (template_step_id) REFERENCES steps (steps),
            FOREIGN KEY (parent_task_id) REFERENCES steps (queue_tasks),
            FOREIGN KEY (parent_subtask_id) REFERENCES steps (queue_subtasks)
        )
    ''')

    connection.commit()
    connection.close()

def drop_tables():
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()

    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS queue_jobs')
    cursor.execute('DROP TABLE IF EXISTS queue_steps')
    cursor.execute('DROP TABLE IF EXISTS queue_subtasks')
    cursor.execute('DROP TABLE IF EXISTS queue_tasks')
    cursor.execute('DROP TABLE IF EXISTS jobs')
    cursor.execute('DROP TABLE IF EXISTS steps')
    cursor.execute('DROP TABLE IF EXISTS subtasks')
    cursor.execute('DROP TABLE IF EXISTS tasks')

    connection.commit()
    connection.close()

def show_tables():
    connection = sqlite3.connect('tasker.db')
    cursor = connection.cursor()

    # Query to retrieve all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print the names of all tables
    for table in tables:
        print(table[0])

    connection.close()

if __name__ == "__main__":
    drop_tables()
    create_schema()
    show_tables()
