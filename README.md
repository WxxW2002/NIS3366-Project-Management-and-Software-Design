## WX To Do - manage everything everywhere all at once

 项目管理与软件设计小作业
 
 一个简单的目标为在Linux下使用的任务管理器，用来管理你的工作与学习任务


demo
-----

boot animation:
 
<img src="/demo/boot.jpg" width = "500" height = "360" alt="LRU list">

normal theme:

<img src="/demo/2.jpg" width = "500" height = "360" alt="LRU list">

color theme:

<img src="/demo/4.jpg" width = "500" height = "360" alt="LRU list">

image theme:

<img src="/demo/3.jpg" width = "500" height = "360" alt="LRU list">

structure:
-----
* `src/` - Source code
  * `src/__pycache__` - Contain python cache files
  * `src/data` - Data directory
    * `src/data/settings.json` - Settings data file
    * `src/data/task_data.json` - Tasks data file
  * `src/photos` - Photos directory
  * `src/main.py` - Main function
  * `src/ui.py` - UI file
  * `src/notifications.py` - Notification function file
  * `src/theme.py` - Theme function file
  * `src/task.py` - Task class
  * `src/task_list.py` - Task list class
  
* `docs/` - Documentation directory

* `demo/` - Demo directory

dependent packages and installation:
-----
PyQt6: ```pip install PyQt6```
pynotifier: ```pip install py-notify```

build&run:
-----
* `cd src`
* `python main.py`
 
 Implemented functions
 -----
 - [x] 创建任务清单：用户可以创建任务清单，为每个任务添加标题、截止日期、重复提醒等
 - [x] 自动排序：用户可以通过通过拖拽的方式改变顺序，优先级高的任务默认显示在上方
 - [x] 任务管理：用户可以设置任务的优先级、完成状态、提醒时间、重复周期等
 - [x] 自定义主题：用户可以选择不同的主题颜色以及背景图片，以便更好地个性化任务清单
 - [x] 提醒通知：当任务到期时，WX To Do会通过桌面通知的方式提醒用户
 - [x] 开机引导界面：在打开软件时，会有一个引导动画（动画图片可自定义）
