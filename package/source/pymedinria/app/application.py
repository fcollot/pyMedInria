# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from threading import Lock, Thread
from traceback import print_exception

import pymedinria
from pymedinria.core import config, console

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication
else:
    from PySide6.QtCore import QCoreApplication


def instance():
    return QCoreApplication.instance()


def create(*args, gui=True, **kwargs):
    """Create the application.

    Set 'gui' to False for a non-GUI application.
    The remaining arguments are forwarded to the class constructor.

    """
    base_class = _select_base_class(gui)
    application_class = _create_application_class(base_class)
    return application_class(*args, **kwargs)


def _select_base_class(gui):
    if gui:
        if config.pyside_version() == 2:
            from PySide2.QtWidgets import QApplication
        else:
            from PySide6.QtWidgets import QApplication

        return QApplication
    else:
        return QCoreApplication


def _create_application_class(base_class):

    class Application(base_class):

        _lock = Lock()
        _is_running = False

        def __init__(self, argv=None):
            super().__init__(argv=argv)
            self.setApplicationName("pyMedInria")

        def gui_enabled(self):
            """Check if GUI functionality is enabled.

            """
            return type(self).__base__ is not QCoreApplication

        def run(self):
            exit_value = 1

            with self._lock:
                if self._is_running:
                    raise RuntimeError(f'{config.application_name()}is already running.')
                self._is_running = True

            self._run_console()

            exit_value = self._run_qt()

            with self._lock:
                self._is_running = False

            return exit_value

        def _run_qt(self):
            self.aboutToQuit.connect(self.deleteLater)

            if config.pyside_version() == 2:
                return self._exec()
            else:
                return self.exec()

        def _run_console(self):
            """Run the console.
            
            Creates and runs a ConsoleWidget if the GUI is enabled, or a simple
            terminal console if not.

            """
            if self.gui_enabled():
                from pymedinria.gui.console_widget import ConsoleWidget as Console
            else:
                from pymedinria.core.console import Console

            console_globals = {'pymedinria' : pymedinria, 'med' : pymedinria}
            console = Console()
            console.run_ended.connect(self._exit_from_console)
            console.run(globals=console_globals)

            if self.gui_enabled():
                console.show()

        def _exit_from_console(self, exception):
            if exception:
                print_exception(exception)
            error_code = 0 if not exception else 1
            self.exit(error_code)

        def console_widget(self):
            return self._console_widget

    return Application
