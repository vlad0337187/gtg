from gi.repository import Gtk

from GTG.core.translations import translate
from GTG.gtk import ViewConfig


class DeletionUI(object):

    MAXIMUM_TIDS_TO_SHOW = 5

    def __init__(self, datastore):
        self.datastore     = datastore
        self.tids_todelete = []  # Tags which must be updated
        self.update_tags   = []
        # Load window tree
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ViewConfig.DELETE_UI_FILE)

        signals = {
            "on_delete_confirm": self.on_delete_confirm,
            "on_delete_cancel" : lambda x: x.hide,
        }
        self.builder.connect_signals(signals)

    def on_delete_confirm(self, widget):
        """if we pass a tid as a parameter, we delete directly
        otherwise, we will look which tid is selected"""
        for tid in self.tids_todelete:
            if self.datastore.has_task(tid):
                self.datastore.delete_task(tid, recursive=True)
        self.tids_todelete = []

        # Update tags
        for tagname in self.update_tags:
            tag = self.datastore.get_tag(tagname)
            tag.modified()
        self.update_tags = []

    def delete_tasks(self, tids=None):
        if tids:
            self.tids_todelete = tids
        # We must at least have something to delete !
        if len(self.tids_todelete) > 0:
            tasklist = []
            self.update_tags = []
            for tid in self.tids_todelete:

                def recursive_list_tasks(task_list, root):
                    """Populate a list of all the subtasks and
                       their children, recursively.

                       Also collect the list of affected tags
                       which should be refreshed"""
                    if root not in task_list:
                        task_list.append(root)
                        for tagname in root.get_tags_name():
                            if tagname not in self.update_tags:
                                self.update_tags.append(tagname)
                        for i in root.get_subtasks():
                            if i not in task_list:
                                recursive_list_tasks(task_list, i)

                task = self.datastore.get_task(tid)
                recursive_list_tasks(tasklist, task)

            # We fill the text and the buttons' labels according to the number
            # of tasks to delete
            label = self.builder.get_object("label1")
            label_text = label.get_text()
            cdlabel2 = self.builder.get_object("cd_question_label")
            cdlabel3 = self.builder.get_object("cd_cancel_label")
            cdlabel4 = self.builder.get_object("cd_delete_label")
            singular = len(tasklist)
            label_text = translate("Deleting a task cannot be undone, "
                                  "and will delete the following task: ",
                                  singular)
            cdlabel2.set_label(translate("Are you sure you want to delete this"
                                        " task?",
                                        singular))

            cdlabel3.set_label(translate("Keep selected task",
                                        singular))
            cdlabel4.set_label(translate("Permanently remove task",
                                        singular))
            label_text = label_text[0:label_text.find(":") + 1]

            # we don't want to end with just one task that doesn't fit the
            # screen and a line saying "And one more task", so we go a
            # little over our limit
            missing_titles_count = len(tasklist) - self.MAXIMUM_TIDS_TO_SHOW
            if missing_titles_count >= 2:
                tasks = tasklist[: self.MAXIMUM_TIDS_TO_SHOW]
                titles_suffix = translate("\nAnd %d more tasks" % missing_titles_count)
            else:
                tasks = tasklist
                titles_suffix = ""

            titles = "".join("\n - " + task.get_title() for task in tasks)
            label.set_text(label_text + titles + titles_suffix)
            delete_dialog = self.builder.get_object("confirm_delete")
            delete_dialog.resize(1, 1)
            cancel_button = self.builder.get_object("cancel")
            cancel_button.grab_focus()
            if delete_dialog.run() != 1:
                tasklist = []
            delete_dialog.hide()
            return tasklist
        else:
            return []
