from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QListWidget


class TaskParameters(QWidget):
    def __init__(self):
        super(TaskParameters, self).__init__()

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Task Parameters")
        self.layout.addWidget(self.title)

        self.form_layout = QFormLayout()

        self.param_name = QLineEdit()
        self.param_value = QLineEdit()

        self.form_layout.addRow("Parameter Name:", self.param_name)
        self.form_layout.addRow("Parameter Value:", self.param_value)

        self.add_button = QPushButton("Add Parameter")
        self.add_button.clicked.connect(self.add_parameter)
        self.form_layout.addWidget(self.add_button)

        self.param_list = QListWidget()
        self.layout.addWidget(self.param_list)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)

    def add_parameter(self):
        param_name = self.param_name.text()
        param_value = self.param_value.text()

        if param_name and param_value:
            self.param_list.addItem(f"{param_name}: {param_value}")
            self.param_name.clear()
            self.param_value.clear()
