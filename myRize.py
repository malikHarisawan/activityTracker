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
    if pid <= 0:
        return None
    try:
         
        process = psutil.Process(pid)
        process_title = process.name()
       # print(process_title)
        file_path = process.exe()
        window_title = win32gui.GetWindowText(hwnd)
       
        active_app = None
        if process_title.lower() != "chrome.exe":
             active_app = get_exe_description(file_path)
             return active_app,process_title
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
                return active_app,process_title
            except Exception:
                return None,None
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None,None


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
        self.save_timer = QTimer(self)
        self.save_timer.timeout.connect(self.save_data)
        self.save_timer.start(60000)

        self.allowed_apps = [ "python.exe","WindowsTerminal.exe", "Code.exe","devenv.exe","explorer.exe"]
        self.distracted_apps = ["skype.exe","chrome.exe" ]
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
        
    def show_popup(self, process_title, current_app):
        if self.isPopUpActive:
            return
        self.isPopUpActive = True
        
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setMinimumSize(1000, 1000)
        timeout_seconds = 5
        msg_box.setText(f"{current_app} is not allowed.")
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
                os.system(f"taskkill /f /im {process_title}")
        
        countdown_timer.timeout.connect(update_countdown)
        countdown_timer.start()
        
        loop = QEventLoop()
        msg_box.finished.connect(loop.quit)
        msg_box.show()
        loop.exec()
        
        countdown_timer.stop()
        self.isPopUpActive = False
        if msg_box.clickedButton() == dismiss_button:
            self.allowed_apps.append(process_title)
            return True
        elif msg_box.clickedButton() == stay_focus_button:
            os.system(f"taskkill /f /im {process_title}")
            return False
        return False 
    
    def close_unallowed_app(self, process_title, app):
        if not self.show_popup(process_title, app):
            os.system(f"taskkill /f /im {app}")
            time.sleep(0.5)

    def update_time_spent(self, time_diff, app, category, date, hour=None):
      
        if date not in self.time_spent:
            self.time_spent[date] = {"apps": {}, "categories": {}, "hourly": {}}
        
        if app not in self.time_spent[date]["apps"]:
            self.time_spent[date]["apps"][app] = 0
        self.time_spent[date]["apps"][app] += time_diff
        
        if category not in self.time_spent[date]["categories"]:
            self.time_spent[date]["categories"][category] = 0
        self.time_spent[date]["categories"][category] += time_diff
        
        if hour is not None:
            if hour not in self.time_spent[date]["hourly"]:
                self.time_spent[date]["hourly"][hour] = {"apps": {}, "categories": {}}
            
            if app not in self.time_spent[date]["hourly"][hour]["apps"]:
                self.time_spent[date]["hourly"][hour]["apps"][app] = 0
            self.time_spent[date]["hourly"][hour]["apps"][app] += time_diff
            
            if category not in self.time_spent[date]["hourly"][hour]["categories"]:
                self.time_spent[date]["hourly"][hour]["categories"][category] = 0
            self.time_spent[date]["hourly"][hour]["categories"][category] += time_diff

    def update_active_window(self):
        current_date = time.strftime("%Y-%m-%d")
        current_time = time.time()
        current_hour = time.strftime("%H:00") 
        result = get_active_window()
        
        if not result:
            return
        else:
            current_app , process_title = result
   

        if process_title not in self.allowed_apps:
            if process_title in self.distracted_apps:
               os.system(f"taskkill /f /im {process_title}")
            else:
                self.close_unallowed_app(process_title, current_app)
     
        if not hasattr(self, "last_date"):
            self.last_date = current_date

        if current_date != self.last_date:
            self.last_switch_time = current_time
            self.last_app = None
            self.last_date = current_date

        if current_app != self.last_app:
            if self.last_app is not None:
                time_diff = current_time - self.last_switch_time
                
                category = self.category_manager.get_app_category(self.last_app)

                self.update_time_spent(time_diff, self.last_app, category, self.last_date, current_hour)

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
            current_hour = time.strftime("%H:00")  

            if self.last_app:
                time_diff = current_time - self.last_switch_time
                category = self.category_manager.get_app_category(self.last_app)
                self.update_time_spent(time_diff, self.last_app, category, current_date, current_hour)
                self.last_switch_time = current_time

            with open("activity_data.json", "w") as file:
                json.dump(self.time_spent, file, indent=4)

    def closeEvent(self, event):
        self.save_data()
        event.accept()


app = QApplication(sys.argv)
window = ActiveWindowMonitor()
window.show()
sys.exit(app.exec())
