""" This file contains Help related funcions for displaying user documentation.
It allows you to:
    - setup F1 as a help shortcut
    - display the documentation help for a given subject (plugins, sync, ...)
"""

from gi.repository import Gtk
from webbrowser import open as openurl

from GTG import info


def construct_help_addr(help_addr=None):
    """ Return the url help address for a specific subject
    (default: general help) """
    return info.HELP_URI + {
        "plugins": "/gtg-plugins",
        "sync": "/gtg-add-sync",
    }.get(help_addr, "")


def show_help(help_addr):
    """ Open a specif help page for a given subject """
    help_url = construct_help_addr(help_addr)
    openurl(help_url)
    return True


def add_help_shortcut(widget, help_addr):
    """ Add F1 as a shortcut for help """
    agr = Gtk.AccelGroup()
    widget.add_accel_group(agr)
    key, modifier = Gtk.accelerator_parse('F1')
    agr.connect(key, modifier, Gtk.AccelFlags.VISIBLE,
                lambda *args: show_help(help_addr))
