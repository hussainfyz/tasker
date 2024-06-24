import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
print(tasker_dir)
sys.path.insert(0, tasker_dir)


from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from .running_tasks_widget import RunningTasksWidget
from .task_config_widget import TaskConfigWidget


class RunTaskWindow(QMainWindow):
    def __init__(self):
        super(RunTaskWindow, self).__init__()
        self.setWindowTitle("Run Tasks")
        self.setGeometry(300, 300, 1200, 800)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.run_tab = QWidget()
        self.run_tab_layout = QVBoxLayout(self.run_tab)

        self.running_tasks_widget = RunningTasksWidget()
        self.task_config_widget = TaskConfigWidget()

        self.run_tab_layout.addWidget(self.running_tasks_widget)
        self.run_tab_layout.addWidget(self.task_config_widget)

        self.tab_widget.addTab(self.run_tab, "Run")

        self.show()
