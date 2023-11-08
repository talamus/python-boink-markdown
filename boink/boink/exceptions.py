class BoinkException(Exception):
    """Base exception (with an optional help text field)"""

    def __init__(self, message: str, help: str = None) -> None:
        super().__init__(message)
        if help:
            self.help = help

class NothingToDo(BoinkException):
    """Raised when there is nothing to do (f.ex. no content paths provided)"""
