from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QDateTimeEdit


class TaskScheduler(QWidget):
    def __init__(self):
        super(TaskScheduler, self).__init__()

        self.layout = QVBoxLayout(self)

        self.title = QLabel("Task Scheduler")
        self.layout.addWidget(self.title)

        self.form_layout = QFormLayout()

        self.schedule_time = QDateTimeEdit()
        self.schedule_time.setCalendarPopup(True)

        self.form_layout.addRow("Schedule Time:", self.schedule_time)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)
