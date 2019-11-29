#!/usr/bin/env python3

# documentation: https://edge.launchpad.net/+apidoc/#bug_task

import os
import sys
from re import findall
from urllib.request import urlopen

from launchpadlib.credentials import Credentials
from launchpadlib.launchpad import Launchpad, EDGE_SERVICE_ROOT


def lp_login():
    cachedir = os.path.expanduser('~/.cache/launchpadlib/')
    if not os.path.isdir(cachedir):
        os.makedirs(cachedir)
    creddir = os.path.expanduser("~/.cache/lp_credentials")
    if not os.path.isdir(creddir):
        os.makedirs(creddir)
        os.chmod(creddir, 0o700)

    credpath = os.path.join(creddir, 'close_launchpad_bugs.txt')
    try:
        credfile = open(credpath, 'r')
        credentials = Credentials()
        credentials.load(credfile)
        credfile.close()
        launchpad = Launchpad(credentials, EDGE_SERVICE_ROOT, cachedir)
    except IOError:
        launchpad = Launchpad.get_token_and_login('close_launchpad_bugs',
                                                  EDGE_SERVICE_ROOT, cachedir)
        credfile = open(credpath, 'w')
        launchpad.credentials.save(credfile)
        credfile.close()

    return launchpad


def process_bug(bug):
    for task in bug.bug_tasks:
        if task.bug_target_name == 'gtg' and task.status == 'Fix Committed':
            task.status = 'Fix Released'
            task.lp_save()

if len(sys.argv) != 2:
    print('Usage: %s <release>' % sys.argv[0])
    sys.exit(1)

data = urlopen('https://launchpad.net/gtg/+milestone/%s' % sys.argv[1]).read()
bugs = findall('<a href="\S+/bugs/(\d+)">', data)
launchpad = lp_login()

if 'gtg' not in [e.name for e in launchpad.people[launchpad.me].super_teams]:
    print('You are not a GTG developer, exiting.')
    sys.exit(0)

for bugno in bugs:
    try:
        process_bug(launchpad.bugs[bugno])
        print("Bug #%s marked as Fix Released: "
              "https://bugs.edge.launchpad.net/gtg/+bug/%s" % (bugno, bugno))
    except:
        print("UNABLE TO PROCESS BUG #%s" % bugno)
