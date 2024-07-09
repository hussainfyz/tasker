import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QTabWidget, QCheckBox, QFrame, QHBoxLayout, QPushButton,
                             QScrollArea, QDialog)
from PyQt5.QtGui import QColor, QPainter, QBrush, QPalette, QScreen
from PyQt5.QtCore import Qt, QTimer, QSize

from notify_db import fetch_recent_notifications


class NotificationWidget(QFrame):
    def __init__(self, category, heading, message, file_path, parent=None):
        super().__init__(parent)
        self.category = category
        self.heading = heading
        self.message = message
        self.file_path = file_path
        self.initUI()

    def initUI(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setAutoFillBackground(True)
        self.setStyleSheet(self.get_default_style())
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        icon_color = self.get_icon_color(self.category)

        # Create and style heading
        heading_label = QLabel(self.heading)
        heading_label.setStyleSheet(f"font-weight: bold; color: {icon_color};")

        # Create and style message
        message_label = QLabel(self.message)
        message_label.setStyleSheet("color: #000;")

        # Add to layout
        layout.addWidget(heading_label)
        layout.addWidget(message_label)
        self.setLayout(layout)

        # Connect hover events
        self.setMouseTracking(True)
        self.mousePressEvent = self.show_detailed_notification

    def get_default_style(self):
        return """
        background-color: #fff;
        border-radius: 10px;
        padding: 10px;
        """

    def get_hover_style(self):
        return """
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 10px;
        """

    def enterEvent(self, event):
        self.setStyleSheet(self.get_hover_style())

    def leaveEvent(self, event):
        self.setStyleSheet(self.get_default_style())

    def get_icon_color(self, category):
        colors = {
            'normal': '#0000FF',  # Blue
            'important': '#FFFF00',  # Yellow
            'warning': '#FFA500',  # Orange
            'error': '#FF0000',  # Red
            'high_importance': '#8B0000'  # Dark Red
        }
        return colors.get(category, '#008000')  # Default to green

    def show_detailed_notification(self, event):
        try:
            with open(self.file_path, 'r') as file:
                detailed_message = file.read()
        except FileNotFoundError:
            detailed_message = "File not found."

        self.detailed_window = DetailedNotificationWindow(self.heading, detailed_message, self.category)
        self.detailed_window.exec_()


class GradientWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QBrush(QColor(0, 128, 128))  # Adjust gradient colors as needed
        painter.setBrush(gradient)
        painter.drawRect(self.rect())


class DetailedNotificationWindow(QDialog):
    def __init__(self, heading, message, category):
        super().__init__()
        self.setWindowTitle("Detailed Notification")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        category_label = QLabel(f"Category: {category.capitalize()}")
        category_label.setStyleSheet(
            f"font-weight: bold; color: {NotificationWidget(None, None, None, None).get_icon_color(category)};")

        heading_label = QLabel(heading)
        heading_label.setStyleSheet("font-weight: bold;")

        message_label = QLabel(message)
        message_label.setWordWrap(True)

        self.layout.addWidget(category_label)
        self.layout.addWidget(heading_label)
        self.layout.addWidget(message_label)

        self.setGeometry(300, 200, 600, 400)


class NotifierWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notifier")

        # Get screen geometry to set initial window size
        screen_geometry = QApplication.primaryScreen().geometry()
        width = screen_geometry.width() // 4
        height = screen_geometry.height()

        self.setGeometry(100, 100, width, height)  # Set window size

        # Set gradient background for the main window
        pal = self.palette()
        gradient_color1 = QColor(0, 128, 128)  # Adjust gradient colors as needed
        gradient_color2 = QColor(72, 61, 139)
        pal.setBrush(QPalette.Window, QBrush(gradient_color1))
        self.setPalette(pal)

        # Create tab widget
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Apply gradient to tab bar
        tab_palette = self.tab_widget.palette()
        tab_palette.setBrush(QPalette.Button, QBrush(gradient_color2))
        self.tab_widget.setPalette(tab_palette)

        # Create tabs
        self.notifications_tab = GradientWidget()
        self.settings_tab = GradientWidget()

        # Add tabs to tab widget
        self.tab_widget.addTab(self.notifications_tab, "Notifications")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Initialize UI elements for notifications tab
        self.init_notifications_tab()

        # Initialize UI elements for settings tab
        self.init_settings_tab()

        # Fetch and display notifications initially
        self.display_notifications()

        # Setup timer for fetching notifications every minute
        self.fetch_timer = QTimer(self)
        self.fetch_timer.timeout.connect(self.display_notifications)
        self.fetch_timer.start(60000)  # Fetch notifications every 1 minute (60000 milliseconds)

    def init_notifications_tab(self):
        # Layout for notifications tab
        self.notifications_layout = QVBoxLayout()
        self.notifications_tab.setLayout(self.notifications_layout)

    def init_settings_tab(self):
        # Layout for settings tab
        layout = QVBoxLayout()

        # Checkbox options for notification categories
        self.category_checkboxes = {}

        categories = ['normal', 'important', 'warning', 'error', 'high_importance']
        for category in categories:
            checkbox = QCheckBox(category.capitalize(), self.settings_tab)
            checkbox.setChecked(True)  # By default, all categories are shown
            layout.addWidget(checkbox)
            self.category_checkboxes[category] = checkbox

        self.settings_tab.setLayout(layout)

    def display_notifications(self):
        # Clear existing notifications
        for i in reversed(range(self.notifications_layout.count())):
            widget_to_remove = self.notifications_layout.itemAt(i).widget()
            self.notifications_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Fetch notifications from the database
        notifications = fetch_recent_notifications("user1")  # Replace with actual user or dynamic fetching

        # Display notifications
        for notification in notifications:
            print(notification)
            notification_widget = NotificationWidget(notification[2], notification[0], notification[1], notification[3])
            self.notifications_layout.addWidget(notification_widget)

        if not notifications:
            no_notifications_label = QLabel("No new notifications.", self.notifications_tab)
            no_notifications_label.setAlignment(Qt.AlignCenter)
            self.notifications_layout.addWidget(no_notifications_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotifierWindow()
    window.show()
    sys.exit(app.exec_())
