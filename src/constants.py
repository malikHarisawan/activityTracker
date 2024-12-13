# constants.py
ALLOWED_APPS = [
    "chrome.exe",
    "python.exe", 
    "Code.exe",
    "devenv.exe",
    "explorer.exe"
]

DISTRACTED_APPS = ["WindowsTerminal.exe"]
RESTRICTED_DOMAINS = ["youtube.com", "chatgpt.com"]

SAVE_INTERVAL = 60000  # 60 seconds
UPDATE_INTERVAL = 1000  # 1 second
POPUP_TIMEOUT = 5  # seconds

UI_DIMENSIONS = {
    "popup_width": 400,
    "popup_height": 150
}