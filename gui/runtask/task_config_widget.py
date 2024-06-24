import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
print(tasker_dir)
sys.path.insert(0, tasker_dir)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QTextEdit, QComboBox
from gui.runtask.task_scheduler import TaskScheduler
from gui.runtask.task_parameters import TaskParameters


class TaskConfigWidget(QWidget):
    def __init__(self):
        super(TaskConfigWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Task Configuration")
        self.layout.addWidget(self.title)

        self.form_layout = QFormLayout()

        self.task_name = QLineEdit()
        self.run_directory = QLineEdit()
        self.log_folder = QLineEdit()
        self.notes = QTextEdit()
        self.notes.setStyleSheet("color: blue;")
        self.execution_space = QComboBox()
        self.execution_space.addItems(["Space 1", "Space 2", "Space 3"])  # Example items

        self.form_layout.addRow("Task Name:", self.task_name)
        self.form_layout.addRow("Run Directory:", self.run_directory)
        self.form_layout.addRow("Log Folder:", self.log_folder)
        self.form_layout.addRow("Notes:", self.notes)
        self.form_layout.addRow("Execution Space:", self.execution_space)

        self.layout.addLayout(self.form_layout)

        self.task_scheduler = TaskScheduler()
        self.layout.addWidget(self.task_scheduler)

        self.task_parameters = TaskParameters()
        self.layout.addWidget(self.task_parameters)

        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_configuration)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_configuration(self):
        # Save the configuration details
        task_name = self.task_name.text()
        run_directory = self.run_directory.text()
        log_folder = self.log_folder.text()
        notes = self.notes.toPlainText()
        execution_space = self.execution_space.currentText()

        # Handle saving the configuration to the database or other storage
        print(f"Task Name: {task_name}")
        print(f"Run Directory: {run_directory}")
        print(f"Log Folder: {log_folder}")
        print(f"Notes: {notes}")
        print(f"Execution Space: {execution_space}")
