# main_app.py

import sys,os
tasker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout

from manage_tab import ManageTab
#from run_tab import
from monitor_tab import MonitorTab
#from run_task_window import RunTaskWindow
from gui.runtask import runtask_window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.manage_tab = ManageTab()
        #self.run_tab = RunTab()
        self.monitor_tab = MonitorTab()
        self.runwindow=runtask_window.RunTaskWindow()
        self.tab_widget.addTab(self.manage_tab, "Manage")
        self.tab_widget.addTab(self.runwindow, "Run")
        self.tab_widget.addTab(self.monitor_tab, "Monitor")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
