# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Getting Things GNOME! - a personal organizer for the GNOME desktop
# Copyright (c) 2008-2013 - Lionel Dricot & Bertrand Rousseau
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
"""
The GTK frontend for browsing collections of tasks.

This is the gnome_frontend package. It's a GTK interface that wants to be
simple, HIG compliant and well integrated with Gnome.
"""
import os

from GTG.core.translations import translate


class GnomeConfig(object):
    current_rep = os.path.dirname(os.path.abspath(__file__))
    BROWSER_UI_FILE = os.path.join(current_rep, "taskbrowser.ui")
    MODIFYTAGS_UI_FILE = os.path.join(current_rep, "modifytags_dialog.ui")

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
