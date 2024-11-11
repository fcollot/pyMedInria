# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import builtins
import importlib
import inspect
import os
from pathlib import Path
import sys
from threading import Thread, RLock
import time
import traceback
import unittest

import pymedinria
from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, QObject, QThread, QTimer, Slot
else:
    from PySide6.QtCore import QCoreApplication, QObject, QThread, QTimer, Slot


_AUTO_RELOAD_THREAD_NAME = "auto reload"


_developer_info_enabled = False
_auto_reload_enabled = False
_import_times = {}
_lock = RLock()


def set_developer_info(enable):
    """Enable printing of development specific information when certain
    functions are called.

    """
    with _lock:
        global _developer_info_enabled
        _developer_info_enabled = enable


def developer_info_enabled():
    with _lock:
        return _developer_info_enabled


def print_developer_info(object):
    if developer_info_enabled():
        print(object)


def set_auto_reload(enable, *, frequency=2):
    """Activate or deactivate the automatic reloading of modules.

    When auto reload is activated the __import__ function is wrapped with code
    that stores the import time of the application's modules (for modules that
    have already been imported the import time is set to the current time).

    In addition a thread is created that regularily checks the file timestamps
    of the imported modules, and those that have changed since the last import
    are reloaded. The 'frequency' argument determines the frequence (in seconds)
    of these checks.

    This function is intended for development purposes and may cause unexpected
    issues.

    """
    with _lock:
        global _auto_reload_enabled

        if enable:
            _auto_reload_enabled = True

            global _builtins_import
            if '_builtins_import' not in globals():
                _builtins_import = builtins.__import__
            builtins.__import__ = _import_and_track_time

            global _import_times
            current_time = time.time()
            for name, module in sys.modules.items():
                if name.startswith('pymedinria') and name not in _import_times:
                    _import_times[name] = current_time

            _run_auto_reload_loop(frequency=frequency)
        else:
            _auto_reload_enabled = False

            if '_builtins_import' in globals():
                builtins.__import__ = _builtins_import


def auto_reload_enabled():
    with _lock:
        return _auto_reload_enabled


def _import_and_track_time(name, globals=None, locals=None, fromlist=(), level=0):
    """Wrapper over the builtin __import__ that tracks import times.

    """
    module = _builtins_import(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

    if level > 0:
        # Get package name for relative imports.
        name_parts = globals['__package__'].split('.')
        if level > 1:
            name_parts = name_parts[:1 - level]
    else:
        name_parts = []

    name_parts += name.split('.')

    if name_parts[0] == 'pymedinria':
        global _import_times
        current_time = time.time()

        # Store time for module and all its parents.
        for i in range(len(name_parts)):
            _import_times['.'.join(name_parts[:i + 1])] = current_time

        # Check if 'fromList' imports modules, and store their times.
        if fromlist:
            full_name = '.'.join(name_parts)
            for item in fromlist:
                if inspect.ismodule(getattr(module, item)):
                    _import_times[f'{full_name}.{item}'] = current_time
    return module


def _run_auto_reload_loop(*, frequency):
    """
    Runs a dedicated thread that handles auto reload (see 'set_auto_reload' for
    more details).

    """
    def auto_reload_loop():
        print_developer_info("Auto reload loop started.")
        while True:
            with _lock:
                if _auto_reload_enabled:
                    for name in _import_times:
                        module = sys.modules[name]
                        if os.path.getmtime(module.__file__) > _import_times[name]:
                            print_developer_info(f'Reloading {name}')
                            module = importlib.reload(sys.modules[name])
                            _import_times[name] = time.time()

                    time.sleep(frequency)
                else:
                    break
        print_developer_info("Auto reload loop stopped.")

    thread = Thread(target=auto_reload_loop, name=_AUTO_RELOAD_THREAD_NAME, daemon=True)
    thread.start() 


def run_tests(*, gui=True):
    """Run the unit tests.

    The 'gui' option determines whether the GUI or non-GUI tests are run. This
    function may be called from the main thread of a running application or
    not; in the latter case a temporary QCoreApplication (or QApplication for
    GUI tests) will be created.

    """
    preexisting_app = QCoreApplication.instance()

    if gui:
        if preexisting_app:
            if QThread.currentThread() is not preexisting_app.thread():
                raise RuntimeError("The GUI tests must be run from the main thread.")
        else:
            return _create_gui_application_and_run_tests()

    if not preexisting_app:
        QCoreApplication()

    try:
        modules = find_test_modules(gui=gui)
        if modules:
            results = run_module_tests(modules)
            success = all([result.wasSuccessful() for result in results])
        else:
            raise RuntimeError("No tests found.")
    finally:
        if not preexisting_app:
            QCoreApplication.instance().shutdown()

    return success


def _create_gui_application_and_run_tests():

    if config.pyside_version() == 2:
        from PySide2.QtWidgets import QApplication
    else:
        from PySide6.QtWidgets import QApplication

    class GUITestRunner(QObject):
        @Slot()
        def run(self):
            try:
                success = run_tests(gui=True)
                exit_code = 0 if success else 1
            except:
                traceback.print_exc()
                exit_code = 1
            finally:
                QApplication.instance().exit(exit_code)

    app = QApplication()
    runner = GUITestRunner()
    timer = QTimer()
    thread = QThread()

    timer.setSingleShot(True)
    timer.timeout.connect(runner.run)
    timer.timeout.connect(thread.terminate)

    thread.started.connect(timer.start)
    thread.start()

    if config.pyside_version() == 2:
        return app._exec() == 0
    else:
        return app.exec() == 0


def run_module_tests(module_names):
    """Run the unit tests from a list of modules.

    If any of the modules contain GUI tests (which require a running
    QApplication), it is up to the caller to ensure the application was created
    beforehand and that this function is called from the main thread.

    """
    loader = unittest.defaultTestLoader
    runner = unittest.TextTestRunner(verbosity=2)
    results = []

    for name in module_names:
        module = importlib.import_module(name)
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromModule(module))
        results.append(runner.run(suite))

    return results


def find_test_modules(gui):
    """Find the unit test modules using prefixes.

    The prefixes are:

        - '_test_' for non GUI tests (which may optionally need a running
          QCoreApplication to handle events).

        - '_gui_test_' for GUI tests (which require a running QApplication).

    """
    pymedinria_root = pymedinria.__path__[0]
    module_prefix = f'_{"gui_" if gui else ""}test_'
    test_module_paths = list(Path(pymedinria_root).glob(f'**/{module_prefix}*.py'))
    modules = []
    
    for module_path in test_module_paths:
        relative_path = module_path.relative_to(Path(pymedinria_root).parent)
        module_file = relative_path.parts[-1]
        full_module_name = '.'.join(relative_path.parts)[:-3]
        if module_file.startswith(module_prefix):
            modules.append(full_module_name)

    return modules
