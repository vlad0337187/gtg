"""
Information where various resources like config, icons, etc. are stored
"""
import os

from GTG.wrappers.xdg import XDG_DATA_HOME, XDG_CONFIG_HOME, XDG_CACHE_HOME

# Folder where core GTG data is stored like services information, tags, etc
DATA_DIR = os.path.join(XDG_DATA_HOME, 'gtg')
# Folder where configuration like opened tasks is stored
CONFIG_DIR = os.path.join(XDG_CONFIG_HOME, 'gtg')

# File defining used services and their parameters
PROJECTS_XMLFILE = os.path.join(DATA_DIR, 'projects.xml')
# File defining used tags
TAGS_XMLFILE = os.path.join(DATA_DIR, 'tags.xml')

# Root is 2 folders up of this file (as it is in GTG/core)
local_rootdir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..'))

# Icons from local folder
ICONS_DIR = os.path.join(local_rootdir, 'data', 'icons')

# Where data & cache for synchronization services is stored
SYNC_DATA_DIR = os.path.join(DATA_DIR, 'backends')
SYNC_CACHE_DIR = os.path.join(XDG_CACHE_HOME, 'gtg')

# Folders where to look for plugins
PLUGIN_DIRS = [os.path.join(local_rootdir, 'GTG', 'plugins')]

# Place for user's plugins installed locally
USER_PLUGINS_DIR = os.path.join(CONFIG_DIR, 'plugins')
if os.path.exists(USER_PLUGINS_DIR):
    PLUGIN_DIRS.append(USER_PLUGINS_DIR)

UI_DIR = os.path.join(local_rootdir, 'GTG', 'gtk', 'ui')

TRANSLATIONS_DIR = os.path.join(local_rootdir, 'translations')


def plugin_configuration_dir(plugin_name):
    """ Returns the directory for plugin configuration. """
    return os.path.join(USER_PLUGINS_DIR, plugin_name)
