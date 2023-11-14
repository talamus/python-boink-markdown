from typing import TypeAlias, Optional, Any

Config: TypeAlias = dict[str, Any]
Path: TypeAlias = str  # May be a file or a directory
DirName: TypeAlias = str
FileName: TypeAlias = str


class BoinkException(Exception):
    """Base exception (with an optional help text field)"""

    def __init__(self, message: str, help: Optional[str] = None) -> None:
        super().__init__(message)
        help = help or "Re-run with -h to see a simple usage."
        self.help = help


class NothingToDo(BoinkException):
    """Raised when there is nothing to do (f.ex. no content paths provided)"""

class SeekingContentFiles(BoinkException):
    """Raised when there is a problem while scanning the `content_path` list."""
