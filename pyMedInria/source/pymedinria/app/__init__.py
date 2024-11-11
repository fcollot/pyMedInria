# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys

from pymedinria.core import config, dev
from . import application as app


def run(*, gui=True, developer_mode=False, splash=False, dry=False):
    """Run the application.

    Use the 'gui' option to run in GUI or console-only mode.

    The developer mode activates various functons such as automatic reloading of
    modules (when modified) or the display of specific information on the
    console.

    """
    if app.instance() is None:
        app.create(gui=gui)

    if developer_mode:
        dev.set_developer_info(True)
        dev.set_auto_reload(True)

    return app.run(splash=splash, dry=dry)


def parse_argv_and_run():
    from argparse import ArgumentParser, BooleanOptionalAction

    sys.argv[0] = config.application_name()
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
    parser.add_argument('--splash', action=BooleanOptionalAction, default=False,
                        help=""
    )
    parser.add_argument('--dry', action='store_true',
                        help=""
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
        exit_code = run(gui=args.gui, developer_mode=args.dev, splash=args.splash, dry=args.dry)

    return exit_code


run_console
