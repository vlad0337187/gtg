'''
The tomboy backend. The actual backend is all in GenericTomboy, since it's
shared with the Gnote backend.
'''

from GTG.backends.genericbackend import GenericBackend
from GTG.backends.generictomboy import GenericTomboy
from GTG.core.translations import translate


class Backend(GenericTomboy):
    '''
    A simple class that adds some description to the GenericTomboy class.
    It's done this way since Tomboy and Gnote backends have different
    descriptions and Dbus addresses but the same backend behind them.
    '''

    _general_description = {
        GenericBackend.BACKEND_NAME: "backend_tomboy",
        GenericBackend.BACKEND_HUMAN_NAME: translate("Tomboy"),
        GenericBackend.BACKEND_AUTHORS: ["Luca Invernizzi"],
        GenericBackend.BACKEND_TYPE: GenericBackend.TYPE_READWRITE,
        GenericBackend.BACKEND_DESCRIPTION:
        translate("This synchronization service can synchronize all or part of"
          " your Tomboy notes in GTG. If you decide it would be handy to"
          " have one of your notes in your TODO list, just tag it "
          "with the tag you have chosen (you'll configure it later"
          "), and it will appear in GTG."),
    }

    _static_parameters = {
        GenericBackend.KEY_ATTACHED_TAGS: {
            GenericBackend.PARAM_TYPE: GenericBackend.TYPE_LIST_OF_STRINGS,
            GenericBackend.PARAM_DEFAULT_VALUE: ["@GTG-Tomboy"]},
    }

    BUS_ADDRESS = ("org.gnome.Tomboy",
                   "/org/gnome/Tomboy/RemoteControl",
                   "org.gnome.Tomboy.RemoteControl")
