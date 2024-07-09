import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton,
    QSplitter, QListWidgetItem, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QRadioButton, QDateTimeEdit, QLineEdit

class TaskDetailsDialog(QDialog):
    def __init__(self, task_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")
        self.setWindowTitle(f"Task Details: Submit Task")
        self.setGeometry(300, 300, 600, 900)
        self.task_id = task_id

        layout = QVBoxLayout()

        # Example: Fetch task details from the database based on task_id
        task_name = "Task Name"
        description = "Task Description"

        task_name_label = QLabel(f"<h1>{task_name}</h1>")
        description_label = QLabel(description)

        layout.addWidget(task_name_label)
        layout.addWidget(description_label)

        # Example: Fetch subtasks and steps from the database based on task_id
        subtasks = ["Subtask 1", "Subtask 2", "Subtask 3"]
        steps = [
            {"name": "Step 1", "param_name": "Param 1"},
            {"name": "Step 2", "param_name": "Param 2"},
            {"name": "Step 3", "param_name": "Param 3"}
        ]

        subtask_label = QLabel("Subtasks:")
        layout.addWidget(subtask_label)

        for subtask in subtasks:
            subtask_label = QLabel(subtask)
            layout.addWidget(subtask_label)

        step_label = QLabel("Steps:")
        layout.addWidget(step_label)

        for step in steps:
            step_label = QLabel(f"{step['name']} - Param Name: {step['param_name']}")
            layout.addWidget(step_label)

            # Example: Add input fields for step parameters
            param_input = QLineEdit()
            layout.addWidget(param_input)

        # Schedule Later Option
        self.schedule_radio = QRadioButton("Schedule Later")
        layout.addWidget(self.schedule_radio)

        self.date_time_edit = QDateTimeEdit()
        layout.addWidget(self.date_time_edit)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_task_details)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def submit_task_details(self):
        # Example: Gather task details and parameters
        task_details = {
            "task_id": self.task_id,
            "scheduled": self.schedule_radio.isChecked(),
            "scheduled_time": self.date_time_edit.dateTime().toString(Qt.ISODate),
            # Add other parameters as needed
        }

        print(task_details)  # Print JSON representation of task details
        self.accept()  # Close the dialog


class TaskItemWidget(QWidget):
    def __init__(self, task_name, description, subtask_count, step_count):
        super().__init__()

        layout = QVBoxLayout()

        # Task Name
        self.task_name = QLabel(f"<b>{task_name}</b>")

        # Description
        self.description = QLabel(description)
        self.task_id=10
        # Counts
        self.counts = QLabel(f"Subtasks: {subtask_count} | Steps: {step_count}")

        # Links
        self.view_link = QLabel('<a href="#">View</a>')
        self.doc_link = QLabel('<a href="#">Documentation</a>')
        self.help_link = QLabel('<a href="#">Help</a>')
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.open_task_details_dialog)

        for link in [self.view_link, self.doc_link, self.help_link]:
            link.setOpenExternalLinks(True)

        link_layout = QHBoxLayout()
        link_layout.addWidget(self.view_link)
        link_layout.addWidget(self.doc_link)
        link_layout.addWidget(self.help_link)

        layout.addWidget(self.task_name)
        layout.addWidget(self.description)
        layout.addWidget(self.counts)
        layout.addLayout(link_layout)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

        # Set the stylesheet for better appearance and hover effect
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid red;
                border-radius: 1px;
                padding: 10px;
                margin: 2px;
            }
            QWidget:hover {
                background-color: #e0f7fa;
                border-color: #80deea;
            }
            QLabel {
                font-size: 14px;
                color: #333;
                border: 1px solid #0077b3;
            }
            QLabel:hover {
                color: #00796b;
            }
            QLabel a {
                text-decoration: none;
                color: #00796b;
            }
             QPushButton {
                background-color: #ffccbc;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffab91;
            }
        """)

    def open_task_details_dialog(self):
        #dialog = TaskDetailsDialog(self.task_id,self.description,10,10)
        dialog = TaskDetailsDialog(self.task_id)
        dialog.exec_()
class TaskDetailsDialog1(QDialog):
    def __init__(self, task_name, description, subtask_count, step_count):
        super().__init__()

        self.setWindowTitle(f"Task Details: {task_name}")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        self.task_name = QLabel(f"<h1>{task_name}</h1>")
        self.description = QLabel(description)
        self.counts = QLabel(f"<p>Subtasks: {subtask_count} | Steps: {step_count}</p>")

        layout.addWidget(self.task_name)
        layout.addWidget(self.description)
        layout.addWidget(self.counts)

        self.setLayout(layout)


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout()

        # Top Layout: Splitter with tasks on the left and details on the right
        top_layout = QSplitter(Qt.Horizontal)

        # Left Side: Running tasks and tasks in queue
        left_side_layout = QVBoxLayout()

        running_tasks_label = QLabel("Running Tasks")
        self.running_tasks_list = QListWidget()
        running_tasks_label.setStyleSheet("background-color: #80deea; padding: 5px; font-weight: bold;")
        self.running_tasks_list.setStyleSheet("background-color: #ffffff;")

        queue_tasks_label = QLabel("Tasks in Queue")
        self.queue_tasks_list = QListWidget()
        queue_tasks_label.setStyleSheet("background-color: #4dd0e1; padding: 5px; font-weight: bold;")
        self.queue_tasks_list.setStyleSheet("background-color: #ffffff;")

        left_side_layout.addWidget(running_tasks_label)
        left_side_layout.addWidget(self.running_tasks_list)
        left_side_layout.addWidget(queue_tasks_label)
        left_side_layout.addWidget(self.queue_tasks_list)

        left_widget = QWidget()
        left_widget.setLayout(left_side_layout)
        left_widget.setMaximumWidth(300)  # Set the maximum width of the left side

        # Right Side: List of tasks from the DB
        right_side_layout = QVBoxLayout()

        db_tasks_label = QLabel("Tasks from DB")
        self.db_tasks_list = QListWidget()
        self.db_tasks_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #b3e6ff;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 2px;
                border: 2px solid #0077b3;
            }
            QListWidget::item:selected {
                background-color: #e0f7fa;
                border-color: #80deea;
                border: 5px solid #0077b3;
            }
        """)
        # Example tasks
        example_tasks = [
            ("Task1", "Description for Task1", 3, 10),
            ("Task2", "Description for Task2", 5, 15),
            ("Task3", "Description for Task3", 2, 8)
        ]

        for task in example_tasks:
            task_item = QListWidgetItem()

            task_widget = TaskItemWidget(*task)
            task_item.setSizeHint(task_widget.sizeHint())
            self.db_tasks_list.addItem(task_item)
            self.db_tasks_list.setItemWidget(task_item, task_widget)

        db_tasks_label.setStyleSheet("background-color: #ffab91; padding: 5px; font-weight: bold;")
        #self.db_tasks_list.setStyleSheet("background-color: #ffffff;")

        db_layout = QVBoxLayout()
        db_layout.addWidget(db_tasks_label)
        db_layout.addWidget(self.db_tasks_list)

        run_task_button = QPushButton("Run Selected Task")
        run_task_button.clicked.connect(self.run_selected_task)
        run_task_button.setStyleSheet("background-color: #ffccbc; padding: 10px; font-weight: bold;")

        db_layout.addWidget(run_task_button)

        right_side_layout.addLayout(db_layout)

        right_widget = QWidget()
        right_widget.setLayout(right_side_layout)

        top_layout.addWidget(left_widget)
        top_layout.addWidget(right_widget)

        # Footer Layout: Information Section
        footer_layout = QHBoxLayout()
        footer_label = QLabel("Developed by: Your Name | Documentation | Help")
        footer_label.setStyleSheet(
            "background-color: #cfd8dc; padding: 10px; font-weight: bold; text-align: center; width: 100%;")
        footer_layout.addWidget(footer_label)

        footer_widget = QWidget()
        footer_widget.setLayout(footer_layout)
        footer_widget.setFixedHeight(50)  # Set a fixed height for the footer

        # Combine Top and Footer Layouts
        main_layout.addWidget(top_layout)
        main_layout.addWidget(footer_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply gradient background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0f7fa, stop:1 #80deea);
            }
        """)

        # Populate the running and queued tasks with dummy data
        self.populate_running_tasks()
        self.populate_queue_tasks()

    def fetch_dummy_tasks(self):
        return [
            (1, "Running Task 1"),
            (2, "Running Task 2"),
            (3, "Queue Task 1"),
            (4, "Queue Task 2")
        ]

    def populate_running_tasks(self):
        tasks = self.fetch_dummy_tasks()[:2]
        for task_id, task_name in tasks:
            item = QListWidgetItem(f"ID: {task_id} | Name: {task_name}")
            self.running_tasks_list.addItem(item)

    def populate_queue_tasks(self):
        tasks = self.fetch_dummy_tasks()[2:]
        for task_id, task_name in tasks:
            item = QListWidgetItem(f"ID: {task_id} | Name: {task_name}")
            self.queue_tasks_list.addItem(item)

    def run_selected_task(self):
        selected_task_item = self.db_tasks_list.currentItem()
        if selected_task_item:
            task_widget = self.db_tasks_list.itemWidget(selected_task_item)
            task_name = task_widget.task_name.text()
            description = task_widget.description.text()
            counts = task_widget.counts.text()

            subtask_count, step_count = map(int, counts.split("|")[0].split(":")[1].strip()), int(
                counts.split("|")[1].split(":")[1].strip())

            # Add to queue
            queue_item = QListWidgetItem()
            queue_item.setSizeHint(task_widget.sizeHint())
            self.queue_tasks_list.addItem(queue_item)
            self.queue_tasks_list.setItemWidget(queue_item, task_widget)

            # Remove from db list
            self.db_tasks_list.takeItem(self.db_tasks_list.row(selected_task_item))

            # Open Task Details Dialog
            self.open_task_details(task_name, description, subtask_count, step_count)

    def open_task_details(self, task_name, description, subtask_count, step_count):
        details_dialog = TaskDetailsDialog(task_name, description, subtask_count, step_count)
        details_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
