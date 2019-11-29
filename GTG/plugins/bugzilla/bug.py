__all__ = ('BugFactory',)


class Bug(object):

    def __init__(self, bug):
        ''' Initialize Bug object using bug object retrieved via Bugzilla
            service XMLRPC
        '''
        self.bug = bug

    @property
    def summary(self):
        return self.bug['summary']

    @property
    def product(self):
        return self.bug['product']

    @property
    def description(self):
        return self.bug['summary']

    @property
    def component(self):
        return self.bug['component']


class GnomeBug(Bug):
    pass


class FreedesktopBug(Bug):
    pass


class GentooBug(Bug):
    pass


class MozillaBug(Bug):
    pass


class SambaBug(Bug):
    pass


class RedHatBug(Bug):
    pass


bugs = {
    'bugzilla.gnome.org': GnomeBug,
    'bugs.freedesktop.org': FreedesktopBug,
    'bugzilla.mozilla.org': MozillaBug,
    'bugzilla.samba.org': SambaBug,
    'bugs.gentoo.org': GentooBug,
    'bugzilla.redhat.com': RedHatBug,
}


class BugFactory(object):
    @staticmethod
    def create(serviceDomain, bug):
        return bugs[serviceDomain](bug)
