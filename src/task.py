# task.py
from datetime import datetime

class Task:
    def __init__(self, title, due_date=None, due_time=None, reminder_time=None, priority=None, repeat=None, files=None, subtasks=None, completed=False):
        self.title = title
        self.due_date = due_date if due_date else None
        self.due_time = due_time if due_time else None
        self.reminder_time = reminder_time if reminder_time else None
        self.priority = priority if priority else None
        self.repeat = repeat if repeat else False
        self.files = files if files else []
        self.subtasks = subtasks if subtasks else []
        self.completed = completed if completed else False

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "repeat": self.repeat,
            "due_date": self.due_date,
            "completed": self.completed
        }

    def set_due_date(self, due_date):
        self.due_date = due_date

    def set_reminder_time(self, reminder_time):
        self.reminder_time = reminder_time

    def set_priority(self, priority):
        self.priority = priority

    def set_repeat(self, repeat):
        self.repeat = repeat

    def add_file(self, file):
        self.files.append(file)

    def remove_file(self, file):
        self.files.remove(file)

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    def remove_subtask(self, subtask):
        self.subtasks.remove(subtask)

    def set_completed(self, status):
        self.completed = status
     
    # 设置到期时间
    def set_due_time(self, due_time):
        self.due_time = due_time
