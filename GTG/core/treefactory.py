from datetime import datetime

from GTG.core.search       import search_filter
from GTG.core              import tag
from GTG.core.task         import Task
from GTG.core.translations import translate
from GTG.tools.dates       import Date
from liblarch              import Tree


class TreeFactory(object):
    """ Factory for creating liblarch suitable trees.
    Main methods:
        get_tasks_tree()
        get_tags_tree() """

    def __init__(self):
        # Keep the tree in memory jus in case we have to use it for filters.
        self.tasktree = None
        self.tagtree  = None

    def get_tasks_tree(self):
        """ This create a liblarch tree suitable for tasks,
        including default filters
        For tags, filter are dynamically created at Tag insertion. """

        def attach_filters_to_tasktree():
            for filter_name, filter_value in filters.items():
                if len(filter_value) > 1:
                    param = filter_value[1]
                else:
                    param = None
                tasktree.add_filter(filter_name, filter_value[0], param)

        tasktree = Tree()
        filters  = {
            'workview'       : [self.workview],
            'active'         : [self.active],
            'closed'         : [self.closed, {'flat': True}],
            'notag'          : [self.notag],
            'workable'       : [self.is_workable],
            'started'        : [self.is_started],
            'workdue'        : [self.workdue],
            'workstarted'    : [self.workstarted],
            'worktostart'    : [self.worktostart],
            'worklate'       : [self.worklate],
            'no_disabled_tag': [self.no_disabled_tag],
        }
        attach_filters_to_tasktree()
        self.tasktree = tasktree
        return tasktree

    def get_tags_tree(self, datastore):
        """ This create a liblarch tree suitable for tags,
        including the all_tags_tag and notag_tag. """

        def add_tag__all(order=0):
            alltag = tag.Tag(tag.TAG_ALLTASKS, datastore=datastore)
            alltag.set_attribute("special", "all")
            alltag.set_attribute("label",   f"<span weight='bold'>{translate('All tasks')}</span>")
            alltag.set_attribute("icon",    "gtg-tags-all")
            alltag.set_attribute("order",   order)
            tagtree.add_node(alltag)
            p = {}
            self.tasktree.add_filter(tag.TAG_ALLTASKS, self.alltag, parameters=p)

        def add_tag__notag(order=0):
            notag_tag = tag.Tag(tag.TAG_NOTAG, datastore=datastore)
            notag_tag.set_attribute("special", "notag")
            notag_tag.set_attribute("label",   f"<span weight='bold'>{translate('Tasks with no tags')}</span>")
            notag_tag.set_attribute("icon",    "gtg-tags-none")
            notag_tag.set_attribute("order",   order)
            tagtree.add_node(notag_tag)
            p = {}
            self.tasktree.add_filter(tag.TAG_NOTAG, self.notag, parameters=p)

        def add_tag__workview(order=0):
            tag_workview = tag.Tag(tag.TAG_WORKVIEW, datastore=datastore)
            tag_workview.set_attribute("special", "workview")
            tag_workview.set_attribute("label",   f"<span weight='bold'>{translate('Workview')}</span>")
            tag_workview.set_attribute("icon",    "gtg-tags-all")
            tag_workview.set_attribute("order",   order)
            tagtree.add_node(tag_workview)
            p = {}
            self.tasktree.add_filter(tag.TAG_WORKVIEW, self.workview, parameters=p)

        def add_tag__closed(order=0):
            tag_closed = tag.Tag(tag.TAG_CLOSED, datastore=datastore)
            tag_closed.set_attribute("special", "closed")
            tag_closed.set_attribute("label",   f"<span weight='bold'>{translate('Closed tasks')}</span>")
            tag_closed.set_attribute("icon",    "gtg-tags-none")
            tag_closed.set_attribute("order",   order)
            tagtree.add_node(tag_closed)
            p = {}
            self.tasktree.add_filter(tag.TAG_CLOSED, self.closed, parameters=p)

        def add_tag__search(order=0):
            search_tag = tag.Tag(tag.TAG_SEARCH, datastore=datastore)
            search_tag.set_attribute("special", "search")
            search_tag.set_attribute("label",   f"<span weight='bold'>{translate('Search')}</span>")
            search_tag.set_attribute("icon",    "search")
            search_tag.set_attribute("order",   order)
            tagtree.add_node(search_tag)
            p = {}
            self.tasktree.add_filter(tag.TAG_SEARCH, search_filter, parameters=p)

        def add_tag__separator(order=0):
            sep_tag = tag.Tag(tag.TAG_SEPARATOR, datastore=datastore)
            sep_tag.set_attribute("special", "sep")
            sep_tag.set_attribute("order",    order)
            tagtree.add_node(sep_tag)

        def add_filters():
            tagtree.add_filter('activetag', self.actively_used_tag)
            tagtree.add_filter('usedtag',   self.used_tag)

        tagtree = Tree()
        add_tag__all      (order=0)
        add_tag__workview (order=1)
        add_tag__separator(order=2)
        add_tag__closed   (order=3)
        add_tag__notag    (order=4)
        add_tag__search   (order=5)
        add_filters()

        activeview = tagtree.get_viewtree(name='activetags', refresh=False)
        activeview.apply_filter('activetag')

        # This view doesn't seem to be used. So it's not useful to build it now
        #usedview = tagtree.get_viewtree(name='usedtags',refresh=False)
        #usedview.apply_filter('usedtag')

        self.tagtree        = tagtree
        self.tagtree_loaded = True
        return tagtree

    # Tag Filters ##########################################

    # filter to display only tags with active tasks
    def actively_used_tag(self, node, parameters=None):
        toreturn = node.is_actively_used()
        return toreturn

    def used_tag(self, node, parameters=None):
        return node.is_used()

    # Task Filters #########################################

    def tag_filter(self, node, parameters):
        """ Is used to filters tag. Is it built dynamically each times
        a tag is added to the tagstore. """
        tag = parameters['tag']
        return node.has_tags([tag])

    def alltag(self, task, parameters=None):
        return True

    def notag(self, task, parameters=None):
        """ Filter of tasks without tags """
        return task.has_tags(notag_only=True)

    def is_leaf(self, task, parameters=None):
        """ Filter of tasks which have no children """
        return not task.has_child()

    def is_workable(self, task, parameters=None):
        """ Filter of tasks that can be worked """
        tree = task.get_tree()
        for child_id in task.get_children():
            if not tree.has_node(child_id):
                continue

            child = tree.get_node(child_id)
            if child.get_status() == Task.STA_ACTIVE:
                return False

        return True

    def is_started(self, task, parameters=None):
        """ Filter for tasks that are already started """
        days_left = task.get_start_date().days_left()

        if days_left is None:
            # without startdate
            return True
        elif days_left == 0:
            # Don't count today's tasks started until morning
            return datetime.now().hour > 4
        else:
            return days_left < 0

    def workview(self, task, parameters=None):
        wv = (self.active(task) and
              self.is_started(task) and
              self.is_workable(task) and
              self.no_disabled_tag(task) and
              task.get_due_date() != Date.someday())
        return wv

    def workdue(self, task):
        ''' Filter for tasks due within the next day '''
        wv = (self.workview(task) and
              task.get_due_date() and
              task.get_days_left() < 2)
        return wv

    def worklate(self, task):
        ''' Filter for tasks due within the next day '''
        wv = (self.workview(task) and
              task.get_due_date() and
              task.get_days_late() > 0)
        return wv

    def workstarted(self, task):
        ''' Filter for workable tasks with a start date specified '''
        wv = self.workview(task) and \
            task.start_date
        return wv

    def worktostart(self, task):
        ''' Filter for workable tasks without a start date specified '''
        wv = self.workview(task) and \
            not task.start_date
        return wv

    def active(self, task, parameters=None):
        """ Filter of tasks which are active """
        return task.get_status() == Task.STA_ACTIVE

    def closed(self, task, parameters=None):
        """ Filter of tasks which are closed """
        ret = task.get_status() in [Task.STA_DISMISSED, Task.STA_DONE]
        return ret

    def no_disabled_tag(self, task, parameters=None):
        """Filter of task that don't have any disabled/nonworkview tag"""
        toreturn = True
        for t in task.get_tags():
            if t.get_attribute("nonworkview") == "True":
                toreturn = False
        return toreturn
