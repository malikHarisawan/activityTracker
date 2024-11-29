# active_window_updater.py
import time
import psutil
import win32gui
import win32process
import win32api

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
        process_description = get_exe_description(file_path)
        return process_title, process_description, window_title, pid
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None, None, None, None

def update_active_window(current_date, last_switch_time, last_app, last_date, time_spent):
    current_time = time.time()
    process_name, process_description, window_name, pid = get_active_window()

    if window_name is None:
        return last_switch_time, last_app, last_date, time_spent

    win_app = window_name.split("-")[-1].strip()

    if process_description == "Application Frame Host":
        current_app = win_app
    else:
        current_app = process_description

    if current_date != last_date:
        last_switch_time = current_time
        last_app = None
        last_date = current_date

    if current_app != last_app and process_description:
        if last_app is not None:
            time_diff = current_time - last_switch_time
            if current_date not in time_spent:
                time_spent.setdefault(current_date, {})
            if last_app not in time_spent[current_date]:
                time_spent[current_date][last_app] = 0
            time_spent[current_date][last_app] += time_diff

        last_app = current_app
        last_switch_time = current_time

    return last_switch_time, last_app, last_date, time_spent
