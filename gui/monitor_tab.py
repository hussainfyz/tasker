from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class MonitorTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("This is the Monitor GUI")
        layout.addWidget(label)
        self.setLayout(layout)
