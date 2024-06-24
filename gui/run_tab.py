import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QListWidget, \
    QListWidgetItem
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QSize


class StatusIndicator(QWidget):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 20, 20)


class TaskItem(QWidget):
    def __init__(self, task_name, status_color, build_status, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()

        self.status_indicator = StatusIndicator(status_color)
        self.layout.addWidget(self.status_indicator)

        self.task_name = QLabel(task_name)
        self.task_name.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.task_name)

        self.build_status = QLabel(build_status)
        self.build_status.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.build_status)

        self.setLayout(self.layout)


class TaskListUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task List")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the main layout
        main_layout = QVBoxLayout()

        # Create a label for the title
        title = QLabel("My Task List")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Create the list widget
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: #f0f0f0;
                font-size: 18px;
            }
            QListWidget::item {
                padding: 10px;
            }
        """)

        # Add some sample tasks
        tasks = [
            ("Task 1: Write code", QColor("green"), "Success"),
            ("Task 2: Review PR", QColor("red"), "Failed"),
            ("Task 3: Write documentation", QColor("yellow"), "Unstable"),
            ("Task 4: Fix bugs", QColor("blue"), "Running")
        ]

        for task_name, status_color, build_status in tasks:
            task_item = TaskItem(task_name, status_color, build_status)
            list_item = QListWidgetItem()
            list_item.setSizeHint(task_item.sizeHint())
            self.task_list.addItem(list_item)
            self.task_list.setItemWidget(list_item, task_item)

        # Add the list widget to the main layout
        main_layout.addWidget(self.task_list)

        # Set the layout to the central widget
        central_widget.setLayout(main_layout)


def main():
    app = QApplication(sys.argv)
    window = TaskListUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
