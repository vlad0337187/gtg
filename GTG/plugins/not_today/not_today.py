from gi.repository import Gtk

from GTG.core.translations import translate
from GTG.tools.dates import Date


class NotTodayPlugin(object):

    def __init__(self):
        self.plugin_api = None
        self.tb_button  = None

    def activate(self, plugin_api):
        self.plugin_api = plugin_api
        self.datastore  = self.plugin_api.datastore
        self._init_gtk()
        self.plugin_api.set_active_selection_changed_callback(
            self.selection_changed)

    def deactivate(self, plugin_api):
        """ Removes the gtk widgets before quitting """
        self._gtk_deactivate()

    def mark_not_today(self, button):
        start_date = Date.parse("tomorrow")
        for tid in self.plugin_api.get_selected():
            task = self.datastore.get_task(tid)
            task.set_start_date(start_date)

    def selection_changed(self, selection):
        if selection.count_selected_rows() > 0:
            self.tb_button.set_sensitive(True)
        else:
            self.tb_button.set_sensitive(False)

    def _init_gtk(self):
        """ Initialize all the GTK widgets """

        self.tb_button = Gtk.ToolButton()
        self.tb_button.set_sensitive(False)
        self.tb_button.set_icon_name("document-revert")
        self.tb_button.set_is_important(True)
        self.tb_button.set_label(translate("Do it tomorrow"))
        self.tb_button.connect('clicked', self.mark_not_today)
        self.tb_button.show()
        self.plugin_api.add_toolbar_item(self.tb_button)

    def _gtk_deactivate(self):
        """ Remove Toolbar Button """
        if self.tb_button:
            self.plugin_api.remove_toolbar_item(self.tb_button)
            self.tb_button = False
