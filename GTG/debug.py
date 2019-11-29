#! /usr/bin/env python3

"""
Functions to use with debug mode.
"""

import sys

def add_system_site_packages_to_path():
    sys.path.append('/usr/lib/python3/dist-packages')

add_system_site_packages_to_path()

import importlib
import os
import os.path as op

import GTG.core.dirs


def before_init(cli_args):
    """
    Should be runned before `init.main()`.
    """
    ensure_not_runned_as_root()
    copy_dataset_if_specified_to_temp_dir(cli_args)
    set_env_vars_for_xdg(cli_args)


def after_init():
    """
    Should be runned after `init.main()`.
    """
    pass


def ensure_not_runned_as_root():
    uid     = os.getuid()
    is_root = uid == 0

    if is_root:
        raise RuntimeError("app shouldn't be launched by root user")


def copy_dataset_if_specified_to_temp_dir(cli_args):
    """
    Dataset - app state data (including cache, config).
    See `./data/test-data/standart` for example.
    """
    is_dataset_specified = cli_args.dataset
    if not is_dataset_specified:
        return

    shutil.copytree(src=cli_args.dataset, dst=GTG.core.dirs.TEMP_DIR_LOCAL)


def set_env_vars_for_xdg(cli_args):
    dataset_name = op.basename(cli_args.dataset) if cli_args.dataset else 'default'
    os.environ['XDG_DATA_HOME']   = op.join(GTG.core.dirs.TEMP_DIR_LOCAL, dataset_name, 'xdg', 'data')
    os.environ['XDG_CACHE_HOME']  = op.join(GTG.core.dirs.TEMP_DIR_LOCAL, dataset_name, 'xdg', 'cache')
    os.environ['XDG_CONFIG_HOME'] = op.join(GTG.core.dirs.TEMP_DIR_LOCAL, dataset_name, 'xdg', 'config')
