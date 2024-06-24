from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

class HomeTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: skyblue;")  # Set background color
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Welcome to Tasker Application")
        label.setFont(QFont('Arial', 20))
        layout.addWidget(label)

        help_button = QPushButton("Help")
        help_button.clicked.connect(self.open_help)
        layout.addWidget(help_button)

        documentation_button = QPushButton("Documentation")
        documentation_button.clicked.connect(self.open_documentation)
        layout.addWidget(documentation_button)

        self.setLayout(layout)

    def open_help(self):
        QDesktopServices.openUrl(QUrl("https://example.com/help"))

    def open_documentation(self):
        QDesktopServices.openUrl(QUrl("https://example.com/documentation"))
