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

    def remove_task(self, task_title):
        task_to_remove = None
        for task in self.tasks:
            if task.title == task_title:
                task_to_remove = task
                break
    
        if task_to_remove:
            self.tasks.remove(task_to_remove)

        