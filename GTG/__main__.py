import argparse
import sys

from . import debug
from . import init


def main():
    cli_args   = parse_cli_args()
    mode_cli   = cli_args.cli
    mode_gui   = not mode_cli
    mode_debug = cli_args.debug

    if mode_debug: debug.before_init(cli_args)
    init.main()
    if mode_debug: debug.after_init()

    if mode_gui:
        run_gui()
    elif mode_cli:
        run_cli()


def run_gui():
    from . import gtg

    try:
        gtg.main()
    except KeyboardInterrupt:
        sys.exit(1)


def run_cli():
    from . import gtcli
    gtcli.main()


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Getting Things app arguments')
    parser.add_argument(
        '--cli',
        help     = 'specify it if you need to run app in cli mode',
        required = False,
        default  = False,
        action   = 'store_true',
    )
    parser.add_argument(
        '--debug',
        help     = 'specify it if you need to run app in debug mode',
        required = False,
        default  = False,
        action   = 'store_true',
    )
    parser.add_argument(
        '--dataset',
        help     = 'dataset for app to use, can be used only in debug mode',
        required = False,
        default  = None,
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
