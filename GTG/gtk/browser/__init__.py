"""
The GTK frontend for browsing collections of tasks.

This is the gnome_frontend package. It's a GTK interface that wants to be
simple, HIG compliant and well integrated with Gnome.
"""
import os

from GTG.core.translations import translate


class GnomeConfig(object):
    _current_dir       = os.path.dirname(os.path.abspath(__file__))
    BROWSER_UI_FILE    = os.path.join(_current_dir, "ui/taskbrowser.ui")
    MODIFYTAGS_UI_FILE = os.path.join(_current_dir, "ui/modifytags_dialog.ui")

    MARK_DONE = translate("Mark as Done")
    MARK_DONE_TOOLTIP = translate("Mark the selected task as done")
    MARK_UNDONE = translate("Mark as not Done")
    MARK_UNDONE_TOOLTIP = translate("Mark the selected task as not done")
    MARK_DISMISS = translate("Dismiss")
    MARK_DISMISS_TOOLTIP = translate("Mark the task as not to be done anymore")
    MARK_UNDISMISS = translate("Undismiss")
    MARK_UNDISMISS_TOOLTIP = translate("Mark the selected task as to be done")
    DELETE_TOOLTIP = translate("Permanently remove the selected task")
    EDIT_TOOLTIP = translate("Edit the selected task")
    NEW_TASK_TOOLTIP = translate("Create a new task")
    NEW_SUBTASK_TOOLTIP = translate("Create a new subtask")
    WORKVIEW_TOGGLE_TOOLTIP = translate("Display only the currently actionable tasks")
    TAG_IN_WORKVIEW_TOGG = translate("Hide this tag from the workview")
    TAG_NOTIN_WORKVIEW_TOGG = translate("Show this tag in the workview")
    QUICKADD_ENTRY_TOOLTIP = \
        translate("You can create, open or filter your tasks here")
    QUICKADD_ICON_TOOLTIP = translate("Clear")
