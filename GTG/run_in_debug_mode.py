#! /usr/bin/env python3

import sys


def add_system_site_packages_to_path():
	sys.path.append('/usr/lib/python3/dist-packages')


if __name__ == '__main__':
	add_system_site_packages_to_path()
	from GTG import gtg
