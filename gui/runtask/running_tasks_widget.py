from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QProgressBar


class RunningTasksWidget(QWidget):
    def __init__(self):
        super(RunningTasksWidget, self).__init__()

        self.layout = QVBoxLayout(self)
        self.title = QLabel("Running Tasks")
        self.running_tasks_list = QListWidget()
        self.progress_bar = QProgressBar()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.running_tasks_list)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)
