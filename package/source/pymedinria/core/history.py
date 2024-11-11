# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import os

from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import QObject, QStandardPaths, Signal, Slot
else:
    from PySide6.QtCore import QObject, QStandardPaths, Signal, Slot


class CommandLineHistory(QObject):

    MAX_NUMBER_OF_ENTRIES = 1000
    MAX_NUMBER_OF_FILE_ENTRIES = 100
    
    FILE_NAME = f'{config.application_name()}.clhistory'

    current_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._entries = []
        self._index = 0
        self._file = self._get_file()
        self._load_entries()

    def _init_file(self):
        file = QStandardPaths.locate(QStandardPaths.AppDataLocation, self.FILE_NAME)
        if not file:
            file_root = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
            file = os.path.join(file_root, self.FILE_NAME)
        return file

    def _load_entries(self):
        with open(self._file, encoding='utf8') as f:
            self._entries = f.readlines()

    @Slot(str)
    def push(self, entry=""):
        with self._lock:
            if entry.strip():
                self._entries.append(entry)
            self._index = len(self._entries)
            self._notify_changed()

    def get(self):
        with self._lock:
            if self._index < len(self._entries):
                return self._entries[self._index]
            else:
                return ""

    @Slot()
    def move_up(self):
        with self._lock:
            self._index = max(self._index - 1, 0)
            self._notify_changed()

    @Slot()
    def move_down(self):
        with self._lock:
            self._index = min(self._index + 1, len(self._history))
            self._notify_changed()

    def _notify_changed(self):
        self.current_changed.emit(self.get())
