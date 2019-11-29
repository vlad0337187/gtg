"""
TaskClipboard allows to cut/copy the content of a TaskView accross multiples
taskeditors, preserving subtasks
"""


class TaskClipboard(object):

    def __init__(self, req):
        self.description = None
        self.content = []
        self.req = req

    """"take two Gtk.TextIter as parameter and copy the
    """

    def copy(self, start, stop, bullet=None):
        self.clear()
        # Now, we take care of the normal, cross application clipboard
        text = start.get_text(stop)
        if text and bullet:
            # we replace the arrow by the original "-"
            newtext = text.replace(bullet, "-")
            self.description = newtext
        elif text:
            self.description = text

        end_line = start.copy()
        # we take line after line in the selection
        nextline = True
        while end_line.get_line() <= stop.get_line() and nextline:
            nextline = end_line.forward_line()
            end_line.backward_char()
            # we want to detect subtasks in the selection
            tags = end_line.get_tags() + end_line.get_toggled_tags(False)
            is_subtask = False
            for ta in tags:
                if hasattr(ta, 'is_subtask'):
                    is_subtask = True
                    tid = ta.child
                    tas = self.req.get_task(tid)
                    tas.set_to_keep()
                    tas.sync()
                    self.content.append(['subtask', tid])
            if not is_subtask:
                if end_line.get_line() < stop.get_line():
                    self.content.append(['text', "%s\n" %
                                         start.get_text(end_line)])
                else:
                    self.content.append(['text', start.get_text(stop)])
            end_line.forward_char()
            start.forward_line()

    def paste_text(self):
        return self.description

    def paste(self):
        return self.content

    def clear(self):
        self.descriptiion = None
        self.content = []
