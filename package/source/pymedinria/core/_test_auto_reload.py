# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import pathlib
import threading
import time
import unittest

from . import dev


class TestAutoReload(unittest.TestCase):

    reload_frequency = 0.1

    def setUp(self):
        self._ensure_auto_reload_thread_closed()

    def tearDown(self):
        self._ensure_auto_reload_thread_closed()

    def _ensure_auto_reload_thread_closed(self):
        for thread in threading.enumerate():
            if thread.name == dev._AUTO_RELOAD_THREAD_NAME:
                dev.set_auto_reload(False)
                thread.join(self.reload_frequency * 2)
                if thread.is_alive():
                    raise RuntimeError("Unable to stop the auto reload thread.")
        return None

    def test_auto_relead_disabled_by_default(self):
        self.assertFalse(dev.auto_reload_enabled())

    def test_enabled_auto_reload(self):
        dev.set_auto_reload(True, frequency=self.reload_frequency)
        time.sleep(self.reload_frequency * 2)
        self.assertTrue(dev.auto_reload_enabled())

    def test_disable_auto_reload(self):
        dev.set_auto_reload(True, frequency=self.reload_frequency)
        dev.set_auto_reload(False)
        time.sleep(self.reload_frequency * 2)
        self.assertFalse(dev.auto_reload_enabled())

    def test_auto_reload_of_modified_module(self):
        from . import _dummy
        dev.set_auto_reload(True, frequency=self.reload_frequency)
        self.assertFalse(_dummy.foo)
        _dummy.foo = True
        try:
            pathlib.Path(_dummy.__file__).touch()
        except PermissionError:
            raise RuntimeError("Permission denied to modify dummy file. Cannot test auto reload.")
        time.sleep(self.reload_frequency * 2)
        self.assertFalse(_dummy.foo)
