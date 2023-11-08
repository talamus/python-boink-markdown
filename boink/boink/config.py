from typing import Any
from collections import UserDict


DEFAULT_CONFIG = {
    "dryrun": False,
}

class Cfg(UserDict):
    """
    Dictionary that allows the object style dot format referencing when reading values.
    (Makes the code cleaner when using the configuration.)
    """

    def __getattr__(self, name: str) -> Any:
        """
        Return property as an attribute, or `None` if attribute does not exist.
        """
        try:
            return self.data[name]
        except KeyError:
            return None
