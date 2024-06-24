import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QLabel,
    QGroupBox, QSplitter, QApplication
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon

from create_task_window import CreateTaskWindow
from create_subtask_window import CreateSubtaskWindow
from create_step_window import CreateStepWindow
from db.database_operations import (
    get_all_tasks, get_subtasks_by_task_name, get_steps_by_subtask_name,
    get_step_params_by_step_id, get_step_id_by_name
)


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

        self.layout = QVBoxLayout(self)

        # Create a QSplitter for resizable layouts
        splitter = QSplitter(Qt.Horizontal)

        # Task List and Buttons
        task_group = QGroupBox("Tasks")
        task_layout = QVBoxLayout()
        self.task_list_widget = QListWidget()
        self.load_tasks()
        self.task_create_button = QPushButton("Create Task")
        self.task_create_button.setIcon(QIcon('icons/add.png'))  # Add icon
        self.task_create_button.clicked.connect(self.create_task)
        self.task_edit_button = QPushButton("Edit Task")
        self.task_edit_button.setIcon(QIcon('icons/edit.png'))  # Add icon
        self.task_remove_button = QPushButton("Remove Task")
        self.task_remove_button.setIcon(QIcon('icons/remove.png'))  # Add icon
        self.task_config_button = QPushButton("Config")
        self.task_config_button.setIcon(QIcon('icons/config.png'))  # Add icon
        self.task_config_button.clicked.connect(self.config_task)

        self.task_list_widget.itemSelectionChanged.connect(self.update_task_buttons)
        task_layout.addWidget(self.task_list_widget)
        task_layout.addWidget(self.task_create_button)
        task_layout.addWidget(self.task_edit_button)
        task_layout.addWidget(self.task_remove_button)
        task_layout.addWidget(self.task_config_button)
        task_group.setLayout(task_layout)

        # Subtask List and Buttons
        subtask_group = QGroupBox("Subtasks")
        subtask_layout = QVBoxLayout()
        self.subtask_list_widget = QListWidget()
        self.subtask_list_widget.itemSelectionChanged.connect(self.update_subtask_buttons)
        self.subtask_create_button = QPushButton("Create Subtask")
        self.subtask_create_button.setIcon(QIcon('icons/add.png'))  # Add icon
        self.subtask_create_button.clicked.connect(self.create_subtask)
        self.subtask_edit_button = QPushButton("Edit Subtask")
        self.subtask_edit_button.setIcon(QIcon('icons/edit.png'))  # Add icon
        self.subtask_remove_button = QPushButton("Remove Subtask")
        self.subtask_remove_button.setIcon(QIcon('icons/remove.png'))  # Add icon
        self.subtask_config_button = QPushButton("Config")
        self.subtask_config_button.setIcon(QIcon('icons/config.png'))  # Add icon
        self.subtask_config_button.clicked.connect(self.config_subtask)

        subtask_layout.addWidget(self.subtask_list_widget)
        subtask_layout.addWidget(self.subtask_create_button)
        subtask_layout.addWidget(self.subtask_edit_button)
        subtask_layout.addWidget(self.subtask_remove_button)
        subtask_layout.addWidget(self.subtask_config_button)
        subtask_group.setLayout(subtask_layout)

        # Step List and Buttons
        step_group = QGroupBox("Steps")
        step_layout = QVBoxLayout()
        self.step_list_widget = QListWidget()
        self.step_list_widget.itemSelectionChanged.connect(self.update_step_buttons)
        self.step_create_button = QPushButton("Create Step")
        self.step_create_button.setIcon(QIcon('icons/add.png'))  # Add icon
        self.step_create_button.clicked.connect(self.create_step)
        self.step_edit_button = QPushButton("Edit Step")
        self.step_edit_button.setIcon(QIcon('icons/edit.png'))  # Add icon
        self.step_remove_button = QPushButton("Remove Step")
        self.step_remove_button.setIcon(QIcon('icons/remove.png'))  # Add icon
        self.step_config_button = QPushButton("Config")
        self.step_config_button.setIcon(QIcon('icons/config.png'))  # Add icon
        self.step_config_button.clicked.connect(self.config_step)

        step_layout.addWidget(self.step_list_widget)
        step_layout.addWidget(self.step_create_button)
        step_layout.addWidget(self.step_edit_button)
        step_layout.addWidget(self.step_remove_button)
        step_layout.addWidget(self.step_config_button)
        step_group.setLayout(step_layout)

        # Add groups to the splitter
        splitter.addWidget(task_group)
        splitter.addWidget(subtask_group)
        splitter.addWidget(step_group)

        # Add splitter to the main layout
        self.layout.addWidget(splitter)
        self.setLayout(self.layout)

        # Apply styles
        self.set_style()

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
        self.step_list_widget.clear()
        selected_subtask_item = self.subtask_list_widget.currentItem()
        if selected_subtask_item:
            subtask_name = selected_subtask_item.text()
            steps = get_steps_by_subtask_name(subtask_name)
            for step in steps:
                self.step_list_widget.addItem(step["function_name"])

    def load_tasks(self):
        self.task_list_widget.clear()
        tasks = get_all_tasks()
        for task in tasks:
            self.task_list_widget.addItem(task["name"])

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
            subtasks = get_subtasks_by_task_name(task_name)
            steps = []
            for subtask in subtasks:
                steps += get_steps_by_subtask_id(subtask["id"])
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
        self.step_params_window = StepParamsWindow(step_params)
        self.step_params_window.show()

    def set_style(self):
        self.setStyleSheet("""
                    QWidget {
                        font-size: 14px;
                    }
                    QGroupBox {
                        font-weight: bold;
                        border: 1px solid gray;
                        border-radius: 5px;
                        margin-top: 10px;
                    }
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        padding: 10px;
                        border: none;
                        border-radius: 5px;
                        text-align: center;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QListWidget {
                        border: 1px solid gray;
                        border-radius: 5px;
                    }
                """)

    def create_task(self):
        self.create_task_window = CreateTaskWindow(self)
        self.create_task_window.show()

    def create_subtask(self):
        self.create_subtask_window = CreateSubtaskWindow(self)
        self.create_subtask_window.show()

    def create_step(self):
        self.create_step_window = CreateStepWindow(self)
        self.create_step_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManageTab()
    window.show()
    sys.exit(app.exec_())

