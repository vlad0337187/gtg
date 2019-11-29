#!/usr/bin/env python3

import os
import sys
import tarfile
from glob import glob

tarlist = list()
dirlist = list()
exclude_list = ('dist/', 'build/', '.bzr', 'test', 'pyc', 'scripts/', 'tmp/',
                'pot', 'HACKING', 'MANIFEST', 'Makefile', 'profile.py', '.swp')

for t in glob('dist/*.tar.gz'):
    tarball = tarfile.open(t, 'r')
    files = tarball.getnames()
    tarball.close()
    for f in [f for f in files if not f.endswith('/')]:
        # Skip the general directory
        if '/' not in f:
            continue
        tarlist.append(f.split('/', 1)[1])

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('/'):
            continue

        filename = os.path.join(root, f).split('/', 1)[1]

        exclude = False
        for ex in exclude_list:
            if filename.count(ex):
                exclude = True
                break
        if exclude:
            continue

        dirlist.append(filename)

missing = list(set(dirlist) - set(tarlist))
if len(missing) > 0:
    missing.sort()
    print('Missing files in tarball:')
    print('\n'.join("\t%s" % f for f in missing))
    sys.exit(1)
