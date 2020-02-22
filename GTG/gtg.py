#!/usr/bin/env python3

# Getting things GNOME!: a gtd-inspired organizer for GNOME
#
# @author : B. Rousseau, L. Dricot
# @date   : November 2008
#
#   main.py contains the configuration and data structures loader
#   taskbrowser.py contains the main GTK interface for the tasklist
#   task.py contains the implementation of a task and a project
#   taskeditor contains the GTK interface for task editing
#       (it's the window you see when writing a task)
#   backends/xml_backend.py is the way to store tasks and project in XML
#
#   tid stand for "Task ID"
#   pid stand for "Project ID"
#   uid stand for "Universal ID" which is generally the tuple [pid,tid]
#
#   Each id are *strings*
#   tid are the form "X@Y" where Y is the pid.
#   For example : 21@2 is the 21st task of the 2nd project
#   This way, we are sure that a tid is unique accross multiple projects
#
#==============================================================================

"""This is the top-level exec script for running GTG"""

#=== IMPORT ===================================================================
import os
import sys
sys.path.append('/usr/lib/python3/dist-packages')  # fix running with system dbus, gi, but inside of pipenv
import logging

import gi
import dbus

from optparse import OptionParser
gi.require_version('Gdk', '3.0')
from gi.repository.Gdk import Screen

from GTG                   import info
from GTG.backends          import BackendFactory
from GTG.core.datastore    import DataStore
from GTG.core.dirs         import DATA_DIR
from GTG.core.translations import translate
from GTG.gtk.dbuswrapper   import BUSNAME, BUSINTERFACE
from GTG.gtk.manager       import Manager
from GTG.tools.logger      import Log

from . import init

#=== OBJECTS ==================================================================

# code borrowed from Specto. Avoid having multiples instances of gtg
# reading the same tasks
# that's why we put the pid file in the data directory :
# we allow one instance of gtg by data directory.


def check_instance(directory, uri_list=[]):
    """
    Check if gtg is already running.
    If so, open the tasks whose ids are in the uri_list
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    pidfile = os.path.join(directory, "gtg.pid")
    if not os.path.exists(pidfile):
        open(pidfile, "w").close()
        os.chmod(pidfile, 0o600)

    # see if gtg is already running
    pid = open(pidfile, "r").readline()
    if pid:
        p = os.system("/bin/ps %s >/dev/null" % pid)
        p_name = os.popen("/bin/ps -f %s" % pid).read()
        if p == 0 and "gtg" in p_name:
            print(translate("gtg is already running!"))
            try:
                d = dbus.SessionBus().get_object(BUSNAME, BUSINTERFACE)
                d.ShowTaskBrowser()
                # if the user has specified a task to open, do that
                for uri in uri_list:
                    if uri.startswith("gtg://"):
                        d.OpenTaskEditor(uri[6:])
                raise SystemExit
            except dbus.exceptions.DBusException:
                # If we cant't connect to the interface (e.g. changed interface
                # between GTG versions), we won't do anything more
                raise SystemExit

    # write the pid file
    with open(pidfile, "w") as f:
        f.write(repr(os.getpid()))


def remove_pidfile(directory):
    """ Remove the pid file """
    pidfile = os.path.join(directory, "gtg.pid")
    try:
        os.remove(pidfile)
    except OSError:
        # Ignore missing PID file
        pass


def x_is_running():
    """ Return True if GTG could be displayed on the current XServer """
    try:
        if Screen().get_default().get_display():
            return True
    except RuntimeError as exc:
        print(exc)
    return False

#=== MAIN CLASS ===============================================================


def parse_args():
    """ Parse arguments """
    parser = OptionParser()
    parser.add_option('-b', '--boot-test', action='store_true',
                      dest='boot_test',
                      help="Exit after completing boot-up actions",
                      default=False)
    parser.add_option('-c', '--no-crash-handler', action='store_true',
                      dest='no_crash_handler',
                      help="Disable the automatic crash handler",
                      default=False)
    parser.add_option('-d', '--debug', action='store_true', dest='debug',
                      help="Enable debug output", default=False)
    parser.add_option('-t', '--title', action='store',
                      help="Use special title for windows' title")
    parser.add_option('-v', '--version', action='store_true',
                      dest='print_version', help="Print GTG's version number",
                      default=False)
    return parser.parse_args()


def main():
    '''
    Calling this starts the full GTG experience
    '''
    options, args = parse_args()
    if options.print_version:
        print("GTG (Getting Things GNOME!)", info.VERSION)
        print()
        print("For more information:", info.URL)
        sys.exit(0)

    elif not x_is_running():
        print("Could not open X display")
        sys.exit(1)

    if options.title is not None:
        info.NAME = options.title

    datastore = core_main_init(options, args)
    # Launch task browser
    manager = Manager(datastore)
    # main loop
    # To be more user friendly and get the logs of crashes, we show an apport
    # hooked window upon crashes
    if not options.no_crash_handler:
        from GTG.gtk.crashhandler import signal_catcher
        with signal_catcher(manager.close_browser):
            manager.main(once_thru=options.boot_test, uri_list=args)
    else:
        manager.main(once_thru=options.boot_test, uri_list=args)
    core_main_quit(datastore)


def core_main_init(options=None, args=None):
    '''
    Part of the main function prior to the UI initialization.
    '''
    # Debugging subsystem initialization
    if options.debug:
        Log.setLevel(logging.DEBUG)
        Log.debug("Debug output enabled.")
    else:
        Log.setLevel(logging.INFO)

    Log.set_debugging_mode(options.debug)
    check_instance(DATA_DIR, args)

    datastore = DataStore()

    # Register backends
    backends_list = BackendFactory().get_saved_backends_list()

    for backend_dic in backends_list:
        datastore.register_backend(backend_dic)

    # save the backends directly to be sure projects.xml is written
    datastore.save(quit=False)

    return datastore


def core_main_quit(datastore):
    '''
    Last bits of code executed in GTG, after the UI has been shut off.
    Currently, it's just saving everything.
    '''
    # Ending the application: we save configuration
    datastore.save(quit=True)
    remove_pidfile(DATA_DIR)
    sys.exit(0)
