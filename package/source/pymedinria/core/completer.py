# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import re
import rlcompleter

from . import config

if config.pyside_version() == 2:
    from PySide2.QtCore import Object, Slot, Signal
else:
    from PySide6.QtCore import QObject, Slot, Signal


class Completer(QObject, rlcompleter.Completer):
    """Code completion for the command line interpreter.

    Based on Python's rlcompleter module, this class is able to complete the
    last token of unfinished statements, and uses signals to send the
    completions.

    """

    successful_completion = Signal(str)
    possible_completions = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(str)
    def complete(self, text):
        """Complete the last symbol of a Python statement.

        Two different Qt signals are used to indicate the completions:

            successful_completion: Triggered when only one possible completion
                                   is found. Returns the statement with the
                                   completion appended to it.

            possible_completions:  Triggered when multiple possible completions
                                   are found. Returns the list of suffixes that
                                   would complete the last symbol of the
                                   statement.

        """
        if text:
            match = re.search("[^\\( ]*$", text)

            try:
                completable_part = match.group(0)
            except IndexError:
                return

            completions = self.find_completions(completable_part)

            if completions:
                if len(completions) == 1:
                    completion = completions[0]
                    self.successful_completion.emit(text[:match.start(0)] + completion)
                else:
                    self.possible_completions.emit(completions)

    def find_completions(self, text):
        """The list of completions for a Python symbol. 

        (See the documentation of rlcompleter for more details)
        """
        state = 0
        completions = []

        while True:
            completion = super().complete(text, state)
            state += 1
            if completion:
                completions.append(completion)
            else:
                break

        return completions
