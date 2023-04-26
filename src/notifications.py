# notifications.py
import time
from datetime import datetime
from pynotifier import Notification

class Notifications:
    def __init__(self, task_list):
        self.task_list = task_list

    def check_and_notify(self):
        while True:
            for task in self.task_list.tasks:
                if not task.completed:
                    if task.reminder_time and task.reminder_time <= datetime.now():
                        self.notify(task)
                        task.reminder_time = None
                    if task.due_date and task.due_date.date() <= datetime.now().date():
                        self.notify(task, is_due=True)
                        task.due_date = None

            # Check every minute
            time.sleep(60)

    def notify(self, task, is_due=False):
        title = "Task Due" if is_due else "Task Reminder"
        message = f"{task.title} is due!" if is_due else f"Reminder: {task.title}"
        Notification(
            title=title,
            description=message,
            duration=5  # Duration in seconds
        )
