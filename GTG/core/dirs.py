"""
Information where various resources like config, icons, etc. are stored.
"""
import os
import os.path as op


# Root is 2 folders up of this file (as it is in GTG/core)
local_rootdir    = op.abspath(op.join(op.dirname(__file__), '..', '..'))
TEMP_DIR_LOCAL   = op.join(local_rootdir, 'tmp')
ICONS_DIR        = op.join(local_rootdir, 'data', 'icons')     # Icons from local folder
PLUGIN_DIRS      = [op.join(local_rootdir, 'GTG', 'plugins')]  # Folders where to look for plugins
UI_DIR           = op.join(local_rootdir, 'GTG', 'gtk', 'ui')
TRANSLATIONS_DIR = op.join(local_rootdir, 'translations')


def init():
    """
    Add variables depending on XDG to module.
    They are not defined in module-level, because XDG module uses variables,
    set in app after importing this module first time.
    """
    from GTG.wrappers.xdg import XDG_DATA_HOME, XDG_CONFIG_HOME, XDG_CACHE_HOME

    DATA_DIR         = op.join(XDG_DATA_HOME,   'gtg')           # Folder where core GTG data is stored like services information, tags, etc
    CONFIG_DIR       = op.join(XDG_CONFIG_HOME, 'gtg')           # Folder where configuration like opened tasks is stored
    PROJECTS_XMLFILE = op.join(DATA_DIR,        'projects.xml')  # File defining used services and their parameters
    TAGS_XMLFILE     = op.join(DATA_DIR,        'tags.xml')      # File defining used tags
    SYNC_DATA_DIR    = op.join(DATA_DIR,        'backends')      # Where data & cache for synchronization services is stored
    SYNC_CACHE_DIR   = op.join(XDG_CACHE_HOME,  'gtg')
    USER_PLUGINS_DIR = op.join(CONFIG_DIR,      'plugins')       # Place for user's plugins installed locally

    if op.exists(USER_PLUGINS_DIR):
        PLUGIN_DIRS.append(USER_PLUGINS_DIR)

    local_variables  = locals()
    module_variables = globals()

    def attach_local_variables_to_module():
        for name, value in local_variables.items():
            module_variables[name] = value

    attach_local_variables_to_module()


def plugin_configuration_dir(plugin_name):
    """ Returns the directory for plugin configuration. """
    return op.join(USER_PLUGINS_DIR, plugin_name)
