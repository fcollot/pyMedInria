# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
from threading import Lock, Thread
from traceback import print_exception

import pymedinria
from pymedinria.core import config, console

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, Qt, QTimer
else:
    from PySide6.QtCore import QCoreApplication, Qt, QTimer


_console = None


def instance():
    return QCoreApplication.instance()


def create(*args, gui=True):
    """Create the application.

    Set 'gui' to False for a non-GUI application.

    """
    base_class = _select_base_class(gui)

    class Application(base_class):

        def __init__(self):
            super().__init__(sys.argv)
            self.setApplicationName("pyMedInria")

        def exec(self):
            return self.exec_()

        def exec_(self):
            self.aboutToQuit.connect(self.deleteLater)
            return super().exec_()

    return Application()


def _select_base_class(gui):
    if gui:
        if config.pyside_version() == 2:
            from PySide2.QtWidgets import QApplication
        else:
            from PySide6.QtWidgets import QApplication

        return QApplication
    else:
        return QCoreApplication


def run(splash=False, dry=False):
    app = instance()

    if splash:
        splash_screen = create_splash()

    run_console()

    if splash:
        splash_screen.finish(_console)

    if dry:
        timer = _create_dry_run_timer(app)

    return _run_qt(app)


def run_console():
    """Run the console.
    
    Creates and runs a ConsoleWidget if the GUI is enabled, or a simple
    terminal console if not.
    
    """
    if config.gui_enabled():
        from pymedinria.gui.console_widget import ConsoleWidget as Console
    else:
        from pymedinria.core.console import Console

    global _console
    console_globals = {'pymedinria' : pymedinria, 'med' : pymedinria}
    _console = Console()
    _console.run_ended.connect(_exit_from_console, Qt.ConnectionType.DirectConnection)
    _console.run(globals=console_globals)
    
    if config.gui_enabled():
        _console.show()


def _exit_from_console(exception):
    global _console
    _console = None
    if exception:
        print_exception(exception)
    error_code = 0 if not exception else 1
    instance().exit(error_code)


def create_splash():
    if config.pyside_version() == 2:
        from PySide2.QtGui import QPixmap
        from PySide2.QtWidgets import QSplashScreen
    else:
        from PySide6.QtGui import QPixmap
        from PySide6.QtWidgets import QSplashScreen

    pixmap = QPixmap(400, 200)
    pixmap.fill(Qt.white)
    splash = QSplashScreen(pixmap)
    splash.show()
    splash.showMessage("Loading pyMedInria...\n", Qt.AlignCenter)
    instance().processEvents()
    return splash


def _create_dry_run_timer(app):
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(app.quit)
    timer.start()
    return timer


def _run_qt(app):
    if config.pyside_version() == 2:
        return app.exec_()
    else:
        return app.exec()
