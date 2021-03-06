from gi.repository import Gtk

from GTG.core.translations import translate


class PeriodUI(Gtk.Box):
    '''A widget to change the frequency of a backend synchronization
    '''

    def __init__(self, datastore, backend, width):
        '''
        Creates the Gtk.Adjustment and the related label. Loads the current
        period.

        @param backend: a backend object
        @param width: the width of the Gtk.Label object
        '''
        super().__init__()
        self.backend   = backend
        self.datastore = datastore
        self._populate_gtk(width)
        self._connect_signals()

    def _populate_gtk(self, width):
        '''Creates the gtk widgets

        @param width: the width of the Gtk.Label object
        '''
        period_label = Gtk.Label(label=translate("Check for new tasks every"))
        period_label.set_alignment(xalign=0, yalign=0.5)
        period_label.set_line_wrap(True)
        period_label.set_size_request(width=width, height=-1)
        self.pack_start(period_label, False, True, 0)
        align = Gtk.Alignment.new(0, 0.5, 1, 0)
        align.set_padding(0, 0, 10, 0)
        self.pack_start(align, False, True, 0)
        period = self.backend.get_parameters()['period']
        self.adjustment = Gtk.Adjustment(value=period,
                                         lower=1,
                                         upper=120,
                                         step_incr=1,
                                         page_incr=0,
                                         page_size=0)
        self.period_spin = Gtk.SpinButton(adjustment=self.adjustment,
                                          climb_rate=0.3,
                                          digits=0)
        self.minutes_label = Gtk.Label()
        self.update_minutes_label()
        self.minutes_label.set_alignment(xalign=0, yalign=0.5)
        self.pack_start(self.minutes_label, False, True, 0)
        align.add(self.period_spin)
        self.show_all()

    def _connect_signals(self):
        '''Connects the gtk signals'''
        self.period_spin.connect('changed', self.on_spin_changed)

    def commit_changes(self):
        '''Saves the changes to the backend parameter'''
        self.backend.set_parameter('period', int(self.adjustment.get_value()))

    def on_spin_changed(self, sender):
        ''' Signal callback, executed when the user changes the period.
        Disables the backend. The user will re-enable it to confirm the changes
        (s)he made.

        @param sender: not used, only here for signal compatibility
        '''
        self.update_minutes_label()
        if self.backend.is_enabled() and not self.backend.is_default():
            self.datastore.set_backend_enabled(self.backend.get_id(), False)

    def update_minutes_label(self):
        adjustment = int(self.adjustment.get_value())
        self.minutes_label.set_markup(translate(" minute",
                                               adjustment))
