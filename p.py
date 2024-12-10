# import ctypes
# from ctypes import wintypes

# def get_file_description(file_path):
#     # Get the size of the version info
#     size = ctypes.windll.version.GetFileVersionInfoSizeW(file_path, None)
#     if size == 0:
#         return None

#     # Create a buffer to store version info
#     buffer = ctypes.create_string_buffer(size)
#     ctypes.windll.version.GetFileVersionInfoW(file_path, None, size, buffer)

#     # Retrieve the list of available languages and code pages
#     r = ctypes.c_void_p()
#     l = ctypes.c_uint()
#     if ctypes.windll.version.VerQueryValueW(buffer, r"\\VarFileInfo\\Translation", ctypes.byref(r), ctypes.byref(l)):
#         # Get the first language and code page
#         lang_code_page = ctypes.cast(r, ctypes.POINTER(wintypes.WORD * 2)).contents
#         lang_code_page_str = f"{lang_code_page[0]:04x}{lang_code_page[1]:04x}"

#         # Query the FileDescription for the detected language
#         query_path = f"\\StringFileInfo\\{lang_code_page_str}\\FileDescription"
#         if ctypes.windll.version.VerQueryValueW(buffer, query_path, ctypes.byref(r), ctypes.byref(l)):
#             description = ctypes.wstring_at(r)
#             return description
#     return None

# # Example usage
# file_path = r"C:\Program Files\WindowsApps\Microsoft.WindowsCalculator_11.2311.0.0_x64__8wekyb3d8bbwe\CalculatorApp.exe"
# description = get_file_description(file_path)
# print(f"Description: {description}")



# import psutil
# import win32gui
# import win32process

# def get_active_window_exe_path():
#     try:
#         # Get the handle of the active window
#         hwnd = win32gui.GetForegroundWindow()
#         if not hwnd:
#             return None, None
        
#         # Get the PID of the process associated with the active window
#         _, pid = win32process.GetWindowThreadProcessId(hwnd)
#         process = psutil.Process(pid)

#         # Get the executable path
#         exe_path = process.exe()

#         # Get the window title
#         window_title = win32gui.GetWindowText(hwnd)

#         return exe_path, window_title
#     except Exception as e:
#         print(f"Error: {e}")
#         return None, None

# # Example usage
# exe_path, window_title = get_active_window_exe_path()

# if exe_path:
#     print(f"Executable Path: {exe_path}")
#     print(f"Window Title: {window_title}")
# else:
#     print("No active window or failed to retrieve path.")

# from pywinauto import Application

# from urllib.parse import urlparse

# try:
#     app = Application(backend='uia')
#     app.connect(title_re=".*Chrome.*")
    
#     dlg = app.top_window()
    
#     element_name = "Address and search bar"
#     url_bar = dlg.child_window(title=element_name, control_type="Edit")
    
    
#     # Get URL and ensure it has a protocol
#     url = url_bar.get_value()
#     if not url.startswith(('http://', 'https://')):
#         url = 'https://' + url
    
    
#     # Parse URL
#     parsed_url = urlparse(url)
#     print(parsed_url)
#     domain = parsed_url.netloc
#     print(domain)

    
#     print(f"Final domain: {domain}")

# except Exception as e:
#     print(f"Error occurred: {str(e)}")

# from datetime import datetime, timedelta

# # Define the starting time and step

# # Print the current time
# # Print the current time in hour:minute AM/PM format
# current_time = datetime.now()
# formatted_time = current_time.strftime("%I:%M %p")
# print(f"Current time: {formatted_time}")


import psutil

def list_chrome_processes():
    chrome_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'chrome.exe':
            chrome_processes.append(proc.info)
    return chrome_processes

# Example Usage
for chrome_proc in list_chrome_processes():
    
    print(f"PID: {chrome_proc['pid']}, Command: {chrome_proc['cmdline']}")
