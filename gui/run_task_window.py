# tabs/run_task_tab.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QSplitter, QListWidget,
    QListWidgetItem, QLabel, QPushButton, QWidget, QScrollArea, QFrame
)
import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
print(tasker_dir)
sys.path.insert(0, tasker_dir)


# tabs/run_task_tab.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QListWidget,
    QListWidgetItem, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

# Ensure the parent directory is in the system path for module imports
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, tasker_dir)

from db.db_queue_tasks import QueueTasksDB  # Adjust import paths as necessary
from db.db_tasks import TaskDB

class RunTaskTab(QWidget):
    def __init__(self, parent=None):
        super(RunTaskTab, self).__init__(parent)
        self.setWindowTitle("Run Task")
        self.setGeometry(300, 300, 1200, 800)
        self.setStyleSheet(self.load_stylesheet())
        self.queue_task_db = QueueTasksDB()
        self.task_db = TaskDB()

        self.layout = QHBoxLayout(self)
        self.setup_left_panel()
        self.setup_right_panel()

    def load_stylesheet(self):
        return """
        QWidget {
            background-color: #282828;
            color: white;
        }
        QLabel, QPushButton {
            font-size: 14px;
            color: white;
        }
        QPushButton {
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QListWidget {
            background-color: #383838;
            border: none;
            font-size: 14px;
            color: white;
        }
        QFrame {
            background-color: #383838;
        }
        """

    def setup_left_panel(self):
        self.left_splitter = QSplitter(Qt.Vertical)

        # Running tasks
        self.running_tasks_list = QListWidget()
        self.populate_task_list(self.running_tasks_list, "running")

        self.running_tasks_label = QLabel("Running Tasks (Max 5)")
        self.running_tasks_layout = QVBoxLayout()
        self.running_tasks_layout.addWidget(self.running_tasks_label)
        self.running_tasks_layout.addWidget(self.running_tasks_list)
        running_tasks_widget = QWidget()
        running_tasks_widget.setLayout(self.running_tasks_layout)
        self.left_splitter.addWidget(running_tasks_widget)

        # Pending tasks
        self.pending_tasks_list = QListWidget()
        self.populate_task_list(self.pending_tasks_list, "pending")

        self.pending_tasks_label = QLabel("Pending Tasks (Max 5)")
        self.pending_tasks_layout = QVBoxLayout()
        self.pending_tasks_layout.addWidget(self.pending_tasks_label)
        self.pending_tasks_layout.addWidget(self.pending_tasks_list)
        pending_tasks_widget = QWidget()
        pending_tasks_widget.setLayout(self.pending_tasks_layout)
        self.left_splitter.addWidget(pending_tasks_widget)

        self.layout.addWidget(self.left_splitter)

    def setup_right_panel(self):
        self.right_layout = QVBoxLayout()

        self.available_tasks_label = QLabel("All Available Tasks")
        self.available_tasks_list = QListWidget()
        self.populate_task_list(self.available_tasks_list, "all")

        self.right_layout.addWidget(self.available_tasks_label)
        self.right_layout.addWidget(self.available_tasks_list)

        self.layout.addLayout(self.right_layout)

    def populate_task_list(self, list_widget, task_type):
        tasks = []
        if task_type == "running":
            tasks = self.queue_task_db.get_running_tasks(limit=5)
        elif task_type == "pending":
            tasks = self.queue_task_db.get_pending_tasks(limit=5)
        elif task_type == "all":
            tasks = self.task_db.get_all_tasks()

        for task in tasks:
            item = QListWidgetItem()
            item_widget = self.create_task_item_widget(task, task_type)
            item.setSizeHint(item_widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, item_widget)

    def create_task_item_widget(self, task, task_type):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        widget.setStyleSheet("border: 1px solid #505050; border-radius: 5px; padding: 10px;")
        print(task)
        task=TaskDB().get_task_by_id(task['template_task_id'])
        # Task Name
        name_label = QLabel(task['name'])
        name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(name_label)

        # Task Description
        desc_label = QLabel(task["description"])
        desc_label.setStyleSheet("font-size: 14px; color: #A0A0A0;")
        layout.addWidget(desc_label)

        # Task Notes
        notes_label = QLabel(task.get("notes", ""))
        notes_label.setStyleSheet("font-size: 12px; color: #A0A0A0;")
        layout.addWidget(notes_label)

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        run_button = QLabel('<a href="#">Run</a>')
        run_button.setOpenExternalLinks(False)
        run_button.linkActivated.connect(lambda: self.run_task(task))
        buttons_layout.addWidget(run_button)

        config_button = QLabel('<a href="#">Config</a>')
        config_button.setOpenExternalLinks(False)
        config_button.linkActivated.connect(lambda: self.config_task(task))
        buttons_layout.addWidget(config_button)

        view_details_button = QLabel('<a href="#">View Details</a>')
        view_details_button.setOpenExternalLinks(False)
        view_details_button.linkActivated.connect(lambda: self.view_task_details(task))
        buttons_layout.addWidget(view_details_button)

        lock_button = QLabel('<a href="#">Lock</a>')
        lock_button.setOpenExternalLinks(False)
        lock_button.linkActivated.connect(lambda: self.lock_task(task))
        buttons_layout.addWidget(lock_button)

        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

        return widget

    def run_task(self, task):
        # Implement the function to run the task
        print(f"Running task: {task['name']}")

    def config_task(self, task):
        # Implement the function to configure the task
        print(f"Configuring task: {task['name']}")

    def view_task_details(self, task):
        # Implement the function to view task details
        print(f"Viewing details for task: {task['name']}")

    def lock_task(self, task):
        # Implement the function to lock the task
        print(f"Locking task: {task['name']}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RunTaskTab()
    window.show()
    sys.exit(app.exec_())
