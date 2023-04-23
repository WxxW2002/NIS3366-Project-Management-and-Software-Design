# main.py
import os
import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import QTimer, Qt, QRect
from PyQt6.QtGui import QPixmap
from ui import MainWindow
from threading import Thread
from notifications import Notifications

# main function
def main():
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Splash screen
    splash_image = QPixmap(os.path.join("photos", "Hogwarts.jpg"))
    splash_screen = QSplashScreen(splash_image, Qt.WindowType.WindowStaysOnTopHint)

    # Center the splash screen on the screen
    screen_geometry = app.primaryScreen().geometry()
    screen_center = screen_geometry.center()
    splash_screen_center = QRect(0, 0, splash_image.width(), splash_image.height()).center()
    splash_screen.move(screen_center - splash_screen_center)

    splash_screen.show()   

    # Create and display the main application window
    window = MainWindow()

    # Set timers for splash screen and main window
    timer = QTimer()
    timer.singleShot(2000, splash_screen.close)
    timer.singleShot(2000, window.show)

    # Create a Notifications instance and start the check_and_notify loop in a new thread
    notifications = Notifications(window.task_list)
    notify_thread = Thread(target=notifications.check_and_notify)
    notify_thread.daemon = True
    notify_thread.start()

    # Start the event loop and exit when it's done
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
