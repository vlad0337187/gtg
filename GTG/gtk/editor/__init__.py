"""
The task editing GUI
"""
import os


class GnomeConfig(object):
    current_rep = os.path.dirname(os.path.abspath(__file__))
    CALENDAR_UI_FILE = os.path.join(current_rep, "calendar.ui")

    # Number of second between to save in the task editor
    SAVETIME = 7
