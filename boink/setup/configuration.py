import os
import sys
import yaml
from collections import UserDict
from typing import Any
from .default_configuration import DEFAULT_CONFIGURATION

_configuration = None  # The current configuration


class DotDict(UserDict):
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


def _die(message: str, code: int = 99):
    """Die with an error message."""
    print(message, file=sys.stderr)
    sys.exit(code)


def setupConfiguration(
    defaults: dict[str, Any] = {}, overrides: dict[str, Any] = {}
) -> None:
    """Build application configuration."""

    global _configuration
    defaults = DEFAULT_CONFIGURATION | defaults
    config = {}

    config_file = None
    if "config_file" in overrides:
        config_file = overrides["config_file"]
    elif "config_file" in defaults:
        config_file = defaults["config_file"]

    if config_file:
        try:
            with open(config_file) as stream:
                config = yaml.safe_load(stream)
        except OSError as error:
            if "config_file" in overrides:
                _die(f"{config_file} is not readable YAML file: {error}")
        except yaml.scanner.ScannerError:
            _die(f"{config_file} is not a YAML file")
        if not isinstance(config, dict):
            _die(f"{config_file} is not a YAML dictionary")

    config = defaults | config
    config = config | overrides
    _configuration = DotDict(config)


def getConfiguration(*argv) -> DotDict:
    """Get configuration for the application. (Build it if needed.)"""
    global _configuration
    if not _configuration:
        setupConfiguration(*argv)
    return _configuration
