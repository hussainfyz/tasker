# task_details_dialog.py

import sys
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QDateTimeEdit, QLineEdit, QApplication,
    QGroupBox, QWidget, QFormLayout, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt,QDateTime
import datetime

class TaskDetailsDialog(QDialog):
    def __init__(self, task_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Task Details")

        self.task_id = task_id

        main_layout = QVBoxLayout()

        # Task Name and Description
        task_name_label = QLabel(f"<h1>Task {task_id}</h1>")
        description_label = QLabel(
            "Task Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget metus sit amet augue tincidunt condimentum.")

        main_layout.addWidget(task_name_label)
        main_layout.addWidget(description_label)

        # Subtasks and Steps Section
        subtasks_steps_layout = QHBoxLayout()

        # Subtasks Section
        subtasks_groupbox = QGroupBox("Subtasks")
        subtasks_layout = QVBoxLayout()

        subtasks = self.fetch_subtasks(task_id)
        for subtask_id, subtask_name in subtasks:
            subtask_label = QLabel(f"{subtask_name} (ID: {subtask_id})")
            subtasks_layout.addWidget(subtask_label)

        subtasks_groupbox.setLayout(subtasks_layout)
        subtasks_steps_layout.addWidget(subtasks_groupbox)

        # Steps Section
        steps_groupbox = QGroupBox("Steps")
        steps_layout = QVBoxLayout()

        steps = self.fetch_steps(subtasks[0][0]) if subtasks else []
        for step_id, step_name, param_name in steps:
            step_label = QLabel(f"Step {step_id}: {step_name} - Param Name: {param_name}")
            steps_layout.addWidget(step_label)

            # Example: Add input fields for step parameters
            param_input = QLineEdit()
            steps_layout.addWidget(param_input)

        steps_groupbox.setLayout(steps_layout)
        subtasks_steps_layout.addWidget(steps_groupbox)

        main_layout.addLayout(subtasks_steps_layout)

        # Schedule and Options Section
        schedule_options_layout = QHBoxLayout()

        # Schedule Later Option
        schedule_groupbox = QGroupBox("Schedule")
        schedule_layout = QVBoxLayout()

        self.schedule_radio = QRadioButton("Schedule Later")
        schedule_layout.addWidget(self.schedule_radio)

        self.date_time_edit = QDateTimeEdit()
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        schedule_layout.addWidget(self.date_time_edit)

        schedule_groupbox.setLayout(schedule_layout)
        schedule_options_layout.addWidget(schedule_groupbox)

        # Run Options
        run_options_groupbox = QGroupBox("Run Options")
        run_options_layout = QVBoxLayout()

        self.run_options = QComboBox()
        self.run_options.addItems(["Space", "Private", "Public"])
        run_options_layout.addWidget(self.run_options)

        run_options_groupbox.setLayout(run_options_layout)
        schedule_options_layout.addWidget(run_options_groupbox)

        main_layout.addLayout(schedule_options_layout)

        # Additional Information Section
        additional_info_groupbox = QGroupBox("Additional Information")
        additional_info_layout = QVBoxLayout()

        info_text = QTextEdit()
        info_text.setPlainText("Additional information about the task goes here.")
        additional_info_layout.addWidget(info_text)

        additional_info_groupbox.setLayout(additional_info_layout)
        main_layout.addWidget(additional_info_groupbox)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_task_details)
        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

    def fetch_subtasks(self, task_id):
        # Replace with actual database query to fetch subtasks for task_id
        return [
            (1, "Subtask 1"),
            (2, "Subtask 2"),
            (3, "Subtask 3")
        ]

    def fetch_steps(self, subtask_id):
        # Replace with actual database query to fetch steps for subtask_id
        return [
            (1, "Step 1", "Param 1"),
            (2, "Step 2", "Param 2"),
            (3, "Step 3", "Param 3")
        ]

    def submit_task_details(self):
        # Example: Gather task details and parameters
        task_details = {
            "task_id": self.task_id,
            "scheduled": self.schedule_radio.isChecked(),
            "scheduled_time": self.date_time_edit.dateTime().toString(Qt.ISODate),
            "run_option": self.run_options.currentText(),
            # Add other parameters as needed
        }

        print(task_details)  # Print JSON representation of task details
        self.accept()  # Close the dialog


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python task_details_dialog.py <task_id>")
        sys.exit(1)

    task_id = int(sys.argv[1])
    app = QApplication(sys.argv)
    dialog = TaskDetailsDialog(task_id)
    dialog.exec_()
    sys.exit(app.exec_())
