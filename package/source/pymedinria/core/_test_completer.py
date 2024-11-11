# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
import unittest

from . import config
from .completer import Completer

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, QEventLoop, Slot
else:
    from PySide6.QtCore import QCoreApplication, QEventLoop, Slot


class TestCompleter(unittest.TestCase):

    def setUp(self):
        self._main_scope = vars(sys.modules['__main__'])
        self._previous_main_scope = self._main_scope.copy()
        self._completer = Completer()
        self._completer.successful_completion.connect(self._handle_successful_completion)
        self._completer.possible_completions.connect(self._handle_possible_completions)
        self._successful_completion = None
        self._possible_completions = None

    def tearDown(self):
        self._main_scope.clear()
        self._main_scope.update(self._previous_main_scope)

    def test_unique_code_completion(self):
        name = 'hopefully_unique_name_1'
        self._main_scope[name] = None
        self._completer.complete(name[:-4])
        self._process_events()
        self.assertEqual(self._successful_completion, name)

    def test_non_unique_code_completion(self):
        names = ('test_name_1', 'test_name_2', 'test_name_3')
        for name in names:
            self._main_scope[name] = None
        self._completer.complete('test_name_')
        self._process_events()
        for name in names:
            self.assertIn(name, self._possible_completions)

    def _process_events(self):
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

    @Slot(str)
    def _handle_successful_completion(self, completion):
        self._successful_completion = completion

    @Slot(list)
    def _handle_possible_completions(self, completions):
        self._possible_completions = completions
