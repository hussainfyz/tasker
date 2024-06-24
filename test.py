import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRectF


class FlowDiagramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.steps = [
            {"name": "Step 1", "rect": QRectF(50, 50, 100, 50), "action": self.show_logs},
            {"name": "Step 2", "rect": QRectF(200, 50, 100, 50), "action": self.show_logs},
            {"name": "Step 3", "rect": QRectF(350, 50, 100, 50), "action": self.show_logs}
        ]

    def show_logs(self, step_name):
        print(f"Showing logs for {step_name}")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black)
        painter.setPen(pen)
        for step in self.steps:
            painter.drawRect(step["rect"])
            painter.drawText(step["rect"], Qt.AlignCenter, step["name"])

    def mousePressEvent(self, event):
        for step in self.steps:
            if step["rect"].contains(event.pos()):
                step["action"](step["name"])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flow Diagram")
        self.setGeometry(100, 100, 600, 400)

        widget = FlowDiagramWidget()
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
