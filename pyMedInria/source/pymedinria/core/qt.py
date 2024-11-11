# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import importlib
import inspect

from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication

    import PySide2
    import pkgutil

    def _find_all_qt_modules():
        return [module.name for module in pkgutil.iter_modules(PySide2.__path__)]
else:
    from PySide6 import _find_all_qt_modules
    from PySide6.QtCore import QCoreApplication


_classes = {}
_application = None


def get_class(name):
    try:
        return _classes[name]
    except KeyError:
        return _find_class(name)


def _find_class(name):
    pyside_version = config.pyside_version()
    for module_name in _find_all_qt_modules():
        module = importlib.import_module(f'PySide{pyside_version}.{module_name}')
        try:
            cls = getattr(module, name)
            _classes[name] = cls
            return cls
        except AttributeError:
            pass
    raise NameError(f'Class not found in PySide{pyside_version}: {name}')


def set_application(app):
    global _application
    _application = app
    QCoreApplication.instance = lambda : _application
