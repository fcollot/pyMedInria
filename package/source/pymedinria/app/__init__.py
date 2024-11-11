# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys

from pymedinria.core import config, dev
from .application import create, instance


def run(*, gui=True, developer_mode=False):
    """Run the application.

    Use the 'gui' option to run in GUI or console-only mode.

    The developer mode activates various functons such as automatic reloading of
    modules (when modified) or the display of specific information on the
    console.

    """
    app = instance()

    if app is None:
        app = create(gui=gui)
    else:
        raise RuntimeError(f'Cannot run {config.application_name()} because another Qt application is already running.')

    if developer_mode:
        dev.set_developer_info(True)
        dev.set_auto_reload(True)

    return app.run()


def main():
    """Application entry point when running from the command line.

    Do not call this function from Python code. Use 'run()' instead.

    """
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()

    parser.add_argument('--gui', action=BooleanOptionalAction, default=True,
                        help="Run in GUI mode or not (default: --gui)"
    )
    parser.add_argument('--test', choices=['no-gui', 'gui', 'all'],
                        help="Run the unit tests"
    )
    parser.add_argument('--dev', action='store_true',
                        help="Enable developer utils when running the application"
    )
    args = parser.parse_args()

    if args.test:
        success = True

        if args.test == 'no-gui' or args.test == 'all':
            success &= dev.run_tests(gui=False)
        if args.test == 'gui' or args.test == 'all':
            success &= dev.run_tests(gui=True)

        exit_code = 0 if success else 1
    else:
        exit_code = run(gui=args.gui, developer_mode=args.dev)

    sys.exit(exit_code)
