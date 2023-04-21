# task_list.py
from task import Task

class TaskList:
    def __init__(self):
        self.tasks = []

    def create_task(self, new_task):
        self.tasks.append(new_task)

    def sort_tasks_by_priority(self):
        priority_values = {"High": 3, "Medium": 2, "Low": 1, None: 0}
        self.tasks.sort(key=lambda x: priority_values[x.priority], reverse=True)

    def sort_tasks_by_due_date(self):
        self.tasks.sort(key=lambda x: x.due_date)

    def remove_task(self, task):
        self.tasks.remove(task)

    def move_task(self, task, new_position):
        self.tasks.remove(task)
        self.tasks.insert(new_position, task)

    def find_task_by_title(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def get_all_completed_tasks(self):
        return [task for task in self.tasks if task.completed]

    def get_all_incomplete_tasks(self):
        return [task for task in self.tasks if not task.completed]


