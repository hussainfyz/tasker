import json

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTabWidget,QWidget,QListWidget,QHBoxLayout
from datetime import datetime
from db.database_operations import create_subtask_step_association

from db.db_tasks import TaskDB
from db.db_subtasks import SubtaskDB
from db.db_steps import StepDB
class CreateSubtaskWindow(QDialog):
    def __init__(self, parent=None):
        super(CreateSubtaskWindow, self).__init__(parent)
        self.setWindowTitle("Create Subtask")

        self.tab_widget = QTabWidget()

        self.general_tab = QWidget()
        self.steps_tab = QWidget()
        self.dbt_task = TaskDB()
        self.dbt_subtask_db = SubtaskDB()
        self.dbt_steps = StepDB()
        self.tab_widget.addTab(self.general_tab, "General")
        self.tab_widget.addTab(self.steps_tab, "Steps")

        self.general_layout = QFormLayout()
        self.subtask_name_input = QLineEdit()
        self.subtask_description_input = QLineEdit()
        self.created_by_input = QLineEdit("John Doe")
        self.created_by_input.setReadOnly(True)
        self.creation_datetime_input = QLineEdit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.creation_datetime_input.setReadOnly(True)
        self.general_layout.addRow(QLabel("Subtask Name:"), self.subtask_name_input)
        self.general_layout.addRow(QLabel("Subtask Description:"), self.subtask_description_input)
        self.general_layout.addRow(QLabel("Created By:"), self.created_by_input)
        self.general_layout.addRow(QLabel("Creation DateTime:"), self.creation_datetime_input)
        self.general_tab.setLayout(self.general_layout)

        self.steps_layout = QVBoxLayout()
        self.step_dropdown = QComboBox()
        self.selected_steps_list = QListWidget()
        self.add_step_button = QPushButton("Add Step")
        self.add_step_button.clicked.connect(self.add_step)
        #steps = get_steps_for_subtask(self.subtask_name_input.text())

        steps=self.dbt_steps.get_all_steps()

        print(steps)
        print(type(steps))
        #exit()
        #steps=json.loads(steps)
        for step in steps:
            print('step',step)
            self.step_dropdown.addItem(step["step_name"])
        self.steps_layout.addWidget(QLabel("Select Steps"))
        self.steps_layout.addWidget(self.step_dropdown)
        self.steps_layout.addWidget(self.add_step_button)
        self.steps_layout.addWidget(QLabel("Selected Steps"))
        self.steps_layout.addWidget(self.selected_steps_list)
        self.steps_tab.setLayout(self.steps_layout)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_subtask)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_step(self):
        selected_step = self.step_dropdown.currentText()
        self.selected_steps_list.addItem(selected_step)

    def save_subtask(self):
        subtask_name = self.subtask_name_input.text()
        subtask_description = self.subtask_description_input.text()
        created_by = self.created_by_input.text()
        creation_datetime = self.creation_datetime_input.text()

        if subtask_name:
            subtask_id = self.dbt_subtask_db.insert_subtask(subtask_name, created_by, subtask_description, "")
            for i in range(self.selected_steps_list.count()):
                step_name = self.selected_steps_list.item(i).text()
                print('selected step name:',step_name)
                step_data = self.dbt_steps.get_step_by_step_name(step_name)
                print("Selected step data")
                print(step_data)
                step_id=step_data[0]['id']
                print(step_id,type(step_id))
                create_subtask_step_association(subtask_id, step_id)
            self.close()
        else:
            print("Subtask name is required")
