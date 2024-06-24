# tabs/create_task_window.py
import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
print(tasker_dir)
sys.path.insert(0, tasker_dir)
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QTabWidget, QWidget, QListWidget
#from ...db.db_tasks import insert_task, get_subtasks, create_task_subtask_association, insert_step, insert_step_param, insert_subtask, create_subtask_step_association
#from tasker.db.db_tasks import TaskDB #insert_task, get_subtasks, create_task_subtask_association, insert_step, insert_step_param, insert_subtask, create_subtask_step_association
#sys.path.append('../')
#from tasker.db.db_tasks import TaskDB
from db.database_operations import create_subtask_step_association,create_task_subtask_association
from db.db_tasks import TaskDB
from db.db_subtasks import SubtaskDB
from db.db_steps import StepDB
class CreateTaskWindow(QDialog):
    def __init__(self, parent=None):
        super(CreateTaskWindow, self).__init__(parent)
        self.setWindowTitle("Create Task")
        self.setGeometry(300, 300, 400, 400)
        self.class_task_db=TaskDB()
        self.layout = QVBoxLayout(self)
        self.dbt_task=TaskDB()
        self.dbt_subtask=SubtaskDB()
        self.dbt_steps=StepDB()
        self.tabs = QTabWidget()
        self.details_tab = QWidget()
        self.subtasks_tab = QWidget()
        self.steps_tab = QWidget()

        self.tabs.addTab(self.details_tab, "Details")
        self.tabs.addTab(self.subtasks_tab, "Subtasks")
        self.tabs.addTab(self.steps_tab, "Steps")

        self.layout.addWidget(self.tabs)

        # Task details form
        self.details_layout = QFormLayout()
        self.task_name = QLineEdit()
        self.task_description = QLineEdit()
        self.details_layout.addRow("Name:", self.task_name)
        self.details_layout.addRow("Description:", self.task_description)
        self.details_tab.setLayout(self.details_layout)

        # Subtasks selection
        self.subtasks_layout = QVBoxLayout()
        self.subtask_list_widget = QListWidget()
        subtasks = self.dbt_subtask.get_all_subtasks()
        for subtask in subtasks:
            self.subtask_list_widget.addItem(subtask["name"])
        self.subtasks_layout.addWidget(self.subtask_list_widget)
        self.subtasks_tab.setLayout(self.subtasks_layout)

        # Steps and parameters
        self.steps_layout = QFormLayout()
        self.step_file_path = QLineEdit()
        self.step_function_name = QLineEdit()
        self.step_description = QLineEdit()
        self.step_param_name = QLineEdit()
        self.step_param_value = QLineEdit()
        self.steps_layout.addRow("File Path:", self.step_file_path)
        self.steps_layout.addRow("Function Name:", self.step_function_name)
        self.steps_layout.addRow("Description:", self.step_description)
        self.steps_layout.addRow("Param Name:", self.step_param_name)
        self.steps_layout.addRow("Param Value:", self.step_param_value)
        self.steps_tab.setLayout(self.steps_layout)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_task)
        self.layout.addWidget(self.save_button)

    def save_task(self):
        # Insert task
        task_name = self.task_name.text()
        task_description = self.task_description.text()
        task_id = self.dbt_task.insert_task(task_name, "current_user", task_description, "", "", "")

        # Associate subtasks with task
        for index in range(self.subtask_list_widget.count()):
            item = self.subtask_list_widget.item(index)
            if item.isSelected():
                subtask_name = item.text()
                subtasks = self.dbt_subtask.get_subtask_by_name(subtask_name)
                for subtask in subtasks:
                    if subtask["name"] == subtask_name:
                        create_task_subtask_association(task_id, subtask["id"])

        # Insert step
        file_path = self.step_file_path.text()
        function_name = self.step_function_name.text()
        step_description = self.step_description.text()
        print("Passing to insert_step")
        print(step_description)
        print(function_name,file_path)
        step_id = self.dbt_steps.insert_step(file_path, function_name, "current_user", "Medium",step_description,)

        # Insert step parameters
        param_name = self.step_param_name.text()
        param_value = self.step_param_value.text()
        insert_step_param(step_id, param_name, param_value)

        # Associate step with subtask
        for index in range(self.subtask_list_widget.count()):
            item = self.subtask_list_widget.item(index)
            if item.isSelected():
                subtask_name = item.text()
                subtasks = get_subtasks()
                for subtask in subtasks:
                    if subtask["name"] == subtask_name:
                        create_subtask_step_association(subtask["id"], step_id)

        self.close()
