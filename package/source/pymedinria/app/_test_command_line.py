# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib
import sys
import unittest

from pymedinria import app


class TestCommandLine(unittest.TestCase):
    """Test that command line options are correctly handled.

    These tests replace the entry functions that would normally be called with
    special functions that allow checking if the expected function was called
    with the expected options (if applicable).

    """

    @classmethod
    def tearDownClass(cls):
        importlib.reload(app)
        importlib.reload(app.dev)

    def setUp(self):
        self._previous_argv = sys.argv
        self._args = {}
        self._kwargs = {}
        app.run = self._function_call_tracker('run', 0)
        app.dev.run_tests = self._function_call_tracker('run_tests', True)
        self._exit = sys.exit
        sys.exit = lambda _ : None

    def tearDown(self):
        sys.exit = self._exit

    def _function_call_tracker(self, name, return_value):
        def _track_function_call(*args, **kwargs):
            if name in self._args:
                self._args[name].append(args)
            else:
                self._args[name] = [args]
            if name in self._kwargs:
                self._kwargs[name].append(kwargs)
            else:
                self._kwargs[name] = [kwargs]
            return return_value

        return _track_function_call

    def tearDown(self):
        sys.argv = self._previous_argv

    def test_non_gui_tests_option(self):
        sys.argv = ['', '--test', 'no-gui']
        app.main()
        self.assertIn('run_tests', self._kwargs)
        kwargs = self._kwargs['run_tests']
        self.assertEqual(len(kwargs), 1)
        self.assertIn('gui', kwargs[0])
        self.assertFalse(kwargs[0]['gui'])

    def test_gui_tests_option(self):
        sys.argv = ['', '--test', 'gui']
        app.main()
        self.assertIn('run_tests', self._kwargs)
        kwargs = self._kwargs['run_tests']
        self.assertEqual(len(kwargs), 1)
        self.assertIn('gui', kwargs[0])
        self.assertTrue(kwargs[0]['gui'])

    def test_all_tests_option(self):
        sys.argv = ['', '--test', 'all']
        app.main()
        self.assertIn('run_tests', self._kwargs)
        kwargs = self._kwargs['run_tests']
        self.assertEqual(len(kwargs), 2)
        self.assertIn('gui', kwargs[0])
        self.assertIn('gui', kwargs[1])
        self.assertNotEqual(kwargs[0]['gui'], kwargs[1]['gui'])

    def test_gui_option(self):
        sys.argv = ['', '--gui']
        app.main()
        self.assertIn('run', self._kwargs)
        kwargs = self._kwargs['run']
        self.assertIn('gui', kwargs[0])
        self.assertTrue(kwargs[0]['gui'])

    def test_no_gui_option(self):
        sys.argv = ['', '--no-gui']
        app.main()
        self.assertIn('run', self._kwargs)
        kwargs = self._kwargs['run']
        self.assertIn('gui', kwargs[0])
        self.assertFalse(kwargs[0]['gui'])

    def test_gui_option_is_default(self):
        sys.argv = ['']
        app.main()
        self.assertIn('run', self._kwargs)
        kwargs = self._kwargs['run']
        self.assertIn('gui', kwargs[0])
        self.assertTrue(kwargs[0]['gui'])

    def test_dev_option(self):
        sys.argv = ['', '--dev']
        app.main()
        self.assertIn('run', self._kwargs)
        kwargs = self._kwargs['run']
        self.assertIn('developer_mode', kwargs[0])
        self.assertTrue(kwargs[0]['developer_mode'])

    def test_dev_option_is_off_by_default(self):
        sys.argv = ['']
        app.main()
        self.assertIn('run', self._kwargs)
        kwargs = self._kwargs['run']
        self.assertIn('developer_mode', kwargs[0])
        self.assertFalse(kwargs[0]['developer_mode'])
