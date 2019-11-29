""" Configuration for browser, it contains path to .ui files """

import os


class ViewConfig(object):
    current_rep = os.path.dirname(os.path.abspath(__file__))
    DELETE_UI_FILE = os.path.join(current_rep, "deletion.ui")
    PLUGINS_UI_FILE = os.path.join(current_rep, "plugins.ui")
    BACKENDS_UI_FILE = os.path.join(current_rep, "backends_dialog.ui")
