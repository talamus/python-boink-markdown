from logging import getLogger
from typing import Any
from boink.boink.types_and_exceptions import *
from boink.boink.config_and_settings import *
from boink.boink.get_content_files import get_content_files_to_be_published


class Result:
    pass


def boink(content_paths: Optional[list[Path]] = None, cfg: Optional[Config] = None) -> Result:
    """### Main interface.
    * `content_paths`: List of directories or markdown files to be processed.
                       Directories will be recursively scanned.
    * `cfg`: Optional configuration. See `config.py` for details.
    """
    log = getLogger(__name__)

    content_paths = content_paths or []
    cfg = DEFAULT_CONFIG | (cfg or {})
    if "content_paths" in cfg:
        content_paths = content_paths + cfg["content_paths"]
    cfg["content_paths"] = content_paths

    log.debug("Configuration", extra={"cfg": cfg})
    log.debug("Content paths", extra={"content_paths": content_paths})

    content = get_content_files_to_be_published(content_paths)

    log.debug("Content to be published", extra={"content": content})

    if not content_paths:
        raise NothingToDo("No content paths provided")

    return Result()
