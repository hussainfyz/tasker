import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QTimer

# Dummy functions returning JSON-like lists
def fetch_tasks():
    return [
        {"id": 1, "name": "Task 1", "created_by": "User A", "status": "Pending"},
        {"id": 2, "name": "Task 2", "created_by": "User B", "status": "In Progress"},
    ]

def fetch_queue_tasks():
    return [
        {"id": 1, "template_task_id": 1, "status": "Pending", "created_datetime": "2023-07-01", "updated_datetime": "2023-07-02", "execution_space": "Server A"},
        {"id": 2, "template_task_id": 2, "status": "In Progress", "created_datetime": "2023-07-01", "updated_datetime": "2023-07-02", "execution_space": "Server B"},
    ]

def fetch_subtasks_for_task(task_id):
    if task_id == 1:
        return [
            {"id": 1, "name": "Subtask 1.1", "created_by": "User A1", "status": "Pending"},
            {"id": 2, "name": "Subtask 1.2", "created_by": "User A2", "status": "Completed"},
        ]
    elif task_id == 2:
        return [
            {"id": 3, "name": "Subtask 2.1", "created_by": "User B1", "status": "In Progress"},
        ]
    return []

def fetch_steps_for_subtask(subtask_id):
    if subtask_id == 1:
        return [
            {"id": 1, "step_name": "Step 1.1.1", "file_path": "/path/to/file1", "function_name": "func1", "status": "Pending"},
        ]
    elif subtask_id == 2:
        return [
            {"id": 2, "step_name": "Step 1.2.1", "file_path": "/path/to/file2", "function_name": "func2", "status": "Completed"},
        ]
    elif subtask_id == 3:
        return [
            {"id": 3, "step_name": "Step 2.1.1", "file_path": "/path/to/file3", "function_name": "func3", "status": "In Progress"},
        ]
    return []

class TaskMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_data()

    def initUI(self):
        self.setWindowTitle('Task Monitor')

        self.layout = QVBoxLayout()

        self.tasks_label = QLabel('Tasks')
        self.layout.addWidget(self.tasks_label)

        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(4)
        self.tasks_table.setHorizontalHeaderLabels(['ID', 'Name', 'Created By', 'Status'])
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.tasks_table)

        self.queue_tasks_label = QLabel('Queue Tasks')
        self.layout.addWidget(self.queue_tasks_label)

        self.queue_tasks_table = QTableWidget()
        self.queue_tasks_table.setColumnCount(6)
        self.queue_tasks_table.setHorizontalHeaderLabels(['ID', 'Template Task ID', 'Status', 'Created', 'Updated', 'Execution Space'])
        self.queue_tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.queue_tasks_table)

        self.setLayout(self.layout)

        # Setup timer to refresh data every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(5000)

    def update_data(self):
        self.update_tasks()
        self.update_queue_tasks()

    def update_tasks(self):
        tasks = fetch_tasks()
        self.tasks_table.setRowCount(len(tasks))
        for row_idx, task in enumerate(tasks):
            self.tasks_table.setItem(row_idx, 0, QTableWidgetItem(str(task['id'])))
            self.tasks_table.setItem(row_idx, 1, QTableWidgetItem(task['name']))
            self.tasks_table.setItem(row_idx, 2, QTableWidgetItem(task['created_by']))
            self.tasks_table.setItem(row_idx, 3, QTableWidgetItem(task['status']))

    def update_queue_tasks(self):
        queue_tasks = fetch_queue_tasks()
        self.queue_tasks_table.setRowCount(len(queue_tasks))
        for row_idx, task in enumerate(queue_tasks):
            self.queue_tasks_table.setItem(row_idx, 0, QTableWidgetItem(str(task['id'])))
            self.queue_tasks_table.setItem(row_idx, 1, QTableWidgetItem(str(task['template_task_id'])))
            self.queue_tasks_table.setItem(row_idx, 2, QTableWidgetItem(task['status']))
            self.queue_tasks_table.setItem(row_idx, 3, QTableWidgetItem(task['created_datetime']))
            self.queue_tasks_table.setItem(row_idx, 4, QTableWidgetItem(task['updated_datetime']))
            self.queue_tasks_table.setItem(row_idx, 5, QTableWidgetItem(task['execution_space']))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskMonitor()
    ex.show()
    sys.exit(app.exec_())
