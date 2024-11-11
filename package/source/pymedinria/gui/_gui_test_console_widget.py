# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import threading
import unittest

from pymedinria.core import config
from .console_widget import ConsoleWidget

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, QEventLoop, QObject, Slot
else:
    from PySide6.QtCore import QCoreApplication, QEventLoop, QObject, Slot


class TestConsoleWidget(unittest.TestCase):

    def setUp(self):
        self._console = ConsoleWidget()
        self._console.run()

    def tearDown(self):
        try:
            self._console.end_run()
            self._console = None
        except:
            pass

    def test_exiting_signals_run_ended(self):
        exit_event = threading.Event()

        class ExitChecker(QObject):

            @Slot()
            def on_exit(self):
                exit_event.set()

        checker = ExitChecker()
        self._console.run_ended.connect(checker.on_exit)
        self._console._handle_input("exit()", ">>>")
        self._process_events()
        self.assertTrue(exit_event.wait(2))

    def _process_events(self):
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
