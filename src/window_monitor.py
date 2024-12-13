# window_monitor.py
import win32gui
import win32process
import win32api
import psutil
from pywinauto import Application
from urllib.parse import urlparse

class WindowMonitor:
    @staticmethod
    def get_exe_description(file_path):
        try:
            return win32api.GetFileVersionInfo(
                file_path, "\\StringFileInfo\\040904b0\\FileDescription"
            )
        except:
            return "No Description Available"

    @staticmethod
    def get_active_window():
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        
        if pid <= 0:
            return None, None, None

        try:
            process = psutil.Process(pid)
            process_title = process.name()
            file_path = process.exe()
            
            if process_title.lower() != "chrome.exe":
                active_app = WindowMonitor.get_exe_description(file_path)
                return active_app, process_title, None

            return WindowMonitor._handle_chrome_window(pid)
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None, None, None

    @staticmethod
    def _handle_chrome_window(pid):
        try:
            app = Application(backend='uia')
            app.connect(process=pid)
            dlg = app.top_window()
            url_bar = dlg.child_window(
                title="Address and search bar", 
                control_type="Edit"
            )

            url = url_bar.get_value()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            active_app = urlparse(url).netloc
            return active_app, "chrome.exe", dlg
        except Exception:
            return None, None, None