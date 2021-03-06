import os.path

from gi.repository import Gtk

from GTG.core.translations import translate


class PathUI(Gtk.Box):
    '''Gtk widgets to show a path in a textbox, and a button to bring up a
    filesystem explorer to modify that path (also, a label to describe those)
    '''

    def __init__(self, datastore, backend, width):
        '''
        Creates the textbox, the button and loads the current path.

        @param backend: a backend object
        @param width: the width of the Gtk.Label object
        '''
        super().__init__()
        self.backend   = backend
        self.datastore = datastore
        self._populate_gtk(width)

    def _populate_gtk(self, width):
        '''Creates the Gtk.Label, the textbox and the button

        @param width: the width of the Gtk.Label object
        '''
        label = Gtk.Label(label=translate("Filename:"))
        label.set_line_wrap(True)
        label.set_alignment(xalign=0, yalign=0.5)
        label.set_size_request(width=width, height=-1)
        self.pack_start(label, False, True, 0)
        align = Gtk.Alignment.new(0, 0.5, 1, 0)
        align.set_padding(0, 0, 10, 0)
        self.pack_start(align, True, True, 0)
        self.textbox = Gtk.Entry()
        self.textbox.set_text(self.backend.get_parameters()['path'])
        self.textbox.connect('changed', self.on_path_modified)
        align.add(self.textbox)
        self.button = Gtk.Button()
        self.button.set_label("Edit")
        self.button.connect('clicked', self.on_button_clicked)
        self.pack_start(self.button, False, True, 0)

    def commit_changes(self):
        '''Saves the changes to the backend parameter'''
        self.backend.set_parameter('path', self.textbox.get_text())

    def on_path_modified(self, sender):
        ''' Signal callback, executed when the user edits the path.
        Disables the backend. The user will re-enable it to confirm the changes
        (s)he made.

        @param sender: not used, only here for signal compatibility
        '''
        if self.backend.is_enabled() and not self.backend.is_default():
            self.datastore.set_backend_enabled(self.backend.get_id(), False)

    def on_button_clicked(self, sender):
        '''Shows the filesystem explorer to choose a new file

        @param sender: not used, only here for signal compatibility
        '''
        self.chooser = Gtk.FileChooserDialog(
            title=None,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL,
                     Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_OK,
                     Gtk.ResponseType.OK))
        self.chooser.set_default_response(Gtk.ResponseType.OK)
        # set default file as the current self.path
        dirname, basename = os.path.split(self.textbox.get_text())
        self.chooser.set_current_name(basename)
        self.chosser.set_current_folder(dirname)

        # filter files
        afilter = Gtk.FileFilter()
        afilter.set_name("All files")
        afilter.add_pattern("*")
        self.chooser.add_filter(afilter)
        afilter = Gtk.FileFilter()
        afilter.set_name("XML files")
        afilter.add_mime_type("text/plain")
        afilter.add_pattern("*.xml")
        self.chooser.add_filter(afilter)
        response = self.chooser.run()
        if response == Gtk.ResponseType.OK:
            self.textbox.set_text(self.chooser.get_filename())
        self.chooser.destroy()
