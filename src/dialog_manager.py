from PyQt6.QtWidgets import QDialog, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QScreen, QPixmap
from constants import UI_DIMENSIONS, POPUP_TIMEOUT


class DistractedAppDialog(QDialog):
    def __init__(self, parent, current_app):
        super().__init__(parent)
     
        self.current_app = current_app
        self.timeout_seconds = POPUP_TIMEOUT
        self._setup_ui()
        self._center_on_screen()
        self._apply_styles()

    def _setup_ui(self):
        self.setWindowTitle("Distracted App Alert")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setModal(True)
        self.setMinimumSize(
            UI_DIMENSIONS["popup_width"], 
            UI_DIMENSIONS["popup_height"]
        )


        self.logo_label = QLabel()
        pixmap = QPixmap("C:/Users/malik/OneDrive/Pictures/welcome-left.png")  
        
        
        desired_width = 200 
        desired_height = 200  
        
        
        scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setFixedSize(desired_width, desired_height)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(self._get_message())
        self.label.setWordWrap(True)

        self.dismiss_button = QPushButton("Dismiss")
        self.stay_focus_button = QPushButton("Stay Focus")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.dismiss_button)
        button_layout.addWidget(self.stay_focus_button)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.logo_label)  # Add logo to the layout
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.dismiss_button.clicked.connect(self.dismiss_action)
        self.stay_focus_button.clicked.connect(self.stay_focus_action)

    def _center_on_screen(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        center_point = screen_geometry.center()
        self.move(center_point - self.rect().center())

    def _get_message(self):
        return f"{self.current_app} is not allowed.\n  Getting distracted."

    def dismiss_action(self):
        self.accept()

    def stay_focus_action(self):
        self.reject()

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #2E3440;
                color: #D8DEE9;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Arial';
            }
            QLabel {
                font-size: 18px;
                color: #D8DEE9;
                font-family: 'Arial';
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #4C566A;
            }
            QPushButton#dismiss_button {
                background-color: #BF616A;
            }
            QPushButton#dismiss_button:hover {
                background-color: #D08770;
            }
            QPushButton#dismiss_button:pressed {
                background-color: #A3BE8C;
            }
        """)
        self.dismiss_button.setObjectName("dismiss_button")
        self.stay_focus_button.setObjectName("stay_focus_button")