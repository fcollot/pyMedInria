# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
import threading
import unittest

from .console import Console


class TestConsole(unittest.TestCase):

    def setUp(self):
        self._main_scope = vars(sys.modules['__main__'])
        self._previous_main_scope = self._main_scope.copy()
        
        if hasattr(self._main_scope, 'foo'):
            del self._main_scope['foo']
        if hasattr(self._main_scope, 'bar'):
            del self._main_scope['bar']

        self._console = Console()
        self._console.welcome_text = ''
        self._console.run(globals={'foo': 1}, command_line_thread=threading.current_thread())

    def tearDown(self):
        self._console.end_run()
        self._console = None
        self._main_scope.clear()
        self._main_scope.update(self._previous_main_scope)

    def test_globals_enter_main_scope(self):
        self.assertIn('foo', self._main_scope)
        self.assertEqual(self._main_scope['foo'], 1)

    def test_assignments_enter_main_scope(self):
        self._console.push("bar = 1")
        self.assertIn('bar', self._main_scope)
        self.assertEqual(self._main_scope['bar'], 1)

    def test_multiline_statements(self):
        self._console.push("def bar(x):")
        self._console.push("    global foo")
        self._console.push("    foo = x")
        self._console.push("")
        self._main_scope['bar'](2)
        self.assertEqual(self._main_scope['foo'], 2)

    def test_history_works_as_expected(self):
        s1 = "foo = 1"
        s2 = "foo = 2"
        s3 = "foo = 3"
        console = self._console

        console.push(s1)
        console.push(s2)
        console.push(s3)
        self.assertEqual(console.current_history_entry(), "")
        console.move_up_history()
        self.assertEqual(console.current_history_entry(), s3)
        console.move_up_history()
        self.assertEqual(console.current_history_entry(), s2)
        console.move_up_history()
        self.assertEqual(console.current_history_entry(), s1)
        console.move_up_history()
        self.assertEqual(console.current_history_entry(), s1)
        console.move_down_history()
        self.assertEqual(console.current_history_entry(), s2)
        console.move_down_history()
        self.assertEqual(console.current_history_entry(), s3)
        console.move_down_history()
        self.assertEqual(console.current_history_entry(), "")
        console.move_down_history()
        self.assertEqual(console.current_history_entry(), "")
