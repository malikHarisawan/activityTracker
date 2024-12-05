import sys
import psutil
import win32gui
import win32process
import win32api
import time
import json
import os
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
from graph import plot_chart
from PyQt6.QtCore import QTimer, QEventLoop, QDate
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QDateEdit,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)
from category_manager import CategoryManager
from config import APP_CATEGORIES
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pywinauto import Application
import matplotlib.pyplot as plt
from urllib.parse import urlparse

def get_exe_description(file_path):
    try:
        info = win32api.GetFileVersionInfo(
            file_path, "\\StringFileInfo\\040904b0\\FileDescription"
        )
        return info
    except:
        return "No Description Available"


def get_active_window():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process = psutil.Process(pid)
        process_title = process.name()
        file_path = process.exe()
        window_title = win32gui.GetWindowText(hwnd)
       
        active_app = None
        if process_title.lower() != "chrome.exe":
             active_app = get_exe_description(file_path)
             return active_app
        elif process_title.lower() == "chrome.exe":
            try:
                app = Application(backend='uia')
                app.connect(process=pid)
                dlg = app.top_window()
                element_name = "Address and search bar"
                url_bar = dlg.child_window(title=element_name, control_type="Edit")

                url = url_bar.get_value()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
  
                parsed_url = urlparse(url)
                active_app = parsed_url.netloc
                return active_app
            except Exception:
                return None
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


class ActiveWindowMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.category_manager = CategoryManager(APP_CATEGORIES)
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        self.decrement_button = QPushButton("◀", self)
        self.increment_button = QPushButton("▶", self)
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        button_layout.addWidget(self.decrement_button)
        button_layout.addWidget(self.date_edit)
        button_layout.addWidget(self.increment_button)
        cur_date = self.date_edit.date()
        cur_date = cur_date.toString("yyyy-MM-dd")
        self.figure, _ = plot_chart(cur_date)
        self.canvas = FigureCanvasQTAgg(self.figure)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.canvas)

        self.increment_button.clicked.connect(self.increment_date)
        self.decrement_button.clicked.connect(self.decrement_date)
        self.date_edit.dateChanged.connect(self.update_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.time_spent = {}
        self.last_switch_time = time.time()
        self.last_app = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_active_window)
        self.timer.start(1000)

        self.isPopUpActive = False
        # save data real time
        # self.save_timer = QTimer(self)
        # self.save_timer.timeout.connect(self.save_data)
        # self.save_timer.start(1000)

        self.allowed_apps = ["Code.exe", "chrome.exe", "python.exe", "explorer.exe"]
        self.start_time = time.time()
        self.load_data()

    def increment_date(self):
        current_date = self.date_edit.date()
        new_date = current_date.addDays(1)
        self.date_edit.setDate(new_date)

    def decrement_date(self):
        current_date = self.date_edit.date()
        new_date = current_date.addDays(-1)
        self.date_edit.setDate(new_date)

    def update_label(self, date):
        new_date = date.toString("yyyy-MM-dd")
        plt.close(self.figure)
        self.figure.clear()
        self.figure, _ = plot_chart(new_date)
        self.canvas.figure = self.figure
        self.canvas.draw()

    def show_popup(self, current_app, title):
        if self.isPopUpActive:
            return
        self.isPopUpActive = True

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setMinimumSize(1000, 1000)
        timeout_seconds = 5
        msg_box.setText(f"{title} is not allowed.")
        msg_box.setInformativeText(f"Getting distracted in {timeout_seconds} seconds.")
        dismiss_button = msg_box.addButton("Dismiss", QMessageBox.ButtonRole.AcceptRole)
        stay_focus_button = msg_box.addButton(
            "Stay Focus", QMessageBox.ButtonRole.DestructiveRole
        )
        msg_box.setDefaultButton(dismiss_button)

        countdown_timer = QTimer()
        countdown_timer.setInterval(1000)

        def update_countdown():
            nonlocal timeout_seconds
            timeout_seconds -= 1
            msg_box.setInformativeText(
                f"Getting distracted in {timeout_seconds} seconds."
            )
            if timeout_seconds == 0:
                countdown_timer.stop()
                msg_box.accept()
                os.system(f"taskkill /f /im {current_app}")

        countdown_timer.timeout.connect(update_countdown)
        countdown_timer.start()

        loop = QEventLoop()
        msg_box.finished.connect(loop.quit)
        msg_box.show()
        loop.exec()

        countdown_timer.stop()
        self.isPopUpActive = False
        if msg_box.clickedButton() == dismiss_button:
            self.allowed_apps.append(current_app)
            return True
        elif msg_box.clickedButton() == stay_focus_button:
            os.system(f"taskkill /f /im {current_app}")
            return False
        return False

    def close_unallowed_app(self, app, win_app):
        if not self.show_popup(app, win_app):
            os.system(f"taskkill /f /im {app}")
            time.sleep(0.5)

    def update_active_window(self):
        current_date = time.strftime("%Y-%m-%d")
        current_time = time.time()
        active_app = get_active_window()

        # if active_app:
        #    print(active_app)

        current_app = active_app

        # if process_name not in self.allowed_apps:
        #     self.close_unallowed_app(process_name, win_app)

        if not hasattr(self, "last_date"):
            self.last_date = current_date

        if current_date != self.last_date:
            self.save_data()
            self.last_switch_time = current_time
            self.last_app = None
            self.last_date = current_date

        if current_app != self.last_app:
            if self.last_app is not None:
                time_diff = current_time - self.last_switch_time
                
                if self.last_date not in self.time_spent:
                    self.time_spent[self.last_date] = {"apps": {}, "categories": {}}
                
                if self.last_app not in self.time_spent[self.last_date]["apps"]:
                    self.time_spent[self.last_date]["apps"][self.last_app] = 0
                
                self.time_spent[self.last_date]["apps"][self.last_app] += time_diff
                
                category = self.category_manager.get_app_category(self.last_app)
                if category not in self.time_spent[self.last_date]["categories"]:
                    self.time_spent[self.last_date]["categories"][category] = 0
                
                self.time_spent[self.last_date]["categories"][category] += time_diff


            self.last_app = current_app
            self.last_switch_time = current_time

        # self.figure = plot_chart()
        # self.canvas.figure = self.figure
        # self.canvas.draw()

    def load_data(self):
        if os.path.exists("activity_data.json"):
            with open("activity_data.json", "r") as file:
                self.time_spent = json.load(file)

    def save_data(self):
        if self.isPopUpActive:
            return

        current_time = time.time()
        current_date = time.strftime("%Y-%m-%d")

        if self.last_app:

            time_diff = current_time - self.last_switch_time

            if self.last_date not in self.time_spent[self.last_date]:
                 self.time_spent[self.last_date] = {"apps": {}, "categories": {}}
            self.last_switch_time = current_time

            if self.last_app not in self.time_spent[self.last_date]["apps"]:
                self.time_spent[self.last_date]["apps"][self.last_app] = 0
            self.time_spent[self.last_date]["apps"][self.last_app] += time_diff
                
            category = self.category_manager.get_app_category(self.last_app)
            if category not in self.time_spent[self.last_date]["categories"]:
                self.time_spent[self.last_date]["categories"][category] = 0    
            self.time_spent[self.last_date]["categories"][category] += time_diff

        with open("activity_data.json", "w") as file:
            json.dump(self.time_spent, file)

    def closeEvent(self, event):
        self.save_data()
        event.accept()


app = QApplication(sys.argv)
window = ActiveWindowMonitor()
window.show()
sys.exit(app.exec())
