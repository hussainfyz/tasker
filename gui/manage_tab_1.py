# tabs/manage_tab.py
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSlot

from create_task_window import CreateTaskWindow
from create_subtask_window import CreateSubtaskWindow
from create_step_window import CreateStepWindow
from db.database_operations import get_tasks, get_subtasks_by_task_id, get_steps_by_subtask_id,get_step_params_by_step_id,get_step_id_by_name,get_steps_by_subtask_name,get_subtasks_by_task_name
from db.db_tasks import TaskDB
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class StepParamsWindow(QWidget):
    def __init__(self, step_params):
        super().__init__()

        self.setWindowTitle("Step Parameters")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        for param_name, param_value in step_params:
            param_label = QLabel(f"{param_name}: {param_value}")
            layout.addWidget(param_label)

        self.setLayout(layout)
class ManageTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        # Task List and Buttons
        self.task_list_layout = QVBoxLayout()
        self.task_list_label = QLabel("Tasks")
        self.task_list_widget = QListWidget()
        self.load_tasks()
        self.task_create_button = QPushButton("Create Task")
        self.task_create_button.clicked.connect(self.create_task)
        self.task_edit_button = QPushButton("Edit Task")
        #self.task_edit_button.setEnabled(False)
        self.task_remove_button = QPushButton("Remove Task")
        self.task_config_button = QPushButton("Config")
        self.task_config_button.clicked.connect(self.config_task)

        self.task_remove_button.setEnabled(False)
        self.task_list_widget.itemSelectionChanged.connect(self.update_task_buttons)
        self.task_list_layout.addWidget(self.task_list_label)
        self.task_list_layout.addWidget(self.task_list_widget)
        self.task_list_layout.addWidget(self.task_create_button)
        self.task_list_layout.addWidget(self.task_edit_button)
        self.task_list_layout.addWidget(self.task_remove_button)
        self.task_list_layout.addWidget(self.task_config_button)

        # Subtask List and Buttons
        self.subtask_list_layout = QVBoxLayout()
        self.subtask_list_label = QLabel("Subtasks")
        self.subtask_list_widget = QListWidget()
        self.subtask_list_widget.itemSelectionChanged.connect(self.update_subtask_buttons)
        self.subtask_create_button = QPushButton("Create Subtask")
        #self.subtask_create_button.setEnabled(False)
        self.subtask_create_button.clicked.connect(self.create_subtask)
        self.subtask_edit_button = QPushButton("Edit Subtask")
        #self.subtask_edit_button.setEnabled(False)
        self.subtask_remove_button = QPushButton("Remove Subtask")
        self.subtask_config_button = QPushButton("Config")
        self.subtask_config_button.clicked.connect(self.config_subtask)
        #self.subtask_remove_button.setEnabled(False)
        self.subtask_list_layout.addWidget(self.subtask_list_label)
        self.subtask_list_layout.addWidget(self.subtask_list_widget)
        self.subtask_list_layout.addWidget(self.subtask_create_button)
        self.subtask_list_layout.addWidget(self.subtask_edit_button)
        self.subtask_list_layout.addWidget(self.subtask_remove_button)


        # Step List and Buttons
        self.step_list_layout = QVBoxLayout()
        self.step_list_label = QLabel("Steps")
        self.step_list_widget = QListWidget()
        self.step_list_widget.itemSelectionChanged.connect(self.update_step_buttons)
        self.step_create_button = QPushButton("Create Step")
        #self.step_create_button.setEnabled(False)
        self.step_create_button.clicked.connect(self.create_step)
        self.step_edit_button = QPushButton("Edit Step")
        #self.step_edit_button.setEnabled(False)
        self.step_remove_button = QPushButton("Remove Step")
        self.step_config_button = QPushButton("Config")
        self.step_config_button.clicked.connect(self.config_step)
        #self.step_remove_button.setEnabled(False)
        self.step_list_layout.addWidget(self.step_list_label)
        self.step_list_layout.addWidget(self.step_list_widget)
        self.step_list_layout.addWidget(self.step_create_button)
        self.step_list_layout.addWidget(self.step_edit_button)
        self.step_list_layout.addWidget(self.step_remove_button)

        # Add layouts to the main layout
        self.layout.addLayout(self.task_list_layout)
        self.layout.addLayout(self.subtask_list_layout)
        self.layout.addLayout(self.step_list_layout)

        self.setLayout(self.layout)
        self.task_list_widget.currentItemChanged.connect(self.load_subtasks_and_steps)
        self.subtask_list_widget.currentItemChanged.connect(self.load_steps)

    # Inside the ManageTab class

    def load_subtasks_and_steps(self):
        self.subtask_list_widget.clear()
        self.step_list_widget.clear()

        selected_task_item = self.task_list_widget.currentItem()
        if selected_task_item:
            task_name = selected_task_item.text()
            subtasks = get_subtasks_by_task_name(task_name)
            for subtask in subtasks:
                self.subtask_list_widget.addItem(subtask["name"])
                steps = get_steps_by_subtask_id(subtask["id"])
                for step in steps:
                    self.step_list_widget.addItem(step["function_name"])


    def load_subtasks(self):
        self.subtask_list_widget.clear()
        selected_task_item = self.task_list_widget.currentItem()
        if selected_task_item:
            task_name = selected_task_item.text()
            subtasks = get_subtasks_by_task_name(task_name)
            for subtask in subtasks:
                self.subtask_list_widget.addItem(subtask["name"])
                self.subtask_list_widget.currentItemChanged.connect(self.load_steps)

    def load_steps(self):
        print("Loading s3teps")
        self.step_list_widget.clear()
        selected_subtask_item = self.subtask_list_widget.currentItem()
        print("selected item",selected_subtask_item)
        if selected_subtask_item:
            subtask_name = selected_subtask_item.text()
            steps = get_steps_by_subtask_name(subtask_name)
            for step in steps:
                print(step)
                self.step_list_widget.addItem(step["function_name"])

    def load_tasks(self):
        self.task_list_widget.clear()
        tasks = get_tasks()
        for task in tasks:
            self.task_list_widget.addItem(task["name"])

    """
    @pyqtSlot()
    def load_subtasks(self):
        self.subtask_list_widget.clear()
        selected_task_item = self.task_list_widget.currentItem()
        if selected_task_item:
            task_name = selected_task_item.text()
            subtasks = get_subtasks_by_task_id(task_name)
            for subtask in subtasks:
                self.subtask_list_widget.addItem(subtask["name"])

    @pyqtSlot()
    def load_steps(self):
        self.step_list_widget.clear()
        selected_subtask_item = self.subtask_list_widget.currentItem()
        if selected_subtask_item:
            subtask_name = selected_subtask_item.text()
            steps = get_steps_by_subtask_id(subtask_name)
            for step in steps:
                self.step_list_widget.addItem(step["function_name"])
    """
    @pyqtSlot()
    def update_task_buttons(self):
        selected_task_item = self.task_list_widget.currentItem()
        if selected_task_item:
            self.task_edit_button.setEnabled(True)
            self.task_remove_button.setEnabled(True)
            self.load_subtasks()
        else:
            self.task_edit_button.setEnabled(False)
            self.task_remove_button.setEnabled(False)
            self.subtask_list_widget.clear()

    @pyqtSlot()
    def update_subtask_buttons(self):
        selected_subtask_item = self.subtask_list_widget.currentItem()
        if selected_subtask_item:
            self.subtask_edit_button.setEnabled
    def create_task(self):
        self.create_task_window = CreateTaskWindow(self)
        self.create_task_window.show()

    def create_subtask(self):
        self.create_subtask_window = CreateSubtaskWindow(self)
        self.create_subtask_window.show()

    def create_step(self):
        self.create_step_window = CreateStepWindow(self)
        self.create_step_window.show()
    @pyqtSlot()
    def update_subtask_buttons(self):
        selected_subtask_item = self.subtask_list_widget.currentItem()
        if selected_subtask_item:
            self.subtask_edit_button.setEnabled(True)
            self.subtask_remove_button.setEnabled(True)
            self.load_steps()
        else:
            self.subtask_edit_button.setEnabled(False)
            self.subtask_remove_button.setEnabled(False)
            self.step_list_widget.clear()

    @pyqtSlot()
    def update_step_buttons(self):
        selected_step_item = self.step_list_widget.currentItem()
        if selected_step_item:
            self.step_edit_button.setEnabled(True)
            self.step_remove_button.setEnabled(True)
        else:
            self.step_edit_button.setEnabled(False)
            self.step_remove_button.setEnabled(False)

    @pyqtSlot()
    def config_task(self):
        selected_task_item = self.task_list_widget.currentItem()
        if selected_task_item:
            task_name = selected_task_item.text()
            subtasks = get_subtasks_by_task_id(task_name)
            steps = []
            for subtask in subtasks:
                steps += get_steps_by_subtask_id(subtask["name"])
            step_params = []
            for step in steps:
                step_params += get_step_params_by_step_id(step["id"])
            # Display the step parameters in a window
            self.display_step_params(step_params)

    @pyqtSlot()
    def config_subtask(self):
        selected_subtask_item = self.subtask_list_widget.currentItem()
        if selected_subtask_item:
            subtask_name = selected_subtask_item.text()
            steps = get_steps_by_subtask_id(subtask_name)
            step_params = []
            for step in steps:
                step_params += get_step_params_by_step_id(step["id"])
            # Display the step parameters in a window
            self.display_step_params(step_params)

    @pyqtSlot()
    def config_step(self):
        selected_step_item = self.step_list_widget.currentItem()
        if selected_step_item:
            step_name = selected_step_item.text()
            step_id = get_step_id_by_name(step_name)
            step_params = get_step_params_by_step_id(step_id)
            # Display the step parameters in a window
            self.display_step_params(step_params)

    def display_step_params(self, step_params):
        print("step params",step_params)
        self.step_params_window = StepParamsWindow(step_params)
        self.step_params_window.show()