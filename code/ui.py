# ui.py
from PyQt6.QtWidgets import QAbstractItemView,QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QInputDialog, QLineEdit, QColorDialog
from PyQt6.QtWidgets import   QPushButton,  QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QInputDialog, QComboBox, QDateEdit, QMenu
from task_list import TaskList
from PyQt6.QtGui import  QAction, QColor, QPalette, QFont
from theme import Theme
from PyQt6.QtCore import Qt, QSize, QPoint
from task import Task
from datetime import datetime, timedelta
from PyQt6.QtCore import QTimer
from notifications import Notification
from plyer import notification

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            self.clearSelection()
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.theme = Theme()

        self.task_list = TaskList()

        self.init_ui()
        self.setWindowTitle("WX To Do")
        self.setGeometry(100, 100, 600, 600)  # Increase the height to 800


    def init_ui(self):
        self.layout = QVBoxLayout()

        self.task_list_widget = CustomListWidget(self)
        self.task_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.task_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.task_list_widget.setDragEnabled(True)
        self.task_list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.layout.addWidget(self.task_list_widget)

        # style sheet for the list widget
        self.task_list_widget.setStyleSheet("""
            CustomListWidget {
                background-color: transparent;
                border: none;
            }
            CustomListWidget::item {
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
        """)

        self.task_list_widget.dropEvent = self.dropEvent  

        self.controls_layout = QHBoxLayout()

        self.new_task_button = QPushButton("New Task", self)
        self.new_task_button.clicked.connect(self.create_new_task)
        self.controls_layout.addWidget(self.new_task_button)

        self.priority_label = QLabel("Priority:", self)
        self.controls_layout.addWidget(self.priority_label)

        self.priority_combobox = QComboBox(self)
        self.priority_combobox.addItems(["Low", "Medium", "High"])
        self.controls_layout.addWidget(self.priority_combobox)

        self.repeat_label = QLabel("Repeat:", self)
        self.controls_layout.addWidget(self.repeat_label)

        self.repeat_combobox = QComboBox(self)
        self.repeat_combobox.addItems(["Never", "Daily", "Weekly", "Monthly", "Yearly"])
        self.controls_layout.addWidget(self.repeat_combobox)

        self.change_theme_button = QPushButton("Change Theme", self)
        self.change_theme_button.clicked.connect(self.change_theme)
        self.controls_layout.addWidget(self.change_theme_button)

        self.change_bg_color_button = QPushButton("Change Background Color", self)
        self.change_bg_color_button.clicked.connect(self.change_background_color)
        self.controls_layout.addWidget(self.change_bg_color_button)

        self.layout.addLayout(self.controls_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    # 添加新任务
    def create_new_task(self, title=None, priority=None, repeat=None):
        if not title:
            title, ok_pressed = QInputDialog.getText(self, "New Task", "Task Title:", QLineEdit.EchoMode.Normal, "")

        if title and (not priority or not repeat):
            new_task = Task(title, due_date = datetime.now(), priority = self.priority_combobox.currentText(), repeat = self.repeat_combobox.currentText())
            self.task_list.create_task(new_task)
            self.task_list.sort_tasks_by_priority()

            # Clear the existing items from the list widget
            self.task_list_widget.clear()

            # Add the sorted tasks to the list widget
            for task in self.task_list.tasks:
                item = QListWidgetItem(task.title)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                
                # Set font size
                font = QFont()
                font.setPointSize(14)  # Set your desired font size here
                item.setFont(font)

                # Set fixed row height
                item.setSizeHint(QSize(item.sizeHint().width(), 40))

                # Set the alignment to center
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                item.setForeground(QColor(0, 0, 0) if not task.completed else QColor(210,180,140))
                self.task_list_widget.addItem(item)
            
            self.task_list_widget.setDropIndicatorShown(True)
        
            self.schedule_repeated_tasks()


    def show_context_menu(self, point):
        item = self.task_list_widget.itemAt(point)
        if item:
            context_menu = QMenu(self)

            mark_completed_action = QAction("Mark as Completed", self)
            context_menu.addAction(mark_completed_action)

            due_today_action = QAction("Due today", self)
            context_menu.addAction(due_today_action)

            due_tomorrow_action = QAction("Due tomorrow", self)
            context_menu.addAction(due_tomorrow_action)

            delete_action = QAction("Delete", self)
            context_menu.addAction(delete_action)

            mark_completed_action.triggered.connect(lambda: self.mark_task_completed(item))
            due_today_action.triggered.connect(lambda: self.set_task_due_time(item, 0))
            due_tomorrow_action.triggered.connect(lambda: self.set_task_due_time(item, 1))
            delete_action.triggered.connect(lambda: self.delete_task(item))

            context_menu.exec(self.task_list_widget.mapToGlobal(point))


    def delete_task(self, item):
        row = self.task_list_widget.row(item)
        task = self.task_list.tasks[row]
        self.task_list.remove_task(task)
        self.task_list_widget.takeItem(row)

    def mark_task_completed(self, item):
        # Remove the item from the task list widget
        row = self.task_list_widget.row(item)
        self.task_list_widget.takeItem(row)

        # Mark the task as completed
        task = self.task_list.tasks[row]
        task.set_completed(True)

        # Update the item appearance
        item.setForeground(QColor(210,180,140))

        # Add the completed task back to the bottom of the list widget
        self.task_list_widget.addItem(item)

        # Move the completed task to the end of the task list
        self.task_list.move_task(task, len(self.task_list.tasks) - 1)


    def change_theme(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")

        if file_name:
            self.theme.set_background_image(file_name)
            self.setStyleSheet(self.theme.get_style_sheet())


    def set_background_image(self, file_name):
        self.setStyleSheet(f"background-image: url({file_name});")

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

    # 设置任务的截止日期
    def set_task_due_time(self, item, days_from_now):
        task_title = item.text()
        task = self.task_list.find_task_by_title(task_title)

        # Calculate the due time
        due_date = datetime.now() + timedelta(days=days_from_now)
        due_date = due_date.replace(hour=23, minute=59, second=59, microsecond=0)
        task.set_due_date(due_date)

        # Calculate the time remaining until the due time
        reminder_time = due_date - datetime.now()

        # Schedule the reminder
        QTimer.singleShot(int(reminder_time.total_seconds() * 1000), lambda: self.show_reminder(task))


    def show_reminder(self, task):
        task_title = task.title if task.title else "Untitled Task"
        notification.notify(
            title=task_title,
            message="This task is due now.",
            app_name="WXToDo"
        )

    def schedule_repeated_tasks(self):
        for task in self.task_list.tasks:
            if task.repeat != "Never":
                repeat_interval = {
                    "Daily": 1,
                    "Weekly": 7,
                    "Monthly": 30,
                    "Yearly": 365
                }.get(task.repeat, 0)

                if repeat_interval > 0:
                    current_time = datetime.now()
                    next_due_date = task.due_date + timedelta(days=repeat_interval)

                    while next_due_date < current_time:
                        next_due_date += timedelta(days=repeat_interval)

                    remaining_time = (next_due_date - current_time).total_seconds()
                    QTimer.singleShot(int(remaining_time * 1000), lambda: self.create_new_task(title=task.title, priority=task.priority, repeat=task.repeat))
    def update_task_order(self):
        # Create a list of task titles from the QListWidget items
        titles = [self.task_list_widget.item(i).text() for i in range(self.task_list_widget.count())]

        # Update the task order in the task_list based on the new order in the QListWidget
        self.task_list.tasks = [task for title in titles for task in self.task_list.tasks if task.title == title]

    def dropEvent(self, event):
        super(CustomListWidget, self.task_list_widget).dropEvent(event)
        self.update_task_order()
