"""
This is the tool package. It contains some useful function and tool
that could be useful for any part of GTG.
"""

from GTG.core.translations import translate


class GnomeConfig(object):
    CANLOAD = translate("Everything necessary to run this plugin is available.")
    CANNOTLOAD = translate("The plugin can not be loaded")
    miss1 = translate("Some python modules are missing")
    miss2 = translate("Please install the following python modules:")
    MODULEMISSING = "%s \n%s" % (miss1, miss2)
    dmiss1 = translate("Some remote dbus objects are missing.")
    dmiss2 = translate("Please start the following applications:")
    DBUSMISSING = "%s \n%s" % (dmiss1, dmiss2)
    bmiss1 = translate("Some modules and remote dbus objects are missing.")
    bmiss2 = translate("Please install or start the following components:")
    MODULANDDBUS = "%s \n%s" % (bmiss1, bmiss2)
    umiss1 = translate("Unknown error while loading the plugin.")
    umiss2 = translate("Very helpful message, isn't it? Please report a bug.")
    UNKNOWN = "%s \n%s" % (umiss1, umiss2)
