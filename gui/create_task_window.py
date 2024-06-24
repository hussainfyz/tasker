# tabs/create_task_window.py
import sys
import os
import inspect
import os,importlib
import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
print(tasker_dir)
sys.path.insert(0, tasker_dir)

# tabs/create_task_window.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QMenu, QSplitter, QHBoxLayout, QWidget,
    QPlainTextEdit, QComboBox,QMessageBox
)
from PyQt5.QtCore import Qt, QPoint, QSize
from db.database_operations import create_task_subtask_association
from db.db_tasks import TaskDB
from db.db_subtasks import SubtaskDB
from db.db_steps import StepDB
from db.db_step_params import StepParamDB


import json
import os


class CreateTaskWindow(QDialog):
    def __init__(self, parent=None):
        super(CreateTaskWindow, self).__init__(parent)
        self.setWindowTitle("Create Task")
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowOpacity(0.9)
        self.setStyleSheet(self.load_stylesheet())
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.task_db = TaskDB()
        self.subtask_db = SubtaskDB()
        self.steps_db = StepDB()
        self.step_params_db = StepParamDB()

        self.layout = QVBoxLayout(self)

        self.setup_task_details()
        self.setup_subtask_selection()
        self.setup_buttons()
        self.selected_subtasks_l=[]
        self.selected_steps_l=[]

    def load_stylesheet(self):
        return """
        QDialog {
            background-color: rgba(0, 0, 0, 0);
            border: 1px solid #FFFFFF;
        }
        QLabel, QLineEdit, QPlainTextEdit, QPushButton, QComboBox {
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
            background-color: white;
            border: 1px solid #ccc;
            font-size: 14px;
            color: black;
        }
        """

    def setup_task_details(self):
        self.details_layout = QFormLayout()
        self.task_name = QLineEdit()
        self.task_name.setStyleSheet("color: blue;")
        self.task_description = QLineEdit()
        self.task_description.setStyleSheet("color: black;")
        self.created_by = QLabel("current_user")  # Replace with the actual user
        self.created_by.setStyleSheet("color: black;")
        self.creation_datetime = QLabel("2024-06-15 12:00:00")
        # Replace with the actual datetime
        self.creation_datetime.setStyleSheet("color:black")
        self.notes = QPlainTextEdit()
        self.notes.setStyleSheet("color: blue;")
        self.custom_type = QLineEdit()
        self.custom_type.setStyleSheet("color: black;")
        self.execution_space = QComboBox()
        self.execution_space.addItems(["Space 1", "Space 2", "Space 3"])

        self.details_layout.addRow("Name:", self.task_name)
        self.details_layout.addRow("Description:", self.task_description)
        self.details_layout.addRow("Created By:", self.created_by)
        self.details_layout.addRow("Creation Date:", self.creation_datetime)
        self.details_layout.addRow("Notes:", self.notes)
        self.details_layout.addRow("Custom Type:", self.custom_type)
        self.details_layout.addRow("Execution Space:", self.execution_space)
        self.layout.addLayout(self.details_layout)

    def setup_subtask_selection(self):
        self.splitter = QSplitter(Qt.Horizontal)

        # Subtask list
        self.available_subtasks_list = QListWidget()
        self.available_subtasks_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.available_subtasks_list.customContextMenuRequested.connect(self.show_context_menu)
        self.available_subtasks_list.itemClicked.connect(self.display_subtask_details)

        self.subtasks = self.subtask_db.get_all_subtasks()
        for idx, subtask in enumerate(self.subtasks, start=1):
            item = QListWidgetItem(f"{idx}. {subtask['name']}")
            item.setData(Qt.UserRole, subtask)
            self.available_subtasks_list.addItem(item)

        self.available_subtasks_label = QLabel("All Available Subtasks")
        self.available_subtasks_info = QLabel()
        self.available_subtasks_layout = QVBoxLayout()
        self.available_subtasks_layout.addWidget(self.available_subtasks_label)
        self.available_subtasks_layout.addWidget(self.available_subtasks_list)
        self.available_subtasks_layout.addWidget(self.available_subtasks_info)

        available_subtasks_widget = QWidget()
        available_subtasks_widget.setLayout(self.available_subtasks_layout)
        self.splitter.addWidget(available_subtasks_widget)

        # Selected subtasks list
        self.selected_subtasks_list = QListWidget()
        self.selected_subtasks_list.itemClicked.connect(self.update_selected_steps)

        self.selected_subtasks_label = QLabel("Selected Subtasks")
        self.selected_subtasks_info = QLabel()
        self.selected_subtasks_layout = QVBoxLayout()
        self.selected_subtasks_layout.addWidget(self.selected_subtasks_label)
        self.selected_subtasks_layout.addWidget(self.selected_subtasks_list)
        self.selected_subtasks_layout.addWidget(self.selected_subtasks_info)

        selected_subtasks_widget = QWidget()
        selected_subtasks_widget.setLayout(self.selected_subtasks_layout)
        self.splitter.addWidget(selected_subtasks_widget)

        # Step details and parameters
        self.steps_list = QListWidget()
        self.steps_list.itemClicked.connect(self.display_step_details)

        self.steps_label = QLabel("Selected Steps")
        self.steps_info = QLabel()
        self.steps_layout = QVBoxLayout()
        self.steps_layout.addWidget(self.steps_label)
        self.steps_layout.addWidget(self.steps_list)
        self.steps_layout.addWidget(self.steps_info)

        steps_widget = QWidget()
        steps_widget.setLayout(self.steps_layout)
        self.splitter.addWidget(steps_widget)

        self.step_params_list = QListWidget()

        self.params_label = QLabel("Required Parameters")
        self.params_info = QLabel()
        self.params_layout = QVBoxLayout()
        self.params_layout.addWidget(self.params_label)
        self.params_layout.addWidget(self.step_params_list)
        self.params_layout.addWidget(self.params_info)

        params_widget = QWidget()
        params_widget.setLayout(self.params_layout)
        self.splitter.addWidget(params_widget)

        self.layout.addWidget(self.splitter)

    def setup_buttons(self):
        self.buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Subtask")
        self.add_button.clicked.connect(self.add_subtask)
        self.buttons_layout.addWidget(self.add_button)

        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.move_subtask_up)
        self.buttons_layout.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.move_subtask_down)
        self.buttons_layout.addWidget(self.move_down_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_task)
        self.buttons_layout.addWidget(self.save_button)

        self.layout.addLayout(self.buttons_layout)

    def show_context_menu(self, pos: QPoint):
        global_pos = self.available_subtasks_list.mapToGlobal(pos)
        context_menu = QMenu()
        details_action = context_menu.addAction("Details")
        edit_action = context_menu.addAction("Edit")
        remove_action = context_menu.addAction("Remove")

        action = context_menu.exec_(global_pos)
        if action == details_action:
            self.show_subtask_details()
        elif action == edit_action:
            self.edit_subtask()
        elif action == remove_action:
            self.remove_subtask_from_list()

    def display_subtask_details(self, item):
        subtask = item.data(Qt.UserRole)
        self.available_subtasks_info.setText(
            f"Created By: {subtask['created_by']}\n"
            f"Creation Date: {subtask['creation_datetime']}\n"
            f"Description: {subtask['description']}\n"
            f"Notes: {subtask['notes']}"
        )

    def update_selected_steps(self, item):
        self.steps_list.clear()
        self.step_params_list.clear()

        for index in range(self.selected_subtasks_list.count()):
            subtask_item = self.selected_subtasks_list.item(index)
            subtask = subtask_item.data(Qt.UserRole)
            steps = self.get_steps_by_subtask_id(subtask["id"])
            for idx, step in enumerate(steps, start=1):
                step_item = QListWidgetItem(f"{idx}. {step['function_name']}")
                step_item.setData(Qt.UserRole, step)
                self.steps_list.addItem(step_item)
                self.selected_steps_l.append(step_item.text())

    def display_step_details(self, item):
        step = item.data(Qt.UserRole)
        self.steps_info.setText(
            f"Created By: {step['created_by']}\n"
            f"Creation Date: {step['creation_datetime']}\n"
            f"Description: {step['description']}\n"
            f"Notes: {step['notes']}"
        )

        self.step_params_list.clear()
        step_params = self.get_params_by_step_id(step["id"])
        for idx, param in enumerate(step_params, start=1):
            self.step_params_list.addItem(f"{idx}. {param['param_name']}: {param['param_value']}")

    def show_subtask_details(self):
        selected_item = self.available_subtasks_list.currentItem()
        if selected_item:
            subtask = selected_item.data(Qt.UserRole)
            self.subtask_details_window = SubtaskDetailsWindow(subtask)
            self.subtask_details_window.show()

    def add_subtask(self):
        selected_item = self.available_subtasks_list.currentItem()
        if selected_item:
            subtask = selected_item.data(Qt.UserRole)
            new_item = QListWidgetItem(selected_item.text())
            new_item.setData(Qt.UserRole, subtask)
            self.selected_subtasks_list.addItem(new_item)
            self.update_selected_steps(new_item)

    def move_subtask_up(self):
        current_row = self.selected_subtasks_list.currentRow()
        if current_row > 0:
            current_item = self.selected_subtasks_list.takeItem(current_row)
            self.selected_subtasks_list.insertItem(current_row - 1, current_item)
            self.selected_subtasks_list.setCurrentRow(current_row - 1)
            self.update_selected_steps(current_item)

    def move_subtask_down(self):
        current_row = self.selected_subtasks_list.currentRow()
        if current_row < self.selected_subtasks_list.count() - 1:
            current_item = self.selected_subtasks_list.takeItem(current_row)
            self.selected_subtasks_list.insertItem(current_row + 1, current_item)
            self.selected_subtasks_list.setCurrentRow(current_row + 1)
            self.update_selected_steps(current_item)


    def save_task1(self):
        task_name = self.task_name.text()
        task_description = self.task_description.text()
        created_by = self.created_by.text()
        creation_datetime = self.creation_datetime.text()
        notes = self.notes.toPlainText()
        custom_type = self.custom_type.text()
        execution_space = self.execution_space.currentText()

        if not task_name:
            # Handle empty task name error
            return

        task_id = self.task_db.create_task({
            "name": task_name,
            "description": task_description,
            "created_by": created_by,
            "creation_datetime": creation_datetime,
            "notes": notes,
            "custom_type": custom_type,
            "execution_space": execution_space
        })

        for index in range(self.selected_subtasks_list.count()):
            subtask_item = self.selected_subtasks_list.item(index)
            self.selected_subtasks_l.append(subtask_item.text())
            subtask = subtask_item.data(Qt.UserRole)
            create_task_subtask_association(task_id, subtask["id"])

        self.close()


    def get_steps_by_subtask_id(self, subtask_id):
        step_ids = self.steps_db.get_step_ids_by_subtask_id(subtask_id)
        steps = [self.steps_db.get_step_by_id(step_id) for step_id in step_ids]
        return steps

    def get_params_by_step_id(self, step_id):
        return self.step_params_db.get_params_by_step_id(step_id)

    def save_task(self):
        task_name = self.task_name.text()
        task_description = self.task_description.text()
        created_by = self.created_by.text()
        creation_datetime = self.creation_datetime.text()
        notes = self.notes.toPlainText()
        custom_type = self.custom_type.text()
        execution_space = self.execution_space.currentText()

        if not task_name:
            QMessageBox.warning(self, "Input Error", "Task name cannot be empty!")
            return

        task_id = self.task_db.create_task({
            "name": task_name,
            "description": task_description,
            "created_by": created_by,
            "creation_datetime": creation_datetime,
            "notes": notes,
            "custom_type": custom_type,
            "execution_space": execution_space
        })

        selected_subtasks = []
        for index in range(self.selected_subtasks_list.count()):
            subtask_item = self.selected_subtasks_list.item(index)
            subtask = subtask_item.data(Qt.UserRole)
            selected_subtasks.append(subtask)
            create_task_subtask_association(task_id, subtask["id"])

        selected_steps = []
        for subtask in selected_subtasks:
            steps = self.get_steps_by_subtask_id(subtask["id"])
            for step in steps:
                params = self.get_params_by_step_id(step["id"])
                step_entry = {
                    "subtask_id": subtask["id"],
                    "step_id": step["id"],
                    "file_path": step["file_path"],
                    "function_name": step["function_name"],
                    "description": step["description"],
                    "params": {param["param_name"]: param["param_value"] for param in params}
                    # Ensure params is a dictionary
                }
                selected_steps.append(step_entry)

        json_path = self.generate_task_json(task_name, task_description, selected_subtasks, selected_steps)
        script_path = self.generate_task_script(task_name, json_path)

        QMessageBox.information(self, "Task Saved",
                                f"Task saved successfully!\nJSON: {json_path}\nScript: {script_path}")

        self.close()

    def generate_task_json(self, task_name, task_description, selected_subtasks, selected_steps):
        task_structure = {
            "task": {
                "name": task_name,
                "description": task_description,
                "subtasks": []
            }
        }

        for subtask in selected_subtasks:
            subtask_entry = {
                "name": subtask["name"],
                "created_by": subtask["created_by"],
                "creation_datetime": subtask["creation_datetime"],
                "description": subtask["description"],
                "steps": []
            }
            for step in selected_steps:
                if step["subtask_id"] == subtask["id"]:
                    step_entry = {
                        "file_path": step["file_path"],
                        "function_name": step["function_name"],
                        "description": step["description"],
                        "params": step["params"]  # Ensure params is already a dictionary
                    }
                    subtask_entry["steps"].append(step_entry)
            task_structure["task"]["subtasks"].append(subtask_entry)

        directory = f"./{task_name}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        json_path = os.path.join(directory, "task_structure.json")
        with open(json_path, 'w') as json_file:
            json.dump(task_structure, json_file, indent=4)

        return json_path

    def row_to_dict(self, row):
        return {key: row[key] for key in row.keys()}

    def generate_task_script(self,task_name, json_path):
        script_content = f"""
import json
import importlib.util
import sys
import os

def load_task_json(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

def run_task(task):
    for subtask in task["subtasks"]:
        for step in subtask["steps"]:
            file_path = step["file_path"]
            function_name = step["function_name"]
            params = step["params"]
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            print(getattr(module, function_name)(**params))

if __name__ == "__main__":
    task = load_task_json("{json_path}")
    run_task(task["task"])
        """

        directory = f"./{task_name}"
        script_path = os.path.join(directory, f"{task_name}.py")
        with open(script_path, 'w') as script_file:
            script_file.write(script_content)

        return script_path


class SubtaskDetailsWindow(QDialog):
    def __init__(self, subtask, parent=None):
        super(SubtaskDetailsWindow, self).__init__(parent)
        self.setWindowTitle("Subtask Details")
        self.setGeometry(300, 300, 400, 400)
        self.setStyleSheet("""
        QDialog {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                stop:0 black, stop:0.33 darkblue, stop:0.66 lightblue, stop:1 skyblue);
        }
        QLabel {
            font-size: 14px;
            color: white;
        }
        """)

        self.subtask = subtask
        self.steps_db = StepDB()
        self.step_params_db = StepParamDB()

        self.layout = QVBoxLayout(self)

        self.subtask_name_label = QLabel(f"Subtask Name: {self.subtask['name']}")
        self.subtask_description_label = QLabel(f"Subtask Description: {self.subtask['description']}")
        self.steps_list = QListWidget()
        self.steps_list.itemClicked.connect(self.display_step_details)

        self.layout.addWidget(self.subtask_name_label)
        self.layout.addWidget(self.subtask_description_label)
        self.layout.addWidget(QLabel("Associated Steps:"))
        self.layout.addWidget(self.steps_list)

        self.step_details_widget = QWidget()
        self.step_details_layout = QVBoxLayout(self.step_details_widget)
        self.step_function_name_label = QLabel("Function Name:")
        self.step_description_label = QLabel("Step Description:")
        self.step_params_list = QListWidget()

        self.step_details_layout.addWidget(self.step_function_name_label)
        self.step_details_layout.addWidget(self.step_description_label)
        self.step_details_layout.addWidget(QLabel("Parameters:"))
        self.step_details_layout.addWidget(self.step_params_list)

        self.layout.addWidget(self.step_details_widget)

        self.populate_steps()

    def populate_steps(self):
        self.steps_list.clear()
        steps = self.get_steps_by_subtask_id(self.subtask["id"])
        for idx, step in enumerate(steps, start=1):
            step_item = QListWidgetItem(f"{idx}. {step['function_name']}")
            step_item.setData(Qt.UserRole, step)
            self.steps_list.addItem(step_item)

    def display_step_details(self, item):
        step = item.data(Qt.UserRole)
        self.step_function_name_label.setText(f"Function Name: {step['function_name']}")
        self.step_description_label.setText(f"Step Description: {step['description']}")

        self.step_params_list.clear()
        step_params = self.get_params_by_step_id(step["id"])
        for idx, param in enumerate(step_params, start=1):
            self.step_params_list.addItem(f"{idx}. {param['param_name']}: {param['param_value']}")

    def get_steps_by_subtask_id(self, subtask_id):
        step_ids = self.steps_db.get_step_ids_by_subtask_id(subtask_id)
        steps = [self.steps_db.get_step_by_id(step_id) for step_id in step_ids]
        return steps

    def get_params_by_step_id(self, step_id):
        return self.step_params_db.get_params_by_step_id(step_id)


class LinkConfigDialog(QDialog):
    def __init__(self, steps, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Link Configuration")
        self.layout = QVBoxLayout(self)

        self.steps = steps
        self.links = []

        self.step_list = QListWidget(self)
        self.step_list.addItems([step["function_name"] for step in steps])
        self.step_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.layout.addWidget(self.step_list)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def get_links(self):
        selected_items = self.step_list.selectedItems()
        for item in selected_items:
            step = self.steps[self.step_list.row(item)]
            self.links.append(step)
        return self.links

class StepConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Step Configuration")
        self.layout = QVBoxLayout(self)

        self.function_name = QLineEdit(self)
        self.function_name.setPlaceholderText("Function Name")
        self.layout.addWidget(self.function_name)

        self.file_path = QLineEdit(self)
        self.file_path.setPlaceholderText("File Path")
        self.layout.addWidget(self.file_path)

        self.params = QTextEdit(self)
        self.params.setPlaceholderText("Parameters (JSON format)")
        self.layout.addWidget(self.params)

        self.outputs = QTextEdit(self)
        self.outputs.setPlaceholderText("Outputs (JSON format)")
        self.layout.addWidget(self.outputs)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def get_step_details(self):
        return {
            "function_name": self.function_name.text(),
            "file_path": self.file_path.text(),
            "params": json.loads(self.params.toPlainText() or "{}"),
            "outputs": json.loads(self.outputs.toPlainText() or "{}")
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CreateTaskWindow()
    window.show()
    sys.exit(app.exec_())
