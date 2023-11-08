from logging import getLogger
from typing import Any
from boink.boink import *


class Result:
    pass


def boink(content_paths: list[str] = None, cfg: dict[str, Any] = None) -> Result:
    """Main interface.
    * `content_paths`: List of directories or markdown files to be processed.
                       Directories will be recursively scanned.
    * `cfg`: Optional configuration. See `config.py` for details.
    """
    log = getLogger(__name__)

    content_paths = content_paths or []
    cfg = Cfg(DEFAULT_CONFIG | (cfg or {}))
    if cfg.content_paths:
        content_paths = content_paths + cfg.content_paths
    cfg["content_paths"] = content_paths

    log.debug("Configuration", extra={"cfg": cfg})
    log.debug("Content paths", extra={"content_paths": content_paths})

    if not content_paths:
        raise NothingToDo("No content paths provided", "Re-run with -h to see a simple usage.")

    return Result()
