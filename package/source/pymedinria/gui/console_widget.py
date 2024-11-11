# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import sys
import threading

from pymedinria.core import completer, config, console
from .line_edit import LineEdit

if config.pyside_version() == 2:
    from PySide2.QtCore import QCoreApplication, QEventLoop, Qt, Signal, Slot
    from PySide2.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
else:
    from PySide6.QtCore import QCoreApplication, QEventLoop, Qt, Signal, Slot
    from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


class ConsoleWidget(QWidget):
    """Widget to display console input and output.

    In addition to the base console, this widget adds code completion using the
    tab key.

    """

    run_ended = Signal(Exception)

    def __init__(self, parent=None, *, size=(800, 600), title=f'{config.application_name()} Python console'):
        super().__init__(parent)
        self._init_window(size, title)
        self._init_output_widget()
        self._init_console()
        self._init_input_widget()
        self._init_fonts()
        self._init_code_completion()
  
    def _init_window(self, size, title):
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.setLayout(layout)
        self.resize(*size)

    def _init_output_widget(self):
        self._output_widget = QLabel()
        self._output_widget.setAlignment(Qt.AlignBottom)
        self._output_widget.setWordWrap(True)
        self._output_widget.setTextFormat(Qt.PlainText)
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidget(self._output_widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.horizontalScrollBar().setEnabled(False)
        scroll_bar = self._scroll_area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda _, max : scroll_bar.setValue(max))
        self.layout().addWidget(self._scroll_area)

    def _init_console(self):
        self._console = console.Console()

    def _init_input_widget(self):
        self._input_widget = LineEdit()
        self.layout().addWidget(self._input_widget)
        self.setFocusProxy(self._input_widget)
        self._update_input_widget()
        self._input_widget.line.connect(self._handle_input)
        self._input_widget.up.connect(self._console.move_up_history)
        self._input_widget.up.connect(self._update_input_widget)
        self._input_widget.down.connect(self._console.move_down_history)
        self._input_widget.down.connect(self._update_input_widget)

    def _init_fonts(self):
        font = self._output_widget.font()
        font.setFamily("Courier")
        self._output_widget.setFont(font)
        self._input_widget.setFont(font)
        self._input_widget.setFrame(False)

    def _init_code_completion(self):
        self._completer = completer.Completer()
        self._input_widget.tab.connect(self._completer.complete)
        self._completer.possible_completions.connect(self._show_possible_completions)
        self._completer.successful_completion.connect(self._input_widget.setText)

    def run(self, *, globals={}):
        self._setup_output_streams()
        self._console.run_ended.connect(self.run_ended)
        self._console.run(globals=globals, command_line_thread=threading.main_thread())

    def _setup_output_streams(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self
        sys.stderr = _StreamWrapper((sys.stderr, self))

    def end_run(self, *, exception=None):
        self._restore_output_streams()
        self._console.end_run(exception=exception)

    @Slot()
    def _restore_output_streams(self):
        sys.stdout = self._stdout
        sys.stderr = self._stderr
  
    @Slot(str, str)
    def _handle_input(self, text, prompt):
        print(f'{prompt}{text}')
        self._output_widget.repaint()
        self._input_widget.set_prompt()
        self._input_widget.setText()
        self._input_widget.repaint()
        QCoreApplication.instance().processEvents(QEventLoop.ExcludeUserInputEvents)

        try:
            self._console.push(text)
        except Exception as e:
            self.end_run(exception=e)
        except SystemExit:
            self.end_run()

        self._update_input_widget()

    def _update_input_widget(self):
        self._input_widget.set_prompt(self._console.prompt())
        self._input_widget.setText(self._console.current_history_entry())

    def write(self, text):
        self._output_widget.setText(f'{self._output_widget.text()}{text}')

    def flush(self):
        pass

    def showEvent(self, event):
        self.setFocus()

    @Slot(list)
    def _show_possible_completions(self, completions):
        print(f'{self._input_widget.prompt()}{self._input_widget.text()}')
        for i in range(len(completions)):
            sys.stdout.write(f'{completions[i]}\t\t')
        sys.stdout.write('\n')


class _StreamWrapper():
    """Combine multiple streams into one.

    Use for printing on both the console and the standard output.
    (This is currently used for the error stream only)

    """

    def __init__(self, streams):
        self._streams = streams

    def write(self, text):
        for stream in self._streams:
            stream.write(text)

    def flush(self):
        for stream in self._streams:
            stream.flush()
