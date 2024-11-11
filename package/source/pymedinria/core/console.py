# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import builtins
import code
import sys
import threading

from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Object, Slot, Signal
else:
    from PySide6.QtCore import QObject, Slot, Signal


class Console(QObject):
    """Interactive console for the Python intepreter.

    This class is a wrapper over the code module's InteractiveConsole class. It
    adds a prompt, a custom welcome message and a history of previously pushed
    expressions, and it modifies some of the builtin functions that can cause
    issues outside the terminal command line environment.
    """

    WELCOME_TEXT = f'Python {sys.version} on {sys.platform}\n{config.application_name()} {config.application_version()}\n'

    run_ended = Signal(Exception)

    _running_instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lock = threading.RLock()
        self._thread = None
        self._init_prompt()
        self._init_history()

    def _init_prompt(self):
        try:
            self._ps1 = sys.ps1
        except AttributeError:
            self._ps1 = ">>> "
        try:
            self._ps2 = sys.ps2
        except AttributeError:
            self._ps2 = "... "
        self._prompt = self._ps1

    def _init_history(self):
        self._history = [""]
        self._history_index = 0

    def is_running(self):
        return self._running_instance is self

    def run(self, *, globals={}, command_line_thread=None):
        """Run the console.

        The 'globals' dict, if provided, will be merged into the __main__ dict,
        allowing the symbols it contains to be accessible within the console.

        The 'command_line_thread' should be the thread from which the console
        instance will be used. If not given, a default thread will be created
        using the builtin 'input' function to read commands (this is suitable
        when running in non-GUI mode only).

        Only one console may be running at a given time.

        """
        with self._lock:
            cls = type(self)
            if cls._running_instance:
                raise RuntimeError("A console is already running.")
            cls._running_instance = self

            self._command_line_thread = command_line_thread
            self._setup_internal_console(globals)
            self._setup_printing()

            sys.stdout.write(f'{self.WELCOME_TEXT}')

            if not self._command_line_thread:
                self._run_command_line_thread()

    def _setup_internal_console(self, globals):
        main_scope = vars(sys.modules['__main__'])
        main_scope.update(globals)
        self._console = code.InteractiveConsole(locals=main_scope)

    def _setup_printing(self):
        if not hasattr(builtins, '_print'):
            builtins._print = print
        builtins.print = self.print

    def _run_command_line_thread(self):
        self._command_line_thread = threading.Thread(
            target=self._command_line_loop,
            name="Console command line"
        )
        self._command_line_thread.start()

    def _command_line_loop(self):
        try:
            while True:
                line = input(self.prompt())
                self.push(line)
        except Exception as e:
            self.end_run(exception=e)
        except SystemExit:
            self.end_run()

    def end_run(self, *, exception=None):
        """Stop a running console.
        """
        with self._lock:
            self._console = None
            builtins.print = builtins._print
            type(self)._running_instance = None
            self._command_line_thread = None
            self.run_ended.emit(exception)

    @Slot(str)
    def print(self, object='', sep='', end='\n', file=None, flush=False):
        """Custom print function for running console.

        """
        with self._lock:
            thread = threading.current_thread()
            if thread is not self._command_line_thread:
                object = f'\n{object}{end}{self.prompt()}'
                end = ''
            builtins._print(object, sep=sep, end=end, file=file or sys.stdout, flush=flush)

    @Slot(str)
    def push(self, line):
        """Push a line of text to the console.

        If the accumulated lines form a complete expression it will be
        evaluated by the interpreter within the __main__ context.

        """
        with self._lock:
            self._history_index = len(self._history) - 1
            self._history[self._history_index] = line

            if line.strip():
                self._history.append("")
                self._history_index += 1

            more = self._console.push(line)

            if more:
                self._prompt = self._ps2
            else:
                self._prompt = self._ps1

    @Slot()
    def reset_input(self):
        """Reset the current stack of lines.

        """
        with self._lock:
            self._console.resetbuffer()

    def prompt(self):
        """The current prompt.

        The prompt for a new expression is '>>>'. The prompt for a
        multiline expression (after the first line) is '...'.

        """
        with self._lock:
            return self._prompt

    def current_history_entry(self):
        with self._lock:
            return self._history[self._history_index]

    @Slot()
    def move_up_history(self):
        with self._lock:
            self._history_index = max(self._history_index - 1, 0)

    @Slot()
    def move_down_history(self):
        with self._lock:
            self._history_index = min(self._history_index + 1, len(self._history) - 1)
