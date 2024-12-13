# main.py
import sys
from PyQt6.QtWidgets import QApplication
from myRize import ActiveWindowMonitor

def main():

    app = QApplication(sys.argv)
    window = ActiveWindowMonitor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()