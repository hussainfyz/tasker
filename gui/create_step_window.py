from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, \
    QListWidget
import inspect
import os,importlib
import sqlite3
from db.database_operations import insert_step_param
from db.db_tasks import TaskDB
from db.db_subtasks import SubtaskDB
from db.db_steps import StepDB

class CreateStepWindow(QDialog):
    def __init__(self, parent=None):
        super(CreateStepWindow, self).__init__(parent)
        self.setWindowTitle("Create Step")
        self.dbt_steps=StepDB()

        layout = QVBoxLayout()

        self.step_name_input = QLineEdit()
        self.step_description_input = QLineEdit()

        layout.addWidget(QLabel("Step Name"))
        layout.addWidget(self.step_name_input)

        layout.addWidget(QLabel("Step Description"))
        layout.addWidget(self.step_description_input)

        self.file_button = QPushButton("Select Python File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.function_dropdown = QComboBox()
        layout.addWidget(QLabel("Functions"))
        layout.addWidget(self.function_dropdown)

        self.selected_functions_list = QListWidget()
        layout.addWidget(QLabel("Selected Functions"))
        layout.addWidget(self.selected_functions_list)

        self.add_function_button = QPushButton("Add Function")
        self.add_function_button.clicked.connect(self.add_function)
        layout.addWidget(self.add_function_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_step)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Python File", "", "Python Files (*.py)",
                                                   options=options)
        if file_path:
            self.file_path = file_path
            self.load_functions(file_path)

    def load_functions(self, file_path):
        module_name = os.path.basename(file_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        functions = [func for func, obj in inspect.getmembers(module, inspect.isfunction)]
        self.function_dropdown.clear()
        self.function_dropdown.addItems(functions)

    def add_function(self):
        selected_function = self.function_dropdown.currentText()
        self.selected_functions_list.addItem(selected_function)

    def save_step(self):
        self.step_name = self.step_name_input.text()
        self.step_description = self.step_description_input.text()
        print(self.step_name,self.step_description)
        #exit()
        if self.step_name and hasattr(self, 'file_path'):
            print("Saving step ",self.file_path,self.step_name,self.step_description)

            step_id =  self.dbt_steps.insert_step(self.step_name,self.file_path, self.selected_functions_list.item(0).text(), "John Doe", self.step_description,)
            print('saved row step id',step_id)
            for i in range(self.selected_functions_list.count()):
                function_name = self.selected_functions_list.item(i).text()


                self.capture_function_params(function_name, step_id)
            self.close()
        else:
            print("Step name and file path are required")

    def capture_function_params(self, function_name, step_id):
        try:
            # Create a local namespace
            local_namespace = {}

            # Execute the Python file in the local namespace
            with open(self.file_path, 'r') as file:
                exec(file.read(), local_namespace)

            # Get the function object from the local namespace
            function = local_namespace.get(function_name)

            if function:
                # Capture function parameters
                params = inspect.signature(function).parameters
                for param_name in params:
                    param_value = params[param_name].default if params[param_name].default != inspect._empty else ""
                    insert_step_param(step_id, param_name, str(param_value))
            else:
                print("Function '{}' not found in file '{}'".format(function_name, self.file_path))
        except Exception as e:
            print("Error capturing function parameters:", e)

    def capture_function_params1(self, function_name, step_id):
        try:
            module = __import__(self.file_path[:-3])
            function = getattr(module, function_name)
            params = inspect.signature(function).parameters
            for param_name in params:
                param_value = params[param_name].default if params[param_name].default != inspect._empty else ""
                insert_step_param(step_id, param_name, str(param_value))
        except Exception as e:
            print("Error capturing function parameters:", e)
