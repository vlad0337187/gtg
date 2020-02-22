from gi.repository import Gtk

from GTG.core.translations import translate


class PasswordUI(Gtk.Box):
    '''Widget displaying a gtk.Label and a textbox to input a password'''

    def __init__(self, datastore, backend, width):
        '''Creates the gtk widgets and loads the current password in the text
        field

        @param backend: a backend object
        @param width: the width of the Gtk.Label object
        '''
        super().__init__()
        self.backend   = backend
        self.datastore = datastore
        self._populate_gtk(width)
        self._load_password()
        self._connect_signals()

    def _populate_gtk(self, width):
        '''Creates the text box and the related label

        @param width: the width of the Gtk.Label object
        '''
        password_label = Gtk.Label(label=translate("Password:"))
        password_label.set_alignment(xalign=0, yalign=0)
        password_label.set_size_request(width=width, height=-1)
        self.pack_start(password_label, False, True, 0)
        align = Gtk.Alignment.new(0, 0.5, 1, 0)
        align.set_padding(0, 0, 10, 0)
        self.pack_start(align, True, True, 0)
        self.password_textbox = Gtk.Entry()
        align.add(self.password_textbox)

    def _load_password(self):
        '''Loads the password from the backend'''
        password = self.backend.get_parameters()['password']
        self.password_textbox.set_invisible_char('*')
        self.password_textbox.set_visibility(False)
        self.password_textbox.set_text(password)

    def _connect_signals(self):
        '''Connects the gtk signals'''
        self.password_textbox.connect('changed', self.on_password_modified)

    def commit_changes(self):
        '''Saves the changes to the backend parameter ('password')'''
        password = self.password_textbox.get_text()
        self.backend.set_parameter('password', password)

    def on_password_modified(self, sender):
        ''' Signal callback, executed when the user edits the password.
        Disables the backend. The user will re-enable it to confirm the changes
        (s)he made.

        @param sender: not used, only here for signal compatibility
        '''
        if self.backend.is_enabled() and not self.backend.is_default():
            self.datastore.set_backend_enabled(self.backend.get_id(), False)
