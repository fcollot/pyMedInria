# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


from . import config


if config.pyside_version() == 2:
    from PySide2.QtCore import QSettings
else:
    from PySide6.QtCore import QSettings


class Settings():
    """ Handle persistent application settings.

    Stored values will persist between application runs.

    """

    def __init__(self):
        self._settings = QSettings('liryc', 'pymedinria')

    def value(self, name, default_value=None):
        return self._settings.value(name, default_value)

    def set_value(self, name, value):
        self._settings.setValue(name, value)
