import dbus
import dbus.glib
import dbus.service

from GTG.tools.dates import Date
from GTG.core.search import InvalidQuery
from GTG.core.search import parse_search_query

BUSNAME = "org.gnome.GTG"
BUSINTERFACE = "/org/gnome/GTG"


def dsanitize(data):
    """
    Clean up a dict so that it can be transmitted through D-Bus.
    D-Bus does not have concepts for empty or null arrays or values
    so these need to be converted into blank values D-Bus accepts.
    @return: Cleaned up dictionary
    """
    for k, v in list(data.items()):
        # Manually specify an arbitrary content type for empty Python arrays
        # because D-Bus can't handle the type conversion for empty arrays
        if not v and isinstance(v, list):
            data[k] = dbus.Array([], "s")
        # D-Bus has no concept of a null or empty value so we have to convert
        # None types to something else. I use an empty string because it has
        # the same behavior as None in a Python conditional expression
        elif v is None:
            data[k] = ""

    return data


def task_to_dict(task):
    """
    Translate a task object into a D-Bus dictionary
    """
    if not task:
        return None
    return dbus.Dictionary(dsanitize({
                                     "id": task.get_id(),
                                     "status": task.get_status(),
                                     "title": task.get_title(),
                                     "duedate": str(task.get_due_date()),
                                     "startdate": str(task.get_start_date()),
                                     "donedate": str(task.get_closed_date()),
                                     "tags": task.get_tags_name(),
                                     "text": task.get_text(),
                                     "subtask": task.get_children(),
                                     "parents": task.get_parents(),
                                     }), signature="sv")


class DBusTaskWrapper(dbus.service.Object):
    """
    D-Bus service object that exposes GTG's task store to third-party apps
    """

    def __init__(self, datastore, view_manager):
        # Attach the object to D-Bus
        self.bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(BUSNAME, bus=self.bus)
        super().__init__(bus_name, BUSINTERFACE)

        self.datastore    = datastore
        self.view_manager = view_manager

        # Start listening for signals from GTG core
        task_tree = self.datastore.get_tasks_tree().get_main_view()
        task_tree.register_cllbck('node-added',    lambda tid, _: self.TaskAdded   (tid))
        task_tree.register_cllbck('node-modified', lambda tid, _: self.TaskModified(tid))
        task_tree.register_cllbck('node-deleted',  lambda tid, _: self.TaskDeleted (tid))

    @dbus.service.method(BUSNAME)
    def GetTask(self, tid):
        """
        Retrieve a specific task by ID and return the data
        """
        toret = task_to_dict(self.datastore.get_task(tid))
        return toret

    @dbus.service.method(BUSNAME)
    def GetTasks(self):
        """
        Retrieve a list of task data dicts
        """
        return self.GetTasksFiltered(['all'])

    @dbus.service.method(BUSNAME, in_signature="as")
    def GetActiveTasks(self, tags):
        """
        Retrieve a list of task data dicts
        """
        return self.GetTasksFiltered(['active', 'workable'])

    @dbus.service.method(BUSNAME, in_signature="as")
    def GetTaskIdsFiltered(self, filters):
        """
        Filters the task list and provides list of remaining ids
        @param:  List of strings for filters to apply.  See the
         filters_bank documentation for a list of stock filters.
        @return: List of ids
        """
        tree = self.datastore.filter_tasks_tree().get_basetree()
        view = tree.get_viewtree()
        for filter in filters:
            if filter[0] == '!':
                view.apply_filter(filter[1:], parameters={'negate': 1})
            else:
                view.apply_filter(filter)
        return view.get_all_nodes()

    @dbus.service.method(BUSNAME, in_signature="as")
    def GetTasksFiltered(self, filters):
        """
        Gets a list of tasks for the given filters
        @param:  List of strings for filters to apply.  See the
         filters_bank documentation for a list of stock filters.
        @return: List of task dicts
        """
        tasks = self.GetTaskIdsFiltered(filters)
        if tasks:
            return [self.GetTask(id) for id in tasks]
        else:
            return dbus.Array([], "s")

    @dbus.service.method(BUSNAME, in_signature="s")
    def SearchTasks(self, query):
        """
        Searches the task list
        """
        tree = self.datastore.filter_tasks_tree().get_basetree()
        view = tree.get_viewtree()
        try:
            search = parse_search_query(query)
            view.apply_filter('search', parameters=search)
            tasks = view.get_all_nodes()
            if tasks:
                return [self.GetTask(id) for id in tasks]
        except InvalidQuery:
            pass
        return dbus.Array([], "s")

    @dbus.service.method(BUSNAME)
    def HasTask(self, tid):
        """
        Returns true if the task id is present in the task backend.
        Task could be either open or closed, but not deleted.
        """
        return self.datastore.has_task(tid)

    @dbus.service.method(BUSNAME)
    def DeleteTask(self, tid):
        """
        Delete the given task id from the repository.
        """
        self.datastore.delete_task(tid)

    @dbus.service.method(BUSNAME, in_signature="sssssassas")
    def NewTask(self, status, title, duedate, startdate, donedate, tags,
                text, subtasks):
        """
        Generate a new task object and return the task data as a dict
        @param status:     One of 'Active', 'Dismiss', or 'Done'
        @param title:      String name of the task
        @param duedate:    Date the task is due, such as "2010-05-01".
         also supports 'now', 'soon', 'someday'
        @param startdate:  Date the task will be started
        @param donedate:   Date the task was finished
        @param tags:       List of strings for tags to apply for this task
        @param text:       String description
        @param subtasks:   A list of task ids of tasks to add as children
        @return: A dictionary with the data of the newly created task
        """
        nt = self.datastore.new_task()
        self.datastore.add_tags_to_task(nt, tags)
        for sub in subtasks:
            nt.add_child(sub)
        nt.set_status(status, donedate=Date.parse(donedate))
        nt.set_title(title)
        nt.set_due_date(Date.parse(duedate))
        nt.set_start_date(Date.parse(startdate))
        nt.set_text(text)
        return task_to_dict(nt)

    @dbus.service.method(BUSNAME)
    def ModifyTask(self, tid, task_data):
        """
        Updates the task with ID tid using the provided information
        in the task_data structure.  Note that any fields left blank
        or undefined in task_data will clear the value in the task,
        so the best way to update a task is to first retrieve it via
        get_task(tid), modify entries as desired, and send it back
        via this function.
        """
        task = self.datastore.get_task(tid)
        task.set_status(task_data["status"],
                        donedate=Date.parse(task_data["donedate"]))
        task.set_title(task_data["title"])
        task.set_due_date(Date.parse(task_data["duedate"]))
        task.set_start_date(Date.parse(task_data["startdate"]))
        task.set_text(task_data["text"])

        for tag in task_data["tags"]:
            task.add_tag(tag)
        for sub in task_data["subtask"]:
            task.add_child(sub)
        return task_to_dict(task)

    @dbus.service.method(BUSNAME)
    def OpenTaskEditor(self, tid):
        """
        Launches the GUI task editor showing the task with ID tid.

        This routine returns as soon as the GUI has launched.
        """
        self.view_manager.open_task(tid)

    @dbus.service.method(BUSNAME, in_signature="ss")
    def OpenNewTask(self, title, description):
        """
        Launches the GUI task editor with a new task.  The task is not
        guaranteed to exist after the editor is closed, since the user
        could cancel the editing session.

        This routine returns as soon as the GUI has launched.
        """
        new_task = self.datastore.new_task()
        if title != "":
            new_task.set_title(title)
        if description != "":
            new_task.set_text(description)
        task_id = new_task.get_id()
        self.view_manager.open_task(task_id, thisisnew=True)

    @dbus.service.method(BUSNAME)
    def HideTaskBrowser(self):
        """
        Causes the main task browser to become invisible.  It is still
        running but there will be no visible indication of this.
        """
        self.view_manager.hide_browser()

    @dbus.service.method(BUSNAME)
    def IconifyTaskBrowser(self):
        """
        Minimizes the task browser
        """
        self.view_manager.iconify_browser()

    @dbus.service.method(BUSNAME)
    def ShowTaskBrowser(self):
        """
        Shows and unminimizes the task browser and brings it to the
        top of the z-order.
        """
        self.view_manager.show_browser()

    @dbus.service.method(BUSNAME)
    def IsTaskBrowserVisible(self):
        """
        Returns true if task browser is visible, either minimized or
        unminimized, with or without active focus.
        """
        return self.view_manager.is_browser_visible()

    @dbus.service.signal(BUSNAME)
    def TaskAdded(self, tid):
        """
        Signal: task added
        """
        pass

    @dbus.service.signal(BUSNAME)
    def TaskModified(self, tid):
        """
        Signal: task modified
        """
        pass

    @dbus.service.signal(BUSNAME)
    def TaskDeleted(self, tid):
        """
        Signal: task deleted
        """
        pass
