# myRize.py
import sys
import time
import json
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QPushButton, QDialog
from PyQt6.QtCore import QTimer, QDate
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

from window_monitor import WindowMonitor
from dialog_manager import DistractedAppDialog
from time_tracker import TimeTracker
from constants import (
    ALLOWED_APPS, 
    DISTRACTED_APPS, 
    RESTRICTED_DOMAINS,
    SAVE_INTERVAL,
    UPDATE_INTERVAL
)
from category_manager import CategoryManager
from config import APP_CATEGORIES
from graph import plot_chart

class ActiveWindowMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.category_manager = CategoryManager(APP_CATEGORIES)
        self.time_tracker = TimeTracker()
        self._init_ui()
        self._init_timers()

    def _init_ui(self):
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
        cur_date = self.date_edit.date().toString("yyyy-MM-dd")
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

    def _init_timers(self):
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_active_window)
        self.update_timer.start(UPDATE_INTERVAL)

        self.save_timer = QTimer(self)
        self.save_timer.timeout.connect(self.save_data)
        self.save_timer.start(SAVE_INTERVAL)

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

    def show_popup(self, current_app):
        

        dialog = DistractedAppDialog(self, current_app)
        result = dialog.exec()
      
        return result == QDialog.DialogCode.Accepted

    def close_unallowed_app(self, process_title, app):
        if app:
            if not self.show_popup( app):
                os.system(f"taskkill /f /im {process_title}")
                time.sleep(0.5)
            else:
                if process_title not in ALLOWED_APPS:
                   ALLOWED_APPS.append(process_title)

    def update_active_window(self):
        current_date = time.strftime("%Y-%m-%d")
        current_time = time.time()
        current_hour = time.strftime("%H:00")
        
        result = WindowMonitor.get_active_window()
        if not result:
            return

        current_app, process_title, dlg = result
        self._handle_restricted_domains(current_app, dlg)
            

        if process_title not in ALLOWED_APPS:
            if process_title in DISTRACTED_APPS:
                os.system(f"taskkill /f /im {process_title}")
            else:
                self.close_unallowed_app(process_title, current_app)

        self._update_time_tracking(current_app, current_date, current_time, current_hour)

    def _handle_restricted_domains(self, current_app, dlg):
        if current_app in RESTRICTED_DOMAINS and dlg:
        
            if not self.show_popup( current_app):
                
                dlg.type_keys('^w')
            else:
                   RESTRICTED_DOMAINS.remove(current_app)

    def _update_time_tracking(self, current_app, current_date, current_time, current_hour):
        if not hasattr(self, "last_date"):
            self.last_date = current_date

        if current_date != self.last_date:
            self.time_tracker.last_switch_time = current_time
            self.time_tracker.last_app = None
            self.last_date = current_date

        if current_app != self.time_tracker.last_app:
            if self.time_tracker.last_app is not None:
                time_diff = current_time - self.time_tracker.last_switch_time
                category = self.category_manager.get_app_category(self.time_tracker.last_app)
                self.time_tracker.update_time_spent(time_diff, self.time_tracker.last_app, category, self.last_date, current_hour)

            self.time_tracker.last_app = current_app
            self.time_tracker.last_switch_time = current_time

    def load_data(self):
        self.time_tracker.load_data()

    def save_data(self):
        
        self.time_tracker.save_data()

    def closeEvent(self, event):
        self.save_data()
        event.accept()

# app = QApplication(sys.argv)
# window = ActiveWindowMonitor()
# window.show()
# sys.exit(app.exec())