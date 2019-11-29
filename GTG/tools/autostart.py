import os
import shutil

from GTG.wrappers.xdg import XDG_CONFIG_HOME

AUTOSTART_DIRECTORY = os.path.join(XDG_CONFIG_HOME, "autostart")
AUTOSTART_FILE = "gtg.desktop"
AUTOSTART_PATH = os.path.join(AUTOSTART_DIRECTORY, AUTOSTART_FILE)


def enable():
    """ Enable autostart

    Firstly, locate gtg.desktop file. Then link it in AUTOSTART_FILE.
    On Windows, there is no os.symlink, just copy the file. """
    desktop_file_path = None
    this_directory = os.path.dirname(os.path.abspath(__file__))
    for path in ["../..", "../../../applications",
                 "../../../../../share/applications"]:
        fullpath = os.path.join(this_directory, path, AUTOSTART_FILE)
        fullpath = os.path.normpath(fullpath)
        if os.path.isfile(fullpath):
            desktop_file_path = fullpath
            break

    if desktop_file_path:
        if not os.path.exists(AUTOSTART_DIRECTORY):
            os.mkdir(AUTOSTART_DIRECTORY)

        # If the path is a symlink and is broken, remove it
        if os.path.islink(AUTOSTART_PATH) and \
                not os.path.exists(os.path.realpath(AUTOSTART_PATH)):
            os.unlink(AUTOSTART_PATH)

        if os.path.isdir(AUTOSTART_DIRECTORY) and \
                not os.path.exists(AUTOSTART_PATH):
            if hasattr(os, "symlink"):
                os.symlink(desktop_file_path, AUTOSTART_PATH)
            else:
                shutil.copyfile(desktop_file_path, AUTOSTART_PATH)


def disable():
    """ Disable autostart, removing the file in autostart_path """
    if os.path.isfile(AUTOSTART_PATH):
        os.remove(AUTOSTART_PATH)


def is_enabled():
    return os.path.isfile(AUTOSTART_PATH)
