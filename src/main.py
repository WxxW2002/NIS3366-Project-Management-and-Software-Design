# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow

from threading import Thread
from notifications import Notifications


def main():
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create and display the main application window
    window = MainWindow()
    window.show()

    # Create a Notifications instance and start the check_and_notify loop in a new thread
    notifications = Notifications(window.task_list)
    notify_thread = Thread(target=notifications.check_and_notify)
    notify_thread.daemon = True
    notify_thread.start()

    # Start the event loop and exit when it's done
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
