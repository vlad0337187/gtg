import os


_current_dir = os.path.dirname(os.path.abspath(__file__))

CALENDAR_UI_FILE = os.path.join(_current_dir, 'ui/calendar.ui')
EDITOR_UI_FILE   = os.path.join(_current_dir, "ui/taskeditor.ui")

AUTO_SAVE_TASK_SECONDS = 7
